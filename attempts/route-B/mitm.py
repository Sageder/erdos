"""
mitm.py -- INDEPENDENT meet-in-the-middle count of the legal U subset [2,N] with
reciprocal sum exactly 1.

Completely different algorithm from bsearch.c: no DFS, no pruning, no p-adic
reachability.  The reduced universe A(N) decomposes into maximal runs; a legal U is
exactly a choice, independently in each run, of a subset with no isolated point
inside that run.  Enumerate every choice for the "left" runs and every choice for the
"right" runs, hash the left partial sums (exact Python integers, weight L/n), and
look up L - s for every right partial sum.

Used as a cross-check of the exhaustive counts of bsearch.c.

usage: python3 mitm.py N [--list]
"""
import sys
from fractions import Fraction
from reduce import reduce_universe, lcm_of
from structure import runs_of, run_configs


def solve(N, want_list=False, verbose=True):
    A, _ = reduce_universe(N)
    if not A:
        if verbose:
            print(f"N={N}: reduced universe empty -> 0 solutions")
        return 0, []
    L = lcm_of(A)
    rs = runs_of(A)
    # config lists per run: (weight, tuple of elements)
    cfg = []
    for a, b in rs:
        cs = []
        for c in run_configs(a, b):
            cs.append((sum(L // n for n in c), c))
        cfg.append(cs)
    sizes = [len(c) for c in cfg]
    # greedy balanced split (runs are independent, order irrelevant)
    order = sorted(range(len(cfg)), key=lambda i: -sizes[i])
    left, right = [], []
    pl, pr = 1, 1
    for i in order:
        if pl <= pr:
            left.append(i); pl *= sizes[i]
        else:
            right.append(i); pr *= sizes[i]
    if verbose:
        print(f"N={N}: |A|={len(A)} runs={len(rs)} space={pl*pr:.4g} "
              f"left={pl:.4g} right={pr:.4g} L={L}")

    def enumerate_side(idxs, keep_elems):
        acc = [(0, ())] if keep_elems else [0]
        for i in idxs:
            nxt = []
            ws = [w for w, c in cfg[i]]
            if keep_elems:
                for s, els in acc:
                    for w, c in cfg[i]:
                        t = s + w
                        if t <= L:
                            nxt.append((t, els + c))
            else:
                for s in acc:
                    for w in ws:
                        t = s + w
                        if t <= L:   # a partial sum may never exceed the target
                            nxt.append(t)
            acc = nxt
        return acc

    # left side into a dict  sum -> list of element tuples
    sols = []
    cnt = 0
    if want_list:
        tab = {}
        for s, els in enumerate_side(left, True):
            tab.setdefault(s, []).append(els)
        for s, els in enumerate_side(right, True):
            for h in tab.get(L - s, ()):
                cnt += 1
                sols.append(tuple(sorted(h + els)))
    else:
        from collections import Counter
        tab = Counter(enumerate_side(left, False))
        for s in enumerate_side(right, False):
            cnt += tab.get(L - s, 0)
    return cnt, sols


if __name__ == "__main__":
    N = int(sys.argv[1])
    want = "--list" in sys.argv
    cnt, sols = solve(N, want)
    print(f"MITM count for max(U) <= {N}: {cnt}")
    if want:
        # exact re-verification of every solution found
        for U in sols:
            assert sum(Fraction(1, n) for n in U) == 1
            S = set(U)
            assert all((n - 1) in S or (n + 1) in S for n in U)
        print(f"all {len(sols)} re-verified with Fraction")
        for U in sorted(sols)[:5]:
            print("  ", U)
