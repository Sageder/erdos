#!/usr/bin/env python3
"""mkuniverse.py N outfile -- write the q-sieved universe for the search."""
import sys, math
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from s4_qsieve import sieve

N = int(sys.argv[1])
out = sys.argv[2]
A = sorted(sieve(N, verbose=False))
L = 1
for n in A:
    L = L * n // math.gcd(L, n)
with open(out, "w") as f:
    f.write("%d\n" % N)
    f.write(" ".join(map(str, A)) + "\n")
print("N=%d universe=%d lcm_bits=%d max=%d" % (N, len(A), L.bit_length(), A[-1]))
