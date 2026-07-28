from audit_core import *
from sympy import primerange, isprime
import math

def smooth_part(m,P0):
    c=1
    for l in primerange(2,P0+1):
        while m%l==0: m//=l; c*=l
    return c,m

def cond_ii(n,k,P0):
    """LADDER Lemma R_k class condition (ii), stated as a property of n itself."""
    for l in primerange(2,P0+1):
        v=[nu(n+j,l) for j in range(1,k+1)]
        V=sum(v); D=1+max(v)
        dg=digits(n,l)
        for pos in range(D,D+2*V+1):
            d=dg[pos] if pos<len(dg) else 0
            if d < -(-l//2): return False
    return True

def lemmaRk_hyp(n,k,P0=None,require_ii=True):
    """Full Lemma R_k hypotheses for this n (class conditions expressed pointwise)."""
    if P0 is None: P0=2*k
    if require_ii and not cond_ii(n,k,P0): return False
    for j in range(1,k+1):
        c,u=smooth_part(n+j,P0)
        f=factorint(u)
        if sum(f.values())!=2 or len(f)!=2: return False   # r != s, both prime
        p1,p2=sorted(f)
        ok=False
        for r,s in ((p1,p2),(p2,p1)):
            if not(r>max(P0,c) and s>max(P0,c)): continue
            if not(c*s-1 < r <= 2*c*s-1): continue
            if (c*r)%s < (s+1)//2: continue
            ok=True
        if not ok: return False
    return True

if __name__=="__main__":
    import sys
    N=int(sys.argv[1]) if len(sys.argv)>1 else 200000
    for k in (2,3):
        hits=[];fp=[]
        for n in range(1,N+1):
            if lemmaRk_hyp(n,k):
                hits.append(n)
                if not in_S_ladder_criterion(n,k): fp.append(n)
        print(f"Lemma R_k k={k} P0={2*k} n<={N}: #hyp-satisfying={len(hits)} falsepos={len(fp)} {fp[:10]}")
        print("   first hits:",hits[:15])
        # also: WITHOUT condition (ii)  -> should break
        hits2=[];fp2=[]
        for n in range(1,N+1):
            if lemmaRk_hyp(n,k,require_ii=False):
                hits2.append(n)
                if not in_S_ladder_criterion(n,k): fp2.append(n)
        print(f"   drop (ii): #={len(hits2)} falsepos={len(fp2)} {fp2[:10]}")
