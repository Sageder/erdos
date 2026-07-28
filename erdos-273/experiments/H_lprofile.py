"""
H_lprofile.py -- Route H, step 1.

CLAIM TESTED: for a candidate lcm L, how much "covering material" does H supply?
For each L we list
    D_H(L) = { m : m | L, m >= 2, 2m+1 prime }        (H-world moduli available)
    budget = sum_{m in D_H(L)} 1/m
    for every prime q | L:  the multiples of q inside D_H(L) and their count.

NECESSARY CONDITION USED (proved in FINDINGS.md, Lemma L1):
  If A is the modulus set of a covering system and q is a prime with
      F_q(A) := sum_{m in A, q ∤ m} 1/m  <  1,
  then A must contain at least q moduli divisible by q; more precisely the multiples of q
  in A must be splittable into q groups each of reciprocal sum >= (1 - F_q(A))/q.

CONCLUSION: printed tables; used to choose the L's fed to H_cover.c.
"""
from sympy import isprime, factorint
from itertools import product
from fractions import Fraction
import sys


def smooth_numbers(primes, limit):
    out = [1]
    for p in primes:
        new = []
        for v in out:
            x = v
            while x <= limit:
                new.append(x)
                x *= p
        out = new
    return sorted(set(out))


def report(primes, limit, show=True):
    S = smooth_numbers(primes, limit)
    DH = [m for m in S if m >= 2 and isprime(2 * m + 1)]
    b = sum(Fraction(1, m) for m in DH)
    if show:
        print("=" * 78)
        print("primes = %s   limit = %d" % (primes, limit))
        print("  |smooth| = %d   |D_H| = %d   budget = %.5f" % (len(S), len(DH), float(b)))
        print("  D_H =", DH[:60], "..." if len(DH) > 60 else "")
        for q in primes:
            mult = [m for m in DH if m % q == 0]
            bq = sum(Fraction(1, m) for m in mult)
            print("     q=%-3d  #mult=%-4d  sum1/m=%.5f   F_q=%.5f  %s"
                  % (q, len(mult), float(bq), float(b - bq),
                     "OK(>=q)" if len(mult) >= q else "*** < q ***"))
    return DH, b


if __name__ == "__main__":
    for primes, lim in [([2, 3], 10 ** 6),
                        ([2, 3, 5], 10 ** 6),
                        ([2, 3, 5, 7], 10 ** 6),
                        ([2, 3, 5, 7, 11], 10 ** 6),
                        ([2, 3, 5, 7, 11, 13], 10 ** 6)]:
        report(primes, lim)

    print()
    print("=" * 78)
    print("How far must we go for the 2/3/5-smooth world to reach budget 1 and 2?")
    for primes in ([2, 3], [2, 3, 5], [2, 3, 5, 7]):
        S = smooth_numbers(primes, 10 ** 7)
        DH = [m for m in S if m >= 2 and isprime(2 * m + 1)]
        s = Fraction(0)
        marks = {}
        for m in DH:
            s += Fraction(1, m)
            for tgt in (1, 2):
                if tgt not in marks and s > tgt:
                    marks[tgt] = (m, float(s))
        print("  primes %s: total budget %.5f (up to 1e7);  >1 at m=%s;  >2 at m=%s"
              % (primes, float(s), marks.get(1), marks.get(2)))
