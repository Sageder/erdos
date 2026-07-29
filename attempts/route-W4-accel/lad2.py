"""lad2.py -- single-shot pair test at a chosen horizon multiple.  Usage:
   python3 lad2.py W:U:mult ...
Only UNSAT is load-bearing (it is a theorem: no monotone-4-AP-free permutation of
N has both W and U as cuts).  SAT means "the necessary system survives THIS
horizon", nothing more.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys

for spec in sys.argv[1:]:
    a, b, c = spec.split(':')
    W, U, m = int(a), int(b), float(c)
    M = int(m * U)
    t0 = time.time()
    S = wsys.Sys((W, U), M)
    v, o = wsys.solve_lazy(S, time_cap=3000)
    if v == 'GEOM_DEAD':
        v = 'UNSAT'
    print(f"  N({W},{U},{M}) rho={U/W:.2f} horizon={m}U -> {v} "
          f"[{time.time()-t0:.0f}s]", flush=True)
