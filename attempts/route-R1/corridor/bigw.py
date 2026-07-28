"""bigw.py -- chain-legal triples whose first cut is LARGE.
A 7-cut chain forces a chain-legal triple with W = V_5 >= 28.  These probe that
regime directly at the two ratio profiles that survive longest at small scale.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_lazy, solve_eager, verify
CASES = [(28,82,244),(28,84,250),(28,90,268),(28,100,298),(28,129,382),(28,140,418),
         (24,110,325),(22,101,299),(46,212,626),(30,138,408)]
for W,U,V in CASES:
    t=time.time()
    n=V-U
    r,w = (solve_eager([W,U,V]) if n<=85 else solve_lazy([W,U,V], time_cap=1500))
    if r=='SAT': verify([W,U,V],w)
    print(f"({W},{U},{V}) U/W={U/W:.2f} V/U={V/U:.2f} -> {r} [{time.time()-t:.0f}s]",flush=True)
