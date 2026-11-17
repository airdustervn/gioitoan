from common import *
def bieu_thuc(g,pts):
    """returns list of 3 questions on expressions with √x; pts = (p1,p2,p3)"""
    a=g.i(1,9);b=g.c([1,2,3,4,5]);t=g.i(4,20)
    while t==b: t=g.i(4,20)
    xs=t*t
    Aval=Fr(t+a,t-b)
    k=g.i(2,6);m=g.i(1,4);c=g.i(1,12)
    if c==m*k-k: c+=1
    P=1+m;Qc=m*k-k-c;R=c*k
    num=f"{P}x"+ (f" {'+' if Qc>0 else '−'} {abs(Qc)}√x" if Qc else "")+f" + {R}"
    Btxt=f"B = √x/(√x + {k}) + {m if m>1 else ''}√x/(√x − {k}) − ({num})/(x − {k*k})"
    s_=g.c([2,3]) if k*k>=9 else 3
    cnt=s_*s_-(1 if k*k<s_*s_ else 0)
    qs=[]
    qs.append(g.F("Đại số","Biểu thức chứa căn",f"Cho A = (√x + {a})/(√x − {b}) với x ≥ 0, x ≠ {b*b}. Tính giá trị của A khi x = {xs} (viết dạng a/b nếu không nguyên).",vn(Aval).replace("−","-") if Aval.denominator>1 else Aval.numerator,f"√{xs} = {t}.",[f"A = ({t} + {a})/({t} − {b}) = {vn(Aval)}."],"Thay √x trước khi tính.",p=pts[0]))
    qs[-1]["a"]=str(Aval.numerator) if Aval.denominator==1 else f"{Aval.numerator}/{Aval.denominator}"
    ok=f"B = {c}/(√x + {k})"
    qs.append(g.MC("Đại số","Rút gọn biểu thức",f"Cho {Btxt} với x ≥ 0, x ≠ {k*k}. Rút gọn B ta được",ok,[f"B = {c}/(√x − {k})",f"B = {c}√x/(√x + {k})",f"B = (√x + {c})/(√x + {k})"],f"Quy đồng với mẫu chung x − {k*k} = (√x − {k})(√x + {k}).",[f"Tử số sau khi quy đồng: {c}√x − {c*k} = {c}(√x − {k}).",f"B = {c}(√x − {k})/[(√x − {k})(√x + {k})] = {c}/(√x + {k})."],"Phân tích x − k² = (√x − k)(√x + k).",p=pts[1]))
    qs.append(g.F("Đại số","Bất phương trình chứa căn",f"Với B = {c}/(√x + {k}) (x ≥ 0, x ≠ {k*k}), có bao nhiêu số nguyên x để B > {vn(Fr(c,k+s_))}?",cnt,f"B > {vn(Fr(c,k+s_))} ⇔ √x + {k} < {k+s_}.",[f"√x < {s_} ⇔ 0 ≤ x < {s_*s_}."]+([f"Loại x = {k*k}."] if k*k<s_*s_ else [])+[f"Có {cnt} số nguyên."],"Nhớ điều kiện xác định.",p=pts[2]))
    return qs
def lap_he(g,p):
    # mua hai loại sản phẩm
    a,b=g.i(8,30),g.i(8,30);pa=g.c([12,15,20,25,30,35,40]);pb=g.c([x for x in [8,10,12,15,18,20] if x<pa])
    tot=a+b;money=a*pa+b*pb
    return [g.F("Đại số","Giải bài toán bằng cách lập hệ",f"Một người mua {tot} bông hoa gồm hoa hồng và hoa cúc hết {money} nghìn đồng. Giá một bông hồng là {pa} nghìn, một bông cúc là {pb} nghìn. Người đó mua bao nhiêu bông hoa hồng?",a,"Gọi x, y là số hoa hồng, hoa cúc.",[f"x + y = {tot}; {pa}x + {pb}y = {money}.",f"x = {a}, y = {b}."],"Kiểm tra lại cả hai phương trình.",p=p/2),
            g.F("Đại số","Giải bài toán bằng cách lập hệ",f"(Tiếp câu trên: {tot} bông hoa, {money} nghìn đồng, hồng {pa} nghìn, cúc {pb} nghìn) Người đó mua bao nhiêu bông hoa cúc?",b,"Lấy tổng trừ số hoa hồng.",[f"{tot} − {a} = {b}."],"Trả lời đủ hai ẩn.",p=p/2)]
