#!/usr/bin/env python3
"""
mk.py T N mode u v D outfile

Build a problem file for search.c.

  mode 1 : exact target u/v.  The universe is pruned by RULE A for that target.
  mode 0 : gadget mode -- any legal system whose reciprocal sum has denominator
           DIVIDING D.  The universe is pruned by RULE A with v_p = -f_p, where
           p^{f_p} || D  (so primes occurring in D are only partially free).

D is given as an integer (e.g. 3628800 = 10!).
"""
import sys
from fractions import Fraction
import universe as UV
from sympy import factorint

T = int(sys.argv[1]); N = int(sys.argv[2]); mode = int(sys.argv[3])
u = int(sys.argv[4]); v = int(sys.argv[5]); D = int(sys.argv[6]); out = sys.argv[7]
ycap = int(sys.argv[8]) if len(sys.argv) > 8 else 0     # 0 = no prime cap
banned = set()
if ycap:
    for n in range(T, N + 1):
        if max(factorint(n)) > ycap:
            banned.add(n)

if mode == 1:
    rho = Fraction(u, v)
    U = UV.build_with_banned(T, N, rho, banned)
    fac = {}
else:
    fac = dict(factorint(D))
    # universe with v_p = -f_p for p | D and v_p = 0 otherwise; realise this by
    # calling build with rho = 1/D (nu_p(1/D) = -f_p, and 0 for other p).
    rho = Fraction(1, D)
    U = UV.build_with_banned(T, N, rho, banned)

if not U:
    print("EMPTY UNIVERSE"); sys.exit(1)
L = UV.lcm_of(U, Fraction(1))
tot = sum(Fraction(1, n) for n in U)
Deff = 1
M = 1
for p, e in factorint(L).items():
    fp = min(fac.get(p, 0), e) if mode == 0 else 0
    Deff *= p ** fp
    M *= p ** (e - fp)
with open(out, "w") as f:
    f.write("%d %d %d %d %d\n" % (T, N, mode, u, v))
    f.write("%d\n" % len(fac))
    f.write(" ".join("%d %d" % (p, e) for p, e in sorted(fac.items())) + "\n")
    f.write("%d\n" % len(U))
    f.write(" ".join(map(str, U)) + "\n")
print("wrote %s |univ|=%d maxsum=%.5f Lbits=%d Deff=%d(%db) Mbits=%d"
      % (out, len(U), float(tot), L.bit_length(), Deff, Deff.bit_length(), M.bit_length()))
