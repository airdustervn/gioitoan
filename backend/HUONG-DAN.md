# Giỏi Toán (gioitoan.com.vn) – Hướng dẫn bật tài khoản học sinh và thu phí

Bộ mã này gồm 3 phần:

| Thư mục | Là gì |
|---|---|
| `site/index.html` | Toàn bộ trang web (1 file). Đưa lên hosting là chạy. |
| `supabase/migrations/0001_init.sql` | Cơ sở dữ liệu: tài khoản, gói, đơn hàng, lượt miễn phí, bảo mật. |
| `supabase/migrations/0002_protect_papers.sql` | Bảng đề `papers` (khóa kín, chỉ máy chủ đọc) và nhật ký mở đề. |
| `supabase/functions/` | 4 hàm máy chủ: tạo mã QR (`create-order`), nhận báo tiền vào (`payos-webhook`), kiểm tra đơn (`check-order`), trả đề sau khi kiểm tra lượt (`get-paper`). |
| `tools/` | `vendor.sh` (tải supabase-js về site + mã SRI), `build_prod.py` (tách đề khỏi site, bật bảo vệ, thêm CSP), `upload_papers.py` (đẩy đề lên Supabase). |

**Cơ chế:**

- Mỗi học sinh có một tài khoản (tên đăng nhập + mật khẩu).
- Tài khoản miễn phí được **10 câu luyện tập và 1 đề thi mỗi ngày**.
- Mua gói bằng **chuyển khoản VietQR qua payOS**. Tiền vào là payOS báo về máy chủ, máy chủ kiểm tra chữ ký rồi tự cộng ngày sử dụng cho học sinh.

Khi `SUPABASE_URL` trong file còn để trống, trang chạy ở **chế độ dùng thử**: không cần đăng nhập, không giới hạn.

---

## Bước 1 – Tạo dự án Supabase (miễn phí)
1. Vào https://supabase.com, đăng ký và bấm **New project**. Chọn vùng **Southeast Asia (Singapore)**.
2. Mở **SQL Editor > New query**, dán toàn bộ nội dung `supabase/migrations/0001_init.sql` rồi bấm **Run**. Làm tiếp như vậy với `0002_protect_papers.sql`.
3. Vào **Authentication > Sign In / Providers > Email**:
   - **Tắt** "Confirm email". Học sinh đăng nhập bằng tên đăng nhập; hệ thống tự đổi thành địa chỉ dạng `tendangnhap@hs.gioitoan.com.vn` nên không có email thật để xác nhận.
4. Vào **Project Settings > API**, chép 2 giá trị: **Project URL** và khóa **anon public**.

## Bước 2 – Đăng ký payOS
1. Vào https://my.payos.vn, đăng ký và tạo **Kênh thanh toán**, liên kết tài khoản ngân hàng nhận tiền.
2. Chép 3 khóa của kênh: **Client ID**, **API Key**, **Checksum Key**.
3. Kiểm tra điều kiện đăng ký của payOS (cá nhân hay hộ kinh doanh/doanh nghiệp) và quy định về tài khoản ngân hàng dùng cho kinh doanh trước khi nhận tiền thật.

## Bước 3 – Đưa 3 hàm máy chủ lên Supabase
Làm trên máy tính của bạn (cần cài Node.js):
```bash
npm install -g supabase
supabase login
cd toan-tu-duy-app
supabase link --project-ref <mã-dự-án>      # mã nằm trong URL dự án: https://<mã-dự-án>.supabase.co

supabase secrets set \
  PAYOS_CLIENT_ID=xxx PAYOS_API_KEY=xxx PAYOS_CHECKSUM_KEY=xxx \
  SITE_URL=https://gioitoan.com.vn SITE_ORIGIN=https://gioitoan.com.vn

supabase functions deploy create-order
supabase functions deploy check-order
supabase functions deploy payos-webhook --no-verify-jwt
supabase functions deploy get-paper
```
`SITE_ORIGIN` là **bắt buộc**: chỉ những miền ghi ở đây (nhiều miền thì cách nhau dấu phẩy, ví dụ `https://gioitoan.com.vn,https://www.gioitoan.com.vn`) mới gọi được các hàm từ trình duyệt. Thiếu biến này thì mọi yêu cầu bị chặn. Tùy chọn: `MAX_PAPERS_PER_DAY` (mặc định 40) là số đề **mới** tối đa một tài khoản mở trong 24 giờ, để chặn tải đề hàng loạt.
`SUPABASE_URL` và `SUPABASE_SERVICE_ROLE_KEY` được Supabase tự cấp cho các hàm, không cần đặt.

## Bước 4 – Khai báo webhook trong payOS
Trong kênh thanh toán payOS, mục **Webhook URL**, điền:
```
https://<mã-dự-án>.supabase.co/functions/v1/payos-webhook
```
rồi bấm xác nhận. payOS sẽ gửi một đơn thử; hàm trả về thành công và bỏ qua đơn thử vì không có trong cơ sở dữ liệu.

