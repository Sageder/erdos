import numpy as np
X=4_000_000
spf=np.zeros(X+3,dtype=np.int32)
for i in range(2,int((X+2)**0.5)+1):
    if spf[i]==0:
        seg=spf[i*i::i]; spf[i*i::i]=np.where(seg==0,i,seg)
for i in range(2,X+3):
    if spf[i]==0: spf[i]=i
def P(m):
    p=1
    while m>1:
        q=int(spf[m]); p=max(p,q)
        while m%q==0: m//=q
    return p
def nuP(m,p):
    e=0
    while m%p==0: m//=p; e+=1
    return e
def inA(n):
    if n<3: return False
    p=P(n)
    if p**2> n and False: pass
    if not (n**0.40 < p <= n**0.50): return False
    if nuP(n,p)!=1: return False
    W=n//p
    return ((W-1)%p) >= (p-1)//2
lo=1000; hi=X//2
cntA=0; diff=0; cntBand=0; diffBand=0
def inBand(n):
    if n<3: return False
    p=P(n); return n**0.40 < p <= n**0.50
for n in range(lo,hi):
    a=inA(n); b=inA(2*n); cntA+=a; diff+= (a!=b)
    c=inBand(n); d=inBand(2*n); cntBand+=c; diffBand+=(c!=d)
N=hi-lo
print("A (band + C at largest prime): density %.5f ; instability d(1_{n in A} != 1_{2n in A}) = %.5f"%(cntA/N,diff/N))
print("Band only (Hildebrand's set):  density %.5f ; instability                              = %.5f"%(cntBand/N,diffBand/N))
