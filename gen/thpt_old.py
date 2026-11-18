from common import *
SUP=str.maketrans("0123456789−","⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
SUB=str.maketrans("0123456789","₀₁₂₃₄₅₆₇₈₉")
def sp(n): return str(n).translate(SUP)
def SUPm(n): return "" if n==1 else sp(n)
def sb(n): return str(n).translate(SUB)
def paper(seed):
    g=G(seed); Q=[]; A=Q.append
    # 1 counting
    n=g.i(5,45);k=g.c([2,3,4]);vv=g.i(0,2)
    if vv==0: A(g.MC("Tổ hợp","Hoán vị – chỉnh hợp",f"Có bao nhiêu cách chọn {k} học sinh từ {n} học sinh và xếp thành một hàng dọc?",str(math.perm(n,k)),[str(math.comb(n,k)),str(n**k),str(math.perm(n,k-1))],"Chọn có thứ tự: chỉnh hợp.",[f"A({n}, {k}) = {math.perm(n,k)}."],"Có thứ tự → chỉnh hợp; không thứ tự → tổ hợp."))
    elif vv==1: A(g.MC("Tổ hợp","Hoán vị – chỉnh hợp",f"Một câu lạc bộ có {n} thành viên. Có bao nhiêu cách bầu ra {k} người giữ {k} chức vụ khác nhau?",str(math.perm(n,k)),[str(math.comb(n,k)),str(n**k),str(math.perm(n,k-1))],"Mỗi chức vụ khác nhau nên có thứ tự.",[f"A({n}, {k}) = {math.perm(n,k)}."],"Chức vụ khác nhau → chỉnh hợp."))
    else: A(g.MC("Tổ hợp","Tổ hợp",f"Có bao nhiêu cách chọn ra {k} học sinh từ một nhóm {n} học sinh để đi trực nhật (không phân biệt thứ tự)?",str(math.comb(n,k)),[str(math.perm(n,k)),str(n*k),str(math.comb(n,k-1)) if math.comb(n,k-1)!=math.comb(n,k) else str(math.comb(n,k)+1)],"Không thứ tự: tổ hợp.",[f"C({n}, {k}) = {math.comb(n,k)}."],"Không thứ tự → tổ hợp."))
    # 2 CSC
    u1=g.i(-25,25);d=g.c([x for x in range(-9,10) if x]);N=g.i(5,15)
    A(g.MC("Đại số","Cấp số cộng",f"Cấp số cộng (uₙ) có u₁ = {vn(u1)}, công sai d = {vn(d)}. Giá trị u{sb(N)} bằng",vn(u1+(N-1)*d),[vn(u1+N*d),vn(u1*d**(N-1)),vn(u1+(N-2)*d)],"uₙ = u₁ + (n − 1)d.",[f"u{sb(N)} = {vn(u1)} + {N-1} × ({vn(d)}) = {vn(u1+(N-1)*d)}."],"Hệ số của d là n − 1."))
    # 3 đồng biến
    a=g.i(1,9);cc=g.i(-30,30)
    A(g.MC("Đại số","Tính đơn điệu",f"Hàm số y = x³ − {3*a}x²{sg(cc) if cc else ''} nghịch biến trên khoảng nào?",f"(0; {2*a})",[f"(−∞; 0)",f"({2*a}; +∞)",f"(−{2*a}; 0)"],"Xét dấu y′.",[f"y′ = 3x² − {6*a}x = 3x(x − {2*a}) < 0 khi 0 < x < {2*a}."],"Nghịch biến khi y′ < 0."))
    # 4 cực đại
    b=g.i(1,12);cc=g.i(-40,40)
    A(g.MC("Đại số","Cực trị",f"Điểm cực đại của hàm số y = x³ − {3*b*b}x{sg(cc) if cc else ''} là",f"x = −{b}",[f"x = {b}",f"x = {3*b*b}",f"x = 0"],"Giải y′ = 0 và xét dấu.",[f"y′ = 3x² − {3*b*b} = 0 ⇔ x = ±{b}.","Hệ số x³ dương nên cực đại ở nghiệm nhỏ: x = −"+str(b)+"."],"a > 0: cực đại tại nghiệm nhỏ hơn."))
    # 5 tiệm cận đứng
    c=g.i(1,15);e=g.i(2,9);f0=g.i(1,9)
    A(g.MC("Đại số","Tiệm cận",f"Tiệm cận đứng của đồ thị hàm số y = ({e}x + {f0})/(x − {c}) là",f"x = {c}",[f"y = {e}",f"x = −{c}",f"y = {c}"],"Nghiệm của mẫu.",[f"x − {c} = 0 ⇔ x = {c} (tử khác 0)."],"Tiệm cận đứng có dạng x = …"))
    # 6 giao điểm trục hoành
    kk=g.c([1,2,3]);M=2*kk**3;m=g.i(-M-5,M+5)
    nr=3 if -M<m<M else (2 if abs(m)==M else 1)
    A(g.MC("Đại số","Tương giao",f"Số giao điểm của đồ thị y = x³ − {3*kk*kk}x{sg(m) if m else ''} với trục hoành là",str(nr),[str(x) for x in (0,1,2,3) if x!=nr],"So sánh giá trị cực đại và cực tiểu với 0.",[f"yCĐ = y(−{kk}) = {vn(M+m)}, yCT = y({kk}) = {vn(m-M)}.",f"Số giao điểm: {nr}."],"yCĐ · yCT < 0 ⇒ 3 giao điểm."))
    # 7 log rule
    bb=g.c([2,3,5,6,7,10]);k=g.i(1,6);mm_=g.i(1,9)
    A(g.MC("Đại số","Lôgarit",f"Với a > 0, log_{bb}({bb**k}a{sp(mm_) if mm_>1 else ''}) bằng",f"{k} + {mm_ if mm_>1 else ''}log_{bb}a",[f"{k}{mm_ if mm_>1 else ''}log_{bb}a",f"{bb**k} + {mm_ if mm_>1 else ''}log_{bb}a",f"{k} − {mm_ if mm_>1 else ''}log_{bb}a"],"log(xy) = log x + log y; log(aᵐ) = m·log a.",[f"log_{bb}{bb**k} = {k}."],"Log của tích bằng tổng các log."))
    # 8 đạo hàm log
    bb=g.i(2,12);cc=g.i(0,40)
    xx=f"(x + {cc})" if cc else "x"
    A(g.MC("Đại số","Đạo hàm",f"Đạo hàm của hàm số y = log_{bb}{xx} là",f"1/({xx} ln {bb})",[f"ln {bb}/{xx}",f"1/{xx}",f"{xx} ln {bb}"],"(logₐu)′ = u′/(u ln a).",[f"y′ = 1/({xx} ln {bb})."],"Nhớ có ln a ở mẫu."))
    # 9 PT mũ
    bb=g.c([2,3,5]);p=g.i(1,5);q2=g.i(1,40)
    A(g.MC("Đại số","Phương trình mũ",f"Nghiệm của phương trình {bb}^(x − {q2}) = {bb**p} là",f"x = {p+q2}",[f"x = {p}",f"x = {p-q2}",f"x = {bb**p+q2}"],f"Đưa về cùng cơ số {bb}.",[f"x − {q2} = {p} ⇒ x = {p+q2}."],"Cùng cơ số thì bằng số mũ."))
    # 10 PT log
    bb=g.c([2,3,5]);r=g.i(1,4);s_=g.i(1,60)
    A(g.MC("Đại số","Phương trình lôgarit",f"Nghiệm của phương trình log_{bb}(x − {s_}) = {r} là",f"x = {bb**r+s_}",[f"x = {bb**r-s_}",f"x = {bb*r+s_}",f"x = {bb**r}"],f"x − {s_} = {bb}^{r}.",[f"x − {s_} = {bb**r} ⇒ x = {bb**r+s_}."],"Kiểm tra điều kiện x > "+str(s_)+"."))
    # 11 nguyên hàm
    k=g.i(3,12);cc=g.i(1,20);cs=f"{cc}" if cc>1 else ""
    if g.i(0,1): A(g.MC("Đại số","Nguyên hàm",f"Họ nguyên hàm của f(x) = {k}x{sp(k-1)} + {cs}sin x là",f"x{sp(k)} − {cs}cos x + C",[f"x{sp(k)} + {cs}cos x + C",f"{k}x{sp(k)} − {cs}cos x + C",f"{k*(k-1)}x{sp(k-2)} + {cs}cos x + C"],"Nguyên hàm từng hạng tử.",[f"∫{k}x{sp(k-1)}dx = x{sp(k)}; ∫{cs}sin x dx = −{cs}cos x."],"Nguyên hàm của sin x là −cos x."))
    else: A(g.MC("Đại số","Nguyên hàm",f"Họ nguyên hàm của f(x) = {k}x{sp(k-1)} + {cs}cos x là",f"x{sp(k)} + {cs}sin x + C",[f"x{sp(k)} − {cs}sin x + C",f"{k}x{sp(k)} + {cs}sin x + C",f"{k*(k-1)}x{sp(k-2)} − {cs}sin x + C"],"Nguyên hàm từng hạng tử.",[f"∫{k}x{sp(k-1)}dx = x{sp(k)}; ∫{cs}cos x dx = {cs}sin x."],"Kiểm tra bằng đạo hàm."))
    # 12 tích phân tính chất
    a1=g.i(1,15);b1=g.i(1,15);ka=g.i(2,4)
    A(g.MC("Đại số","Tích phân",f"Biết ∫₀¹ f(x)dx = {a1} và ∫₀¹ g(x)dx = {b1}. Khi đó ∫₀¹ [{ka}f(x) − g(x)]dx bằng",vn(ka*a1-b1),[vn(a1-b1),vn(ka*a1+b1),vn(ka*(a1-b1))],"Tích phân tuyến tính.",[f"{ka} × {a1} − {b1} = {ka*a1-b1}."],"Tách tổng, đưa hằng số ra ngoài."))
    # 13 tích phân đơn giản
    u=g.i(2,15);cc=g.i(1,20);val=u*u+cc*u
    A(g.MC("Đại số","Tích phân",f"∫₀^{u} (2x + {cc})dx bằng",str(val),[str(u*u),str(2*u+cc),str(val+cc)],f"Nguyên hàm x² + {cc}x.",[f"({u}² + {cc}·{u}) − 0 = {val}."],"F(b) − F(a)."))
    # 14 số phức mô đun
    x,y=g.c([(3,4),(5,12),(8,15),(7,24),(20,21),(9,40),(12,35),(11,60),(28,45),(33,56)]);kk=g.i(1,10);x,y=x*kk,y*kk
    if g.i(0,1): x,y=y,x
    sgn=g.c(["−","+"])
    A(g.MC("Đại số","Số phức",f"Mô đun của số phức z = {x} {sgn} {y}i bằng",str(int(math.hypot(x,y))),[str(x+y),str(x*x+y*y),str(abs(x-y))],"|a + bi| = √(a² + b²).",[f"√({x}² + {y}²) = {int(math.hypot(x,y))}."],"Mô đun luôn không âm."))
    # 15 số phức tổng
    a2,b2,c2,d2=g.i(1,5),g.i(1,5),g.i(1,5),g.i(1,5)
    A(g.MC("Đại số","Số phức",f"Cho z₁ = {a2} + {b2}i, z₂ = {c2} − {d2}i. Phần ảo của z₁ + z₂ là",vn(b2-d2),[vn(a2+c2),vn(b2+d2),f"{vn(b2-d2)}i"],"Cộng phần ảo với phần ảo.",[f"z₁ + z₂ = {a2+c2} + ({vn(b2-d2)})i."],"Phần ảo là số thực, không kèm i."))
    # 16 điểm biểu diễn
    a3,b3=g.i(-15,15) or 2,g.i(1,15)
    A(g.MC("Đại số","Số phức",f"Điểm biểu diễn số phức liên hợp của z = {vn(a3)} + {b3}i là",f"({vn(a3)}; −{b3})",[f"({vn(a3)}; {b3})",f"({vn(-a3)}; {b3})",f"({b3}; {vn(a3)})"],"z̄ = a − bi.",[f"z̄ = {vn(a3)} − {b3}i → ({vn(a3)}; −{b3})."],"Liên hợp đổi dấu phần ảo."))
    # 17 khối lập phương
    a4=g.i(2,99)
    if g.i(0,2)==0: A(g.MC("Hình học","Diện tích toàn phần",f"Diện tích toàn phần của hình lập phương cạnh {a4} bằng",str(6*a4*a4),[str(a4**3),str(4*a4*a4),str(a4*a4)],"6 mặt là hình vuông.",[f"6 × {a4}² = {6*a4*a4}."],"Stp = 6a²."))
    else: A(g.MC("Hình học","Thể tích",f"Thể tích khối lập phương cạnh {a4} bằng",str(a4**3),[str(a4**2),str(6*a4*a4),str(3*a4)],"V = a³.",[f"{a4}³ = {a4**3}."],"Diện tích toàn phần mới là 6a²."))
    # 18 chóp
    B=g.i(2,99);h=3*g.i(1,15)
    A(g.MC("Hình học","Thể tích khối chóp",f"Khối chóp có diện tích đáy B = {B} và chiều cao h = {h}. Thể tích khối chóp bằng",str(B*h//3),[str(B*h),str(B*h//2) if B*h%2==0 else str(B*h+1),str(B*h//3+B)],"V = Bh/3.",[f"{B} × {h} : 3 = {B*h//3}."],"Chóp chia 3, lăng trụ không chia."))
    # 19 lăng trụ
    B2=g.i(2,20);h2=g.i(2,15)
    A(g.MC("Hình học","Thể tích khối lăng trụ",f"Khối lăng trụ có diện tích đáy {B2} và chiều cao {h2}. Thể tích bằng",str(B2*h2),[str(B2*h2//1//3) if B2*h2%3==0 else str(B2+h2),str(2*B2*h2),str(B2*h2+B2)],"V = Bh.",[f"{B2} × {h2} = {B2*h2}."],"Lăng trụ không chia 3."))
    # 20 nón
    r1=g.i(2,40);h3=3*g.i(1,15)
    A(g.MC("Hình học","Khối nón",f"Thể tích khối nón có bán kính đáy {r1} và chiều cao {h3} bằng",f"{r1*r1*h3//3}π",[f"{r1*r1*h3}π",f"{2*r1*h3}π",f"{r1*h3}π"],"V = πr²h/3.",[f"π × {r1}² × {h3} : 3 = {r1*r1*h3//3}π."],"Nón = 1/3 trụ."))
    # 21 trụ Sxq
    r2=g.i(2,12);h4=g.i(2,15)
    A(g.MC("Hình học","Hình trụ",f"Diện tích xung quanh hình trụ có bán kính đáy {r2} và chiều cao {h4} bằng",f"{2*r2*h4}π",[f"{r2*h4}π",f"{r2*r2*h4}π",f"{2*r2*(r2+h4)}π"],"Sxq = 2πrh.",[f"2π × {r2} × {h4} = {2*r2*h4}π."],"Toàn phần mới cộng thêm 2 đáy."))
    # 22 mặt cầu
    R=g.i(2,300)
    A(g.MC("Hình học","Mặt cầu",f"Diện tích mặt cầu bán kính {R} bằng",f"{4*R*R}π",[f"{R*R}π",f"{2*R*R}π",f"{8*R*R}π"],"S = 4πR².",[f"4π × {R}² = {4*R*R}π."],"Thể tích khối cầu là 4πR³/3."))
    # 23 hình chiếu
    x0,y0,z0=g.i(1,15),g.i(-15,15) or 1,g.i(1,15)
    A(g.MC("Hình học","Tọa độ Oxyz",f"Trong không gian Oxyz, hình chiếu vuông góc của M({x0}; {vn(y0)}; {z0}) lên mặt phẳng (Oxy) là",f"({x0}; {vn(y0)}; 0)",[f"(0; 0; {z0})",f"({x0}; 0; {z0})",f"(0; {vn(y0)}; {z0})"],"Lên (Oxy) thì z = 0.",[f"Giữ x, y; cho z = 0."],"Chiếu lên mặt nào thì tọa độ còn lại bằng 0."))
    # 24 mặt cầu tâm
    a5,b5,c5,R5=g.i(1,4),g.i(1,4),g.i(1,4),g.i(2,5)
    A(g.MC("Hình học","Mặt cầu",f"Mặt cầu (S): (x − {a5})² + (y + {b5})² + (z − {c5})² = {R5*R5} có bán kính bằng",str(R5),[str(R5*R5),str(2*R5),f"√{R5}"],"Vế phải bằng R².",[f"R = √{R5*R5} = {R5}."],"Đừng lấy nhầm R²."))
    # 25 mặt phẳng VTPT
    n1,n2,n3,dd=g.i(1,4),g.i(1,4),g.i(1,4),g.i(1,9)
    A(g.MC("Hình học","Mặt phẳng",f"Mặt phẳng (P): {n1}x − {n2}y + {n3}z − {dd} = 0 có một vectơ pháp tuyến là",f"({n1}; −{n2}; {n3})",[f"({n1}; {n2}; {n3})",f"({n1}; −{n2}; −{dd})",f"(−{n2}; {n3}; −{dd})"],"Hệ số của x, y, z.",[f"n = ({n1}; −{n2}; {n3})."],"Không lấy hệ số tự do."))
    # 26 VTCP
    p1,p2,p3=g.i(1,5),g.i(1,5),g.i(1,5);s1,s2,s3=g.i(1,4),g.i(1,4),g.i(1,4)
    A(g.MC("Hình học","Đường thẳng",f"Đường thẳng d: (x − {p1})/{s1} = (y + {p2})/{s2} = (z − {p3})/(−{s3}) có một vectơ chỉ phương là",f"({s1}; {s2}; −{s3})",[f"({p1}; −{p2}; {p3})",f"({s1}; {s2}; {s3})",f"({p1}; {p2}; {p3})"],"Lấy các mẫu số.",[f"u = ({s1}; {s2}; −{s3})."],"Tử số cho điểm, mẫu số cho VTCP."))
    # 27 xác suất
    nb,nr=g.i(3,20),g.i(3,20)
    tot=math.comb(nb+nr,2);fav=math.comb(nb,2);it=g.c([("bi","bi"),("quả cầu","quả cầu"),("viên kẹo","viên kẹo")])[0]
    A(g.MC("Tổ hợp","Xác suất",f"Hộp có {nb} {it} xanh và {nr} {it} đỏ. Lấy ngẫu nhiên 2 {it}. Xác suất lấy được 2 {it} xanh là",vn(Fr(fav,tot)),[vn(Fr(nb,nb+nr)),vn(Fr(nb*nb,(nb+nr)**2)),vn(Fr(math.comb(nr,2),tot)) if Fr(math.comb(nr,2),tot)!=Fr(fav,tot) else vn(Fr(fav+1,tot))],"Đếm bằng tổ hợp.",[f"C({nb}, 2) : C({nb+nr}, 2) = {fav}/{tot} = {vn(Fr(fav,tot))}."],"Lấy đồng thời → tổ hợp."))
    # 28 góc
    ang,sa=g.c([(30,"a√6/3"),(45,"a√2"),(60,"a√6")]);kk=g.i(1,12);sc=lambda t:t if kk==1 else t.replace("a",f"{kk}a",1)
    sq=g.c(["S.ABCD","S.MNPQ","S.EFGH","S.IJKL","S.KLMN","S.UVXY"]);L=sq[2:];A0,C0=L[0],L[2]
    A(g.MC("Hình học","Góc",f"Hình chóp {sq} có đáy là hình vuông cạnh {sc('a')}, S{A0} vuông góc với mặt đáy và S{A0} = {sc(sa)}. Góc giữa đường thẳng S{C0} và mặt đáy bằng",f"{ang}°",[f"{a_}°" for a_ in [30,45,60,90] if a_!=ang],f"Góc giữa S{C0} và đáy là góc S{C0}{A0}.",[f"{A0}{C0} = {sc('a√2')}; tan = S{A0}/{A0}{C0} → góc {ang}°."],"Hình chiếu của đường xiên lên đáy."))
    # 29 GTLN trên đoạn
    c=g.i(-99,99) or 100;kk=g.c([1,2,3])
    vals={0:c,kk:c-2*kk**3,2*kk:c+2*kk**3}
    A(g.MC("Đại số","GTLN – GTNN",f"Giá trị lớn nhất của hàm số y = x³ − {3*kk*kk}x + {c} trên đoạn [0; {2*kk}] bằng",str(c+2*kk**3),[str(c),str(c-2*kk**3),str(c+kk**3)],"So sánh giá trị tại cực trị và hai đầu mút.",[f"y(0) = {c}, y({kk}) = {c-2*kk**3}, y({2*kk}) = {c+2*kk**3}."],"Tính tại cực trị và hai đầu mút."))

    # 30 bất PT mũ
    bb=g.c([2,3,4,5,6,7]);k=g.i(1,20);lt=g.i(0,3)
    sgn=["<",">","≤","≥"][lt];ok_=[f"(−∞; {k})",f"({k}; +∞)",f"(−∞; {k}]",f"[{k}; +∞)"][lt];op_=[f"({k}; +∞)",f"(−∞; {k})",f"[{k}; +∞)",f"(−∞; {k}]"][lt]
    A(g.MC("Đại số","Bất phương trình mũ",f"Tập nghiệm của bất phương trình {bb}^x {sgn} {bb**k} là",ok_,[op_,f"(0; {k})",f"(−∞; {bb**k})"],"Cơ số > 1 giữ chiều.",[f"x {sgn} {k}."],"Cơ số > 1 không đổi chiều."))
    # 31 tích phân thêm
    a6=g.i(1,99);up=g.i(1,9)
    A(g.MC("Đại số","Tích phân",f"Biết ∫₀^{up} f(x)dx = {a6}. Khi đó ∫₀^{up} [f(x) + 2x]dx bằng",str(a6+up*up),[str(a6+2*up),str(a6+2*up*up),str(2*a6)],f"∫₀^{up} 2x dx = {up*up}.",[f"{a6} + {up*up} = {a6+up*up}."],"Tách tích phân."))
    # 32 số phức nhân
    a7,b7=g.i(1,6),g.i(1,6);c7,d7=g.c([(1,1),(2,1),(1,2),(1,-1),(2,-1)])
    re_,im_=c7*a7-d7*b7,c7*b7+d7*a7
    A(g.MC("Đại số","Số phức",f"Số phức z = ({c7} {'+' if d7>0 else '−'} {abs(d7) if abs(d7)>1 else ''}i)({a7} + {b7}i) có phần thực bằng",vn(re_),[vn(im_),vn(c7*a7+d7*b7),vn(a7*b7)],"Nhân phân phối, i² = −1.",[f"Phần thực: {c7}·{a7} − ({d7})·{b7} = {vn(re_)}."],"i² = −1."))
    # 33 khoảng cách điểm-mp
    A_,B_,C_=g.c([(1,2,2),(2,1,2),(2,2,1),(2,-1,2)]);xm,ym,zm=g.i(0,3),g.i(0,3),g.i(0,3)
    D_=g.i(1,5);num=abs(A_*xm+B_*ym+C_*zm+D_)
    A(g.MC("Hình học","Khoảng cách",f"Khoảng cách từ M({xm}; {ym}; {zm}) đến (P): {A_}x {'+ ' if B_>0 else '− '}{abs(B_)}y + {C_}z + {D_} = 0 bằng",vn(Fr(num,3)),[vn(Fr(num,9)),str(num),vn(Fr(num+D_,3))],"d = |Ax₀ + By₀ + Cz₀ + D|/√(A² + B² + C²).",[f"|{num}|/√9 = {vn(Fr(num,3))}."],"Mẫu là √(A² + B² + C²) = 3."))
    # 34 mặt cầu qua điểm
    I=(g.i(-5,9),g.i(-5,9),g.i(-5,9));dd=g.c([(2,1,2),(1,2,2),(2,2,1),(2,3,6),(1,4,8)]);Ap=(I[0]+dd[0],I[1]+dd[1],I[2]+dd[2]);R2=sum(t*t for t in dd)
    f=lambda c,t:f"(x − {c})²".replace("x",t) if c>0 else (f"(x + {-c})²".replace("x",t) if c<0 else f"{t}²")
    eq=lambda P,r:f"{f(P[0],'x')} + {f(P[1],'y')} + {f(P[2],'z')} = {r}"
    A(g.MC("Hình học","Mặt cầu",f"Mặt cầu tâm I({I[0]}; {I[1]}; {I[2]}) đi qua A({Ap[0]}; {Ap[1]}; {Ap[2]}) có phương trình",eq(I,R2),[eq(I,int(math.isqrt(R2))),eq((-I[0],-I[1],-I[2]),R2),eq(Ap,R2)],"R = IA.",[f"IA² = {dd[0]}² + {dd[1]}² + {dd[2]}² = {R2}."],"Vế phải là R²."))
    # 35 CSN
    u=g.i(1,15);qq=g.c([2,3,-2,-3,4,5]);n=g.i(4,9)
    A(g.MC("Đại số","Cấp số nhân",f"Cấp số nhân có u₁ = {u}, công bội q = {vn(qq)}. Số hạng u{sb(n)} bằng",vn(u*qq**(n-1)),[vn(u*qq**n),vn(u+(n-1)*qq),vn(u*qq*(n-1))],"uₙ = u₁qⁿ⁻¹.",[f"{u} × ({vn(qq)}){sp(n-1)} = {vn(u*qq**(n-1))}."],"Số mũ là n − 1."))
    # 36 số nghiệm f(x)=m
    kk=g.c([1,2,3]);c=g.i(-99,99);hi=c+2*kk**3;lo=c-2*kk**3
    A(g.MC("Đại số","Tương giao",f"Hàm số y = x³ − {3*kk*kk}x{sg(c) if c else ''} có giá trị cực đại {vn(hi)} và cực tiểu {vn(lo)}. Số giá trị nguyên của m để phương trình x³ − {3*kk*kk}x{sg(c) if c else ''} = m có 3 nghiệm phân biệt là",str(hi-lo-1),[str(hi-lo+1),str(hi-lo),str(hi-lo-2)],f"Đường y = m cắt đồ thị 3 điểm khi {vn(lo)} < m < {vn(hi)}.",[f"Số nguyên trong ({vn(lo)}; {vn(hi)}): {hi-lo-1}."],"Nằm giữa hai giá trị cực trị (không lấy dấu bằng)."))

    # 37 diện tích hình phẳng
    a_=g.i(1,9);k=g.i(1,40)
    S=Fr(k**3,6*a_*a_);ax="" if a_==1 else str(a_)
    A(g.MC("Đại số","Diện tích hình phẳng",f"Diện tích hình phẳng giới hạn bởi y = {ax}x² và y = {k}x bằng",vn(S),[vn(2*S),vn(Fr(k*k,2*a_)),vn(3*S)],f"Giao điểm x = 0, x = {vn(Fr(k,a_))}.",[f"∫₀^{vn(Fr(k,a_))} ({k}x − {ax}x²)dx = {vn(S)}."],"Hàm trên trừ hàm dưới."))
    # 38 bất PT log nghiệm nguyên
    bb=g.c([2,3]);t=g.i(1,4 if bb==2 else 3);sh=g.i(1,30)
    A(g.MC("Đại số","Bất phương trình lôgarit",f"Số nghiệm nguyên của bất phương trình log_{bb}(x − {sh}) < {t} là",str(bb**t-1),[str(bb**t),str(bb**t+1),str(t)],f"Điều kiện x > {sh}.",[f"0 < x − {sh} < {bb**t} ⇒ {sh} < x < {bb**t+sh}.",f"Có {bb**t-1} số nguyên."],"Nhớ điều kiện xác định."))
    # 39 chóp đều
    a8=g.i(1,20);h8=3*g.i(1,10)
    A(g.MC("Hình học","Thể tích khối chóp",f"Hình chóp tứ giác đều có cạnh đáy {a8} và chiều cao {h8}. Thể tích khối chóp bằng",str(a8*a8*h8//3),[str(a8*a8*h8),str(a8*a8*h8//3+a8*a8),str(a8*h8)],"Đáy là hình vuông.",[f"{a8}² × {h8} : 3 = {a8*a8*h8//3}."],"Chóp đều: đáy đa giác đều."))
    # 40 lãi kép
    P=50*g.i(1,10);rr=g.i(5,9);yrs=g.i(2,4)
    val=P*(1+rr/100)**yrs
    A(g.MC("Đại số","Lãi kép",f"Gửi {P} triệu đồng, lãi suất {rr}%/năm, lãi nhập gốc. Sau {yrs} năm số tiền cả gốc lẫn lãi (làm tròn đến triệu) là",f"{round(val)} triệu",[f"{round(P*(1+rr*yrs/100))} triệu" if round(P*(1+rr*yrs/100))!=round(val) else f"{round(val)-3} triệu",f"{round(val)+5} triệu",f"{round(P*(1+rr/100))} triệu"],"T = P(1 + r)ⁿ.",[f"{P} × {1+rr/100:.2f}^{yrs} ≈ {val:.2f}."],"Lãi kép khác lãi đơn."))
    # 41 khoảng cách 2 điểm
    d1,d2,d3=g.c([(1,2,2),(2,3,6),(1,4,8),(2,6,9),(4,4,7),(2,10,11)]);x0_,y0_,z0_=g.i(-5,5),g.i(-5,5),g.i(-5,5)
    L_=int(math.sqrt(d1*d1+d2*d2+d3*d3))
    A(g.MC("Hình học","Tọa độ Oxyz",f"Cho A({x0_}; {y0_}; {z0_}), B({x0_+d1}; {y0_+d2}; {z0_+d3}). Độ dài AB bằng",str(L_),[str(d1+d2+d3),str(L_*L_),str(L_+1)],"AB = √(Δx² + Δy² + Δz²).",[f"√({d1}² + {d2}² + {d3}²) = {L_}."],"Bộ ba Pythagore trong không gian."))
    # 42 PT bậc hai số phức
    a9=g.i(1,25);b9=g.i(1,25)
    A(g.MC("Đại số","Số phức",f"Gọi z₁, z₂ là nghiệm phức của z² − {2*a9}z + {a9*a9+b9*b9} = 0. Giá trị |z₁| + |z₂| bằng",f"2√{a9*a9+b9*b9}" if int(math.isqrt(a9*a9+b9*b9))**2!=a9*a9+b9*b9 else str(2*math.isqrt(a9*a9+b9*b9)),[str(2*a9),str(a9*a9+b9*b9),str(2*b9)],"z = "+str(a9)+" ± "+str(b9)+"i.",[f"|z₁| = |z₂| = √{a9*a9+b9*b9}."],"Hai nghiệm liên hợp có cùng mô đun."))
    # 43 tham số đồng biến
    lim=g.i(10,80);aa=g.i(1,3)
    cnt_=lim-3*aa*aa+1
    A(g.MC("Đại số","Tham số",f"Có bao nhiêu số nguyên m ∈ [−{lim}; {lim}] để hàm số y = x³ − {3*aa}x² + mx + 1 đồng biến trên ℝ?",str(cnt_),[str(cnt_-1),str(cnt_+1),str(2*lim+1-cnt_)],f"y′ = 3x² − {6*aa}x + m ≥ 0 với mọi x.",[f"Δ′ = {9*aa*aa} − 3m ≤ 0 ⇔ m ≥ {3*aa*aa}.",f"m ∈ {{{3*aa*aa}; …; {lim}}}: {cnt_} số."],"Bậc ba đồng biến trên ℝ ⇔ y′ ≥ 0, Δ′ ≤ 0."))
    # 44 xác suất tổng chẵn
    n=g.i(7,200);ev=n//2;od=n-ev;par=g.i(0,1)
    fav=(math.comb(ev,2)+math.comb(od,2)) if par==0 else ev*od;tot=math.comb(n,2)
    A(g.MC("Tổ hợp","Xác suất",f"Chọn ngẫu nhiên 2 số khác nhau từ 1 đến {n}. Xác suất tổng hai số là số {'chẵn' if par==0 else 'lẻ'} bằng",vn(Fr(fav,tot)),[vn(Fr(tot-fav,tot)) if tot-fav!=fav else vn(Fr(1,3)),vn(Fr(fav,tot*2)),vn(Fr(math.comb(od,2),tot)) if Fr(math.comb(od,2),tot)!=Fr(fav,tot) else vn(Fr(fav+1,tot+1))],"Tổng chẵn khi cùng tính chẵn lẻ.",[f"Có {od} số lẻ, {ev} số chẵn.",f"Số cách thuận lợi {fav}/{tot}."],"Cùng tính chẵn lẻ → tổng chẵn."))
    # 45 đổi biến
    kk=g.c([2,3,4]);aa=g.c([1,2]);ex=aa**kk;cm=g.i(1,60);C_="" if cm==1 else str(cm)
    A(g.MC("Đại số","Tích phân đổi biến",f"∫₀^{aa} {cm*kk}x{SUPm(kk-1)}·e^(x{SUPm(kk)}) dx bằng",(f"{C_}(e^{ex} − 1)" if C_ else f"e^{ex} − 1") if ex>1 else (f"{C_}(e − 1)" if C_ else "e − 1"),[(f"{C_}e^{ex}" if ex>1 else f"{C_}e"),(f"{C_}(e^{ex} + 1)" if ex>1 else f"{C_}(e + 1)"),(f"{cm*kk}(e^{ex} − 1)" if ex>1 else f"{cm*kk}(e − 1)")],f"Đặt t = x{SUPm(kk)}.",[f"dt = {kk}x{SUPm(kk-1)} dx; ∫₀^{ex} eᵗ dt = e^{ex} − 1."],"Đổi cận khi đổi biến."))

    # 46 max |z|
    a10,b10=g.c([(3,4),(5,12),(8,15),(7,24)]);m10=g.i(1,5);a10,b10=a10*m10,b10*m10;rr2=g.i(1,9)
    A(g.MC("Đại số","Số phức",f"Số phức z thỏa |z − {a10} − {b10}i| = {rr2}. Giá trị lớn nhất của |z| bằng",str(int(math.hypot(a10,b10))+rr2),[str(int(math.hypot(a10,b10))-rr2),str(int(math.hypot(a10,b10))),str(a10+b10+rr2)],"Tập hợp z là đường tròn.",[f"|z|max = OI + R = {int(math.hypot(a10,b10))} + {rr2}."],"Max = OI + R, min = |OI − R|."))
    # 47 khối hộp
    l,w,hh=g.i(2,9),g.i(2,9),g.i(2,9)
    A(g.MC("Hình học","Khối hộp",f"Khối hộp chữ nhật có ba kích thước {l}, {w}, {hh}. Độ dài đường chéo bằng",f"√{l*l+w*w+hh*hh}",[f"{l+w+hh}",f"√{l*w*hh}",f"{l*w*hh}"],"d = √(a² + b² + c²).",[f"√({l*l} + {w*w} + {hh*hh})."],"Đường chéo hình hộp."))
    # 48 mặt phẳng qua 3 điểm chắn
    a11,b11,c11=g.i(1,9),g.i(1,9),g.i(1,9)
    A(g.MC("Hình học","Mặt phẳng",f"Mặt phẳng đi qua A({a11}; 0; 0), B(0; {b11}; 0), C(0; 0; {c11}) có phương trình",f"x/{a11} + y/{b11} + z/{c11} = 1",[f"x/{a11} + y/{b11} + z/{c11} = 0",f"{a11}x + {b11}y + {c11}z = 1",f"x + y + z = {a11+b11+c11}"],"Phương trình đoạn chắn.",["x/a + y/b + z/c = 1."],"Vế phải bằng 1."))
    # 49 tiếp tuyến
    x0=g.i(-5,5);kk=g.i(1,40)
    y0=x0**3-kk*x0;k=3*x0*x0-kk
    A(g.MC("Đại số","Tiếp tuyến",f"Hệ số góc của tiếp tuyến với đồ thị y = x³ − {kk}x tại điểm có hoành độ x = {vn(x0)} là",vn(k),[vn(y0) if y0!=k else vn(k+2),vn(3*x0*x0),vn(k+3)],"Hệ số góc = y′(x₀).",[f"y′ = 3x² − {kk}; y′({vn(x0)}) = {vn(k)}."],"Không nhầm với tung độ."))
    # 50 min biểu thức đơn giản (AM-GM)
    c_=g.i(2,30)**2;d_=g.i(0,30)
    A(g.MC("Đại số","GTNN",f"Giá trị nhỏ nhất của f(x) = x + {c_}/x{sg(d_) if d_ else ''} với x > 0 bằng",str(2*math.isqrt(c_)+d_),[str(math.isqrt(c_)+d_),str(c_+d_),str(2*c_+d_)],"Bất đẳng thức Cô-si.",[f"x + {c_}/x ≥ 2√{c_} = {2*math.isqrt(c_)}, dấu bằng khi x = {math.isqrt(c_)}; cộng thêm {d_}."],"Cô-si cho hai số dương."))
    assert len(Q)==50,len(Q)
    return Q
