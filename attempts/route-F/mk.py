#!/usr/bin/env python3
"""Write a problem file for search.c.

usage:
  mk.py gadget  x y D  outfile [cap] [lo] [hi]
      find legal U in [x,y] with denom(Sigma(U)) | D  and Sigma(U) in [lo,hi]
  mk.py exact   x y rho outfile [cap]
      find legal U in [x,y] with Sigma(U) = rho exactly

Everything here is exact integer / Fraction arithmetic.  The only inexact object
is the fixed-point sum bound written for the C prune; it is written with
DIRECTED rounding so the prune is conservative (never discards a solution).
"""
import sys
from fractions import Fraction
from math import gcd
from lib import smallest_prime_factors
from universe import prune, lcm_of

SCALE = 1 << 50


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def write_problem(fn, U, D, target, lo, hi, extra_lcm=1):
    """U: universe list.  D: allowed denominator (1 = exact mode).
    target: Fraction (exact mode) or None (gadget mode).
    lo,hi: Fractions bounding Sigma(U)."""
    L = lcm_of(U)
    if extra_lcm != 1:
        L = L // gcd(L, extra_lcm) * extra_lcm
    primes = sorted({p for n in U for p in factorset(n)})
    rows = []
    for p in primes:
        E = max(nu(n, p) for n in U)
        f = nu(D, p) if D % p == 0 else 0
        if L % p == 0:
            E = nu(L, p)
        e = E - min(E, f)
        if e <= 0:
            continue
        m = p ** e
        w = [(L // n) % m for n in U]
        if target is None:
            t = 0
        else:
            assert (target * L).denominator == 1, "target denominator must divide L"
            t = int(target * L) % m
        rows.append((p, m, t, w))
    with open(fn, "w") as g:
        g.write("%d\n" % len(U))
        g.write(" ".join(map(str, U)) + "\n")
        g.write("%d\n" % len(rows))
        for p, m, t, w in rows:
            g.write("%d %d %d\n" % (p, m, t))
            g.write(" ".join(map(str, w)) + "\n")
        LOi = lo.numerator * SCALE // lo.denominator          # floor
        HIi = -((-hi.numerator * SCALE) // hi.denominator)     # ceil
        g.write("%d %d\n" % (LOi, HIi))
    return L, rows


def factorset(n):
    s = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            s.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        s.add(n)
    return s


def main():
    mode = sys.argv[1]
    x = int(sys.argv[2]); y = int(sys.argv[3])
    spf = smallest_prime_factors(y + 2)
    if mode == "gadget":
        D = int(sys.argv[4]); fn = sys.argv[5]
        cap = int(sys.argv[6]) if len(sys.argv) > 6 else 0
        lo = Fraction(sys.argv[7]) if len(sys.argv) > 7 else Fraction(0)
        hi = Fraction(sys.argv[8]) if len(sys.argv) > 8 else Fraction(10)
        U = prune(x, y, D, spf, prime_cap=(cap or None))
        ms = sum(Fraction(1, n) for n in U)
        hi = min(hi, ms)
        L, rows = write_problem(fn, U, D, None, lo, hi)
        print("universe %d  L bits %d  primes %d  lambda %d  maxsum %s"
              % (len(U), L.bit_length(), len(rows),
                 sum((m - 1).bit_length() for _, m, _, _ in rows), float(ms)))
    else:
        rho = Fraction(sys.argv[4]); fn = sys.argv[5]
        cap = int(sys.argv[6]) if len(sys.argv) > 6 else 0
        U = prune(x, y, 1, spf, prime_cap=(cap or None))
        ms = sum(Fraction(1, n) for n in U)
        L, rows = write_problem(fn, U, 1, rho, rho, rho,
                                extra_lcm=rho.denominator)
        print("universe %d  L bits %d  primes %d  maxsum %s"
              % (len(U), L.bit_length(), len(rows), float(ms)))


if __name__ == "__main__":
    main()
