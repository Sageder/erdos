#!/usr/bin/env python3
"""mk.py T N B u v outfile  -- build a problem file for search.c

B  : smoothness bound for gadget mode (primes <= B are unconstrained).
     Pass B=0 for exact mode (then the universe is pruned for the target u/v).
u/v: the exact target (used in mode 1; also fixes the universe pruning).
"""
import sys
from fractions import Fraction
import universe as UV
from sympy import factorint

T = int(sys.argv[1]); N = int(sys.argv[2]); B = int(sys.argv[3])
u = int(sys.argv[4]); v = int(sys.argv[5]); out = sys.argv[6]
rho = Fraction(u, v)
U = UV.build(T, N, rho, smoothB=B)
if not U:
    print("EMPTY UNIVERSE")
    sys.exit(1)
L = UV.lcm_of(U, rho)
tot = sum(Fraction(1, n) for n in U)
D = 1; M = 1
for p, e in factorint(L).items():
    if p <= B:
        D *= p ** e
    else:
        M *= p ** e
with open(out, "w") as f:
    f.write("%d %d %d %d %d\n" % (T, N, B, u, v))
    f.write("%d\n" % len(U))
    f.write(" ".join(map(str, U)) + "\n")
print("wrote %s |univ|=%d maxsum=%.5f Lbits=%d Dbits=%d Mbits=%d target=%s reachable=%s"
      % (out, len(U), float(tot), L.bit_length(), D.bit_length(), M.bit_length(), rho, tot >= rho))
