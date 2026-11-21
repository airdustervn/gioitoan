#!/usr/bin/env python3
"""Sinh các trang đích SEO, sitemap.xml, robots.txt và thẻ meta cho trang chủ.
Chạy lại mỗi khi đổi tên miền (sửa SITE) hoặc thêm đề:  python3 tools/seo_build.py
"""
import json, os, re, html, datetime
ROOT = os.path.join(os.path.dirname(__file__), "..", "public")
SITE = "https://gioitoan.com.vn"          # đổi thành https://gioitoan.com.vn khi gắn tên miền
TODAY = datetime.date.today().isoformat()
E = html.escape
idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

def J(prefix):
    i = idx.index(prefix); j = idx.index("\n", i)
    return json.loads(idx[i + len(prefix):j].rstrip(";").rstrip(")"))
HN_TWIN, HN_MORE = J("const HN_TWIN="), J("const HN_MORE=")
DHY, DHX, V10, V10X, XP = J("const DHY="), J("DHS.push(..."), J("const V10="), J("V10.push(..."), J("const XP=")
MODES = {k: v for k, v in re.findall(r'\n ([A-Z]+):\{name:"([^"]+)"', idx[idx.index("const HN_MODES={"):][:20000])}
XO = json.loads(re.search(r'const XO=(\[[^\]]*\])', idx).group(1))
# đề quốc tế bổ sung trong các khối Object.assign(XP,…) đã tách – lấy tên từ dữ liệu tĩnh
XNAMES = {}
for m in re.finditer(r'^Object\.assign\(XP,(\{.*\})\);$', idx, re.M):
    for k, v in json.loads(m.group(1)).items(): XNAMES[k] = v.get("name") or k
for k, v in XP.items(): XNAMES[k] = v.get("name") or k

LOGO = idx[idx.index('<svg class="logo-mark"'):idx.index('</svg>', idx.index('<svg class="logo-mark"')) + 6]
CSS = """*{box-sizing:border-box}body{margin:0;font-family:"Be Vietnam Pro",system-ui,sans-serif;color:#1c1a17;background:#fbf7ef;line-height:1.65}
a{color:#c8102e}header{background:#fff;border-bottom:1px solid #e7dcc7}.w{max-width:920px;margin:0 auto;padding:0 20px}
.top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0}.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:#1c1a17;font-weight:800;font-size:1.2rem}
.brand em{font-style:normal;color:#c8102e}.logo-mark{width:36px;height:36px}.nav a{margin-left:14px;font-weight:700;text-decoration:none}
main{padding:24px 0 40px}.crumb{font-size:.9rem;color:#6f6758;margin-bottom:6px}.crumb a{color:#6f6758}
h1{font-size:clamp(1.6rem,4vw,2.3rem);line-height:1.2;margin:0 0 10px}.lead{font-size:1.08rem;color:#3c362d;margin:0 0 18px}
.cta{display:inline-block;background:#c8102e;color:#fff;font-weight:800;padding:12px 20px;border-radius:999px;text-decoration:none;box-shadow:0 6px 16px rgba(200,16,46,.25)}
.card{background:#fff;border:1px solid #e7dcc7;border-radius:16px;padding:20px 22px;margin:16px 0;box-shadow:0 6px 18px rgba(28,26,23,.05)}
h2{font-size:1.2rem;margin:0 0 10px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;padding:0;list-style:none;margin:0}
.grid li{background:#fbf7ef;border:1px solid #e7dcc7;border-radius:12px;padding:10px 12px}.grid b{display:block}.grid span{font-size:.88rem;color:#6f6758}
ul.feat li{margin:6px 0}.more{display:flex;flex-wrap:wrap;gap:8px}.more a{background:#fff;border:1px solid #e7dcc7;border-radius:999px;padding:6px 12px;text-decoration:none;font-weight:600}
footer{border-top:1px solid #e7dcc7;padding:18px 0 28px;color:#6f6758;font-size:.92rem}footer a{margin-right:14px}"""

PAGES = []  # (slug, title, h1, desc, lead, sections_html, hash, keywords)
def lst(items):
    return '<ul class="grid">' + "".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a, b in items) + "</ul>"
