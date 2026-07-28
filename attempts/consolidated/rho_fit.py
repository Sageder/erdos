"""rho_fit.py — the decision-relevant statistic requested by the coordinator:
how does rho(N) := min over monotone-4-AP-free permutations sigma of [1..N] of
max_v pos_sigma(v)/v grow with N?

rho is nondecreasing in N (restriction only lowers positions), so it is fully
determined by the staircase of crossing points
    N*(C) := least N with rho(N) > C   (= extinction level of the C-bounded tree).

All N*(C) below are EXACT complete enumerations reproduced independently in
this directory (attempts/consolidated/tamedfs.c), agreeing level-by-level with
route R9's census.c and route R4's fast2.
"""
import math
from fractions import Fraction

# (C, N*(C)) -- exact complete enumerations
pts = [
    (Fraction(1, 1), 4),
    (Fraction(5, 4), 4),
    (Fraction(4, 3), 10),
    (Fraction(11, 8), 10),
    (Fraction(3, 2), 15),
    (Fraction(8, 5), 18),
    (Fraction(13, 8), 21),
    (Fraction(5, 3), 26),
    (Fraction(7, 4), 31),
    (Fraction(9, 5), 34),
    (Fraction(15, 8), 37),
]

print("EXACT crossing points N*(C) (k=4, plain, pos(v) <= floor(C v)):")
for C, N in pts:
    print(f"   C = {str(C):6s} = {float(C):.4f}   N*(C) = {N:3d}   "
          f"=> rho(N) <= {float(C):.4f} for N <= {N-1}, rho({N}) > {float(C):.4f}")
print("   C = 2      = 2.0000   N*(2) in [57, 85]  (witness at N=56 verified here; "
      "eager SAT UNSAT at N=85, cadical+glucose)")
print("   C = 3      = 3.0000   N*(3) >= 76        (witness at N=75 verified here)")

# least-squares fit ln N* = ln a + b C over the exact points with distinct C
xs = [float(C) for C, N in pts]
ys = [math.log(N) for C, N in pts]
n = len(xs)
mx, my = sum(xs) / n, sum(ys) / n
b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
la = my - b * mx
ss_tot = sum((y - my) ** 2 for y in ys)
ss_res = sum((y - (la + b * x)) ** 2 for x, y in zip(xs, ys))
print(f"\nleast squares over the 11 exact points:  N*(C) ~ {math.exp(la):.4f} * exp({b:.4f} C)"
      f"   (R^2 = {1 - ss_res/ss_tot:.4f})")
print(f"   predictions: N*(2) = {math.exp(la+2*b):6.1f}   [truth in 57..85]")
print(f"                N*(3) = {math.exp(la+3*b):6.1f}   [truth >= 76]")
print(f"                N*(4) = {math.exp(la+4*b):6.1f}")
print(f"   inverse: rho(N) ~ {(-la)/b:.3f} + {1/b:.3f} ln N")

# same fit on the last 6 points only (large-C regime)
xs2, ys2 = xs[-6:], ys[-6:]
n2 = len(xs2); mx2, my2 = sum(xs2)/n2, sum(ys2)/n2
b2 = sum((x-mx2)*(y-my2) for x, y in zip(xs2, ys2)) / sum((x-mx2)**2 for x in xs2)
la2 = my2 - b2*mx2
print(f"\nfit restricted to C in [1.6, 1.875]:  N*(C) ~ {math.exp(la2):.4f} * exp({b2:.4f} C)"
      f";  predicts N*(2) = {math.exp(la2+2*b2):.1f}, N*(3) = {math.exp(la2+3*b2):.1f}, "
      f"N*(4) = {math.exp(la2+4*b2):.1f}")
print(f"   inverse: rho(N) ~ {(-la2)/b2:.3f} + {1/b2:.3f} ln N")

# ---------------- k = 5 calibration ----------------
print("\n" + "=" * 78)
print("CALIBRATION AGAINST k = 5, WHERE THE INFINITE ANSWER IS KNOWN")
print("=" * 78)
k5 = [(Fraction(5, 4), 13), (Fraction(4, 3), 35)]
for C, N in k5:
    print(f"   k=5  C = {str(C):5s}  N*_5(C) = {N}   (exact complete enumeration, this dir)")
print("   k=5  C >= 4          N*_5(C) = +INFINITY  -- THEOREM: route R2 / CORE Thm 21")
print("        'Construction A' is a 5-AP-free permutation of N with sup_v pos(v)/v = 4")
print("        (verified here to N = 65535: max pos(v)/v = 3.999878, limsup = 4).")
xs5 = [float(C) for C, N in k5]; ys5 = [math.log(N) for C, N in k5]
b5 = (ys5[1] - ys5[0]) / (xs5[1] - xs5[0]); la5 = ys5[0] - b5 * xs5[0]
print(f"\n   two-point exponential fit for k=5:  N*_5(C) ~ {math.exp(la5):.4g} exp({b5:.3f} C)")
print(f"      -> predicts a FINITE N*_5(4) = {math.exp(la5+4*b5):.3g}, which is FALSE.")
print("      LESSON: an exponential fit to small-C extinction data cannot detect a")
print("      divergence at finite C*.  In the one case where C* is known (k=5, C* <= 4)")
print("      the fit gives no warning whatsoever.  Therefore the k=4 fit")
print("      N*(C) ~ a e^{bC} is NOT evidence that rho(N) -> infinity.")
