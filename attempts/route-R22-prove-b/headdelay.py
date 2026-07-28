"""headdelay.py -- route R22 main result: an explicit REFUTATION of Conjecture R21-C
(and of its three natural repairs).

THE HEAD-DELAY ARCHITECTURE.  Fix b >= 3.  For each block B_m = [b^m, b^{m+1}) let
H_m := [b^m, b^m + s_m)  (a nonempty proper INITIAL SEGMENT of B_m) and let (K_m) be a
NON-DECREASING sequence of positive integers.  Put

        t(v) = K_m  if v in H_m,      t(v) = 0 otherwise      (m = floor(log_b v)),
        c(v) = floor(log_b v) + t(v).

Claims verified here (exact integer arithmetic, all 4-APs with largest term <= M):
  (a) t >= 0 and every fibre is finite, with |F_j| = |B_j| - s_j + [s_m if m+K_m = j] ;
      so |F_j| / b^j is bounded above and below -- a GEOMETRIC fibre design.
  (b) c satisfies condition (ii).
  (c) if s_m -> oo and K_m -> oo then, along EVERY infinite AP P,
        - t|_P is unbounded and takes the value 0 infinitely often  (so t is not
          constant on any infinite AP -> Conjecture R21-C is FALSE);
        - c|_P has infinitely many strict descents (so no AP is TAME -> the repair
          "some AP is tame", which is what Prop. 29 needs, is FALSE);
        - the coarse displacement (1 + #{m : c(p_m) < c(p_n)})/n, a LOWER bound for
          pos_P(n)/n valid for every within-class order, is unbounded (so design
          principle D1 HOLDS for this architecture).
  (d) both hypotheses are necessary: moving the head to the interior/end of a block, or
      making (K_m) decrease somewhere, breaks (ii).
"""

import sys, json
from fractions import Fraction
import numpy as np

sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
from arch import (blk_array, block_bounds, check_ii_fast, check_ii_slow,
                  count_ii_violations, delay_head, fibre_sizes,
                  budget_identity_check)                                  # noqa: E402


def build(M, b, s_of_m, K_of_m):
    return delay_head(M, b, s_of_m, K_of_m)


def ap_descents(c, M, q, r, lo=1):
    """number of strict descents of c along P = {r + q n} inside [lo..M]."""
    el = [v for v in range(r + q, M + 1, q) if v >= lo]
    return sum(1 for i in range(len(el) - 1) if c[el[i + 1]] < c[el[i]]), len(el)


def ap_t_profile(t, M, q, r):
    el = list(range(r + q, M + 1, q))
    vals = [int(t[v]) for v in el]
    return min(vals), max(vals), vals.count(0)


def coarse_disp(c, M, q, r):
    """max_n (1 + #{m : c(p_m) < c(p_n)})/n over the AP P inside [1..M].
    This is a lower bound for pos_P(n)/n valid for EVERY within-class emission order,
    because every P-element in a strictly smaller class is emitted earlier."""
    el = list(range(r + q, M + 1, q))
    cs = np.array([c[v] for v in el], dtype=np.int64)
    order = np.argsort(cs, kind='stable')
    # rank_below[i] = #{m : cs[m] < cs[i]}
    srt = cs[order]
    below = np.searchsorted(srt, cs, side='left')
    best = Fraction(0)
    arg = None
    for i, v in enumerate(el):
        f = Fraction(int(below[i]) + 1, i + 1)
        if f > best:
            best, arg = f, (i + 1, v, int(cs[i]))
    return best, arg


def run(b, s_of_m, K_of_m, M, tag, verbose=True):
    t, c = build(M, b, s_of_m, K_of_m)
    out = {'tag': tag, 'b': b, 'M': M}

    # (b) condition (ii)
    w = check_ii_fast(c, M)
    out['ii_holds'] = (w is None)
    out['ii_witness'] = w
    inc, dec = count_ii_violations(c, M)
    out['ii_violation_counts'] = (inc, dec)

    # (a) fibre design
    fs = fibre_sizes(c, M)
    Jfull = 0
    while b ** (Jfull + 2) - 1 <= M:
        Jfull += 1
    ratios = [(j, int(fs[j]), float(Fraction(int(fs[j]), b ** j))) for j in range(Jfull + 1)]
    out['fibres'] = ratios

    # budget identity (Lemma B1)
    out['budget'] = budget_identity_check(t, b, M)
    out['budget_ok'] = all(x[3] for x in out['budget'])

    if verbose:
        print(f"--- {tag}: b={b}, M={M}")
        print(f"    (ii): {'HOLDS' if w is None else 'FAILS ' + str(w)}   "
              f"(strictly-inc 4-APs: {inc}, strictly-dec: {dec})")
        print(f"    fibres |F_j|/b^j for j<= {Jfull}: "
              + ", ".join(f"{j}:{r:.3f}" for j, _, r in ratios))
        print(f"    Lemma B1 budget identity: {'OK' if out['budget_ok'] else 'MISMATCH'} "
              f"({len(out['budget'])} values of J)")
    return t, c, out


