#!/usr/bin/env python3
"""
s2_block_eq_unit.py -- SUB-QUESTION 3, part 1.

Claim tested:  is  H(a,b) = 1/m  ever solvable with b > a >= 1, m >= 1 ?

Two independent attacks:

  (A) DIRECT float-filtered exhaustive scan.  For every a and every b>a with
      H(a,b) <= 1/2 we compute a double approximation of 1/H(a,b); if it is
      within 1e-6 of an integer we re-check the pair EXACTLY with Fractions.

  (B) STRUCTURAL sieve, using proved necessary conditions (see REPORT.md):
        L := b-a+1 >= 2  and  m = 1/H(a,b) <= b/L      (since H >= L/b)
        (i)  For every prime p > L there is at most one multiple of p in [a,b],
             so nu_p is uniquely maximised and  p^{nu_p(n)} | m.
             Consequently   R(a,b) := prod_{n=a}^{b} rough_L(n)   divides m,
             where rough_L(n) = n with all prime factors <= L removed.
             (The rough parts are pairwise coprime: a prime p>L dividing two
              elements would divide their difference, which is < L < p.)
             => necessary:  R(a,b) <= b/L.
        (ii) Kuerschak: the maximal 2-power 2^t in [a,b] is unique, so 2^t | m,
             and since [a,b] contains a multiple of 2^{floor(log2 L)} we get
             2^t > L/2, hence L^2 < 2b.
        (iii) a > b/2 : otherwise Bertrand gives a prime p in (b/2,b] with
             p >= a, p is its own unique multiple in [a,b], so p | m, whence
             m >= p > b/2 >= b/L, contradicting m <= b/L.
      We *verify* (i)-(iii) as filters and report every surviving pair.

Both are run over a wide range and the outcome is printed.
"""
import sys
from fractions import Fraction


def sieve_smallest_prime_factor(N):
    spf = list(range(N + 1))
    i = 2
    while i * i <= N:
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf


def attack_A(AMAX):
    """float-filtered exhaustive scan over a <= AMAX."""
    print("=== attack A: float-filtered scan, a <= %d ===" % AMAX)
    hits = []
    tested = 0
    for a in range(1, AMAX + 1):
        s = 1.0 / a
        b = a
        while True:
            b += 1
            s += 1.0 / b
            if s > 0.5000001 and b > a + 1:
                # H(a,b) <= 1/2 needed for m >= 2; m=1 impossible (Kuerschak)
                break
            if b - a + 1 < 2:
                continue
            tested += 1
            inv = 1.0 / s
            r = round(inv)
            if r >= 2 and abs(inv - r) < 1e-6:
                exact = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
                if exact == Fraction(1, r):
                    hits.append((a, b, r))
            if b > 40 * a + 100:
                break
    print("   pairs tested: %d   exact hits: %s" % (tested, hits if hits else "NONE"))
    return hits


def rough_parts(a, b, L, spf):
    """product of the parts of n in [a,b] coprime to all primes <= L; early abort."""
    prod = 1
    lim = b // L
    for n in range(a, b + 1):
        m = n
        while m > 1:
            p = spf[m]
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            if p > L:
                prod *= p ** e
                if prod > lim:
                    return None
    return prod


def attack_B(BMAX):
    """structural sieve over all b <= BMAX (uses only the proved necessary conditions)."""
    print("=== attack B: structural sieve, b <= %d ===" % BMAX)
    spf = sieve_smallest_prime_factor(BMAX + 1)
    isprime = [False] * (BMAX + 2)
    for n in range(2, BMAX + 1):
        isprime[n] = (spf[n] == n)
    # prefix count of primes for the "no prime in [a,b]" test
    pc = [0] * (BMAX + 2)
    for n in range(2, BMAX + 1):
        pc[n] = pc[n - 1] + (1 if isprime[n] else 0)
    survivors = []
    checked = 0
    for b in range(3, BMAX + 1):
        Lmax = int((2 * b) ** 0.5)          # from L^2 < 2b
        for L in range(2, Lmax + 1):
            a = b - L + 1
            if a <= b // 2:                 # need a > b/2
                continue
            if a < 2:
                continue
            if pc[b] - pc[a - 1] > 0:       # a prime in [a,b] with p>=a>b/2 kills it
                continue
            checked += 1
            R = rough_parts(a, b, L, spf)
            if R is None:
                continue
            survivors.append((a, b, L, R))
    print("   intervals passing (a>b/2, prime-free, L^2<2b): %d" % checked)
    print("   also passing the rough-part bound R <= b/L : %d" % len(survivors))
    real = []
    for (a, b, L, R) in survivors:
        s = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
        if s.numerator == 1:
            real.append((a, b, s))
    print("   exact solutions H(a,b)=1/m :", real if real else "NONE")
    if survivors[:20]:
        print("   first few survivors (a,b,L,R):", survivors[:20])
    return real


if __name__ == "__main__":
    AMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    BMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    hA = attack_A(AMAX)
    hB = attack_B(BMAX)
    print()
    print("CONCLUSION: H(a,b) = 1/m has NO solution with a <= %d (scan) "
          "and none with b <= %d (structural sieve): %s"
          % (AMAX, BMAX, (not hA) and (not hB)))
