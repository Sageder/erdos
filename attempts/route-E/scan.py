#!/usr/bin/env python3
"""
scan.py -- for a list of T, find the smallest N for which the pruned universe of
the window [T,N] is nonempty, and the smallest N for which the total available
sum reaches a given target rho.  Exact arithmetic (Fraction) only.

usage: python3 scan.py T1 T2 ...          (uses rho = 1/2, 1/3, 1)
"""
import sys
from fractions import Fraction
import universe as UV


def maxsum(U):
    return sum(Fraction(1, n) for n in U)


def scan_T(T, rhos, Nmax, step=10):
    print("=" * 78)
    firstN = None
    rows = []
    N = T + step
    while N <= Nmax:
        U = UV.build(T, N, Fraction(1, 2))
        if U:
            ms = maxsum(U)
            L = UV.lcm_of(U, Fraction(1, 2))
            rows.append((N, len(U), ms, L.bit_length()))
            if firstN is None:
                firstN = N
        else:
            rows.append((N, 0, Fraction(0), 0))
        N += step
    print("T=%d : N, |univ|, maxsum, Lbits" % T)
    for (N, k, ms, lb) in rows:
        marks = " ".join("<=%s" % r for r in rhos if ms >= r)
        print("   N=%5d |U|=%4d maxsum=%.5f Lbits=%4d   %s" % (N, k, float(ms), lb, marks))


if __name__ == "__main__":
    rhos = [Fraction(1, 3), Fraction(1, 2), Fraction(1)]
    for t in sys.argv[1:]:
        T = int(t)
        scan_T(T, rhos, Nmax=int(3.2 * T), step=max(10, T // 10))
