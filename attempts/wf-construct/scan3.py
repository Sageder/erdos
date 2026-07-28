#!/usr/bin/env python3
"""scan3.py -- like scan2 but also scans the upper smoothness cap z."""
import sys, os
from fractions import Fraction
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import designed_universe
from design import rulep_fixpoint

def main():
    a = sys.argv[1:]
    T = int(a[0]); u = int(a[1]); v = int(a[2])
    Ns = [int(x) for x in a[3].split(",")]
    Z0s = [int(x) for x in a[4].split(",")]
    Zs = [int(x) for x in a[5].split(",")]
    margin = Fraction(a[6]) if len(a) > 6 else Fraction(11, 10)
    tgt = Fraction(u, v)
    print(f"T={T} target={tgt} margin={margin}")
    print(f"{'N':>7} {'z0':>4} {'z':>5} {'|A|':>6} {'bits':>5} {'maxsum':>9}")
    best = None
    for N in Ns:
        for z0 in Z0s:
            for z in Zs:
                if z <= z0: continue
                A, S0, rough = designed_universe(T, N, z0, min(z, N))
                A = rulep_fixpoint(A, N, u, v)
                if not A: continue
                tot = sum(Fraction(1, n) for n in A)
                if tot < tgt * margin: continue
                L = 1
                for n in A: L = L * n // gcd(L, n)
                print(f"{N:>7} {z0:>4} {z:>5} {len(A):>6} {L.bit_length():>5} {float(tot):>9.5f}")
                if best is None or len(A) < best[3]:
                    best = (N, z0, z, len(A))
    print("best:", best)

main()
