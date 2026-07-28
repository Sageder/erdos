"""
B_closable.py -- Route B: which node moduli D can be CLOSED in one step?

CLAIM TESTED
------------
A node of the Route-B tree carrying the class r (mod D) is finished outright as soon as the
local pool  P(D) = { f >= 2 : D f + 1 prime }  contains the modulus set of some covering
system of Z with distinct moduli.  The cheapest such set is Selfridge's {2,3,4,6,12}
(reciprocal sum 4/3); so D is closable by a "Selfridge block" iff

        2D+1, 3D+1, 4D+1, 6D+1, 12D+1   are all prime,

in which case the five moduli 2D, 3D, 4D, 6D, 12D all lie in E and, with residues
r + D*{0,1,3,5,9} scaled from Selfridge's system, they cover r (mod D) exactly.

This script (a) verifies the Selfridge block identity from scratch, (b) enumerates further
small covering-system patterns with distinct moduli, and (c) scans the divisors of a given L
counting how many are closable by some pattern.

CONCLUSION: printed; recorded in attempts/route-B-recursive/FINDINGS.md

usage: python3 B_closable.py [L ...]
"""
import sys
from sympy import isprime, factorint

# Selfridge: 0 mod 2, 1 mod 3, 3 mod 4, 5 mod 6, 9 mod 12  (verified below)
SELFRIDGE = [(2, 0), (3, 1), (4, 3), (6, 5), (12, 9)]

# further patterns (modulus, residue) found by exhaustive DFS over divisors of small lcms;
# each is verified at import time.
PATTERNS = [
    SELFRIDGE,
    [(2, 0), (3, 2), (4, 1), (6, 3), (12, 7)],
    [(2, 0), (3, 1), (4, 3), (8, 5), (12, 9), (24, 17)],
    [(2, 0), (3, 1), (4, 3), (6, 5), (8, 7), (12, 9), (24, 21)],
    [(2, 0), (3, 1), (5, 3), (6, 5), (10, 7), (15, 13), (30, 29)],
    [(2, 0), (3, 1), (4, 3), (9, 5), (12, 9), (18, 11), (36, 17)],
    [(3, 0), (4, 1), (5, 2), (6, 3), (8, 7), (10, 9), (12, 11), (15, 4),
     (20, 14), (24, 19), (30, 24), (40, 34), (60, 44), (120, 104)],
]


def divisors(n):
    ds = [1]
    for p, a in factorint(n).items():
        ds = [d * p ** i for d in ds for i in range(a + 1)]
    return sorted(ds)


def lcm_list(xs):
    from math import gcd
    L = 1
    for x in xs:
        L = L * x // gcd(L, x)
    return L


def is_covering(pat):
    L = lcm_list([m for m, _ in pat])
    cov = bytearray(L)
    for m, a in pat:
        for x in range(a % m, L, m):
            cov[x] = 1
    return all(cov), L


def verify_patterns():
    ok = []
    for p in PATTERNS:
        good, L = is_covering(p)
        mods = [m for m, _ in p]
        assert len(set(mods)) == len(mods)
        if good:
            ok.append(p)
        print(f"  pattern moduli {mods}  lcm={L}  covering={good}  "
              f"weight={sum(1.0/m for m in mods):.5f}")
    return ok


def closable(D, pats):
    """returns the first pattern whose moduli all lie in P(D), else None"""
    for p in pats:
        if all(isprime(D * m + 1) for m, _ in p):
            return p
    return None


def main():
    print("verifying the closing patterns (exhaustive mod-lcm check):")
    pats = verify_patterns()
    print()
    Ls = [int(x) for x in sys.argv[1:]] or [248648400, 183783600, 86486400, 10810800]
    for L in Ls:
        ds = divisors(L)
        hits = []
        selfr = []
        for D in ds:
            if D < 2:
                continue
            p = closable(D, pats)
            if p is not None:
                hits.append((D, [m for m, _ in p]))
                if p is pats[0]:
                    selfr.append(D)
        print(f"L = {L}  ({factorint(L)})  #div={len(ds)}")
        print(f"   closable divisors: {len(hits)}   (Selfridge-closable: {len(selfr)})")
        for D, mods in hits[:25]:
            print(f"      D={D:<12} pattern {mods}")
        print()


if __name__ == "__main__":
    main()
