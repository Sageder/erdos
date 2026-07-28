#!/usr/bin/env python3
"""mkprob.py T N u v outfile  -- build the pruned universe and write a problem file."""
import sys
from fractions import Fraction
import universe as UV

T = int(sys.argv[1]); N = int(sys.argv[2]); u = int(sys.argv[3]); v = int(sys.argv[4])
out = sys.argv[5]
rho = Fraction(u, v)
U = UV.build(T, N, rho)
if not U:
    print("EMPTY UNIVERSE")
    sys.exit(1)
L = UV.lcm_of(U, rho)
tot = sum(Fraction(1, n) for n in U)
with open(out, "w") as f:
    f.write("%d %d %d %d\n" % (T, N, u, v))
    f.write("%d\n" % len(U))
    f.write(" ".join(map(str, U)) + "\n")
print("wrote %s : |univ|=%d Lbits=%d maxsum=%s (~%.5f) target=%s reachable=%s"
      % (out, len(U), L.bit_length(), tot, float(tot), rho, tot >= rho))
