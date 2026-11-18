from common import *
from thpt_old import paper as oldp
def paper(seed):
    g=G(seed); O=oldp(seed+77)
    P1=[]
    for i in [0,1,2,4,10,12,17,22,24,25,26,29]:
        q=dict(O[i]);q["p"]=0.25;P1.append(q)
    P2=[]
    # G1 hàm bậc ba f = x³ − 3a x² + c
    a=g.i(1,5);c=g.i(-40,40) or 1
    f=lambda x:x**3-3*a*x*x+c
    fmin=min(f(0),f(2*a),f(3*a)); nroots=3 if f(0)>0 and f(2*a)<0 else (1 if f(0)*f(2*a)>0 else 2)
    stmt_d=g.c([3,1])
    P2.append(g.TF(f"Câu 1. Cho hàm số f(x) = x³ − {3*a}x²{sg(c)}.",[
      (f"a) f′(x) = 3x² − {6*a}x.",True,"Đạo hàm từng hạng tử.",f"f′(x) = 3x² − {6*a}x."),
      (f"b) Hàm số đạt cực tiểu tại x = 0.",False,"Xét dấu f′.",f"f′ đổi dấu từ + sang − tại x = 0 nên x = 0 là điểm cực đại."),
      (f"c) Giá trị nhỏ nhất của f(x) trên đoạn [0; {3*a}] bằng {vn(fmin)}.",True,"So sánh f tại 0, "+str(2*a)+", "+str(3*a)+".",f"f(0) = {vn(f(0))}, f({2*a}) = {vn(f(2*a))}, f({3*a}) = {vn(f(3*a))}; nhỏ nhất {vn(fmin)}."),
      (f"d) Phương trình f(x) = 0 có đúng {stmt_d} nghiệm thực.",nroots==stmt_d,"Xét dấu giá trị cực đại, cực tiểu.",f"f(0) = {vn(f(0))}, f({2*a}) = {vn(f(2*a))} → phương trình có {nroots} nghiệm.")]))
    # G2 Oxyz
    A_=(g.i(-5,6),g.i(-5,6),g.i(-5,6));n=(1,2,2);D=-(A_[0]+2*A_[1]+2*A_[2])+g.c([3,6,9])
    dA=abs(A_[0]+2*A_[1]+2*A_[2]+D)//3
    B_=(A_[0]+2,A_[1]+4,A_[2]+4)
    P2.append(g.TF(f"Câu 2. Trong không gian Oxyz, cho mặt phẳng (P): x + 2y + 2z {'+' if D>=0 else '−'} {abs(D)} = 0 và các điểm A({vn(A_[0])}; {vn(A_[1])}; {vn(A_[2])}), B({vn(B_[0])}; {vn(B_[1])}; {vn(B_[2])}).",[
      ("a) Vectơ n = (1; 2; 2) là một vectơ pháp tuyến của (P).",True,"Hệ số của x, y, z.","n = (1; 2; 2)."),
      ("b) Điểm A thuộc mặt phẳng (P).",False,"Thay tọa độ A.",f"Thay A: {A_[0]+2*A_[1]+2*A_[2]+D} ≠ 0."),
      (f"c) Khoảng cách từ A đến (P) bằng {dA}.",True,"Công thức khoảng cách.",f"|{A_[0]+2*A_[1]+2*A_[2]+D}|/3 = {dA}."),
      ("d) Đường thẳng AB song song với (P).",False,"So sánh AB với n.","AB = (2; 4; 4) = 2n nên AB vuông góc với (P).")]))
    # G3 xác suất có điều kiện
    D1=lambda x,n=1:f"{x:.{n}f}".replace(".",",")
    p1=g.c([0.2,0.3,0.4,0.5,0.6,0.7,0.8]);r1=g.c([0.6,0.7,0.8,0.9]);r2=g.c([0.1,0.2,0.3,0.4,0.5]);ctx=g.c([("ôn tập đều đặn","ôn đều đặn"),("tham gia câu lạc bộ Toán","tham gia câu lạc bộ"),("làm đủ bài tập về nhà","làm đủ bài tập")])
    pT=p1*r1+(1-p1)*r2;bay=p1*r1/pT
    P2.append(g.TF(f"Câu 3. Một lớp có {int(round(p1*100))}% học sinh {ctx[0]}. Xác suất đạt điểm giỏi của học sinh {ctx[1]} là {D1(r1)}, của học sinh còn lại là {D1(r2)}. Chọn ngẫu nhiên một học sinh.",[
      (f"a) Xác suất chọn được học sinh {ctx[1]} là {D1(p1)}.",True,"Đọc dữ kiện.",f"{int(round(p1*100))}% = {D1(p1)}."),
      (f"b) Xác suất học sinh đạt điểm giỏi, biết học sinh đó {ctx[1]}, là {D1(r2)}.",False,"Xác suất có điều kiện đã cho.",f"P(giỏi | {ctx[1]}) = {D1(r1)}."),
      (f"c) Xác suất học sinh đạt điểm giỏi là {D1(pT,2)}.",True,"Công thức xác suất toàn phần.",f"{D1(p1)} × {D1(r1)} + {D1(1-p1)} × {D1(r2)} = {D1(pT,2)}."),
      (f"d) Biết học sinh đạt điểm giỏi, xác suất học sinh đó {ctx[1]} lớn hơn 0,9.",bay>0.9,"Công thức Bayes.",f"{D1(p1*r1,2)} : {D1(pT,2)} ≈ {D1(bay,3)}.")]))
    # G4 chuyển động
    v0=g.i(5,60);a_=g.i(1,10)
    T=v0/a_;S=v0*T-a_*T*T/2
    P2.append(g.TF(f"Câu 4. Một ô tô đang chạy với vận tốc {v0} m/s thì hãm phanh, chuyển động chậm dần đều với vận tốc v(t) = {v0} − {a_}t (m/s), t tính bằng giây.",[
      (f"a) Sau 1 giây kể từ lúc hãm phanh, vận tốc ô tô là {v0-a_} m/s.",True,"Thay t = 1.",f"v(1) = {v0-a_}."),
      (f"b) Ô tô dừng hẳn sau {vn(Fr(v0,a_))} giây.",True,"Giải v(t) = 0.",f"t = {v0}/{a_} = {vn(Fr(v0,a_))}."),
      (f"c) Quãng đường ô tô đi được từ lúc hãm phanh đến khi dừng là {vn(Fr(v0*v0,a_))} m.",False,"S = ∫ v(t)dt.",f"S = v₀²/(2a) = {vn(Fr(v0*v0,2*a_))} m."),
      (f"d) Trong 2 giây đầu ô tô đi được {2*v0-2*a_} m.",True,"∫₀² v(t)dt.",f"{2*v0} − {a_} × 2 = {2*v0-2*a_} m.")]))
    P3=[]
    L=6*g.i(1,600);x=L//6;V=(L-2*x)**2*x
    P3.append(g.F("Đại số","Tối ưu thực tế",f"Từ tấm bìa hình vuông cạnh {L} dm, cắt bỏ bốn hình vuông bằng nhau ở bốn góc rồi gấp thành hộp không nắp. Thể tích lớn nhất của hộp là bao nhiêu dm³?",V,"V(x) = x(L − 2x)², tìm x.",[f"V′ = 0 tại x = L/6 = {x}.",f"V = {x} × {L-2*x}² = {V}."],"Khảo sát hàm thể tích."))
    a2=g.i(2,40);h2=g.i(2,50)
    P3.append(g.F("Hình học","Thể tích lăng trụ",f"Lăng trụ đứng ABC.A′B′C′ có đáy là tam giác vuông cân tại A, AB = {a2}, AA′ = {h2}. Tính thể tích khối lăng trụ.",a2*a2*h2/2,"V = S đáy × chiều cao.",[f"S đáy = {a2}²/2; V = {vn(Fr(a2*a2*h2,2))}."],"Lăng trụ đứng: chiều cao là cạnh bên."))
    pa=g.i(2,9)/100;pb=g.i(1,8)/100;sa=g.i(3,8)/10;sb=round(1-sa,1)
    pd=sa*pa+sb*pb;ans=round(sa*pa/pd,2)
    P3.append(g.F("Tổ hợp","Công thức Bayes",f"Nhà máy A sản xuất {int(round(sa*100))}% sản phẩm với tỉ lệ lỗi {int(round(pa*100))}%, nhà máy B sản xuất phần còn lại với tỉ lệ lỗi {int(round(pb*100))}%. Lấy ngẫu nhiên một sản phẩm thấy bị lỗi. Xác suất sản phẩm đó do A sản xuất là bao nhiêu? (làm tròn đến hàng phần trăm)",ans,"P(A | lỗi) = P(A)P(lỗi | A)/P(lỗi).",[f"P(lỗi) = {D1(pd,3)}.",f"P(A | lỗi) ≈ {D1(ans,2)}."],"Xác suất toàn phần ở mẫu số."))
    d1=g.c([(2,3,6),(1,4,8),(4,4,7),(2,6,9),(1,2,2),(2,10,11),(6,6,7),(3,4,12)]);o0=(g.i(0,9),g.i(0,9),g.i(0,9))
    P3.append(g.F("Hình học","Tọa độ ứng dụng",f"Trong hệ trục Oxyz (đơn vị mét), một flycam bay từ điểm M({o0[0]}; {o0[1]}; {o0[2]}) đến N({o0[0]+d1[0]}; {o0[1]+d1[1]}; {o0[2]+d1[2]}) theo đường thẳng. Quãng đường bay là bao nhiêu mét?",int(math.sqrt(sum(t*t for t in d1))),"MN = √(Δx² + Δy² + Δz²).",[f"√({d1[0]}² + {d1[1]}² + {d1[2]}²) = {int(math.sqrt(sum(t*t for t in d1)))}."],"Khoảng cách hai điểm."))
    k=g.i(1,12);T2=g.i(2,9);c0=g.i(1,30)
    P3.append(g.F("Đại số","Tích phân ứng dụng",f"Một vật chuyển động với vận tốc v(t) = {3*k}t² + {c0} (m/s). Quãng đường vật đi được trong {T2} giây đầu là bao nhiêu mét?",k*T2**3+c0*T2,"S = ∫₀ᵀ v(t)dt.",[f"∫₀^{T2} ({3*k}t² + {c0})dt = {k}·{T2}³ + {c0}·{T2} = {k*T2**3+c0*T2}."],"Quãng đường là tích phân của vận tốc."))
    n=g.i(3,12);q=g.c([2,3,4]);u=g.i(1,30)
    P3.append(g.F("Đại số","Cấp số nhân",f"Một loài vi khuẩn cứ mỗi giờ tăng gấp {q} lần. Ban đầu có {u} nghìn con. Sau {n} giờ có bao nhiêu nghìn con?",u*q**n,f"uₙ = u₀ · {q}ⁿ.",[f"{u} × {q}^{n} = {u*q**n}."],f"Mỗi giờ nhân với công bội {q}."))
    return {"P1":P1,"P2":P2,"P3":P3}
