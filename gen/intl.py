import random, math
from fractions import Fraction as Fr
def T(t,q,vi,a,h,s,m): return {"t":t,"q":q,"vi":vi,"a":a,"h":h,"s":s,"m":m}
def isprime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def coins(N): return sum(1 for b in range(N//2+1) for c in range(N//5+1) if 2*b+5*c<=N)
DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];VD=["thứ Hai","thứ Ba","thứ Tư","thứ Năm","thứ Sáu","thứ Bảy","Chủ nhật"]
def gens(r):
    R=r.randint;C=r.choice;L=[]
    n=R(20,60);L.append(T("Số học",f"Find 1 + 2 + 3 + … + {n}.",f"Tính 1 + 2 + 3 + … + {n}.",n*(n+1)//2,"Ghép cặp đầu – cuối.",[f"{n} × {n+1} : 2 = {n*(n+1)//2}."],"Tổng n số tự nhiên đầu tiên = n(n + 1)/2."))
    k=R(4,6);av=R(10,20);nav=av+R(1,3)
    L.append(T("Số học",f"The average of {k} numbers is {av}. After one more number is added, the average becomes {nav}. What number was added?",f"Trung bình cộng {k} số là {av}. Thêm một số thì trung bình là {nav}. Số thêm vào là?",nav*(k+1)-av*k,"So sánh hai tổng.",[f"{nav} × {k+1} − {av} × {k} = {nav*(k+1)-av*k}."],"Tổng = trung bình × số lượng."))
    m=C([3,4,5]);s=R(6,12);y=s*(m-1)//1;yy=R(4,12);  # father m times son; in yy years father is (m-? )
    son=R(6,12);f=m*son;yrs=C([y2 for y2 in range(2,40) if (f+y2)%(son+y2)==0 and (f+y2)//(son+y2)<m][:3] or [son*(m-2)//1])
    L.append(T("Số học",f"A father is {m} times as old as his son. In {yrs} years, he will be {(f+yrs)//(son+yrs)} times as old as his son. How old is the son now?",f"Bố gấp {m} lần tuổi con. {yrs} năm nữa bố gấp {(f+yrs)//(son+yrs)} lần tuổi con. Con hiện nay bao nhiêu tuổi?",son,"Hiệu số tuổi không đổi.",[f"Thử: con {son}, bố {f}; {yrs} năm nữa: {son+yrs} và {f+yrs}."],"Lập phương trình theo tuổi con."))
    h=R(15,30);rb=R(3,h-3);legs=2*h+2*rb
    L.append(T("Logic",f"There are chickens and rabbits on a farm: {h} heads and {legs} legs. How many rabbits are there?",f"Có gà và thỏ: {h} đầu, {legs} chân. Có bao nhiêu thỏ?",rb,"Giả sử tất cả là gà.",[f"{h} gà có {2*h} chân; thừa {legs-2*h} chân; mỗi thỏ thêm 2 chân → {rb} thỏ."],"Phương pháp giả thiết tạm."))
    a,b=C([(4,6),(5,7),(6,8),(3,7)]);ra=a-1;rb2=b-1;lc=a*b//math.gcd(a,b)
    L.append(T("Số học",f"What is the smallest positive number that leaves remainder {ra} when divided by {a} and remainder {rb2} when divided by {b}?",f"Số nguyên dương nhỏ nhất chia {a} dư {ra}, chia {b} dư {rb2} là?",lc-1,"Thêm 1 thì chia hết cho cả hai.",[f"BCNN({a}, {b}) = {lc}; số cần tìm {lc} − 1 = {lc-1}."],"Thiếu 1 thì cộng 1."))
    p,q=C([(12,18),(10,15),(8,12),(9,12)]);lc=p*q//math.gcd(p,q)
    L.append(T("Số học",f"Bus A leaves every {p} minutes and bus B every {q} minutes. Both leave at 7:00. After how many minutes do they next leave together?",f"Xe A cứ {p} phút một chuyến, xe B cứ {q} phút. Cùng xuất bến lúc 7:00. Sau bao nhiêu phút lại cùng xuất bến?",lc,"Tìm BCNN.",[f"BCNN({p}, {q}) = {lc}."],"Bài “lại gặp nhau” là BCNN."))
    w=R(3,9);k=C([2,3]);P=2*(w+k*w)
    L.append(T("Hình học",f"A rectangle's length is {k} times its width, and its perimeter is {P} cm. What is its area in cm²?",f"Chiều dài gấp {k} lần chiều rộng, chu vi {P} cm. Diện tích (cm²)?",w*k*w,"Nửa chu vi = "+str(k+1)+" phần.",[f"Rộng {w}, dài {k*w}; diện tích {k*w*w}."],"Chia nửa chu vi theo phần."))
    s=R(10,20);d=C([1,2,3])
    L.append(T("Hình học",f"A square garden of side {s} m has a path {d} m wide all around the outside. What is the area of the path in m²?",f"Vườn vuông cạnh {s} m có lối đi rộng {d} m bao quanh phía ngoài. Diện tích lối đi (m²)?",(s+2*d)**2-s*s,"Lấy hình vuông lớn trừ hình nhỏ.",[f"({s+2*d})² − {s}² = {(s+2*d)**2-s*s}."],"Cạnh lớn tăng 2 lần độ rộng lối đi."))
    n=R(7,15);L.append(T("Tổ hợp",f"{n} people each shake hands with every other person once. How many handshakes are there?",f"{n} người, mỗi hai người bắt tay một lần. Có bao nhiêu cái bắt tay?",n*(n-1)//2,"Mỗi người bắt tay "+str(n-1)+" người.",[f"{n} × {n-1} : 2 = {n*(n-1)//2}."],"Chia 2 vì đếm trùng."))
    n=R(5,9);L.append(T("Tổ hợp",f"A strip has {n} squares in a row. How many rectangles (including squares) are in the strip?",f"Dải {n} ô vuông thẳng hàng có bao nhiêu hình chữ nhật (kể cả hình vuông)?",n*(n+1)//2,"Đếm theo độ dài.",[f"{n} + {n-1} + … + 1 = {n*(n+1)//2}."],"n(n + 1)/2."))
    N=R(110,250);dg=9+180+3*(N-99)
    L.append(T("Số học",f"How many digits are used to number the pages of a book from 1 to {N}?",f"Đánh số trang sách từ 1 đến {N} cần bao nhiêu chữ số?",dg,"Chia theo số có 1, 2, 3 chữ số.",[f"9 + 180 + 3 × {N-99} = {dg}."],"Trang 1–9: 1 chữ số; 10–99: 2 chữ số."))
    b=C([2,3,7,8]);e=R(20,99);cyc={2:[2,4,8,6],3:[3,9,7,1],7:[7,9,3,1],8:[8,4,2,6]}[b]
    L.append(T("Số học",f"What is the units digit of {b}^{e}?",f"Chữ số hàng đơn vị của {b}^{e} là?",cyc[(e-1)%4],"Chu kì chữ số tận cùng dài 4.",[f"Chu kì {', '.join(map(str,cyc))}; {e} chia 4 dư {e%4}."],"Tìm chu kì rồi lấy số dư."))
    n=R(20,60);z=n//5+n//25
    L.append(T("Số học",f"How many zeros are at the end of 1 × 2 × 3 × … × {n}?",f"Tích 1 × 2 × … × {n} có bao nhiêu chữ số 0 tận cùng?",z,"Đếm thừa số 5.",[f"{n//5} bội của 5, {n//25} bội của 25 → {z}."],"Thừa số 5 ít hơn thừa số 2."))
    n=C([36,48,60,72,84,90,96,100]);dv=sum(1 for d in range(1,n+1) if n%d==0)
    L.append(T("Số học",f"How many positive divisors does {n} have?",f"{n} có bao nhiêu ước nguyên dương?",dv,"Phân tích thừa số nguyên tố.",[f"{n} có {dv} ước."],"Số ước = tích (số mũ + 1)."))
    pr=C([80,120,160,200,240]);d1=C([10,20,25])
    L.append(T("Số học",f"A toy costs ${pr}. Its price is reduced by {d1}%, and then the new price is reduced by 10%. What is the final price in dollars?",f"Món đồ giá {pr} đô, giảm {d1}% rồi giảm tiếp 10% giá mới. Giá cuối (đô)?",round(pr*(100-d1)*90/10000,2),"Nhân liên tiếp.",[f"{pr} × {(100-d1)/100} × 0,9 = {round(pr*(100-d1)*90/10000,2)}."],"Hai lần giảm không cộng phần trăm."))
    v1,v2=C([(40,50),(45,55),(60,40),(35,45)]);t=C([2,3]);D=(v1+v2)*t
    L.append(T("Số học",f"Two cars start {D} km apart and drive towards each other at {v1} km/h and {v2} km/h. After how many hours do they meet?",f"Hai ô tô cách nhau {D} km, đi ngược chiều với {v1} và {v2} km/giờ. Sau mấy giờ gặp nhau?",t,"Cộng vận tốc.",[f"{D} : ({v1} + {v2}) = {t}."],"Ngược chiều: tổng vận tốc."))
    t1,t2=C([(3,6),(4,12),(6,12),(10,15)]);tt=Fr(t1*t2,t1+t2)
    L.append(T("Số học",f"Pipe A fills a tank in {t1} hours and pipe B in {t2} hours. How many hours do both pipes together take?",f"Vòi A chảy đầy bể trong {t1} giờ, vòi B trong {t2} giờ. Cả hai cùng chảy mất mấy giờ?",tt.numerator if tt.denominator==1 else float(tt),"Cộng năng suất.",[f"1/{t1} + 1/{t2}; thời gian {tt}."],"Năng suất = phần bể mỗi giờ."))
    n=R(3,7);L.append(T("Hình học",f"How many squares of all sizes are there in a {n} × {n} grid?",f"Lưới {n} × {n} có tất cả bao nhiêu hình vuông?",sum(i*i for i in range(1,n+1)),"Đếm theo kích thước.",[" + ".join(str(i*i) for i in range(n,0,-1))+f" = {sum(i*i for i in range(1,n+1))}."],"Tổng các số chính phương."))
    n=C([5,6,8,10,12]);L.append(T("Hình học",f"What is the sum of the interior angles of a polygon with {n} sides, in degrees?",f"Tổng các góc trong của đa giác {n} cạnh (độ)?",(n-2)*180,"(n − 2) × 180°.",[f"({n} − 2) × 180 = {(n-2)*180}."],"Chia đa giác thành tam giác."))
    hh=R(1,11);mm=C([0,30])
    ang=abs(30*hh+mm/2-6*mm);ang=min(ang,360-ang)
    L.append(T("Hình học",f"What is the smaller angle between the hands of a clock at {hh}:{mm:02d}, in degrees?",f"Góc nhỏ giữa hai kim lúc {hh} giờ {mm} phút là bao nhiêu độ?",int(ang) if ang==int(ang) else ang,"Kim giờ quay 0,5° mỗi phút.",[f"Kim giờ {30*hh+mm/2}°, kim phút {6*mm}° → {ang}°."],"Tính vị trí từng kim từ số 12."))
    a0=R(1,5);d0=R(2,4);dd=R(1,3);seq=[a0];
    for i in range(5): seq.append(seq[-1]+d0+i*dd)
    L.append(T("Logic",f"Find the next number: {', '.join(map(str,seq[:5]))}, …",f"Tìm số tiếp theo: {', '.join(map(str,seq[:5]))}, …",seq[5],"Xét hiệu hai số liền nhau.",[f"Hiệu tăng đều {dd} → số tiếp theo {seq[5]}."],"Dãy có hiệu cách đều."))
    st=R(0,6);N=R(40,200)
    L.append(T("Logic",f"Today is {DAYS[st]}. Counting today as day 0, which day of the week is it {N} days later? (answer 1 = Monday, …, 7 = Sunday)",f"Hôm nay {VD[st]}. Sau {N} ngày là thứ mấy? (ghi 1 = thứ Hai, …, 7 = Chủ nhật)",(st+N)%7+1,"Lấy số dư khi chia cho 7.",[f"{N} chia 7 dư {N%7} → {VD[(st+N)%7]}."],"Một tuần có 7 ngày."))
    k=C([3,4,5]);L.append(T("Logic",f"A drawer has socks of {k} different colours. In the dark, how many socks must you take to be sure of getting 2 of the same colour?",f"Ngăn kéo có tất của {k} màu. Trong bóng tối phải lấy ít nhất bao nhiêu chiếc để chắc chắn có 2 chiếc cùng màu?",k+1,"Trường hợp xấu nhất.",[f"{k} chiếc có thể khác màu; chiếc thứ {k+1} chắc chắn trùng."],"Nguyên lí Dirichlet."))
    N=C([8,10,12,15]);L.append(T("Tổ hợp",f"In how many ways can you make {N} cents using 1-cent, 2-cent and 5-cent coins?",f"Có bao nhiêu cách đổi {N} xu bằng đồng 1, 2, 5 xu?",coins(N),"Chia theo số đồng 5 xu.",[f"Đếm lần lượt: {coins(N)} cách."],"Xét đồng giá trị lớn trước."))
    n=R(5,10);fib=[1,1]
    for i in range(n): fib.append(fib[-1]+fib[-2])
    L.append(T("Tổ hợp",f"You climb stairs 1 or 2 steps at a time. In how many ways can you climb {n} steps?",f"Mỗi bước lên 1 hoặc 2 bậc. Có bao nhiêu cách lên {n} bậc?",fib[n],"Cách(n) = cách(n − 1) + cách(n − 2).",[f"1, 2, 3, 5, 8, … → {fib[n]}."],"Dãy Fibonacci."))
    n=R(3,6);L.append(T("Hình học",f"A {n} × {n} × {n} cube is painted on all faces and cut into unit cubes. How many unit cubes have no painted face?",f"Khối {n}×{n}×{n} sơn mọi mặt rồi cắt thành khối đơn vị. Bao nhiêu khối không có mặt nào được sơn?",(n-2)**3,"Phần lõi bên trong.",[f"({n} − 2)³ = {(n-2)**3}."],"Bỏ lớp ngoài cùng."))
    a,b=C([(2,3),(3,5),(4,7),(2,5)]);add=C([4,6,8,10]);k=add//(b-a) if add%(b-a)==0 else None
    if k is None: add=(b-a)*2;k=2
    L.append(T("Số học",f"The ratio of red to blue marbles is {a} : {b}. After {add} red marbles are added, the ratio becomes 1 : 1. How many blue marbles are there?",f"Bi đỏ : xanh = {a} : {b}. Thêm {add} bi đỏ thì tỉ số 1 : 1. Có bao nhiêu bi xanh?",b*k,"Số bi xanh không đổi.",[f"{b} − {a} = {b-a} phần = {add} → 1 phần = {k}; xanh {b*k}."],"Neo theo đại lượng không đổi."))
    f1,f2=C([(Fr(1,4),Fr(3,4)),(Fr(2,5),Fr(7,10)),(Fr(1,3),Fr(5,6))]);V=C([12,18,24,30])
    cap=Fr(V)/(f2-f1)
    L.append(T("Số học",f"A tank is {f1} full. After {V} litres are added it is {f2} full. What is the capacity in litres?",f"Bể đang đầy {f1}. Thêm {V} lít thì đầy {f2}. Bể chứa bao nhiêu lít?",int(cap) if cap.denominator==1 else float(cap),"Lượng thêm ứng với hiệu hai phân số.",[f"{V} : ({f2} − {f1}) = {cap}."],"Tìm phân số ứng với lượng đã biết."))
    x1,y1=R(0,2),R(0,2);w=R(4,10);h2=R(3,9);x3=x1+R(0,w)
    L.append(T("Hình học",f"Find the area of the triangle with vertices ({x1}, {y1}), ({x1+w}, {y1}) and ({x3}, {y1+h2}).",f"Tính diện tích tam giác có ba đỉnh ({x1}, {y1}), ({x1+w}, {y1}) và ({x3}, {y1+h2}).",Fr(w*h2,2) if (w*h2)%2 else w*h2//2,"Đáy nằm ngang.",[f"Đáy {w}, cao {h2}: {w} × {h2} : 2."],"Đáy song song trục hoành."))
    L[-1]["a"]=w*h2/2 if (w*h2)%2 else w*h2//2
    k=R(6,12);m=C([2026,1234,4321,999]);v=10**k-m
    L.append(T("Số học",f"Find the sum of the digits of 10^{k} − {m}.",f"Tổng các chữ số của 10^{k} − {m} là?",sum(map(int,str(v))),"Viết phép trừ ra.",[f"10^{k} − {m} = {v}."],"Phía trước toàn chữ số 9."))
    a,b=R(2,5),R(2,5);L.append(T("Tổ hợp",f"Moving only right or up, how many shortest paths are there across a {a} × {b} grid from one corner to the opposite corner?",f"Chỉ đi phải hoặc lên, có bao nhiêu đường ngắn nhất qua lưới {a} × {b} từ góc này sang góc đối?",math.comb(a+b,a),"Chọn vị trí các bước đi lên.",[f"C({a+b}, {a}) = {math.comb(a+b,a)}."],"Đường đi trên lưới = tổ hợp."))
    a,b=C([(10,40),(20,60),(30,70),(50,100)]);L.append(T("Số học",f"How many prime numbers are there between {a} and {b}?",f"Có bao nhiêu số nguyên tố nằm giữa {a} và {b}?",sum(isprime(x) for x in range(a+1,b)),"Liệt kê, loại số chia hết cho 2, 3, 5, 7.",[", ".join(str(x) for x in range(a+1,b) if isprime(x))+"."],"Kiểm tra đến căn bậc hai."))
    a,b=C([(10,100),(50,300),(100,500),(20,200)]);L.append(T("Số học",f"How many perfect squares are there between {a} and {b}?",f"Có bao nhiêu số chính phương nằm giữa {a} và {b}?",sum(1 for x in range(1,30) if a<x*x<b),"Tìm căn của hai đầu.",[", ".join(str(x*x) for x in range(1,30) if a<x*x<b)+"."],"Đếm số nguyên có bình phương trong khoảng."))
    S=C([3*x for x in range(20,60)]);L.append(T("Số học",f"The sum of three consecutive whole numbers is {S}. What is the largest of them?",f"Tổng ba số tự nhiên liên tiếp là {S}. Số lớn nhất là?",S//3+1,"Số giữa bằng trung bình.",[f"Số giữa {S//3}; lớn nhất {S//3+1}."],"Số giữa = tổng : 3."))
    r.shuffle(L);return L
def mc(r,q,n):
    import re
    a=q["a"];sa=str(a).replace(".",",")
    opts=[sa];val=float(a)
    for d in r.sample([1,-1,2,-2,3,5,10,4,-3],9):
        if len(opts)>=n: break
        v=val+d
        if v<0: continue
        s=(str(int(v)) if v==int(v) else str(round(v,2))).replace(".",",")
        if s not in opts: opts.append(s)
    r.shuffle(opts);o=dict(q);o["o"]=opts;o["a"]=opts.index(sa);return o
def build(seed,nmc,nopen,mcopts):
    r=random.Random(seed);L=gens(r)+gens(random.Random(seed+999))
    seen=set();U=[]
    for q in L:
        key=q["vi"][:18]
        if key in seen: continue
        seen.add(key);U.append(q)
    out=[mc(r,q,mcopts) for q in U[:nmc]]
    for q in U[nmc:nmc+nopen]:
        q=dict(q);a=q["a"];q["a"]=str(int(a) if float(a)==int(float(a)) else a);q["f"]=True;out.append(q)
    return out
