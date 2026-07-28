"""scaleinv.py -- SCALE-INVARIANCE test of the first-cut law.

Conjecture W (R1) says the ratio-~5 corridor survives at every scale.  If the cut
system were scale-invariant, feasibility of (W,U,V) would depend only on the ratios
(U/W, V/U).  This tests ratio profiles along a geometric family of scales:

  profile A = (4.60, 2.96)  -- ratios of the VERIFIED depth-6 chain step (10,46,136)
  profile B = (5.00, 5.00)  -- R1's pure ratio-5 point {5,25,125}
  profile C = (3.00, 3.00)  -- the geometric ratio-3 family (known dead at scale)

A death at some scale = the corridor closes at that scale; survival at growing scale
= evidence for Conjecture W (EVIDENCE ONLY -- Remark 27's blind spot applies).
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_eager, solve_lazy, verify


def run(name, triples):
    print(f"## profile {name}", flush=True)
    for W, U, V in triples:
        t = time.time()
        n = V - U
        r, w = (solve_eager([W, U, V]) if n <= 90
                else solve_lazy([W, U, V], time_cap=2400))
        ok = ''
        if r == 'SAT':
            verify([W, U, V], w)
            ok = ' (witness verified)'
        print(f"   ({W},{U},{V})  U/W={U/W:.2f} V/U={V/U:.2f}  -> {r}{ok}  "
              f"[{time.time()-t:.0f}s]", flush=True)


A = [(2, 9, 27), (3, 14, 41), (4, 18, 53), (5, 23, 68), (6, 28, 83), (8, 37, 110),
     (10, 46, 136), (12, 55, 163), (14, 64, 190), (16, 74, 219), (18, 83, 246),
     (20, 92, 272)]
B = [(2, 10, 50), (3, 15, 75), (4, 20, 100), (5, 25, 125), (6, 30, 150),
     (8, 40, 200), (10, 50, 250), (12, 60, 300), (14, 70, 350), (16, 80, 400)]
C = [(2, 6, 18), (3, 9, 27), (4, 12, 36), (6, 18, 54), (8, 24, 72), (10, 30, 90)]

if __name__ == "__main__":
    run("A ratios (4.6, 2.96)", A)
    run("B ratios (5, 5)", B)
    run("C ratios (3, 3)", C)
