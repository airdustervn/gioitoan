// Dùng chung cho các Edge Function: gọi API payOS và kiểm tra chữ ký.
// Tài liệu: https://payos.vn/docs/api/  và  https://payos.vn/docs/tich-hop-webhook/kiem-tra-du-lieu-voi-signature
import { createClient } from "npm:@supabase/supabase-js@2";
export { withCors } from "./cors.ts";

export const PAYOS_BASE = "https://api-merchant.payos.vn";
export const env = (k: string) => {
  const v = Deno.env.get(k);
  if (!v) throw new Error(`Thiếu biến môi trường ${k}`);
  return v;
};

export const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

// HMAC-SHA256, kết quả dạng hex chữ thường
export async function hmacHex(key: string, message: string): Promise<string> {
  const enc = new TextEncoder();
  const k = await crypto.subtle.importKey("raw", enc.encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", k, enc.encode(message));
  return Array.from(new Uint8Array(sig)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Chuỗi ký khi tạo link: các trường sắp xếp theo alphabet
export function paymentRequestString(d: { amount: number; cancelUrl: string; description: string; orderCode: number; returnUrl: string }) {
  return `amount=${d.amount}&cancelUrl=${d.cancelUrl}&description=${d.description}&orderCode=${d.orderCode}&returnUrl=${d.returnUrl}`;
}

// Chuỗi ký của webhook: toàn bộ object `data`, key sắp xếp alphabet, null/undefined -> chuỗi rỗng
export function webhookDataString(data: Record<string, unknown>) {
  return Object.keys(data).sort().map((key) => {
    let v = data[key];
    if (v === null || v === undefined || v === "null" || v === "undefined") v = "";
    else if (Array.isArray(v)) v = JSON.stringify(v.map((x) => (x && typeof x === "object" ? sortKeys(x as Record<string, unknown>) : x)));
    else if (typeof v === "object") v = JSON.stringify(sortKeys(v as Record<string, unknown>));
    return `${key}=${v}`;
  }).join("&");
}
function sortKeys(o: Record<string, unknown>) {
  return Object.keys(o).sort().reduce((a, k) => { a[k] = o[k]; return a; }, {} as Record<string, unknown>);
}

export async function payos(path: string, init: RequestInit = {}) {
  const res = await fetch(PAYOS_BASE + path, {
    ...init,
    headers: {
      "x-client-id": env("PAYOS_CLIENT_ID"),
      "x-api-key": env("PAYOS_API_KEY"),
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok || body.code !== "00") throw new Error(`payOS lỗi: ${body.code ?? res.status} ${body.desc ?? ""}`);
  return body.data;
}

// Client quyền quản trị (bỏ qua RLS) – chỉ dùng trong Edge Function
export const admin = () => createClient(env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });

// Lấy người dùng từ header Authorization (JWT của học sinh)
export async function getUser(req: Request) {
  const token = (req.headers.get("Authorization") ?? "").replace(/^Bearer\s+/i, "");
  if (!token) return null;
  const { data } = await admin().auth.getUser(token);
  return data.user ?? null;
}
