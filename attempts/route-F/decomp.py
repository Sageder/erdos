#!/usr/bin/env python3
"""Evaluate a geometric decomposition of [T, YMAX] into windows [x, r*x]:
report per-window lambda, Lambda, maxsum, and the cumulative available sum.
usage: decomp.py T YMAX r D
"""
import sys
from math import gcd, log2
from fractions import Fraction
from lib import smallest_prime_factors
from universe import prune, lcm_of
from entropy import count_legal

T = int(sys.argv[1]); YMAX = int(sys.argv[2])
r = float(sys.argv[3]); D = int(sys.argv[4])
ppcap = int(sys.argv[5]) if len(sys.argv) > 5 else 0
spf = smallest_prime_factors(YMAX + 2)
x = T
tot = Fraction(0)
print("T=%d ymax=%d ratio=%.2f D=%d ppcap=%d" % (T, YMAX, r, D, ppcap))
while x <= YMAX:
    y = min(int(x * r), YMAX)
    U = prune(x, y, D, spf, pp_cap=(ppcap or None))
    if U:
        L = lcm_of(U); lam = (L // gcd(L, D)).bit_length()
        ms = sum(Fraction(1, n) for n in U)
        Lam = log2(count_legal(U))
        tot += ms
        print("  [%6d,%7d] |U|=%-4d lam=%-4d Lam=%-7.1f maxsum=%.4f  cum=%.4f"
              % (x, y, len(U), lam, Lam, float(ms), float(tot)))
    else:
        print("  [%6d,%7d] EMPTY" % (x, y))
    x = y + 2
print("TOTAL available sum = %.4f" % float(tot))
