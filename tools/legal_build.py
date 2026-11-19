import html, os
PUB=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','public')
LOGO='''<svg class="mk" viewBox="0 0 100 100" aria-hidden="true"><rect x="4" y="4" width="44" height="44" rx="11" fill="#c8102e"/><rect x="52" y="4" width="44" height="44" rx="11" fill="#f2a900"/><rect x="4" y="52" width="44" height="44" rx="11" fill="#2f7fd8"/><rect x="52" y="52" width="44" height="44" rx="11" fill="#1c1a17"/><g stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none"><path d="M26 15v22M15 26h22"/><path d="M63 26h22" stroke="#1c1a17"/><path d="M18 66l16 16M34 66l-16 16"/><path d="M63 74h22"/></g><circle cx="74" cy="64.5" r="4" fill="#fff"/><circle cx="74" cy="83.5" r="4" fill="#fff"/></svg>'''
CSS='''*{box-sizing:border-box}body{margin:0;font-family:"Be Vietnam Pro",system-ui,sans-serif;color:#1c1a17;background:#fbf7ef;line-height:1.65}
a{color:#c8102e}header{background:#fff;border-bottom:1px solid #e7dcc7}.w{max-width:820px;margin:0 auto;padding:0 20px}
.top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0}.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:#1c1a17;font-weight:800;letter-spacing:.02em;font-size:1.2rem}
.brand em{font-style:normal;color:#c8102e}.mk{width:36px;height:36px}.back{font-weight:700;text-decoration:none}
main{padding:28px 0 40px}h1{font-size:clamp(1.6rem,4vw,2.2rem);line-height:1.2;margin:0 0 6px}.meta{color:#6f6758;margin:0 0 22px}
.card{background:#fff;border:1px solid #e7dcc7;border-radius:16px;padding:22px 24px;box-shadow:0 6px 18px rgba(28,26,23,.05)}
h2{font-size:1.15rem;margin:26px 0 8px}h2:first-child{margin-top:0}ul{padding-left:22px}li{margin:4px 0}
.toc{columns:2;column-gap:28px;margin:0 0 4px;padding-left:20px}@media(max-width:600px){.toc{columns:1}.card{padding:18px}}
footer{border-top:1px solid #e7dcc7;padding:18px 0 28px;color:#6f6758;font-size:.92rem}footer a{margin-right:14px}.own{margin:8px 0 4px;line-height:1.6}'''
OWNER='''<p class="own">Chủ sở hữu website: <b>Lê Anh Tuấn</b> · Mã số thuế: 038088003952 · Địa chỉ: P1803, CT2B Nam Cường, Phường Nghĩa Đô, TP Hà Nội · Hotline: <a href="tel:0388130130">0388 130 130</a> · Email: <a href="mailto:airdustervn@gmail.com">airdustervn@gmail.com</a></p>'''
LINKS='<a href="/">Trang chủ</a><a href="/dieu-khoan">Điều khoản sử dụng</a><a href="/chinh-sach-bao-mat">Chính sách bảo mật</a><a href="/chinh-sach-thanh-toan">Chính sách thanh toán</a><a href="/chinh-sach-hoan-tien">Hoàn tiền &amp; đổi gói</a><a href="/giai-quyet-khieu-nai">Giải quyết khiếu nại</a>'
CONTACT='''<ul><li>Chủ sở hữu: Lê Anh Tuấn – Mã số thuế: 038088003952</li><li>Địa chỉ: P1803, CT2B Nam Cường, Phường Nghĩa Đô, TP Hà Nội</li><li>Website: <a href="https://gioitoan.com.vn">gioitoan.com.vn</a></li><li>Email: <a href="mailto:airdustervn@gmail.com">airdustervn@gmail.com</a></li><li>Hotline: <a href="tel:0388130130">0388 130 130</a></li></ul>'''
def page(title,desc,sections,path,eff="17/11/2026"):
    toc=''.join(f'<li><a href="#m{i+1}">{html.escape(h)}</a></li>' for i,(h,_) in enumerate(sections))
    body=''.join(f'<h2 id="m{i+1}">{i+1}. {html.escape(h)}</h2>{c}' for i,(h,c) in enumerate(sections))
    return f'''<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} – Giỏi Toán</title><meta name="description" content="{desc}"><link rel="canonical" href="https://gioitoan.com.vn/{path}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&display=swap" rel="stylesheet"><style>{CSS}</style></head>
<body><header><div class="w top"><a class="brand" href="/">{LOGO}<span><em>GIỎI</em> TOÁN</span></a><a class="back" href="/">← Về trang chủ</a></div></header>
<main class="w"><h1>{title}</h1><p class="meta">Áp dụng cho website Giỏi Toán (gioitoan.com.vn, gioitoan.pages.dev) · Hiệu lực từ ngày {eff}</p>
<div class="card"><ol class="toc">{toc}</ol></div><div class="card" style="margin-top:16px">{body}</div></main>
<footer><div class="w">{LINKS}<br>{OWNER}© 2026 Giỏi Toán – Luyện toán mỗi ngày lớp 1–12</div></footer></body></html>
'''
privacy=[
("Giới thiệu","<p>Giỏi Toán (“chúng tôi”) cung cấp website luyện toán lớp 1–12. Chính sách này giải thích chúng tôi thu thập thông tin cá nhân nào, dùng vào việc gì, lưu ở đâu và bạn có những quyền gì. Chúng tôi xử lý dữ liệu cá nhân theo quy định của pháp luật Việt Nam về bảo vệ dữ liệu cá nhân (Nghị định 13/2023/NĐ-CP).</p>"),
("Thông tin chúng tôi thu thập","""<ul>
<li><b>Khi đăng ký bằng tên đăng nhập:</b> tên đăng nhập, họ tên học sinh, lớp và mật khẩu (mật khẩu được mã hóa một chiều, chúng tôi không đọc được).</li>
<li><b>Khi đăng nhập bằng Google:</b> chỉ địa chỉ email và họ tên trên tài khoản Google. Chúng tôi không truy cập Gmail, danh bạ, Google Drive hay bất kỳ dữ liệu nào khác của tài khoản Google.</li>
<li><b>Dữ liệu học tập (khi đã đăng nhập):</b> theo từng ngày – số câu luyện tập đã trả lời và số câu đúng, số đề đã nộp kèm tên đề và số câu đúng, số lần mở trang, thời gian học (chỉ tính khi trang đang mở và có thao tác) và thời điểm hoạt động gần nhất. Chúng tôi không lưu nội dung từng câu trả lời; bài làm chi tiết được lưu ngay trên trình duyệt của bạn.</li>
<li><b>Khi mua gói trả phí:</b> mã đơn hàng, gói đã chọn, số tiền, trạng thái và thời điểm thanh toán. Việc thanh toán diễn ra qua chuyển khoản ngân hàng (VietQR) do payOS xử lý; chúng tôi <b>không</b> nhận và không lưu số thẻ hay thông tin tài khoản ngân hàng của bạn.</li>
<li><b>Thống kê truy cập:</b> một mã ngẫu nhiên ẩn danh lưu trên trình duyệt, nguồn truy cập (ví dụ đến từ Facebook, Google, mã chiến dịch trong đường link) và trang đã mở. Thống kê này không lưu địa chỉ IP, chỉ dùng để biết web được biết đến từ đâu.</li>
<li><b>Dữ liệu kỹ thuật:</b> nhật ký truy cập cơ bản (địa chỉ IP, loại trình duyệt) do nhà cung cấp hạ tầng ghi lại để vận hành và chống lạm dụng.</li></ul>"""),
("Mục đích sử dụng","""<ul><li>Tạo và duy trì tài khoản học sinh, cho phép đăng nhập.</li><li>Tính lượt dùng miễn phí mỗi ngày và kích hoạt gói trả phí.</li><li>Hỗ trợ khi bạn liên hệ, xử lý sự cố thanh toán.</li><li>Thống kê mức độ học tập (tổng hợp và theo từng tài khoản) để cải thiện nội dung đề, bài luyện và hỗ trợ học sinh; chỉ quản trị viên Giỏi Toán xem được.</li><li>Bảo đảm an toàn hệ thống, ngăn gian lận.</li></ul>
<p>Chúng tôi <b>không</b> bán, cho thuê hay trao đổi dữ liệu cá nhân, và không dùng dữ liệu cho quảng cáo của bên thứ ba.</p>"""),
("Lưu trữ và chia sẻ","""<p>Dữ liệu chỉ được chia sẻ với các nhà cung cấp dịch vụ cần thiết để website hoạt động:</p>
<ul><li><b>Supabase</b> – cơ sở dữ liệu và đăng nhập (máy chủ tại Singapore).</li><li><b>Cloudflare</b> – lưu trữ và phân phối website.</li><li><b>Google</b> – xác thực khi bạn chọn “Đăng nhập bằng Google”.</li><li><b>payOS</b> và ngân hàng – xử lý chuyển khoản khi bạn mua gói.</li></ul>
<p>Chúng tôi chỉ cung cấp thông tin cho cơ quan nhà nước khi có yêu cầu hợp pháp. Dữ liệu được lưu trong thời gian tài khoản còn hoạt động; dữ liệu đơn hàng có thể được giữ lâu hơn theo quy định về kế toán, thuế.</p>"""),
("Học sinh dưới 16 tuổi","<p>Phần lớn người dùng là học sinh. Với học sinh dưới 16 tuổi, phụ huynh hoặc người giám hộ nên là người tạo tài khoản, đăng nhập bằng Gmail của phụ huynh, và đồng ý với chính sách này thay cho con. Chúng tôi chỉ thu thập lượng thông tin tối thiểu (họ tên, lớp) và không yêu cầu ảnh, địa chỉ hay số điện thoại của học sinh.</p>"),
("Cookie và bộ nhớ trình duyệt","<p>Website dùng bộ nhớ của trình duyệt (localStorage) để giữ phiên đăng nhập, lớp đang học, tiến độ luyện tập, các tùy chọn hiển thị, cùng mã ẩn danh và nguồn truy cập dùng cho thống kê (mục 2). Chúng tôi không dùng cookie quảng cáo hay công cụ theo dõi của bên thứ ba. Bạn có thể xóa dữ liệu này bất cứ lúc nào trong cài đặt trình duyệt.</p>"),
("Bảo mật","<p>Kết nối luôn được mã hóa HTTPS. Mật khẩu được mã hóa một chiều. Dữ liệu tài khoản được bảo vệ bằng phân quyền theo từng người dùng: mỗi tài khoản chỉ xem được dữ liệu của chính mình; chỉ quản trị viên được xem danh sách tài khoản để hỗ trợ và quản lý gói. Không hệ thống nào an toàn tuyệt đối; nếu phát hiện sự cố ảnh hưởng tới dữ liệu của bạn, chúng tôi sẽ thông báo theo quy định.</p>"),
("Quyền của bạn","""<p>Bạn có quyền xem, sửa (họ tên, lớp trong trang Tài khoản), yêu cầu xóa tài khoản và dữ liệu, rút lại sự đồng ý, hoặc khiếu nại về việc xử lý dữ liệu. Để xóa tài khoản hoặc thực hiện các quyền khác, hãy liên hệ theo mục 10; chúng tôi phản hồi trong vòng 72 giờ làm việc.</p>
<p>Nếu đăng nhập bằng Google, bạn cũng có thể gỡ quyền truy cập của Giỏi Toán tại trang quản lý tài khoản Google (myaccount.google.com › Bảo mật › Ứng dụng bên thứ ba).</p>"""),
("Thay đổi chính sách","<p>Khi chính sách thay đổi, chúng tôi cập nhật ngày hiệu lực ở đầu trang và thông báo trên website nếu thay đổi quan trọng.</p>"),
("Liên hệ",CONTACT),
]
terms=[
("Chấp nhận điều khoản","<p>Khi truy cập hoặc tạo tài khoản trên Giỏi Toán, bạn đồng ý với các điều khoản này và <a href=\"/chinh-sach-bao-mat\">Chính sách bảo mật</a>. Nếu người dùng là học sinh dưới 16 tuổi, phụ huynh hoặc người giám hộ đồng ý thay và chịu trách nhiệm hướng dẫn con sử dụng.</p>"),
("Dịch vụ","<p>Giỏi Toán cung cấp bài luyện tập, đề thi thử và đề mô phỏng môn Toán từ lớp 1 đến lớp 12. Đề mô phỏng do Giỏi Toán tự soạn theo cấu trúc các kỳ thi, với số liệu mới; đó <b>không phải</b> đề thi chính thức của trường, Sở hay tổ chức thi nào, và không bảo đảm kết quả thi thật.</p>"),
("Tài khoản","<ul><li>Mỗi học sinh dùng một tài khoản; không chia sẻ tài khoản cho nhiều người.</li><li>Bạn chịu trách nhiệm giữ bí mật mật khẩu và mọi hoạt động trên tài khoản của mình.</li><li>Thông tin đăng ký phải trung thực; không dùng tên đăng nhập, họ tên phản cảm hoặc mạo danh người khác.</li></ul>"),
("Gói miễn phí và gói trả phí","""<ul><li>Tài khoản mới được <b>dùng thử đầy đủ 7 ngày</b> kể từ khi đăng ký, không cần thanh toán và không tự gia hạn thành gói trả phí. Mỗi học sinh chỉ dùng thử một lần; tạo nhiều tài khoản để kéo dài dùng thử có thể bị khóa.</li>
<li>Sau thời gian dùng thử, tài khoản miễn phí có giới hạn lượt luyện tập và làm đề mỗi ngày, được công bố trên website.</li>
<li>Gói trả phí mở khóa không giới hạn trong thời hạn của gói. Giá, thời hạn được ghi rõ trước khi thanh toán.</li>
<li>Thanh toán bằng chuyển khoản VietQR qua payOS; gói được kích hoạt tự động khi hệ thống nhận đủ tiền. Nếu sau 30 phút gói chưa kích hoạt, hãy liên hệ hotline kèm mã đơn hàng.</li>
<li>Gói đã kích hoạt không hoàn tiền, trừ trường hợp bị trừ tiền nhưng không kích hoạt được, chuyển trùng hoặc lỗi từ phía Giỏi Toán – khi đó chúng tôi kích hoạt lại hoặc hoàn tiền trong vòng 7 ngày làm việc.</li></ul>"""),
("Hành vi không được phép","<ul><li>Sao chép, tải hàng loạt, bán lại hoặc đăng tải lại đề, lời giải của Giỏi Toán khi chưa được đồng ý bằng văn bản.</li><li>Dùng công cụ tự động để truy cập, dò quét hoặc vượt giới hạn lượt dùng.</li><li>Tấn công, làm gián đoạn hệ thống hoặc truy cập trái phép dữ liệu của người khác.</li><li>Dùng website vào mục đích trái pháp luật.</li></ul><p>Vi phạm có thể dẫn tới khóa tài khoản mà không hoàn phí.</p>"),
("Quyền sở hữu trí tuệ","<p>Giao diện, logo, câu hỏi, lời giải và mẹo ghi nhớ trên Giỏi Toán thuộc quyền của Giỏi Toán. Bạn được dùng cho mục đích học tập cá nhân. Tên các kỳ thi (AMC, Kangaroo, SASMO, IMSO…) và tên trường được nhắc đến chỉ để mô tả dạng đề, thuộc về chủ sở hữu tương ứng.</p>"),
("Giới hạn trách nhiệm","<p>Chúng tôi cố gắng bảo đảm đề và đáp án chính xác, website hoạt động liên tục, nhưng không bảo đảm tuyệt đối. Nếu phát hiện câu hỏi hoặc đáp án sai, hãy báo cho chúng tôi để sửa. Giỏi Toán không chịu trách nhiệm cho thiệt hại gián tiếp phát sinh từ việc sử dụng website; trách nhiệm tối đa không vượt quá số tiền bạn đã trả cho gói đang dùng.</p>"),
("Tạm ngừng và chấm dứt","<p>Bạn có thể ngừng sử dụng và yêu cầu xóa tài khoản bất cứ lúc nào. Chúng tôi có thể tạm ngừng dịch vụ để bảo trì, hoặc khóa tài khoản vi phạm điều khoản. Nếu Giỏi Toán ngừng hoạt động hẳn, phần thời hạn còn lại của gói trả phí sẽ được hoàn tiền tương ứng.</p>"),
("Thay đổi điều khoản và luật áp dụng","<p>Điều khoản có thể được cập nhật; ngày hiệu lực ghi ở đầu trang. Việc tiếp tục sử dụng sau khi cập nhật nghĩa là bạn đồng ý với bản mới. Điều khoản này tuân theo pháp luật Việt Nam; tranh chấp được ưu tiên giải quyết bằng thương lượng.</p>"),
("Liên hệ",CONTACT),
]