def lap_pt(g,p):
    w=g.i(5,25);d=g.i(2,9);S=w*(w+d)
    return g.F("Đại số","Phương trình bậc hai thực tế",f"Một mảnh vườn hình chữ nhật có chiều dài hơn chiều rộng {d} m và diện tích {S} m². Tính chiều rộng mảnh vườn (m).",w,"Gọi chiều rộng là x > 0.",[f"x(x + {d}) = {S} ⇔ x² + {d}x − {S} = 0.",f"x = {w} (loại nghiệm âm)."],"Loại nghiệm không thỏa điều kiện.",p=p)
def vong_lam(g,p):
    t1,t2=g.i(2,30),g.i(2,30)
    while t1==t2: t2=g.i(2,30)
    T=Fr(t1*t2,t1+t2)
    return g.F("Đại số","Bài toán làm chung",f"Hai vòi nước cùng chảy vào một bể cạn. Vòi thứ nhất chảy riêng đầy bể trong {t1} giờ, vòi thứ hai trong {t2} giờ. Hỏi cả hai vòi cùng chảy thì bao nhiêu giờ đầy bể?",T.numerator if T.denominator==1 else f"{T.numerator}/{T.denominator}","Cộng năng suất mỗi giờ.",[f"1/{t1} + 1/{t2} = {vn(Fr(1,t1)+Fr(1,t2))} bể/giờ.",f"Thời gian: {vn(T)} giờ."],"Năng suất là phần bể mỗi giờ.",p=p)
def tru(g,p):
    r=g.i(3,15)/10;h=g.i(8,40)/10;V=round(3.14*r*r*h,2)
    return g.F("Hình học","Hình trụ thực tế",f"Một bồn nước hình trụ có bán kính đáy {vn(r)} m, chiều cao {vn(h)} m. Tính thể tích bồn (m³), lấy π ≈ 3,14 và làm tròn đến hàng phần trăm.",V,"V = πr²h.",[f"3,14 × {vn(r)}² × {vn(h)} ≈ {vn(V)} m³."],"Bình phương bán kính, không phải đường kính.",p=p)
def non(g,p):
    r=g.i(2,15);h=g.i(3,20);V=round(3.14*r*r*h/3,2)
    return g.F("Hình học","Hình nón thực tế",f"Một chiếc nón lá có dạng hình nón với bán kính đáy {r} dm, chiều cao {h} dm. Tính thể tích phần không gian bên trong nón (dm³), lấy π ≈ 3,14, làm tròn đến hàng phần trăm.",V,"V = πr²h/3.",[f"3,14 × {r}² × {h} : 3 ≈ {vn(V)}."],"Nón bằng 1/3 trụ cùng đáy, cùng cao.",p=p)
def he_pt(g,p):
    x,y=g.i(2,9),g.i(0,9);u=Fr(1,x-1);v=Fr(1,y+1)
    while True:
        a,b,c,d=g.i(1,6),g.i(1,6),g.i(1,6),g.c([-3,-2,-1,1,2,3])
        if a*d-b*c: break
    r1=a*u+b*v;r2=c*u+d*v
    return g.F("Đại số","Hệ phương trình",f"Giải hệ phương trình: {a}/(x − 1) + {b}/(y + 1) = {vn(r1)} và {c}/(x − 1) {'+' if d>0 else '−'} {abs(d)}/(y + 1) = {vn(r2)}. Tính x + y.",x+y,"Đặt u = 1/(x − 1), v = 1/(y + 1).",[f"Giải được u = {vn(u)}, v = {vn(v)}.",f"x = {x}, y = {y} ⇒ x + y = {x+y}."],"Đặt ẩn phụ rồi đổi lại.",p=p)
