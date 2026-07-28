"""
C_dfilter.py  --  Route C: a sharper UNCONDITIONAL necessary condition on a divisor
lattice L, one inequality for every divisor d of L.

LEMMA (proved here, elementary).  Let M be a covering system of Z with pairwise distinct
moduli, all dividing L.  Fix d | L and split M = M' u M'' with M' = {m in M : d | m}.
For c in Z/d write the class c + dZ.  A class a mod m with m in M'' meets c + dZ only if
a = c (mod g), g = gcd(m,d), and then the intersection is a class mod lcm(m,d) = md/g, so
its RELATIVE density inside c + dZ is g/m.  A class with m in M' lies inside a single
c + dZ, where its relative density is d/m.  Since c + dZ must be covered,

      1  <=  sum_{m in M'', a_m compatible with c} g_m/m   +   sum_{m in M'_c} d/m
         <=  A(d)                                          +   sum_{m in M'_c} d/m ,

      where   A(d) := sum_{ m in D_H(L),  d does not divide m }  gcd(m,d)/m
              D_H(L) := { m : m | L, 2m+1 prime, m >= 2 }.

The sets M'_c (c in Z/d) are disjoint, so summing the resulting bound over the d classes,

      (LEM)      sum_{m in M, d | m} 1/m   >=   1 - A(d).

Since the moduli of M are distinct divisors of L,  sum_{m in M, d|m} 1/m <= T(d) :=
sum_{m in D_H(L), d | m} 1/m.  Hence a NECESSARY CONDITION for a single H-covering inside
the lattice:

      (C1)       T(d)  >=  1 - A(d)      for every d | L.

By the Step-1 equivalence, problem 273 needs TWO H-coverings with DISJOINT modulus sets
inside one lattice, so their multiples-of-d masses add:

      (C2)       T(d)  >=  2 (1 - A(d))  for every d | L.

Both are computed exactly here (rational arithmetic via Fraction).  A lattice failing (C2)
for some d is UNCONDITIONALLY ruled out for problem 273 -- no search needed -- and the
exclusion propagates to nothing else (it is a statement about that L only), but combined
with the divisibility-monotonicity of D_H it is a genuine sieve on candidate lattices.

CONCLUSION: printed per lattice.
"""
import sys
from fractions import Fraction
from math import gcd
from sympy import isprime


def divisors(L):
    ds = []
    d = 1
    while d * d <= L:
        if L % d == 0:
            ds.append(d)
            if d != L // d:
                ds.append(L // d)
        d += 1
    return sorted(ds)


def analyse(L, verbose=True):
    ds = divisors(L)
    DH = [m for m in ds if m >= 2 and isprime(2 * m + 1)]
    B = sum(Fraction(1, m) for m in DH)
    worst1 = None
    worst2 = None
    for d in ds:
        A = sum(Fraction(gcd(m, d), m) for m in DH if m % d != 0)
        T = sum(Fraction(1, m) for m in DH if m % d == 0)
        s1 = T - (1 - A)          # (C1) needs >= 0
        s2 = T - 2 * (1 - A)      # (C2) needs >= 0
        if worst1 is None or s1 < worst1[1]:
            worst1 = (d, s1, A, T)
        if worst2 is None or s2 < worst2[1]:
            worst2 = (d, s2, A, T)
    ok1 = worst1[1] >= 0
    ok2 = worst2[1] >= 0
    if verbose:
        print(f"L = {L}   |D_H| = {len(DH)}   B_H(L) = {float(B):.6f}")
        print(f"   global budget test:  single needs B>1: {'ok' if B > 1 else 'FAILS'};"
              f"   pair needs B>2: {'ok' if B > 2 else 'FAILS -> EXCLUDED'}")
        d, s, A, T = worst1
        print(f"   (C1) worst divisor d = {d}: A(d) = {float(A):.6f}, T(d) = {float(T):.6f},"
              f" slack = {float(s):+.6f}  {'ok' if ok1 else '-> NO single H-covering'}")
        d, s, A, T = worst2
        print(f"   (C2) worst divisor d = {d}: A(d) = {float(A):.6f}, T(d) = {float(T):.6f},"
              f" slack = {float(s):+.6f}  {'ok' if ok2 else '-> NO disjoint pair: EXCLUDED'}")
    return ok1, ok2, float(B)


def main():
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            analyse(int(a))
            print()
        return
    LS = [360, 720, 2520, 5040, 27720, 32760, 50400, 55440, 75400, 75600, 110880,
          166320, 180180, 360360, 720720, 1081080, 2162160, 4324320, 10810800,
          21621600]
    excluded = []
    for L in LS:
        try:
            ok1, ok2, B = analyse(L)
        except Exception as e:
            print(L, "error", e)
            continue
        if not ok2:
            excluded.append(L)
        print()
    print("lattices excluded for problem 273 by (C2) or by B_H(L) <= 2:", excluded)


if __name__ == "__main__":
    main()