if __name__ == "__main__":
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 3 ** 9

    # main instance: s_m = m+1 (-> oo), K_m = m (non-decreasing, -> oo)
    s_of_m = lambda m: m + 1
    K_of_m = lambda m: m
    t, c, out = run(B, s_of_m, K_of_m, M, "HEAD(s=m+1, K=m)")

    print("\n    delay levels present:", sorted(set(int(x) for x in t[1:M + 1])))

    # (c) no tame AP / t unbounded / D1
    print("\n    AP diagnostics (P = {r+qn}), tail = second half of [1..M]:")
    print("      q  r   descents  |P|   min t  max t   #t=0   coarse-disp  at (n,v,class)")
    rows = []
    for q in range(1, 9):
        for r in range(q):
            de, L = ap_descents(c, M, q, r, lo=1)
            mn, mx, z = ap_t_profile(t, M, q, r)
            cd, arg = coarse_disp(c, M, q, r)
            rows.append((q, r, de, L, mn, mx, z, cd, arg))
    for q, r, de, L, mn, mx, z, cd, arg in rows:
        if r < 2 or q <= 2:
            print(f"      {q:2d} {r:2d}  {de:8d} {L:5d}  {mn:5d} {mx:5d} {z:6d}   "
                  f"{float(cd):10.2f}  {arg}")
    print(f"    ALL {len(rows)} APs with q<=8: min #descents = {min(x[2] for x in rows)}, "
          f"min max-t = {min(x[5] for x in rows)}, min #(t=0) = {min(x[6] for x in rows)}, "
          f"min coarse-disp = {float(min(x[7] for x in rows)):.2f}")

    # (d) necessity of the two hypotheses
    print("\n    necessity checks:")
    from arch import blk_array as _ba
    # (d1) head moved to the END of each block
    tt = np.zeros(M + 1, dtype=np.int64)
    m, lo = 0, 1
    while lo <= M:
        hi = min(M, lo * B - 1)
        s = min(s_of_m(m), hi - lo + 1)
        tt[hi - s + 1:hi + 1] = K_of_m(m)
        m += 1
        lo *= B
    cc = _ba(M, B) + tt
    cc[0] = 0
    print(f"      tail-segment delay : (ii) {'HOLDS' if check_ii_fast(cc, M) is None else 'FAILS ' + str(check_ii_fast(cc, M))}")
    # (d2) head, but K decreasing
    t2, c2 = build(M, B, s_of_m, lambda m: 12 - m if m < 12 else 1)
    print(f"      head, K decreasing : (ii) {'HOLDS' if check_ii_fast(c2, M) is None else 'FAILS ' + str(check_ii_fast(c2, M))}")
    # (d3) head, K constant 1  (still non-decreasing) -> should hold
    t3, c3 = build(M, B, s_of_m, lambda m: 1)
    print(f"      head, K = 1        : (ii) {'HOLDS' if check_ii_fast(c3, M) is None else 'FAILS'}")
    # (d4) interior segment
    t4 = np.zeros(M + 1, dtype=np.int64)
    m, lo = 0, 1
    while lo <= M:
        hi = min(M, lo * B - 1)
        mid = (lo + hi) // 2
        s = s_of_m(m)
        t4[mid:min(hi, mid + s - 1) + 1] = K_of_m(m)
        m += 1
        lo *= B
    c4 = _ba(M, B) + t4
    c4[0] = 0
    print(f"      interior segment   : (ii) {'HOLDS' if check_ii_fast(c4, M) is None else 'FAILS ' + str(check_ii_fast(c4, M))}")
