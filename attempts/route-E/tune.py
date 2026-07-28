#!/usr/bin/env python3
"""
tune.py -- choose a good sub-universe for a window.

For a window [T,N], a denominator D and a prime cap y, form the universe by
(i) deleting every n with a prime power p^e || n and p > y, then (ii) running
the legality + RULE A fixpoint (universe.build with an extra pre-deletion).

Reports
   |U|          : universe size
   logN         : log2 (# legal subsets of U)  -- exact DP count, no isolated pt
   Mbits        : log2 (L/gcd(L,D)), i.e. the number of "bits of coincidence"
                  a gadget must hit
   margin       : logN - Mbits.  Heuristically the log2 of the number of
                  gadgets;  the search is easy when the margin is large AND
                  Mbits is small (empirically Mbits <~ 65 is searchable).
"""
import sys
from fractions import Fraction
from sympy import factorint
import universe as UV


def count_legal(U):
    """exact number of subsets of the integer set U with no isolated point"""
    U = sorted(U)
    a, b, c = 1, 0, 0          # 0: prev not chosen; 1: prev chosen unsupported; 2: prev chosen supported
    prev = None
    for n in U:
        adj = (prev is not None and n == prev + 1)
        na = nb = nc = 0
        if adj:
            # take n: from 0 -> 1 ; from 1 -> 2 ; from 2 -> 2
            nb += a
            nc += b + c
            # skip n: from 0 -> 0 ; from 2 -> 0 ; from 1 -> illegal
            na += a + c
        else:
            # gap: state 1 dies
            nb += a + c        # take n, starts a new run, unsupported
            na += a + c        # skip n
        a, b, c = na, nb, nc
        prev = n
    return a + c


def build_capped(T, N, rho, y):
    banned = set()
    for n in range(T, N + 1):
        m = n
        for p, e in factorint(n).items():
            if p > y:
                banned.add(n)
                break
    # run the fixpoint on [T,N] minus banned by temporarily monkeypatching
    return UV.build_with_banned(T, N, rho, banned)


if __name__ == "__main__":
    T = int(sys.argv[1]); N = int(sys.argv[2]); D = int(sys.argv[3])
    ys = [int(x) for x in sys.argv[4:]] or [10 ** 9]
    fac = dict(factorint(D))
    for y in ys:
        U = build_capped(T, N, Fraction(1, D), y)
        if not U:
            print("y=%-5d EMPTY" % y); continue
        L = UV.lcm_of(U, Fraction(1))
        M = 1
        for p, e in factorint(L).items():
            M *= p ** (e - min(fac.get(p, 0), e))
        cl = count_legal(U)
        tot = sum(Fraction(1, n) for n in U)
        print("y=%-5d |U|=%4d maxsum=%.4f Lbits=%3d Mbits=%3d log2#legal=%6.1f margin=%6.1f"
              % (y, len(U), float(tot), L.bit_length(), M.bit_length(),
                 cl.bit_length() - 1 + 0.0, cl.bit_length() - 1 - M.bit_length()))
