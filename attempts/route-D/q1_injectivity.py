"""
Q1 (continued).  Injectivity of (a,b) -> H(a,b), and denominator structure.

INJECTIVITY TEST.  For each block [a,b] in the tested range we call
blocks_with_sum(H(a,b)) which is a COMPLETE solver: it returns *every* block
(anywhere in Z_{>=2}, of any length) whose sum equals H(a,b).  So for each
tested block the statement "no other block has this sum" is verified
absolutely, not just inside a box.

PROVED SUB-CASE (see REPORT.md): two blocks of the SAME length k with the same
sum are equal, because c -> H(c,c+k-1) is strictly decreasing.

DENOMINATOR STRUCTURE.  With D = den H(a,b), L = lcm(a..b), k = b-a+1,
t = -v_2(H) and R = prod of the k-rough parts of a..b, we record
    * v_2(D) = t                      (proved)
    * R | D                           (proved)
    * D | L                           (trivial)
    * the cofactor L/D.
"""

import sys
from fractions import Fraction
from math import gcd, isqrt

from blocks import H, blocks_with_sum, v2, max_pow2_in_block


def spf_sieve(n):
    spf = list(range(n + 1))
    i = 2
    while i * i <= n:
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf


def rough_part(n, k, spf):
    r = 1
    while n > 1:
        p = spf[n]
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if p > k:
            r *= p ** e
    return r


def injectivity(AMAX, KMAX):
    bad = []
    cnt = 0
    for a in range(2, AMAX + 1):
        for k in range(2, KMAX + 1):
            b = a + k - 1
            r = H(a, b)
            sols = blocks_with_sum(r, cmin=2)
            cnt += 1
            if sols != [(a, b)]:
                bad.append((a, b, sols))
    return cnt, bad


def denominators(AMAX, KMAX):
    spf = spf_sieve(AMAX + KMAX + 2)
    rows = []
    cof = {}
    for a in range(2, AMAX + 1):
        for k in range(2, KMAX + 1):
            b = a + k - 1
            h = H(a, b)
            D = h.denominator
            L = 1
            for n in range(a, b + 1):
                L = L * n // gcd(L, n)
            t = max_pow2_in_block(a, b)
            R = 1
            for n in range(a, b + 1):
                R *= rough_part(n, k, spf)
            assert -v2(h) == t, (a, b)
            assert D % R == 0, (a, b, D, R)
            assert L % D == 0, (a, b)
            cof[L // D] = cof.get(L // D, 0) + 1
            rows.append((a, b, h.numerator, D, L // D))
    return rows, cof


if __name__ == "__main__":
    AMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    cnt, bad = injectivity(AMAX, KMAX)
    print("INJECTIVITY: %d blocks (2<=a<=%d, 2<=k<=%d) each checked against ALL "
          "blocks in Z_{>=2} of ALL lengths." % (cnt, AMAX, KMAX))
    print("   collisions:", bad if bad else "NONE")

    rows, cof = denominators(min(AMAX, 200), min(KMAX, 10))
    print("DENOMINATORS: v_2(den)=t and R | den and den | lcm verified for all "
          "%d blocks tested." % len(rows))
    top = sorted(cof.items(), key=lambda kv: -kv[1])[:12]
    print("   distribution of the cofactor lcm(a..b)/den :", top)
    print("   fraction with den = lcm(a..b) : %d/%d" % (cof.get(1, 0), len(rows)))
