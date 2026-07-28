from audit_core import *
from sympy import factorint, primerange

def Rppp(n,k,P0):
    """Lemma R''' predicate, verbatim from LADDER.md 4.5."""
    # (a)
    for l in primerange(2,P0+1):
        if carries(n,n,l) < 2*sum(nu(n+j,l) for j in range(1,k+1)): return False
    # (b)
    for j in range(1,k+1):
        for l,e in factorint(n+j).items():
            if l<=P0: continue
            if e!=1: return False
            W=(n+j)//l
            if (W-1)%l < (l-1)//2: return False   # (l-1)/2 exact since l odd
    return True

for (k,P0,N) in [(2,4,60000),(2,5,60000),(3,5,60000),(3,6,60000),(3,7,60000),(4,8,60000)]:
    fp=[];cov=0;tot=0;certN=0
    covE=0;totE=0
    for n in range(1,N+1):
        r=Rppp(n,k,P0)
        if r: certN+=1
        s=in_S_ladder_criterion(n,k)
        if s:
            tot+=1
            if n%2==0: totE+=1
            if r:
                cov+=1
                if n%2==0: covE+=1
        if r and not s: fp.append(n)
    print(f"k={k} P0={P0} N={N}: #R'''={certN} falsepos={len(fp)} {fp[:8]}  coverage={cov}/{tot}  even-coverage={covE}/{totE}")
