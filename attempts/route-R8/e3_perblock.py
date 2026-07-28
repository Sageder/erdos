"""e3_perblock.py — per-block sufficient conditions for the dyadic-block construction, k=5 and
k=4 (route R8: locate exactly where length 4 resists the mechanism that works for length 5).

Macro: A = tau_0 ++ tau_1 ++ ..., tau_m a permutation of B_m = [2^m, 2^(m+1)).
Cross-block position order = value order.  For k in {4, 5} write an AP as t, t+d, ..., t+(k-1)d.

Sharpened pigeonhole (L2', machine-checked below): the last three terms t+(k-3)d, t+(k-2)d,
t+(k-1)d satisfy (t+(k-1)d)/(t+(k-3)d) < 2 (t >= 1), so they occupy <= 2 consecutive dyadic
blocks, hence two ADJACENT ones share a block.

Sufficient per-block conditions for "no monotone k-AP" of the assembled permutation:
  (A) tau_m has no internal monotone decreasing k-AP  [cross pairs are increasing, so any
      decreasing k-AP lives inside one block]  -- we also add: no internal increasing k-AP
      (implied by (B)+(C) but kept as a safety clause);
  (B) for every 3-AP u, u+d, u+2d inside B_m with u > (k-3)d: pairs (u,u+d), (u+d,u+2d) not
      both increasing;
  (C) forced-decreasing pairs:
      R1_m = {(w, w+d) in B_m : w > (k-3)d, w+2d >= 2^(m+1)}          [next AP term overflows]
      R2_m = {(w, w+d) in B_m : w > (k-2)d, w-d < 2^m}                [previous AP term underflows]
      all pairs in R1_m u R2_m must be position-decreasing.

Soundness argument (proved in REPORT.md; sketch): an increasing k-AP has, among its last three
terms, an adjacent same-block pair.  If both last pairs are in B_m, (B) with u = t+(k-3)d breaks
it; if exactly the earlier pair (t+(k-3)d, t+(k-2)d) is in B_m, that pair is in R1_m; if exactly
the later pair (t+(k-2)d, t+(k-1)d) is in B_m, it is in R2_m; both-cross is impossible since the
three terms span < ratio 2.  Decreasing k-APs die by (A).  So per-block SAT for all m proves the
full theorem (for the range of m solved; closed form needed for all m).

This file: per-block SAT (transitivity + clauses above); reports SAT/UNSAT per m and k; if SAT,
extracts tau_m; assembles prefix and INDEPENDENTLY verifies with the exact vectorized checker.
"""

import sys
import os
import functools
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "experiments"))
from fastcheck import has_kap_perm_np  # noqa: E402

from pysat.solvers import Cadical153  # noqa: E402


def check_last3_pigeonhole(k, maxt, maxd):
    """L2': last three terms of a k-AP occupy <= 2 consecutive dyadic blocks; adjacent pair
    shares a block."""
    def blk(v):
        return v.bit_length() - 1
    for t in range(1, maxt + 1):
        for d in range(1, maxd + 1):
            a, b, c = t + (k - 3) * d, t + (k - 2) * d, t + (k - 1) * d
            if blk(a) != blk(b) and blk(b) != blk(c):
                return (t, d)
    return None


def solve_block(m, k):
    """Per-block SAT for conditions (A),(B),(C).  Returns tau_m (list) or None."""
    lo, hi = 2 ** m, 2 ** (m + 1)  # block = [lo, hi)
    blk = list(range(lo, hi))
    n = len(blk)
    idx = {v: i for i, v in enumerate(blk)}
    # variable x_{u,v} for u<v in block: True = u before v (increasing pair)
    vid = {}
    ctr = [0]

    def var(u, v):
        assert lo <= u < v < hi
        if (u, v) not in vid:
            ctr[0] += 1
            vid[(u, v)] = ctr[0]
        return vid[(u, v)]

    cnf = []
    for a, b, c in combinations(blk, 3):
        cnf.append([-var(a, b), -var(b, c), var(a, c)])
        cnf.append([var(a, b), var(b, c), -var(a, c)])
    # (A): no internal monotone decreasing k-AP (and no increasing, as safety)
    maxd_int = (n - 1) // (k - 1) if k > 1 else 0
    for d in range(1, maxd_int + 1):
        for t in range(lo, hi - (k - 1) * d):
            terms = [t + j * d for j in range(k)]
            cnf.append([var(terms[j], terms[j + 1]) for j in range(k - 1)])   # not all dec
            cnf.append([-var(terms[j], terms[j + 1]) for j in range(k - 1)])  # not all inc
    # (B): 3-APs inside block with u > (k-3) d: not both pairs increasing
    for d in range(1, (n - 1) // 2 + 1):
        for u in range(lo, hi - 2 * d):
            if u > (k - 3) * d:
                cnf.append([-var(u, u + d), -var(u + d, u + 2 * d)])
    # (C): forced decreasing pairs
    forced = []
    for d in range(1, n):
        for w in range(lo, hi - d):
            r1 = (w > (k - 3) * d) and (w + 2 * d >= hi)
            r2 = (w > (k - 2) * d) and (w - d < lo)
            if r1 or r2:
                forced.append((w, w + d))
                cnf.append([-var(w, w + d)])
    with Cadical153(bootstrap_with=cnf) as s:
        if not s.solve():
            return None, len(forced)
        model = set(l for l in s.get_model() if l > 0)

    def cmp(u, v):
        if u == v:
            return 0
        a, b = min(u, v), max(u, v)
        if (a, b) not in vid:
            before = True  # unconstrained pair: default increasing
        else:
            before = vid[(a, b)] in model
        return (-1 if before else 1) if (u, v) == (a, b) else (1 if before else -1)

    tau = sorted(blk, key=functools.cmp_to_key(cmp))
    return tau, len(forced)


if __name__ == "__main__":
    for k in (5, 4):
        ph = check_last3_pigeonhole(k, 4000, 2000)
        print(f"L2' (k={k}) exhaustive t<=4000,d<=2000:",
              "HOLDS" if ph is None else f"FAILS {ph}")
    for k in (5, 4):
        print(f"=== per-block SAT, k={k} ===")
        taus = []
        for m in range(0, 11):
            tau, nforced = solve_block(m, k)
            if tau is None:
                print(f"  m={m}: UNSAT  (forced pairs: {nforced})")
                break
            taus.append(tau)
            show = tau if len(tau) <= 32 else tau[:16] + ["..."]
            print(f"  m={m}: SAT (forced {nforced})  tau: {show}")
        else:
            m = 11
        if taus and len(taus) >= 4:
            seq = [v for tau in taus for v in tau]
            N = len(seq)
            assert sorted(seq) == list(range(1, N + 1))
            if k == 5:
                ok = not has_kap_perm_np(seq, k)
                print(f"  assembled prefix N={N}: independent exact check "
                      f"no monotone {k}-AP: {ok}")
            else:
                # k=4: the sound claim is: no decreasing 4-AP at all, and no increasing
                # 4-AP with d < t (first term).  Verify via full witness scan.
                from fastcheck import find_kaps_perm_np
                wits = find_kaps_perm_np(seq, 4, limit=10 ** 9)
                bad = [w for w in wits if w[2] == -1 or w[1] < w[0]]
                res = [w for w in wits if w[2] == +1 and w[1] >= w[0]]
                print(f"  assembled prefix N={N}: monotone 4-APs violating the conditional "
                      f"claim (dec, or inc with d < x): {len(bad)}; residual inc 4-APs with "
                      f"d >= x: {len(res)} e.g. {res[:6]}")
