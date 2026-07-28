#!/usr/bin/env python3
"""
Multiplicative structure mining over CORPUS.txt.  Exact integer arithmetic only.

(1) largest-prime-factor distribution of elements (smoothness);
(2) for each prime p and each solution, the set of multiples of p used, and the
    exact Rule-(P) residue check  sum_{p|n} p^E/n = 0 mod p^E;
(3) how the multiples of a given prime pair up  (the "cofactor multiset" C_p(U)
    = { n/p^{nu_p(n)} ... } and more usefully  M_p(U) = { n/p : p|n } );
(4) which primes are ALWAYS present / never present.
"""
import sys
from collections import Counter, defaultdict
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, runs_of, stat

NMAX = 4000
spf = list(range(NMAX + 1))
for i in range(2, int(NMAX ** .5) + 1):
    if spf[i] == i:
        for j in range(i * i, NMAX + 1, i):
            if spf[j] == j:
                spf[j] = i


def factor(n):
    f = {}
    while n > 1:
        p = spf[n]
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        f[p] = e
    return f


def lpf(n):
    return max(factor(n))


def primes_upto(n):
    return [p for p in range(2, n + 1) if spf[p] == p]


if __name__ == "__main__":
    S = load()
    P = primes_upto(400)

    # ---- (1) smoothness ------------------------------------------------
    lpf_cnt = Counter()
    ratio_hist = Counter()          # floor(10 * lpf(n) / N)
    for U in S:
        N = U[-1]
        for n in U:
            q = lpf(n)
            lpf_cnt[q] += 1
            ratio_hist[min(10, (10 * q) // N)] += 1
    tot = sum(lpf_cnt.values())
    print("=== largest prime factor of elements: total %d element-occurrences" % tot)
    print("top 25 lpf values (value: share):")
    for q, c in lpf_cnt.most_common(25):
        print("   %4d : %7.4f%%" % (q, 100.0 * c / tot))
    print("share of elements with lpf > N/2 :", lpf_cnt and
          sum(c for i, c in ratio_hist.items() if i >= 5) / tot)
    print("lpf/N decile histogram (share):",
          [round(ratio_hist[i] / tot, 4) for i in range(11)])

    # how big is lpf compared to sqrt(N)?  and to fixed constants
    for B in (13, 19, 23, 31, 37, 41, 53, 61, 71, 89, 101):
        c = sum(v for k, v in lpf_cnt.items() if k <= B)
        print("   elements that are %3d-smooth: %6.3f%%" % (B, 100.0 * c / tot))

    # ---- (2) per-prime usage counts -----------------------------------
    print("\n=== per-prime: in how many solutions does p divide some element?")
    present = Counter()
    multcount = defaultdict(Counter)   # p -> Counter(#multiples of p in U)
    for U in S:
        Us = set(U)
        for p in P:
            k = sum(1 for n in U if n % p == 0)
            if k:
                present[p] += 1
            multcount[p][k] += 1
    for p in P[:30]:
        print("   p=%3d present in %6d/%d (%5.1f%%)  #multiples histogram %s" %
              (p, present[p], len(S), 100.0 * present[p] / len(S),
               dict(sorted(multcount[p].items()))))

    # ---- (3) Rule (P) verification and top-level attainer structure ----
    print("\n=== Rule (P): top-level attainers, exact check")
    bad = 0
    attain_hist = Counter()
    for U in S[:4000]:
        for p in P:
            mults = [n for n in U if n % p == 0]
            if not mults:
                continue
            E = max(factor(n)[p] for n in mults)
            tot2 = sum(Fraction(p ** E, n) for n in mults)
            if tot2.denominator != 1 or (tot2.numerator % (p ** E)) != 0:
                bad += 1
            top = [n for n in mults if factor(n)[p] == E]
            attain_hist[(p, len(top))] += 1
    print("   Rule (P) violations in first 4000 solutions:", bad)
    tl = Counter()
    for (p, k), c in attain_hist.items():
        tl[k] += c
    print("   #top-level attainers histogram (all primes, 4000 sols):",
          dict(sorted(tl.items())))
