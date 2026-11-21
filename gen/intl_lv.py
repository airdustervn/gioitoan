"""Mẫu câu hỏi thi Toán quốc tế theo cấp lớp (đề mô phỏng, số liệu sinh ngẫu nhiên).
A: lớp 1–2 · B: lớp 3–4 · C: lớp 5–6 (dùng intl.gens) · D: lớp 7–9 · E: lớp 10–12.
Mỗi hàm trả về danh sách câu {t,q,vi,a,h,s,m}; đáp án luôn là số."""
import math, random
from fractions import Fraction as Fr
from intl import gens as genC
def T(t,q,vi,a,h,s,m): return {"t":t,"q":q,"vi":vi,"a":a,"h":h,"s":s,"m":m}
DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
VD=["thứ Hai","thứ Ba","thứ Tư","thứ Năm","thứ Sáu","thứ Bảy","Chủ nhật"]
NAMES=["Tom","Anna","Ben","Lily","Sam","Mia","Leo","Nam","Lan","Minh"]
VN={"Tom":"Tôm","Anna":"An","Ben":"Bình","Lily":"Ly","Sam":"Sơn","Mia":"My","Leo":"Long","Nam":"Nam","Lan":"Lan","Minh":"Minh"}
def isprime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def ndiv(n): return sum(1 for d in range(1,n+1) if n%d==0)

