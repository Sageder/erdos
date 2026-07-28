#!/usr/bin/env python3
"""
smoothstats.py -- OBSERVATIONAL.  For every known solution in the corpus,
record the largest prime factor P(U) = max_{n in U} P(n) against max(U) and
min(U).  Purpose: calibrate the DESIGN threshold z below which we may restrict
the universe to z-smooth integers without (empirically) losing solutions.

Everything here is exact integer arithmetic; the only floats are printed
ratios (diagnostics), never used in a decision.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import largest_prime_factor_sieve, runs
from collections import Counter


def load(path, tag="SOL"):
    sols = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if parts[0] == tag:
                parts = parts[1:]
            try:
                U = [int(x) for x in parts]
            except ValueError:
                continue
            if U:
                sols.append(U)
    return sols


def main():
    paths = sys.argv[1:] or ["/home/user/erdos/experiments/ALLSOLS.txt"]
    sols = []
    for p in paths:
        sols += load(p)
    print("solutions loaded:", len(sols))
    M = max(max(U) for U in sols)
    lpf = largest_prime_factor_sieve(M)
    rows = []
    for U in sols:
        mx = max(U)
        mn = min(U)
        P = max(lpf[n] for n in U)
        rows.append((mn, mx, P))
    # histogram of P/max
    print("\n  min  max   P(U)   P/max   P/min")
    buckets = Counter()
    for mn, mx, P in rows:
        buckets[(P * 20) // mx] += 1
    for k in sorted(buckets):
        print("   P/max in [%.2f,%.2f) : %d" % (k / 20, (k + 1) / 20, buckets[k]))
    # worst cases
    rows.sort(key=lambda t: -t[2] / t[1])
    print("\nlargest P/max:")
    for r in rows[:5]:
        print("   min=%d max=%d P=%d  P/max=%.3f" % (r[0], r[1], r[2], r[2] / r[1]))
    rows.sort(key=lambda t: t[2] / t[1])
    print("smallest P/max:")
    for r in rows[:5]:
        print("   min=%d max=%d P=%d  P/max=%.3f" % (r[0], r[1], r[2], r[2] / r[1]))
    # how many solutions are z-smooth for z = max/2, max/3, max/4 ...
    print("\nfraction of solutions all of whose elements are max/c - smooth:")
    for c in (2, 2.5, 3, 4, 5, 6, 8, 10):
        cnt = sum(1 for mn, mx, P in rows if P * c <= mx)
        print("   c=%-4s : %d / %d" % (c, cnt, len(rows)))
    # relative to min
    print("\nfraction with P(U) <= min(U)*c:")
    for c in (0.5, 0.75, 1, 1.5, 2, 3):
        cnt = sum(1 for mn, mx, P in rows if P <= c * mn)
        print("   c=%-4s : %d / %d" % (c, cnt, len(rows)))


if __name__ == "__main__":
    main()
