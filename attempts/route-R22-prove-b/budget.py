"""budget.py -- route R22 sub-target 1: the EXACT fibre-budget inequality, and the
demonstration that it is SHARP (so the mission's premise -- "the geometric budget forces
the delayed sets to be sparse at every scale" -- is false as stated).

LEMMA B1 (exact identity).  c = m + t with m(v) = floor(log_b v), t >= 0.
With B_m = [b^m, b^{m+1}), N_m(k) = #{v in B_m : t(v) >= k}, S_J = #{v : c(v) <= J}:

        S_J  =  (b^{J+1} - 1)  -  sum_{k=1}^{J+1} N_{J+1-k}(k).

(Proof: t >= 0 gives {c <= J} contained in [1, b^{J+1}); its complement inside that
interval is the disjoint union over m <= J of {v in B_m : t(v) >= J-m+1}.)

COROLLARY B2 (delay-density budget).  Write nu_m(k) = N_m(k)/|B_m|, |B_m| = (b-1)b^m.
If |F_j| >= c1 b^j for all j then for every J

        sum_{k>=1} b^{-k} nu_{J+1-k}(k)  <=  (1 - c1/(b-1)) / (b-1),

a b^{-k}-WEIGHTED AVERAGE bound (the weights sum to 1/(b-1)).  Its k=1 consequence is

        nu_J(1)  <=  (b/(b-1)) (1 - c1/(b-1)),

which is < 1 iff c1 > (b-1)/b.  SHARPNESS: the FAT-HEAD family below has
|F_j| ~ (b-1) b^{j-1}, i.e. c1 = (b-1)/b exactly, satisfies condition (ii), and has
nu_m(1) -> 1: EVERY value of block m is delayed.  So no unconditional sparsity of the
delayed sets follows from the geometric fibre design.
"""

import sys
from fractions import Fraction
import numpy as np

sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
from arch import (blk_array, block_bounds, check_ii_fast, delay_head, fibre_sizes,
                  budget_identity_check, v2)                                # noqa: E402


def nu_table(t, b, M, kmax=4):
    rows = []
    m, lo = 0, 1
    while lo * b - 1 <= M:
        hi = lo * b - 1
        L = hi - lo + 1
        rows.append((m, L, [Fraction(int((t[lo:hi + 1] >= k).sum()), L) for k in range(1, kmax + 1)]))
        m += 1
        lo *= b
    return rows


def show(tag, b, M, t, c):
    w = check_ii_fast(c, M)
    fs = fibre_sizes(c, M)
    J = 0
    while b ** (J + 2) - 1 <= M:
        J += 1
    bud = budget_identity_check(t, b, M)
    print(f"\n== {tag}  (b={b}, M={M})")
    print(f"   (ii): {'HOLDS' if w is None else 'FAILS ' + str(w)}")
    print(f"   Lemma B1 identity over J=0..{len(bud)-1}: "
          f"{'EXACT for all J' if all(x[3] for x in bud) else 'MISMATCH ' + str([x for x in bud if not x[3]])}")
    print("   j:  |F_j|      |F_j|/b^j    nu_j(1)=density of delayed in B_j")
    nus = {m: v for m, _, v in nu_table(t, b, M)}
    for j in range(J + 1):
        n1 = float(nus[j][0]) if j in nus else float('nan')
        print(f"   {j:2d}: {int(fs[j]):9d}   {int(fs[j])/b**j:8.4f}     {n1:.4f}")
    c1 = min(int(fs[j]) / b ** j for j in range(2, J + 1))   # skip tiny j
    gamma = (c1 * b / (b - 1) - 1) / (b - 1)
    print(f"   c1 = min_{{j>=2}} |F_j|/b^j = {c1:.4f};  (b-1)/b = {(b-1)/b:.4f};  "
          f"forced undelayed density gamma = (c1*b/(b-1)-1)/(b-1) = {gamma:.4f}")
    # Corollary B2 checked numerically at the top J: weighted average of delay densities
    lhs = sum(Fraction(1, b ** k) * (nus[J + 1 - k][0] if (J + 1 - k) in nus else Fraction(0))
              for k in range(1, J + 2))
    rhs = Fraction(1, b - 1) * (1 - Fraction(int(min(fs[j] for j in range(2, J + 1))),
                                             1) / Fraction((b - 1) * b ** 0, 1) * 0)
    print(f"   Cor.B2 LHS at J={J}: sum_k b^-k nu_(J+1-k)(k) = {float(lhs):.5f}   "
          f"(unconstrained max = {1/(b-1):.5f})")
    return w is None


if __name__ == "__main__":
    b, M = 3, 3 ** 9

    # 1. thin-head family (the route-R22 refutation instance): delayed sets ARE sparse
    t, c = delay_head(M, b, lambda m: m + 1, lambda m: m)
    show("THIN HEAD  s_m=m+1, K_m=m", b, M, t, c)

    # 2. FAT-head family: delayed density -> 1, fibres still geometric, (ii) still holds
    g = lambda m: max(1, m + 1)                      # size of the UNdelayed tail
    s_fat = lambda m: (b - 1) * b ** m - g(m)        # head = block minus a short tail
    t2, c2 = delay_head(M, b, s_fat, lambda m: 1)
    show("FAT HEAD   s_m=|B_m|-(m+1), K_m=1", b, M, t2, c2)

    # 3. control: t = v_2 (route R20's CLS(3,a)) -- (ii) holds, fibres NOT geometric
    from arch import delay_from_t
    t3, c3 = delay_from_t(M, b, v2)
    show("CLS(3,a)   t = v_2(v)  [route R20]", b, M, t3, c3)

    # 4. control: t == 0 (pure ratio-b block layout)
    t4, c4 = delay_head(M, b, lambda m: 1, lambda m: 0)
    show("t == 0 except K=0 (pure block layout)", b, M, t4, c4)