FEAT = """<ul class="feat"><li><b>Đúng cấu trúc đề thật:</b> số câu, thang điểm và thời gian giống kỳ thi; số liệu mới, không chép đề gốc.</li>
<li><b>Chấm điểm ngay</b> khi nộp bài, xem đáp án và <b>lời giải từng bước</b>, gợi ý và mẹo ghi nhớ cho từng câu.</li>
<li><b>Đồng hồ đếm ngược</b> như phòng thi, luyện được trên điện thoại, máy tính bảng và máy tính.</li>
<li><b>Tài khoản mới dùng thử đầy đủ 7 ngày</b>, đăng nhập nhanh bằng Gmail, không cần thanh toán.</li>
<li><b>Đề mới mỗi ngày</b>, không trùng lặp; mục HOT cập nhật đề mô phỏng các kỳ thi vừa diễn ra.</li></ul>"""

# 1. vào lớp 6
schools = {}
for k, e in HN_TWIN.items(): schools.setdefault(k, []).append(e["year"])
for k, l in HN_MORE.items():
    for e in l: schools.setdefault(k, []).append(e["year"])
rows = []
for k, ys in schools.items():
    yrs = sorted({y.split(" ")[0] for y in ys if re.match(r"\d", y)}, reverse=True)
    hb = [y for y in ys if y.startswith("Học bổng")]; prac = sum(1 for y in ys if y.startswith("Đề luyện"))
    parts = (["Năm học " + ", ".join(yrs[:4])] if yrs else []) + hb + ([f"{prac} đề luyện"] if prac else [])
    desc = " · ".join(parts)
    rows.append((MODES.get(k, k), desc or f"{len(ys)} đề"))
PAGES.append(("de-thi-vao-lop-6", "Đề thi vào lớp 6 môn Toán các trường CLC Hà Nội – luyện online có đáp án",
  "Đề thi vào lớp 6 môn Toán – Cầu Giấy, Nguyễn Tất Thành, Lương Thế Vinh, Amsterdam…",
  "Luyện đề thi vào lớp 6 môn Toán các trường chất lượng cao Hà Nội: Cầu Giấy, Nguyễn Tất Thành, Lương Thế Vinh, Hà Nội – Amsterdam, Ngôi Sao, Marie Curie, Archimedes. Làm online, chấm điểm ngay, có lời giải.",
  "Bộ đề mô phỏng thi vào lớp 6 môn Toán theo từng trường THCS chất lượng cao ở Hà Nội, bám đúng cấu trúc đề các năm và các kỳ thi học bổng. Học sinh lớp 5 làm bài trực tuyến như thi thật, nộp bài là có điểm và lời giải chi tiết.",
  f'<div class="card"><h2>Các trường đã có đề</h2>{lst(rows)}</div>', "vao-lop-6", "đề thi vào lớp 6, đề thi vào lớp 6 Cầu Giấy, đề thi vào lớp 6 Nguyễn Tất Thành, toán lớp 5 nâng cao"))
# 2. vào lớp 10
v = [(f"Hà Nội {e['y']}–{e['y']+1}" if not e.get("lab") else e["lab"], e.get("title", "")[:70]) for e in V10] + [(e.get("lab") or "Đề luyện", "Đề luyện theo cấu trúc Hà Nội") for e in V10X]
PAGES.append(("de-thi-vao-lop-10", "Đề thi vào lớp 10 môn Toán Hà Nội 2020–2026 – thi thử online có đáp án",
  "Đề thi vào lớp 10 môn Toán Hà Nội và các tỉnh",
  "Thi thử vào lớp 10 môn Toán: đề mô phỏng Hà Nội các năm 2020–2026, TP.HCM, Đà Nẵng, Hải Phòng… Làm bài online 90–120 phút, chấm điểm theo thang 10, có lời giải từng bước.",
  "Đề mô phỏng tuyển sinh vào lớp 10 môn Toán theo cấu trúc đề của Sở GD&ĐT Hà Nội từ năm 2020 đến 2026 và một số tỉnh, thành lớn. Mỗi đề gồm phần trắc nghiệm, đúng/sai và tự luận chuyển thành ô ghi đáp số để chấm tự động.",
  f'<div class="card"><h2>Danh sách đề</h2>{lst(v[:24])}</div>', "vao-lop-10", "đề thi vào lớp 10 môn toán, đề thi vào 10 Hà Nội, thi thử vào lớp 10"))
