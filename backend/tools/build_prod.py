#!/usr/bin/env python3
"""Tạo bản chạy thật có bảo vệ đề.

Dùng:  python3 tools/build_prod.py <thư-mục-site> <thư-mục-ra> --url https://<ma>.supabase.co --anon <khoa-anon> [--free S_x_AMC8,...]

- <thư-mục-site>: bản site đầy đủ (index.html, data/, auto/, lib/) – ví dụ tải từ artifact.
- Kết quả:
    <ra>/dist/        : site để đưa lên hosting – KHÔNG còn file đề/đáp án (data/*.js, auto/b*.js, auto/m*.js)
    <ra>/papers.jsonl : toàn bộ đề, mỗi dòng {"id","cat","free","data"} để upload_papers.py đẩy lên Supabase
- index.html được điền CONFIG (URL, khóa anon, PROTECT_PAPERS:true) và thêm Content-Security-Policy.
"""
import argparse, json, os, re, shutil, sys
from urllib.parse import urlparse

ap = argparse.ArgumentParser()
ap.add_argument("site"); ap.add_argument("out")
ap.add_argument("--url", required=True); ap.add_argument("--anon", required=True)
ap.add_argument("--supabase-js", default="lib/sb.js"); ap.add_argument("--sri", default="")
ap.add_argument("--free", default="", help="id đề cho xem miễn phí, phân tách bằng dấu phẩy")
a = ap.parse_args()
free = {x for x in a.free.split(",") if x}
PFX = "Object.assign(window.AUTO_DATA=window.AUTO_DATA||{},"

def read_data(path):
    t = open(path, encoding="utf-8").read().strip()
    if not t.startswith(PFX): sys.exit(f"Định dạng lạ: {path}")
    return json.loads(t[len(PFX):].rstrip(";").rstrip(")"))

papers = {}
for sub in ("data", "auto"):
    d = os.path.join(a.site, sub)
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if f.endswith(".js") and f != "manifest.js":
            for k, v in read_data(os.path.join(d, f)).items():
                papers[k] = (sub + "/" + f, v)

dist = os.path.join(a.out, "dist"); shutil.rmtree(dist, ignore_errors=True); os.makedirs(dist)
for root, _, files in os.walk(a.site):
    rel = os.path.relpath(root, a.site)
    for f in files:
        r = os.path.normpath(os.path.join(rel, f))
        if r.startswith("data" + os.sep) or (r.startswith("auto" + os.sep) and f != "manifest.js") or r.startswith("gen" + os.sep):
            continue                                   # đề, đáp án, bộ sinh đề: không đưa lên hosting công khai
        os.makedirs(os.path.join(dist, rel), exist_ok=True); shutil.copy(os.path.join(root, f), os.path.join(dist, r))

with open(os.path.join(a.out, "papers.jsonl"), "w", encoding="utf-8") as fo:
    for k, (src, v) in papers.items():
        fo.write(json.dumps({"id": k, "cat": src, "free": k in free, "data": v}, ensure_ascii=False) + "\n")

p = os.path.join(dist, "index.html"); s = open(p, encoding="utf-8").read()
def setcfg(key, val):
    global s
    s, n = re.subn(r'(\n\s*%s:)("[^"]*"|true|false)' % key, lambda m: m.group(1) + val, s, count=1)
    if n != 1: sys.exit("Không tìm thấy CONFIG." + key)
setcfg("SUPABASE_URL", json.dumps(a.url)); setcfg("SUPABASE_ANON_KEY", json.dumps(a.anon))
setcfg("SUPABASE_JS", json.dumps(a.supabase_js)); setcfg("SUPABASE_JS_SRI", json.dumps(a.sri)); setcfg("PROTECT_PAPERS", "true")
sb = urlparse(a.url); sbo = f"{sb.scheme}://{sb.netloc}"
js = urlparse(a.supabase_js); jso = f" {js.scheme}://{js.netloc}" if js.scheme else ""
if jso and not a.sri: sys.exit("Thư viện từ CDN cần --sri (chạy tools/vendor.sh để lấy).")
csp = ("default-src 'self'; script-src 'self' 'unsafe-inline'" + jso + "; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self' " + sbo + " " + sbo.replace("https://", "wss://") +
       "; object-src 'none'; base-uri 'self'; form-action 'self'")
s = s.replace("<head>", '<head>\n<meta http-equiv="Content-Security-Policy" content="' + csp + '">\n<meta name="referrer" content="strict-origin-when-cross-origin">', 1)
open(p, "w", encoding="utf-8").write(s)
print(f"{len(papers)} đề -> {a.out}/papers.jsonl ; site -> {dist}")