pay=[
("Giá và gói dịch vụ","<p>Giá các gói được niêm yết công khai tại mục <a href=\"/#thanh-toan\">Bảng giá</a> và trong trang Tài khoản trước khi thanh toán, đã bao gồm mọi khoản phí. Hiện có các gói 1 tháng, 3 tháng, 6 tháng và 1 năm; thời hạn tính theo số ngày ghi trên từng gói. Tài khoản mới được dùng thử đầy đủ 7 ngày miễn phí, không cần thanh toán và không tự chuyển sang gói trả phí.</p>"),
("Phương thức thanh toán","<ul><li><b>Chuyển khoản ngân hàng qua mã VietQR</b>: sau khi chọn gói, hệ thống tạo mã QR riêng cho đơn hàng gồm đúng số tiền và nội dung chuyển khoản. Mở ứng dụng ngân hàng bất kỳ, quét mã và xác nhận.</li><li>Cổng thanh toán payOS xử lý việc đối soát giao dịch. Giỏi Toán <b>không thu thập</b> số thẻ, số tài khoản hay mật khẩu ngân hàng của bạn.</li><li>Không sửa số tiền hay nội dung chuyển khoản; nếu sửa, hệ thống không tự kích hoạt được và bạn cần liên hệ hỗ trợ.</li></ul>"),
("Kích hoạt gói (giao dịch vụ)","<p>Gói được kích hoạt <b>tự động ngay khi hệ thống nhận đủ tiền</b>, thường trong vòng 1–5 phút; tài khoản hiện nhãn PRO và ngày hết hạn trong trang Tài khoản. Mua thêm khi gói còn hạn thì số ngày được cộng dồn. Nếu sau 30 phút gói chưa kích hoạt, hãy gọi hotline hoặc gửi email kèm ảnh giao dịch và tên đăng nhập; chúng tôi xử lý trong giờ làm việc, chậm nhất 24 giờ.</p>"),
("Hóa đơn và chứng từ","<p>Lịch sử đơn hàng (mã đơn, gói, số tiền, thời điểm) được lưu trong tài khoản. Nếu cần chứng từ thanh toán, hãy gửi email kèm mã đơn hàng.</p>"),
("Bảo mật giao dịch","<p>Kết nối luôn mã hóa HTTPS. Thông tin đơn hàng chỉ dùng để kích hoạt gói, hỗ trợ và đối soát theo <a href=\"/chinh-sach-bao-mat\">Chính sách bảo mật</a>.</p>"),
("Liên hệ",CONTACT)]
ref=[
("Trường hợp được hoàn tiền","<p>Chúng tôi hoàn lại <b>100% số tiền</b> trong các trường hợp:</p><ul><li>Đã chuyển tiền nhưng gói không được kích hoạt và chúng tôi không khắc phục được trong 24 giờ.</li><li>Chuyển trùng (thanh toán hai lần cho cùng một đơn) hoặc chuyển thừa so với giá gói – hoàn phần chuyển thừa.</li><li>Lỗi kỹ thuật từ phía Giỏi Toán khiến bạn không sử dụng được dịch vụ liên tục quá 72 giờ trong thời hạn gói – hoàn phần tương ứng số ngày còn lại, hoặc cộng bù ngày nếu bạn đồng ý.</li></ul>"),
("Trường hợp không hoàn tiền","<p>Vì mỗi tài khoản đã được dùng thử đầy đủ 7 ngày trước khi mua, gói đã kích hoạt và hoạt động bình thường không được hoàn tiền khi bạn đổi ý hoặc không dùng hết thời hạn. Tài khoản bị khóa do vi phạm <a href=\"/dieu-khoan\">Điều khoản sử dụng</a> (chia sẻ tài khoản, tải đề hàng loạt…) cũng không được hoàn tiền.</p>"),
("Đổi và nâng cấp gói","<ul><li>Có thể mua gói dài hơn bất kỳ lúc nào; số ngày của gói mới được cộng thêm vào ngày hết hạn hiện tại, không mất ngày nào.</li><li>Nếu mua nhầm gói trong vòng 24 giờ và chưa làm đề thi nào, chúng tôi hỗ trợ đổi sang gói khác và hoàn hoặc thu thêm phần chênh lệch.</li><li>Gói gắn với một tài khoản học sinh; có thể chuyển sang tài khoản khác của cùng gia đình một lần, khi liên hệ hỗ trợ.</li></ul>"),
("Cách yêu cầu và thời hạn","<ol><li>Gọi hotline hoặc gửi email kèm: tên đăng nhập, mã đơn hàng hoặc ảnh giao dịch, số tài khoản nhận lại tiền.</li><li>Chúng tôi xác nhận trong vòng 24 giờ làm việc.</li><li>Tiền được hoàn bằng chuyển khoản về tài khoản đã thanh toán trong <b>tối đa 7 ngày làm việc</b> kể từ khi xác nhận.</li></ol><p>Yêu cầu hoàn tiền cần gửi trong vòng 30 ngày kể từ ngày thanh toán.</p>"),
("Liên hệ",CONTACT)]
cpl=[
("Kênh tiếp nhận","<ul><li>Hotline / Zalo: <a href=\"tel:0388130130\">0388 130 130</a> (8:00–21:00 hằng ngày)</li><li>Email: <a href=\"mailto:airdustervn@gmail.com\">airdustervn@gmail.com</a></li></ul><p>Khi gửi phản ánh, vui lòng nêu: tên đăng nhập, nội dung sự việc, thời điểm, mã đơn hàng hoặc ảnh chụp liên quan (nếu có). Phản ánh về câu hỏi hoặc đáp án sai xin ghi rõ tên đề và số câu.</p>"),
("Quy trình xử lý","<ol><li><b>Tiếp nhận:</b> xác nhận đã nhận phản ánh trong vòng 24 giờ.</li><li><b>Xác minh:</b> kiểm tra thông tin tài khoản, giao dịch, nội dung đề.</li><li><b>Phản hồi:</b> trả lời phương án giải quyết trong tối đa 3 ngày làm việc.</li><li><b>Giải quyết:</b> thực hiện phương án (sửa đề, kích hoạt gói, cộng ngày, hoàn tiền theo <a href=\"/chinh-sach-hoan-tien\">Chính sách hoàn tiền</a>) trong tối đa 7 ngày làm việc kể từ khi hai bên thống nhất.</li></ol>"),
("Nguyên tắc","<p>Mọi phản ánh được giải quyết trên tinh thần thương lượng, tôn trọng quyền lợi người tiêu dùng, bảo mật thông tin người phản ánh. Thông tin trao đổi chỉ dùng cho việc giải quyết khiếu nại.</p>"),
("Khi chưa đạt được thỏa thuận","<p>Nếu không đồng ý với phương án giải quyết, bạn có quyền đề nghị hòa giải, gửi yêu cầu tới cơ quan, tổ chức bảo vệ quyền lợi người tiêu dùng, hoặc khởi kiện tại Tòa án có thẩm quyền theo quy định của pháp luật Việt Nam.</p>"),
("Thông tin người bán",CONTACT)]
for slug,title,desc,sec,eff in [("chinh-sach-bao-mat","Chính sách bảo mật","Giỏi Toán thu thập, sử dụng và bảo vệ thông tin cá nhân như thế nào.",privacy,"17/11/2026"),
 ("dieu-khoan","Điều khoản sử dụng","Điều khoản sử dụng website luyện toán Giỏi Toán.",terms,"17/11/2026"),
 ("chinh-sach-thanh-toan","Chính sách thanh toán","Phương thức thanh toán, kích hoạt gói học và chứng từ trên Giỏi Toán.",pay,"18/11/2026"),
 ("chinh-sach-hoan-tien","Chính sách hoàn tiền và đổi gói","Các trường hợp hoàn tiền, đổi và nâng cấp gói học trên Giỏi Toán.",ref,"18/11/2026"),
 ("giai-quyet-khieu-nai","Quy trình giải quyết khiếu nại","Kênh tiếp nhận và quy trình giải quyết phản ánh, khiếu nại của khách hàng Giỏi Toán.",cpl,"18/11/2026")]:
    os.makedirs(f"{PUB}/{slug}",exist_ok=True)
    open(f"{PUB}/{slug}/index.html","w").write(page(title,desc,sec,slug,eff))
print("ok")
