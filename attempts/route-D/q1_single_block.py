"""
Q1.  Single blocks.

CLAIMS TESTED
  (1a) H(a,b) is never a unit fraction 1/N   [exhaustive exact scan]
  (1b) H(a,b) = H(c,d) forces (a,b)=(c,d)    [injectivity scan]
  (1c) structure of numerator / denominator  [data]

The scan uses the rigorously derived necessary condition (see REPORT.md,
Lemma Q1.2):  if H(a,b) = 1/N then  2^t <= N < b/k  where k = b-a+1 and 2^t is
the largest power of two in [a,b]; since 2^(t+1) >= k+1 this forces
      k(k+1) < 2b   i.e.   k <= (1+sqrt(8a-7))/2 .
So a full exhaustive search over unit-fraction block sums only needs k up to
O(sqrt(a)).  We ALSO run a slow brute-force with no such restriction on a
smaller range, to check the derived bound empirically.

Run:  python3 q1_single_block.py
"""

import sys
from fractions import Fraction
from math import gcd, isqrt

from blocks import H, max_pow2_in_block


def brute_all_lengths(AMAX, HCAP=Fraction(1)):
    """Fully naive: all a <= AMAX, all b with H(a,b) <= HCAP. No theory used."""
    unit = []
    seen = {}
    collisions = []
    for a in range(2, AMAX + 1):
        num, den = 0, 1
        b = a - 1
        while True:
            b += 1
            num, den = num * b + den, den * b
            g = gcd(num, den)
            num //= g
            den //= g
            if b == a:
                continue
            if Fraction(num, den) > HCAP:
                break
            if num == 1:
                unit.append((a, b, den))
            key = (num, den)
            if key in seen:
                collisions.append((seen[key], (a, b)))
            else:
                seen[key] = (a, b)
    return unit, collisions, len(seen)


def scan_with_klimit(AMAX, verbose_every=200000):
    """
    Exhaustive over the region allowed by Lemma Q1.2: k(k+1) < 2b.
    Reports any (a,b) with numerator 1, and also the closest calls.
    """
    unit = []
    best = []          # smallest numerators seen
    checked = 0
    for a in range(2, AMAX + 1):
        num, den = 0, 1
        kmax = (1 + isqrt(8 * a - 7)) // 2 + 2   # generous
        for k in range(1, kmax + 1):
            b = a + k - 1
            num, den = num * b + den, den * b
            g = gcd(num, den)
            num //= g
            den //= g
            if k < 2:
                continue
            checked += 1
            if num == 1:
                unit.append((a, b, den))
            if num <= 3:
                best.append((num, a, b))
    return unit, best, checked


def cheap_necessary_scan(AMAX):
    """
    Integer-only necessary condition:  H(a,b)=1/N  ==>  2^t <= N < b/k,
    hence  2^t * k < b.  Count how many (a,b) survive this.
    Also apply the stronger condition 2^t * R < b/k  where R = product of the
    k-rough parts (primes > k) of the elements -- see Lemma Q1.3.
    """
    # smallest prime factor sieve
    LIM = AMAX + 2 * isqrt(2 * AMAX) + 10
    spf = list(range(LIM + 1))
    i = 2
    while i * i <= LIM:
        if spf[i] == i:
            for j in range(i * i, LIM + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1

    def rough_part(n, k):
        """product of p^e || n over primes p > k"""
        r = 1
        m = n
        while m > 1:
            p = spf[m]
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            if p > k:
                r *= p ** e
        return r

    surv_2adic = 0
    surv_rough = []
    total = 0
    for a in range(2, AMAX + 1):
        kmax = (1 + isqrt(8 * a - 7)) // 2 + 2
        for k in range(2, kmax + 1):
            b = a + k - 1
            total += 1
            t = max_pow2_in_block(a, b)
            if (1 << t) * k >= b:
                continue
            surv_2adic += 1
            R = 1
            for n in range(a, b + 1):
                R *= rough_part(n, k)
                if R * (1 << t) * k >= b:
                    break
            if R * (1 << t) * k < b:
                surv_rough.append((a, b))
    return total, surv_2adic, surv_rough


def denominator_data(AMAX):
    """Which denominators occur?  Record den(H(a,b)) and gcd data."""
    from collections import Counter
    dens = Counter()
    rows = []
    for a in range(2, AMAX + 1):
        for k in range(2, 8):
            b = a + k - 1
            h = H(a, b)
            rows.append((a, k, h.numerator, h.denominator))
    return rows


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "brute"):
        AM = int(sys.argv[2]) if len(sys.argv) > 2 else 400
        unit, coll, nseen = brute_all_lengths(AM)
        print("[brute, no theory] a<=%d, all b with H<=1 : %d block sums" % (AM, nseen))
        print("   unit-fraction block sums :", unit)
        print("   collisions H(a,b)=H(c,d) :", coll)

    if mode in ("all", "scan"):
        AM = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
        unit, best, checked = scan_with_klimit(AM)
        print("[k<=~sqrt(2a) exhaustive] a<=%d, %d (a,b) pairs checked" % (AM, checked))
        print("   unit-fraction block sums :", unit)
        print("   numerator<=3 cases       :", best[:40], "(total %d)" % len(best))

    if mode in ("all", "cheap"):
        AM = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
        tot, s2, sr = cheap_necessary_scan(AM)
        print("[necessary-condition sieve] a<=%d: %d pairs, %d survive 2-adic, "
              "%d survive rough-part test" % (AM, tot, s2, len(sr)))
        print("   survivors:", sr[:50])
