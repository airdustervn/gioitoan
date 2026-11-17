import re,hashlib,random
def norm(s): return re.sub(r"\s+"," ",str(s).strip())
def H(s): return hashlib.sha1(norm(s).encode()).hexdigest()[:12]
def qkey(q): return H(q["stem"]) if q.get("stem") else H(q["q"])
def pick_list(cands,seen):
    """cands: list of candidate lists (same length); choose per position first unseen; fallback first."""
    out=[];n=len(cands[0]);dup=0
    for i in range(n):
        ch=None
        for c in cands:
            if i<len(c) and qkey(c[i]) not in seen and all(qkey(c[i])!=qkey(o) for o in out): ch=c[i];break
        if ch is None: ch=cands[0][i];dup+=1
        out.append(ch);seen.add(qkey(ch))
    return out,dup
K=120
def thpt_old(fn,seed,seen):
    return pick_list([fn(seed+97*k) for k in range(K)],seen)
def thpt_new(fn,seed,seen):
    C=[fn(seed+97*k) for k in range(K)];d=0;out={}
    for part in ("P1","P2","P3"):
        out[part],x=pick_list([c[part] for c in C],seen);d+=x
    return out,d
def parts(fn,seed,seen):
    C=[fn(seed+97*k) for k in range(K)]
    shape=[len(p[1]) for p in C[0]];C=[c for c in C if [len(p[1]) for p in c]==shape]
    flat,d=pick_list([[q for p in c for q in p[1]] for c in C],seen)
    res=[];i=0
    for nm,qs in C[0]:
        res.append([nm,flat[i:i+len(qs)]]);i+=len(qs)
    return res,d
def intl_build(gens,mc,seed,nmc,nopen,mcopts,seen,key="q"):
    out=[];tk=set();t=0
    while len(out)<nmc+nopen and t<200:
        r=random.Random(seed*1000+t);t+=1
        for q in gens(r):
            k=q["vi"][:18]
            if k in tk or H(q[key]) in seen: continue
            tk.add(k);seen.add(H(q[key]));out.append(q)
            if len(out)>=nmc+nopen: break
        if t>3: tk=set()  # allow template reuse with new numbers once templates exhausted
    rr=random.Random(seed)
    res=[mc(rr,q,mcopts) for q in out[:nmc]]
    for q in out[nmc:]:
        q=dict(q);a=q["a"];q["a"]=str(int(a) if float(a)==int(float(a)) else a);q["f"]=True;res.append(q)
    return res
