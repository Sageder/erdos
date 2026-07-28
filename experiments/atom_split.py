#!/usr/bin/env python3
"""
CLAIM TESTED: does the "atom split" identity
      1/a + 1/(a+1)  =  1/c + 1/(c+1) + 1/d + 1/(d+1)
have solutions with  a+1 < c,  c+1 < d  (so the three atoms are pairwise
disjoint and the two new ones lie strictly above the old one)?

If yes for infinitely many a, then replacing an atom of a solution by the two
new atoms increases the number of blocks by exactly one, for ever.

Exact arithmetic.  For fixed a and c we must solve  beta_d = rho := beta_a-beta_c
with beta_d = (2d+1)/(d(d+1)); writing rho = p/q this is
      p d^2 + (p-2q) d - q = 0,
so d is an integer iff  D := p^2 + 4 q^2  is a perfect square and 2p | (2q-p+sqrt D).
"""
import sys
from fractions import Fraction
from math import isqrt


def beta(a):
    return Fraction(2 * a + 1, a * (a + 1))


def solve_atom(rho):
    """all integers d>=1 with beta(d) == rho"""
    p, q = rho.numerator, rho.denominator
    if p <= 0:
        return []
    D = p * p + 4 * q * q
    s = isqrt(D)
    if s * s != D:
        return []
    out = []
    for sg in (s, -s):
        num = 2 * q - p + sg
        if num > 0 and num % (2 * p) == 0:
            d = num // (2 * p)
            if d >= 1 and beta(d) == rho:
                out.append(d)
    return out


def scan(amax, cmax_mult=8):
    hits = []
    for a in range(2, amax + 1):
        ba = beta(a)
        c = a + 2
        while c <= cmax_mult * a + 40:
            rho = ba - beta(c)
            if rho <= 0:
                c += 1
                continue
            for d in solve_atom(rho):
                if d >= c + 2:
                    assert beta(a) == beta(c) + beta(d)
                    hits.append((a, c, d))
            c += 1
    return hits


if __name__ == "__main__":
    amax = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    hits = scan(amax)
    print(f"atom-split solutions with a <= {amax}: {len(hits)}")
    for h in hits[:80]:
        a, c, d = h
        assert beta(a) == beta(c) + beta(d)
        print(f"  1/{a}+1/{a+1} = 1/{c}+1/{c+1} + 1/{d}+1/{d+1}")
