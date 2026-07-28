"""Large-scale independent false-positive hunt for Lemma R''' (and the P0>=2k hypothesis)."""
import sys
from audit_core import carries, nu, in_S_ladder_criterion
from sympy import primerange

N=int(sys.argv[1]) if len(sys.argv)>1 else 1000000
# smallest prime factor sieve
spf=list(range(N+8))
i=2
while i*i<=N+7:
    if spf[i]==i:
        for m in range(i*i,N+8,i): 
            if spf[m]==m: spf[m]=i
    i+=1
def fac(m):
    d={}
    while m>1:
        p=spf[m]; e=0
        while m%p==0: m//=p; e+=1
        d[p]=e
    return d

def Rppp(n,k,P0,smallpr):
    for l in smallpr:
        if carries(n,n,l) < 2*sum(nu(n+j,l) for j in range(1,k+1)): return False
    for j in range(1,k+1):
        for l,e in fac(n+j).items():
            if l<=P0: continue
            if e!=1: return False
            if ((n+j)//l-1)%l < (l-1)//2: return False
    return True

for (k,P0) in [(2,4),(3,6),(4,8),(5,10),(6,12),(3,4),(4,5),(5,8)]:
    smallpr=list(primerange(2,P0+1))
    cert=0; fp=[]
    for n in range(2,N+1):
        if Rppp(n,k,P0,smallpr):
            cert+=1
            if not in_S_ladder_criterion(n,k): fp.append(n)
    tag="  <-- P0 < 2k (hypothesis VIOLATED)" if P0<2*k else ""
    print(f"k={k} P0={P0} n<={N}: certified={cert} FALSE POSITIVES={len(fp)} {fp[:6]}{tag}")