def parabol(g,p):
    k_=g.i(1,4)
    while True:
        m=g.i(-12,6);K=4*k_*k_-2*m+2
        if k_*k_-m+1>0: break
    return g.F("Đại số","Parabol và đường thẳng",f"Cho (P): y = x² và d: y = {2*k_}x − m + 1. Tìm m để d cắt (P) tại hai điểm phân biệt có hoành độ x₁, x₂ thỏa x₁² + x₂² = {K}.",m,f"Phương trình hoành độ x² − {2*k_}x + m − 1 = 0.",[f"Δ′ = {k_*k_} − m + 1 > 0 ⇔ m < {k_*k_+1}.",f"x₁² + x₂² = {4*k_*k_} − 2(m − 1) = {K} ⇒ m = {m} (thỏa)."],"Kiểm tra điều kiện Δ.",p=p)
def viet(g,p):
    s=g.i(3,12);pp=g.i(1,min(20,s*s//4))
    return g.F("Đại số","Hệ thức Vi-ét",f"Phương trình x² − {s}x + {pp} = 0 có hai nghiệm x₁, x₂. Tính x₁² + x₂².",s*s-2*pp,"x₁ + x₂ = "+str(s)+", x₁x₂ = "+str(pp)+".",[f"(x₁ + x₂)² − 2x₁x₂ = {s*s} − {2*pp} = {s*s-2*pp}."],"Không cần giải phương trình.",p=p)
def circle(g,ps):
    al=g.i(15,75);tri=g.c([(3,4,5),(5,12,13),(8,15,17),(7,24,25),(20,21,29)]);k=g.i(1,6);R,T,D=tri[0]*k,tri[1]*k,tri[2]*k
    if g.i(0,1): R,T=T,R
    th=g.c([20,30,36,40,45,60,72,80,90,100,120,135,150]);R2=g.i(3,20)
    L=round(3.14*R2*th/180,2)
    return [g.F("Hình học","Góc nội tiếp",f"Cho đường tròn (O) đường kính AB, điểm C thuộc đường tròn sao cho góc CAB = {al}°. Tính số đo góc ABC (độ).",90-al,"Góc nội tiếp chắn nửa đường tròn.",[f"Góc ACB = 90° ⇒ góc ABC = 90° − {al}° = {90-al}°."],"Góc nội tiếp chắn nửa đường tròn là góc vuông.",p=ps[0]),
            g.F("Hình học","Tiếp tuyến",f"Từ điểm M nằm ngoài đường tròn (O; {R} cm) kẻ tiếp tuyến MA (A là tiếp điểm). Biết OM = {D} cm. Tính độ dài MA (cm).",T,"OA ⊥ MA.",[f"MA = √(OM² − OA²) = √({D*D} − {R*R}) = {T} cm."],"Bán kính vuông góc với tiếp tuyến tại tiếp điểm.",p=ps[1]),
            g.F("Hình học","Độ dài cung",f"Trên đường tròn (O; {R2} cm), góc ở tâm AOB = {th}°. Tính độ dài cung nhỏ AB (cm), lấy π ≈ 3,14, làm tròn đến hàng phần trăm.",L,"l = πRn/180.",[f"3,14 × {R2} × {th} : 180 ≈ {vn(L)} cm."],"Độ dài cung tỉ lệ với số đo góc ở tâm.",p=ps[2])]
def cuc_tri_cu(g,p):
    a=g.i(3,9);c=g.i(2,a*a-1)
    return g.F("Đại số","Giá trị nhỏ nhất",f"Cho x ≥ {a}. Tìm giá trị nhỏ nhất của P = x + {c}/x.",vn(Fr(a*a+c,a)).replace("−","-") if Fr(a*a+c,a).denominator==1 else f"{a*a+c}/{a}","P đồng biến khi x ≥ √"+str(c)+".",[f"Với x ≥ {a} > √{c}, P tăng theo x.",f"Pmin = P({a}) = {a} + {c}/{a} = {vn(Fr(a*a+c,a))}."],"Điểm rơi của Cô-si nằm ngoài miền thì xét tại đầu mút.",p=p)
def toi_uu_moi(g,p):
    L=4*g.i(4,100)
    return g.F("Đại số","Tối ưu thực tế",f"Bác An có {L} m lưới để rào một khu vườn hình chữ nhật, một cạnh tựa vào bức tường (không cần rào). Diện tích lớn nhất có thể rào được là bao nhiêu m²?",L*L//8,"Gọi cạnh vuông góc với tường là x.",[f"S = x({L} − 2x), lớn nhất khi x = {L//4}.",f"Smax = {L//4} × {L//2} = {L*L//8} m²."],"Biến đổi về dạng bình phương hoặc dùng Cô-si.",p=p)
def thong_ke(g,p):
    f=[g.i(4,10) for _ in range(5)];n=sum(f);j=g.i(1,3)
    while (f[j]*100)%n: f[0]+=1;n=sum(f)
    groups=["[140; 145)","[145; 150)","[150; 155)","[155; 160)","[160; 165)"]
    tab="; ".join(f"{gr}: {x}" for gr,x in zip(groups,f))
    return g.F("Tổ hợp","Thống kê ghép nhóm",f"Chiều cao (cm) của {n} học sinh được ghép nhóm: {tab}. Tần số tương đối của nhóm {groups[j]} là bao nhiêu phần trăm?",f[j]*100//n,"Tần số tương đối = tần số : tổng × 100%.",[f"{f[j]} : {n} × 100% = {f[j]*100//n}%."],"Tổng tần số bằng số học sinh.",p=p)
def xs_the(g,p):
    N=5*g.i(4,16);d=g.i(3,9)
    cnt=N//d
    return g.F("Tổ hợp","Xác suất",f"Một hộp có {N} tấm thẻ đánh số từ 1 đến {N}. Rút ngẫu nhiên một thẻ. Tính xác suất thẻ rút được mang số chia hết cho {d} (viết dạng a/b tối giản).",f"{Fr(cnt,N).numerator}/{Fr(cnt,N).denominator}","Đếm các bội của "+str(d)+".",[f"Có {cnt} bội của {d} từ 1 đến {N}.",f"P = {cnt}/{N} = {vn(Fr(cnt,N))}."],"Xác suất = số kết quả thuận lợi : số kết quả có thể.",p=p)
def old(seed):
    g=G(seed)
    return [["Bài I (2 điểm) · Biểu thức chứa căn",bieu_thuc(g,(0.5,1,0.5))],
            ["Bài II (2,5 điểm) · Giải bài toán bằng cách lập phương trình, hệ phương trình",lap_he(g,1)+[g.c([lap_pt,vong_lam])(g,1),tru(g,0.5)]],
            ["Bài III (2 điểm) · Hệ phương trình; parabol và đường thẳng",[he_pt(g,1),parabol(g,1)]],
            ["Bài IV (3 điểm) · Hình học đường tròn",circle(g,(1,1,1))],
            ["Bài V (0,5 điểm) · Giá trị nhỏ nhất",[cuc_tri_cu(g,0.5)]]]
def new(seed):
    g=G(seed)
    return [["Bài I (1,5 điểm) · Thống kê và xác suất",[thong_ke(g,0.75),xs_the(g,0.75)]],
            ["Bài II (1,5 điểm) · Biểu thức chứa căn",bieu_thuc(g,(0.5,0.5,0.5))],
            ["Bài III (2,5 điểm) · Bài toán thực tế; phương trình bậc hai",lap_he(g,1)+[lap_pt(g,1),viet(g,0.5)]],
            ["Bài IV (4 điểm) · Hình học thực tế và đường tròn",[g.c([tru,non])(g,1)]+circle(g,(1,1,1))],
            ["Bài V (0,5 điểm) · Tối ưu thực tế",[toi_uu_moi(g,0.5)]]]
