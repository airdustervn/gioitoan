"""Usage: python3 auto_batch.py OUTDIR
OUTDIR has manifest.js and seen.txt (hashes of every question already on the site).
Writes b<N>.js, updates manifest.js and seen.txt. Up to 20 papers; a paper is skipped
rather than published if it would repeat any question already on the site."""
import sys,os,json,random
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from dedup import *
from intl import gens,mc
from thpt_new import paper as pn
from thpt_old import paper as po
from v10 import new as vnw, old as vo
OUT=sys.argv[1];MF=os.path.join(OUT,"manifest.js");SF=os.path.join(OUT,"seen.txt")
M=[]
if os.path.exists(MF):
    t=open(MF).read();M=json.loads(t[t.index("["):t.rindex("]")+1])
seen=set(open(SF).read().split()) if os.path.exists(SF) else set()
N=len(M)+1
while os.path.exists(os.path.join(OUT,f"b{N}.js")): N+=1
BASE={"AMC8":4,"SASMO":4,"TIMO":3,"HKIMO":3,"IMSO":4,"AIMO":2,"DHnew":5,"DHold":3,"V10new":5,"V10old":2,"HN_CHUNG":8,"HN_CG":4,"HN_NS":3,"HN_NTT":2}
cnt=dict(BASE)
for b in M:
    for it in b["items"]: cnt[it["g"]]=cnt.get(it["g"],0)+1
labels={(it.get("cat"),it.get("key") or it.get("y") or it.get("lab") or (it.get("m"),it.get("year"))) for b in M for it in b["items"]}
S=1000003*N;items=[];data={};skipped=[]
def try_make(maker,tries=4):
    for t in range(tries):
        trial=set(seen);obj,d=maker(S+7919*t,trial)
        if d==0: seen.clear();seen.update(trial);return obj
    return None
def add(meta,full):
    iid=f"b{N}_{len(items)}";meta["id"]=iid;meta["f"]=f"auto/b{N}.js";items.append(meta);data[iid]=full
INTL=[("AMC8","amc8",40,25,"25 câu · 40 phút",[["25 câu trắc nghiệm A–E · đúng 1 điểm",25]],25,0,5),
 ("SASMO","sasmo",90,85,"25 câu · 90 phút",[["Section A · 15 câu trắc nghiệm (+2 / −1 / 0)",15],["Section B · 10 câu điền đáp số (+4)",10]],15,10,4),
 ("TIMO","flat4",90,100,"25 câu · 90 phút",[["25 câu điền đáp số · 4 điểm/câu",25]],0,25,4),
 ("HKIMO","flat4",90,100,"25 câu · 90 phút",[["25 câu điền đáp số · 4 điểm/câu",25]],0,25,4),
 ("IMSO","flat1",60,25,"25 câu · 60 phút",[["Short Answer · 25 câu (1 điểm/câu)",25]],0,25,4),
 ("AIMO","flat5",90,150,"30 câu · 150 điểm",[["30 câu điền đáp số · 5 điểm/câu",30]],0,30,4)]
for j,(g,rule,mn,mx,tag,secs,nmc,nop,mo) in enumerate(INTL):
    def mk(sd,trial,nmc=nmc,nop=nop,mo=mo):
        qs=intl_build(gens,mc,sd+j,nmc,nop,mo,trial);return qs,(0 if len(qs)==nmc+nop else 1)
    qs=try_make(mk)
    if qs is None: skipped.append(g);continue
    n=nxt=cnt[g]=cnt.get(g,0)+1;nm=f"{'AMC 8' if g=='AMC8' else g} · Đề {n}";key=f"{g}_{n}"
    full={"name":nm,"title":"Đề mô phỏng "+nm.replace(" ·"," –"),"min":mn,"rule":rule,"max":mx,"tag":tag,"secs":secs,"note":"Đề mô phỏng do Giỏi Toán tự sinh theo đúng thể thức kỳ thi; đáp án được máy tính kiểm tra; không câu nào trùng với đề đã có.","qs":qs}
    add({"cat":"x","g":g,"key":key,"name":nm,"min":mn,"rule":rule,"max":mx,"tag":tag,"title":full["title"]},full)
