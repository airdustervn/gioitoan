"""Câu luyện tập theo Chương trình GDPT 2018 môn Toán (lớp 1–12), chia theo chương và mạch nội dung.
Mỗi mẫu là hàm r -> câu hỏi; số liệu ngẫu nhiên, đáp án tính bằng máy. Dùng bởi build_ct.py."""
import math, random
from fractions import Fraction as Fr

def vn(x):
    if isinstance(x,Fr):
        return str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"
    if isinstance(x,float):
        if abs(x-round(x))<1e-9: x=int(round(x))
        else: return (f"{x:.4f}".rstrip("0").rstrip(".")).replace(".",",").replace("-","−")
    return str(x).replace("-","−")
def fa(x):  # đáp án ô điền: dấu chấm thập phân, dấu trừ thường
    if isinstance(x,Fr): return str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"
    if isinstance(x,float):
        if abs(x-round(x))<1e-9: return str(int(round(x)))
        return f"{x:.4f}".rstrip("0").rstrip(".")
    return str(x)
def MC(r,t,d,q,ans,dis,h,s,m):
    ans=str(ans);o=[ans]
    for x in dis:
        x=str(x)
        if x not in o: o.append(x)
        if len(o)==4: break
    if len(o)<3: return None
    r.shuffle(o);return {"t":t,"d":d,"q":q,"o":o,"a":o.index(ans),"h":h,"s":s if isinstance(s,list) else [s],"m":m,"p":1}
def FL(t,d,q,ans,h,s,m):
    return {"t":t,"d":d,"q":q,"a":fa(ans),"f":True,"h":h,"s":s if isinstance(s,list) else [s],"m":m,"p":1}
def near(r,v,k=3,step=1,low=None):
    out=[];c=[v+i*step for i in range(-k-2,k+3) if i]
    r.shuffle(c)
    for x in c:
        if low is not None and x<low: continue
        out.append(vn(x))
    return out
SH,HH,DS,TK,XS,GT,LG,TH="Số học","Hình học","Đại số","Thống kê","Xác suất","Giải tích","Lượng giác","Tổ hợp"
DAYS=["thứ Hai","thứ Ba","thứ Tư","thứ Năm","thứ Sáu","thứ Bảy","Chủ nhật"]
NM=["An","Bình","Chi","Dũng","Hà","Lan","Mai","Minh","Nam","Phúc"]

T={}  # (lớp, chương) -> [mẫu]
def reg(g,c):
    def deco(f):
        T.setdefault((g,c),[]).append(f);return f
    return deco

# ======================= LỚP 1 =======================
@reg(1,"Các số từ 0 đến 10")
def _(r):
    a,b=r.sample(range(0,11),2);big=max(a,b)
    return MC(r,SH,"So sánh số",f"Trong hai số {a} và {b}, số nào lớn hơn?",big,[min(a,b),a+b if a+b<=10 else abs(a-b),10 if big!=10 else 9],"Số nào đếm sau thì lớn hơn.",f"{big} lớn hơn {min(a,b)}.","Đếm từ 0 đến 10: số đứng sau lớn hơn.")
@reg(1,"Các số từ 0 đến 10")
def _(r):
    n=r.randint(1,9)
    return FL(SH,"Số liền sau",f"Số liền sau của số {n} là số nào?",n+1,"Số liền sau hơn số đó 1 đơn vị.",f"{n} + 1 = {n+1}.","Liền sau: thêm 1; liền trước: bớt 1.")
@reg(1,"Các số từ 0 đến 10")
def _(r):
    xs=sorted(r.sample(range(0,11),4));sh=xs[:];r.shuffle(sh)
    return MC(r,SH,"Sắp xếp",f"Số bé nhất trong các số {', '.join(map(str,sh))} là:",xs[0],[xs[1],xs[3],xs[2]],"So sánh từng cặp số.",f"Số bé nhất là {xs[0]}.","Số bé nhất đứng đầu khi xếp từ bé đến lớn.")
@reg(1,"Phép cộng, phép trừ trong phạm vi 10")
def _(r):
    a=r.randint(1,8);b=r.randint(1,10-a)
    return FL(SH,"Phép cộng",f"Tính: {a} + {b} = ?",a+b,"Đếm thêm.",f"{a} + {b} = {a+b}.","Đếm thêm từ số lớn hơn.")
@reg(1,"Phép cộng, phép trừ trong phạm vi 10")
def _(r):
    a=r.randint(3,10);b=r.randint(1,a)
    return MC(r,SH,"Phép trừ",f"{a} − {b} = ?",a-b,near(r,a-b,low=0),"Bớt đi rồi đếm phần còn lại.",f"{a} − {b} = {a-b}.","Trừ là bớt đi.")
@reg(1,"Phép cộng, phép trừ trong phạm vi 10")
def _(r):
    a=r.randint(2,8);c=r.randint(a+1,10);nm=r.choice(NM)
    return FL(SH,"Bài toán có lời văn",f"{nm} có {a} quả táo, mẹ cho thêm một số quả nữa thì {nm} có tất cả {c} quả. Mẹ cho {nm} mấy quả?",c-a,"Lấy số quả có tất cả trừ số quả lúc đầu.",f"{c} − {a} = {c-a} (quả).","Tìm số hạng chưa biết: lấy tổng trừ số hạng đã biết.")
