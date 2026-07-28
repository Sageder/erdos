"""fix1.py -- REPLACEMENTS for the grid points of scaleinv.py / bigw.py whose V fell
BELOW the dead-zone bound 3U-2 (those UNSATs were trivial geometry, not information).
Every V here is exactly 3U-2 (the shoulder), so the triple is not geometry-dead.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_lazy, solve_eager, verify
CASES = [(16,74,220),(18,83,247),(20,92,274),(22,101,301),(24,110,328),
         (28,140,418),(30,138,412),(46,212,634)]
for W,U,V in CASES:
    assert V >= 3*U-2, (W,U,V)
    t=time.time(); n=V-U
    r,w = (solve_eager([W,U,V]) if n<=85 else solve_lazy([W,U,V], time_cap=2000))
    if r=='SAT': verify([W,U,V],w)
    print(f"({W},{U},{V}) U/W={U/W:.2f} V/U={V/U:.2f} -> {r} [{time.time()-t:.0f}s]",flush=True)
