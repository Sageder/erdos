import sys, itertools, time
sys.path.insert(0,'/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos, has_monotone_kap_general
def recs_of(seq):
    R=[];m=0
    for v in seq:
        if v>m: R.append(v); m=v
    return R
def viol_allAP(perm,K):
    """records of a|_S for EVERY AP S contain no (K-1)-AP with successor in S."""
    N=len(perm)
    for d in range(1,N+1):
        for c in range(1,d+1):
            S=list(range(c,N+1,d))
            if len(S)<K: continue
            sub=[v for v in perm if v in set(S)]
            R=recs_of(sub); Rs=set(R)
            for i in range(len(R)):
                for j in range(i+1,len(R)):
                    dd=R[j]-R[i]
                    if dd % d: continue
                    terms=[R[i]+t*dd for t in range(K-1)]
                    if all(t in Rs for t in terms) and terms[-1]+dd<=N:
                        return (d,c,terms)
    return None
for N in range(4,9):
    for K in (4,5):
        cnt=0;viol=0
        for p in itertools.permutations(range(1,N+1)):
            if has_monotone_kap_pos(p,K): continue
            cnt+=1
            if viol_allAP(p,K): viol+=1
        print(f"N={N} K={K}: {cnt} perms, {viol} violate the ALL-AP record theorem", flush=True)
