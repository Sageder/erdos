"""d6map.py -- the DEPTH-6 feasible set over the prefix [1,2,4,10].
For each V5 with [1,2,4,10,V5] feasible, scan V6 >= 3*V5-2 for feasibility of the
full 6-cut chain.  (R1/final's depth-6 grids only ever tested V5 in {28,30,35,40,60,90}.)
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_eager, solve_lazy, verify

def feas(cuts, tcap=600):
    n = cuts[-1] - cuts[-2]
    r, w = (solve_eager(cuts) if n <= 85 else solve_lazy(cuts, time_cap=tcap))
    if r == 'SAT':
        verify(cuts, w)
    return r

print("# V5 with [1,2,4,10,V5] feasible:", flush=True)
good5 = []
for V5 in range(28, 121):
    r = feas([1, 2, 4, 10, V5])
    if r == 'SAT':
        good5.append(V5)
print("  ", good5, flush=True)

print("# depth-6 continuations", flush=True)
hits = []
for V5 in good5:
    Vs = sorted({v for v in list(range(3*V5-2, 3*V5+4))
                 + [int(round(c*V5)) for c in (3.3,3.6,4.0,4.4,4.8,5.0,5.3,5.6,6.0)]
                 if v >= 3*V5-2 and v <= 700})
    row = []
    for V6 in Vs:
        r = feas([1, 2, 4, 10, V5, V6])
        if r == 'SAT':
            row.append(V6); hits.append((V5, V6))
    print(f"  V5={V5}: feasible V6 = {row}", flush=True)
print("# DEPTH-6 FEASIBLE (V5,V6) pairs over prefix [1,2,4,10]:", hits, flush=True)
