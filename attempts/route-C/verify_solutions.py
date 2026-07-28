#!/usr/bin/env python3
"""
verify_solutions.py -- independent exact verification of claimed legal solutions.

Reads SOL lines (from run_dfs.py / dfs) on stdin or from a file and checks, with
fractions.Fraction (exact rational arithmetic, no floats anywhere):
   (1) every element is an integer >= 2,
   (2) elements are distinct,
   (3) sum_{n in U} 1/n == 1 exactly,
   (4) U has no isolated point: every n in U has n-1 in U or n+1 in U,
   (5) reports the maximal runs, r = #runs, M = sum floor(L_i/2), so that the
       set of k with P(k) realised by this U is exactly the interval [r, M].
Also re-checks (3) a second, independent way with integer arithmetic over
Lcm = lcm(U): sum_{n in U} Lcm/n == Lcm.
"""
import sys
from fractions import Fraction
from math import lcm


def check(U):
    U = sorted(U)
    assert all(isinstance(n, int) and n >= 2 for n in U), "elements must be ints >= 2"
    assert len(set(U)) == len(U), "elements must be distinct"
    s = sum(Fraction(1, n) for n in U)
    ok_sum = (s == 1)
    Lc = lcm(*U)
    ok_int = (sum(Lc // n for n in U) == Lc)
    S = set(U)
    iso = [n for n in U if (n - 1) not in S and (n + 1) not in S]
    runs = []
    cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append(cur); cur = [x]
    runs.append(cur)
    r = len(runs)
    M = sum(len(R) // 2 for R in runs)
    return dict(sum_ok=ok_sum, int_ok=ok_int, sum=s, isolated=iso, runs=[(R[0], R[-1]) for R in runs],
                r=r, M=M, maxU=max(U))


def parse(line):
    parts = line.split()
    if parts and parts[0] == 'SOL':
        parts = parts[1:]
    return [int(x) for x in parts]


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    n_ok = n_bad = 0
    for line in src:
        line = line.strip()
        if not line.startswith('SOL'):
            continue
        U = parse(line)
        res = check(U)
        good = res['sum_ok'] and res['int_ok'] and not res['isolated']
        n_ok += good; n_bad += (not good)
        print(("OK  " if good else "FAIL") +
              f" max={res['maxU']:4d} |U|={len(U):3d} r={res['r']:2d} M={res['M']:2d} "
              f"k-range=[{res['r']},{res['M']}] sum={res['sum']} iso={res['isolated']}")
        print("      runs:", res['runs'])
    print(f"\n{n_ok} verified, {n_bad} failed")
