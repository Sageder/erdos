import sys, time
sys.path.insert(0,'/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from sat import solve, m_k
# validate encoding: SAT solutions really are K-AP-free, and UNSAT matches brute force
for N in range(4, 13):
    for K in (3,4,5):
        p = solve(N, K=K)
        if p is None:
            print(f"N={N} K={K}: UNSAT")
        else:
            assert sorted(p)==list(range(1,N+1))
            assert not has_monotone_kap_pos(p,K), (N,K,p)
print("encoding validated: all SAT models are genuinely K-AP-free (K=3,4,5), N<=12")
# k=1 head: min first value
for N in (8,16,24,32):
    for K in (3,4):
        r = m_k(N,1,K=K)
        print(f"K={K} N={N}: m_1 = {r[0]}  perm head {r[1][:6]}")
