"""
Q3 -- exhaustive window census.

Enumerate EVERY subset U of a window [T,X] with no isolated point, compute
sum_{n in U} 1/n exactly, and report all values whose denominator is <= DCAP.
This gives a complete list of the "arithmetically nice" elements of B(T) whose
representation fits in the window.

It answers, inside the window, the question "which rho are representable, and
does it depend on the size of rho relative to T?"

Run:  python3 q3_window.py T X DCAP
      python3 q3_window.py 2 26 400
"""

import sys
from collections import defaultdict
from fractions import Fraction


def census(T, X, dcap):
    n = X - T + 1
    vals = defaultdict(list)      # Fraction -> list of representations
    total = 0
    inv = [Fraction(1, T + i) for i in range(n)]

    # dfs over maximal runs
    def dfs(i, s, runs):
        nonlocal total
        if i >= n:
            total += 1
            if runs and s.denominator <= dcap:
                vals[s].append(list(runs))
            return
        # skip position i
        dfs(i + 1, s, runs)
        # start a run at i of length >= 2, then leave a gap
        acc = inv[i]
        for j in range(i + 1, n):
            acc = acc + inv[j]
            runs.append((T + i, T + j))
            dfs(j + 2, s + acc, runs)
            runs.pop()

    dfs(0, Fraction(0), [])
    return total, vals


if __name__ == "__main__":
    T = int(sys.argv[1])
    X = int(sys.argv[2])
    dcap = int(sys.argv[3])
    total, vals = census(T, X, dcap)
    print("window [%d,%d]: %d subsets with no isolated point "
          "(including the empty one)" % (T, X, total))
    print("values with denominator <= %d : %d" % (dcap, len(vals)))
    for v in sorted(vals):
        reps = vals[v]
        print("   %-14s  (%d reps)  e.g. %s" % (v, len(reps), reps[0]))
