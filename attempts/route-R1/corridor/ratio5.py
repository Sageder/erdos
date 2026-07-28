"""ratio5.py -- the decisive scale test for R1's Conjecture W: the PURE ratio-5
profile (U/W, V/U) = (5,5), which is R1's island corridor, at growing scale.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_lazy, verify
for W in (12, 10, 14, 16):
    U, V = 5*W, 25*W
    t=time.time(); r,w = solve_lazy([W,U,V], time_cap=7000)
    if r=='SAT': verify([W,U,V],w)
    print(f"({W},{U},{V}) ratio (5,5) -> {r} [{time.time()-t:.0f}s]",flush=True)
