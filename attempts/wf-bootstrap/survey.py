#!/usr/bin/env python3
"""
survey.py -- systematic map-space survey: LIFTABILITY OF BLOCK VALUES.

For each block B = [a,b] (a run of consecutive integers, length >= 2) and each
threshold T, decide whether q = H(a,b) is the reciprocal sum of a legal system
with min >= T and max <= N, scanning N upward.  Records:
    * the smallest N for which a lift exists   (POSITIVE, with certificate), or
    * "NONE up to N"                            (EXHAUSTIVE negative, exact range).

By the Reduction Lemma this table IS the space of blockwise sum-preserving maps.

usage: survey.py mode
   mode = pairs   : blocks {a,a+1}, a = 2..amax, thresholds T = b+1, 2b, 3b
   mode = runs    : blocks [a,b] of length 2..4
"""
import sys, os
from fractions import Fraction
import liftscan as LS

amax = int(sys.argv[2]) if len(sys.argv) > 2 else 30
mode = sys.argv[1]

def scan(a, b, T, Nmax=900):
    q = sum(Fraction(1, n) for n in range(a, b + 1))
    N = max(T + 6, 2 * T)
    last = None
    while N <= Nmax:
        st, sols, nodes, lb = LS.run(q, T, N, nsol=1)
        if st == "SOL":
            return ("SOL", N, sols[0], lb, nodes)
        if st in ("TOOBIG", "PARTIAL"):
            return (st, N, None, lb, nodes)
        last = (N, lb, nodes)
        N = int(N * 1.25) + 2
    return ("NONE", last[0] if last else N, None, last[1] if last else 0, last[2] if last else 0)


if mode == "pairs":
    for a in range(2, amax + 1):
        b = a + 1
        q = Fraction(1, a) + Fraction(1, b)
        for mult, T in (("min+1", b + 1), ("2b", 2 * b), ("3b", 3 * b)):
            st, N, S, lb, nodes = scan(a, b, T)
            print("block {%d,%d} q=%s  T=%d(%s)  %s N=%d Lbits=%d nodes=%d %s"
                  % (a, b, q, T, mult, st, N, lb, nodes,
                     ("" if S is None else " ".join(map(str, S)))), flush=True)
elif mode == "runs":
    for a in range(2, amax + 1):
        for ln in (2, 3, 4):
            b = a + ln - 1
            q = sum(Fraction(1, n) for n in range(a, b + 1))
            T = b + 1
            st, N, S, lb, nodes = scan(a, b, T)
            print("block [%d,%d] q=%s  T=%d  %s N=%d Lbits=%d nodes=%d %s"
                  % (a, b, q, T, st, N, lb, nodes,
                     ("" if S is None else " ".join(map(str, S)))), flush=True)
