# Giỏi Toán – gioitoan.com.vn

Luyện toán lớp 1–12: đề luyện, đề mô phỏng kỳ thi thật, mục HOT đề thi nóng hổi.

| Thư mục | Nội dung |
|---|---|
| `public/` | Toàn bộ website tĩnh. Cloudflare Pages đăng thư mục này (Build output directory = `public`, không cần lệnh build). |
| `public/auto/` | Đề do 2 tác vụ tự động soạn: `b<N>.js` (đề luyện), `m<N>.js` (mô phỏng đề thật), `manifest.js` (danh sách), `seen.txt` (mã chống trùng). |
| `public/data/` | Đề có sẵn, tải khi học sinh mở đề. |
| `gen/` | Bộ sinh đề tự động (Python). |
| `tools/seo_build.py` | Sinh trang đích SEO, sitemap.xml, robots.txt, thẻ meta. Đổi `SITE` khi gắn tên miền rồi chạy lại. |
| `backend/` | Supabase (SQL `migrations/0001–0003`, hàm máy chủ thanh toán/bảo vệ đề) và hướng dẫn triển khai. |

Mỗi lần đẩy lên nhánh `main`, Cloudflare Pages tự đăng lại web sau khoảng 1 phút.