## Bước 5 – Tạo bản chạy thật (đề nằm trên máy chủ) và đưa lên mạng
Làm trên máy của bạn, trong thư mục chứa bản site đầy đủ (`index.html`, `data/`, `auto/`, `lib/`):
```bash
# 1) Tự lưu thư viện supabase-js trên site, không phụ thuộc CDN (in ra mã SRI để đối chiếu)
bash tools/vendor.sh site

# 2) Tách toàn bộ đề + đáp án khỏi site, điền cấu hình, bật PROTECT_PAPERS và Content-Security-Policy
python3 tools/build_prod.py site out --url https://<mã-dự-án>.supabase.co --anon <khóa-anon-public> \
        --free S_x_AMC8,S_dh_y0          # (tùy chọn) vài đề cho xem thử không trừ lượt

# 3) Đẩy đề lên bảng papers (khóa service role chỉ dùng trên máy bạn)
SUPABASE_URL=https://<mã-dự-án>.supabase.co SUPABASE_SERVICE_ROLE_KEY=<service-role> \
  python3 tools/upload_papers.py out/papers.jsonl
```
Đưa **thư mục `out/dist`** lên hosting tĩnh (Cloudflare Pages, Netlify…) và gắn tên miền. Thư mục này không còn file đề nào; trang chỉ nhận đề từ hàm `get-paper` sau khi:
- đã đăng nhập, và
- là gói trả phí, hoặc còn lượt thi miễn phí hôm nay (mở lại cùng một đề trong 24 giờ không bị trừ thêm).

Mỗi lần tác vụ tự động thêm đề mới, chạy lại bước 2 và 3 (lệnh 3 ghi đè an toàn theo `id`).

Nếu muốn dùng supabase-js từ CDN thay vì tự lưu: thêm `--supabase-js <URL CDN cố định phiên bản> --sri <mã sha384 do vendor.sh in ra>`. Trang sẽ từ chối chạy thư viện CDN nếu thiếu mã SRI.

Khóa **anon** được phép nằm công khai trong trang. **Tuyệt đối không** đưa khóa `service_role` hay khóa payOS vào file trang.

## Bước 6 – Chạy thử bằng tiền thật nhỏ
Trong **SQL Editor** chạy:
```sql
insert into public.plans (id, name, price_vnd, days, sort) values ('thu', 'Gói thử', 2000, 1, 0);
```
Tạo một tài khoản học sinh, mua "Gói thử", chuyển 2.000đ. Trong vài giây trang sẽ báo "Thanh toán thành công" và hiện nhãn **PRO**. Thử xong thì ẩn gói:
```sql
update public.plans set active = false where id = 'thu';
```

---

## Quản trị hằng ngày
Dùng ngay giao diện Supabase, không cần trang quản trị riêng.

| Việc | Cách làm |
|---|---|
| Đổi giá, thêm gói | **Table Editor > plans**: sửa `price_vnd`, `days`; `active = false` để ẩn gói |
| Đổi giới hạn miễn phí | Sửa số `10, 1` trong hàm `free_limits()` rồi chạy lại đoạn đó |
| Tặng hoặc gia hạn gói tay | `update public.profiles set premium_until = greatest(coalesce(premium_until, now()), now()) + interval '30 days' where username = 'ten_dang_nhap';` |
| Xem doanh thu | `select date_trunc('month', paid_at) thang, count(*) so_don, sum(amount) doanh_thu from public.orders where status = 'paid' group by 1 order by 1 desc;` |
| Xem đơn, học sinh | **Table Editor > orders / profiles** |
| Học sinh quên mật khẩu | **Authentication > Users**, chọn tài khoản rồi đặt lại mật khẩu, hoặc xóa và cho tạo lại |

## Bảo mật đã có
- Đề và đáp án chỉ nằm trong bảng `papers` (không có quyền đọc công khai); hàm `get-paper` trừ lượt rồi mới trả đề, giới hạn số đề mới mỗi ngày.
- CORS chỉ cho phép các miền trong `SITE_ORIGIN`; trang có Content-Security-Policy, không tải script ngoài nào thiếu mã SRI; mã QR tạo ngay trong trang, không dùng thư viện CDN.
- Đề do tác vụ tự động soạn được lọc thẻ HTML trước khi hiển thị (chống chèn mã).
- Học sinh chỉ xem được hồ sơ, đơn hàng và lượt dùng **của chính mình**. Cơ chế RLS đã được kiểm thử.
- Học sinh **không thể tự sửa** hạn gói (`premium_until`) và không thể tự tạo đơn đã thanh toán. Chỉ hàm máy chủ có quyền làm hai việc này.
- Webhook kiểm tra **chữ ký HMAC-SHA256** bằng Checksum Key, đúng cách payOS mô tả.
- Mỗi đơn chỉ được cộng ngày **một lần**, kể cả khi payOS gửi webhook nhiều lần.
- Đơn chuyển thiếu tiền sẽ không được kích hoạt.

## Giới hạn hiện tại (nên làm ở giai đoạn sau)
1. **Đề thi đã khóa trên máy chủ** (bước 5). Riêng **ngân hàng câu luyện tập hằng ngày** và các đề sinh ngẫu nhiên từ ngân hàng đó (vào 6 tổng hợp, Kangaroo, đề nhanh) vẫn nằm trong trang và được tính lượt trên trình duyệt. Một học sinh đã được cấp đề thì xem được đáp án của đề đó (để chấm điểm ngay trên máy).
2. **Chưa có email phụ huynh** nên học sinh không tự lấy lại mật khẩu được. Có thể thêm ô email phụ huynh (không bắt buộc) khi đăng ký.
3. **Tiến độ làm bài** (số sao, câu đã làm) vẫn lưu trên từng máy, chưa đồng bộ lên tài khoản.
4. Trước khi thu tiền thật, cần lo phần pháp lý: đăng ký kinh doanh và thuế, chính sách bảo vệ dữ liệu cá nhân của trẻ em, điều khoản sử dụng và hoàn tiền.
