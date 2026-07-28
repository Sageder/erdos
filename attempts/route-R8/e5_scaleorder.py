"""e5_scaleorder.py — pure-cross AP obstructions for annulus macros (route R8 core experiment).

Setting: partition values into annuli A_m = {v : b^m <= |v| < b^(m+1)} (base b; A_0 also
contains 0 and the units).  A macro construction assigns each annulus (as a contiguous position
block) to a slot; the slot order is a total order on annuli.  Within-annulus order is free.
For an AP whose ADJACENT terms always lie in DISTINCT annuli ("pure-cross"), every adjacent
position comparison is a constant of the slot order; the AP is monotone iff the annulus sequence
is slot-monotone.  Such APs cannot be broken by within-annulus arrangements.

Questions answered by machine here (then proved by hand in REPORT.md where UNSAT):
  For each (side, base, k): does there EXIST a total order on annuli making every realizable
  pure-cross annulus pattern non-monotone?
    side = N (t >= 1)  or  Z (t arbitrary; APs may cross 0)
  Expected highlights:
    N, base 3, k = 4: NO pure-cross 4-APs at all ((t+3d)/(t+d) < 3) -> trivially satisfiable.
    N, base 2, k = 4: pure-cross patterns exist (1, 6, 11, 16); is some order still OK?
    Z, any base, k = 4: crossing-zero pure-cross 4-APs; UNSAT expected -> impossibility lemma.
    Z, base 2/3, k = 5: alternating-slot order should work (matches e4_zjoint SAT).
Exact enumeration of patterns for values up to VCAP; SAT over pairwise order vars with
transitivity.  UNSAT within scales <= S is monotone in S (more scales, more constraints), and
already UNSAT at S proves impossibility for all macros using these annuli.
"""

import sys
from itertools import combinations
from pysat.solvers import Cadical153


def scale_of(v, b):
    a = abs(v)
    if a <= b - 1:
        return 0 if a <= 0 else len_scale(a, b)
    return len_scale(a, b)


def len_scale(a, b):
    # m with b^m <= a < b^(m+1); a >= 1
    m = 0
    x = 1
    while a >= x * b:
        x *= b
        m += 1
    return m


def scale0(v, b):
    """scale with 0 mapped to annulus 0."""
    a = abs(v)
    if a == 0:
        return 0
    return len_scale(a, b)


def pure_cross_patterns(k, b, side, S):
    """All annulus sequences (s_1..s_k) of realizable pure-cross k-APs with every |term| <
    b^(S+1); adjacent terms in distinct annuli."""
    V = b ** (S + 1) - 1
    pats = {}
    tlo = 1 if side == "N" else -V
    maxd = (V - tlo) // (k - 1) if side == "N" else (2 * V) // (k - 1)
    for d in range(1, maxd + 1):
        for t in range(tlo, V - (k - 1) * d + 1):
            terms = [t + j * d for j in range(k)]
            if side == "Z" and any(abs(x) > V for x in terms):
                continue
            ss = [scale0(x, b) for x in terms]
            if any(ss[j] == ss[j + 1] for j in range(k - 1)):
                continue
            key = tuple(ss)
            if key not in pats:
                pats[key] = (t, d)
    return pats


def slot_order_sat(pats, S):
    """SAT: total order on scales 0..S; for each pattern, forbid slot-monotone (both ways).
    Returns a satisfying order (list of scales in slot order) or None."""
    vid = {}
    ctr = [0]

    def var(a, bb):
        x, y = (a, bb) if a < bb else (bb, a)
        if (x, y) not in vid:
            ctr[0] += 1
            vid[(x, y)] = ctr[0]
        lit = vid[(x, y)]
        return lit if (a, bb) == (x, y) else -lit

    cnf = []
    for a, bb, c in combinations(range(S + 1), 3):
        cnf.append([-var(a, bb), -var(bb, c), var(a, c)])
        cnf.append([var(a, bb), var(bb, c), -var(a, c)])
    for ss in pats:
        # monotone increasing in slots: var(ss[j], ss[j+1]) for all j -- forbid conjunction
        cnf.append([-var(ss[j], ss[j + 1]) for j in range(len(ss) - 1)])
        cnf.append([var(ss[j], ss[j + 1]) for j in range(len(ss) - 1)])
    with Cadical153(bootstrap_with=cnf) as s:
        if not s.solve():
            return None
        model = set(l for l in s.get_model() if l > 0)
    import functools

    def cmp(a, bb):
        if a == bb:
            return 0
        x, y = (a, bb) if a < bb else (bb, a)
        before = vid[(x, y)] in model
        return (-1 if before else 1) if (a, bb) == (x, y) else (1 if before else -1)

    return sorted(range(S + 1), key=functools.cmp_to_key(cmp))


if __name__ == "__main__":
    for side in ("N", "Z"):
        for b in (2, 3, 4):
            for k in (3, 4, 5, 6):
                S = {2: 10, 3: 7, 4: 6}[b]
                pats = pure_cross_patterns(k, b, side, S)
                if not pats:
                    print(f"{side} base {b} k={k}: NO pure-cross patterns up to scale {S} "
                          f"-> annulus macro unconstrained at pure-cross level")
                    continue
                order = slot_order_sat(pats, S)
                ex = list(pats.items())[:3]
                if order is None:
                    print(f"{side} base {b} k={k}: {len(pats)} patterns, scales<= {S}: "
                          f"UNSAT -- NO slot order works (impossibility). e.g. {ex}")
                else:
                    print(f"{side} base {b} k={k}: {len(pats)} patterns, scales<= {S}: SAT, "
                          f"e.g. slot order {order}")
    sys.exit(0)
