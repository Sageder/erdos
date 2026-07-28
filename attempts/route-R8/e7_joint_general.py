"""e7_joint_general.py — joint SAT for band macros on N with arbitrary band-to-slot orders.

Universe [1, base^(M+1)); bands T_m = [base^m, base^(m+1)).  Macro: slot(m) gives the position
block order (any permutation of 0..M realizable as prefix of an omega-order).  Within-band
orders free (pair vars + transitivity).  Clauses: for every k-AP inside the universe with
d passing dpred: forbid all-adjacent-increasing and all-adjacent-decreasing, with cross-band
comparisons constant (slot order).  Pure-cross APs with monotone constants refute the macro.

Joint solving uses cross-band slack ("earlier pair help") that per-band decoupling loses.
SAT -> extract taus, assemble, verify independently with the exact checker.
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


def make_band_of(base, M):
    V = base ** (M + 1) - 1
    tab = [0] * (V + 1)
    m, nxt = 0, base
    for a in range(1, V + 1):
        if a >= nxt:
            m += 1
            nxt *= base
        tab[a] = m
    return tab, V


def solve_joint(base, M, k, dpred, slot, verbose=True, dname=""):
    band, V = make_band_of(base, M)
    vid = {}
    ctr = [0]

    def var(u, v):
        a, b = (u, v) if u < v else (v, u)
        if (a, b) not in vid:
            ctr[0] += 1
            vid[(a, b)] = ctr[0]
        lit = vid[(a, b)]
        return lit if (u, v) == (a, b) else -lit

    solver = Cadical153()
    ncl = 0
    for m in range(M + 1):
        vals = list(range(base ** m, min(base ** (m + 1), V + 1)))
        for a, b, c in combinations(vals, 3):
            solver.add_clause([-var(a, b), -var(b, c), var(a, c)])
            solver.add_clause([var(a, b), var(b, c), -var(a, c)])
            ncl += 2
    refuted = []
    for d in range(1, (V - 1) // (k - 1) + 1):
        if not dpred(d):
            continue
        for t in range(1, V - (k - 1) * d + 1):
            terms = [t + j * d for j in range(k)]
            inc_cl, dec_cl = [], []
            inc_ok = dec_ok = True
            for j in range(k - 1):
                u, v = terms[j], terms[j + 1]
                mu, mv = band[u], band[v]
                if mu == mv:
                    inc_cl.append(-var(u, v))
                    dec_cl.append(var(u, v))
                elif slot(mu) < slot(mv):
                    dec_ok = False
                else:
                    inc_ok = False
            if inc_ok:
                if inc_cl:
                    solver.add_clause(inc_cl)
                    ncl += 1
                else:
                    refuted.append((t, d, "inc"))
            if dec_ok:
                if dec_cl:
                    solver.add_clause(dec_cl)
                    ncl += 1
                else:
                    refuted.append((t, d, "dec"))
    tag = f"base{base} M={M} k={k} d:{dname}"
    if refuted:
        print(f"  {tag}: MACRO REFUTED e.g. {refuted[:5]} (total {len(refuted)})", flush=True)
        solver.delete()
        return None
    ok = solver.solve()
    if not ok:
        print(f"  {tag}: UNSAT ({ncl} clauses)", flush=True)
        solver.delete()
        return None
    model = set(l for l in solver.get_model() if l > 0)
    solver.delete()

    def cmp(u, v):
        if u == v:
            return 0
        a, b = (u, v) if u < v else (v, u)
        before = ((a, b) not in vid) or (vid[(a, b)] in model)
        return (-1 if before else 1) if (u, v) == (a, b) else (1 if before else -1)

    taus = {}
    for m in range(M + 1):
        vals = list(range(base ** m, min(base ** (m + 1), V + 1)))
        taus[m] = sorted(vals, key=functools.cmp_to_key(cmp))
    seq = []
    for m in sorted(range(M + 1), key=slot):
        seq.extend(taus[m])
    # independent verification on the assembled sequence (a permutation of [1..V] iff slot
    # order is the ascending one; otherwise a permutation of the same SET in scrambled band
    # order -- use the general checker via ranks)
    wits = find_kaps_perm_np(rerank(seq), k, limit=10 ** 9)
    # rerank preserves AP structure? NO -- must check on raw values.  Use exact scan:
    from zcheck import has_monotone_kap_window, find_monotone_kaps
    badall = find_monotone_kaps(seq, k, limit=10 ** 6)
    bad = [w for w in badall if dpred(abs(w[0][1] - w[0][0]))]
    print(f"  {tag}: SAT ({ncl} cls); assembled |{len(seq)}|; filtered monotone {k}-APs: "
          f"{len(bad)} {'FAIL ' + str(bad[:3]) if bad else '(NONE -- verified)'}", flush=True)
    if verbose:
        for m in range(min(M, 3) + 1):
            show = taus[m] if len(taus[m]) <= 30 else taus[m][:30] + ["..."]
            print(f"    tau_{m}: {show}", flush=True)
    return taus


def rerank(seq):
    """rank values 1..n by sorted order (order-isomorphic relabel; NOT AP-preserving --
    only used where a permutation-of-interval is guaranteed)."""
    order = {v: i + 1 for i, v in enumerate(sorted(seq))}
    return [order[v] for v in seq]


SLOTS = {
    "asc": lambda m: m,
    "swap23": lambda m: m if m < 2 else (m + 1 if m % 2 == 0 else m - 1),   # 0,1,3,2,5,4,...
    "swap01": lambda m: (m + 1 if m % 2 == 0 else m - 1),                   # 1,0,3,2,...
    "swap12": lambda m: m if m == 0 else (m + 1 if m % 2 == 1 else m - 1),  # 0,2,1,4,3,...
}

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=int, default=2)
    ap.add_argument("--M", type=int, default=7)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--dmode", default="odd")
    ap.add_argument("--slot", default="asc")
    args = ap.parse_args()
    dpreds = {"all": lambda d: True, "odd": lambda d: d % 2 == 1,
              "ndiv4": lambda d: d % 4 != 0, "ndiv8": lambda d: d % 8 != 0}
    dpred = dpreds[args.dmode]
    for M in range(2, args.M + 1):
        r = solve_joint(args.base, M, args.k, dpred, SLOTS[args.slot],
                        dname=args.dmode + "/" + args.slot)
        if r is None:
            break
