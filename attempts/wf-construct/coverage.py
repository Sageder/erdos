#!/usr/bin/env python3
"""
coverage.py -- collect every legal system with reciprocal sum 1/2 produced in
this directory (min element >= 104), pair each with a DISJOINT 1/2-system
inside [2,103], and report the block counts k that the resulting genuine
solutions of sum = 1 realise (r <= k <= cap).

Exact arithmetic only.  Every combined solution is re-verified from scratch.
usage: coverage.py FILE...   (files containing "SOL ..." or bare element lists)
"""
import sys, os, glob
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import verify_solution, runs, run_count, capacity, exact_sum

LOW = {  # the ONLY two 1/2-systems inside [2,103] (esearch exhausted: 2 solutions)
    (5, 5): [6, 7, 20, 21, 44, 45, 77, 78, 90, 91],
    (7, 7): None,   # filled in from log_low103b.txt if present
}


def load(paths):
    out = []
    for p in paths:
        if not os.path.exists(p):
            continue
        for line in open(p):
            t = line.split()
            if t and t[0] == "SOL":
                t = t[1:]
            if not t:
                continue
            try:
                U = sorted(int(x) for x in t)
            except ValueError:
                continue
            if U and exact_sum(U) == Fraction(1, 2):
                out.append(U)
    return out


def main():
    lows = load(["log_low103.txt", "log_low103b.txt"])
    lows = [U for U in lows if max(U) <= 103]
    lowpairs = {}
    for U in lows:
        lowpairs[(run_count(U), capacity(U))] = U
    if not lowpairs:
        lowpairs[(5, 5)] = LOW[(5, 5)]
    print("low 1/2-systems in [2,103]:", sorted(lowpairs))
    highs = load(sys.argv[1:] if len(sys.argv) > 1 else
                 glob.glob("cert*.txt") + glob.glob("cons_cert.txt") +
                 glob.glob("log_*.txt"))
    highs = [U for U in highs if min(U) >= 104]
    hp = {}
    for U in highs:
        hp.setdefault((run_count(U), capacity(U)), U)
    print("far 1/2-systems with min >= 104 (r,cap):", sorted(hp))
    covered = set()
    best = {}
    for (r1, c1), A in lowpairs.items():
        for (r2, c2), B in hp.items():
            if max(A) >= min(B):
                continue
            U = sorted(A + B)
            ok, info = verify_solution(U, Fraction(1))
            assert ok, info
            for k in range(info["r"], info["cap"] + 1):
                covered.add(k)
                best.setdefault(k, (info["r"], info["cap"], info["max"]))
    ks = sorted(covered)
    print("k realised:", ks)
    if ks:
        lo, hi = ks[0], ks[-1]
        miss = [k for k in range(lo, hi + 1) if k not in covered]
        print("range:", lo, "..", hi, " missing inside:", miss)


if __name__ == "__main__":
    main()
