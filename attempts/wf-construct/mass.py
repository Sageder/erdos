#!/usr/bin/env python3
"""
mass.py -- for a window [T,N] and a smoothness bound z, report the exact mass
   sum_{n in V_z} 1/n,  V_z = { n in [T,N] : P(n) <= z, n in a run of length >=2 of V_z }
(the "legal mass": elements that are isolated in V_z can never be used).

This is the quantity that decides whether a z-smooth DESIGN can carry a given
target at all.  Exact Fractions; the printed decimals are diagnostics only.

usage: mass.py T N [target_num target_den]
"""
import sys, os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import largest_prime_factor_sieve, primes_upto, runs


def legal_core(S):
    """iteratively drop elements with no neighbour in S."""
    S = set(S)
    while True:
        dead = [n for n in S if (n - 1) not in S and (n + 1) not in S]
        if not dead:
            return S
        S.difference_update(dead)


def main():
    T, N = int(sys.argv[1]), int(sys.argv[2])
    tn, td = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1, 2)
    target = Fraction(tn, td)
    lpf = largest_prime_factor_sieve(N)
    print(f"[{T},{N}] target={target}")
    print(f"{'z':>6} {'|V_z|':>7} {'|core|':>7} {'mass':>10} {'atoms':>6}  {'>=target':>8}")
    for z in primes_upto(N):
        if z < 5:
            continue
        V = [n for n in range(T, N + 1) if lpf[n] <= z]
        core = legal_core(V)
        m = sum(Fraction(1, n) for n in core) if core else Fraction(0)
        atoms = sum(1 for n in core if n + 1 in core)
        flag = "YES" if m >= target else ""
        if core:
            print(f"{z:>6} {len(V):>7} {len(core):>7} {float(m):>10.5f} {atoms:>6}  {flag:>8}")
        if m >= target * 3 and z > 20:
            break


if __name__ == "__main__":
    main()
