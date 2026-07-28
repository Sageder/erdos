"""
F_infimum.py -- Route F, Erdos 273, task (b).

CLAIM TESTED (and PROVED by the construction this script instantiates):

  THEOREM.  inf { sum_i 1/n_i : {a_i mod n_i} a covering system of Z with
                  pairwise distinct moduli n_i > 1 }  =  1,
  and the infimum is NOT attained.

  Lower bound / non-attainment: sum_i 1/n_i >= 1 always (density), with
  equality iff the classes partition Z; by the Davenport-Mirsky-Newman-Rado
  theorem an exact cover of Z by k >= 2 classes has its largest modulus
  repeated, and k = 1 forces modulus 1.  Hence sum_i 1/n_i > 1 strictly.

  Upper bound (the DOUBLING STAIRCASE): let C = {b_i mod m_i}_{i<=k} be ANY
  covering system with distinct moduli m_i > 1 and cost c = sum 1/m_i.  For
  m >= 1 define  D(C, m) :=
        { 0 mod 2, 1 mod 4, 3 mod 8, ..., 2^{j-1}-1 mod 2^j, ..., 2^{m-1}-1 mod 2^m }
      U { (2^m - 1) + 2^m b_i   mod   2^m m_i   :  i = 1..k }.
  The staircase classes cover every x with x not congruent to 2^m - 1 (mod 2^m);
  and x = 2^m-1+2^m y is covered because y lies in some b_i mod m_i.  The moduli
  2, 4, ..., 2^m are distinct, the moduli 2^m m_i are distinct and all >= 2^{m+1},
  so the whole list has pairwise distinct moduli > 1.  Its cost is
        (1 - 2^-m) + 2^-m c   =  1 + 2^-m (c - 1).
  Iterating from the classical c = 4/3 gives cost 1 + 1/(3*2^m) -> 1.       QED

This script builds D(C,m) for many m, VERIFIES the covering property
exhaustively modulo L = lcm, verifies distinctness, and checks the cost
formula in exact rational arithmetic.

CONCLUSION: verified for m = 0..12 (and, with the 4/3 seed, cost
1 + 1/(3*2^m), waste = 4 modulo L = 3*2^{m+2}).  So the "reciprocal budget"
of a set of admissible moduli can NEVER by itself rule out the existence of a
covering system as long as that budget exceeds 1.
"""
from fractions import Fraction
from math import lcm
import sys

CLASSIC = [(2, 0), (3, 0), (4, 1), (6, 5), (12, 7)]      # (modulus, residue)


def staircase(C, m):
    """D(C,m) as in the header.  C = list of (modulus, residue)."""
    out = [(2 ** j, 2 ** (j - 1) - 1) for j in range(1, m + 1)]
    out += [(2 ** m * n, (2 ** m - 1) + 2 ** m * a) for (n, a) in C]
    return [(n, a % n) for (n, a) in out]


def verify(C, verbose=True):
    mods = [n for n, a in C]
    assert len(set(mods)) == len(mods), "moduli NOT distinct: " + str(sorted(mods))
    assert all(n > 1 for n in mods), "modulus <= 1"
    L = 1
    for n in mods:
        L = lcm(L, n)
    cov = bytearray(L)
    tot = 0
    for n, a in C:
        for x in range(a % n, L, n):
            cov[x] += 1
            tot += 1
    assert all(c >= 1 for c in cov), "NOT a covering"
    cost = sum(Fraction(1, n) for n in mods)
    waste = tot - L
    assert cost - 1 == Fraction(waste, L)
    if verbose:
        print(f"  k={len(C):3} L={L:<12} cost={cost} = {float(cost):.10f} "
              f"excess={cost-1} waste={waste}")
    return L, cost, waste


if __name__ == "__main__":
    mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print("seed = classical system", CLASSIC)
    verify(CLASSIC)
    print("\ndoubling staircase D(classical, m):")
    for m in range(0, mmax + 1):
        C = staircase(CLASSIC, m)
        L, cost, waste = verify(C, verbose=False)
        pred = 1 + Fraction(1, 3 * 2 ** m)
        assert cost == pred, (cost, pred)
        print(f"  m={m:<3} k={len(C):3} L={L:<12} cost={cost} = {float(cost):.12f}"
              f"  excess={cost-1} = 1/(3*2^{m})  waste·(1/L)={waste}/{L}")
    print("\n  -> excess -> 0 : the infimum over distinct-moduli covering systems is 1.")

    # also iterate the construction (staircase of a staircase) as a cross-check
    print("\niterated: D(D(classical,3),3) etc.")
    C = CLASSIC
    for it in range(3):
        C = staircase(C, 3)
        L, cost, waste = verify(C, verbose=False)
        print(f"  iterate {it+1}: k={len(C)} L={L} cost={cost} = {float(cost):.12f}")