# 3. THPT
d = [(f"Đề {e['y']}", e.get("title", "")[:70]) for e in DHY] + [(str(e.get("y")), e.get("title", "")[:70]) for e in DHX]
PAGES.append(("de-thi-tot-nghiep-thpt-mon-toan", "Đề thi tốt nghiệp THPT môn Toán 2020–2026 – thi thử online, chấm điểm ngay",
  "Đề thi tốt nghiệp THPT môn Toán (thi thử đại học)",
  "Luyện đề thi tốt nghiệp THPT môn Toán: cấu trúc mới 2025 (12 trắc nghiệm, 4 câu đúng/sai, 6 câu trả lời ngắn) và cấu trúc 50 câu trắc nghiệm các năm 2020–2024. Thi thử online, chấm điểm ngay.",
  "Bộ đề mô phỏng kỳ thi tốt nghiệp THPT môn Toán dùng để xét tuyển đại học: đủ cả định dạng mới từ năm 2025 và định dạng 50 câu trắc nghiệm các năm trước. Hệ thống tính điểm đúng quy chế từng phần và giải thích từng câu.",
  f'<div class="card"><h2>Danh sách đề</h2>{lst(d)}</div>', "dai-hoc", "đề thi tốt nghiệp THPT môn toán, đề thi thử đại học môn toán, đề minh họa 2026"))
# 4. quốc tế
groups = {}
for k in XO:
    g = re.sub(r"_.*", "", k); groups.setdefault(g, []).append(XNAMES.get(k, k))
GN = {"AMC8": "AMC 8 (Mỹ)", "SASMO": "SASMO (Singapore)", "TIMO": "TIMO", "HKIMO": "HKIMO (Hồng Kông)", "IMSO": "IMSO", "AIMO": "AIMO", "IKMC": "Kangaroo IKMC"}
x = [(GN.get(g, g), f"{len(l)} đề mô phỏng") for g, l in groups.items()]
PAGES.append(("de-thi-toan-quoc-te", "Đề thi Toán quốc tế AMC 8, Kangaroo IKMC, SASMO, TIMO, HKIMO, IMSO – luyện online",
  "Đề thi Toán quốc tế: AMC 8, Kangaroo, SASMO, TIMO, HKIMO, IMSO, AIMO",
  "Luyện đề thi Toán quốc tế cho học sinh tiểu học và THCS: AMC 8, Kangaroo IKMC, SASMO, TIMO, HKIMO, IMSO, AIMO. Đề song ngữ Anh – Việt, chấm điểm đúng luật từng kỳ thi.",
  "Đề mô phỏng các kỳ thi Toán quốc tế phổ biến với học sinh Việt Nam, giữ đúng số câu, thời gian và cách tính điểm (ví dụ Kangaroo bắt đầu 30 điểm và trừ điểm khi sai, SASMO cộng điểm theo phần). Câu hỏi tiếng Anh kèm bản dịch tiếng Việt.",
  f'<div class="card"><h2>Các kỳ thi</h2>{lst(x)}</div>', "de-quoc-te", "đề thi AMC 8, đề thi Kangaroo, đề SASMO, đề TIMO, toán quốc tế lớp 5"))
# 5. Violympic, 6. Kangaroo
PAGES.append(("luyen-thi-violympic", "Luyện thi Violympic Toán lớp 1–9 – đề luyện online miễn phí",
  "Luyện thi Violympic Toán", "Luyện thi Violympic Toán online lớp 1–9 với đề theo vòng, có đồng hồ và lời giải. Miễn phí 10 câu luyện tập và 1 đề thi mỗi ngày.",
  "Đề luyện Violympic Toán theo từng lớp, gồm các dạng điền số, chọn đáp án và toán tư duy thường gặp trong các vòng thi. Học sinh làm bài có tính giờ, xem lời giải và mẹo ngay sau khi nộp.", "", "violympic", "luyện thi violympic toán, đề violympic lớp 5"))
PAGES.append(("luyen-thi-kangaroo", "Luyện thi Kangaroo (IKMC) – đề mô phỏng 37 chủ đề lớp 5",
  "Luyện thi Toán Kangaroo IKMC", "Luyện thi Kangaroo IKMC online: đề mô phỏng 30 câu theo 37 chủ đề, chấm điểm đúng luật Kangaroo (30 điểm khởi đầu, trừ 1/4 khi sai), có lời giải.",
  "Đề mô phỏng kỳ thi Toán Kangaroo quốc tế (IKMC) dành cho học sinh tiểu học, bao phủ đủ 37 chủ đề thường gặp: logic, hình học, đếm, quy luật, xúc xắc, khối lập phương… Điểm được tính đúng như thi thật.", "", "kangaroo", "đề thi kangaroo lớp 5, IKMC, luyện thi kangaroo"))
