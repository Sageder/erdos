#!/usr/bin/env python3
"""mkgad.py T N B outfile -- build the gadget-search universe for window [T,N]
with smoothness bound B (primes <= B are unconstrained) and write a problem file."""
import sys
from fractions import Fraction
import universe as UV

T = int(sys.argv[1]); N = int(sys.argv[2]); B = int(sys.argv[3]); out = sys.argv[4]
U = UV.build(T, N, Fraction(1), smoothB=B)
if not U:
    print("EMPTY UNIVERSE")
    sys.exit(1)
L = UV.lcm_of(U, Fraction(1))
tot = sum(Fraction(1, n) for n in U)
# D = B-smooth part of L
from sympy import factorint
D = 1
M = 1
for p, e in factorint(L).items():
    if p <= B:
        D *= p ** e
    else:
        M *= p ** e
with open(out, "w") as f:
    f.write("%d %d %d\n" % (T, N, B))
    f.write("%d\n" % len(U))
    f.write(" ".join(map(str, U)) + "\n")
print("wrote %s : |univ|=%d maxsum=%.5f  Lbits=%d  Dbits=%d (D=%d)  Mbits=%d"
      % (out, len(U), float(tot), L.bit_length(), D.bit_length(), D, M.bit_length()))
