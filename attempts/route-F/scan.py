#!/usr/bin/env python3
"""Scan windows [x,y] x prime-cap for (lambda, maxsum, Lambda).
usage: scan.py x  y1,y2,...  cap1,cap2,...  D
"""
import sys
from lib import smallest_prime_factors
from entropy import stats

x = int(sys.argv[1])
ys = [int(t) for t in sys.argv[2].split(",")]
caps = [int(t) for t in sys.argv[3].split(",")]
D = int(sys.argv[4])
spf = smallest_prime_factors(max(ys) + 2)
print("x=%d D=%d" % (x, D))
for y in ys:
    for cap in caps:
        s = stats(x, y, D, None if cap == 0 else cap, spf)
        print("  y=%-7d cap=%-3d |U|=%-5d Lam=%-7.1f lam=%-4d maxsum=%.4f"
              % (y, cap, s["n"], s["Lam"], s["lam"], s["maxsum"]))
        sys.stdout.flush()
