// POST { plan_id }  (cần đăng nhập)  ->  { order_code, amount, qr_code, checkout_url }
import { admin, withCors, env, getUser, hmacHex, json, paymentRequestString, payos } from "../_shared/payos.ts";

Deno.serve(withCors(async (req) => {
  try {
    const user = await getUser(req);
    if (!user) return json({ error: "Bạn cần đăng nhập." }, 401);

    const { plan_id } = await req.json();
    const db = admin();
    const { data: plan } = await db.from("plans").select("*").eq("id", plan_id).eq("active", true).single();
    if (!plan) return json({ error: "Gói không tồn tại." }, 400);

    // Dùng lại đơn đang chờ cùng gói trong 15 phút, tránh tạo nhiều mã QR
    const since = new Date(Date.now() - 15 * 60 * 1000).toISOString();
    const { data: open } = await db.from("orders").select("*")
      .eq("user_id", user.id).eq("plan_id", plan.id).eq("status", "pending").gte("created_at", since)
      .order("created_at", { ascending: false }).limit(1).maybeSingle();
    if (open?.qr_code) return json({ order_code: open.order_code, amount: open.amount, qr_code: open.qr_code, checkout_url: open.checkout_url });

    // Mã đơn: số nguyên duy nhất (giây hiện tại * 1000 + 3 số ngẫu nhiên)
    const orderCode = Math.floor(Date.now() / 1000) * 1000 + Math.floor(Math.random() * 1000);
    const site = env("SITE_URL").replace(/\/$/, "");
    const req2 = {
      orderCode,
      amount: plan.price_vnd,
      description: `GIOITOAN ${orderCode}`.slice(0, 25),   // ngân hàng giới hạn độ dài nội dung
      returnUrl: `${site}/#tai-khoan`,
      cancelUrl: `${site}/#tai-khoan`,
    };
    const signature = await hmacHex(env("PAYOS_CHECKSUM_KEY"), paymentRequestString(req2));
    const link = await payos("/v2/payment-requests", {
      method: "POST",
      body: JSON.stringify({ ...req2, items: [{ name: plan.name, quantity: 1, price: plan.price_vnd }], signature }),
    });

    const { error } = await db.from("orders").insert({
      order_code: orderCode, user_id: user.id, plan_id: plan.id, amount: plan.price_vnd,
      payos_link_id: link.paymentLinkId, checkout_url: link.checkoutUrl, qr_code: link.qrCode,
    });
    if (error) throw error;
    return json({ order_code: orderCode, amount: plan.price_vnd, qr_code: link.qrCode, checkout_url: link.checkoutUrl });
  } catch (e) {
    console.error(e);
    return json({ error: "Không tạo được đơn thanh toán. Vui lòng thử lại." }, 500);
  }
}));
