"""
CLAIM TESTED: which L are even candidates for the lcm of a covering system with all moduli in E?

  f(L) := sum of 1/n over n | L with n >= 4 and n+1 prime.
  Every covering system with moduli in E has lcm L with f(L) > 1 (all moduli divide L, and
  sum 1/n_i > 1 for distinct moduli).  f(L) - 1 is exactly the OVERLAP BUDGET available: a
  covering of Z/L by classes of total density f'(<=f) must have total multiplicity f'*L over L
  residues, so the excess (f'-1)*L bounds the number of double-covered residues.

This script sieves f(L) exactly-in-double for all L <= LMAX and reports
  (a) the minimal L with f(L) > 1  (a rigorous lower bound on the lcm of ANY qualifying system),
  (b) the L maximising f, i.e. the most promising lattices to search,
  (c) the L that are minimal under DIVISIBILITY among {f(L) > 1} -- every qualifying lcm must be
      a multiple of one of these.

CONCLUSION: printed; recorded in NOTES.md.
"""
import numpy as np
from sympy import isprime, factorint
from fractions import Fraction
import sys

LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7


def sieve_primes(N):
    bs = bytearray([1]) * (N + 1)
    bs[0] = bs[1] = 0
    i = 2
    while i * i <= N:
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
        i += 1
    return bs


def main():
    pr = sieve_primes(LMAX + 1)
    adm = [n for n in range(4, LMAX + 1) if pr[n + 1]]
    print(f"admissible moduli <= {LMAX}: {len(adm)}   budget {sum(1.0/n for n in adm):.6f}")
    f = np.zeros(LMAX + 1, dtype=np.float64)
    for n in adm:
        f[n::n] += 1.0 / n
    # (a) minimal L with f(L) > 1
    idx = np.flatnonzero(f > 1.0 + 1e-12)
    print(f"\n# L <= {LMAX} with f(L) > 1: {len(idx)}")
    Lmin = int(idx[0])
    print(f"minimal such L = {Lmin} = {factorint(Lmin)}   f = {f[Lmin]:.6f}")
    # exact rational check of the minimum
    divs = [d for d in range(4, Lmin + 1) if Lmin % d == 0 and isprime(d + 1)]
    ex = sum(Fraction(1, d) for d in divs)
    print(f"   exact f({Lmin}) = {ex} = {float(ex):.8f}  (#moduli {len(divs)})")
    assert ex > 1

    # (b) best lattices by f
    order = idx[np.argsort(-f[idx])][:25]
    print("\ntop 25 lattices L <= %d by overlap budget f(L)-1:" % LMAX)
    for L in order:
        L = int(L)
        print(f"   L = {L:<10} f = {f[L]:.6f}   overlap budget (f-1)*L = {(f[L]-1)*L:12.1f}"
              f"   {factorint(L)}")

    # (c) minimal under divisibility
    S = set(int(x) for x in idx)
    minimal = []
    for L in sorted(S):
        red = False
        for q in factorint(L):
            if (L // q) in S:
                red = True
                break
        if not red:
            minimal.append(L)
    print(f"\nminimal-under-divisibility L with f(L) > 1 (within L <= {LMAX}): {len(minimal)}")
    for L in minimal[:40]:
        print(f"   {L:<10} f={f[L]:.6f}  {factorint(L)}")
    print("\nNOTE: the lcm of any qualifying covering system must be a multiple of one of these"
          " (restricted to lcm <= LMAX; larger lcms may have other minimal ancestors).")


if __name__ == "__main__":
    main()