# 7–9. theo cấp
for slug, t, h, dsc, lead, hs, kw in [
  ("luyen-toan-tieu-hoc", "Luyện toán tiểu học lớp 1–5 online – bài tập theo dạng có lời giải", "Luyện toán tiểu học lớp 1–5",
   "Bài tập toán lớp 1, 2, 3, 4, 5 theo từng dạng: số học, hình học, đo lường, logic, tổ hợp. Có gợi ý, lời giải từng bước và mẹo ghi nhớ.",
   "Ngân hàng bài luyện toán tiểu học sắp xếp theo lớp và theo dạng, đi từ dễ đến khó. Phù hợp ôn tập hằng ngày, chuẩn bị thi học kỳ, thi Violympic, Kangaroo và thi vào lớp 6.", "tieu-hoc", "toán lớp 5, bài tập toán lớp 4, toán tư duy tiểu học"),
  ("luyen-toan-thcs", "Luyện toán THCS lớp 6–9 online – bài tập theo chương có lời giải", "Luyện toán THCS lớp 6–9",
   "Bài tập toán lớp 6, 7, 8, 9 theo chương trình mới: số và đại số, hình học và đo lường, thống kê và xác suất. Luyện online, có lời giải.",
   "Bài luyện toán trung học cơ sở bám chương trình giáo dục phổ thông 2018, kèm đề thi thử vào lớp 10 các năm.", "thcs", "toán lớp 9, bài tập toán lớp 8, ôn thi vào 10"),
  ("luyen-toan-thpt", "Luyện toán THPT lớp 10–12 online – ôn thi tốt nghiệp có lời giải", "Luyện toán THPT lớp 10–12",
   "Bài tập toán lớp 10, 11, 12: đại số và giải tích, hình học và tọa độ, tổ hợp – xác suất. Ôn thi tốt nghiệp THPT với đề thi thử chấm điểm ngay.",
   "Bài luyện toán trung học phổ thông theo chủ đề, kết hợp đề thi thử tốt nghiệp THPT định dạng mới và cũ.", "thpt", "toán lớp 12, ôn thi tốt nghiệp môn toán")]:
    PAGES.append((slug, t, h, dsc, lead, "", hs, kw))

def page(slug, title, h1, desc, lead, body, hsh, kw):
    url = f"{SITE}/{slug}"
    others = "".join(f'<a href="/{p[0]}">{E(p[2].split(" – ")[0].split(":")[0])}</a>' for p in PAGES if p[0] != slug)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Giỏi Toán", "item": SITE + "/"},
                                                       {"@type": "ListItem", "position": 2, "name": h1, "item": url}]},
        {"@type": "WebPage", "name": title, "description": desc, "url": url, "inLanguage": "vi",
         "isPartOf": {"@type": "WebSite", "name": "Giỏi Toán", "url": SITE + "/"}}]}
    return f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Giỏi Toán"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og.png"><meta property="og:locale" content="vi_VN">
<meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&display=swap" rel="stylesheet"><style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>
<body><header><div class="w top"><a class="brand" href="/">{LOGO}<span><em>GIỎI</em> TOÁN</span></a><nav class="nav"><a href="/#{hsh}">Làm bài</a><a href="/#tai-khoan">Đăng nhập</a></nav></div></header>
<main class="w"><div class="crumb"><a href="/">Giỏi Toán</a> › {E(h1)}</div><h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>
<a class="cta" href="/#{hsh}">Làm bài ngay – miễn phí →</a>{body}
<div class="card"><h2>Vì sao luyện trên Giỏi Toán</h2>{FEAT}</div>
<div class="card"><h2>Xem thêm</h2><div class="more">{others}<a href="/#hot">🔥 Đề thi nóng hổi</a></div></div></main>
<footer><div class="w"><a href="/">Trang chủ</a><a href="/dieu-khoan">Điều khoản sử dụng</a><a href="/chinh-sach-bao-mat">Chính sách bảo mật</a><a href="/chinh-sach-thanh-toan">Chính sách thanh toán</a><a href="/chinh-sach-hoan-tien">Hoàn tiền &amp; đổi gói</a><a href="/giai-quyet-khieu-nai">Giải quyết khiếu nại</a><a href="https://www.facebook.com/gioitoan.com.vn" target="_blank" rel="noopener">Fanpage Facebook</a><br><span style="display:block;margin:8px 0 4px">Chủ sở hữu website: <b>Lê Anh Tuấn</b> · Mã số thuế: 038088003952 · Địa chỉ: 02 Thành Công, Phường Đông Thọ, Thành Phố Thanh Hóa · Hotline 0388 130 130</span>© 2026 Giỏi Toán – Luyện toán mỗi ngày lớp 1–12</div></footer></body></html>
"""
for p in PAGES:
    os.makedirs(os.path.join(ROOT, p[0]), exist_ok=True)
    open(os.path.join(ROOT, p[0], "index.html"), "w", encoding="utf-8").write(page(*p))

# favicon
logo_svg = LOGO.replace('class="logo-mark" ', 'xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', "")
open(os.path.join(ROOT, "favicon.svg"), "w").write(logo_svg)
# sitemap + robots
LEGAL = ("chinh-sach-bao-mat", "dieu-khoan", "chinh-sach-thanh-toan", "chinh-sach-hoan-tien", "giai-quyet-khieu-nai")
urls = [("", "daily", "1.0")] + [(p[0], "weekly", "0.8") for p in PAGES] + [(x, "yearly", "0.2") for x in LEGAL]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n" for u, c, pr in urls) + "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nAllow: /auto/manifest.js\nDisallow: /auto/\nDisallow: /data/\n\nSitemap: {SITE}/sitemap.xml\n")

# meta trang chủ (giữa 2 dấu mốc, chạy lại được)
desc = "Giỏi Toán – luyện toán online lớp 1–12 mỗi ngày: đề thi vào lớp 6 các trường CLC Hà Nội, đề thi vào lớp 10, đề thi tốt nghiệp THPT môn Toán, Kangaroo, AMC 8, Violympic. Chấm điểm ngay, có lời giải từng bước."
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "WebSite", "name": "Giỏi Toán", "alternateName": "gioitoan", "url": SITE + "/", "inLanguage": "vi"},
  {"@type": "EducationalOrganization", "name": "Giỏi Toán", "url": SITE + "/", "logo": SITE + "/favicon.svg", "telephone": "+84388130130", "sameAs": ["https://www.facebook.com/gioitoan.com.vn"],
   "description": desc}]}
meta = f"""<!--SEO-->
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE}/">
<meta property="og:type" content="website"><meta property="og:site_name" content="Giỏi Toán"><meta property="og:locale" content="vi_VN">
<meta property="og:title" content="Giỏi Toán – Luyện toán mỗi ngày lớp 1–12"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{SITE}/"><meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#c8102e">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="sitemap" href="/sitemap.xml">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<!--/SEO-->"""
s = idx
s = re.sub(r"<!--SEO-->.*?<!--/SEO-->\n?", "", s, flags=re.S)
s = s.replace("<title>Giỏi Toán – Luyện toán mỗi ngày lớp 1–12</title>", "<title>Giỏi Toán – Luyện toán mỗi ngày lớp 1–12</title>\n" + meta, 1)
# liên kết thu thập được ở chân trang
links = "".join(f'<a href="/{p[0]}">{E(p[2].split(" – ")[0].split(":")[0])}</a>' for p in PAGES)
s = re.sub(r'<!--SEOLINKS-->.*?<!--/SEOLINKS-->', '', s, flags=re.S)
s = s.replace('<div class="wrap foot-copy">', f'<!--SEOLINKS--><nav class="wrap foot-seo" aria-label="Đề thi và luyện tập">{links}</nav><!--/SEOLINKS--><div class="wrap foot-copy">', 1)
if ".foot-seo{" not in s:
    s = s.replace("</style>", ".foot-seo{display:flex;flex-wrap:wrap;gap:6px 16px;padding-top:10px;font-size:.9rem}.foot-seo a{color:inherit;opacity:.85}\n</style>", 1)
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(s)
# trang pháp lý: canonical theo SITE
for slug in LEGAL:
    f = os.path.join(ROOT, slug, "index.html"); t = open(f, encoding="utf-8").read()
    t = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{SITE}/{slug}">', t)
    open(f, "w", encoding="utf-8").write(t)
print(len(PAGES), "trang đích;", SITE)
