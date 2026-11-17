// payOS gọi vào đây khi có tiền vào. Triển khai với --no-verify-jwt.
import { admin, env, hmacHex, webhookDataString } from "../_shared/payos.ts";

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("ok");
  let body: any;
  try { body = await req.json(); } catch { return new Response("bad json", { status: 400 }); }

  const data = body?.data;
  if (!data || !body.signature) return new Response("missing data", { status: 400 });

  const expected = await hmacHex(env("PAYOS_CHECKSUM_KEY"), webhookDataString(data));
  if (expected !== String(body.signature).toLowerCase()) {
    console.warn("Sai chữ ký webhook", data?.orderCode);
    return new Response("invalid signature", { status: 401 });
  }

  // Chỉ kích hoạt khi giao dịch thành công
  if (body.code === "00" && data.code === "00") {
    const { data: result, error } = await admin().rpc("activate_order", {
      p_order_code: data.orderCode, p_amount: data.amount, p_raw: body,
    });
    if (error) { console.error(error); return new Response("db error", { status: 500 }); }
    console.log("Đơn", data.orderCode, result);   // activated | already_paid | not_found (webhook thử) | amount_mismatch
  }
  return new Response(JSON.stringify({ success: true }), { headers: { "Content-Type": "application/json" } });
});
