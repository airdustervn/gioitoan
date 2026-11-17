// POST { id } (cần đăng nhập) -> { paper } hoặc { reason: "login" | "quota" | "limit" | "not_found" }
// Trả đề + đáp án chỉ khi: đề miễn phí, hoặc đã mở đề này trong 24 giờ, hoặc trừ được 1 lượt "exam"
// (gói trả phí thì consume luôn cho phép). Giới hạn số đề mới mỗi ngày để chặn tải hàng loạt.
import { createClient } from "npm:@supabase/supabase-js@2";
import { admin, env, getUser, json, withCors } from "../_shared/payos.ts";

const MAX_NEW_PER_DAY = Number(Deno.env.get("MAX_PAPERS_PER_DAY") ?? "40");

Deno.serve(withCors(async (req) => {
  if (req.method !== "POST") return json({ reason: "method" }, 405);
  try {
    const user = await getUser(req);
    if (!user) return json({ reason: "login" }, 401);
    const { id } = await req.json().catch(() => ({}));
    if (typeof id !== "string" || !/^[A-Za-z0-9_\-]{1,80}$/.test(id)) return json({ reason: "not_found" }, 400);

    const db = admin();
    const { data: paper } = await db.from("papers").select("id, free, data").eq("id", id).maybeSingle();
    if (!paper) return json({ reason: "not_found" }, 404);
    if (paper.free) return json({ paper: paper.data });

    const dayAgo = new Date(Date.now() - 24 * 3600 * 1000).toISOString();
    const { data: seen } = await db.from("paper_access").select("opened_at")
      .eq("user_id", user.id).eq("paper_id", id).gte("opened_at", dayAgo).maybeSingle();
    if (seen) return json({ paper: paper.data });

    const { count } = await db.from("paper_access").select("paper_id", { count: "exact", head: true })
      .eq("user_id", user.id).gte("opened_at", dayAgo);
    if ((count ?? 0) >= MAX_NEW_PER_DAY) return json({ reason: "limit" }, 429);

    // Trừ lượt bằng chính phiên của học sinh để hàm consume() nhận đúng auth.uid()
    const asUser = createClient(env("SUPABASE_URL"), env("SUPABASE_ANON_KEY"), {
      auth: { persistSession: false },
      global: { headers: { Authorization: req.headers.get("Authorization") ?? "" } },
    });
    const { data: c, error } = await asUser.rpc("consume", { kind: "exam" });
    if (error) throw error;
    if (!c?.allowed) return json({ reason: c?.reason === "login" ? "login" : "quota" }, 402);

    await db.from("paper_access").upsert({ user_id: user.id, paper_id: id, opened_at: new Date().toISOString() });
    return json({ paper: paper.data });
  } catch (e) {
    console.error(e);
    return json({ reason: "error" }, 500);
  }
}));
