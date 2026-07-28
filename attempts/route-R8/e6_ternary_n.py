"""e6_ternary_n.py — ternary-band macro on N: per-band SAT with SOUND sufficient conditions.

Bands T_m = [3^m, 3^(m+1)) (T_0 = {1,2}), macro ascending: A = tau_0 ++ tau_1 ++ ...

Ternary pigeonhole (proved in REPORT.md, verified here): for ANY k-AP of positive integers
with k >= 4, among the last three terms u = t+(k-3)d, u+d, u+2d we have (u+2d)/u < 3
(as u > (k-3)d >= d), so these three terms span at most 2 ternary bands, hence two adjacent
ones share a band.  For k = 4 this is unconditional on N (contrast: base 2 requires d < t).

Sufficient per-band conditions for NO monotone k-AP (whole construction):
  (A) tau_m has no internal monotone decreasing k-AP  (cross-band pairs are increasing);
  (B) for every 3-AP u, u+d, u+2d inside T_m with u > (k-3) d: not both pairs increasing;
  (C) forced-decreasing pairs (w, w+d) in T_m:
      R1: w + 2d >= 3^(m+1)  and  w >= (k-3) d + 1     [P2 crosses up; P1 must break]
      R2: w - d  <  3^m      and  w >= (k-2) d + 1     [P1 crosses down; P2 must break]
Soundness: increasing k-AP -> adjacent same-band pair among last three; cases both-in / only
P1 / only P2 handled by (B) / R1 / R2; both-cross impossible (three terms, <= 2 bands, bands
are intervals).  Decreasing k-AP -> internal, killed by (A).  So SAT for all m ==> theorem.

Modes:
  k=4 dfilter=all   : if SAT for all m -> would resolve Erdos 196 (expect UNSAT somewhere;
                      report exactly where and extract the obstruction)
  k=4 dfilter=odd   : LeSaulnier-Vijay-type target: no monotone 4-AP with odd d
  k=4 dfilter=mod4  : Adenwalla-type: no monotone 4-AP with d not divisible by 4
  k=5 dfilter=all   : DEGS-type: no monotone 5-AP at all
"""

import sys
import os
import functools
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "experiments"))
from fastcheck import find_kaps_perm_np  # noqa: E402

from pysat.solvers import Cadical153  # noqa: E402


def band_bounds(m):
    return 3 ** m, 3 ** (m + 1)


def solve_band(m, k, dpred, return_core=False):
    lo, hi = band_bounds(m)
    vals = list(range(lo, hi))
    vid = {}
    ctr = [0]

    def var(u, v):
        a, b = (u, v) if u < v else (v, u)
        if (a, b) not in vid:
            ctr[0] += 1
            vid[(a, b)] = ctr[0]
        lit = vid[(a, b)]
        return lit if (u, v) == (a, b) else -lit

    cnf = []
    for a, b, c in combinations(vals, 3):
        cnf.append([-var(a, b), -var(b, c), var(a, c)])
        cnf.append([var(a, b), var(b, c), -var(a, c)])
    n = len(vals)
    # (A) internal monotone k-APs (both directions, any d passing dpred)
    for d in range(1, (n - 1) // (k - 1) + 1):
        if not dpred(d):
            continue
        for t in range(lo, hi - (k - 1) * d):
            terms = [t + j * d for j in range(k)]
            cnf.append([var(terms[j], terms[j + 1]) for j in range(k - 1)])
            cnf.append([-var(terms[j], terms[j + 1]) for j in range(k - 1)])
    # (B)
    for d in range(1, (n - 1) // 2 + 1):
        if not dpred(d):
            continue
        for u in range(max(lo, (k - 3) * d + 1), hi - 2 * d):
            cnf.append([-var(u, u + d), -var(u + d, u + 2 * d)])
    # (C)
    nforced = 0
    for d in range(1, n):
        if not dpred(d):
            continue
        for w in range(lo, hi - d):
            r1 = (w + 2 * d >= hi) and (w >= (k - 3) * d + 1)
            r2 = (w - d < lo) and (w >= (k - 2) * d + 1)
            if r1 or r2:
                cnf.append([-var(w, w + d)])
                nforced += 1
    with Cadical153(bootstrap_with=cnf) as s:
        if not s.solve():
            return None, nforced
        model = set(l for l in s.get_model() if l > 0)

    def cmp(u, v):
        if u == v:
            return 0
        a, b = (u, v) if u < v else (v, u)
        before = ((a, b) not in vid) or (vid[(a, b)] in model)
        return (-1 if before else 1) if (u, v) == (a, b) else (1 if before else -1)

    return sorted(vals, key=functools.cmp_to_key(cmp)), nforced


def run(k, dname, dpred, mmax):
    print(f"=== N ternary bands, k={k}, d filter: {dname} ===", flush=True)
    taus = []
    for m in range(mmax + 1):
        tau, nf = solve_band(m, k, dpred)
        if tau is None:
            print(f"  band {m} (size {3**m*2}): UNSAT (forced {nf})", flush=True)
            return taus, m
        taus.append(tau)
        show = tau if len(tau) <= 24 else tau[:24] + ["..."]
        print(f"  band {m}: SAT (forced {nf})  {show}", flush=True)
    # assemble and independently verify the conditional claim on the prefix
    seq = [v for tau in taus for v in tau]
    N = len(seq)
    assert sorted(seq) == list(range(1, N + 1))
    wits = find_kaps_perm_np(seq, k, limit=10 ** 9)
    bad = [w for w in wits if dpred(w[1])]
    print(f"  assembled prefix N={N}: monotone {k}-APs with filtered d: {len(bad)} "
          f"{'FAIL ' + str(bad[:5]) if bad else '(NONE -- verified)'}; "
          f"other monotone {k}-APs present: {len(wits) - len(bad)}", flush=True)
    return taus, None


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="all4")
    ap.add_argument("--mmax", type=int, default=4)
    args = ap.parse_args()
    modes = {
        "all4": (4, "all", lambda d: True),
        "odd4": (4, "odd", lambda d: d % 2 == 1),
        "mod44": (4, "not div by 4", lambda d: d % 4 != 0),
        "all5": (5, "all", lambda d: True),
    }
    k, dname, dpred = modes[args.mode]
    run(k, dname, dpred, args.mmax)
