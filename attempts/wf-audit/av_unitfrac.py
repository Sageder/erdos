#!/usr/bin/env python3
"""
Recon-3 audit of Theorem "no block sum is a unit fraction": H(a,b) != 1/N.

Part 1 (brute force, exact):  for all 1 <= a < b <= B, reduced numerator of
H(a,b) is checked to be != 1.

Part 2 (audit of the proof sketch):  the sketch reduces the theorem to the
inequality
      k(k+1) * C(b,k)  >  2 * b^(1+pi(k))          (INEQ)
in the region  b >= k(k+1)/2  (which is forced by 2^t <= N <= b/k and
2^t >= (k+1)/2).  Here we (i) list every (k,b) in that region with k <= KMAX
where (INEQ) FAILS, and (ii) check the monotonicity in b that lets a finite
check settle each k.

All integer arithmetic; no floats anywhere in the decision.
"""
from fractions import Fraction
from math import comb
import sys


def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= n:
        if s[i]:
            s[i * i:: i] = bytearray(len(s[i * i:: i]))
        i += 1
    return [i for i in range(2, n + 1) if s[i]]


def part1(B):
    # prefix harmonic numbers as exact fractions
    P = [Fraction(0)] * (B + 1)
    for n in range(1, B + 1):
        P[n] = P[n - 1] + Fraction(1, n)
    worst = None
    hits = []
    for a in range(1, B):
        for b in range(a + 1, B + 1):
            h = P[b] - P[a - 1]
            if h.numerator == 1:
                hits.append((a, b, h))
            if worst is None or h.numerator < worst[0]:
                worst = (h.numerator, a, b)
    return hits, worst


def part2(KMAX):
    pr = primes_upto(KMAX + 10)
    fails = []
    for k in range(2, KMAX + 1):
        pik = sum(1 for p in pr if p <= k)
        b0 = (k * (k + 1) + 1) // 2          # ceil(k(k+1)/2)
        # find the largest b where INEQ fails, scanning until it holds for a long
        # stretch and the monotone criterion k > 1+pi(k) guarantees it stays true
        b = max(b0, k)
        lastfail = None
        # monotonicity: log C(b,k) - (1+pi(k)) log b is increasing in b once
        # (b+1)/(b+1-k) >= ((b+1)/b)^(1+pi(k)); certainly once k >= 1+pi(k) and
        # b >= (1+pi(k))*k.  Scan to that point plus slack, exactly.
        bstop = max(b0 + 5 * k * (1 + pik), 4 * k * k + 50)
        while b <= bstop:
            lhs = k * (k + 1) * comb(b, k)
            rhs = 2 * b ** (1 + pik)
            if not lhs > rhs:
                lastfail = b
                fails.append((k, b))
            b += 1
        # certify the tail: check the multiplicative step condition holds from bstop on
        # C(b+1,k)/C(b,k) = (b+1)/(b+1-k); need (b+1)^(1+pik)*... exact integer test:
        bb = bstop
        ok_tail = ((bb + 1) * bb ** pik) * 1 >= 1 and \
                  ((bb + 1) ** (1 + pik)) * (bb + 1 - k) <= (bb ** (1 + pik)) * (bb + 1)
        yield k, pik, b0, lastfail, ok_tail


if __name__ == "__main__":
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    print("PART 1: brute force over 1 <= a < b <= %d" % B)
    hits, worst = part1(B)
    print("   unit-fraction block sums found:", hits)
    print("   smallest reduced numerator over all blocks: %d at (a,b)=(%d,%d)"
          % worst)
    print()
    print("PART 2: failures of INEQ  k(k+1)C(b,k) > 2 b^(1+pi(k))  for b >= k(k+1)/2")
    allfails = []
    tailbad = []
    for k, pik, b0, lastfail, ok_tail in part2(KMAX):
        if lastfail is not None:
            allfails.append((k, b0, lastfail))
        if not ok_tail:
            tailbad.append(k)
    print("   k with some failing b (k, b0=ceil(k(k+1)/2), largest failing b):")
    for t in allfails:
        print("     ", t)
    print("   k where the monotone tail test did not certify:", tailbad)