for j in range(5):
    newf=j<4
    d=try_make((lambda sd,tr:thpt_new(pn,sd+100+j,tr)) if newf else (lambda sd,tr:thpt_old(po,sd+100+j,tr)))
    if d is None: skipped.append("THPT");continue
    g="DHnew" if newf else "DHold";n=cnt[g]=cnt.get(g,0)+1
    full=({"y":f"Luyện {n} (cấu trúc 2025)","fmt":"new","title":f"Đề luyện tốt nghiệp THPT môn Toán số {n} – cấu trúc từ 2025","note":"Đề luyện theo cấu trúc 22 câu từ năm 2025: 12 trắc nghiệm, 4 đúng/sai, 6 trả lời ngắn, 90 phút.","d":d} if newf else
          {"y":f"Luyện {n} (cấu trúc cũ)","fmt":"old","title":f"Đề luyện tốt nghiệp THPT môn Toán số {n} – cấu trúc 50 câu","note":"Đề luyện theo cấu trúc 50 câu trắc nghiệm (2017–2024), 0,2 điểm/câu, 90 phút.","d":{"P1":d,"P2":[],"P3":[]}})
    add({"cat":"dh","g":g,"y":full["y"],"fmt":full["fmt"],"title":full["title"],"note":full["note"]},full)
for j in range(5):
    newf=j<4
    pr=try_make(lambda sd,tr:parts(vnw if newf else vo,sd+200+j,tr))
    if pr is None: skipped.append("V10");continue
    g="V10new" if newf else "V10old";n=cnt[g]=cnt.get(g,0)+1
    full={"y":0,"lab":f"Đề luyện {n}" if newf else f"Đề luyện cũ {n}","title":f"Đề luyện vào lớp 10 Hà Nội môn Toán số {n} – "+("cấu trúc từ 2025" if newf else "cấu trúc 2019–2024"),"note":"5 bài tự luận, 120 phút, thang 10; phần tự luận chuyển thành ô ghi đáp số." if newf else "Cấu trúc cũ: rút gọn biểu thức, lập phương trình/hệ, hệ phương trình và parabol, đường tròn, cực trị.","parts":pr}
    add({"cat":"v10","g":g,"lab":full["lab"],"title":full["title"],"note":full["note"]},full)
for j,(m,name) in enumerate([("CHUNG","Đề chung các trường"),("CHUNG","Đề chung các trường"),("CG","Cầu Giấy"),(("NS","Ngôi Sao Hà Nội") if N%2 else ("NTT","Nguyễn Tất Thành"))]):
    def mk(sd,tr):
        qs=intl_build(gens,mc,sd+300+j,0,20,4,tr,key="vi");return qs,(0 if len(qs)==20 else 1)
    qs=try_make(mk)
    if qs is None: skipped.append("HN");continue
    g="HN_"+m;n=cnt[g]=cnt.get(g,0)+1
    full={"name":name,"year":f"Đề luyện số {n}","min":60,"note":"Đề luyện 20 câu điền đáp số × 0,5 điểm theo các dạng hay gặp trong đề vào lớp 6 CLC và thi học bổng.","parts":[["Điền đáp số (20 câu × 0,5 điểm)",[{"t":q["t"],"d":q["t"],"q":q["vi"],"a":q["a"],"f":True,"p":0.5,"h":q["h"],"s":q["s"],"m":q["m"]} for q in qs]]]}
    add({"cat":"hn","g":g,"m":m,"name":name,"year":full["year"],"min":60,"note":full["note"]},full)
if not items: print("nothing new (all variants used)");sys.exit(0)
open(os.path.join(OUT,f"b{N}.js"),"w").write("Object.assign(window.AUTO_DATA=window.AUTO_DATA||{},"+json.dumps(data,ensure_ascii=False,separators=(",",":"))+");\n")
M.append({"n":N,"items":items})
open(MF,"w").write("window.AUTO_M="+json.dumps(M,ensure_ascii=False,separators=(",",":"))+";\n")
open(SF,"w").write("\n".join(sorted(seen))+"\n")
print("batch",N,"papers",len(items),"skipped",skipped,"seen",len(seen))
