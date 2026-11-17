// POST { order_code } (cần đăng nhập) -> { status }
// Trang web gọi định kỳ khi đang hiện mã QR. Nếu webhook bị lỡ, hàm này hỏi lại payOS và tự kích hoạt.
import { admin, withCors, getUser, json, payos } from "../_shared/payos.ts";

Deno.serve(withCors(async (req) => {
  try {
    const user = await getUser(req);
    if (!user) return json({ error: "Bạn cần đăng nhập." }, 401);
    const { order_code } = await req.json();
    const db = admin();
    const { data: order } = await db.from("orders").select("*").eq("order_code", order_code).eq("user_id", user.id).single();
    if (!order) return json({ error: "Không tìm thấy đơn." }, 404);
    if (order.status !== "pending") return json({ status: order.status });

    const info = await payos(`/v2/payment-requests/${order_code}`);
    if (info.status === "PAID") {
      await db.rpc("activate_order", { p_order_code: order.order_code, p_amount: info.amountPaid ?? info.amount, p_raw: info });
      return json({ status: "paid" });
    }
    if (info.status === "CANCELLED" || info.status === "EXPIRED") {
      await db.from("orders").update({ status: "cancelled" }).eq("id", order.id);
      return json({ status: "cancelled" });
    }
    return json({ status: "pending" });
  } catch (e) {
    console.error(e);
    return json({ status: "pending" });
  }
}));
