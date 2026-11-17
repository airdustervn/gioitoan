import random, math
from fractions import Fraction as Fr
def vn(x):
    if isinstance(x,Fr):
        if x.denominator==1: x=x.numerator
        else: return ("−" if x<0 else "")+f"{abs(x.numerator)}/{x.denominator}"
    if isinstance(x,float):
        x=round(x,4)
        if x==int(x): x=int(x)
        else: return (("−" if x<0 else "")+str(abs(x))).replace(".",",")
    return ("−" if x<0 else "")+str(abs(x))
def sg(x,first=False):
    """signed term for polynomials: returns ' + 3' or ' − 3'"""
    return (" − " if x<0 else " + ")+vn(abs(x) if not isinstance(x,Fr) else abs(x))
class G:
    def __init__(s,seed): s.r=random.Random(seed)
    def i(s,a,b): return s.r.randint(a,b)
    def c(s,l): return s.r.choice(l)
    def MC(s,t,d,q,ok,bad,h,sol,m="",p=0.2):
        opts=[ok]
        for b in bad:
            if b not in opts and len(opts)<4: opts.append(b)
        import re
        for dlt in [1,-1,2,-2,3,4,-3,5,6,10]:
            if len(opts)>=4: break
            mm=re.search(r"\d+",ok)
            if not mm: break
            v=int(mm.group())+dlt
            if v<0: continue
            cand=ok[:mm.start()]+str(v)+ok[mm.end():]
            if cand not in opts: opts.append(cand)
        assert len(opts)==4,(q,opts)
        s.r.shuffle(opts)
        return {"t":t,"d":d,"q":q,"o":opts,"a":opts.index(ok),"p":p,"h":h,"s":sol,"m":m or h}
    def F(s,t,d,q,a,h,sol,m="",p=0.5):
        if isinstance(a,float): a=round(a,2); a=int(a) if a==int(a) else a
        return {"t":t,"d":d,"q":q,"a":str(a),"f":True,"p":p,"h":h,"s":sol,"m":m or h}
    def TF(s,stem,items):
        return {"stem":stem,"items":[{"t":"Đại số","d":"Đúng/Sai","q":q,"o":["Đúng","Sai"],"a":0 if ok else 1,"h":h,"s":[sol+(" Đúng." if ok else " Sai.")],"m":""} for q,ok,h,sol in items]}
