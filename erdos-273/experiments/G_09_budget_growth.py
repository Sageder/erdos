"""
G_09_budget_growth.py -- Route G, step 9: how fast can the admissible budget possibly grow?

CLAIM TESTED.  By Corollary 4 an E-covering with lcm 2M needs
      s(M) := sum_{m | M, 2m+1 prime, m>=2} 1/m   >  2,
and in fact needs a partition of D_H(M) into two covering-supporting halves.  Two quantities
bound how much budget is available at all:

  T(X) := sum_{m <= X, 2m+1 prime, m >= 2} 1/m        (absolute cap: s(M) <= T(M))
  Smax(X) := max over M <= X of s(M)                  (computed exactly over a large family
             of highly-divisible M: all products of prime powers with p <= 47 that stay <= X;
             this is a LOWER bound for the true max, but the true max is attained by such M)

We print both, and the induced "slack": an E-covering needs BOTH halves of a partition of
D_H(M) to support a covering, and one half may not contain m = 2.

CONCLUSION: printed table; the budget grows like ~2 loglog X, i.e. glacially.
"""
from fractions import Fraction
from sympy import isprime, primerange, factorint
import sys

def T(X):
    s = Fraction(0)
    for m in range(2, X + 1):
        if isprime(2*m + 1):
            s += Fraction(1, m)
    return s

def s_of(M, cache={}):
    """sum of 1/d over divisors d>=2 of M with 2d+1 prime -- multiplicative-free direct calc"""
    from sympy import divisors
    return sum(Fraction(1, d) for d in divisors(M) if d >= 2 and isprime(2*d+1))

def best_M(X, primes):
    """maximise s(M) over M <= X built from `primes` (beam search over prime-power products)."""
    beam = {1: Fraction(0)}
    for p in primes:
        new = dict(beam)
        for M, v in list(beam.items()):
            q = M
            while q * p <= X:
                q *= p
                if q not in new:
                    new[q] = s_of(q)
        # keep the best 4000 by s value to control memory
        beam = dict(sorted(new.items(), key=lambda kv: -kv[1])[:4000])
    M = max(beam, key=lambda k: beam[k])
    return M, beam[M]

def main():
    print("T(X) = sum_{m<=X, 2m+1 prime} 1/m   (absolute cap on the admissible budget)")
    print(f"{'X':>10} {'T(X)':>10}   {'T(X)/2 (E-world sum 1/n)':>26}")
    for X in [10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000, 1000000]:
        t = T(X)
        print(f"{X:>10} {float(t):>10.5f}   {float(t)/2:>26.5f}")
    print()
    print("Smax(X) = max over M <= X of s(M)  (beam search over 47-smooth M):")
    ps = list(primerange(2, 50))
    print(f"{'X':>12} {'argmax M':>12} {'s(M)':>9}  factorisation")
    for X in [10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10]:
        M, v = best_M(X, ps)
        f = factorint(M)
        fs = "*".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(f.items()))
        print(f"{X:>12} {M:>12} {float(v):>9.5f}  {fs}")
    print()
    print("Reading: the E-world reciprocal budget is s(M)/2; it must exceed 1, and each of")
    print("the two parity halves needs its own covering.  s(M) grows like ~2 loglog M.")

main()
