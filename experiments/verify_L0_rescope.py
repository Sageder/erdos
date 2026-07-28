"""Independent check of R13's finding L0: the C_ell-form of the residual target is FALSE
(vanishing density), while the exact-criterion form has positive density.

Claims tested, over successive ranges, restricted to n whose window {n+1, n+2} is n^b-smooth:
 (A) fraction satisfying C_ell at EVERY prime ell > P0 dividing the window
     [C_ell: ((n+j)/ell - 1) mod ell >= (ell-1)/2] -- predicted to DECAY like (log x)^{-1/2};
 (B) fraction satisfying the EXACT criterion kappa_ell(n) >= 2 nu_ell(n+j) at every such ell
     -- predicted to be a stable positive proportion.
Run at b = 1/2 and b = 0.35.  Exact integer arithmetic.
"""
import sys, math
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import carries_add
from sympy import factorint

P0 = 4
RANGES = [(100000, 400000), (400000, 800000), (800000, 1600000)]

def analyse(lo, hi, b):
    smooth = allC = allExact = 0
    for n in range(lo, hi):
        facts = []
        ok_smooth = True
        thr = math.exp(b * math.log(n))
        for j in (1, 2):
            for p, e in factorint(n + j).items():
                facts.append((p, e, j))
                if p > thr:
                    ok_smooth = False
            if not ok_smooth:
                break
        if not ok_smooth:
            continue
        smooth += 1
        cok = True
        for p, e, j in facts:
            if p <= P0:
                continue
            if e != 1 or ((n + j) // p - 1) % p < (p - 1) // 2:
                cok = False
                break
        allC += cok
        eok = True
        for p, e, j in facts:
            if p <= P0:
                continue
            dem = 2 * sum(f[1] for f in facts if f[0] == p)
            if carries_add(n, n, p) < dem:
                eok = False
                break
        allExact += eok
    return smooth, allC, allExact

for b in (0.5, 0.35):
    print(f"--- b = {b} (window n^b-smooth), P0 = {P0}")
    for lo, hi in RANGES:
        s, c, e = analyse(lo, hi, b)
        if s == 0:
            print(f"  [{lo},{hi}): no smooth pairs")
            continue
        print(f"  [{lo},{hi}): smooth pairs {s};  all-C_ell {c/s:.4f};  exact-criterion {e/s:.4f}")
print()
print("Expect: all-C_ell DECAYING (~(log x)^{-1/2}); exact-criterion STABLE and positive.")