# ---------------- A: lớp 1–2 ----------------
def genA(r):
    R=r.randint;C=r.choice;L=[];nm=C(NAMES);vn=VN[nm]
    a,b=R(12,58),R(11,39);L.append(T("Số học",f"What is {a} + {b}?",f"Tính tổng {a} + {b}.",a+b,"Cộng hàng đơn vị trước, nhớ sang hàng chục.",[f"{a} + {b} = {a+b}."],"Cộng có nhớ."))
    a=R(40,99);b=R(11,a-10);L.append(T("Số học",f"What is {a} − {b}?",f"Tính hiệu {a} − {b}.",a-b,"Trừ hàng đơn vị trước.",[f"{a} − {b} = {a-b}."],"Trừ có nhớ."))
    a=R(15,45);c=R(a+5,a+50);L.append(T("Số học",f"Find the missing number: {a} + ? = {c}",f"Tìm số còn thiếu: {a} + ? = {c}",c-a,"Lấy tổng trừ số hạng đã biết.",[f"{c} − {a} = {c-a}."],"Số hạng chưa biết = tổng − số hạng đã biết."))
    n=R(4,12);L.append(T("Số học",f"A farmer has {n} chickens. How many legs do they have altogether?",f"Bác nông dân có {n} con gà. Tất cả có bao nhiêu chân?",2*n,"Mỗi con gà có 2 chân.",[f"{n} × 2 = {2*n}."],"Đếm theo nhóm 2."))
    n=R(3,9);L.append(T("Số học",f"There are {n} cats in a garden. How many legs are there in total?",f"Trong vườn có {n} con mèo. Có tất cả bao nhiêu chân?",4*n,"Mỗi con mèo có 4 chân.",[f"{n} × 4 = {4*n}."],"Đếm theo nhóm 4."))
    s0=R(2,9);k=R(2,6);seq=[s0+k*i for i in range(6)]
    L.append(T("Logic",f"What number comes next? {', '.join(map(str,seq[:5]))}, ?",f"Số tiếp theo của dãy là bao nhiêu? {', '.join(map(str,seq[:5]))}, ?",seq[5],f"Mỗi số hơn số trước {k}.",[f"{seq[4]} + {k} = {seq[5]}."],"Tìm khoảng cách giữa hai số liền nhau."))
    s0=R(60,99);k=R(3,9);seq=[s0-k*i for i in range(6)]
    L.append(T("Logic",f"Find the next number in the pattern: {', '.join(map(str,seq[:5]))}, ?",f"Tìm số tiếp theo trong dãy giảm: {', '.join(map(str,seq[:5]))}, ?",seq[5],f"Mỗi số kém số trước {k}.",[f"{seq[4]} − {k} = {seq[5]}."],"Dãy giảm đều."))
    a=R(12,30);b=R(3,a-4);c=R(2,15);L.append(T("Số học",f"{nm} has {a} stickers, gives away {b}, then gets {c} more. How many stickers does {nm} have now?",f"{vn} có {a} nhãn dán, cho bạn {b} cái rồi được tặng thêm {c} cái. {vn} còn bao nhiêu nhãn dán?",a-b+c,"Làm lần lượt: bớt đi rồi thêm vào.",[f"{a} − {b} + {c} = {a-b+c}."],"Tính từ trái sang phải."))
    x,y=r.sample(range(1,10),2);L.append(T("Số học",f"Using the digits {x} and {y} once each, what is the largest two-digit number you can make?",f"Dùng mỗi chữ số {x} và {y} một lần, số có hai chữ số lớn nhất viết được là?",10*max(x,y)+min(x,y),"Chữ số lớn hơn đặt ở hàng chục.",[f"Số lớn nhất: {10*max(x,y)+min(x,y)}."],"Hàng chục quyết định độ lớn."))
    a=R(5,30);b=R(a+8,a+40);L.append(T("Số học",f"How many whole numbers are there from {a} to {b}, including both?",f"Từ {a} đến {b} (tính cả hai số) có bao nhiêu số tự nhiên?",b-a+1,"Lấy số cuối trừ số đầu rồi cộng 1.",[f"{b} − {a} + 1 = {b-a+1}."],"Đếm cả hai đầu thì cộng 1."))
    a=R(10,30);b=R(a+10,a+40);ev=sum(1 for v in range(a+1,b) if v%2==0)
    L.append(T("Số học",f"How many even numbers are there between {a} and {b}?",f"Có bao nhiêu số chẵn nằm giữa {a} và {b} (không tính hai số đó)?",ev,"Liệt kê các số chẵn.",[f"Có {ev} số chẵn."],"Số chẵn tận cùng 0, 2, 4, 6, 8."))
    h=R(1,12);k=R(2,9);ans=(h+k-1)%12+1
    L.append(T("Logic",f"It is {h} o'clock now. What time will it be in {k} hours? (write the hour)",f"Bây giờ là {h} giờ. Sau {k} giờ nữa là mấy giờ? (ghi số giờ, theo mặt đồng hồ 12 giờ)",ans,"Quá 12 thì quay lại 1.",[f"{h} + {k} = {h+k}"+(f" → {ans} giờ." if h+k>12 else ".")],"Đồng hồ quay vòng 12 giờ."))
    st=R(0,6);k=R(3,12);L.append(T("Logic",f"Today is {DAYS[st]}. What day will it be in {k} days? (1 = Monday, …, 7 = Sunday)",f"Hôm nay là {VD[st]}. Sau {k} ngày nữa là thứ mấy? (ghi 1 = thứ Hai, …, 7 = Chủ nhật)",(st+k)%7+1,"Đếm tiếp từng ngày; 7 ngày là quay lại.",[f"Sau {k} ngày là {VD[(st+k)%7]}."],"Một tuần có 7 ngày."))
    a,b=R(2,8),R(1,6);L.append(T("Số học",f"{nm} has {a} coins of 2 cents and {b} coins of 5 cents. How many cents is that?",f"{vn} có {a} đồng xu loại 2 xu và {b} đồng loại 5 xu. Tất cả bao nhiêu xu?",2*a+5*b,"Tính từng loại rồi cộng.",[f"{a} × 2 + {b} × 5 = {2*a+5*b}."],"Nhân rồi cộng."))
    a,b=R(2,6),R(2,6);L.append(T("Hình học",f"How many sides do {a} triangles and {b} squares have altogether?",f"{a} hình tam giác và {b} hình vuông có tất cả bao nhiêu cạnh?",3*a+4*b,"Tam giác 3 cạnh, hình vuông 4 cạnh.",[f"{a} × 3 + {b} × 4 = {3*a+4*b}."],"Nhớ số cạnh mỗi hình."))
    a,b=R(3,12),R(3,12);L.append(T("Logic",f"In a line, {nm} is {a}th from the front and {b}th from the back. How many children are in the line?",f"Trong một hàng, {vn} đứng thứ {a} tính từ đầu và thứ {b} tính từ cuối. Hàng có bao nhiêu bạn?",a+b-1,f"{vn} bị đếm hai lần.",[f"{a} + {b} − 1 = {a+b-1}."],"Trừ 1 vì đếm trùng một bạn."))
    a=R(5,9);d=R(2,6);k=R(2,8);L.append(T("Số học",f"Mai is {a} years old. Her brother is {d} years older. How old will her brother be in {k} years?",f"Mai {a} tuổi. Anh trai hơn Mai {d} tuổi. {k} năm nữa anh trai bao nhiêu tuổi?",a+d+k,"Tìm tuổi anh bây giờ trước.",[f"Anh: {a} + {d} = {a+d}; {k} năm nữa: {a+d+k}."],"Mỗi năm ai cũng thêm 1 tuổi."))
    n=R(6,24);m=R(3,15);L.append(T("Số học",f"Double {n}, then add {m}. What do you get?",f"Gấp đôi số {n} rồi cộng thêm {m}. Kết quả là?",2*n+m,"Gấp đôi là nhân 2.",[f"{n} × 2 + {m} = {2*n+m}."],"Làm phép nhân trước."))
    k=R(2,5);n=R(3,9);L.append(T("Số học",f"A frog starts at 0 and jumps {k} steps each time. Where is it after {n} jumps?",f"Ếch bắt đầu ở số 0, mỗi lần nhảy {k} bậc. Sau {n} lần nhảy ếch ở số mấy?",k*n,"Nhảy đều nhau.",[f"{n} × {k} = {k*n}."],"Phép nhân là cộng lặp."))
    k=C([2,3,4,5]);n=k*R(3,9);L.append(T("Số học",f"{n} candies are shared equally among {k} children. How many does each child get?",f"Chia đều {n} cái kẹo cho {k} bạn. Mỗi bạn được mấy cái?",n//k,"Chia đều.",[f"{n} : {k} = {n//k}."],"Phép chia hết."))
    a=R(30,90);b=R(10,a-5);L.append(T("Số học",f"A red box has {a} beads and a blue box has {b} beads. How many more beads are in the red box?",f"Hộp đỏ có {a} hạt, hộp xanh có {b} hạt. Hộp đỏ nhiều hơn bao nhiêu hạt?",a-b,"Nhiều hơn: lấy hiệu.",[f"{a} − {b} = {a-b}."],"So sánh bằng phép trừ."))
    n=R(23,98);L.append(T("Số học",f"What is the sum of the digits of {n}?",f"Tổng các chữ số của số {n} là?",n//10+n%10,"Cộng chữ số hàng chục và hàng đơn vị.",[f"{n//10} + {n%10} = {n//10+n%10}."],"Tách hàng chục, hàng đơn vị."))
    s=R(3,12);cnt=sum(1 for v in range(10,100) if v//10+v%10==s)
    L.append(T("Tổ hợp",f"How many two-digit numbers have digits that add up to {s}?",f"Có bao nhiêu số có hai chữ số mà tổng hai chữ số bằng {s}?",cnt,"Thử lần lượt chữ số hàng chục.",[f"Đếm được {cnt} số."],"Hàng chục khác 0."))
    a=R(2,6);n=R(3,8);L.append(T("Số học",f"One bag of rice weighs {a} kg. How many kilograms do {n} bags weigh?",f"Một bao gạo nặng {a} kg. {n} bao như thế nặng bao nhiêu ki-lô-gam?",a*n,"Nhân với số bao.",[f"{a} × {n} = {a*n}."],"Các bao như nhau thì nhân."))
    p=C([2,3,4,5]);L0=p*R(4,10);L.append(T("Số học",f"A ribbon {L0} cm long is cut into pieces of {p} cm. How many pieces are there?",f"Sợi ruy băng dài {L0} cm cắt thành các đoạn dài {p} cm. Được bao nhiêu đoạn?",L0//p,"Chia chiều dài cho mỗi đoạn.",[f"{L0} : {p} = {L0//p}."],"Chia đều."))
    n=R(4,10);d=C([2,3,5]);L.append(T("Logic",f"{n} trees stand in a row, {d} m apart. How far is it from the first tree to the last tree, in metres?",f"{n} cây trồng thẳng hàng, hai cây liền nhau cách {d} m. Từ cây đầu đến cây cuối dài bao nhiêu mét?",(n-1)*d,"Số khoảng ít hơn số cây 1.",[f"({n} − 1) × {d} = {(n-1)*d}."],"Số khoảng = số cây − 1."))
    n=C([3,4,5]);L.append(T("Hình học",f"A strip has {n} small squares in a row. How many rectangles of any size can you find (squares count too)?",f"Một dải gồm {n} ô vuông nhỏ xếp thẳng hàng. Đếm được tất cả bao nhiêu hình chữ nhật (kể cả hình vuông)?",n*(n+1)//2,"Đếm theo số ô ghép lại.",[" + ".join(str(i) for i in range(n,0,-1))+f" = {n*(n+1)//2}."],"Đếm có thứ tự để không sót."))
    a=R(10,40);b=R(5,30);c=R(5,20);L.append(T("Số học",f"What is {a} + {b} − {c}?",f"Tính {a} + {b} − {c}.",a+b-c,"Tính lần lượt từ trái sang phải.",[f"{a+b} − {c} = {a+b-c}."],"Thứ tự thực hiện phép tính."))
    a,b=C([(5,10),(10,20),(10,50),(20,50)]);x=R(1,4);y=R(1,4);L.append(T("Số học",f"{nm} pays with {x} notes of {b} and {y} notes of {a}. How much money is that?",f"{vn} đưa {x} tờ {b} nghìn và {y} tờ {a} nghìn. Tất cả bao nhiêu nghìn đồng?",x*b+y*a,"Tính từng loại tiền.",[f"{x} × {b} + {y} × {a} = {x*b+y*a}."],"Cộng các mệnh giá."))
    n=R(2,5);L.append(T("Hình học",f"How many squares of any size are in a {n} × {n} grid?",f"Lưới ô vuông {n} × {n} có tất cả bao nhiêu hình vuông?",sum(i*i for i in range(1,n+1)),"Đếm hình 1×1, 2×2, …",[" + ".join(str(i*i) for i in range(n,0,-1))+f" = {sum(i*i for i in range(1,n+1))}."],"Đếm theo kích thước."))
    r.shuffle(L);return L

# ---------------- B: lớp 3–4 ----------------
def genB(r):
    R=r.randint;C=r.choice;L=[];nm=C(NAMES);vn=VN[nm]
    a=R(12,98);b=R(3,9);L.append(T("Số học",f"Calculate {a} × {b}.",f"Tính {a} × {b}.",a*b,"Nhân từng hàng.",[f"{a} × {b} = {a*b}."],"Nhân số có hai chữ số."))
    d=R(3,9);n=R(50,500);L.append(T("Số học",f"What is the remainder when {n} is divided by {d}?",f"Số dư khi chia {n} cho {d} là?",n%d,"Chia rồi tìm phần dư.",[f"{n} = {d} × {n//d} + {n%d}."],"Số dư nhỏ hơn số chia."))
    w=R(3,15);l=R(w+1,w+20);L.append(T("Hình học",f"A rectangle is {l} cm long and {w} cm wide. What is its perimeter in cm?",f"Hình chữ nhật dài {l} cm, rộng {w} cm. Chu vi bằng bao nhiêu xăng-ti-mét?",2*(l+w),"(dài + rộng) × 2.",[f"({l} + {w}) × 2 = {2*(l+w)}."],"Chu vi hình chữ nhật."))
    w=R(3,12);l=R(w+1,w+15);L.append(T("Hình học",f"Find the area of a rectangle that is {l} m long and {w} m wide, in m².",f"Tính diện tích hình chữ nhật dài {l} m, rộng {w} m (m²).",l*w,"Dài × rộng.",[f"{l} × {w} = {l*w}."],"Diện tích hình chữ nhật."))
    s=R(3,15);L.append(T("Hình học",f"A square has a perimeter of {4*s} cm. What is its area in cm²?",f"Hình vuông có chu vi {4*s} cm. Diện tích bằng bao nhiêu cm²?",s*s,"Tìm cạnh trước.",[f"Cạnh {4*s} : 4 = {s}; diện tích {s} × {s} = {s*s}."],"Cạnh = chu vi : 4."))
    n=R(10,30);L.append(T("Số học",f"Find 1 + 2 + 3 + … + {n}.",f"Tính tổng 1 + 2 + 3 + … + {n}.",n*(n+1)//2,"Ghép số đầu với số cuối.",[f"{n} × {n+1} : 2 = {n*(n+1)//2}."],"Ghép cặp."))
    a=R(1,9);d=C([2,3,4,5]);n=R(8,15);last=a+(n-1)*d
    L.append(T("Số học",f"Find the sum {a} + {a+d} + {a+2*d} + … + {last}.",f"Tính tổng dãy cách đều {a} + {a+d} + {a+2*d} + … + {last}.",(a+last)*n//2,"Đếm số số hạng rồi ghép cặp.",[f"Có {n} số hạng; tổng ({a} + {last}) × {n} : 2 = {(a+last)*n//2}."],"Tổng = (đầu + cuối) × số số hạng : 2."))
    while True:
        s=R(4,12);k=C([3,4,5]);f=s*k;m=k-1;y=None
        for yy in range(1,30):
            if (f+yy)==(k-1)*(s+yy): y=yy;break
        if y: break
    L.append(T("Số học",f"A father is {f} years old and his son is {s}. In how many years will the father be {k-1} times as old as his son?",f"Bố {f} tuổi, con {s} tuổi. Sau bao nhiêu năm nữa tuổi bố gấp {k-1} lần tuổi con?",y,"Hiệu số tuổi không đổi.",[f"Hiệu {f-s}; khi bố gấp {k-1} lần, con {(f-s)//(k-2)} tuổi → sau {y} năm."],"Hiệu tuổi không đổi theo thời gian."))
    h=R(10,20);rb=R(2,h-2);L.append(T("Logic",f"A farm has chickens and rabbits: {h} heads and {2*h+2*rb} legs. How many rabbits are there?",f"Có gà và thỏ, tất cả {h} đầu và {2*h+2*rb} chân. Có bao nhiêu con thỏ?",rb,"Giả sử tất cả là gà.",[f"{h} gà có {2*h} chân; thừa {2*rb} chân; mỗi thỏ thêm 2 → {rb} thỏ."],"Giả thiết tạm."))
    big=R(30,90);sm=R(10,big-5);L.append(T("Số học",f"The sum of two numbers is {big+sm} and their difference is {big-sm}. What is the larger number?",f"Tổng hai số là {big+sm}, hiệu là {big-sm}. Số lớn là?",big,"(tổng + hiệu) : 2.",[f"({big+sm} + {big-sm}) : 2 = {big}."],"Bài toán tổng – hiệu."))
    sm=R(6,30);k=C([2,3,4,5]);L.append(T("Số học",f"The sum of two numbers is {sm*(k+1)}. One number is {k} times the other. What is the smaller number?",f"Tổng hai số là {sm*(k+1)}, số này gấp {k} lần số kia. Số bé là?",sm,f"Số bé 1 phần, số lớn {k} phần.",[f"{sm*(k+1)} : {k+1} = {sm}."],"Bài toán tổng – tỉ."))
    N=R(20,99);L.append(T("Số học",f"How many digits are used to number the pages of a book from 1 to {N}?",f"Đánh số trang sách từ 1 đến {N} cần dùng bao nhiêu chữ số?",9+2*(N-9),"Trang 1–9 dùng 1 chữ số.",[f"9 + 2 × ({N} − 9) = {9+2*(N-9)}."],"Tách nhóm 1 chữ số, 2 chữ số."))
    st=R(0,6);N=R(20,100);L.append(T("Logic",f"Today is {DAYS[st]}. What day of the week will it be {N} days from today? (1 = Monday, …, 7 = Sunday)",f"Hôm nay là {VD[st]}. {N} ngày nữa là thứ mấy? (1 = thứ Hai, …, 7 = Chủ nhật)",(st+N)%7+1,"Chia số ngày cho 7, xem số dư.",[f"{N} chia 7 dư {N%7} → {VD[(st+N)%7]}."],"Chu kì tuần 7 ngày."))
    n=R(4,9);L.append(T("Tổ hợp",f"{n} friends each shake hands with every other friend once. How many handshakes are there?",f"{n} bạn, mỗi hai bạn bắt tay nhau một lần. Có tất cả bao nhiêu cái bắt tay?",n*(n-1)//2,"Mỗi bạn bắt tay "+str(n-1)+" bạn, rồi chia 2.",[f"{n} × {n-1} : 2 = {n*(n-1)//2}."],"Mỗi cái bắt tay được đếm hai lần."))
    k=C([3,4,6,7,8,9]);a=R(10,60);b=R(a+30,a+150);cnt=b//k-(a-1)//k
    L.append(T("Số học",f"How many numbers from {a} to {b} are multiples of {k}?",f"Từ {a} đến {b} có bao nhiêu số chia hết cho {k}?",cnt,"Tìm bội đầu tiên và bội cuối cùng.",[f"{b//k} − {(a-1)//k} = {cnt}."],"Đếm bội số trong một khoảng."))
    h1=R(6,9);m1=C([5,10,15,20,25,35,40,45,50]);dur=R(40,130);t2=h1*60+m1+dur
    L.append(T("Logic",f"A film starts at {h1}:{m1:02d} and lasts {dur} minutes. At what time does it end? (write as hours×100 + minutes, e.g. 9:05 → 905)",f"Bộ phim bắt đầu lúc {h1} giờ {m1} phút và kéo dài {dur} phút. Phim kết thúc lúc mấy giờ? (ghi giờ × 100 + phút, ví dụ 9 giờ 5 phút ghi 905)",(t2//60)*100+t2%60,"Đổi ra phút rồi cộng.",[f"Kết thúc lúc {t2//60} giờ {t2%60} phút."],"60 phút = 1 giờ."))
    k=R(1,9);m=R(10,950);L.append(T("Số học",f"How many metres are there in {k} km {m} m?",f"{k} km {m} m bằng bao nhiêu mét?",1000*k+m,"1 km = 1000 m.",[f"{k} × 1000 + {m} = {1000*k+m}."],"Đổi đơn vị độ dài."))
    p,q=C([(1,2),(1,3),(2,3),(1,4),(3,4),(2,5),(3,5)]);n=q*R(4,20);L.append(T("Số học",f"What is {p}/{q} of {n}?",f"{p}/{q} của {n} là bao nhiêu?",n*p//q,"Chia cho mẫu rồi nhân với tử.",[f"{n} : {q} × {p} = {n*p//q}."],"Tìm phân số của một số."))
    k=R(3,6);avg=R(10,40);vals=[avg+R(-8,8) for _ in range(k-1)];last=avg*k-sum(vals)
    if last<=0: last=avg;vals=[avg]*(k-1)
    vals.append(last);L.append(T("Số học",f"Find the average of {', '.join(map(str,vals))}.",f"Tìm trung bình cộng của các số {', '.join(map(str,vals))}.",avg,"Cộng tất cả rồi chia cho số các số.",[f"Tổng {avg*k} : {k} = {avg}."],"Trung bình cộng."))
    d=C([2,3,4,5]);Lr=d*R(8,30);L.append(T("Logic",f"Trees are planted along a {Lr} m road, {d} m apart, with a tree at both ends. How many trees are there?",f"Trồng cây dọc con đường dài {Lr} m, cây nọ cách cây kia {d} m, hai đầu đều có cây. Có bao nhiêu cây?",Lr//d+1,"Số cây = số khoảng + 1.",[f"{Lr} : {d} + 1 = {Lr//d+1}."],"Trồng cây hai đầu."))
    pc=R(3,8);t=C([2,3,4,5]);L.append(T("Logic",f"A log is cut into {pc} pieces. Each cut takes {t} minutes. How many minutes does the cutting take?",f"Cưa một khúc gỗ thành {pc} đoạn, mỗi lần cưa mất {t} phút. Cưa hết bao nhiêu phút?",(pc-1)*t,"Số lần cưa ít hơn số đoạn 1.",[f"({pc} − 1) × {t} = {(pc-1)*t}."],"Số lần cắt = số đoạn − 1."))
    s=R(5,25);v=next(x for x in range(100,1000) if sum(map(int,str(x)))==s)
    L.append(T("Số học",f"What is the smallest three-digit number whose digits add up to {s}?",f"Số nhỏ nhất có ba chữ số mà tổng các chữ số bằng {s} là?",v,"Hàng trăm nhỏ nhất có thể, hàng đơn vị lớn nhất có thể.",[f"Số đó là {v}."],"Muốn số nhỏ: chữ số lớn dồn về bên phải."))
    n=R(5,15);L.append(T("Số học",f"What is the sum of the first {n} odd numbers, 1 + 3 + 5 + …?",f"Tổng của {n} số lẻ đầu tiên 1 + 3 + 5 + … là?",n*n,"Thử với 1, 2, 3 số hạng để thấy quy luật.",[f"Tổng {n} số lẻ đầu tiên = {n} × {n} = {n*n}."],"Tổng n số lẻ đầu tiên = n × n."))
    k=R(3,8);p=C([12,15,18,25,35,45]);B=C([200,500]);
    if k*p>=B: B=500
    L.append(T("Số học",f"{nm} buys {k} notebooks at {p} thousand dong each and pays with a {B} thousand note. How much change, in thousand dong?",f"{vn} mua {k} quyển vở, mỗi quyển {p} nghìn đồng, đưa tờ {B} nghìn. Được trả lại bao nhiêu nghìn đồng?",B-k*p,"Tính tiền vở trước.",[f"{B} − {k} × {p} = {B-k*p}."],"Tiền thừa = tiền đưa − tiền hàng."))
    x,y=R(3,12),R(2,9);L.append(T("Số học",f"Define a ◆ b = a × b + a. What is {x} ◆ {y}?",f"Quy ước a ◆ b = a × b + a. Tính {x} ◆ {y}.",x*y+x,"Thay a và b vào công thức.",[f"{x} × {y} + {x} = {x*y+x}."],"Phép toán tự định nghĩa."))
    a,b=C([(4,6),(6,8),(6,9),(4,10),(8,12),(9,12)]);N=R(30,90);lc=a*b//math.gcd(a,b);v=(N//lc+1)*lc
    L.append(T("Số học",f"What is the smallest number greater than {N} that is divisible by both {a} and {b}?",f"Số nhỏ nhất lớn hơn {N} chia hết cho cả {a} và {b} là?",v,"Tìm BCNN.",[f"BCNN({a}, {b}) = {lc}; bội nhỏ nhất lớn hơn {N} là {v}."],"Chia hết cho cả hai ⇔ chia hết cho BCNN."))
    a0=R(1,5);seq=[a0*2**i for i in range(6)];L.append(T("Logic",f"What comes next: {', '.join(map(str,seq[:5]))}, ?",f"Số tiếp theo của dãy {', '.join(map(str,seq[:5]))}, ? là",seq[5],"Mỗi số gấp đôi số trước.",[f"{seq[4]} × 2 = {seq[5]}."],"Dãy nhân."))
    n=C([3,4]);L.append(T("Hình học",f"How many squares of all sizes can be found in a {n} × {n} grid?",f"Trong lưới {n} × {n} có tất cả bao nhiêu hình vuông?",sum(i*i for i in range(1,n+1)),"Đếm theo cạnh 1, 2, 3, …",[" + ".join(str(i*i) for i in range(n,0,-1))+f" = {sum(i*i for i in range(1,n+1))}."],"Đếm theo kích thước."))
    k=C([4,5,6]);L.append(T("Logic",f"A bag has red, blue{', green' if k>=5 else ''}{', yellow' if k>=6 else ''} and {k-2 if k<5 else ('2 other' if k==6 else '1 other')} colours of marbles — {k} colours in all. Without looking, how many marbles must you take to be sure two have the same colour?",f"Túi có bi {k} màu khác nhau. Không nhìn, phải lấy ít nhất bao nhiêu viên để chắc chắn có 2 viên cùng màu?",k+1,"Xét trường hợp xấu nhất.",[f"{k} viên có thể khác màu; viên thứ {k+1} chắc chắn trùng."],"Nguyên lí Dirichlet."))
    L[-1]["q"]=f"A bag has marbles in {k} different colours. Without looking, how many marbles must you take to be sure that two have the same colour?"
    r.shuffle(L);return L

# ---------------- D: lớp 7–9 ----------------
TRIP=[(3,4,5),(5,12,13),(8,15,17),(7,24,25),(6,8,10),(9,12,15),(20,21,29),(9,40,41),(12,16,20),(15,20,25)]
WORDS=[("LEVEL",30),("APPLE",60),("BANANA",60),("MATHS",120),("PEPPER",60),("COOKIE",180),("ARRAY",30),("NOON",6)]
def genD(r):
    R=r.randint;C=r.choice;L=[]
    a=R(2,9);x=R(-12,15);b=R(-30,30);c=a*x+b
    L.append(T("Đại số",f"Solve for x: {a}x {'+' if b>=0 else '−'} {abs(b)} = {c}.",f"Giải phương trình {a}x {'+' if b>=0 else '−'} {abs(b)} = {c}. Tìm x.",x,"Chuyển vế rồi chia.",[f"{a}x = {c-b} → x = {x}."],"Phương trình bậc nhất."))
    x=R(5,30);y=R(1,x-1);L.append(T("Đại số",f"If x + y = {x+y} and x − y = {x-y}, find xy.",f"Cho x + y = {x+y} và x − y = {x-y}. Tính xy.",x*y,"Cộng hai đẳng thức để tìm x.",[f"x = {x}, y = {y} → xy = {x*y}."],"Hệ phương trình bậc nhất."))
    P=C([200,400,500,800,1000]);u=C([10,20,25,50]);d=C([10,20,50]);v=P*(100+u)*(100-d)//10000
    L.append(T("Số học",f"A price of {P} is increased by {u}% and then the new price is decreased by {d}%. What is the final price?",f"Một món hàng giá {P}, tăng {u}% rồi giảm {d}% giá mới. Giá cuối cùng là?",v,"Nhân liên tiếp các hệ số.",[f"{P} × {(100+u)/100:g} × {(100-d)/100:g} = {v}."],"Tăng rồi giảm cùng % không về giá cũ."))
    p,q,h=C(TRIP);L.append(T("Hình học",f"A right triangle has legs {p} and {q}. How long is the hypotenuse?",f"Tam giác vuông có hai cạnh góc vuông {p} và {q}. Cạnh huyền dài bao nhiêu?",h,"Định lí Pythagore.",[f"√({p}² + {q}²) = √{p*p+q*q} = {h}."],"c² = a² + b²."))
    p,q,h=C(TRIP);L.append(T("Hình học",f"A right triangle has hypotenuse {h} and one leg {p}. What is its area?",f"Tam giác vuông có cạnh huyền {h}, một cạnh góc vuông {p}. Diện tích tam giác bằng?",p*q//2 if p*q%2==0 else p*q/2,"Tìm cạnh góc vuông còn lại.",[f"Cạnh còn lại √({h}² − {p}²) = {q}; diện tích {p} × {q} : 2 = {p*q/2:g}."],"Diện tích tam giác vuông = nửa tích hai cạnh góc vuông."))
    n=C([5,6,8,9,10,12,15,18,20]);L.append(T("Hình học",f"What is the measure, in degrees, of each interior angle of a regular {n}-gon?",f"Mỗi góc trong của đa giác đều {n} cạnh bằng bao nhiêu độ?",(n-2)*180//n if (n-2)*180%n==0 else (n-2)*180/n,"Tổng góc trong rồi chia đều.",[f"({n} − 2) × 180 : {n} = {(n-2)*180/n:g}."],"Tổng góc trong = (n − 2) × 180°."))
    n=R(6,20);L.append(T("Hình học",f"How many diagonals does a convex polygon with {n} sides have?",f"Đa giác lồi {n} cạnh có bao nhiêu đường chéo?",n*(n-3)//2,"Mỗi đỉnh nối với n − 3 đỉnh.",[f"{n} × {n-3} : 2 = {n*(n-3)//2}."],"Số đường chéo = n(n − 3)/2."))
    g=R(2,12);x,y=C([(2,3),(3,4),(3,5),(4,7),(5,6),(5,8),(7,9)]);A,B=g*x,g*y
    L.append(T("Số học",f"The GCD of two numbers is {g} and their LCM is {g*x*y}. One number is {A}. What is the other?",f"ƯCLN của hai số là {g}, BCNN là {g*x*y}. Một số là {A}. Số kia là?",B,"Tích hai số = ƯCLN × BCNN.",[f"{g} × {g*x*y} : {A} = {B}."],"ab = ƯCLN × BCNN."))
    n=C([120,144,180,200,210,240,252,288,300,360,420,480,500,540,600,720]);L.append(T("Số học",f"How many positive divisors does {n} have?",f"{n} có bao nhiêu ước nguyên dương?",ndiv(n),"Phân tích ra thừa số nguyên tố.",[f"{n} có {ndiv(n)} ước."],"Số ước = tích (số mũ + 1)."))
    b=C([2,3,7,8,9]);e=R(30,300);L.append(T("Số học",f"What is the units digit of {b}^{e}?",f"Chữ số tận cùng của {b}^{e} là?",pow(b,e,10),"Tìm chu kì chữ số tận cùng.",[f"Chữ số tận cùng là {pow(b,e,10)}."],"Chu kì tận cùng dài tối đa 4."))
    a=R(2,9);n=R(20,99);m=C([7,9,11,13]);L.append(T("Số học",f"Find the remainder when {a}^{n} is divided by {m}.",f"Tìm số dư khi chia {a}^{n} cho {m}.",pow(a,n,m),"Tìm chu kì số dư.",[f"Số dư là {pow(a,n,m)}."],"Đồng dư thức."))
    k=R(3,9);L.append(T("Đại số",f"If x + 1/x = {k}, find x² + 1/x².",f"Cho x + 1/x = {k}. Tính x² + 1/x².",k*k-2,"Bình phương hai vế.",[f"{k}² − 2 = {k*k-2}."],"(x + 1/x)² = x² + 2 + 1/x²."))
    s=R(4,15);p=R(1,s*s//4);L.append(T("Đại số",f"If a + b = {s} and ab = {p}, find a² + b².",f"Cho a + b = {s}, ab = {p}. Tính a² + b².",s*s-2*p,"(a + b)² = a² + 2ab + b².",[f"{s}² − 2 × {p} = {s*s-2*p}."],"Hằng đẳng thức."))
    a1=R(-10,20);d=R(2,9);n=R(15,60);L.append(T("Đại số",f"An arithmetic sequence starts {a1}, {a1+d}, {a1+2*d}, … What is its {n}th term?",f"Cấp số cộng {a1}, {a1+d}, {a1+2*d}, … có số hạng thứ {n} bằng?",a1+(n-1)*d,"a_n = a₁ + (n − 1)d.",[f"{a1} + {n-1} × {d} = {a1+(n-1)*d}."],"Cấp số cộng."))
    s=R(3,11);cnt=sum(1 for i in range(1,7) for j in range(1,7) if i+j==s)
    L.append(T("Xác suất",f"Two fair dice are rolled. Of the 36 equally likely outcomes, how many give a sum of {s}?",f"Gieo hai con xúc xắc. Trong 36 kết quả, có bao nhiêu kết quả có tổng bằng {s}?",cnt,"Liệt kê các cặp.",[f"Có {cnt} cặp."],"Đếm có thứ tự (1, 2) khác (2, 1)."))
    n=R(6,12);k=C([2,3]);L.append(T("Tổ hợp",f"In how many ways can a committee of {k} be chosen from {n} students?",f"Có bao nhiêu cách chọn {k} bạn từ {n} học sinh để lập một nhóm?",math.comb(n,k),"Không phân biệt thứ tự.",[f"C({n}, {k}) = {math.comb(n,k)}."],"Tổ hợp chập k."))
    w,c=C(WORDS);L.append(T("Tổ hợp",f"How many different arrangements of the letters of the word {w} are there?",f"Có bao nhiêu cách sắp xếp các chữ cái của từ {w}?",c,"Chia cho số cách đổi chỗ các chữ cái giống nhau.",[f"Số cách: {c}."],"Hoán vị có lặp."))
    rr=R(2,12);L.append(T("Hình học",f"A circle has radius {rr}. Its area is kπ. Find k.",f"Hình tròn bán kính {rr} có diện tích kπ. Tìm k.",rr*rr,"S = πr².",[f"k = {rr}² = {rr*rr}."],"Diện tích hình tròn."))
    a,b=C([(30,60),(20,30),(40,60),(12,24),(60,90),(10,15)]);L.append(T("Số học",f"A car goes from A to B at {a} km/h and returns at {b} km/h. What is its average speed for the round trip, in km/h?",f"Ô tô đi từ A đến B với vận tốc {a} km/giờ và về với {b} km/giờ. Vận tốc trung bình cả đi lẫn về (km/giờ)?",2*a*b//(a+b) if 2*a*b%(a+b)==0 else 2*a*b/(a+b),"Không lấy trung bình hai vận tốc.",[f"2 × {a} × {b} : ({a} + {b}) = {2*a*b/(a+b):g}."],"Vận tốc TB = tổng quãng đường : tổng thời gian."))
    t1,t2=C([(3,6),(4,12),(6,12),(10,15),(12,24),(20,30)]);tt=t1*t2/(t1+t2)
    L.append(T("Số học",f"A can finish a job in {t1} days and B in {t2} days. How many days do they take working together?",f"A làm xong việc trong {t1} ngày, B trong {t2} ngày. Hai người cùng làm hết bao nhiêu ngày?",int(tt) if tt==int(tt) else tt,"Cộng năng suất.",[f"1/{t1} + 1/{t2} → {tt:g} ngày."],"Năng suất = phần việc mỗi ngày."))
    x,p,y,q=C([(10,20,30,40),(20,10,30,30),(4,25,6,50),(5,30,15,10),(10,15,40,25)]);res=(x*p+y*q)/(x+y)
    L.append(T("Số học",f"{x} litres of a {p}% salt solution are mixed with {y} litres of a {q}% salt solution. What is the salt percentage of the mixture?",f"Trộn {x} lít dung dịch muối {p}% với {y} lít dung dịch muối {q}%. Nồng độ muối của hỗn hợp là bao nhiêu phần trăm?",int(res) if res==int(res) else res,"Tính lượng muối mỗi phần.",[f"({x}·{p} + {y}·{q}) : {x+y} = {res:g}%."],"Nồng độ = lượng chất : tổng lượng."))
    u,v=r.sample(range(-6,10),2);S,P=u+v,u*v
    L.append(T("Đại số",f"The equation x² {'−' if S>=0 else '+'} {abs(S)}x {'+' if P>=0 else '−'} {abs(P)} = 0 has two roots. Find the sum of the squares of the roots.",f"Phương trình x² {'−' if S>=0 else '+'} {abs(S)}x {'+' if P>=0 else '−'} {abs(P)} = 0 có hai nghiệm. Tính tổng bình phương hai nghiệm.",u*u+v*v,"Dùng hệ thức Vi-ét.",[f"x₁ + x₂ = {S}, x₁x₂ = {P}; tổng bình phương {S}² − 2·({P}) = {u*u+v*v}."],"x₁² + x₂² = S² − 2P."))
    if S==0 and P==0: L.pop()
    a=R(-8,12);b=R(1,15);L.append(T("Đại số",f"Find the sum of all solutions of |x − {a}| = {b}." if a>=0 else f"Find the sum of all solutions of |x + {-a}| = {b}.",f"Tìm tổng các nghiệm của phương trình |x − {a}| = {b}." if a>=0 else f"Tìm tổng các nghiệm của phương trình |x + {-a}| = {b}.",2*a,"Hai nghiệm đối xứng qua "+str(a)+".",[f"x = {a+b} hoặc x = {a-b}; tổng {2*a}."],"Giá trị tuyệt đối."))
    b=R(-5,5);lo=R(-10,5);hi=lo+R(15,40);cnt=sum(1 for x in range(-100,100) if lo<3*x+b<hi)
    L.append(T("Đại số",f"How many integers x satisfy {lo} < 3x {'+' if b>=0 else '−'} {abs(b)} < {hi}?",f"Có bao nhiêu số nguyên x thỏa mãn {lo} < 3x {'+' if b>=0 else '−'} {abs(b)} < {hi}?",cnt,"Giải bất phương trình kép.",[f"Có {cnt} số nguyên."],"Chia ba vế cho 3."))
    k=C([7,11,13,17,19,23]);cnt=999//k-99//k;L.append(T("Số học",f"How many three-digit numbers are divisible by {k}?",f"Có bao nhiêu số có ba chữ số chia hết cho {k}?",cnt,"Đếm bội số từ 100 đến 999.",[f"{999//k} − {99//k} = {cnt}."],"Bội số trong khoảng."))
    n=R(60,250);z=n//5+n//25+n//125;L.append(T("Số học",f"How many zeros does {n}! end with?",f"{n}! có bao nhiêu chữ số 0 tận cùng?",z,"Đếm thừa số 5.",[f"{n//5} + {n//25} + {n//125} = {z}."],"Công thức Legendre."))
    k1,k2=C([(2,3),(3,4),(2,5),(3,5),(4,5)]);A1=k1*k1*R(2,6);A2=A1*k2*k2//(k1*k1)
    L.append(T("Hình học",f"Two similar triangles have corresponding sides in the ratio {k1} : {k2}. The smaller has area {A1}. What is the area of the larger?",f"Hai tam giác đồng dạng có tỉ số cạnh {k1} : {k2}. Tam giác nhỏ có diện tích {A1}. Diện tích tam giác lớn?",A2,"Tỉ số diện tích bằng bình phương tỉ số đồng dạng.",[f"{A1} × {k2}² : {k1}² = {A2}."],"Tỉ số diện tích = k²."))
    x1,y1=R(-5,5),R(-5,5);m=R(-4,5);dx=R(1,6);L.append(T("Đại số",f"What is the slope of the line through ({x1}, {y1}) and ({x1+dx}, {y1+m*dx})?",f"Hệ số góc của đường thẳng đi qua ({x1}, {y1}) và ({x1+dx}, {y1+m*dx}) là?",m,"Hiệu tung độ chia hiệu hoành độ.",[f"({m*dx}) : {dx} = {m}."],"k = (y₂ − y₁)/(x₂ − x₁)."))
    p,q,h=C(TRIP);x1,y1=R(-6,6),R(-6,6);L.append(T("Hình học",f"Find the distance between the points ({x1}, {y1}) and ({x1+p}, {y1-q}).",f"Tính khoảng cách giữa hai điểm ({x1}, {y1}) và ({x1+p}, {y1-q}).",h,"Dùng định lí Pythagore.",[f"√({p}² + {q}²) = {h}."],"Khoảng cách hai điểm."))
    a,b=C([(30,60),(40,100),(50,120),(20,80),(100,200)]);L.append(T("Số học",f"How many primes are there between {a} and {b}?",f"Có bao nhiêu số nguyên tố nằm giữa {a} và {b}?",sum(isprime(v) for v in range(a+1,b)),"Loại các số chia hết cho 2, 3, 5, 7, 11, 13.",[", ".join(str(v) for v in range(a+1,b) if isprime(v))+"."],"Kiểm tra đến căn bậc hai."))
    r.shuffle(L);return L

# ---------------- E: lớp 10–12 ----------------
def genE(r):
    R=r.randint;C=r.choice;L=[]
    a,b=R(2,9),R(1,7);L.append(T("Đại số",f"Compute log₂(2^{a} · 4^{b}).",f"Tính log₂(2^{a} · 4^{b}).",a+2*b,"4 = 2².",[f"2^{a} · 2^{2*b} = 2^{a+2*b} → {a+2*b}."],"log_a(a^k) = k."))
    k=R(2,5);L.append(T("Đại số",f"Solve log₃ x = {k}.",f"Giải phương trình log₃ x = {k}.",3**k,"x = 3 mũ "+str(k)+".",[f"x = 3^{k} = {3**k}."],"Định nghĩa lôgarit."))
    a=R(-4,6);b=R(a+1,a+9);L.append(T("Đại số",f"Solve 2^(x + {a}) = 2^{b}." if a>=0 else f"Solve 2^(x − {-a}) = 2^{b}.",f"Giải phương trình 2^(x + {a}) = 2^{b}." if a>=0 else f"Giải phương trình 2^(x − {-a}) = 2^{b}.",b-a,"Cùng cơ số thì so sánh số mũ.",[f"x + {a} = {b} → x = {b-a}."],"Phương trình mũ cùng cơ số."))
    a1=R(1,20);d=R(2,9);n=R(10,40);L.append(T("Đại số",f"Find the sum of the first {n} terms of the arithmetic sequence {a1}, {a1+d}, {a1+2*d}, …",f"Tính tổng {n} số hạng đầu của cấp số cộng {a1}, {a1+d}, {a1+2*d}, …",n*(2*a1+(n-1)*d)//2,"S_n = n(2a₁ + (n − 1)d)/2.",[f"{n} × ({2*a1} + {(n-1)*d}) : 2 = {n*(2*a1+(n-1)*d)//2}."],"Tổng cấp số cộng."))
    a1=R(1,5);q=C([2,3]);n=R(5,9);L.append(T("Đại số",f"Find the sum of the first {n} terms of the geometric sequence {a1}, {a1*q}, {a1*q*q}, …",f"Tính tổng {n} số hạng đầu của cấp số nhân {a1}, {a1*q}, {a1*q*q}, …",a1*(q**n-1)//(q-1),"S_n = a₁(qⁿ − 1)/(q − 1).",[f"{a1} × ({q}^{n} − 1) : {q-1} = {a1*(q**n-1)//(q-1)}."],"Tổng cấp số nhân."))
    a=C([2,3,-2]);b=C([v for v in range(-5,6) if v]);k=R(-3,4);fa=("−2" if a==-2 else str(a));L.append(T("Đại số",f"Let f(x) = {fa}x {'+' if b>=0 else '−'} {abs(b)}. Find f(f({k})).",f"Cho f(x) = {fa}x {'+' if b>=0 else '−'} {abs(b)}. Tính f(f({k})).",a*(a*k+b)+b,"Tính f("+str(k)+") trước.",[f"f({k}) = {a*k+b}; f({a*k+b}) = {a*(a*k+b)+b}."],"Hàm hợp."))
    n=R(5,10);k=R(2,n-2);L.append(T("Tổ hợp",f"What is the coefficient of x^{k} in the expansion of (1 + x)^{n}?",f"Hệ số của x^{k} trong khai triển (1 + x)^{n} là?",math.comb(n,k),"Nhị thức Newton.",[f"C({n}, {k}) = {math.comb(n,k)}."],"(1 + x)ⁿ = Σ C(n, k)xᵏ."))
    n=R(4,7);k=R(1,n-1);L.append(T("Tổ hợp",f"Find the coefficient of x^{k} in (x + 2)^{n}.",f"Tìm hệ số của x^{k} trong khai triển (x + 2)^{n}.",math.comb(n,k)*2**(n-k),"Số hạng tổng quát C(n, k)·x^k·2^(n−k).",[f"C({n}, {k}) × 2^{n-k} = {math.comb(n,k)*2**(n-k)}."],"Nhị thức Newton."))
    n=R(6,12);k=R(2,4);L.append(T("Tổ hợp",f"How many {k}-element subsets does the set {{1, 2, …, {n}}} have?",f"Tập {{1, 2, …, {n}}} có bao nhiêu tập con gồm {k} phần tử?",math.comb(n,k),"Chọn không thứ tự.",[f"C({n}, {k}) = {math.comb(n,k)}."],"Tổ hợp."))
    a,b=R(2,4),C([v for v in range(-5,6) if v]);k=R(-2,3);L.append(T("Giải tích",f"Let f(x) = {a}x³ {'+' if b>=0 else '−'} {abs(b)}x². Find f′({k}).",f"Cho f(x) = {a}x³ {'+' if b>=0 else '−'} {abs(b)}x². Tính f′({k}).",3*a*k*k+2*b*k,"Đạo hàm từng số hạng.",[f"f′(x) = {3*a}x² {'+' if b>=0 else '−'} {abs(2*b)}x → f′({k}) = {3*a*k*k+2*b*k}."],"(xⁿ)′ = n·xⁿ⁻¹."))
    a=C([2,4,6]);b=R(-3,5);k=R(1,6);L.append(T("Giải tích",f"Evaluate the integral of ({a}x {'+' if b>=0 else '−'} {abs(b)}) dx from 0 to {k}.",f"Tính tích phân từ 0 đến {k} của ({a}x {'+' if b>=0 else '−'} {abs(b)}) dx.",a*k*k//2+b*k,"Nguyên hàm rồi thay cận.",[f"[{a//2}x² {'+' if b>=0 else '−'} {abs(b)}x] từ 0 đến {k} = {a*k*k//2+b*k}."],"Tích phân xác định."))
    combos=[("2sin30° + 4cos60°","2sin30° + 4cos60°",3),("4sin²45° + 2","4sin²45° + 2",4),("6tan45° − 2cos0°","6tan45° − 2cos0°",4),("8cos²60° + sin90°","8cos²60° + sin90°",3),("12sin30°·cos60°","12sin30°·cos60°",3),("2tan²60° − 1","2tan²60° − 1",5)]
    e,ev,v=C(combos);L.append(T("Lượng giác",f"Compute {e}.",f"Tính giá trị {ev}.",v,"Dùng giá trị lượng giác của góc đặc biệt.",[f"Kết quả: {v}."],"sin30° = 1/2, cos60° = 1/2, tan45° = 1, tan60° = √3."))
    b=C([3,7,9,11,13]);n=R(20,200);L.append(T("Số học",f"What are the last two digits of {b}^{n}? (answer as a number from 0 to 99)",f"Hai chữ số tận cùng của {b}^{n} tạo thành số nào? (ghi số từ 0 đến 99)",pow(b,n,100),"Tìm số dư khi chia cho 100.",[f"{b}^{n} mod 100 = {pow(b,n,100)}."],"Chu kì đồng dư modulo 100."))
    n=R(5,15);L.append(T("Tổ hợp",f"How many solutions in non-negative integers does x + y + z = {n} have?",f"Phương trình x + y + z = {n} có bao nhiêu nghiệm nguyên không âm?",math.comb(n+2,2),"Phương pháp chia kẹo Euler.",[f"C({n+2}, 2) = {math.comb(n+2,2)}."],"Số nghiệm = C(n + 2, 2)."))
    while True:
        x0,y0=R(-5,5),R(-5,5);c=R(-30,30);v=3*x0+4*y0+c
        if v%5==0 and v!=0: break
    L.append(T("Hình học",f"Find the distance from the point ({x0}, {y0}) to the line 3x + 4y {'+' if c>=0 else '−'} {abs(c)} = 0.",f"Tính khoảng cách từ điểm ({x0}, {y0}) đến đường thẳng 3x + 4y {'+' if c>=0 else '−'} {abs(c)} = 0.",abs(v)//5,"Công thức khoảng cách.",[f"|{v}| : 5 = {abs(v)//5}."],"d = |ax₀ + by₀ + c| / √(a² + b²)."))
    h,k,rr=R(-6,6),R(-6,6),R(2,9);D,E,F=-2*h,-2*k,h*h+k*k-rr*rr
    sgn=lambda v,s:(f" + {v}{s}" if v>0 else (f" − {-v}{s}" if v<0 else ""))
    L.append(T("Hình học",f"Find the radius of the circle x² + y²{sgn(D,'x')}{sgn(E,'y')}{sgn(F,'')} = 0.",f"Tìm bán kính đường tròn x² + y²{sgn(D,'x')}{sgn(E,'y')}{sgn(F,'')} = 0.",rr,"Đưa về dạng (x − a)² + (y − b)² = R².",[f"Tâm ({h}, {k}), R = {rr}."],"R² = a² + b² − c."))
    u=(R(-6,6),R(-6,6));v=(R(-6,6),R(-6,6));L.append(T("Hình học",f"Compute the dot product of u = ({u[0]}, {u[1]}) and v = ({v[0]}, {v[1]}).",f"Tính tích vô hướng của u = ({u[0]}, {u[1]}) và v = ({v[0]}, {v[1]}).",u[0]*v[0]+u[1]*v[1],"Nhân tọa độ tương ứng rồi cộng.",[f"{u[0]}·{v[0]} + {u[1]}·{v[1]} = {u[0]*v[0]+u[1]*v[1]}."],"u·v = x₁x₂ + y₁y₂."))
    a,b,c,d=[R(-6,9) for _ in range(4)];L.append(T("Đại số",f"Compute the determinant of the 2×2 matrix with rows ({a}, {b}) and ({c}, {d}).",f"Tính định thức ma trận 2×2 có hai hàng ({a}, {b}) và ({c}, {d}).",a*d-b*c,"ad − bc.",[f"{a}·{d} − {b}·{c} = {a*d-b*c}."],"Định thức cấp 2."))
    a1=R(1,4);k=R(5,8);seq=[a1]
    for _ in range(k-1): seq.append(2*seq[-1]+1)
    L.append(T("Đại số",f"A sequence has a₁ = {a1} and aₙ₊₁ = 2aₙ + 1. Find a_{k}.",f"Dãy số có a₁ = {a1} và aₙ₊₁ = 2aₙ + 1. Tính a_{k}.",seq[-1],"Tính lần lượt.",[", ".join(map(str,seq))+"."],"Dãy truy hồi."))
    b=2*R(1,8);c=R(-10,20);L.append(T("Giải tích",f"Find the maximum value of f(x) = −x² + {b}x {'+' if c>=0 else '−'} {abs(c)}.",f"Tìm giá trị lớn nhất của f(x) = −x² + {b}x {'+' if c>=0 else '−'} {abs(c)}.",b*b//4+c,"Đỉnh parabol tại x = "+str(b//2)+".",[f"f({b//2}) = {b*b//4+c}."],"Đỉnh x = −b/(2a)."))
    n=R(5,8);L.append(T("Tổ hợp",f"In how many ways can {n} people stand in a row if two particular people must stand next to each other?",f"Có bao nhiêu cách xếp {n} người thành một hàng sao cho hai người cho trước luôn đứng cạnh nhau?",2*math.factorial(n-1),"Coi hai người là một khối.",[f"2 × {n-1}! = {2*math.factorial(n-1)}."],"Gộp khối rồi hoán vị trong khối."))
    k=R(2,7);L.append(T("Hình học",f"A triangle has sides {3*k}, {4*k} and {5*k}. What is its area?",f"Tam giác có ba cạnh {3*k}, {4*k}, {5*k}. Diện tích tam giác bằng?",6*k*k,"Đây là tam giác vuông.",[f"{3*k} × {4*k} : 2 = {6*k*k}."],"Bộ ba Pythagore."))
    rr=3*R(1,4);L.append(T("Hình học",f"A sphere has radius {rr}. Its volume is kπ. Find k.",f"Hình cầu bán kính {rr} có thể tích kπ. Tìm k.",4*rr**3//3,"V = (4/3)πr³.",[f"k = 4 × {rr}³ : 3 = {4*rr**3//3}."],"Thể tích hình cầu."))
    a,b,c=R(1,5),R(1,4),R(1,3);L.append(T("Số học",f"How many positive divisors does 2^{a} · 3^{b} · 5^{c} have?",f"Số 2^{a} · 3^{b} · 5^{c} có bao nhiêu ước nguyên dương?",(a+1)*(b+1)*(c+1),"Nhân (số mũ + 1).",[f"({a}+1)({b}+1)({c}+1) = {(a+1)*(b+1)*(c+1)}."],"Đếm ước qua thừa số nguyên tố."))
    g=R(10,60);x,y=C([(7,11),(9,13),(12,17),(15,22),(8,21)]);L.append(T("Số học",f"Find gcd({g*x}, {g*y}).",f"Tìm ƯCLN({g*x}, {g*y}).",g*math.gcd(x,y),"Thuật toán Euclid.",[f"ƯCLN = {g*math.gcd(x,y)}."],"gcd(a, b) = gcd(b, a mod b)."))
    lo=R(10,50);hi=lo+R(100,300);d=C([6,7,9,11]);cnt=hi//d-(lo-1)//d
    L.append(T("Số học",f"How many multiples of {d} lie between {lo} and {hi}, inclusive?",f"Có bao nhiêu bội của {d} nằm trong đoạn [{lo}; {hi}]?",cnt,"Đếm bội số.",[f"{hi//d} − {(lo-1)//d} = {cnt}."],"⌊b/d⌋ − ⌊(a − 1)/d⌋."))
    p,q=C([(1,2),(1,3),(2,3),(1,4),(3,4)]);n=R(3,5);k=R(1,n);num=math.comb(n,k)*p**k*(q-p)**(n-k);den=q**n
    fr=Fr(num,den);L.append(T("Xác suất",f"A coin lands heads with probability {p}/{q}. It is tossed {n} times. The probability of exactly {k} heads is a/b in lowest terms. Find a + b.",f"Một đồng xu ra mặt ngửa với xác suất {p}/{q}. Tung {n} lần. Xác suất có đúng {k} lần ngửa là a/b tối giản. Tính a + b.",fr.numerator+fr.denominator,"Công thức Bernoulli.",[f"C({n}, {k})·({p}/{q})^{k}·({q-p}/{q})^{n-k} = {fr} → {fr.numerator+fr.denominator}."],"P = C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ."))
    a=R(2,6);b=R(1,9);L.append(T("Giải tích",f"Find the limit as x → ∞ of ({a}x² + {b}x) / (x² + 1).",f"Tính giới hạn khi x → ∞ của ({a}x² + {b}x) / (x² + 1).",a,"Chia tử và mẫu cho x².",[f"Giới hạn bằng {a}."],"Bậc tử bằng bậc mẫu: lấy tỉ số hệ số cao nhất."))
    r.shuffle(L);return L

BANDS={"A":(genA,"lớp 1–2",[1,2]),"B":(genB,"lớp 3–4",[3,4]),"C":(genC,"lớp 5–6",[5,6]),"D":(genD,"lớp 7–9",[7,8,9]),"E":(genE,"lớp 10–12",[10,11,12])}

def mcs(r,q,n):
    """Trắc nghiệm cho cả đáp án âm."""
    a=q["a"];fmt=lambda v:(str(int(v)) if float(v)==int(v) else str(round(v,2))).replace(".",",").replace("-","−")
    sa=fmt(a);opts=[sa];val=float(a)
    for d in r.sample([1,-1,2,-2,3,-3,4,5,-5,10,-10,6],12):
        if len(opts)>=n: break
        v=val+d
        if val>=0 and v<0: continue
        s=fmt(v)
        if s not in opts: opts.append(s)
    r.shuffle(opts);o=dict(q);o["o"]=opts;o["a"]=opts.index(sa);return o
