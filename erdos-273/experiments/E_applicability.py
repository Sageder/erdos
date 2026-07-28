"""
CLAIM TESTED (Route E, literature applicability checks).

For each imported theorem the question "do its hypotheses hold for
    E = {p-1 : p prime, p >= 5} = {4,6,10,12,16,18,22,28,30,36,40,42,46,52,58,60,...}"
requires a few exact facts about E.  This script computes them.

Facts computed:
 (1) min E = 4, and the growth of the reciprocal budget  B(X) = sum_{n in E, n <= X} 1/n
     compared with ln ln X (Mertens for shifted primes).
 (2) whether every element of E is even  (relevant to Hough-Nielsen);
     whether elements of E are squarefree (relevant to BBMST / Cummings-Filaseta-Trifonov).
 (3) divisibility pairs inside E (relevant to Schinzel's conjecture, proved by BBMST):
     a covering system with distinct moduli must contain n_i | n_j, i != j.
 (4) smallest X with B(X) > 1, and the corresponding lcm.
Deterministic, exact where it matters (Fraction), floats only for display.
"""
from fractions import Fraction
from math import lcm, log
from sympy import isprime, factorint


_SIEVE_LIMIT = 10 ** 7 + 2
_sieve = bytearray([1]) * _SIEVE_LIMIT
_sieve[0] = _sieve[1] = 0
for _i in range(2, int(_SIEVE_LIMIT ** 0.5) + 1):
    if _sieve[_i]:
        _sieve[_i * _i::_i] = bytearray(len(_sieve[_i * _i::_i]))


def _isprime(n):
    if n < _SIEVE_LIMIT:
        return bool(_sieve[n])
    return isprime(n)


def E_upto(X):
    return [n for n in range(4, X + 1) if _isprime(n + 1)]


def main():
    print("=" * 78)
    print("(1) minimum of E and reciprocal budget growth")
    E = E_upto(200)
    print("  E cap [4,200] =", E)
    print("  min E =", min(E), " (4 = 5-1, 5 prime) -> the least modulus available is 4")
    print("   X        |E cap [4,X]|   B(X)=sum 1/n      ln ln X    B(X)-ln ln X")
    # exact rational sum only for the small ranges (denominators explode otherwise);
    # for the large ranges a float sum in increasing order is amply accurate for a
    # log log comparison.
    for k in range(2, 8):
        X = 10 ** k
        Ek = E_upto(X)
        if k <= 4:
            B = float(sum(Fraction(1, n) for n in Ek))
        else:
            B = sum(1.0 / n for n in Ek)
        print("  10^%d    %10d    %12.6f   %10.6f   %+10.6f"
              % (k, len(Ek), B, log(log(X)), B - log(log(X))))

    print()
    print("=" * 78)
    print("(2) parity / squarefreeness of elements of E")
    E1000 = E_upto(1000)
    print("  all elements of E cap [4,1000] even? ", all(n % 2 == 0 for n in E1000))
    sf = [n for n in E1000 if all(e == 1 for e in factorint(n).values())]
    nsf = [n for n in E1000 if not all(e == 1 for e in factorint(n).values())]
    print("  squarefree elements of E cap [4,1000]: %d of %d, first ten: %s"
          % (len(sf), len(E1000), sf[:10]))
    print("  NON-squarefree elements, first ten:", nsf[:10])
    print("  => E is neither an odd set nor a squarefree set: the odd-moduli and")
    print("     squarefree-moduli theorems do not apply to E as a whole.")

    print()
    print("=" * 78)
    print("(3) divisibility pairs inside E (Schinzel's conjecture, proved by BBMST 2022:")
    print("    every covering system with distinct moduli has n_i | n_j for some i != j)")
    E200 = E_upto(200)
    pairs = [(a, b) for a in E200 for b in E200 if a < b and b % a == 0]
    print("  #{(a,b) in E^2 : a<b, a|b, b<=200} =", len(pairs))
    print("  first 20 such pairs:", pairs[:20])
    # elements of E that divide NO other element of E below 10^4
    E4 = E_upto(10 ** 4)
    Eset = set(E4)
    lonely = [a for a in E200 if not any(b % a == 0 for b in E4 if b > a)]
    print("  elements of E<=200 dividing no larger element of E below 10^4:", lonely)

    print()
    print("=" * 78)
    print("(4) where the E-budget first exceeds 1")
    tot = Fraction(0)
    for n in E_upto(10 ** 4):
        tot += Fraction(1, n)
        if tot > 1:
            print("  budget first exceeds 1 at n =", n, " with sum =", tot,
                  "=", float(tot))
            Ecut = E_upto(n)
            L = 1
            for m in Ecut:
                L = lcm(L, m)
            print("  using E cap [4,%d] (%d moduli); lcm = %d = %s"
                  % (n, len(Ecut), L, factorint(L)))
            break

    print()
    print("=" * 78)
    print("(5) small-modulus facts used when quoting Dalton-Trifonov")
    print("  4 in E:", 4 in Eset, "   6 in E:", 6 in Eset, "   60 in E:", 60 in Eset)
    print("  divisors of 360 lying in E:", [d for d in range(1, 361) if 360 % d == 0
                                            and d >= 4 and isprime(d + 1)])
    print("  sum of their reciprocals =",
          float(sum(Fraction(1, d) for d in range(1, 361)
                    if 360 % d == 0 and d >= 4 and isprime(d + 1))))


if __name__ == "__main__":
    main()