@reg(1,"Các số trong phạm vi 100")
def _(r):
    n=r.randint(11,99)
    return FL(SH,"Chục và đơn vị",f"Số {n} gồm mấy chục và mấy đơn vị? Ghi số chục.",n//10,"Chữ số bên trái chỉ số chục.",f"{n} gồm {n//10} chục và {n%10} đơn vị.","Hàng chục bên trái, hàng đơn vị bên phải.")
@reg(1,"Các số trong phạm vi 100")
def _(r):
    a,b=r.sample(range(10,100),2)
    s="<" if a<b else ">"
    return MC(r,SH,"So sánh số có hai chữ số",f"Điền dấu thích hợp: {a} … {b}",s,["<" if s==">" else ">","=","+"],"So sánh chữ số hàng chục trước.",f"{a} {s} {b}.","Hàng chục lớn hơn thì số lớn hơn.")
@reg(1,"Các số trong phạm vi 100")
def _(r):
    t=r.randint(1,9);u=r.randint(0,9)
    return FL(SH,"Viết số",f"Số gồm {t} chục và {u} đơn vị là số nào?",10*t+u,"Viết chữ số chục rồi chữ số đơn vị.",f"{t} chục {u} đơn vị là {10*t+u}.","Chục đứng trước, đơn vị đứng sau.")
@reg(1,"Cộng, trừ trong phạm vi 100")
def _(r):
    a=r.randint(1,8)*10+r.randint(0,4);b=r.randint(1,9-a//10)*10+r.randint(0,5)
    if (a%10)+(b%10)>9: b=b-b%10
    return FL(SH,"Cộng không nhớ",f"Tính: {a} + {b}",a+b,"Cộng đơn vị với đơn vị, chục với chục.",f"{a} + {b} = {a+b}.","Đặt tính thẳng hàng.")
@reg(1,"Cộng, trừ trong phạm vi 100")
def _(r):
    a=r.randint(4,9)*10+r.randint(5,9);b=r.randint(1,a//10-1)*10+r.randint(0,a%10)
    return MC(r,SH,"Trừ không nhớ",f"{a} − {b} = ?",a-b,near(r,a-b,step=r.choice([1,10]),low=0),"Trừ đơn vị rồi trừ chục.",f"{a} − {b} = {a-b}.","Đặt tính rồi trừ từ phải sang trái.")
@reg(1,"Cộng, trừ trong phạm vi 100")
def _(r):
    a=r.randint(2,6)*10;b=r.randint(1,3)*10;nm=r.choice(NM)
    return FL(SH,"Bài toán có lời văn",f"Lớp 1A có {a} quyển truyện, lớp 1B có {b} quyển truyện. Cả hai lớp có bao nhiêu quyển truyện?",a+b,"Gộp lại thì làm phép cộng.",f"{a} + {b} = {a+b} (quyển).","“Cả hai” → phép cộng.")
@reg(1,"Hình phẳng và hình khối")
def _(r):
    sh=r.choice([("hình tam giác",3),("hình vuông",4),("hình chữ nhật",4)]);n=r.randint(2,4)
    return FL(HH,"Đếm cạnh",f"{n} {sh[0]} rời nhau có tất cả bao nhiêu cạnh?",n*sh[1],f"Mỗi {sh[0]} có {sh[1]} cạnh.",f"{n} × {sh[1]} = {n*sh[1]}.","Tam giác 3 cạnh, hình vuông 4 cạnh.")
@reg(1,"Hình phẳng và hình khối")
def _(r):
    x=r.choice([("Quả bóng","khối cầu"),("Hộp sữa","khối hộp chữ nhật"),("Viên xúc xắc","khối lập phương"),("Lon nước ngọt","khối trụ")])
    return MC(r,HH,"Nhận dạng hình khối",f"{x[0]} có dạng hình gì?",x[1],[y for y in ["khối cầu","khối hộp chữ nhật","khối lập phương","khối trụ"] if y!=x[1]],"Quan sát hình dạng đồ vật.",f"{x[0]} có dạng {x[1]}.","Liên hệ đồ vật quen thuộc với hình khối.")
@reg(1,"Hình phẳng và hình khối")
def _(r):
    n=r.choice([2,3])
    return FL(HH,"Đếm hình vuông",f"Một tấm bảng được chia thành lưới {n} × {n} ô vuông nhỏ. Có bao nhiêu ô vuông nhỏ?",n*n,"Đếm số hàng và số ô mỗi hàng.",f"{n} hàng, mỗi hàng {n} ô: {n*n} ô.","Đếm theo hàng.")
@reg(1,"Vị trí, định hướng trong không gian")
def _(r):
    L=r.sample(NM,5);i=r.randint(1,3)
    return MC(r,HH,"Trước – sau",f"Năm bạn xếp hàng theo thứ tự từ đầu hàng: {', '.join(L)}. Bạn đứng ngay sau {L[i]} là ai?",L[i+1],[L[i-1],L[0],L[4] if i+1!=4 else L[2]],"Sau là đứng phía cuối hàng.",f"Ngay sau {L[i]} là {L[i+1]}.","Trước – sau theo chiều đi của hàng.")
@reg(1,"Vị trí, định hướng trong không gian")
def _(r):
    a,b=r.randint(2,8),r.randint(2,8)
    return FL(HH,"Đếm vị trí",f"Trong một hàng, Mai đứng thứ {a} tính từ bên trái và thứ {b} tính từ bên phải. Hàng có bao nhiêu bạn?",a+b-1,"Mai được đếm hai lần.",f"{a} + {b} − 1 = {a+b-1}.","Trừ 1 vì đếm trùng.")
@reg(1,"Vị trí, định hướng trong không gian")
def _(r):
    x=r.choice([("trên","dưới"),("trái","phải"),("trước","sau")])
    return MC(r,HH,"Vị trí",f"Quả bóng ở bên {x[0]} cái hộp. Vậy cái hộp ở bên … quả bóng.",x[1],[x[0],"giữa","cạnh"] if x[0]!="trên" else ["trên","giữa","cạnh"],"Đổi chỗ người quan sát.",f"Cái hộp ở bên {x[1]} quả bóng.","Hai vị trí ngược nhau: trên – dưới, trái – phải, trước – sau.")
@reg(1,"Độ dài và đo độ dài")
def _(r):
    a,b=r.randint(3,15),r.randint(2,12)
    return FL(HH,"Cộng độ dài",f"Đoạn thẳng AB dài {a} cm, đoạn thẳng BC dài {b} cm. Đoạn gấp khúc ABC dài bao nhiêu xăng-ti-mét?",a+b,"Cộng độ dài các đoạn.",f"{a} + {b} = {a+b} (cm).","Đơn vị đo độ dài: xăng-ti-mét (cm).")
@reg(1,"Độ dài và đo độ dài")
def _(r):
    a=r.randint(10,40);b=r.randint(2,a-2)
    return MC(r,HH,"So sánh độ dài",f"Bút chì dài {a} cm, cục tẩy dài {b} cm. Bút chì dài hơn cục tẩy bao nhiêu xăng-ti-mét?",f"{a-b} cm",[f"{a+b} cm",f"{a-b+1} cm",f"{a-b-1} cm"],"Dài hơn: lấy hiệu.",f"{a} − {b} = {a-b} (cm).","Hơn bao nhiêu → phép trừ.")
@reg(1,"Độ dài và đo độ dài")
def _(r):
    k=r.randint(3,9)
    return FL(HH,"Đo bằng gang tay",f"Mặt bàn dài {k} gang tay của bạn Nam. Nếu mỗi gang tay dài 10 cm thì mặt bàn dài bao nhiêu xăng-ti-mét?",10*k,"Đếm thêm 10.",f"{k} chục cm = {10*k} cm.","Đếm theo chục.")
@reg(1,"Thời gian: giờ và lịch")
def _(r):
    st=r.randint(0,6);k=r.randint(1,6)
    return MC(r,SH,"Ngày trong tuần",f"Hôm nay là {DAYS[st]}. {k} ngày nữa là thứ mấy?",DAYS[(st+k)%7],[DAYS[(st+k+1)%7],DAYS[(st+k-1)%7],DAYS[(st+k+2)%7]],"Đếm tiếp từng ngày.",f"Sau {k} ngày là {DAYS[(st+k)%7]}.","Một tuần có 7 ngày.")
@reg(1,"Thời gian: giờ và lịch")
def _(r):
    h=r.randint(1,10);k=r.randint(1,12-h)
    return FL(SH,"Xem giờ",f"Bây giờ là {h} giờ đúng. Sau {k} giờ nữa là mấy giờ?",h+k,"Cộng thêm số giờ.",f"{h} + {k} = {h+k} giờ.","Kim ngắn chỉ giờ, kim dài chỉ phút.")
@reg(1,"Thời gian: giờ và lịch")
def _(r):
    h=r.randint(1,12)
    return MC(r,SH,"Kim đồng hồ",f"Lúc {h} giờ đúng, kim dài (kim phút) chỉ vào số nào?",12,[h if h!=12 else 6,6,3],"Giờ đúng thì kim phút chỉ số 12.","Kim phút chỉ số 12.","Giờ đúng: kim dài chỉ 12.")

# ======================= LỚP 2 =======================
@reg(2,"Phép cộng, phép trừ trong phạm vi 100")
def _(r):
    while True:
        a=r.randint(15,68);b=r.randint(15,99-a)
        if (a%10)+(b%10)>=10: break
    return FL(SH,"Cộng có nhớ",f"Tính: {a} + {b}",a+b,"Cộng đơn vị, nhớ 1 sang hàng chục.",f"{a} + {b} = {a+b}.","Đủ 10 đơn vị thì nhớ 1 chục.")
@reg(2,"Phép cộng, phép trừ trong phạm vi 100")
def _(r):
    while True:
        a=r.randint(40,99);b=r.randint(11,a-10)
        if (a%10)<(b%10): break
    return MC(r,SH,"Trừ có nhớ",f"{a} − {b} = ?",a-b,near(r,a-b,step=r.choice([1,10]),low=0),"Mượn 1 chục ở hàng chục.",f"{a} − {b} = {a-b}.","Không trừ được thì mượn 1 chục.")
@reg(2,"Phép cộng, phép trừ trong phạm vi 100")
def _(r):
    a=r.randint(25,60);b=r.randint(8,a-5);nm=r.choice(NM)
    return FL(SH,"Bài toán ít hơn",f"{nm} có {a} viên bi, Hà có ít hơn {nm} {b} viên bi. Hà có bao nhiêu viên bi?",a-b,"Ít hơn → phép trừ.",f"{a} − {b} = {a-b} (viên).","Nhiều hơn: cộng; ít hơn: trừ.")
@reg(2,"Các số trong phạm vi 1000")
def _(r):
    n=r.randint(101,999)
    return FL(SH,"Cấu tạo số",f"Số {n} có chữ số hàng chục là bao nhiêu?",(n//10)%10,"Hàng trăm – chục – đơn vị.",f"{n} = {n//100} trăm {(n//10)%10} chục {n%10} đơn vị.","Đọc từ trái sang: trăm, chục, đơn vị.")
@reg(2,"Các số trong phạm vi 1000")
def _(r):
    a,b,c=r.randint(1,9),r.randint(0,9),r.randint(0,9)
    return MC(r,SH,"Viết số",f"Số gồm {a} trăm, {b} chục và {c} đơn vị là:",100*a+10*b+c,[100*a+b+10*c,100*a+10*c+b,10*a+b*100+c if b else 100*a+10*b+c+10],"Viết lần lượt trăm, chục, đơn vị.",f"{a}{b}{c}.","Hàng nào không có thì viết 0.")
@reg(2,"Các số trong phạm vi 1000")
def _(r):
    xs=r.sample(range(100,1000),4)
    return MC(r,SH,"So sánh số",f"Số lớn nhất trong các số {', '.join(map(str,xs))} là:",max(xs),[x for x in xs if x!=max(xs)],"So sánh hàng trăm trước.",f"Số lớn nhất là {max(xs)}.","Hàng trăm bằng nhau thì so hàng chục.")
@reg(2,"Cộng, trừ trong phạm vi 1000")
def _(r):
    a=r.randint(120,560);b=r.randint(110,430)
    return FL(SH,"Cộng số có ba chữ số",f"Tính: {a} + {b}",a+b,"Đặt tính và cộng từ phải sang trái.",f"{a} + {b} = {a+b}.","Nhớ khi tổng một hàng ≥ 10.")
@reg(2,"Cộng, trừ trong phạm vi 1000")
def _(r):
    a=r.randint(500,999);b=r.randint(105,a-100)
    return MC(r,SH,"Trừ số có ba chữ số",f"{a} − {b} = ?",a-b,near(r,a-b,step=r.choice([1,10,100]),low=0),"Đặt tính, trừ từ hàng đơn vị.",f"{a} − {b} = {a-b}.","Thử lại: hiệu + số trừ = số bị trừ.")
@reg(2,"Cộng, trừ trong phạm vi 1000")
def _(r):
    a=r.randint(200,500);b=r.randint(50,300)
    return FL(SH,"Bài toán nhiều hơn",f"Thùng thứ nhất có {a} lít nước, thùng thứ hai nhiều hơn thùng thứ nhất {b} lít. Thùng thứ hai có bao nhiêu lít?",a+b,"Nhiều hơn → cộng.",f"{a} + {b} = {a+b} (lít).","Nhiều hơn: cộng thêm.")
@reg(2,"Phép nhân, phép chia")
def _(r):
    k=r.choice([2,5]);n=r.randint(2,10)
    return FL(SH,"Bảng nhân",f"Tính: {k} × {n}",k*n,f"Bảng nhân {k}.",f"{k} × {n} = {k*n}.","Nhân là cộng các số hạng bằng nhau.")
@reg(2,"Phép nhân, phép chia")
def _(r):
    k=r.choice([2,5]);n=r.randint(2,10)
    return MC(r,SH,"Phép chia",f"{k*n} : {k} = ?",n,near(r,n,low=1),f"Dựa vào bảng nhân {k}.",f"{k} × {n} = {k*n} nên {k*n} : {k} = {n}.","Chia là phép ngược của nhân.")
@reg(2,"Phép nhân, phép chia")
def _(r):
    k=r.choice([2,5]);n=r.randint(3,9)
    return FL(SH,"Bài toán nhân",f"Mỗi đĩa có {k} quả cam. {n} đĩa như thế có bao nhiêu quả cam?",k*n,"Nhân số quả mỗi đĩa với số đĩa.",f"{k} × {n} = {k*n} (quả).","Nhiều nhóm bằng nhau → phép nhân.")
@reg(2,"Điểm, đoạn thẳng, đường gấp khúc, tứ giác")
def _(r):
    xs=[r.randint(2,9) for _ in range(r.randint(3,4))]
    return FL(HH,"Độ dài đường gấp khúc",f"Đường gấp khúc gồm các đoạn thẳng dài {', '.join(map(str,xs))} cm. Đường gấp khúc dài bao nhiêu xăng-ti-mét?",sum(xs),"Cộng độ dài các đoạn.",f"{' + '.join(map(str,xs))} = {sum(xs)} (cm).","Độ dài đường gấp khúc = tổng các đoạn.")
@reg(2,"Điểm, đoạn thẳng, đường gấp khúc, tứ giác")
def _(r):
    n=r.randint(3,6)
    return FL(TH,"Đếm đoạn thẳng",f"Trên một đường thẳng có {n} điểm. Có bao nhiêu đoạn thẳng có hai đầu là hai trong các điểm đó?",n*(n-1)//2,"Mỗi điểm nối với các điểm còn lại.",f"{' + '.join(str(i) for i in range(n-1,0,-1))} = {n*(n-1)//2}.","Đếm có thứ tự để không sót.")
@reg(2,"Điểm, đoạn thẳng, đường gấp khúc, tứ giác")
def _(r):
    return MC(r,HH,"Nhận dạng tứ giác","Hình nào dưới đây là hình tứ giác?","Hình có 4 cạnh và 4 đỉnh",["Hình có 3 cạnh","Hình có 5 cạnh","Hình tròn"],"Tứ giác có 4 cạnh.","Tứ giác là hình có 4 cạnh, 4 đỉnh.","Tứ = bốn.")
@reg(2,"Hình khối: khối trụ, khối cầu")
def _(r):
    x=r.choice([("Quả địa cầu","khối cầu"),("Hộp bút hình ống","khối trụ"),("Viên bi","khối cầu"),("Cái trống","khối trụ")])
    return MC(r,HH,"Nhận dạng khối",f"{x[0]} có dạng:",x[1],["khối lập phương","khối hộp chữ nhật","khối cầu" if x[1]=="khối trụ" else "khối trụ"],"Khối cầu tròn đều mọi phía; khối trụ có hai đáy tròn.",f"{x[0]} có dạng {x[1]}.","Khối trụ lăn được và đứng được.")
@reg(2,"Hình khối: khối trụ, khối cầu")
def _(r):
    a,b=r.randint(2,6),r.randint(2,6)
    return FL(HH,"Đếm hình khối",f"Trên kệ có {a} khối trụ và {b} khối cầu. Có tất cả bao nhiêu khối?",a+b,"Cộng số khối.",f"{a} + {b} = {a+b}.","Gộp lại → cộng.")
@reg(2,"Hình khối: khối trụ, khối cầu")
def _(r):
    return MC(r,HH,"Đặc điểm hình khối","Khối nào có thể vừa lăn được vừa đặt đứng yên được trên mặt bàn?","Khối trụ",["Khối cầu","Khối lập phương","Khối hộp chữ nhật"],"Nghĩ đến lon nước.","Khối trụ có mặt cong để lăn và mặt đáy phẳng để đứng.","Khối cầu chỉ lăn; khối hộp chỉ đứng.")
@reg(2,"Đo lường: ki-lô-gam, lít, mét, ki-lô-mét")
def _(r):
    a,b=r.randint(10,40),r.randint(5,30)
    return FL(HH,"Ki-lô-gam",f"Bao gạo nặng {a} kg, bao ngô nặng {b} kg. Cả hai bao nặng bao nhiêu ki-lô-gam?",a+b,"Cộng khối lượng.",f"{a} + {b} = {a+b} (kg).","Cùng đơn vị mới cộng được.")
@reg(2,"Đo lường: ki-lô-gam, lít, mét, ki-lô-mét")
def _(r):
    m=r.randint(1,9)
    return MC(r,HH,"Đổi đơn vị",f"{m} m = … dm",m*10,[m,m*100,m*10+1],"1 m = 10 dm.",f"{m} m = {m*10} dm.","m → dm: nhân 10.")
@reg(2,"Đo lường: ki-lô-gam, lít, mét, ki-lô-mét")
def _(r):
    a=r.randint(20,60);b=r.randint(5,a-5)
    return FL(HH,"Lít",f"Can to có {a} l dầu, đã rót ra {b} l. Can còn lại bao nhiêu lít dầu?",a-b,"Còn lại → trừ.",f"{a} − {b} = {a-b} (l).","Lít (l) đo lượng chất lỏng.")
@reg(2,"Thời gian: ngày, giờ, tháng")
def _(r):
    h=r.randint(7,11);k=r.randint(2,5)
    return FL(SH,"Giờ",f"Lan bắt đầu học lúc {h} giờ sáng và học trong {k} giờ. Lan học xong lúc mấy giờ?",h+k if h+k<=12 else h+k-12,"Cộng thêm số giờ.",f"{h} + {k} = {h+k} giờ.","1 ngày có 24 giờ.")
@reg(2,"Thời gian: ngày, giờ, tháng")
def _(r):
    d=r.randint(1,20);k=r.randint(3,9)
    return MC(r,SH,"Ngày trong tháng",f"Hôm nay là ngày {d} tháng 5. {k} ngày nữa là ngày bao nhiêu tháng 5?",d+k,[d+k-1,d+k+1,d-k if d>k else d+k+7],"Cộng số ngày.",f"{d} + {k} = {d+k}.","Tháng 5 có 31 ngày.")
@reg(2,"Thời gian: ngày, giờ, tháng")
def _(r):
    m=r.choice([("tháng 1",31),("tháng 4",30),("tháng 6",30),("tháng 7",31),("tháng 9",30),("tháng 12",31)])
    return MC(r,SH,"Số ngày trong tháng",f"{m[0].capitalize()} có bao nhiêu ngày?",m[1],[30 if m[1]==31 else 31,28,29],"Đếm theo nắm tay.",f"{m[0].capitalize()} có {m[1]} ngày.","Tháng 4, 6, 9, 11 có 30 ngày.")
@reg(2,"Tiền Việt Nam")
def _(r):
    a,b=r.choice([(1000,2000),(2000,5000),(5000,10000),(1000,5000)]);x,y=r.randint(1,4),r.randint(1,3)
    return FL(SH,"Cộng tiền",f"Mẹ có {x} tờ {a} đồng và {y} tờ {b} đồng. Mẹ có tất cả bao nhiêu đồng?",x*a+y*b,"Tính từng loại rồi cộng.",f"{x*a} + {y*b} = {x*a+y*b} (đồng).","Cộng các tờ tiền.")
@reg(2,"Tiền Việt Nam")
def _(r):
    p=r.choice([3000,4000,6000,7000,8000]);B=10000
    return MC(r,SH,"Trả lại tiền",f"Hà mua một quyển vở giá {p} đồng, đưa cô bán hàng tờ {B} đồng. Cô trả lại Hà bao nhiêu tiền?",f"{B-p} đồng",[f"{B+p} đồng",f"{B-p+1000} đồng",f"{p} đồng"],"Lấy tiền đưa trừ tiền vở.",f"{B} − {p} = {B-p} (đồng).","Tiền thừa = tiền đưa − giá tiền.")
@reg(2,"Tiền Việt Nam")
def _(r):
    k=r.randint(2,5)
    return FL(SH,"Đổi tiền",f"Một tờ 10 000 đồng đổi được bao nhiêu tờ 2000 đồng?",5,"Đếm thêm 2000.","2000 × 5 = 10 000.","Chia đều mệnh giá lớn.")
@reg(2,"Thống kê và xác suất")
def _(r):
    a,b,c=r.randint(2,9),r.randint(2,9),r.randint(2,9)
    return FL(TK,"Kiểm đếm",f"Kết quả kiểm đếm số quả trong rổ: táo {a}, cam {b}, lê {c}. Trong rổ có tất cả bao nhiêu quả?",a+b+c,"Cộng các số liệu.",f"{a} + {b} + {c} = {a+b+c}.","Kiểm đếm rồi cộng.")
@reg(2,"Thống kê và xác suất")
def _(r):
    x=r.choice([("Mặt trời mọc ở đằng Đông","chắc chắn"),("Tung đồng xu được mặt ngửa","có thể"),("Thả hòn đá vào nước thì hòn đá bay lên","không thể")])
    return MC(r,XS,"Khả năng xảy ra",f"Sự kiện “{x[0]}” là:",x[1],[y for y in ["chắc chắn","có thể","không thể"] if y!=x[1]]+["luôn luôn sai"],"Xét sự kiện có luôn xảy ra không.",f"Đó là sự kiện {x[1]}.","Chắc chắn – có thể – không thể.")
@reg(2,"Thống kê và xác suất")
def _(r):
    a,b=r.randint(5,12),r.randint(3,10)
    return MC(r,TK,"Biểu đồ tranh",f"Biểu đồ tranh: lớp 2A có {a} bạn thích bóng đá, {b} bạn thích cầu lông. Số bạn thích bóng đá nhiều hơn số bạn thích cầu lông là:",abs(a-b) if a>b else 0,[a+b,abs(a-b)+1,abs(a-b)+2] if a>b else [1,2,a+b],"Lấy hiệu hai số liệu.",f"{a} − {b} = {a-b}." if a>b else "Không nhiều hơn.","Đọc số liệu trên biểu đồ.") if a!=b else None

# ======================= LỚP 3 =======================
@reg(3,"Bảng nhân, bảng chia")
def _(r):
    k=r.randint(6,9);n=r.randint(3,10)
    return FL(SH,"Bảng nhân",f"Tính: {k} × {n}",k*n,f"Bảng nhân {k}.",f"{k} × {n} = {k*n}.","Thuộc bảng nhân 6, 7, 8, 9.")
@reg(3,"Bảng nhân, bảng chia")
def _(r):
    k=r.randint(6,9);n=r.randint(3,10)
    return MC(r,SH,"Bảng chia",f"{k*n} : {k} = ?",n,near(r,n,low=1),f"Bảng chia {k}.",f"{k*n} : {k} = {n}.","Chia ngược với nhân.")
@reg(3,"Bảng nhân, bảng chia")
def _(r):
    k=r.randint(3,9);n=r.randint(3,9)
    return FL(SH,"Gấp lên nhiều lần",f"Bao xanh có {n} kg, bao đỏ nặng gấp {k} lần bao xanh. Bao đỏ nặng bao nhiêu ki-lô-gam?",k*n,"Gấp lên → nhân.",f"{n} × {k} = {k*n} (kg).","Gấp lên: nhân; giảm đi: chia.")
@reg(3,"Các số trong phạm vi 10 000 và 100 000")
def _(r):
    n=r.randint(10000,99999)
    return FL(SH,"Hàng nghìn",f"Chữ số hàng nghìn của số {n} là chữ số nào?",(n//1000)%10,"Hàng: chục nghìn – nghìn – trăm – chục – đơn vị.",f"{n}: hàng nghìn là {(n//1000)%10}.","Đếm hàng từ phải sang trái.")
@reg(3,"Các số trong phạm vi 10 000 và 100 000")
def _(r):
    n=r.randint(1000,99999);k=r.choice([10,100,1000]);rd=int(round(n/k))*k
    if abs(n/k-round(n/k))==.5: n+=1;rd=int(round(n/k))*k
    return MC(r,SH,"Làm tròn số",f"Làm tròn số {n} đến hàng {'chục' if k==10 else 'trăm' if k==100 else 'nghìn'} được:",rd,[rd+k,rd-k,n//k*k if n//k*k!=rd else rd+2*k],"Xét chữ số ngay bên phải hàng làm tròn.",f"{n} ≈ {rd}.","Chữ số bên phải ≥ 5 thì làm tròn lên.")
@reg(3,"Các số trong phạm vi 10 000 và 100 000")
def _(r):
    a=r.randint(10,99)*1000;b=r.randint(1,9)*1000
    return FL(SH,"Cộng nghìn tròn",f"Tính nhẩm: {a} + {b}",a+b,"Cộng số nghìn.",f"{a//1000} nghìn + {b//1000} nghìn = {(a+b)//1000} nghìn.","Nhẩm theo nghìn.")
@reg(3,"Nhân, chia với số có một chữ số")
def _(r):
    a=r.randint(1012,4999);k=r.randint(2,9)
    if a*k>99999: k=2
    return FL(SH,"Nhân với số có một chữ số",f"Tính: {a} × {k}",a*k,"Nhân từ hàng đơn vị.",f"{a} × {k} = {a*k}.","Nhân rồi cộng phần nhớ.")
@reg(3,"Nhân, chia với số có một chữ số")
def _(r):
    k=r.randint(2,9);q=r.randint(100,999);rem=r.randint(0,k-1);n=k*q+rem
    return MC(r,SH,"Chia có dư",f"Số dư của phép chia {n} : {k} là:",rem,[x for x in range(k) if x!=rem][:2]+[k],"Số dư nhỏ hơn số chia.",f"{n} = {k} × {q} + {rem}.","Số dư luôn bé hơn số chia.")
@reg(3,"Nhân, chia với số có một chữ số")
def _(r):
    k=r.randint(3,8);n=k*r.randint(12,60)
    return FL(SH,"Bài toán chia",f"Có {n} quyển sách xếp đều vào {k} ngăn. Mỗi ngăn có bao nhiêu quyển?",n//k,"Chia đều → phép chia.",f"{n} : {k} = {n//k} (quyển).","Chia đều thành các phần bằng nhau.")
@reg(3,"Biểu thức số")
def _(r):
    a,b,c=r.randint(10,90),r.randint(2,9),r.randint(2,9)
    return FL(SH,"Thứ tự thực hiện",f"Tính giá trị biểu thức: {a} + {b} × {c}",a+b*c,"Nhân trước, cộng sau.",f"{b} × {c} = {b*c}; {a} + {b*c} = {a+b*c}.","Nhân, chia trước; cộng, trừ sau.")
@reg(3,"Biểu thức số")
def _(r):
    a,b,c=r.randint(20,60),r.randint(5,19),r.randint(2,6)
    return MC(r,SH,"Biểu thức có ngoặc",f"Giá trị của biểu thức ({a} + {b}) × {c} là:",(a+b)*c,[a+b*c,(a+b)*c+c,(a+b)*(c+1)],"Trong ngoặc làm trước.",f"({a} + {b}) × {c} = {a+b} × {c} = {(a+b)*c}.","Có ngoặc: tính trong ngoặc trước.")
@reg(3,"Biểu thức số")
def _(r):
    a,b,c=r.randint(50,99),r.randint(10,40),r.randint(2,9)
    v=a-b+c
    return FL(SH,"Cộng trừ từ trái sang phải",f"Tính: {a} − {b} + {c}",v,"Chỉ có cộng, trừ: làm từ trái sang phải.",f"{a-b} + {c} = {v}.","Cùng cấp: trái sang phải.")
@reg(3,"Làm quen với phân số")
def _(r):
    k=r.randint(2,9);n=k*r.randint(2,10)
    return FL(SH,"Một phần mấy",f"1/{k} của {n} là bao nhiêu?",n//k,f"Chia {n} thành {k} phần bằng nhau.",f"{n} : {k} = {n//k}.","Tìm 1/n của một số: chia cho n.")
@reg(3,"Làm quen với phân số")
def _(r):
    k=r.randint(2,8)
    return MC(r,SH,"Đọc phân số",f"Một cái bánh chia thành {k} phần bằng nhau, An ăn 1 phần. An đã ăn mấy phần cái bánh?",f"1/{k}",[f"{k}/1",f"1/{k+1}",f"{k-1}/{k}"],"Tử số là số phần lấy đi, mẫu số là số phần bằng nhau.",f"An ăn 1/{k} cái bánh.","Mẫu số: chia thành mấy phần.")
@reg(3,"Làm quen với phân số")
def _(r):
    a,b=r.sample(range(2,10),2)
    return MC(r,SH,"So sánh một phần mấy",f"So sánh 1/{a} và 1/{b}:",f"1/{a} {'>' if a<b else '<'} 1/{b}",[f"1/{a} {'<' if a<b else '>'} 1/{b}",f"1/{a} = 1/{b}","Không so sánh được"],"Chia càng nhiều phần thì mỗi phần càng nhỏ.",f"Vì {min(a,b)} < {max(a,b)} nên 1/{min(a,b)} lớn hơn.","Cùng tử 1: mẫu bé thì phân số lớn.")
@reg(3,"Góc, hình tam giác, hình tứ giác, hình tròn")
def _(r):
    rr=r.randint(2,15)
    return FL(HH,"Bán kính – đường kính",f"Hình tròn tâm O có bán kính {rr} cm. Đường kính của hình tròn dài bao nhiêu xăng-ti-mét?",2*rr,"Đường kính gấp đôi bán kính.",f"{rr} × 2 = {2*rr} (cm).","d = 2r.")
@reg(3,"Góc, hình tam giác, hình tứ giác, hình tròn")
def _(r):
    L=r.randint(4,30)*2
    return FL(HH,"Trung điểm",f"M là trung điểm của đoạn thẳng AB dài {L} cm. Đoạn AM dài bao nhiêu xăng-ti-mét?",L//2,"Trung điểm chia đôi đoạn thẳng.",f"{L} : 2 = {L//2} (cm).","AM = MB = AB : 2.")
@reg(3,"Góc, hình tam giác, hình tứ giác, hình tròn")
def _(r):
    x=r.choice([("hình vuông",4),("hình chữ nhật",4),("hình tam giác vuông",1)])
    return FL(HH,"Góc vuông",f"Một {x[0]} có bao nhiêu góc vuông?",x[1],"Dùng ê ke để kiểm tra.",f"{x[0].capitalize()} có {x[1]} góc vuông.","Hình vuông, hình chữ nhật có 4 góc vuông.")
@reg(3,"Chu vi và diện tích")
def _(r):
    a,b=r.randint(4,20),r.randint(2,12)
    return FL(HH,"Chu vi hình chữ nhật",f"Hình chữ nhật có chiều dài {a+b} cm, chiều rộng {b} cm. Tính chu vi (cm).",2*(a+2*b),"(dài + rộng) × 2.",f"({a+b} + {b}) × 2 = {2*(a+2*b)} (cm).","Chu vi HCN = (a + b) × 2.")
@reg(3,"Chu vi và diện tích")
def _(r):
    s=r.randint(3,12)
    return MC(r,HH,"Diện tích hình vuông",f"Diện tích hình vuông cạnh {s} cm là:",f"{s*s} cm²",[f"{4*s} cm²",f"{s*s} cm",f"{2*s} cm²"],"Cạnh × cạnh.",f"{s} × {s} = {s*s} (cm²).","Diện tích đo bằng cm².")
@reg(3,"Chu vi và diện tích")
def _(r):
    s=r.randint(3,15)
    return FL(HH,"Cạnh hình vuông",f"Một hình vuông có chu vi {4*s} cm. Cạnh hình vuông dài bao nhiêu xăng-ti-mét?",s,"Chu vi : 4.",f"{4*s} : 4 = {s} (cm).","Chu vi hình vuông = cạnh × 4.")
@reg(3,"Đo lường: mi-li-mét, gam, mi-li-lít, nhiệt độ")
def _(r):
    c=r.randint(2,30);m=r.randint(1,9)
    return FL(HH,"Đổi mm",f"{c} cm {m} mm = … mm",10*c+m,"1 cm = 10 mm.",f"{c} × 10 + {m} = {10*c+m}.","cm → mm: nhân 10.")
@reg(3,"Đo lường: mi-li-mét, gam, mi-li-lít, nhiệt độ")
def _(r):
    k=r.randint(1,4);g=r.randint(100,900)
    return MC(r,HH,"Đổi gam",f"{k} kg {g} g = … g",1000*k+g,[100*k+g,k+g,1000*k+g+100],"1 kg = 1000 g.",f"{k} × 1000 + {g} = {1000*k+g}.","kg → g: nhân 1000.")
@reg(3,"Đo lường: mi-li-mét, gam, mi-li-lít, nhiệt độ")
def _(r):
    a=r.randint(15,30);d=r.randint(3,10)
    return FL(HH,"Nhiệt độ",f"Buổi sáng nhiệt độ là {a} °C, buổi trưa tăng thêm {d} °C. Nhiệt độ buổi trưa là bao nhiêu độ C?",a+d,"Tăng thêm → cộng.",f"{a} + {d} = {a+d} (°C).","Đơn vị nhiệt độ: độ C (°C).")
@reg(3,"Thời gian, tháng – năm")
def _(r):
    h=r.randint(7,10);m=r.choice([10,15,20,25,30]);d=r.choice([25,35,40,45,50])
    t=h*60+m+d
    return FL(SH,"Cộng thời gian",f"Tiết học bắt đầu lúc {h} giờ {m} phút và kéo dài {d} phút. Tiết học kết thúc lúc mấy giờ bao nhiêu phút? (ghi giờ × 100 + phút, ví dụ 9 giờ 5 phút ghi 905)",(t//60)*100+t%60,"Cộng phút, đủ 60 phút thì đổi thành 1 giờ.",f"Kết thúc lúc {t//60} giờ {t%60} phút.","60 phút = 1 giờ.")
@reg(3,"Thời gian, tháng – năm")
def _(r):
    return MC(r,SH,"Tháng trong năm","Một năm có bao nhiêu tháng có 31 ngày?",7,[6,5,4],"Đếm theo nắm tay.","Tháng 1, 3, 5, 7, 8, 10, 12 có 31 ngày.","Đốt ngón tay là 31 ngày.")
@reg(3,"Thời gian, tháng – năm")
def _(r):
    w=r.randint(2,6);d=r.randint(1,6)
    return FL(SH,"Tuần lễ",f"{w} tuần {d} ngày là bao nhiêu ngày?",7*w+d,"1 tuần = 7 ngày.",f"{w} × 7 + {d} = {7*w+d}.","Một tuần lễ có 7 ngày.")
@reg(3,"Số La Mã")
def _(r):
    n=r.randint(1,20);R=["","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX"]
    return FL(SH,"Đọc số La Mã",f"Số La Mã {R[n]} có giá trị là bao nhiêu?",n,"I = 1, V = 5, X = 10.",f"{R[n]} = {n}.","Chữ số nhỏ đứng trước chữ số lớn thì trừ.")
@reg(3,"Số La Mã")
def _(r):
    n=r.choice([4,6,9,11,12,14,19]);R={4:"IV",6:"VI",9:"IX",11:"XI",12:"XII",14:"XIV",19:"XIX"};alt={4:["VI","IIII","IIV"],6:["IV","VII","IIV"],9:["XI","VIIII","IIX"],11:["IX","XII","IXI"],12:["XI","IIX","XIII"],14:["XVI","XIIII","IVX"],19:["XXI","XVIIII","IXX"]}
    return MC(r,SH,"Viết số La Mã",f"Số {n} viết bằng chữ số La Mã là:",R[n],alt[n],"I đứng trước V, X thì trừ 1.",f"{n} = {R[n]}.","Không viết một chữ số quá 3 lần liền.")
@reg(3,"Số La Mã")
def _(r):
    h=r.randint(1,12);R=["","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
    return FL(SH,"Đồng hồ La Mã",f"Kim giờ của đồng hồ chỉ vào số {R[h]}, kim phút chỉ vào số XII. Lúc đó là mấy giờ?",h,"Đọc số La Mã kim giờ chỉ.",f"{R[h]} = {h} → {h} giờ.","Kim phút chỉ XII: giờ đúng.")
@reg(3,"Thống kê và xác suất")
def _(r):
    xs=[r.randint(10,40) for _ in range(4)];L=["Thứ Hai","Thứ Ba","Thứ Tư","Thứ Năm"]
    return FL(TK,"Bảng số liệu",f"Số sách thư viện cho mượn: {', '.join(f'{L[i]} {xs[i]}' for i in range(4))} quyển. Cả bốn ngày cho mượn bao nhiêu quyển?",sum(xs),"Cộng các số liệu.",f"{' + '.join(map(str,xs))} = {sum(xs)}.","Đọc bảng số liệu.")
@reg(3,"Thống kê và xác suất")
def _(r):
    a,b=r.randint(2,6),r.randint(1,5)
    return MC(r,XS,"Khả năng",f"Trong hộp có {a} bi đỏ và {b} bi xanh. Lấy ra 1 viên bi. Khả năng lấy được bi màu nào nhiều hơn?","bi đỏ" if a>b else "bi xanh",["bi xanh" if a>b else "bi đỏ","như nhau","không lấy được"],"Màu nào nhiều bi hơn thì dễ lấy được hơn.",f"Đỏ {a}, xanh {b}.","Nhiều hơn → khả năng cao hơn.") if a!=b else None
@reg(3,"Thống kê và xác suất")
def _(r):
    xs=[r.randint(5,30) for _ in range(5)]
    return FL(TK,"Số liệu lớn nhất – nhỏ nhất",f"Chiều cao các cây (cm): {', '.join(map(str,xs))}. Cây cao nhất hơn cây thấp nhất bao nhiêu xăng-ti-mét?",max(xs)-min(xs),"Tìm số lớn nhất và nhỏ nhất.",f"{max(xs)} − {min(xs)} = {max(xs)-min(xs)}.","So sánh để tìm số liệu lớn nhất, nhỏ nhất.")

# ======================= LỚP 4 =======================
@reg(4,"Số có nhiều chữ số")
def _(r):
    n=r.randint(1_000_000,999_999_999)
    return FL(SH,"Hàng triệu",f"Chữ số hàng triệu của số {n:,} là chữ số nào?".replace(",","."),(n//1_000_000)%10,"Lớp triệu gồm hàng triệu, chục triệu, trăm triệu.",f"Hàng triệu: {(n//1_000_000)%10}.","Mỗi lớp có 3 hàng.")
@reg(4,"Số có nhiều chữ số")
def _(r):
    n=r.randint(100_000,9_999_999);k=r.choice([1000,10000,100000]);rd=int(round(n/k))*k
    nm={1000:"nghìn",10000:"chục nghìn",100000:"trăm nghìn"}[k]
    return MC(r,SH,"Làm tròn",f"Làm tròn số {n:,} đến hàng {nm} được:".replace(",","."),f"{rd:,}".replace(",","."),[f"{x:,}".replace(",",".") for x in (rd+k,rd-k,(n//k)*k if (n//k)*k!=rd else rd+2*k)],"Xét chữ số ngay sau hàng làm tròn.",f"≈ {rd:,}".replace(",","."),"≥ 5 làm tròn lên, < 5 làm tròn xuống.")
@reg(4,"Số có nhiều chữ số")
def _(r):
    a,b=r.sample(range(1,10),2);c=r.randint(0,9)
    n=a*10**6+b*10**4+c
    return FL(SH,"Viết số",f"Viết số gồm {a} triệu, {b} chục nghìn và {c} đơn vị.",n,"Hàng nào không có thì viết chữ số 0.",f"{n:,}".replace(",","."),"Viết theo từng lớp.")
@reg(4,"Bốn phép tính với số tự nhiên")
def _(r):
    a=r.randint(12,99);b=r.randint(12,99)
    return FL(SH,"Nhân với số có hai chữ số",f"Tính: {a} × {b}",a*b,"Nhân với từng chữ số rồi cộng.",f"{a} × {b} = {a*b}.","Tích riêng thứ hai lùi sang trái một hàng.")
@reg(4,"Bốn phép tính với số tự nhiên")
def _(r):
    b=r.randint(12,60);q=r.randint(12,99)
    return MC(r,SH,"Chia cho số có hai chữ số",f"{b*q} : {b} = ?",q,near(r,q,low=1),"Ước lượng thương.",f"{b} × {q} = {b*q}.","Thử lại bằng phép nhân.")
@reg(4,"Bốn phép tính với số tự nhiên")
def _(r):
    a=r.randint(10000,90000);b=r.randint(1000,9000);c=r.randint(1000,9000)
    return FL(SH,"Bài toán ba bước",f"Kho có {a} kg gạo, ngày đầu xuất {b} kg, ngày sau xuất {c} kg. Kho còn bao nhiêu ki-lô-gam gạo?",a-b-c,"Trừ lần lượt hoặc trừ tổng.",f"{a} − ({b} + {c}) = {a-b-c}.","a − b − c = a − (b + c).")
@reg(4,"Tính chất các phép tính")
def _(r):
    a=r.choice([25,4*r.randint(3,9),50,125]);b={25:4,50:2,125:8}.get(a,25);c=r.randint(11,99)
    return FL(SH,"Tính thuận tiện",f"Tính nhanh: {a} × {c} × {b}",a*b*c,"Nhóm hai thừa số có tích tròn chục, tròn trăm.",f"({a} × {b}) × {c} = {a*b} × {c} = {a*b*c}.","Giao hoán, kết hợp để tính nhanh.")
@reg(4,"Tính chất các phép tính")
def _(r):
    a=r.randint(12,99);b,c=r.randint(10,90),0;c=100-b
    return MC(r,SH,"Nhân một số với một tổng",f"{a} × {b} + {a} × {c} = ?",a*100,[a*b+c,a*(b+c+1),a*10],"Đặt thừa số chung.",f"{a} × ({b} + {c}) = {a} × 100 = {a*100}.","a × b + a × c = a × (b + c).")
@reg(4,"Tính chất các phép tính")
def _(r):
    xs=[r.randint(100,900) for _ in range(2)];y=[1000-xs[0],1000-xs[1]]
    return FL(SH,"Cộng thuận tiện",f"Tính nhanh: {xs[0]} + {xs[1]} + {y[0]} + {y[1]}",2000,"Ghép các cặp có tổng tròn nghìn.",f"({xs[0]} + {y[0]}) + ({xs[1]} + {y[1]}) = 1000 + 1000 = 2000.","Ghép cặp tròn trăm, tròn nghìn.")
@reg(4,"Trung bình cộng")
def _(r):
    k=r.randint(3,5);avg=r.randint(20,80);xs=[avg+r.randint(-15,15) for _ in range(k-1)];xs.append(avg*k-sum(xs))
    return FL(SH,"Tìm trung bình cộng",f"Tìm trung bình cộng của các số: {', '.join(map(str,xs))}.",avg,"Tổng chia số các số hạng.",f"{sum(xs)} : {k} = {avg}.","TBC = tổng : số lượng.")
@reg(4,"Trung bình cộng")
def _(r):
    k=r.randint(3,5);avg=r.randint(30,60)
    return MC(r,SH,"Tìm tổng từ trung bình",f"Trung bình cộng của {k} số là {avg}. Tổng của {k} số đó là:",avg*k,[avg+k,avg*k+k,avg*(k-1)],"Tổng = trung bình × số lượng.",f"{avg} × {k} = {avg*k}.","Đảo ngược công thức trung bình.")
@reg(4,"Trung bình cộng")
def _(r):
    a,b=r.randint(30,50),r.randint(30,50);avg=(a+b+r.randint(30,50))
    c=r.randint(30,50);avg=(a+b+c)
    if avg%3: c+=3-avg%3
    return FL(SH,"Bài toán trung bình",f"Ba lớp quyên góp được lần lượt {a}, {b} và {c} quyển sách. Trung bình mỗi lớp quyên góp được bao nhiêu quyển?",(a+b+c)//3,"Cộng rồi chia 3.",f"({a} + {b} + {c}) : 3 = {(a+b+c)//3}.","TBC của 3 số.")
@reg(4,"Tìm hai số khi biết tổng và hiệu")
def _(r):
    big=r.randint(30,200);sm=r.randint(10,big-5)
    return FL(SH,"Số lớn",f"Tổng hai số là {big+sm}, hiệu là {big-sm}. Tìm số lớn.",big,"(Tổng + hiệu) : 2.",f"({big+sm} + {big-sm}) : 2 = {big}.","Số lớn = (T + H) : 2.")
@reg(4,"Tìm hai số khi biết tổng và hiệu")
def _(r):
    big=r.randint(30,200);sm=r.randint(10,big-5)
    return MC(r,SH,"Số bé",f"Tổng hai số là {big+sm}, hiệu là {big-sm}. Số bé là:",sm,[big,sm+1,(big+sm)//2],"(Tổng − hiệu) : 2.",f"({big+sm} − {big-sm}) : 2 = {sm}.","Số bé = (T − H) : 2.")
@reg(4,"Tìm hai số khi biết tổng và hiệu")
def _(r):
    d=r.randint(2,10);c=r.randint(8,30)
    return FL(SH,"Tuổi",f"Tổng số tuổi của hai anh em là {2*c+d}, anh hơn em {d} tuổi. Em bao nhiêu tuổi?",c,"(Tổng − hiệu) : 2.",f"({2*c+d} − {d}) : 2 = {c}.","Tuổi em = (tổng − hiệu) : 2.")
@reg(4,"Tổng – tỉ, hiệu – tỉ")
def _(r):
    k=r.randint(2,5);s=r.randint(6,40)
    return FL(SH,"Tổng – tỉ",f"Tổng hai số là {s*(k+1)}, số lớn gấp {k} lần số bé. Tìm số bé.",s,f"Số bé 1 phần, số lớn {k} phần.",f"{s*(k+1)} : {k+1} = {s}.","Tổng số phần = k + 1.")
@reg(4,"Tổng – tỉ, hiệu – tỉ")
def _(r):
    k=r.randint(2,5);s=r.randint(6,40)
    return MC(r,SH,"Hiệu – tỉ",f"Hiệu hai số là {s*(k-1)}, số lớn gấp {k} lần số bé. Số lớn là:",s*k,[s,s*(k-1),s*k+s],f"Hiệu ứng với {k-1} phần.",f"1 phần = {s*(k-1)} : {k-1} = {s}; số lớn {s*k}.","Hiệu số phần = k − 1.")
@reg(4,"Tổng – tỉ, hiệu – tỉ")
def _(r):
    a,b=r.choice([(2,3),(3,4),(3,5),(2,5),(4,5)]);u=r.randint(3,15)
    return FL(SH,"Tỉ số",f"Lớp có {(a+b)*u} học sinh, tỉ số giữa số nam và số nữ là {a}/{b}. Lớp có bao nhiêu học sinh nam?",a*u,"Tổng số phần là "+str(a+b)+".",f"{(a+b)*u} : {a+b} × {a} = {a*u}.","Chia tổng theo tỉ số.")
@reg(4,"Phân số")
def _(r):
    a,b=r.randint(1,9),r.randint(2,9);k=r.randint(2,6)
    return MC(r,SH,"Phân số bằng nhau",f"Phân số nào bằng phân số {a}/{b}?",f"{a*k}/{b*k}",[f"{a+k}/{b+k}",f"{a*k}/{b}",f"{a}/{b*k}"],"Nhân cả tử và mẫu với cùng một số.",f"{a}/{b} = {a*k}/{b*k}.","Tính chất cơ bản của phân số.")
@reg(4,"Phân số")
def _(r):
    g=r.randint(2,9);a,b=r.choice([(1,2),(2,3),(3,4),(2,5),(3,7),(4,9),(5,6)])
    return FL(SH,"Rút gọn phân số",f"Rút gọn phân số {a*g}/{b*g} về phân số tối giản (ghi dạng a/b).",f"{a}/{b}","Chia cả tử và mẫu cho ƯCLN.",f"{a*g}/{b*g} = {a}/{b}.","Tối giản: tử và mẫu không còn ước chung > 1.")
@reg(4,"Phân số")
def _(r):
    b=r.randint(3,12);a,c=r.sample(range(1,b),2)
    return MC(r,SH,"So sánh phân số cùng mẫu",f"So sánh {a}/{b} và {c}/{b}:",f"{a}/{b} {'<' if a<c else '>'} {c}/{b}",[f"{a}/{b} {'>' if a<c else '<'} {c}/{b}",f"{a}/{b} = {c}/{b}","Không so sánh được"],"Cùng mẫu: so sánh tử.",f"{a} {'<' if a<c else '>'} {c}.","Cùng mẫu, tử lớn hơn thì lớn hơn.")
@reg(4,"Các phép tính với phân số")
def _(r):
    b,d=r.sample([2,3,4,5,6,8,10],2);a,c=r.randint(1,b-1),r.randint(1,d-1);v=Fr(a,b)+Fr(c,d)
    return FL(SH,"Cộng phân số",f"Tính {a}/{b} + {c}/{d} (ghi kết quả tối giản dạng a/b).",v,"Quy đồng mẫu số.",f"= {v}.","Khác mẫu: quy đồng rồi cộng tử.")
@reg(4,"Các phép tính với phân số")
def _(r):
    a,b,c,d=r.randint(1,7),r.randint(2,9),r.randint(1,7),r.randint(2,9);v=Fr(a,b)*Fr(c,d)
    return MC(r,SH,"Nhân phân số",f"{a}/{b} × {c}/{d} = ?",vn(v),[vn(Fr(a+c,b+d)),vn(Fr(a*d,b*c)),vn(v+Fr(1,v.denominator))],"Tử nhân tử, mẫu nhân mẫu.",f"{a*c}/{b*d} = {vn(v)}.","Nhân rồi rút gọn.")
@reg(4,"Các phép tính với phân số")
def _(r):
    b=r.choice([4,5,6,8]);a=r.randint(1,b-1);n=b*r.randint(3,12)
    return FL(SH,"Phân số của một số",f"Một mảnh vườn có {n} cây, trong đó {a}/{b} số cây là cam. Có bao nhiêu cây cam?",n*a//b,"Lấy số đó nhân với phân số.",f"{n} × {a}/{b} = {n*a//b}.","Tìm a/b của n: n : b × a.")
@reg(4,"Góc, đường thẳng vuông góc, song song")
def _(r):
    x=r.choice([(r.randint(10,80),"góc nhọn"),(90,"góc vuông"),(r.randint(100,170),"góc tù"),(180,"góc bẹt")])
    return MC(r,HH,"Phân loại góc",f"Góc có số đo {x[0]}° là:",x[1],[y for y in ["góc nhọn","góc vuông","góc tù","góc bẹt"] if y!=x[1]],"Nhọn < 90° < tù < 180°.",f"{x[0]}° là {x[1]}.","Vuông 90°, bẹt 180°.")
@reg(4,"Góc, đường thẳng vuông góc, song song")
def _(r):
    a=r.randint(20,160)
    return FL(HH,"Góc kề bù",f"Hai góc kề nhau tạo thành một góc bẹt. Một góc bằng {a}°. Góc còn lại bằng bao nhiêu độ?",180-a,"Góc bẹt bằng 180°.",f"180° − {a}° = {180-a}°.","Hai góc tạo thành góc bẹt có tổng 180°.")
@reg(4,"Góc, đường thẳng vuông góc, song song")
def _(r):
    return MC(r,HH,"Cạnh song song","Hình chữ nhật ABCD có bao nhiêu cặp cạnh song song với nhau?",2,[1,4,0],"AB ∥ CD, AD ∥ BC.","Có 2 cặp: AB ∥ CD và AD ∥ BC.","Cạnh đối của hình chữ nhật song song.")
@reg(4,"Hình bình hành, hình thoi")
def _(r):
    a,b=r.randint(5,20),r.randint(3,15)
    return FL(HH,"Chu vi hình bình hành",f"Hình bình hành có hai cạnh kề dài {a} cm và {b} cm. Tính chu vi (cm).",2*(a+b),"(a + b) × 2.",f"({a} + {b}) × 2 = {2*(a+b)}.","Hai cạnh đối bằng nhau.")
@reg(4,"Hình bình hành, hình thoi")
def _(r):
    s=r.randint(3,25)
    return MC(r,HH,"Chu vi hình thoi",f"Hình thoi có cạnh {s} cm. Chu vi hình thoi là:",f"{4*s} cm",[f"{2*s} cm",f"{s*s} cm",f"{4*s} cm²"],"Hình thoi có 4 cạnh bằng nhau.",f"{s} × 4 = {4*s} (cm).","Chu vi hình thoi = cạnh × 4.")
@reg(4,"Hình bình hành, hình thoi")
def _(r):
    return MC(r,HH,"Đặc điểm hình thoi","Hình nào có bốn cạnh bằng nhau và hai cặp cạnh đối song song?","Hình thoi",["Hình bình hành có hai cạnh kề khác nhau","Hình thang","Hình chữ nhật có hai cạnh kề khác nhau"],"Nhớ đặc điểm từng hình.","Hình thoi có 4 cạnh bằng nhau, các cặp cạnh đối song song.","Hình vuông cũng là một hình thoi đặc biệt.")
@reg(4,"Đo lường: yến, tạ, tấn; giây, thế kỉ; dm², m²")
def _(r):
    t=r.randint(1,9);q=r.randint(1,9)
    return FL(HH,"Đổi tấn, tạ",f"{t} tấn {q} tạ = … kg",1000*t+100*q,"1 tấn = 1000 kg, 1 tạ = 100 kg.",f"{1000*t} + {100*q} = {1000*t+100*q}.","Tấn – tạ – yến – kg: hơn kém 10 lần.")
@reg(4,"Đo lường: yến, tạ, tấn; giây, thế kỉ; dm², m²")
def _(r):
    y=r.randint(1001,2099);c=(y-1)//100+1
    return MC(r,HH,"Thế kỉ",f"Năm {y} thuộc thế kỉ thứ mấy?",c,[c-1,c+1,y//100],"Thế kỉ I: năm 1 đến 100.",f"Năm {y} thuộc thế kỉ {c}.","Thế kỉ = (năm − 1) : 100 + 1 (bỏ phần dư).")
@reg(4,"Đo lường: yến, tạ, tấn; giây, thế kỉ; dm², m²")
def _(r):
    m=r.randint(1,9);d=r.randint(1,99)
    return FL(HH,"Đổi m², dm²",f"{m} m² {d} dm² = … dm²",100*m+d,"1 m² = 100 dm².",f"{100*m} + {d} = {100*m+d}.","Diện tích: hai đơn vị liền nhau hơn kém 100 lần.")
@reg(4,"Thống kê và xác suất")
def _(r):
    xs=[r.randint(10,60) for _ in range(4)]
    return FL(TK,"Biểu đồ cột",f"Biểu đồ cột số cây trồng của 4 tổ: {', '.join(f'tổ {i+1}: {xs[i]}' for i in range(4))}. Trung bình mỗi tổ trồng bao nhiêu cây? (ghi số thập phân nếu cần)",sum(xs)/4,"Cộng rồi chia 4.",f"{sum(xs)} : 4 = {vn(sum(xs)/4)}.","Đọc biểu đồ cột rồi tính.")
@reg(4,"Thống kê và xác suất")
def _(r):
    n=r.randint(20,50);h=r.randint(5,n-5)
    return MC(r,XS,"Kiểm đếm số lần",f"Tung đồng xu {n} lần, có {h} lần mặt ngửa. Số lần mặt sấp là:",n-h,[h,n-h+1,n],"Tổng số lần = ngửa + sấp.",f"{n} − {h} = {n-h}.","Kiểm đếm số lần xuất hiện.")
@reg(4,"Thống kê và xác suất")
def _(r):
    xs=sorted(r.sample(range(110,160),5))
    return FL(TK,"Dãy số liệu",f"Chiều cao (cm) của 5 bạn: {', '.join(map(str,r.sample(xs,5)))}. Bạn cao nhất cao bao nhiêu xăng-ti-mét?",xs[-1],"Sắp xếp dãy số liệu.",f"Cao nhất: {xs[-1]} cm.","Xếp dãy số liệu từ bé đến lớn.")

# ======================= LỚP 5 =======================
@reg(5,"Ôn tập phân số, hỗn số")
def _(r):
    w=r.randint(1,9);b=r.randint(2,9);a=r.randint(1,b-1)
    return FL(SH,"Hỗn số",f"Chuyển hỗn số {w} {a}/{b} thành phân số (ghi dạng a/b).",f"{w*b+a}/{b}","Nhân phần nguyên với mẫu rồi cộng tử.",f"({w} × {b} + {a})/{b} = {w*b+a}/{b}.","Hỗn số → phân số.")
@reg(5,"Ôn tập phân số, hỗn số")
def _(r):
    a,b=r.choice([(3,4),(2,5),(7,10),(1,4),(3,5),(9,20),(1,8)])
    v=a/b
    return MC(r,SH,"Phân số thập phân",f"Phân số {a}/{b} viết thành số thập phân là:",vn(v),[vn(v*10),vn(a/(b*10)),vn(round(v+0.1,3))],"Đưa về mẫu 10, 100, 1000.",f"{a}/{b} = {vn(v)}.","Mẫu 10 → 1 chữ số sau dấu phẩy.")
@reg(5,"Ôn tập phân số, hỗn số")
def _(r):
    b,d=r.sample([3,4,5,6,8,9,12],2);a,c=r.randint(1,b-1),r.randint(1,d-1)
    if Fr(a,b)==Fr(c,d): return None
    v=Fr(a,b)-Fr(c,d) if Fr(a,b)>Fr(c,d) else Fr(c,d)-Fr(a,b);x,y=(a,b,c,d) if Fr(a,b)>Fr(c,d) else (c,d,a,b),None
    return FL(SH,"Trừ phân số",f"Tính {x[0]}/{x[1]} − {x[2]}/{x[3]} (ghi tối giản dạng a/b).",v,"Quy đồng rồi trừ.",f"= {v}.","Quy đồng mẫu số.")
@reg(5,"Số thập phân")
def _(r):
    n=r.randint(1000,99999)/1000
    return FL(SH,"Hàng phần trăm",f"Chữ số hàng phần trăm của số {vn(n)} là chữ số nào?",int(round(n*1000))//10%10,"Sau dấu phẩy: phần mười, phần trăm, phần nghìn.",f"{vn(n)}: phần trăm là {int(round(n*1000))//10%10}.","Đếm từ dấu phẩy sang phải.")
@reg(5,"Số thập phân")
def _(r):
    xs=[round(r.uniform(1,9),2) for _ in range(4)]
    if len(set(xs))<4: return None
    return MC(r,SH,"So sánh số thập phân",f"Số lớn nhất trong các số {', '.join(vn(x) for x in xs)} là:",vn(max(xs)),[vn(x) for x in xs if x!=max(xs)],"So sánh phần nguyên rồi đến phần thập phân.",f"Lớn nhất: {vn(max(xs))}.","So sánh từng hàng từ trái sang phải.")
@reg(5,"Số thập phân")
def _(r):
    n=round(r.uniform(1,99),3);rd=round(n,1)
    return MC(r,SH,"Làm tròn số thập phân",f"Làm tròn số {vn(n)} đến hàng phần mười được:",vn(rd),[vn(round(rd+0.1,1)),vn(round(rd-0.1,1)),vn(round(n,2))],"Xét chữ số hàng phần trăm.",f"{vn(n)} ≈ {vn(rd)}.","≥ 5 thì làm tròn lên.") if abs(n*100-int(n*100)-0.5)>0.01 else None
@reg(5,"Các phép tính với số thập phân")
def _(r):
    a=round(r.uniform(1,50),2);b=round(r.uniform(1,30),2)
    return FL(SH,"Cộng số thập phân",f"Tính: {vn(a)} + {vn(b)} (ghi số thập phân)",round(a+b,2),"Đặt dấu phẩy thẳng cột.",f"= {vn(round(a+b,2))}.","Dấu phẩy thẳng hàng.")
@reg(5,"Các phép tính với số thập phân")
def _(r):
    a=round(r.uniform(1,20),1);k=r.randint(2,9)
    return MC(r,SH,"Nhân số thập phân",f"{vn(a)} × {k} = ?",vn(round(a*k,1)),[vn(round(a*k*10,1)),vn(round(a*k/10,2)),vn(round(a*k+k,1))],"Nhân như số tự nhiên rồi đặt dấu phẩy.",f"= {vn(round(a*k,1))}.","Tích có bao nhiêu chữ số thập phân như thừa số.")
@reg(5,"Các phép tính với số thập phân")
def _(r):
    n=r.randint(3,8);h=round(r.uniform(2.5,3.9),1)
    return FL(SH,"Bài toán thực tế",f"Một tòa nhà có {n} tầng, mỗi tầng cao {vn(h)} m. Tòa nhà cao bao nhiêu mét? (ghi số thập phân)",round(n*h,1),"Nhân chiều cao mỗi tầng với số tầng.",f"{vn(h)} × {n} = {vn(round(n*h,1))} (m).","Nhân số thập phân với số tự nhiên.")
@reg(5,"Tỉ số phần trăm")
def _(r):
    p=r.choice([5,10,15,20,25,30,40,60,75]);n=r.choice([20,40,60,80,120,200,240,400])
    return FL(SH,"Tìm phần trăm của một số",f"Tìm {p}% của {n}.",n*p/100,"Nhân với số phần trăm rồi chia 100.",f"{n} × {p} : 100 = {vn(n*p/100)}.","a% của b = b × a : 100.")
@reg(5,"Tỉ số phần trăm")
def _(r):
    b=r.choice([20,25,40,50,80]);a=r.randint(1,b-1)
    return MC(r,SH,"Tỉ số phần trăm của hai số",f"Tỉ số phần trăm của {a} và {b} là:",vn(a*100/b)+"%",[vn(b*100/a)+"%" if a else "0%",vn(a/b)+"%",vn(a*100/b+5)+"%"],"Chia rồi nhân 100.",f"{a} : {b} × 100 = {vn(a*100/b)}%.","Tỉ số % = a : b × 100%.")
@reg(5,"Tỉ số phần trăm")
def _(r):
    w=r.choice([60,64,72,80]);p=r.choice([2,3,4,5])
    return FL(SH,"Bài toán thực tế",f"Một vận động viên nặng {w} kg, sau cuộc chạy bị giảm {p}% cân nặng. Vận động viên còn nặng bao nhiêu ki-lô-gam? (ghi số thập phân)",round(w*(100-p)/100,2),"Tính số kg bị giảm trước.",f"Giảm {vn(w*p/100)} kg; còn {vn(round(w*(100-p)/100,2))} kg.","Đề minh họa CT 2018 lớp 5.")
@reg(5,"Tỉ lệ bản đồ")
def _(r):
    k=r.choice([1000,2000,5000,10000]);c=r.randint(2,15)
    return FL(HH,"Độ dài thật",f"Trên bản đồ tỉ lệ 1 : {k}, một đoạn đường dài {c} cm. Độ dài thật của đoạn đường là bao nhiêu mét?",c*k/100,"Nhân với "+str(k)+" rồi đổi ra mét.",f"{c} × {k} = {c*k} cm = {vn(c*k/100)} m.","Độ dài thật = độ dài bản đồ × mẫu số tỉ lệ.")
@reg(5,"Tỉ lệ bản đồ")
def _(r):
    k=r.choice([1000,10000,100000]);m=r.randint(2,9)*k//100
    return MC(r,HH,"Độ dài trên bản đồ",f"Quãng đường thật dài {m} m. Trên bản đồ tỉ lệ 1 : {k}, quãng đường đó dài:",f"{vn(m*100/k)} cm",[f"{vn(m*100/k*10)} cm",f"{vn(m/k)} cm",f"{m} cm"],"Đổi ra cm rồi chia cho "+str(k)+".",f"{m*100} : {k} = {vn(m*100/k)} cm.","Bản đồ = thật : mẫu số tỉ lệ.")
@reg(5,"Tỉ lệ bản đồ")
def _(r):
    a,b=r.randint(2,8),r.randint(2,8);k=1000
    return FL(HH,"Diện tích thật",f"Một mảnh đất hình chữ nhật trên bản đồ tỉ lệ 1 : 1000 có kích thước {a} cm × {b} cm. Diện tích thật là bao nhiêu mét vuông?",a*10*b*10,"Đổi mỗi cạnh ra mét trước.",f"{a} cm → {a*10} m; {b} cm → {b*10} m; {a*10} × {b*10} = {a*b*100} m².","Tính độ dài thật từng cạnh rồi nhân.")
@reg(5,"Hình tam giác, hình thang")
def _(r):
    a,h=r.randint(4,30),r.randint(3,20)
    return FL(HH,"Diện tích tam giác",f"Tam giác có đáy {a} cm, chiều cao {h} cm. Tính diện tích (cm²).",a*h/2,"Đáy × cao : 2.",f"{a} × {h} : 2 = {vn(a*h/2)}.","S = a × h : 2.")
@reg(5,"Hình tam giác, hình thang")
def _(r):
    a,b,h=r.randint(5,20),r.randint(3,15),r.randint(2,12)
    return MC(r,HH,"Diện tích hình thang",f"Hình thang có hai đáy {a} cm và {b} cm, chiều cao {h} cm. Diện tích là:",f"{vn((a+b)*h/2)} cm²",[f"{(a+b)*h} cm²",f"{vn(a*b*h/2)} cm²",f"{vn((a+b)*h/2+h)} cm²"],"(Đáy lớn + đáy bé) × cao : 2.",f"({a} + {b}) × {h} : 2 = {vn((a+b)*h/2)}.","S hình thang = (a + b) × h : 2.")
@reg(5,"Hình tam giác, hình thang")
def _(r):
    S=r.randint(20,120)*2;a=r.choice([x for x in range(4,40) if S*2%x==0] or [S])
    return FL(HH,"Tìm chiều cao",f"Tam giác có diện tích {S} cm² và đáy {a} cm. Chiều cao tam giác là bao nhiêu xăng-ti-mét?",S*2/a,"h = S × 2 : a.",f"{S} × 2 : {a} = {vn(S*2/a)}.","Đảo công thức diện tích.")
@reg(5,"Hình tròn")
def _(r):
    rr=r.randint(2,20)
    return FL(HH,"Chu vi hình tròn",f"Tính chu vi hình tròn bán kính {rr} cm (lấy π = 3,14; ghi số thập phân).",round(2*rr*3.14,2),"C = r × 2 × 3,14.",f"{rr} × 2 × 3,14 = {vn(round(2*rr*3.14,2))}.","C = d × 3,14.")
@reg(5,"Hình tròn")
def _(r):
    rr=r.randint(2,15)
    return MC(r,HH,"Diện tích hình tròn",f"Diện tích hình tròn bán kính {rr} cm (π = 3,14) là:",f"{vn(round(rr*rr*3.14,2))} cm²",[f"{vn(round(2*rr*3.14,2))} cm²",f"{vn(round(rr*3.14,2))} cm²",f"{vn(round(4*rr*rr*3.14,2))} cm²"],"S = r × r × 3,14.",f"{rr} × {rr} × 3,14 = {vn(round(rr*rr*3.14,2))}.","Diện tích hình tròn.")
@reg(5,"Hình tròn")
def _(r):
    d=round(r.choice([0.5,0.6,0.7,0.8,1.2]),1);n=r.choice([10,50,100,200])
    return FL(HH,"Bánh xe lăn",f"Bánh xe có đường kính {vn(d)} m lăn {n} vòng. Xe đi được bao nhiêu mét? (π = 3,14)",round(d*3.14*n,2),"Mỗi vòng đi được một chu vi.",f"{vn(d)} × 3,14 × {n} = {vn(round(d*3.14*n,2))} m.","Quãng đường = chu vi × số vòng.")
@reg(5,"Hình hộp chữ nhật, hình lập phương")
def _(r):
    a,b,c=r.randint(2,12),r.randint(2,10),r.randint(2,9)
    return FL(HH,"Thể tích hình hộp",f"Hình hộp chữ nhật dài {a} dm, rộng {b} dm, cao {c} dm. Thể tích là bao nhiêu đề-xi-mét khối?",a*b*c,"V = a × b × c.",f"{a} × {b} × {c} = {a*b*c}.","Đơn vị thể tích: dm³.")
@reg(5,"Hình hộp chữ nhật, hình lập phương")
def _(r):
    a,b,c=r.randint(3,12),r.randint(2,10),r.randint(2,9)
    return MC(r,HH,"Diện tích xung quanh",f"Hình hộp chữ nhật dài {a} cm, rộng {b} cm, cao {c} cm. Diện tích xung quanh là:",f"{2*(a+b)*c} cm²",[f"{(a+b)*c} cm²",f"{2*(a*b+b*c+a*c)} cm²",f"{a*b*c} cm²"],"Chu vi đáy × chiều cao.",f"({a} + {b}) × 2 × {c} = {2*(a+b)*c}.","Sxq = chu vi đáy × cao.")
@reg(5,"Hình hộp chữ nhật, hình lập phương")
def _(r):
    s=r.randint(2,12)
    return FL(HH,"Diện tích toàn phần lập phương",f"Hình lập phương cạnh {s} cm có diện tích toàn phần là bao nhiêu xăng-ti-mét vuông?",6*s*s,"6 mặt bằng nhau.",f"{s} × {s} × 6 = {6*s*s}.","Stp = cạnh × cạnh × 6.")
@reg(5,"Số đo thời gian")
def _(r):
    h=r.randint(1,4);m=r.choice([15,30,45,12,24,36])
    return FL(HH,"Đổi giờ ra phút",f"{h} giờ {m} phút = … phút",60*h+m,"1 giờ = 60 phút.",f"{h} × 60 + {m} = {60*h+m}.","Giờ → phút: nhân 60.")
@reg(5,"Số đo thời gian")
def _(r):
    h=r.choice([1.5,2.25,0.75,1.2,2.5,3.25])
    return MC(r,HH,"Giờ thập phân",f"{vn(h)} giờ = … phút",int(h*60),[int(h*100),int(h*60)+10,int(h)*60],"Nhân với 60.",f"{vn(h)} × 60 = {int(h*60)} phút.","0,5 giờ = 30 phút.")
@reg(5,"Số đo thời gian")
def _(r):
    a1,b1=r.randint(1,5),r.randint(10,50);a2,b2=r.randint(1,5),r.randint(10,50);t=(a1+a2)*60+b1+b2
    return FL(HH,"Cộng số đo thời gian",f"Tính: {a1} giờ {b1} phút + {a2} giờ {b2} phút = ? (ghi tổng số phút)",t,"Cộng giờ với giờ, phút với phút.",f"= {t//60} giờ {t%60} phút = {t} phút.","Phút ≥ 60 thì đổi sang giờ.")
@reg(5,"Chuyển động đều")
def _(r):
    v=r.randint(30,60);t=r.choice([1.5,2,2.5,3])
    return FL(HH,"Quãng đường",f"Một ô tô đi với vận tốc {v} km/giờ trong {vn(t)} giờ. Quãng đường ô tô đi được là bao nhiêu ki-lô-mét?",v*t,"s = v × t.",f"{v} × {vn(t)} = {vn(v*t)} km.","Quãng đường = vận tốc × thời gian.")
@reg(5,"Chuyển động đều")
def _(r):
    t=r.randint(2,5);v=r.randint(10,50)
    return MC(r,HH,"Vận tốc",f"Một người đi xe đạp được {v*t} km trong {t} giờ. Vận tốc của người đó là:",f"{v} km/giờ",[f"{v*t*t} km/giờ",f"{v+t} km/giờ",f"{v-2} km/giờ"],"v = s : t.",f"{v*t} : {t} = {v} km/giờ.","Vận tốc = quãng đường : thời gian.")
@reg(5,"Chuyển động đều")
def _(r):
    v1,v2=r.randint(30,50),r.randint(30,50);t=r.randint(2,4)
    return FL(HH,"Chuyển động ngược chiều",f"Hai xe khởi hành cùng lúc từ hai thành phố cách nhau {(v1+v2)*t} km, đi ngược chiều với vận tốc {v1} km/giờ và {v2} km/giờ. Sau mấy giờ hai xe gặp nhau?",t,"Thời gian gặp = quãng đường : tổng vận tốc.",f"{(v1+v2)*t} : ({v1} + {v2}) = {t} giờ.","Ngược chiều: cộng vận tốc.")
@reg(5,"Thống kê và xác suất")
def _(r):
    p=r.choice([(40,25,20,15),(50,20,20,10),(35,30,25,10)]);n=r.choice([40,60,80,200])
    return FL(TK,"Biểu đồ hình quạt",f"Biểu đồ hình quạt: trong {n} học sinh, {p[0]}% thích bóng đá, {p[1]}% thích cầu lông, {p[2]}% thích bơi, còn lại thích cờ vua. Có bao nhiêu học sinh thích cờ vua?",n*p[3]//100,"Tìm phần trăm còn lại.",f"{p[3]}% × {n} = {n*p[3]//100}.","Các phần của biểu đồ hình quạt cộng lại 100%.")
@reg(5,"Thống kê và xác suất")
def _(r):
    n=r.randint(20,50);k=r.randint(5,n-5)
    return MC(r,XS,"Tỉ số mô tả khả năng",f"Gieo một con xúc xắc {n} lần thì có {k} lần xuất hiện mặt 6 chấm. Tỉ số của số lần xuất hiện mặt 6 chấm và tổng số lần gieo là:",f"{k}/{n}",[f"{n}/{k}",f"{n-k}/{n}",f"{k}/{n-k}"],"Số lần xuất hiện : tổng số lần.",f"{k}/{n}.","Dùng phân số để mô tả khả năng xảy ra.")
@reg(5,"Thống kê và xác suất")
def _(r):
    xs=[r.randint(5,10) for _ in range(5)]
    return FL(TK,"Đọc bảng số liệu",f"Điểm kiểm tra của 5 bạn: {', '.join(map(str,xs))}. Điểm trung bình của 5 bạn là bao nhiêu? (ghi số thập phân nếu cần)",sum(xs)/5,"Cộng rồi chia 5.",f"{sum(xs)} : 5 = {vn(sum(xs)/5)}.","Trung bình cộng dãy số liệu.")

# ======================= LỚP 6 =======================
@reg(6,"Tập hợp các số tự nhiên")
def _(r):
    a=r.randint(5,30);b=a+r.randint(5,30)
    return FL(SH,"Số phần tử của tập hợp",f"Tập hợp A = {{x ∈ ℕ | {a} ≤ x ≤ {b}}} có bao nhiêu phần tử?",b-a+1,"Đếm số tự nhiên từ "+str(a)+" đến "+str(b)+".",f"{b} − {a} + 1 = {b-a+1}.","Số phần tử = cuối − đầu + 1.")
@reg(6,"Tập hợp các số tự nhiên")
def _(r):
    a,n=r.randint(2,5),r.randint(2,5)
    return MC(r,SH,"Lũy thừa",f"Giá trị của {a}^{n} là:",a**n,[a*n,a**(n-1),a**n+a],"Nhân "+str(n)+" thừa số "+str(a)+".",f"{a}^{n} = {a**n}.","aⁿ = a · a · … · a (n thừa số).")
@reg(6,"Tập hợp các số tự nhiên")
def _(r):
    a,m,n=r.randint(2,7),r.randint(2,6),r.randint(2,6)
    return FL(SH,"Nhân hai lũy thừa cùng cơ số",f"Viết {a}^{m} · {a}^{n} dưới dạng một lũy thừa {a}^k. Tìm k.",m+n,"Giữ cơ số, cộng số mũ.",f"k = {m} + {n} = {m+n}.","aᵐ · aⁿ = aᵐ⁺ⁿ.")
@reg(6,"Tính chia hết")
def _(r):
    g=r.randint(2,12);x,y=r.choice([(2,3),(3,4),(3,5),(4,5),(5,6),(2,7),(5,7)])
    return FL(SH,"ƯCLN",f"Tìm ƯCLN({g*x}, {g*y}).",g,"Phân tích ra thừa số nguyên tố.",f"ƯCLN = {g}.","Lấy thừa số chung với số mũ nhỏ nhất.")
@reg(6,"Tính chia hết")
def _(r):
    a,b=r.choice([(4,6),(6,8),(6,9),(8,12),(10,15),(12,18),(9,15)])
    l=a*b//math.gcd(a,b)
    return MC(r,SH,"BCNN",f"BCNN({a}, {b}) bằng:",l,[a*b,math.gcd(a,b),l*2],"Lấy thừa số chung và riêng với số mũ lớn nhất.",f"BCNN({a}, {b}) = {l}.","BCNN × ƯCLN = a × b.")
@reg(6,"Tính chia hết")
def _(r):
    d=r.choice([2,3,5,9]);xs=r.sample(range(100,999),4);good=[x for x in xs if x%d==0]
    if len(good)!=1: return None
    return MC(r,SH,"Dấu hiệu chia hết",f"Trong các số {', '.join(map(str,xs))}, số nào chia hết cho {d}?",good[0],[x for x in xs if x%d],{2:"Chữ số tận cùng chẵn.",5:"Tận cùng 0 hoặc 5.",3:"Tổng các chữ số chia hết cho 3.",9:"Tổng các chữ số chia hết cho 9."}[d],f"{good[0]} chia hết cho {d}.","Dấu hiệu chia hết cho 2, 3, 5, 9.")
@reg(6,"Số nguyên")
def _(r):
    a,b=r.randint(-30,30),r.randint(-30,30)
    return FL(SH,"Cộng số nguyên",f"Tính: ({a}) + ({b})",a+b,"Cùng dấu: cộng giá trị tuyệt đối; khác dấu: trừ.",f"= {a+b}.","Quy tắc cộng số nguyên.")
@reg(6,"Số nguyên")
def _(r):
    a,b=r.randint(-12,12),r.randint(-12,12)
    return MC(r,SH,"Nhân số nguyên",f"({a}) · ({b}) = ?",vn(a*b),[vn(-a*b),vn(a+b),vn(abs(a*b)+1)],"Khác dấu thì tích âm.",f"= {vn(a*b)}.","Cùng dấu → dương; khác dấu → âm.") if a*b else None
@reg(6,"Số nguyên")
def _(r):
    t1=r.randint(-10,5);d=r.randint(3,15)
    return FL(SH,"Nhiệt độ",f"Nhiệt độ buổi sáng ở Sa Pa là {t1} °C, buổi trưa tăng thêm {d} °C. Nhiệt độ buổi trưa là bao nhiêu độ C?",t1+d,"Cộng số nguyên.",f"{t1} + {d} = {t1+d}.","Nhiệt độ dưới 0 °C là số âm.")
@reg(6,"Phân số")
def _(r):
    a,b,c,d=r.randint(1,9),r.randint(2,9),r.randint(1,9),r.randint(2,9);v=Fr(a,b)/Fr(c,d)
    return FL(SH,"Chia phân số",f"Tính {a}/{b} : {c}/{d} (ghi tối giản dạng a/b hoặc số nguyên).",v,"Nhân với phân số nghịch đảo.",f"= {a}/{b} · {d}/{c} = {v}.","Chia = nhân nghịch đảo.")
@reg(6,"Phân số")
def _(r):
    a,b=r.choice([(-2,3),(3,-4),(-5,6),(4,-7)])
    return MC(r,SH,"Phân số âm",f"Phân số {a}/{b} bằng phân số nào?",f"{-a}/{-b}",[f"{abs(a)}/{abs(b)}",f"{b}/{a}",f"{a}/{-b}"],"Nhân cả tử và mẫu với −1.",f"{a}/{b} = {-a}/{-b}.","a/b = (−a)/(−b).")
@reg(6,"Phân số")
def _(r):
    b=r.choice([3,4,5,8]);a=r.randint(1,b-1);x=a*r.randint(2,10)
    return FL(SH,"Tìm một số khi biết giá trị phân số",f"{a}/{b} của một số bằng {x}. Tìm số đó (ghi phân số tối giản nếu không nguyên).",Fr(x*b,a),"Lấy giá trị chia cho phân số.",f"{x} : {a}/{b} = {Fr(x*b,a)}.","Số cần tìm = giá trị : phân số.")
@reg(6,"Số thập phân")
def _(r):
    a=round(r.uniform(-20,20),1);b=round(r.uniform(-20,20),1)
    return FL(SH,"Cộng số thập phân",f"Tính: ({vn(a)}) + ({vn(b)}) (ghi số thập phân)",round(a+b,1),"Cộng như số nguyên rồi đặt dấu phẩy.",f"= {vn(round(a+b,1))}.","Quy tắc dấu như số nguyên.")
@reg(6,"Số thập phân")
def _(r):
    n=round(r.uniform(10,99),3);rd=round(n,1)
    return MC(r,SH,"Làm tròn",f"Làm tròn {vn(n)} đến hàng phần mười:",vn(rd),[vn(round(rd+0.1,1)),vn(round(n,2)),vn(round(n))],"Xét chữ số hàng phần trăm.",f"≈ {vn(rd)}.","Làm tròn số thập phân.") if abs(n*100-int(n*100)-0.5)>0.01 else None
@reg(6,"Số thập phân")
def _(r):
    p=r.choice([12,15,18,25,35]);P=r.choice([200000,450000,800000])
    return FL(SH,"Tỉ số phần trăm",f"Một chiếc áo giá {P:,} đồng được giảm {p}%. Giá sau khi giảm là bao nhiêu đồng?".replace(",","."),P*(100-p)//100,"Giá mới = giá cũ × (100% − "+str(p)+"%).",f"{P} × {100-p}% = {P*(100-p)//100}.","Giảm a% còn (100 − a)%.")
@reg(6,"Hình phẳng trong thực tiễn")
def _(r):
    a,h=r.randint(4,20),r.randint(3,15)
    return FL(HH,"Diện tích hình bình hành",f"Hình bình hành có cạnh đáy {a} cm và chiều cao tương ứng {h} cm. Diện tích là bao nhiêu cm²?",a*h,"S = đáy × chiều cao.",f"{a} × {h} = {a*h}.","S hình bình hành = a · h.")
@reg(6,"Hình phẳng trong thực tiễn")
def _(r):
    d1,d2=r.randint(4,20),r.randint(4,20)
    return MC(r,HH,"Diện tích hình thoi",f"Hình thoi có hai đường chéo dài {d1} cm và {d2} cm. Diện tích là:",f"{vn(d1*d2/2)} cm²",[f"{d1*d2} cm²",f"{2*(d1+d2)} cm²",f"{vn(d1*d2/4)} cm²"],"Tích hai đường chéo chia 2.",f"{d1} × {d2} : 2 = {vn(d1*d2/2)}.","S hình thoi = d₁ · d₂ : 2.")
@reg(6,"Hình phẳng trong thực tiễn")
def _(r):
    s=r.randint(2,12)
    return FL(HH,"Lục giác đều",f"Lục giác đều cạnh {s} cm được chia thành 6 tam giác đều. Chu vi lục giác là bao nhiêu xăng-ti-mét?",6*s,"Lục giác đều có 6 cạnh bằng nhau.",f"6 × {s} = {6*s}.","Lục giác đều: 6 cạnh, 6 góc bằng nhau.")
@reg(6,"Tính đối xứng của hình phẳng")
def _(r):
    x=r.choice([("hình vuông",4),("hình chữ nhật (không phải hình vuông)",2),("tam giác đều",3),("hình thoi (không phải hình vuông)",2),("lục giác đều",6),("hình tròn","vô số")])
    return MC(r,HH,"Trục đối xứng",f"{x[0].capitalize()} có bao nhiêu trục đối xứng?",x[1],[y for y in [0,1,2,3,4,6,"vô số"] if y!=x[1]][:3],"Gấp đôi hình sao cho hai nửa trùng nhau.",f"{x[0].capitalize()} có {x[1]} trục đối xứng.","Trục đối xứng chia hình thành hai nửa trùng khít.")
@reg(6,"Tính đối xứng của hình phẳng")
def _(r):
    x=r.choice([("Hình bình hành","có"),("Tam giác đều","không có"),("Hình thang cân","không có"),("Hình chữ nhật","có")])
    return MC(r,HH,"Tâm đối xứng",f"{x[0]} … tâm đối xứng.",x[1],["không có" if x[1]=="có" else "có","có hai","có vô số"],"Quay 180° quanh tâm thì hình trùng với chính nó.",f"{x[0]} {x[1]} tâm đối xứng.","Hình bình hành có tâm đối xứng là giao điểm hai đường chéo.")
@reg(6,"Tính đối xứng của hình phẳng")
def _(r):
    w=r.choice(["HOA","MẸ","TOÁN","VUI","MAI"]);sym={"H","O","A","M","T","V","U","I","Ạ","Ẹ"}
    k=sum(1 for c in w if c in "HOAMTVUI")
    return FL(HH,"Chữ cái có trục đối xứng",f"Trong từ “{w}”, có bao nhiêu chữ cái (không tính dấu) có trục đối xứng dọc?",sum(1 for c in w if c in "HOAMTVUIÁ"),"Kiểm tra từng chữ: gấp đôi theo chiều dọc.",f"Các chữ có trục đối xứng dọc: {', '.join(c for c in w if c in 'HOAMTVUIÁ')}.","A, H, I, M, O, T, U, V có trục đối xứng dọc.")
@reg(6,"Hình học cơ bản")
def _(r):
    n=r.randint(4,12)
    return FL(TH,"Đếm đoạn thẳng",f"Cho {n} điểm, không có ba điểm nào thẳng hàng. Vẽ đoạn thẳng nối mọi cặp điểm. Có bao nhiêu đoạn thẳng?",n*(n-1)//2,"Mỗi điểm nối với n − 1 điểm còn lại.",f"{n} · {n-1} : 2 = {n*(n-1)//2}.","Chia 2 vì mỗi đoạn được đếm hai lần.")
@reg(6,"Hình học cơ bản")
def _(r):
    L=2*r.randint(4,30)
    return MC(r,HH,"Trung điểm",f"M là trung điểm của đoạn thẳng AB, AB = {L} cm. Độ dài MB là:",f"{L//2} cm",[f"{L} cm",f"{L*2} cm",f"{L//2+1} cm"],"MA = MB = AB : 2.",f"{L} : 2 = {L//2}.","Trung điểm chia đoạn thẳng thành hai phần bằng nhau.")
@reg(6,"Hình học cơ bản")
def _(r):
    n=r.randint(3,8)
    return FL(TH,"Đếm góc",f"Từ điểm O vẽ {n} tia phân biệt (không có hai tia nào trùng nhau hay đối nhau). Có bao nhiêu góc tạo bởi hai trong các tia đó?",n*(n-1)//2,"Mỗi cặp tia tạo một góc.",f"{n} · {n-1} : 2 = {n*(n-1)//2}.","Đếm số cặp.")
@reg(6,"Dữ liệu và xác suất thực nghiệm")
def _(r):
    n=r.choice([20,25,40,50]);k=r.randint(3,n-3)
    return FL(XS,"Xác suất thực nghiệm",f"Tung một đồng xu {n} lần thấy {k} lần mặt ngửa. Xác suất thực nghiệm xuất hiện mặt ngửa là bao nhiêu? (ghi phân số tối giản)",Fr(k,n),"Số lần xảy ra : tổng số lần.",f"{k}/{n} = {Fr(k,n)}.","Xác suất thực nghiệm = k/n.")
@reg(6,"Dữ liệu và xác suất thực nghiệm")
def _(r):
    xs=[r.randint(5,25) for _ in range(4)];L=["Toán","Văn","Anh","Tin"]
    i=xs.index(max(xs))
    return MC(r,TK,"Biểu đồ cột",f"Biểu đồ cột về môn học yêu thích: Toán {xs[0]}, Văn {xs[1]}, Anh {xs[2]}, Tin {xs[3]} học sinh. Môn được yêu thích nhất là:",L[i],[x for j,x in enumerate(L) if j!=i],"Tìm cột cao nhất.",f"{L[i]} với {xs[i]} học sinh.","Cột cao nhất ứng với số liệu lớn nhất.") if xs.count(max(xs))==1 else None
@reg(6,"Dữ liệu và xác suất thực nghiệm")
def _(r):
    xs=[r.randint(5,25) for _ in range(4)]
    return FL(TK,"Bảng thống kê",f"Bảng thống kê số học sinh đi học bằng: xe đạp {xs[0]}, đi bộ {xs[1]}, xe buýt {xs[2]}, bố mẹ đưa {xs[3]}. Lớp có bao nhiêu học sinh?",sum(xs),"Cộng tất cả số liệu.",f"{' + '.join(map(str,xs))} = {sum(xs)}.","Tổng các tần số = số đối tượng.")

# ======================= LỚP 7 =======================
@reg(7,"Số hữu tỉ")
def _(r):
    a,b,c,d=r.randint(-9,9),r.randint(2,9),r.randint(-9,9),r.randint(2,9);v=Fr(a,b)+Fr(c,d)
    return FL(SH,"Cộng số hữu tỉ",f"Tính {a}/{b} + ({c}/{d}) (ghi tối giản dạng a/b hoặc số nguyên).",v,"Quy đồng mẫu.",f"= {v}.","Số hữu tỉ viết được dạng a/b.") if a and c else None
@reg(7,"Số hữu tỉ")
def _(r):
    a,n=r.choice([Fr(1,2),Fr(-1,2),Fr(2,3),Fr(-2,3),Fr(3,2)]),r.randint(2,4)
    return MC(r,SH,"Lũy thừa số hữu tỉ",f"({vn(a)})^{n} = ?",vn(a**n),[vn(a*n),vn(-(a**n)),vn(Fr(a.numerator**n,a.denominator))] ,"Lũy thừa cả tử và mẫu.",f"= {vn(a**n)}.","(a/b)ⁿ = aⁿ/bⁿ.")
@reg(7,"Số hữu tỉ")
def _(r):
    x=Fr(r.randint(-9,9),r.choice([2,3,4,5]));a=Fr(r.randint(1,5),r.choice([2,3,4]));b=x+a
    return FL(SH,"Tìm x",f"Tìm x biết x + {vn(a)} = {vn(b)} (ghi tối giản).",x,"Chuyển vế.",f"x = {vn(b)} − {vn(a)} = {vn(x)}.","Chuyển vế đổi dấu.")
@reg(7,"Số thực")
def _(r):
    n=r.randint(2,25)
    return FL(SH,"Căn bậc hai số học",f"Tính √{n*n}.",n,"Số không âm có bình phương bằng "+str(n*n)+".",f"√{n*n} = {n}.","√(a²) = a với a ≥ 0.")
@reg(7,"Số thực")
def _(r):
    n=r.choice([2,3,5,7,11]);v=round(math.sqrt(n),2)
    return MC(r,SH,"Làm tròn căn",f"Làm tròn √{n} đến hàng phần trăm được:",vn(v),[vn(round(v+0.01,2)),vn(round(math.sqrt(n),1)),vn(round(v-0.01,2))],"Dùng máy tính cầm tay.",f"√{n} ≈ {vn(v)}.","Số vô tỉ có phần thập phân vô hạn không tuần hoàn.")
@reg(7,"Số thực")
def _(r):
    a=r.randint(-20,20)
    return FL(SH,"Giá trị tuyệt đối",f"Tính |{a}| + |{-a-3}|.",abs(a)+abs(-a-3),"|x| là khoảng cách từ x đến 0.",f"{abs(a)} + {abs(-a-3)} = {abs(a)+abs(-a-3)}.","|x| ≥ 0.")
@reg(7,"Tỉ lệ thức và đại lượng tỉ lệ")
def _(r):
    a,b,k=r.randint(2,9),r.randint(2,9),r.randint(2,6)
    return FL(DS,"Tỉ lệ thức",f"Tìm x biết x/{a*k} = {b}/{a}.",b*k,"Nhân chéo.",f"x = {a*k} · {b} : {a} = {b*k}.","a/b = c/d ⇒ ad = bc.")
@reg(7,"Tỉ lệ thức và đại lượng tỉ lệ")
def _(r):
    n1,t1=r.randint(4,12),r.randint(6,20);cs=[x for x in range(2,25) if (n1*t1)%x==0 and x!=n1 and x!=t1]
    if not cs: return None
    n2=r.choice(cs)
    return MC(r,DS,"Tỉ lệ nghịch",f"{n1} công nhân làm xong một công việc trong {t1} ngày. Với {n2} công nhân (năng suất như nhau) thì làm xong trong bao nhiêu ngày?",n1*t1//n2,[t1*n2//n1 if t1*n2%n1==0 else t1+n2,n1*t1//n2+1,t1],"Số người và số ngày tỉ lệ nghịch.",f"{n1} · {t1} : {n2} = {n1*t1//n2}.","Tỉ lệ nghịch: tích không đổi.")
@reg(7,"Tỉ lệ thức và đại lượng tỉ lệ")
def _(r):
    a,b,c=r.randint(2,5),r.randint(2,6),r.randint(2,7);u=r.randint(3,20)
    return FL(DS,"Dãy tỉ số bằng nhau",f"Chia {(a+b+c)*u} quyển vở cho ba lớp tỉ lệ với {a}, {b}, {c}. Lớp thứ ba nhận bao nhiêu quyển?",c*u,"Dùng tính chất dãy tỉ số bằng nhau.",f"Mỗi phần {u}; lớp ba {c} × {u} = {c*u}.","x/a = y/b = z/c = (x + y + z)/(a + b + c).")
@reg(7,"Biểu thức đại số và đa thức")
def _(r):
    a,b,c,x=r.randint(1,5),r.randint(-9,9),r.randint(-9,9),r.randint(-3,3)
    return FL(DS,"Giá trị biểu thức",f"Tính giá trị của P(x) = {a}x² {'+' if b>=0 else '−'} {abs(b)}x {'+' if c>=0 else '−'} {abs(c)} tại x = {x}.",a*x*x+b*x+c,"Thay x vào biểu thức.",f"P({x}) = {a*x*x+b*x+c}.","Lũy thừa trước, nhân chia, rồi cộng trừ.")
@reg(7,"Biểu thức đại số và đa thức")
def _(r):
    a,b=r.randint(-9,9),r.randint(1,9)
    return MC(r,DS,"Nghiệm của đa thức",f"Nghiệm của đa thức P(x) = {b}x {'+' if -a*b>=0 else '−'} {abs(a*b)} là:",f"x = {vn(a)}",[f"x = {vn(-a)}",f"x = {vn(a*b)}",f"x = {vn(a+1)}"],"Giải P(x) = 0.",f"{b}x = {a*b} ⇒ x = {vn(a)}.","Nghiệm: giá trị làm đa thức bằng 0.") if a else None
@reg(7,"Biểu thức đại số và đa thức")
def _(r):
    n=r.randint(2,6);a=r.randint(2,9)
    return MC(r,DS,"Bậc của đa thức",f"Bậc của đa thức {a}x^{n} − 3x² + x − 1 (n = {n}) là:",max(n,2),[n+1,1,a] if max(n,2)!=a else [n+1,1,0],"Bậc là số mũ cao nhất.",f"Bậc {max(n,2)}.","Bậc đa thức một biến = số mũ lớn nhất.")
@reg(7,"Hình khối trong thực tiễn")
def _(r):
    a,b,h=r.randint(3,10),r.randint(3,10),r.randint(4,15)
    return FL(HH,"Lăng trụ đứng tam giác",f"Lăng trụ đứng có đáy là tam giác vuông với hai cạnh góc vuông {a} cm và {b} cm, chiều cao {h} cm. Thể tích là bao nhiêu cm³?",a*b*h/2,"V = S đáy × h.",f"{a} · {b} : 2 · {h} = {vn(a*b*h/2)}.","Thể tích lăng trụ đứng = diện tích đáy × chiều cao.")
@reg(7,"Hình khối trong thực tiễn")
def _(r):
    a,b,c=r.randint(2,9),r.randint(2,9),r.randint(2,9)
    return MC(r,HH,"Hình hộp chữ nhật",f"Hình hộp chữ nhật có kích thước {a} × {b} × {c} (cm). Thể tích là:",f"{a*b*c} cm³",[f"{2*(a*b+b*c+a*c)} cm³",f"{a+b+c} cm³",f"{a*b*c} cm²"],"V = a · b · c.",f"{a} · {b} · {c} = {a*b*c}.","Đơn vị thể tích cm³.")
@reg(7,"Hình khối trong thực tiễn")
def _(r):
    return MC(r,HH,"Số mặt, đỉnh","Hình lăng trụ đứng tam giác có bao nhiêu mặt?",5,[6,4,9],"2 mặt đáy + 3 mặt bên.","5 mặt (2 đáy, 3 mặt bên).","Lăng trụ đứng tứ giác có 6 mặt.")
@reg(7,"Góc và đường thẳng song song")
def _(r):
    a=r.randint(25,155)
    return FL(HH,"Góc so le trong",f"Hai đường thẳng song song bị một đường thẳng cắt. Một góc so le trong bằng {a}°. Góc so le trong còn lại bằng bao nhiêu độ?",a,"Hai đường thẳng song song thì góc so le trong bằng nhau.",f"Bằng {a}°.","Song song ⇒ so le trong bằng nhau, đồng vị bằng nhau.")
@reg(7,"Góc và đường thẳng song song")
def _(r):
    a=r.randint(25,155)
    return MC(r,HH,"Góc trong cùng phía",f"Hai đường thẳng song song bị cắt bởi một cát tuyến. Một góc trong cùng phía bằng {a}°. Góc trong cùng phía còn lại bằng:",f"{180-a}°",[f"{a}°",f"{90-a if a<90 else a-90}°",f"{360-a}°"],"Hai góc trong cùng phía bù nhau.",f"180° − {a}° = {180-a}°.","Trong cùng phía: tổng 180°.")
@reg(7,"Góc và đường thẳng song song")
def _(r):
    a=2*r.randint(20,80)
    return FL(HH,"Tia phân giác",f"Ot là tia phân giác của góc xOy, góc xOy = {a}°. Góc xOt bằng bao nhiêu độ?",a//2,"Tia phân giác chia đôi góc.",f"{a} : 2 = {a//2}°.","Phân giác: hai góc bằng nhau.")
@reg(7,"Tam giác bằng nhau")
def _(r):
    a,b=r.randint(30,80),r.randint(30,80)
    return FL(HH,"Tổng ba góc",f"Tam giác ABC có Â = {a}°, B̂ = {b}°. Tính Ĉ (độ).",180-a-b,"Tổng ba góc bằng 180°.",f"180 − {a} − {b} = {180-a-b}.","Tổng ba góc trong tam giác = 180°.")
@reg(7,"Tam giác bằng nhau")
def _(r):
    a=r.randint(20,140)
    return MC(r,HH,"Tam giác cân",f"Tam giác ABC cân tại A có Â = {a}°. Góc B bằng:",f"{vn((180-a)/2)}°",[f"{a}°",f"{180-a}°",f"{vn((180-a)/2+5)}°"],"Hai góc ở đáy bằng nhau.",f"(180 − {a}) : 2 = {vn((180-a)/2)}°.","Tam giác cân: hai góc đáy bằng nhau.")
@reg(7,"Tam giác bằng nhau")
def _(r):
    x=r.choice([("c.g.c","hai cạnh và góc xen giữa"),("g.c.g","một cạnh và hai góc kề"),("c.c.c","ba cạnh")])
    return MC(r,HH,"Trường hợp bằng nhau",f"Hai tam giác có {x[1]} tương ứng bằng nhau thì bằng nhau theo trường hợp:",x[0],[y for y in ["c.g.c","g.c.g","c.c.c","g.g.g"] if y!=x[0]],"Nhớ ba trường hợp bằng nhau.",f"Trường hợp {x[0]}.","g.g.g không phải trường hợp bằng nhau.")
@reg(7,"Quan hệ trong tam giác")
def _(r):
    a,b=r.randint(3,12),r.randint(3,12)
    return FL(HH,"Bất đẳng thức tam giác",f"Tam giác có hai cạnh {a} cm và {b} cm, cạnh thứ ba là số nguyên (cm). Có bao nhiêu giá trị có thể của cạnh thứ ba?",(a+b-1)-abs(a-b),"|a − b| < c < a + b.",f"{abs(a-b)} < c < {a+b}: có {(a+b-1)-abs(a-b)} giá trị.","Bất đẳng thức tam giác.")
@reg(7,"Quan hệ trong tam giác")
def _(r):
    xs=[(2,3,6),(3,4,5),(1,2,3),(4,5,10)];good=(3,4,5);r.shuffle(xs)
    return MC(r,HH,"Ba cạnh tam giác","Bộ ba độ dài nào là ba cạnh của một tam giác?","3 cm, 4 cm, 5 cm",["2 cm, 3 cm, 6 cm","1 cm, 2 cm, 3 cm","4 cm, 5 cm, 10 cm"],"Tổng hai cạnh nhỏ phải lớn hơn cạnh lớn nhất.","3 + 4 > 5.","a + b > c với c lớn nhất.")
@reg(7,"Quan hệ trong tam giác")
def _(r):
    m=r.randint(3,12)*3
    return FL(HH,"Trọng tâm",f"G là trọng tâm tam giác ABC, đường trung tuyến AM = {m} cm. Độ dài AG là bao nhiêu xăng-ti-mét?",m*2//3,"AG = 2/3 AM.",f"{m} · 2/3 = {m*2//3}.","Trọng tâm cách đỉnh 2/3 trung tuyến.")
@reg(7,"Thu thập và biểu diễn dữ liệu")
def _(r):
    n=r.choice([20,25,40,50]);k=r.randint(2,n-2)
    return FL(TK,"Biểu đồ hình quạt",f"Trong {n} học sinh có {k} bạn thích bơi. Trên biểu đồ hình quạt tròn, phần “bơi” chiếm bao nhiêu phần trăm? (ghi số)",k*100/n,"Tỉ lệ × 100%.",f"{k} : {n} × 100 = {vn(k*100/n)}%.","Biểu đồ hình quạt biểu diễn tỉ lệ %.")
@reg(7,"Thu thập và biểu diễn dữ liệu")
def _(r):
    xs=[r.randint(20,40) for _ in range(5)]
    i=max(range(1,5),key=lambda j:xs[j]-xs[j-1])
    return MC(r,TK,"Biểu đồ đoạn thẳng",f"Nhiệt độ trung bình 5 ngày: {', '.join(f'ngày {j+1}: {xs[j]}°C' for j in range(5))}. Nhiệt độ tăng nhiều nhất từ ngày nào sang ngày nào?",f"ngày {i} sang ngày {i+1}",[f"ngày {j} sang ngày {j+1}" for j in range(1,5) if j!=i],"Tính hiệu hai ngày liên tiếp.",f"Tăng {xs[i]-xs[i-1]}°C.","Biểu đồ đoạn thẳng cho thấy sự thay đổi.") if xs[i]>xs[i-1] else None
@reg(7,"Thu thập và biểu diễn dữ liệu")
def _(r):
    return MC(r,TK,"Loại biểu đồ","Để biểu diễn sự thay đổi nhiệt độ theo các ngày trong tuần, nên dùng loại biểu đồ nào?","Biểu đồ đoạn thẳng",["Biểu đồ hình quạt tròn","Biểu đồ tranh","Bảng số liệu ban đầu"],"Dữ liệu thay đổi theo thời gian.","Biểu đồ đoạn thẳng thể hiện xu hướng theo thời gian.","Hình quạt: cơ cấu; đoạn thẳng: xu hướng.")
@reg(7,"Biến cố và xác suất")
def _(r):
    n=r.randint(10,40);k=r.randint(2,n-2)
    return FL(XS,"Xác suất",f"Một hộp có {n} thẻ đánh số từ 1 đến {n}. Rút ngẫu nhiên một thẻ. Xác suất rút được thẻ ghi số chia hết cho 5 là bao nhiêu? (ghi phân số tối giản)",Fr(n//5,n),"Đếm số thẻ là bội của 5.",f"{n//5}/{n} = {Fr(n//5,n)}.","P = số kết quả thuận lợi / số kết quả có thể.")
@reg(7,"Biến cố và xác suất")
def _(r):
    x=r.choice([("Gieo xúc xắc được mặt có số chấm nhỏ hơn 7","chắc chắn"),("Gieo xúc xắc được mặt 7 chấm","không thể"),("Gieo xúc xắc được mặt chẵn","ngẫu nhiên")])
    return MC(r,XS,"Loại biến cố",f"Biến cố “{x[0]}” là biến cố:",x[1],[y for y in ["chắc chắn","không thể","ngẫu nhiên"] if y!=x[1]]+["đồng khả năng"],"Xét biến cố luôn, không bao giờ hay có thể xảy ra.",f"Biến cố {x[1]}.","Chắc chắn: P = 1; không thể: P = 0.")
@reg(7,"Biến cố và xác suất")
def _(r):
    return FL(XS,"Xác suất gieo xúc xắc","Gieo một con xúc xắc cân đối. Xác suất xuất hiện mặt có số chấm là số nguyên tố là bao nhiêu? (ghi phân số tối giản)","1/2","Số nguyên tố trong 1–6: 2, 3, 5.","3/6 = 1/2.","Liệt kê các kết quả thuận lợi.")

# ======================= LỚP 8 =======================
@reg(8,"Đa thức")
def _(r):
    a,b,c,d=[r.randint(-6,6) or 1 for _ in range(4)]
    A,B,C=a*c,a*d+b*c,b*d
    return FL(DS,"Nhân đa thức",f"Khai triển ({a}x {'+' if b>=0 else '−'} {abs(b)})({c}x {'+' if d>=0 else '−'} {abs(d)}) = Ax² + Bx + C. Tính B.",B,"Nhân từng hạng tử.",f"B = {a}·{d} + {b}·{c} = {B}.","Nhân đa thức với đa thức.")
@reg(8,"Đa thức")
def _(r):
    x,y=r.randint(-3,3),r.randint(-3,3);a,b=r.randint(1,4),r.randint(1,4)
    return MC(r,DS,"Giá trị đa thức nhiều biến",f"Giá trị của P = {a}x²y − {b}xy² tại x = {x}, y = {y} là:",vn(a*x*x*y-b*x*y*y),[vn(a*x*x*y+b*x*y*y),vn(-(a*x*x*y-b*x*y*y)) if a*x*x*y-b*x*y*y else "1",vn(a*x*y-b*x*y)],"Thay giá trị rồi tính.",f"= {vn(a*x*x*y-b*x*y*y)}.","Lũy thừa trước.")
@reg(8,"Đa thức")
def _(r):
    m,n=r.randint(1,5),r.randint(1,5);p=r.randint(1,4)
    return FL(DS,"Bậc của đơn thức",f"Bậc của đơn thức 5x^{m}y^{n}z^{p} là bao nhiêu?",m+n+p,"Cộng số mũ các biến.",f"{m} + {n} + {p} = {m+n+p}.","Bậc đơn thức = tổng số mũ.")
@reg(8,"Phân thức đại số")
def _(r):
    a=r.randint(-9,9)
    return FL(DS,"Điều kiện xác định",f"Phân thức (x + 1)/(x − {a}) xác định khi x ≠ ?" if a>=0 else f"Phân thức (x + 1)/(x + {-a}) xác định khi x ≠ ?",a,"Mẫu khác 0.",f"x ≠ {a}.","Phân thức xác định khi mẫu ≠ 0.")
@reg(8,"Phân thức đại số")
def _(r):
    a=r.randint(1,9)
    return MC(r,DS,"Rút gọn phân thức",f"Rút gọn (x² − {a*a})/(x − {a}) với x ≠ {a}:",f"x + {a}",[f"x − {a}",f"x + {a*a}",f"{a}x"],"Phân tích tử thành nhân tử.",f"(x − {a})(x + {a})/(x − {a}) = x + {a}.","Hiệu hai bình phương.")
@reg(8,"Phân thức đại số")
def _(r):
    a,b=r.randint(1,9),r.randint(1,9);x=r.choice([v for v in range(-5,10) if v not in (0,)])
    return FL(DS,"Giá trị phân thức",f"Tính giá trị của {a}/x + {b}/x tại x = {x} (ghi tối giản).",Fr(a+b,x),"Cộng hai phân thức cùng mẫu.",f"({a} + {b})/{x} = {Fr(a+b,x)}.","Cùng mẫu: cộng tử.")
@reg(8,"Phương trình và hàm số bậc nhất")
def _(r):
    a=r.randint(2,9);x=r.randint(-10,12);b=r.randint(-20,20)
    return FL(DS,"Giải phương trình bậc nhất",f"Giải phương trình {a}x {'+' if b>=0 else '−'} {abs(b)} = {a*x+b}.",x,"Chuyển vế rồi chia.",f"{a}x = {a*x} ⇒ x = {x}.","ax + b = 0 ⇒ x = −b/a.")
@reg(8,"Phương trình và hàm số bậc nhất")
def _(r):
    a=r.choice([v for v in range(-5,6) if v]);b=r.randint(-8,8);x=r.randint(-4,4)
    return MC(r,DS,"Hàm số bậc nhất",f"Cho hàm số y = {a}x {'+' if b>=0 else '−'} {abs(b)}. Giá trị của y tại x = {x} là:",a*x+b,near(r,a*x+b),"Thay x vào công thức.",f"y = {a}·({x}) {'+' if b>=0 else '−'} {abs(b)} = {a*x+b}.","Hàm số bậc nhất y = ax + b (a ≠ 0).")
@reg(8,"Phương trình và hàm số bậc nhất")
def _(r):
    v=r.choice([5,6,8,10]);x=r.randint(8,30)
    return FL(DS,"Giải bài toán bằng cách lập phương trình",f"Tuổi bố hiện nay gấp {v//2+1} lần tuổi con, tổng tuổi hai bố con là {x*(v//2+2)}. Con bao nhiêu tuổi?",x,"Gọi tuổi con là x.",f"x + {v//2+1}x = {x*(v//2+2)} ⇒ x = {x}.","Lập phương trình bậc nhất.")
@reg(8,"Hình khối trong thực tiễn")
def _(r):
    a,h=r.randint(2,12),r.randint(3,15)
    return FL(HH,"Thể tích hình chóp tứ giác đều",f"Hình chóp tứ giác đều có cạnh đáy {a} cm, chiều cao {h} cm. Thể tích là bao nhiêu cm³? (ghi phân số hoặc số)",Fr(a*a*h,3),"V = 1/3 · S đáy · h.",f"{a}² · {h} : 3 = {vn(Fr(a*a*h,3))}.","V hình chóp = 1/3 · S · h.")
@reg(8,"Hình khối trong thực tiễn")
def _(r):
    a,d=r.randint(3,12),r.randint(4,15)
    return MC(r,HH,"Diện tích xung quanh hình chóp đều",f"Hình chóp tứ giác đều có cạnh đáy {a} cm, trung đoạn {d} cm. Diện tích xung quanh là:",f"{2*a*d} cm²",[f"{a*d} cm²",f"{4*a*d} cm²",f"{a*a+2*a*d} cm²"],"Sxq = nửa chu vi đáy × trung đoạn.",f"{4*a} : 2 · {d} = {2*a*d}.","Sxq hình chóp đều = p · d.")
@reg(8,"Hình khối trong thực tiễn")
def _(r):
    return MC(r,HH,"Hình chóp tam giác đều","Hình chóp tam giác đều có bao nhiêu mặt bên?",3,[4,5,6],"Đáy là tam giác.","3 mặt bên là các tam giác cân bằng nhau.","Số mặt bên = số cạnh đáy.")
@reg(8,"Định lí Pythagore")
def _(r):
    p,q,h=r.choice([(3,4,5),(5,12,13),(6,8,10),(8,15,17),(9,12,15),(7,24,25)])
    return FL(HH,"Cạnh huyền",f"Tam giác vuông có hai cạnh góc vuông {p} cm và {q} cm. Cạnh huyền dài bao nhiêu xăng-ti-mét?",h,"Định lí Pythagore.",f"√({p}² + {q}²) = {h}.","c² = a² + b².")
@reg(8,"Định lí Pythagore")
def _(r):
    p,q,h=r.choice([(3,4,5),(5,12,13),(6,8,10),(8,15,17),(9,12,15),(12,16,20)])
    return MC(r,HH,"Cạnh góc vuông",f"Tam giác ABC vuông tại A có BC = {h} cm, AB = {p} cm. AC bằng:",f"{q} cm",[f"{h-p} cm",f"{h+p} cm",f"{q+1} cm"],"AC² = BC² − AB².",f"√({h}² − {p}²) = {q}.","Định lí Pythagore đảo chiều.")
@reg(8,"Định lí Pythagore")
def _(r):
    p,q,h=r.choice([(6,8,10),(9,12,15),(5,12,13),(12,16,20)])
    return FL(HH,"Bài toán thực tế",f"Một chiếc thang dài {h} m dựa vào tường, chân thang cách tường {p} m. Đỉnh thang cao bao nhiêu mét so với mặt đất?",q,"Thang, tường và mặt đất tạo thành tam giác vuông.",f"√({h}² − {p}²) = {q} m.","Ứng dụng định lí Pythagore.")
@reg(8,"Tứ giác")
def _(r):
    a,b,c=r.randint(60,120),r.randint(60,120),r.randint(60,120)
    d=360-a-b-c
    return FL(HH,"Tổng các góc tứ giác",f"Tứ giác ABCD có Â = {a}°, B̂ = {b}°, Ĉ = {c}°. Tính D̂ (độ).",d,"Tổng bốn góc của tứ giác bằng 360°.",f"360 − {a} − {b} − {c} = {d}.","Tổng các góc tứ giác = 360°.") if 20<d<200 else None
@reg(8,"Tứ giác")
def _(r):
    a=r.randint(40,140)
    return MC(r,HH,"Hình bình hành",f"Hình bình hành ABCD có Â = {a}°. Góc B bằng:",f"{180-a}°",[f"{a}°",f"{360-a}°",f"{90+a//2}°"],"Hai góc kề một cạnh bù nhau.",f"180 − {a} = {180-a}.","Hình bình hành: góc đối bằng nhau, góc kề bù nhau.")
@reg(8,"Tứ giác")
def _(r):
    d=r.choice([10,13,17,25]);p,q=r.choice([(6,8),(5,12),(8,15),(7,24)])
    h=int(math.hypot(p,q))
    return FL(HH,"Hình chữ nhật",f"Hình chữ nhật có hai cạnh {p} cm và {q} cm. Độ dài đường chéo là bao nhiêu xăng-ti-mét?",h,"Đường chéo là cạnh huyền.",f"√({p}² + {q}²) = {h}.","Hai đường chéo hình chữ nhật bằng nhau.")
@reg(8,"Định lí Thalès")
def _(r):
    ad,db,ae=r.randint(2,9),r.randint(2,9),r.randint(2,9)
    return FL(HH,"Định lí Thalès",f"Tam giác ABC có DE ∥ BC (D ∈ AB, E ∈ AC), AD = {ad} cm, DB = {db} cm, AE = {ae} cm. Tính EC (cm, ghi phân số hoặc số).",Fr(ae*db,ad),"AD/DB = AE/EC.",f"EC = {ae} · {db} : {ad} = {vn(Fr(ae*db,ad))}.","Định lí Thalès trong tam giác.")
@reg(8,"Định lí Thalès")
def _(r):
    bc=2*r.randint(3,15)
    return MC(r,HH,"Đường trung bình",f"M, N là trung điểm AB, AC của tam giác ABC; BC = {bc} cm. MN bằng:",f"{bc//2} cm",[f"{bc} cm",f"{bc*2} cm",f"{bc//2+1} cm"],"Đường trung bình bằng nửa cạnh đáy.",f"{bc} : 2 = {bc//2}.","MN ∥ BC và MN = BC/2.")
@reg(8,"Định lí Thalès")
def _(r):
    ab,ac,bc=r.randint(3,12),r.randint(3,12),r.randint(5,15)
    return FL(HH,"Tính chất phân giác",f"Tam giác ABC có AB = {ab} cm, AC = {ac} cm, BC = {bc} cm, AD là phân giác (D ∈ BC). Tính BD (cm, ghi phân số hoặc số).",Fr(bc*ab,ab+ac),"DB/DC = AB/AC.",f"BD = {bc} · {ab}/({ab} + {ac}) = {vn(Fr(bc*ab,ab+ac))}.","Phân giác chia cạnh đối theo tỉ lệ hai cạnh kề.") if ab+ac>bc and abs(ab-ac)<bc else None
@reg(8,"Tam giác đồng dạng")
def _(r):
    k=r.choice([2,3,Fr(3,2),Fr(5,2)]);p=r.randint(10,40)
    return FL(HH,"Tỉ số chu vi",f"Tam giác A′B′C′ đồng dạng với tam giác ABC theo tỉ số k = {vn(k)}. Chu vi tam giác ABC là {p} cm. Chu vi tam giác A′B′C′ là bao nhiêu xăng-ti-mét? (ghi số)",k*p,"Tỉ số chu vi bằng tỉ số đồng dạng.",f"{p} · {vn(k)} = {vn(k*p)}.","Chu vi tỉ lệ k, diện tích tỉ lệ k².")
@reg(8,"Tam giác đồng dạng")
def _(r):
    k=r.choice([2,3,4]);S=r.randint(3,20)
    return MC(r,HH,"Tỉ số diện tích",f"Hai tam giác đồng dạng với tỉ số {k}. Tam giác nhỏ có diện tích {S} cm². Diện tích tam giác lớn là:",f"{S*k*k} cm²",[f"{S*k} cm²",f"{S*k*k*k} cm²",f"{S+k} cm²"],"Tỉ số diện tích bằng bình phương tỉ số đồng dạng.",f"{S} · {k}² = {S*k*k}.","S′/S = k².")
@reg(8,"Tam giác đồng dạng")
def _(r):
    c=r.randint(2,9);s=r.randint(2,6);b=r.randint(10,40)
    return FL(HH,"Đo chiều cao bằng bóng",f"Một cọc cao {c} m có bóng dài {s} m. Cùng lúc đó bóng của một tòa nhà dài {b} m. Tòa nhà cao bao nhiêu mét? (ghi phân số hoặc số)",Fr(c*b,s),"Hai tam giác vuông đồng dạng.",f"{c} · {b} : {s} = {vn(Fr(c*b,s))}.","Ứng dụng tam giác đồng dạng.")
@reg(8,"Dữ liệu và biểu đồ")
def _(r):
    n=r.choice([32,40,45,50]);xs=[r.randint(3,15) for _ in range(3)];xs.append(n-sum(xs))
    if xs[3]<=0: return None
    return FL(TK,"Tỉ lệ phần trăm",f"Lớp 8A có {n} học sinh: {xs[0]} giỏi, {xs[1]} khá, {xs[2]} trung bình, còn lại chưa đạt. Học sinh chưa đạt chiếm bao nhiêu phần trăm? (ghi số)",round(xs[3]*100/n,2),"Tìm số học sinh chưa đạt trước.",f"{xs[3]} : {n} × 100 = {vn(round(xs[3]*100/n,2))}%.","Tỉ lệ % = phần : tổng × 100.")
@reg(8,"Dữ liệu và biểu đồ")
def _(r):
    return MC(r,TK,"Phân loại dữ liệu","Dữ liệu nào sau đây là dữ liệu định lượng (là số)?","Chiều cao của học sinh (cm)",["Màu sắc yêu thích","Môn thể thao yêu thích","Tên các tỉnh"],"Định lượng là dữ liệu số.","Chiều cao là số đo.","Định tính: mô tả; định lượng: số.")
@reg(8,"Dữ liệu và biểu đồ")
def _(r):
    a,b=r.randint(20,60),r.randint(20,60)
    return FL(TK,"Biểu đồ cột kép",f"Biểu đồ cột kép: năm 2024 cửa hàng bán {a} chiếc tivi, năm 2025 bán {b} chiếc. Tổng hai năm bán bao nhiêu chiếc?",a+b,"Đọc hai cột rồi cộng.",f"{a} + {b} = {a+b}.","Đọc biểu đồ cột kép.")
@reg(8,"Xác suất của biến cố")
def _(r):
    a,b=r.randint(2,9),r.randint(2,9)
    return FL(XS,"Xác suất",f"Hộp có {a} bi đỏ và {b} bi xanh. Lấy ngẫu nhiên 1 bi. Xác suất lấy được bi đỏ là bao nhiêu? (ghi phân số tối giản)",Fr(a,a+b),"Kết quả thuận lợi / tổng kết quả.",f"{a}/{a+b} = {Fr(a,a+b)}.","Các kết quả đồng khả năng.")
@reg(8,"Xác suất của biến cố")
def _(r):
    n=r.randint(20,60);k=r.randint(5,n-5)
    return MC(r,XS,"Xác suất thực nghiệm",f"Bắn {n} mũi tên thì trúng đích {k} lần. Xác suất thực nghiệm của biến cố “trúng đích” là:",vn(Fr(k,n)),[vn(Fr(n-k,n)),vn(Fr(k,n-k)) if n-k else "1",vn(Fr(n,k))],"Số lần trúng / tổng số lần.",f"{k}/{n} = {vn(Fr(k,n))}.","Xác suất thực nghiệm.")
@reg(8,"Xác suất của biến cố")
def _(r):
    s=r.randint(3,11);cnt=sum(1 for i in range(1,7) for j in range(1,7) if i+j==s)
    return FL(XS,"Gieo hai xúc xắc",f"Gieo hai con xúc xắc. Xác suất để tổng số chấm bằng {s} là bao nhiêu? (ghi phân số tối giản)",Fr(cnt,36),"Có 36 kết quả đồng khả năng.",f"{cnt}/36 = {Fr(cnt,36)}.","Liệt kê các cặp có tổng bằng "+str(s)+".")

# ======================= LỚP 9 (bổ sung) =======================
@reg(9,"Phương trình, bất phương trình bậc nhất")
def _(r):
    a=r.randint(2,9);b=r.randint(-20,20);c=r.randint(-20,20)
    import math as _m
    lo=_m.floor((c-b)/a)+1 if (c-b)%a else (c-b)//a+1
    return FL(DS,"Bất phương trình",f"Tìm số nguyên x nhỏ nhất thỏa mãn {a}x {'+' if b>=0 else '−'} {abs(b)} > {c}.",lo,"Chuyển vế, chia cho số dương.",f"x > {vn(Fr(c-b,a))} ⇒ x nhỏ nhất là {lo}.","Chia cho số dương: giữ chiều bất đẳng thức.")
@reg(9,"Phương trình, bất phương trình bậc nhất")
def _(r):
    p,q=r.randint(1,6),r.randint(1,6)
    return MC(r,DS,"Phương trình tích",f"Tập nghiệm của phương trình (x − {p})(x + {q}) = 0 là:",f"{{{p}; −{q}}}",[f"{{−{p}; {q}}}",f"{{{p}; {q}}}",f"{{{p}}}"],"Tích bằng 0 khi một thừa số bằng 0.",f"x = {p} hoặc x = −{q}.","A·B = 0 ⇔ A = 0 hoặc B = 0.")
@reg(9,"Phương trình, bất phương trình bậc nhất")
def _(r):
    a=r.randint(-9,9);b=r.randint(1,9)
    return FL(DS,"Phương trình chứa ẩn ở mẫu",f"Giải phương trình {b}/(x − {a}) = 1 (x ≠ {a})." if a>=0 else f"Giải phương trình {b}/(x + {-a}) = 1 (x ≠ {a}).",a+b,"Quy đồng, khử mẫu.",f"x − {a} = {b} ⇒ x = {a+b}.","Nhớ đối chiếu điều kiện xác định.")
@reg(9,"Hệ thức lượng trong tam giác vuông")
def _(r):
    h=2*r.randint(3,15)
    return FL(HH,"Tỉ số lượng giác",f"Tam giác vuông có cạnh huyền {h} cm và một góc nhọn 30°. Cạnh đối diện góc 30° dài bao nhiêu xăng-ti-mét?",h//2,"sin 30° = 1/2.",f"{h} · sin 30° = {h//2}.","Cạnh đối góc 30° bằng nửa cạnh huyền.")
@reg(9,"Hệ thức lượng trong tam giác vuông")
def _(r):
    p,q,h=r.choice([(3,4,5),(5,12,13),(8,15,17),(7,24,25)])
    return MC(r,LG,"sin, cos, tan",f"Tam giác ABC vuông tại A có AB = {p}, AC = {q}, BC = {h}. Giá trị sin B là:",f"{q}/{h}",[f"{p}/{h}",f"{q}/{p}",f"{p}/{q}"],"sin = đối / huyền.",f"sin B = AC/BC = {q}/{h}.","Sin đi học, cos không hư, tan đoàn kết…")
@reg(9,"Hệ thức lượng trong tam giác vuông")
def _(r):
    d=r.randint(10,60)
    return FL(HH,"Đo chiều cao",f"Từ một điểm cách chân tháp {d} m, nhìn đỉnh tháp với góc nâng 45°. Tháp cao bao nhiêu mét (bỏ qua chiều cao người đo)?",d,"tan 45° = 1.",f"h = {d} · tan 45° = {d}.","h = d · tan α.")
@reg(9,"Đa giác đều")
def _(r):
    n=r.choice([5,6,8,9,10,12])
    return FL(HH,"Góc đa giác đều",f"Mỗi góc trong của đa giác đều {n} cạnh bằng bao nhiêu độ?",(n-2)*180/n,"Tổng các góc trong chia cho số góc.",f"({n} − 2) · 180 : {n} = {vn((n-2)*180/n)}.","Tổng góc trong = (n − 2) · 180°.")
@reg(9,"Đa giác đều")
def _(r):
    n=r.choice([3,4,5,6,8,10,12])
    return MC(r,HH,"Phép quay",f"Phép quay tâm O với góc quay nhỏ nhất (khác 0°) giữ nguyên đa giác đều {n} cạnh tâm O là:",f"{vn(360/n)}°",[f"{vn(180/n)}°",f"{vn((n-2)*180/n)}°",f"{360-int(360/n)}°"],"Chia 360° cho số cạnh.",f"360° : {n} = {vn(360/n)}°.","Đa giác đều n cạnh: quay 360°/n.")
@reg(9,"Tần số và tần số tương đối")
def _(r):
    xs=[r.randint(1,10) for _ in range(5)];n=sum(xs);i=r.randint(0,4)
    return FL(TK,"Tần số tương đối",f"Bảng tần số điểm số (5, 6, 7, 8, 9): {', '.join(map(str,xs))}. Tần số tương đối của điểm {5+i} là bao nhiêu phần trăm? (ghi số, làm tròn 2 chữ số thập phân nếu cần)",round(xs[i]*100/n,2),"Tần số : tổng × 100%.",f"{xs[i]} : {n} × 100 ≈ {vn(round(xs[i]*100/n,2))}%.","Tần số tương đối = n_i / N.")

# ======================= LỚP 10 =======================
@reg(10,"Mệnh đề và tập hợp")
def _(r):
    a,b=r.randint(-5,3),r.randint(5,10);c,d=r.randint(a+1,b-1),r.randint(b+1,b+8)
    return FL(DS,"Giao hai tập hợp",f"Cho A = [{a}; {b}] và B = [{c}; {d}]. Tập A ∩ B là đoạn [m; n]. Tính m + n.",c+b,"Giao là phần chung.",f"A ∩ B = [{c}; {b}], m + n = {c+b}.","Biểu diễn trên trục số.")
@reg(10,"Mệnh đề và tập hợp")
def _(r):
    n=r.randint(2,6)
    return MC(r,DS,"Số tập con",f"Tập hợp có {n} phần tử có bao nhiêu tập con?",2**n,[n*n,2*n,2**n-1],"Mỗi phần tử: có hoặc không.",f"2^{n} = {2**n}.","Số tập con = 2ⁿ.")
@reg(10,"Mệnh đề và tập hợp")
def _(r):
    return MC(r,DS,"Mệnh đề phủ định","Phủ định của mệnh đề “∀x ∈ ℝ, x² ≥ 0” là:","∃x ∈ ℝ, x² < 0",["∀x ∈ ℝ, x² < 0","∃x ∈ ℝ, x² ≥ 0","∀x ∈ ℝ, x² ≤ 0"],"∀ đổi thành ∃, phủ định kết luận.","∃x ∈ ℝ, x² < 0.","Phủ định: ∀ ↔ ∃.")
@reg(10,"Bất phương trình bậc nhất hai ẩn")
def _(r):
    a,b,c=r.randint(1,5),r.randint(1,5),r.randint(5,20);x,y=r.randint(0,4),r.randint(0,4)
    ok=a*x+b*y<=c
    return MC(r,DS,"Nghiệm của bất phương trình",f"Cặp số ({x}; {y}) có là nghiệm của bất phương trình {a}x + {b}y ≤ {c} không?","Có" if ok else "Không",["Không" if ok else "Có","Chỉ khi x = y","Không xác định"],"Thay vào kiểm tra.",f"{a}·{x} + {b}·{y} = {a*x+b*y} {'≤' if ok else '>'} {c}.","Thay tọa độ điểm vào bất phương trình.")
@reg(10,"Bất phương trình bậc nhất hai ẩn")
def _(r):
    a,b=r.randint(2,6),r.randint(2,6);c=a*b*r.randint(1,3)
    pts=[(0,0),(c//a,0),(0,c//b)];F=lambda p:r_*p[0]+s_*p[1]
    r_,s_=r.randint(1,5),r.randint(1,5);best=max(r_*p[0]+s_*p[1] for p in pts)
    return FL(DS,"Giá trị lớn nhất trên miền nghiệm",f"Tìm giá trị lớn nhất của F = {r_}x + {s_}y trên miền x ≥ 0, y ≥ 0, {a}x + {b}y ≤ {c}.",best,"GTLN đạt tại một đỉnh của miền nghiệm.",f"Các đỉnh (0;0), ({c//a};0), (0;{c//b}) → max = {best}.","Xét giá trị tại các đỉnh.")
@reg(10,"Hàm số và đồ thị")
def _(r):
    a=r.choice([1,2,-1,-2]);p=r.randint(-4,4);q=r.randint(-6,6);b=-2*a*p;c=a*p*p+q
    return FL(DS,"Đỉnh parabol",f"Tìm tung độ đỉnh của parabol y = {a}x² {'+' if b>=0 else '−'} {abs(b)}x {'+' if c>=0 else '−'} {abs(c)}.",q,"x đỉnh = −b/(2a).",f"x = {p}, y = {q}.","Đỉnh I(−b/2a; −Δ/4a).")
@reg(10,"Hàm số và đồ thị")
def _(r):
    p,q=sorted(r.sample(range(-5,7),2))
    return MC(r,DS,"Dấu tam thức bậc hai",f"Tập nghiệm của bất phương trình x² − {p+q}x + {p*q} < 0 là:".replace("− -","+ ").replace("+ -","− "),f"({p}; {q})",[f"(−∞; {p}) ∪ ({q}; +∞)",f"[{p}; {q}]",f"({q}; +∞)"],"a > 0: âm giữa hai nghiệm.",f"Nghiệm {p} và {q} ⇒ ({p}; {q}).","Trong trái, ngoài cùng.")
@reg(10,"Hàm số và đồ thị")
def _(r):
    x=r.randint(0,6)
    return FL(DS,"Tập xác định",f"Hàm số y = √(x − {x}) + 1/(x − {x+3}) có tập xác định [a; +∞) \\ {{b}}. Tính a + b.",2*x+3,"Biểu thức dưới căn ≥ 0, mẫu ≠ 0.",f"x ≥ {x}, x ≠ {x+3} ⇒ a + b = {2*x+3}.","Tìm điều kiện xác định.")
@reg(10,"Hệ thức lượng trong tam giác")
def _(r):
    b,c=r.randint(2,9),r.randint(2,9)
    return FL(HH,"Định lí côsin",f"Tam giác ABC có AB = {c}, AC = {b}, góc A = 60°. Tính BC².",b*b+c*c-b*c,"a² = b² + c² − 2bc·cos A.",f"{b}² + {c}² − {b}·{c} = {b*b+c*c-b*c}.","cos 60° = 1/2.")
@reg(10,"Hệ thức lượng trong tam giác")
def _(r):
    a=r.randint(2,12)*2
    return MC(r,HH,"Định lí sin",f"Tam giác ABC có BC = {a} và Â = 30°. Bán kính đường tròn ngoại tiếp R bằng:",a,[a//2,2*a,a*3//2],"a/sin A = 2R.",f"2R = {a} : (1/2) = {2*a} ⇒ R = {a}.","Định lí sin.")
@reg(10,"Hệ thức lượng trong tam giác")
def _(r):
    p,q,h=r.choice([(3,4,5),(5,12,13),(6,8,10),(9,12,15)]);k=r.randint(1,3)
    a,b,c=p*k,q*k,h*k;s=(a+b+c)/2
    return FL(HH,"Công thức Heron",f"Tính diện tích tam giác có ba cạnh {a}, {b}, {c}.",a*b/2,"Heron: S = √(p(p−a)(p−b)(p−c)).",f"p = {vn(s)}; S = {vn(a*b/2)}.","Có thể nhận ra tam giác vuông.")
@reg(10,"Vectơ")
def _(r):
    a=(r.randint(-5,5),r.randint(-5,5));b=(r.randint(-5,5),r.randint(-5,5))
    return FL(HH,"Tích vô hướng",f"Cho a = ({a[0]}; {a[1]}), b = ({b[0]}; {b[1]}). Tính a · b.",a[0]*b[0]+a[1]*b[1],"Nhân tọa độ tương ứng rồi cộng.",f"= {a[0]*b[0]+a[1]*b[1]}.","a·b = x₁x₂ + y₁y₂.")
@reg(10,"Vectơ")
def _(r):
    a=(r.randint(-5,5),r.randint(-5,5));b=(r.randint(-5,5),r.randint(-5,5));k=r.randint(2,3)
    return MC(r,HH,"Tọa độ vectơ",f"Cho a = ({a[0]}; {a[1]}), b = ({b[0]}; {b[1]}). Tọa độ của {k}a − b là:",f"({k*a[0]-b[0]}; {k*a[1]-b[1]})",[f"({k*a[0]+b[0]}; {k*a[1]+b[1]})",f"({a[0]-b[0]}; {a[1]-b[1]})",f"({k*a[0]-b[0]}; {k*a[1]+b[1]})"],"Nhân rồi trừ từng tọa độ.","Tính từng thành phần.","ka − b = (kx₁ − x₂; ky₁ − y₂).")
@reg(10,"Vectơ")
def _(r):
    p,q,h=r.choice([(3,4,5),(6,8,10),(5,12,13),(8,15,17)])
    return FL(HH,"Độ dài vectơ",f"Tính độ dài vectơ u = ({p}; {-q}).",h,"|u| = √(x² + y²).",f"√({p}² + {q}²) = {h}.","Độ dài vectơ.")
@reg(10,"Tọa độ trong mặt phẳng")
def _(r):
    while True:
        x0,y0=r.randint(-5,5),r.randint(-5,5);c=r.randint(-30,30);v=3*x0+4*y0+c
        if v%5==0 and v: break
    return FL(HH,"Khoảng cách điểm – đường thẳng",f"Tính khoảng cách từ M({x0}; {y0}) đến đường thẳng 3x + 4y {'+' if c>=0 else '−'} {abs(c)} = 0.",abs(v)//5,"d = |ax₀ + by₀ + c|/√(a² + b²).",f"|{v}| : 5 = {abs(v)//5}.","Khoảng cách từ điểm đến đường thẳng.")
@reg(10,"Tọa độ trong mặt phẳng")
def _(r):
    a,b,rr=r.randint(-5,5),r.randint(-5,5),r.randint(1,9)
    return MC(r,HH,"Phương trình đường tròn",f"Đường tròn (x {'−' if a>=0 else '+'} {abs(a)})² + (y {'−' if b>=0 else '+'} {abs(b)})² = {rr*rr} có tâm và bán kính là:",f"I({a}; {b}), R = {rr}",[f"I({-a}; {-b}), R = {rr}",f"I({a}; {b}), R = {rr*rr}",f"I({b}; {a}), R = {rr}"],"Dạng (x − a)² + (y − b)² = R².",f"I({a}; {b}), R = {rr}.","Nhớ dấu ngược khi đọc tâm.")
@reg(10,"Tọa độ trong mặt phẳng")
def _(r):
    x1,y1,x2,y2=[r.randint(-6,6) for _ in range(4)]
    if x1==x2: return None
    return FL(HH,"Trung điểm",f"Cho A({x1}; {y1}), B({x2}; {y2}). Trung điểm M của AB có hoành độ bằng bao nhiêu? (ghi số thập phân nếu cần)",(x1+x2)/2,"x_M = (x_A + x_B)/2.",f"({x1} + {x2}) : 2 = {vn((x1+x2)/2)}.","Công thức trung điểm.")
@reg(10,"Ba đường conic")
def _(r):
    a,b=r.choice([(5,4),(5,3),(13,12),(10,8),(10,6)]);c=int(math.sqrt(a*a-b*b))
    return FL(HH,"Tiêu cự elip",f"Elip (E): x²/{a*a} + y²/{b*b} = 1 có tiêu cự 2c bằng bao nhiêu?",2*c,"c² = a² − b².",f"c = √({a*a} − {b*b}) = {c}; 2c = {2*c}.","Elip: c² = a² − b².")
@reg(10,"Ba đường conic")
def _(r):
    a,b=r.choice([(3,4),(4,3),(6,8),(5,12)]);c=int(math.hypot(a,b))
    return MC(r,HH,"Hypebol",f"Hypebol (H): x²/{a*a} − y²/{b*b} = 1 có tiêu điểm F₂(c; 0) với c bằng:",c,[a+b,abs(a-b),c+1],"c² = a² + b².",f"c = √({a*a} + {b*b}) = {c}.","Hypebol: c² = a² + b².")
@reg(10,"Ba đường conic")
def _(r):
    p=r.randint(1,8)
    return FL(HH,"Parabol",f"Parabol y² = {2*p}x có tiêu điểm F(m; 0). Tính m (ghi số thập phân nếu cần).",p/2,"y² = 2px có tiêu điểm (p/2; 0).",f"p = {p}, F({vn(p/2)}; 0).","Parabol chính tắc y² = 2px.")
@reg(10,"Số đặc trưng của mẫu số liệu")
def _(r):
    xs=sorted(r.randint(1,20) for _ in range(r.choice([5,7,9])));n=len(xs)
    return FL(TK,"Trung vị",f"Tìm trung vị của mẫu số liệu: {', '.join(map(str,r.sample(xs,n)))}.",xs[n//2],"Sắp xếp rồi lấy số ở giữa.",f"Sắp xếp: {', '.join(map(str,xs))} ⇒ Me = {xs[n//2]}.","n lẻ: trung vị là số chính giữa.")
@reg(10,"Số đặc trưng của mẫu số liệu")
def _(r):
    xs=[r.randint(1,30) for _ in range(6)]
    return MC(r,TK,"Khoảng biến thiên",f"Khoảng biến thiên của mẫu số liệu {', '.join(map(str,xs))} là:",max(xs)-min(xs),[max(xs),sum(xs)//6,max(xs)-min(xs)+1],"Lớn nhất trừ nhỏ nhất.",f"{max(xs)} − {min(xs)} = {max(xs)-min(xs)}.","R = x_max − x_min.")
@reg(10,"Số đặc trưng của mẫu số liệu")
def _(r):
    m=r.randint(3,10);d=[r.choice([-2,-1,1,2]) for _ in range(2)];xs=[m+d[0],m-d[0],m+d[1],m-d[1]]
    v=sum((x-m)**2 for x in xs)/4
    return FL(TK,"Phương sai",f"Tính phương sai của mẫu số liệu {', '.join(map(str,xs))} (ghi số thập phân nếu cần).",v,"s² = trung bình bình phương độ lệch.",f"x̄ = {m}; s² = {vn(v)}.","s² = (1/n)Σ(xᵢ − x̄)².")
@reg(10,"Xác suất cổ điển")
def _(r):
    a,b=r.randint(3,8),r.randint(3,8);v=Fr(math.comb(a,2),math.comb(a+b,2))
    return FL(XS,"Xác suất cổ điển",f"Hộp có {a} bi trắng và {b} bi đen. Lấy ngẫu nhiên 2 bi. Xác suất lấy được 2 bi trắng là bao nhiêu? (ghi phân số tối giản)",v,"Dùng tổ hợp.",f"C({a},2)/C({a+b},2) = {v}.","P(A) = n(A)/n(Ω).")
@reg(10,"Xác suất cổ điển")
def _(r):
    n=r.randint(3,5)
    return MC(r,XS,"Không gian mẫu",f"Tung một đồng xu {n} lần. Số phần tử của không gian mẫu là:",2**n,[2*n,n*n,2**n-1],"Mỗi lần có 2 kết quả.",f"2^{n} = {2**n}.","Quy tắc nhân.")
@reg(10,"Xác suất cổ điển")
def _(r):
    return FL(XS,"Biến cố đối","Gieo hai con xúc xắc. Xác suất để có ít nhất một mặt 6 chấm là bao nhiêu? (ghi phân số tối giản)","11/36","Dùng biến cố đối: không có mặt 6.","1 − (5/6)² = 11/36.","P(A) = 1 − P(Ā).")

# ======================= LỚP 11 =======================
@reg(11,"Hàm số và phương trình lượng giác")
def _(r):
    a=r.choice([30,45,60,120,135,150])
    import math as m
    v={30:"1/2",45:"√2/2",60:"√3/2",120:"√3/2",135:"√2/2",150:"1/2"}[a]
    return MC(r,LG,"Giá trị lượng giác",f"Giá trị của sin {a}° là:",v,[x for x in ["1/2","√2/2","√3/2","−1/2"] if x!=v],"Dùng đường tròn lượng giác.",f"sin {a}° = {v}.","sin(180° − α) = sin α.")
@reg(11,"Hàm số và phương trình lượng giác")
def _(r):
    k=r.choice([1,2,3,4])
    return FL(LG,"Chu kì",f"Hàm số y = sin({k}x) có chu kì T = mπ. Tính m (ghi phân số tối giản nếu cần).",Fr(2,k),"T = 2π/|k|.",f"T = 2π/{k} ⇒ m = {vn(Fr(2,k))}.","sin, cos có chu kì 2π; tan có chu kì π.")
@reg(11,"Hàm số và phương trình lượng giác")
def _(r):
    n=r.randint(2,6)
    return FL(LG,"Số nghiệm phương trình",f"Phương trình sin x = 0 có bao nhiêu nghiệm thuộc đoạn [0; {n}π]?",n+1,"sin x = 0 ⇔ x = kπ.",f"k = 0, 1, …, {n}: {n+1} nghiệm.","Nghiệm x = kπ.")
@reg(11,"Giới hạn, hàm số liên tục")
def _(r):
    a,b=r.randint(1,9),r.randint(1,9);c=r.randint(1,9)
    return FL(GT,"Giới hạn dãy số",f"Tính lim ({a}n² + {b}n)/({c}n² + 1) (ghi phân số tối giản).",Fr(a,c),"Chia tử và mẫu cho n².",f"= {a}/{c} = {vn(Fr(a,c))}.","Bậc tử = bậc mẫu: tỉ số hệ số cao nhất.")
@reg(11,"Giới hạn, hàm số liên tục")
def _(r):
    a=r.randint(1,9)
    return MC(r,GT,"Giới hạn dạng 0/0",f"lim(x→{a}) (x² − {a*a})/(x − {a}) bằng:",2*a,[a,0,a*a],"Phân tích tử thành nhân tử.",f"= lim (x + {a}) = {2*a}.","Khử dạng 0/0.")
@reg(11,"Giới hạn, hàm số liên tục")
def _(r):
    q=r.choice([Fr(1,2),Fr(1,3),Fr(2,3),Fr(1,4)]);u=r.randint(1,9)
    return FL(GT,"Cấp số nhân lùi vô hạn",f"Tính tổng S = {u} + {vn(u*q)} + {vn(u*q*q)} + … (cấp số nhân lùi vô hạn, ghi tối giản).",Fr(u)/(1-q),"S = u₁/(1 − q).",f"{u} : (1 − {vn(q)}) = {vn(Fr(u)/(1-q))}.","|q| < 1.")
@reg(11,"Quan hệ song song trong không gian")
def _(r):
    return MC(r,HH,"Vị trí tương đối","Hai đường thẳng phân biệt cùng song song với một mặt phẳng thì:","có thể cắt nhau, song song hoặc chéo nhau",["luôn song song","luôn cắt nhau","luôn chéo nhau"],"Vẽ thử trong hình hộp.","Cả ba khả năng đều xảy ra.","Đừng suy diễn từ hình phẳng.")
@reg(11,"Quan hệ song song trong không gian")
def _(r):
    x=r.choice([("hình hộp","6"),("hình lăng trụ tam giác","3")])
    return MC(r,HH,"Mặt phẳng song song",f"Trong {x[0]} ABCD.A′B′C′D′, mặt phẳng (ABCD) song song với mặt phẳng nào?","(A′B′C′D′)",["(ABB′A′)","(ADD′A′)","(BCC′B′)"],"Hai mặt đáy của hình hộp.","(ABCD) ∥ (A′B′C′D′).","Hình hộp có các cặp mặt đối song song.")
@reg(11,"Quan hệ song song trong không gian")
def _(r):
    return FL(HH,"Đếm cạnh song song","Trong hình lập phương ABCD.A′B′C′D′, có bao nhiêu cạnh song song với cạnh AB (không tính AB)?",3,"Các cạnh cùng phương với AB.","CD, A′B′, C′D′: 3 cạnh.","Lập phương có 12 cạnh chia 3 nhóm song song.")
@reg(11,"Mẫu số liệu ghép nhóm")
def _(r):
    f=[r.randint(2,12) for _ in range(4)];L=[(10,20),(20,30),(30,40),(40,50)];n=sum(f)
    mean=sum((a+b)/2*k for (a,b),k in zip(L,f))/n
    return FL(TK,"Số trung bình ghép nhóm",f"Mẫu ghép nhóm: [10;20): {f[0]}, [20;30): {f[1]}, [30;40): {f[2]}, [40;50): {f[3]}. Tính số trung bình (làm tròn 2 chữ số thập phân).",round(mean,2),"Dùng giá trị đại diện là trung điểm mỗi nhóm.",f"x̄ = (15·{f[0]} + 25·{f[1]} + 35·{f[2]} + 45·{f[3]})/{n} ≈ {vn(round(mean,2))}.","Giá trị đại diện = trung điểm nhóm.")
@reg(11,"Mẫu số liệu ghép nhóm")
def _(r):
    f=[r.randint(2,12) for _ in range(4)];i=f.index(max(f))
    return MC(r,TK,"Nhóm chứa mốt",f"Mẫu ghép nhóm: [0;5): {f[0]}, [5;10): {f[1]}, [10;15): {f[2]}, [15;20): {f[3]}. Nhóm chứa mốt là:",["[0;5)","[5;10)","[10;15)","[15;20)"][i],[x for j,x in enumerate(["[0;5)","[5;10)","[10;15)","[15;20)"]) if j!=i],"Nhóm có tần số lớn nhất.",f"Tần số lớn nhất {max(f)}.","Mốt nằm trong nhóm có tần số lớn nhất.") if f.count(max(f))==1 else None
@reg(11,"Quy tắc tính xác suất")
def _(r):
    p,q=r.choice([(Fr(1,2),Fr(1,3)),(Fr(2,3),Fr(3,4)),(Fr(3,5),Fr(1,2)),(Fr(4,5),Fr(2,3))])
    return FL(XS,"Quy tắc nhân",f"Hai xạ thủ bắn độc lập, xác suất bắn trúng lần lượt là {vn(p)} và {vn(q)}. Xác suất cả hai cùng bắn trúng là bao nhiêu? (ghi phân số tối giản)",p*q,"Hai biến cố độc lập: nhân xác suất.",f"{vn(p)} · {vn(q)} = {vn(p*q)}.","P(AB) = P(A)·P(B) khi độc lập.")
@reg(11,"Quy tắc tính xác suất")
def _(r):
    p,q=r.choice([(Fr(1,2),Fr(1,3)),(Fr(2,3),Fr(3,4)),(Fr(3,5),Fr(1,2))])
    v=1-(1-p)*(1-q)
    return MC(r,XS,"Ít nhất một",f"Hai xạ thủ bắn độc lập với xác suất trúng {vn(p)} và {vn(q)}. Xác suất có ít nhất một người bắn trúng là:",vn(v),[vn(p*q),vn(p+q) if p+q<=1 else vn(1-p*q),vn((1-p)*(1-q))],"Dùng biến cố đối.",f"1 − (1 − {vn(p)})(1 − {vn(q)}) = {vn(v)}.","P(A ∪ B) = 1 − P(Ā)P(B̄).")

# ======================= LỚP 12 =======================
@reg(12,"Độ phân tán của mẫu số liệu")
def _(r):
    f=[r.randint(2,10) for _ in range(4)]
    return MC(r,TK,"Khoảng biến thiên ghép nhóm",f"Mẫu ghép nhóm: [40;45): {f[0]}, [45;50): {f[1]}, [50;55): {f[2]}, [55;60): {f[3]}. Khoảng biến thiên của mẫu là:",20,[15,5,sum(f)],"Đầu mút phải nhóm cuối trừ đầu mút trái nhóm đầu.","60 − 40 = 20.","R = a_{k+1} − a₁.")
@reg(12,"Độ phân tán của mẫu số liệu")
def _(r):
    m=r.randint(5,20);d=r.choice([1,2,3]);xs=[m-d,m+d,m-d,m+d]
    return FL(TK,"Độ lệch chuẩn",f"Mẫu số liệu {', '.join(map(str,xs))} có độ lệch chuẩn bằng bao nhiêu?",d,"Tính phương sai rồi lấy căn.",f"x̄ = {m}; s² = {d*d}; s = {d}.","s = √(s²).")
@reg(12,"Độ phân tán của mẫu số liệu")
def _(r):
    f=[r.randint(3,10) for _ in range(4)];n=sum(f);L=[(0,10),(10,20),(20,30),(30,40)]
    mids=[5,15,25,35];mean=sum(a*b for a,b in zip(mids,f))/n;var=sum(b*(a-mean)**2 for a,b in zip(mids,f))/n
    return FL(TK,"Phương sai ghép nhóm",f"Mẫu ghép nhóm: [0;10): {f[0]}, [10;20): {f[1]}, [20;30): {f[2]}, [30;40): {f[3]}. Tính phương sai (làm tròn 2 chữ số thập phân).",round(var,2),"Dùng giá trị đại diện.",f"x̄ ≈ {vn(round(mean,2))}; s² ≈ {vn(round(var,2))}.","s² = (1/n)Σnᵢ(cᵢ − x̄)².")
@reg(12,"Xác suất có điều kiện")
def _(r):
    a,b=r.randint(3,9),r.randint(3,9);c=r.randint(1,a-1)
    return FL(XS,"Xác suất có điều kiện",f"Lớp có {a} nam và {b} nữ, trong đó có {c} bạn nam đeo kính và không bạn nữ nào đeo kính. Chọn ngẫu nhiên một bạn đeo kính. Biết bạn được chọn là nam, xác suất bạn đó đeo kính bằng bao nhiêu? (P(đeo kính | nam), ghi phân số tối giản)",Fr(c,a),"P(A|B) = P(AB)/P(B).",f"P = {c}/{a} = {vn(Fr(c,a))}.","Thu hẹp không gian mẫu về biến cố điều kiện.")
@reg(12,"Xác suất có điều kiện")
def _(r):
    pa=r.choice([Fr(1,2),Fr(2,5),Fr(3,5),Fr(1,4)]);pab=pa*r.choice([Fr(1,2),Fr(1,3),Fr(2,3)])
    return MC(r,XS,"Công thức xác suất có điều kiện",f"Cho P(B) = {vn(pa)} và P(A ∩ B) = {vn(pab)}. Khi đó P(A | B) bằng:",vn(pab/pa),[vn(pab),vn(pa*pab),vn(pa-pab) if pa!=2*pab else vn(1-pab)],"P(A|B) = P(A ∩ B)/P(B).",f"{vn(pab)} : {vn(pa)} = {vn(pab/pa)}.","Chia cho xác suất của biến cố điều kiện.")
@reg(12,"Xác suất có điều kiện")
def _(r):
    p1,q1,q2=r.choice([(Fr(3,5),Fr(1,20),Fr(1,10)),(Fr(7,10),Fr(1,50),Fr(1,25)),(Fr(1,2),Fr(1,10),Fr(1,5)),(Fr(4,5),Fr(1,25),Fr(1,20))])
    v=p1*q1+(1-p1)*q2
    return FL(XS,"Xác suất toàn phần",f"Máy I sản xuất {vn(p1*100)}% sản phẩm với tỉ lệ lỗi {vn(q1*100)}%, máy II sản xuất phần còn lại với tỉ lệ lỗi {vn(q2*100)}%. Lấy ngẫu nhiên một sản phẩm, xác suất sản phẩm bị lỗi bằng bao nhiêu? (ghi phân số tối giản)",v,"Công thức xác suất toàn phần.",f"{vn(p1)}·{vn(q1)} + {vn(1-p1)}·{vn(q2)} = {vn(v)}.","P(A) = P(B)P(A|B) + P(B̄)P(A|B̄).")
@reg(11,"Quan hệ song song trong không gian")
def _(r):
    L=2*r.randint(3,20);M,N=r.choice([("SA","SB"),("SA","SC"),("SB","SC")])
    e={("SA","SB"):"AB",("SA","SC"):"AC",("SB","SC"):"BC"}[(M,N)]
    return FL(HH,"Đường trung bình trong không gian",f"Cho hình chóp S.ABC có {e} = {L} cm. Gọi M, N lần lượt là trung điểm của {M} và {N}. Độ dài MN bằng bao nhiêu xăng-ti-mét? (MN song song với {e})",L//2,"MN là đường trung bình của một mặt bên.",f"MN = {e}/2 = {L//2}.","Đường trung bình song song và bằng nửa cạnh đáy.")
@reg(11,"Quan hệ song song trong không gian")
def _(r):
    k=r.choice([2,3,4]);L=k*r.randint(2,12)
    return FL(HH,"Thiết diện song song đáy",f"Hình chóp S.ABCD có đáy là hình vuông cạnh {L} cm. Mặt phẳng song song với đáy cắt SA tại M sao cho SM = SA/{k}. Thiết diện là hình vuông có cạnh bao nhiêu xăng-ti-mét?",L//k,"Thiết diện đồng dạng với đáy theo tỉ số SM/SA.",f"{L} : {k} = {L//k}.","Mặt phẳng song song đáy tạo thiết diện đồng dạng với đáy.")
@reg(11,"Quy tắc tính xác suất")
def _(r):
    pa,pb=r.choice([(Fr(1,2),Fr(1,3)),(Fr(2,5),Fr(1,4)),(Fr(3,10),Fr(1,2)),(Fr(1,3),Fr(1,4))]);pab=r.choice([Fr(1,10),Fr(1,12),Fr(1,20)])
    if pab>min(pa,pb): return None
    return FL(XS,"Quy tắc cộng",f"Cho hai biến cố A, B với P(A) = {vn(pa)}, P(B) = {vn(pb)}, P(AB) = {vn(pab)}. Tính P(A ∪ B) (ghi phân số tối giản).",pa+pb-pab,"Quy tắc cộng tổng quát.",f"{vn(pa)} + {vn(pb)} − {vn(pab)} = {vn(pa+pb-pab)}.","P(A ∪ B) = P(A) + P(B) − P(AB).")
