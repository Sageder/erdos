import sys, time
sys.path.insert(0,'/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from profile import ProfileSolver
from nu import nu
# validate ProfileSolver against nu(): nu_L(N) = min n with profile n_v=n for v<=L
for (L,N,K) in [(2,16,3),(3,16,3),(4,24,3),(2,24,4),(4,32,4),(5,24,4)]:
    ps = ProfileSolver(N,K=K,L0=L)
    n = L
    while not ps.sat({v:n for v in range(1,L+1)}): n+=1
    p = ps.perm(); assert not has_monotone_kap_pos(p,K)
    n2,_ = nu(L,N,K=K)
    assert n==n2, (L,N,K,n,n2)
    ps.close()
print("ProfileSolver validated against nu() on 6 cases")
