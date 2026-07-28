#!/usr/bin/env python3
"""
s7_twoblocks.py -- SUB-QUESTION 3, part 2:  is  1/N = H(a,b) + H(c,d)  solvable
with two DISJOINT blocks (b < c), each of length >= 2 ?

Method (exact, no floats in the decision path):
  * pick a large prime P (> any element used) and precompute
        h[n] = sum_{k=1}^{n} k^{-1}  mod P .
    Then H(a,b) mod P = h[b] - h[a-1].
  * put every admissible "second block" value into a dict  value -> list of (c,d).
  * for every "first block" (a,b) and every N with 1/N > H(a,b), look up
        (1/N - H(a,b))  mod P
    and EXACTLY re-check every hit with Fraction arithmetic.
False positives are possible mod P and are filtered by the exact recheck;
false negatives are impossible (a true solution satisfies the congruence).

usage: python3 s7_twoblocks.py MAXELT NMAX
"""
import sys
from fractions import Fraction

P = (1 << 61) - 1   # Mersenne prime


def run(M, NMAX):
    inv = [0] * (M + 2)
    inv[1] = 1
    for i in range(2, M + 2):
        inv[i] = (P - (P // i) * inv[P % i] % P) % P
    h = [0] * (M + 2)
    for n in range(1, M + 1):
        h[n] = (h[n - 1] + inv[n]) % P

    # float prefix sums for range control only (never in a decision)
    hf = [0.0] * (M + 2)
    for n in range(1, M + 1):
        hf[n] = hf[n - 1] + 1.0 / n

    # dictionary of ALL block values with max element <= M and H <= 1/2
    d = {}
    nblocks = 0
    for a in range(2, M):
        for b in range(a + 1, M + 1):
            if hf[b] - hf[a - 1] > 0.5000001:
                break
            v = (h[b] - h[a - 1]) % P
            d.setdefault(v, []).append((a, b))
            nblocks += 1
    print("blocks stored: %d (max element %d)" % (nblocks, M))

    hits = []
    invN = [0] * (NMAX + 1)
    for N in range(2, NMAX + 1):
        invN[N] = pow(N, P - 2, P)

    tried = 0
    for a in range(2, M):
        for b in range(a + 1, M + 1):
            s = hf[b] - hf[a - 1]
            if s > 0.5000001:
                break
            v1 = (h[b] - h[a - 1]) % P
            lo = int(1.0 / s) + 1 if s > 0 else NMAX
            # need 1/N > H(a,b)  =>  N < 1/s
            for N in range(2, min(NMAX, int(1.0 / s) + 1) + 1):
                if 1.0 / N <= s:
                    continue
                tried += 1
                tgt = (invN[N] - v1) % P
                for (c, dd) in d.get(tgt, ()):
                    if c <= b:
                        continue
                    e1 = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
                    e2 = sum((Fraction(1, n) for n in range(c, dd + 1)), Fraction(0))
                    if e1 + e2 == Fraction(1, N):
                        hits.append((N, a, b, c, dd))
                        print("  HIT 1/%d = H(%d,%d) + H(%d,%d)" % (N, a, b, c, dd))
    print("candidate (block,N) pairs tried: %d" % tried)
    print("exact solutions: %s" % (hits if hits else "NONE"))
    return hits


if __name__ == "__main__":
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
    NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    run(M, NMAX)
