#!/usr/bin/env python3
"""
scan2.py -- scan the DESIGNED universe of build.py over (N, z0) for a fixed T
and target, reporting |A|, lcm bits and the maximal mass.  We look for the
smallest |A| whose mass exceeds margin*target.

usage: scan2.py T u v -N N1,N2,... -z0 a,b,c [-margin M]
"""
import sys, os
from fractions import Fraction
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import designed_universe
from design import rulep_fixpoint


def main():
    args = sys.argv[1:]
    margin = Fraction(13, 10)
    Ns = None; Z0s = None
    if "-margin" in args:
        k = args.index("-margin"); margin = Fraction(args[k + 1]); del args[k:k + 2]
    if "-N" in args:
        k = args.index("-N"); Ns = [int(x) for x in args[k + 1].split(",")]; del args[k:k + 2]
    if "-z0" in args:
        k = args.index("-z0"); Z0s = [int(x) for x in args[k + 1].split(",")]; del args[k:k + 2]
    T = int(args[0]); u = int(args[1]); v = int(args[2])
    target = Fraction(u, v)
    print(f"T={T} target={target} margin={margin}")
    print(f"{'N':>7} {'z0':>4} {'|A|':>6} {'bits':>5} {'maxsum':>9} {'smoothpart':>10}")
    best = None
    for N in Ns:
        for z0 in Z0s:
            A, S0, rough = designed_universe(T, N, z0)
            A = rulep_fixpoint(A, N, u, v)
            if not A:
                continue
            tot = sum(Fraction(1, n) for n in A)
            sm = sum(Fraction(1, n) for n in A if n in S0)
            if tot < target * margin:
                continue
            L = 1
            for n in A:
                L = L * n // gcd(L, n)
            print(f"{N:>7} {z0:>4} {len(A):>6} {L.bit_length():>5} {float(tot):>9.5f} {float(sm):>10.5f}")
            if best is None or len(A) < best[2]:
                best = (N, z0, len(A))
    print("best:", best)


if __name__ == "__main__":
    main()
