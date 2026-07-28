"""measure_gamma.py -- the ledger constant gamma = (sum_j tau_j)/N^2 on known objects.

REDUCTION (REPORT.md Prop 2):  CORE Theorem 12's ledger proves LP-inc(C) exactly when
one can prove the DEMAND bound   sum_{j=1}^N tau_j >= gamma N^2 - o(N^2)
for all increasing-4-AP-free permutations of [1..N], with C < 1/(2 - 2 gamma).

  gamma = 1/2      <->  C < 1     (trivial tau_j >= j)
  gamma = 5/9      <->  C < 9/8   (CORE Theorem 12)
  gamma = 31/43    <->  C < 43/24 (route R6's machine-assisted level)
  gamma = 3/4      <->  C < 2
  gamma = 5/6      <->  C < 3     (would match the Theorem-14 ceiling)

Any TRUE demand bound must hold on every increasing-4-AP-free permutation; this script
measures gamma on the extremal candidates.
"""

import sys
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
from r19lib import (triadic, sigma_parity, geom_blocks, ledger_stats,
                    has_inc_4ap, has_dec_4ap, pos_array, A_sizes)


def gamma_of(perm):
    st = ledger_stats(perm)
    return st


def show(name, perm, extra=""):
    st = ledger_stats(perm)
    N = st["N"]
    pos = pos_array(perm)
    prof = max(Fraction(pos[v], v) for v in range(1, N + 1))
    print(f"{name:28s} N={N:6d}  gamma={st['gamma']:.5f}  beta={st['beta']:.5f} "
          f" inc4AP={has_inc_4ap(perm)} dec4AP={has_dec_4ap(perm)} "
          f" max pos(v)/v = {float(prof):.4f}  {extra}")
    return st


if __name__ == "__main__":
    print("== triadic (CORE Thm 14 extremal object for increasing-only methods) ==")
    for K in range(1, 9):
        N = 3 ** K - 1                     # exactly complete blocks
        show("triadic  N=3^k-1", triadic(N))
    print("  (theory: gamma -> 3/4 = 0.75 exactly along N = 3^k - 1)")

    print("\n== triadic at generic N (block partially filled) ==")
    for N in (100, 200, 400, 800, 1600, 3200):
        show("triadic", triadic(N))

    print("\n== reversed geometric blocks, other ratios ==")
    for r in (2.0, 2.5, 3.0, 3.5, 4.0, 6.0, 9.0):
        N = 3000
        p = geom_blocks(N, r)
        show(f"geom ratio {r}", p)

    print("\n== parity (sigma_N): 3-AP-free, hence inc-4-AP-free ==")
    for K in range(3, 14):
        N = 2 ** K
        show("parity 2^k", sigma_parity(N))

    print("\n== parity at generic N ==")
    for N in (100, 300, 1000, 3000):
        show("parity", sigma_parity(N))

    print("\n== identity / reverse sanity ==")
    N = 1000
    show("identity", list(range(1, N + 1)))
    show("reverse", list(range(N, 0, -1)))
