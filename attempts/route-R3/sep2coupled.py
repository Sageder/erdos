"""sep2coupled.py — coupled CP-SAT probe: 2-separated dyadic orderings of [1..N]."""
import sys, time
import numpy as np
sys.path.insert(0, "/home/user/erdos/attempts/route-R3")
from satprobe import probe_separated

for N, tl in [(127, 1500), (255, 3000)]:
    t0 = time.time()
    st, data = probe_separated(2, N, tl)
    print(f"sep2 dyadic coupled N={N}: {st} ({time.time()-t0:.1f}s)", flush=True)
    if st == "SAT":
        np.save(f"/home/user/erdos/attempts/route-R3/sat_sep2_{N}.npy", np.array(data))
        print("saved model", flush=True)
    elif st != "UNSAT":
        break
