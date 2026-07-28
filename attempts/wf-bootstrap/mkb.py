#!/usr/bin/env python3
"""
mkb.py T N mode u v D outfile [banfile] [ycap]

Same as route-E's mk.py but with an optional file of BANNED integers (one per
line or whitespace separated).  Banning elements is always sound: it only
shrinks the search space, so every system found is a genuine legal system, and
an EXHAUSTIVE negative answer is a negative answer for the banned universe only
(stated as such).

mode 1 : exact target u/v.
mode 0 : gadget mode -- denominator of the sum must divide D.
"""
import sys
from fractions import Fraction
import universe as UV
from sympy import factorint

T = int(sys.argv[1]); N = int(sys.argv[2]); mode = int(sys.argv[3])
u = int(sys.argv[4]); v = int(sys.argv[5]); D = int(sys.argv[6]); out = sys.argv[7]
banned = set()
if len(sys.argv) > 8 and sys.argv[8] not in ("-", ""):
    banned = set(int(x) for x in open(sys.argv[8]).read().split())
ycap = int(sys.argv[9]) if len(sys.argv) > 9 else 0
if ycap:
    for n in range(T, N + 1):
        if n > 1 and max(factorint(n)) > ycap:
            banned.add(n)

if mode == 1:
    rho = Fraction(u, v)
    fac = {}
else:
    fac = dict(factorint(D))
    rho = Fraction(1, D)
U = UV.build_with_banned(T, N, rho, banned)
if not U:
    print("EMPTY UNIVERSE"); sys.exit(1)
L = UV.lcm_of(U, Fraction(1) if mode == 0 else Fraction(u, v))
tot = sum(Fraction(1, n) for n in U)
with open(out, "w") as f:
    f.write("%d %d %d %d %d\n" % (T, N, mode, u, v))
    f.write("%d\n" % len(fac))
    f.write(" ".join("%d %d" % (p, e) for p, e in sorted(fac.items())) + "\n")
    f.write("%d\n" % len(U))
    f.write(" ".join(map(str, U)) + "\n")
print("wrote %s |univ|=%d maxsum=%.5f Lbits=%d" % (out, len(U), float(tot), L.bit_length()))
