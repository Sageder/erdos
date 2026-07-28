#!/usr/bin/env python3
"""
estimate.py -- HEURISTIC (explicitly NOT a proof) estimate of how many legal
systems inside a given universe have reciprocal sum exactly equal to a target.

Counts legal subsets by bucketed sum with a DP.  Floating point is used ONLY
here; it never touches a certificate, a verification, or a negative claim.

Expected #solutions ~ (density of the sum distribution at rho) / L.

usage: python3 estimate.py T N u v y1,y2,...
"""
import sys, math
from fractions import Fraction
from sympy import factorint
import universe as UV


def estimate(U, rho, nb=8000):
    tot = sum(1.0 / n for n in U)
    if tot < float(rho):
        return 0.0, tot
    w = tot / nb
    A = [0.0] * (nb + 2); B = [0.0] * (nb + 2); C = [0.0] * (nb + 2)
    A[0] = 1.0
    prev = None
    for n in sorted(U):
        adj = (prev is not None and n == prev + 1)
        d = int(round((1.0 / n) / w))
        NA = [0.0] * (nb + 2); NB = [0.0] * (nb + 2); NC = [0.0] * (nb + 2)
        for i in range(nb + 1):
            a, b, c = A[i], B[i], C[i]
            if a == 0.0 and b == 0.0 and c == 0.0:
                continue
            j = i + d
            if j <= nb:
                if adj:
                    NB[j] += a; NC[j] += b + c
                else:
                    NB[j] += a + c
            NA[i] += a + c
        A, B, C = NA, NB, NC
        prev = n
    dens = [A[i] + C[i] for i in range(nb + 1)]
    k = int(round(float(rho) / w))
    lo = max(0, k - 2); hi = min(nb, k + 2)
    f = sum(dens[lo:hi + 1]) / ((hi - lo + 1) * w)
    return f, tot


if __name__ == "__main__":
    T = int(sys.argv[1]); N = int(sys.argv[2]); u = int(sys.argv[3]); v = int(sys.argv[4])
    ys = [int(x) for x in sys.argv[5].split(",")]
    rho = Fraction(u, v)
    for y in ys:
        banned = set()
        if y:
            for n in range(T, N + 1):
                if max(factorint(n)) > y:
                    banned.add(n)
        U = UV.build_with_banned(T, N, rho, banned)
        if not U:
            print("y=%d EMPTY" % y); continue
        L = UV.lcm_of(U, rho)
        f, tot = estimate(U, rho)
        print("y=%-4d |U|=%4d maxsum=%.4f Lbits=%3d  log2 E[#sol] = %s"
              % (y, len(U), tot, L.bit_length(),
                 ("%.1f" % (math.log2(f) - math.log2(L))) if f > 0 else "-inf"))
