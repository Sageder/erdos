import sys
from audit_core import *
from audit_Rk import cond_ii
from sympy import primerange
N=2000000
spf=list(range(N+8)); i=2
while i*i<=N+7:
    if spf[i]==i:
        for m in range(i*i,N+8,i):
            if spf[m]==m: spf[m]=i
    i+=1
def fac(m):
    d={}
    while m>1:
        p=spf[m];e=0
        while m%p==0: m//=p;e+=1
        d[p]=e
    return d
def smooth_part(m,P0):
    c=1
    for l in primerange(2,P0+1):
        while m%l==0: m//=l;c*=l
    return c,m
def full_Rk(n,k,P0):
    if not cond_ii(n,k,P0): return False
    for j in range(1,k+1):
        c,u=smooth_part(n+j,P0)
        f=fac(u)
        if sum(f.values())!=2 or len(f)!=2: return False
        p1,p2=sorted(f); ok=False
        for r,s in ((p1,p2),(p2,p1)):
            if r>max(P0,c) and s>max(P0,c) and c*s-1<r<=2*c*s-1 and (c*r)%s>=(s+1)//2: ok=True
        if not ok: return False
    return True
for k in (2,3):
    P0=2*k; hits=[];fp=[]
    for n in range(2,N+1):
        if full_Rk(n,k,P0):
            hits.append(n)
            if not in_S_ladder_criterion(n,k): fp.append(n)
    print("FULL Lemma R_k (incl. cond (ii)), k=%d P0=%d, n<=%d: hits=%d %s  FALSE POSITIVES=%d %s"%(k,P0,N,len(hits),hits[:12],len(fp),fp[:5]))
