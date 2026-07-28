import time, sys
from nu import nu
sys.path.insert(0,'/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
K=int(sys.argv[1]); Ls=[int(x) for x in sys.argv[2].split(',')]; Ns=[int(x) for x in sys.argv[3].split(',')]
print(f"nu_L(N) for K={K}")
for L in Ls:
    for N in Ns:
        if N<L: continue
        t=time.time(); n,perm = nu(L,N,K=K)
        assert not has_monotone_kap_pos(perm,K)
        assert max(perm.index(v) for v in range(1,L+1))+1 == n
        print(f"  L={L} N={N}: nu={n}   ({time.time()-t:.1f}s)  head={perm[:n]}", flush=True)
