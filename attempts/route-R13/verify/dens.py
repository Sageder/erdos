import numpy as np, math
X=3_000_000
# smallest prime factor sieve
spf=np.zeros(X+3,dtype=np.int32)
for i in range(2,int((X+2)**0.5)+1):
    if spf[i]==0:
        spf[i*i::i]=np.where(spf[i*i::i]==0,i,spf[i*i::i])
for i in range(2,X+3):
    if spf[i]==0: spf[i]=i
def fact(m):
    f={}
    while m>1:
        p=int(spf[m]); e=0
        while m%p==0: m//=p; e+=1
        f[p]=e
    return f
def largest(m): return max(fact(m)) if m>1 else 1
def carries(n,l):
    # number of carries adding n+n base l
    c=0; carry=0
    while n>0:
        d=n%l; s=2*d+carry
        if s>=l: carry=1; c+=1
        else: carry=0
        n//=l
    return c
P0=4
def check(n,b):
    # n+1,n+2 both n^b smooth; report (Cl_ok, carry_ok)
    Cl=True; car=True
    for j in (1,2):
        m=n+j; f=fact(m)
        for l,e in f.items():
            if l<=P0: continue
            if e>1: Cl=False
            else:
                W=m//l
                if ((W-1)%l) < (l-1)//2: Cl=False
            if carries(n,l) < 2*e: car=False
    return Cl,car
for b in (0.5,0.35,0.25,0.15,0.10):
    tot=0; cl=0; car=0
    lo=100000
    for n in range(lo,X,1):
        thr=n**b
        if largest(n+1)<=thr and largest(n+2)<=thr:
            tot+=1
            a,c=check(n,b)
            cl+=a; car+=c
    print("b=%.2f  smooth-pairs=%d (dens %.4f)  C_l-all: %d (%.4f of pairs)  exact-carry-all: %d (%.4f)"%(
        b,tot,tot/(X-lo),cl,cl/max(tot,1),car,car/max(tot,1)))
