"""midgrowth.py — is the MID (middle-digit) delay family D1-compatible?

MID(b, frac): c(v) = floor(log_b v) + v_2( floor(v / 2^{floor(frac*bitlen(v))}) ).
Its delayed sets {t >= k} are 'middle digit window = 0' sets, which meet EVERY residue
class modulo every m -- the property Corollary R21-5 shows congruence-determined delays
(all p-adic valuations, all shifts, all Boolean combinations of congruences) can never
have.  Measured here: the minimum over APs (q <= 8) of the maximal relative displacement,
as M grows, for several within-class orders.  Growth of this minimum with M is the
signature of D1-compatibility (unbounded displacement on every AP).

CAVEAT (stated in the report): MID violates condition (ii) -- it has 4-APs with strictly
increasing class sequence -- so it is NOT a legal class architecture.  It is measured
here only to show that the two requirements are individually achievable and that the
obstruction is their conjunction.
"""

import sys, random
from fractions import Fraction

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_elements, ranks_in_subset                 # noqa: E402
from rules import MID, CLS, check_ii                            # noqa: E402
from tamebound import emit, tame_aps                            # noqa: E402


def min_ap_disp(c, M, qmax=8, within='dec', rng=None):
    perm = emit(c, M, within, rng)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    worst, who = None, None
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(M, q, r)
            if len(el) < 4:
                continue
            rk = ranks_in_subset(pos, el)
            d = max(Fraction(rk[n - 1], n) for n in range(1, len(el) + 1))
            # tail-robust statistic: the largest displacement attained at index >= L/8
            lo = max(1, len(el) // 8)
            dt = max(Fraction(rk[n - 1], n) for n in range(lo, len(el) + 1))
            if worst is None or dt < worst:
                worst, who = dt, (q, r)
    return worst, who


if __name__ == "__main__":
    rng = random.Random(77)
    print("family        M      min over APs(q<=8) of max_{n>=L/8} pos_P(n)/n   #tameAPs")
    for name, c in (("CLS(3,a)", CLS(3)), ("CLS(5,a)", CLS(5)),
                    ("MID(3,1/2)", MID(3, Fraction(1, 2))),
                    ("MID(3,2/3)", MID(3, Fraction(2, 3)))):
        for M in (200, 400, 800, 1600, 3200):
            d, who = min_ap_disp(c, M, 8, 'dec', rng)
            t = len(tame_aps(c, M))
            print(f"{name:12s} {M:5d}   {float(d):8.3f}  (AP q={who[0]},r={who[1]})   {t}",
                  flush=True)
        print()
    print("(ii) status:", {n: (check_ii(c, 200) is None)
                          for n, c in (("CLS(3,a)", CLS(3)),
                                       ("MID(3,1/2)", MID(3, Fraction(1, 2))))})
