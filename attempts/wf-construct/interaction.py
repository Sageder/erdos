#!/usr/bin/env python3
"""
interaction.py -- THE INTERACTION BETWEEN PRIMES, made precise.

Two exact statements are produced here.

(A)  DECOUPLING LEMMA (PROVED, and verified exactly below).
     In the designed universe A(T,N,z0,z) of build.py every element n has
     AT MOST ONE prime factor > z0: indeed n is either z0-smooth, or
     n = p*a with p = P(n) in (z0,z] and P(a) <= z0.  Consequently, for two
     distinct primes p,q > z0 the sets  {n in A : p | n}  and
     {n in A : q | n}  are DISJOINT, so the Rule (P) congruences at p and at q
     constrain disjoint sets of binary variables: among the large primes the
     interaction is switched off by construction.  What remains coupled is
     exactly the set of primes <= z0, and their joint condition is a single
     exact condition modulo the FIXED SMOOTH modulus
          L0 = prod_{r <= z0} r^{floor(log_r N)}.

(B)  THE STORMER WALL (a NEGATIVE result: why no "descent" construction can
     work).  A construction that fixes the primes one at a time from the
     largest downwards, using at each prime p only moves that are NEUTRAL for
     every larger prime, must use blocks all of whose elements are p-smooth.
     For a block of length 2 this asks for n, n+1 both p-smooth inside [T,N].
     This script counts those pairs EXACTLY.  They die out fast as p decreases
     (for FIXED p and T -> infinity there are only finitely many by Stormer's
     classical theorem, but we do not need that: the exact counts below are
     already zero or tiny in the ranges we use).  Hence a pure top-down
     descent stalls at a smoothness bound of order (a small power of) N, and
     the SMALL primes must be handled jointly with the large ones.  That is
     precisely the coupling that the designed universe of (A) confines to the
     single modulus L0.

usage: interaction.py T N [z0]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import largest_prime_factor_sieve, primes_upto


def main():
    T, N = int(sys.argv[1]), int(sys.argv[2])
    z0 = int(sys.argv[3]) if len(sys.argv) > 3 else 23
    lpf = largest_prime_factor_sieve(N + 1)

    # ---------- (A) verify the decoupling on the designed universe ----------
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from build import designed_universe
    A, S0, rough = designed_universe(T, N, z0)
    Aset = set(A)
    bad = 0
    for n in A:
        big = []
        m = n
        for p in primes_upto(min(N, m)):
            if p * p > m:
                break
            while m % p == 0:
                m //= p
                if p > z0:
                    big.append(p)
        if m > 1 and m > z0:
            big.append(m)
        if len(set(big)) > 1:
            bad += 1
            print("  DECOUPLING VIOLATED at", n, big)
    print(f"(A) designed universe [{T},{N}] z0={z0}: |A|={len(A)}, "
          f"elements with >1 prime factor > z0: {bad}   (must be 0)")
    # pairwise disjointness of the large-prime multiple sets
    seen = {}
    clash = 0
    for p in sorted(rough):
        for n in rough[p]:
            if n in seen and seen[n] != p:
                clash += 1
            seen[n] = p
    print(f"    large-prime multiple sets pairwise disjoint: {clash == 0}")

    # ---------- (B) the Stormer wall ----------
    print(f"\n(B) number of n in [{T},{N-1}] with n and n+1 both y-smooth:")
    print(f"{'y':>6} {'pairs':>8} {'y-smooth n':>11}")
    for y in primes_upto(min(N, 400)):
        cnt = sum(1 for n in range(T, N) if lpf[n] <= y and lpf[n + 1] <= y)
        sm = sum(1 for n in range(T, N + 1) if lpf[n] <= y)
        print(f"{y:>6} {cnt:>8} {sm:>11}")
        if cnt > (N - T) // 4:
            break


if __name__ == "__main__":
    main()
