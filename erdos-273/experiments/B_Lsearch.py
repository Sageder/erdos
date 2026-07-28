"""
B_Lsearch.py -- Route B: which L give the largest E-budget / H-budget among their divisors?

CLAIM TESTED
------------
A covering system whose moduli all divide L must satisfy   sum_{n | L, n in E} 1/n  >  1
(Davenport-Mirsky-Newman-Rado forbids equality with distinct moduli).  This script searches
over smooth L (bounded size and bounded divisor count) for the maximum of
    bE(L) = sum_{n | L, n >= 4, n+1 prime} 1/n
and of the halved-world analogue bH(L) = sum_{m | L, m >= 2, 2m+1 prime} 1/m.
It is the feasibility screen for the flat (root) step of the Route-B tree.

CONCLUSION: printed table; recorded in attempts/route-B-recursive/FINDINGS.md
"""
import sys, heapq
from sympy import isprime

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]


def sieve(n):
    bs = bytearray([1]) * (n + 1)
    bs[0:2] = b"\x00\x00"
    i = 2
    while i * i <= n:
        if bs[i]:
            bs[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
        i += 1
    return bs


def budgets(fac, isp, Lmaxsieve):
    """(bE, bH, #div, list of E-divisors) for L = prod p^a; needs a prime sieve up to 2L+1."""
    ds = [1]
    for p, a in fac:
        ds = [d * p ** i for d in ds for i in range(a + 1)]
    bE = 0.0
    bH = 0.0
    NE = []
    for d in ds:
        if d >= 4 and d + 1 <= Lmaxsieve and isp[d + 1]:
            bE += 1.0 / d
            NE.append(d)
        if d >= 2 and 2 * d + 1 <= Lmaxsieve and isp[2 * d + 1]:
            bH += 1.0 / d
    return bE, bH, len(ds), NE


def main():
    Lmax = float(sys.argv[1]) if len(sys.argv) > 1 else 3e8
    dmax = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    SIEVE = int(2 * Lmax + 10)
    if SIEVE > 8e8:
        SIEVE = int(8e8)
    print(f"sieving to {SIEVE} ...", flush=True)
    isp = sieve(SIEVE)
    res = []
    # enumerate exponent vectors with L <= Lmax and #div <= dmax
    def rec(i, L, nd, fac):
        if i == len(PRIMES):
            if L >= 4:
                bE, bH, ndv, NE = budgets(fac, isp, SIEVE)
                res.append((bE, bH, L, ndv, tuple(fac)))
            return
        p = PRIMES[i]
        pw = 1
        a = 0
        while True:
            if L * pw > Lmax or nd * (a + 1) > dmax:
                break
            rec(i + 1, L * pw, nd * (a + 1), fac + ([(p, a)] if a else []))
            a += 1
            pw *= p
    rec(0, 1, 1, [])
    print(f"candidates: {len(res)}")
    res.sort(reverse=True)
    print("\nTOP by bE (E-world flat feasibility):")
    for r in res[:20]:
        print(f"  bE={r[0]:.5f} bH={r[1]:.5f} L={r[2]:<14} #div={r[3]:<7} {dict(r[4])}")
    res.sort(key=lambda r: -r[1])
    print("\nTOP by bH (H-world):")
    for r in res[:20]:
        print(f"  bH={r[1]:.5f} bE={r[0]:.5f} L={r[2]:<14} #div={r[3]:<7} {dict(r[4])}")


if __name__ == "__main__":
    main()
