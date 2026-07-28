#!/usr/bin/env python3
"""
INDEPENDENT verifier.  Reads lines "SOL n1 n2 ..." (a set U) from stdin or argv
files and checks, in exact rational arithmetic and from scratch:
  (1) every element is an integer >= 2                        (no 1, no 0)
  (2) sum_{n in U} 1/n == 1 exactly                           (Fraction, no floats)
  (3) U has no isolated point  <=>  U is a disjoint union of
      blocks of length >= 2
  (4) prints the maximal runs, r = #runs, M = sum floor(L_i/2),
      and hence the exact set of block counts k realised: r <= k <= M.
Nothing is imported from the search code.
"""
import sys
from fractions import Fraction


def runs_of(U):
    U = sorted(set(U))
    runs, cur = [], [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append(cur); cur = [x]
    runs.append(cur)
    return runs


def check(U, verbose=True):
    U = sorted(U)
    assert len(U) == len(set(U)), "repeated element"
    assert all(isinstance(n, int) and n >= 2 for n in U), "element < 2"
    s = Fraction(0)
    for n in U:
        s += Fraction(1, n)
    ok_sum = (s == 1)
    R = runs_of(U)
    ok_runs = all(len(r) >= 2 for r in R)
    # independent isolated-point test
    S = set(U)
    ok_iso = all((n - 1 in S) or (n + 1 in S) for n in U)
    L = [len(r) for r in R]
    r, M = len(L), sum(l // 2 for l in L)
    if verbose:
        print(f"  sum={s} {'OK' if ok_sum else 'WRONG'};  runs={L}; "
              f"no-isolated={ok_iso}; r={r} M={M} -> k in [{r},{M}]")
        print(f"  blocks: {[ (rr[0],rr[-1]) for rr in R ]}")
    assert ok_sum and ok_runs and ok_iso
    return r, M


if __name__ == "__main__":
    lines = []
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            lines += open(f).read().splitlines()
    else:
        lines = sys.stdin.read().splitlines()
    ks = {}
    cnt = 0
    for ln in lines:
        ln = ln.strip()
        if not ln.startswith("SOL"):
            continue
        U = [int(x) for x in ln.split()[1:]]
        cnt += 1
        print(f"solution #{cnt}  max={max(U)}  |U|={len(U)}")
        r, M = check(U)
        for k in range(r, M + 1):
            ks.setdefault(k, U)
    print()
    print(f"verified {cnt} solutions; block counts k realised: {sorted(ks)}")
