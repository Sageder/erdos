#!/usr/bin/env python3
"""
scan.py -- for a fixed T and target, scan over (N, z) and report the size of the
DESIGNED universe (z-smooth restriction + Rule (P)/legality fixpoint) together
with its maximal mass.  We want the SMALLEST universe whose mass comfortably
exceeds the target, because the search cost grows like c^{|A|}.

usage: scan.py T num den N1 N2 ... [-margin M]
"""
import sys, os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import primes_upto
from design import build
from math import gcd


def main():
    args = sys.argv[1:]
    margin = Fraction(13, 10)
    if "-margin" in args:
        k = args.index("-margin"); margin = Fraction(args[k + 1]); del args[k:k + 2]
    T = int(args[0]); u = int(args[1]); v = int(args[2])
    Ns = [int(x) for x in args[3:]]
    target = Fraction(u, v)
    print(f"T={T} target={target} margin={margin}")
    print(f"{'N':>7} {'z':>5} {'|A|':>6} {'bits':>5} {'maxsum':>9}")
    best = None
    for N in Ns:
        for z in primes_upto(min(N, 400)):
            if z < 11:
                continue
            A, _ = build(T, N, u, v, z)
            if not A:
                continue
            tot = sum(Fraction(1, n) for n in A)
            if tot >= target * margin:
                L = 1
                for n in A:
                    L = L * n // gcd(L, n)
                print(f"{N:>7} {z:>5} {len(A):>6} {L.bit_length():>5} {float(tot):>9.5f}")
                if best is None or len(A) < best[2]:
                    best = (N, z, len(A))
                break
    if best:
        print("best:", best)


if __name__ == "__main__":
    main()
