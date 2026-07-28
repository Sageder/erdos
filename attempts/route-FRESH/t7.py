import sys, time
sys.path.insert(0,'/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from profile import ProfileSolver
K=int(sys.argv[1]); L0=int(sys.argv[2]); Ns=[int(x) for x in sys.argv[3].split(',')]
print(f"lex-min profile (n_1..n_{L0}) for K={K}; lex-non-decreasing in N")
for N in Ns:
    t=time.time(); ps=ProfileSolver(N,K=K,L0=min(L0,N))
    prof=ps.lexmin_profile()
    p=ps.perm(); assert not has_monotone_kap_pos(p,K)
    ranks=[p.index(v)+1 for v in range(1,min(L0,N)+1)]
    print(f"  N={N:3d}: {[prof[v] for v in sorted(prof)]}   ({time.time()-t:.1f}s)")
    print(f"        witness head: {p[:max(x for x in prof.values() if x)]}", flush=True)
    ps.close()
