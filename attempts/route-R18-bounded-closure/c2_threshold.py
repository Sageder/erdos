import sys, time
sys.path.insert(0,'/home/user/erdos/attempts/route-R18-bounded-closure')
from sat_height import solve
# NEW plain-family extinction threshold at C=2 (convention pos(v) <= ceil(C v)), two engines
for N in (68,70,72,74,76,78,80):
    for eng in ("cadical","glucose"):
        st,dt,perm = solve(N, K=None, C=2, solver=eng)
        print(f"plain C=2 N={N} [{eng}]: {st} ({dt:.1f}s)", flush=True)
        if st=="SAT": break
