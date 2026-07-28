import numpy as np
X=8_000_000
spf=np.zeros(X+3,dtype=np.int32)
for i in range(2,int((X+2)**0.5)+1):
    if spf[i]==0:
        seg=spf[i*i::i]; spf[i*i::i]=np.where(seg==0,i,seg)
for i in range(2,X+3):
    if spf[i]==0: spf[i]=i
def fact(m):
    f={}
    while m>1:
        p=int(spf[m]); e=0
        while m%p==0: m//=p; e+=1
        f[p]=e
    return f
def carries(n,l):
    c=0; carry=0
    while n>0:
        d=n%l; s=2*d+carry
        if s>=l: carry=1; c+=1
        else: carry=0
        n//=l
    return c
P0=4
import math
def run(lo,hi,b):
    tot=cl=car=0
    for n in range(lo,hi):
        thr=n**b
        f1=fact(n+1); f2=fact(n+2)
        if max(f1)>thr or max(f2)>thr: continue
        tot+=1; C=True; K=True
        for f,j in ((f1,1),(f2,2)):
            m=n+j
            for l,e in f.items():
                if l<=P0: continue
                if e>1 or ((m//l -1)%l) < (l-1)//2: C=False
                if carries(n,l) < 2*e: K=False
        cl+=C; car+=K
    return tot,cl,car
for (lo,hi) in [(100000,2000000),(2000000,4000000),(4000000,8000000)]:
    t,c,k=run(lo,hi,0.5)
    print("range [%d,%d) b=0.5: smoothpairs=%d dens=%.4f  C_l-all frac=%.4f  exact-carry frac=%.4f"%(lo,hi,t,t/(hi-lo),c/t,k/t))
