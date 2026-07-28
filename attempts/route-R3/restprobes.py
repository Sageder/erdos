"""restprobes.py — restarted probes after container restart.
1) single-block sweep for bases 5, 6, 8 (base 3,4 already UNSAT at D_3, verified twice)
2) 2-separated dyadic coupled probe at N=127 then 255
"""
import sys, time
import numpy as np
sys.path.insert(0, "/home/user/erdos/attempts/route-R3")
from singleblock import solve_block
from satprobe import probe_separated

for b, j in [(5, 2), (6, 2), (8, 1), (8, 2)]:
    L = b ** j
    t0 = time.time()
    st, order, sizes = solve_block(L, b, 1500)
    print(f"base {b} block D_{j}=[{L},{b*L}): {st} "
          f"(|4AP|={sizes[0]},|g3|={sizes[1]},|forced|={sizes[2]}) "
          f"({time.time()-t0:.1f}s)", flush=True)

for N, tl in [(127, 900), (255, 2700)]:
    t0 = time.time()
    st, data = probe_separated(2, N, tl)
    print(f"sep2 dyadic N={N}: {st} ({time.time()-t0:.1f}s)", flush=True)
    if st == "SAT":
        np.save(f"/home/user/erdos/attempts/route-R3/sat_sep2_{N}.npy", np.array(data))
        print("  saved solution", flush=True)
    elif st != "UNSAT":
        break
