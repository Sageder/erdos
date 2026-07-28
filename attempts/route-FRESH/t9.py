"""Test Theorem 2: in a monotone-4-AP-free permutation, the set of left-to-right
maxima (records) contains no 3-term AP.  Finite version: no 3-AP u1<u2<u3 of
records with u3+delta <= N.   Also the general k-version: no (k-1)-AP of records."""
import sys, itertools
sys.path.insert(0,'/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos

def records(perm):
    R=[]; m=0
    for v in perm:
        if v>m: R.append(v); m=v
    return R

def bad_records(perm, K):
    """does the record set contain a (K-1)-AP whose next term is still <= N?"""
    N=len(perm); R=records(perm); S=set(R)
    for i in range(len(R)):
        for j in range(i+1,len(R)):
            d=R[j]-R[i]
            terms=[R[i]+t*d for t in range(K-1)]
            if all(t in S for t in terms) and terms[-1]+d<=N:
                return terms
    return None

# exhaustive check, small N, K=3,4,5
for N in range(4,10):
    for K in (3,4,5):
        cnt=0; viol=0
        for p in itertools.permutations(range(1,N+1)):
            if has_monotone_kap_pos(p,K): continue
            cnt+=1
            if bad_records(p,K) is not None: viol+=1
        print(f"N={N} K={K}: {cnt} K-AP-free perms, {viol} violate 'records have no (K-1)-AP-with-successor'")
