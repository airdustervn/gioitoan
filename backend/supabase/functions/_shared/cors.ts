// CORS chặt: chỉ các miền khai báo trong SITE_ORIGIN (phân tách bằng dấu phẩy) được gọi hàm từ trình duyệt.
// Thiếu SITE_ORIGIN => không trả header cho phép nào (trình duyệt chặn), thay vì mở cho mọi trang như "*".
const allowed = (Deno.env.get("SITE_ORIGIN") ?? "").split(",").map((s) => s.trim().replace(/\/$/, "")).filter(Boolean);
if (!allowed.length) console.error("SITE_ORIGIN chưa đặt: mọi yêu cầu từ trình duyệt sẽ bị chặn CORS.");

export function corsHeaders(req: Request): Record<string, string> {
  const origin = req.headers.get("Origin") ?? "";
  const h: Record<string, string> = {
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
  if (origin && allowed.includes(origin)) h["Access-Control-Allow-Origin"] = origin;
  return h;
}

// Bọc handler: trả lời preflight, gắn header CORS cho mọi phản hồi, chặn yêu cầu trình duyệt từ miền lạ.
export function withCors(handler: (req: Request) => Promise<Response>) {
  return async (req: Request) => {
    const h = corsHeaders(req);
    const origin = req.headers.get("Origin");
    if (req.method === "OPTIONS") return new Response(null, { status: h["Access-Control-Allow-Origin"] ? 204 : 403, headers: h });
    if (origin && !h["Access-Control-Allow-Origin"]) return new Response("origin not allowed", { status: 403, headers: h });
    const res = await handler(req);
    const out = new Headers(res.headers);
    for (const [k, v] of Object.entries(h)) out.set(k, v);
    return new Response(res.body, { status: res.status, headers: out });
  };
}
