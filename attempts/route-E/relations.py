#!/usr/bin/env python3
"""
relations.py -- search for EXACT relations between block sums.

H(a,b) := sum_{n=a}^{b} 1/n.  A "push-up move" would be an identity
      H(a,b) = H(c1,d1) + ... + H(ck,dk)      with c1 > b
i.e. a block replaced by blocks strictly further out with the SAME sum.  If such
a move existed (and could be iterated) it would immediately give legal systems
with arbitrarily large minimum element.

Here we settle k = 1 and k = 2 exhaustively in a range, and k = 3 for short
blocks, by meet-in-the-middle with a 61-bit modular fingerprint plus exact
rational confirmation of every candidate.

usage: python3 relations.py BMAX DMAX
   BMAX : bound on b for the block being replaced (a < b <= BMAX)
   DMAX : bound on all elements of the replacing blocks
"""
import sys
from fractions import Fraction

BMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
DMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 600
P = (1 << 61) - 1

inv = [0] * (DMAX + 2)
for n in range(1, DMAX + 1):
    inv[n] = pow(n, P - 2, P)

# prefix sums mod P
pre = [0] * (DMAX + 2)
for n in range(1, DMAX + 1):
    pre[n] = (pre[n - 1] + inv[n]) % P


def Hm(a, b):
    return (pre[b] - pre[a - 1]) % P


def Hx(a, b):
    return sum(Fraction(1, n) for n in range(a, b + 1))


# ---- k = 1 : H(a,b) = H(c,d), c > b  (block sums injective?) ----
tab = {}
for c in range(2, DMAX):
    for d in range(c + 1, DMAX + 1):
        tab.setdefault(Hm(c, d), []).append((c, d))
n1 = 0
for a in range(2, BMAX):
    for b in range(a + 1, BMAX + 1):
        for (c, d) in tab.get(Hm(a, b), []):
            if c > b and Hx(a, b) == Hx(c, d):
                print("k=1 RELATION H(%d,%d)=H(%d,%d)" % (a, b, c, d)); n1 += 1
print("# k=1: %d push-up relations with b<=%d, elements <=%d" % (n1, BMAX, DMAX))

# ---- k = 2 : H(a,b) = H(c,d)+H(e,f) with b < c <= d < e <= f ----
n2 = 0
for a in range(2, BMAX):
    for b in range(a + 1, BMAX + 1):
        S = Hx(a, b)
        Sm = Hm(a, b)
        for c in range(b + 1, DMAX):
            if Fraction(1, c) + Fraction(1, c + 1) > S:
                continue
            acc = Fraction(0)
            for d in range(c, DMAX + 1):
                acc += Fraction(1, d)
                if d == c:
                    continue
                r = S - acc
                if r <= 0:
                    break
                # need r = H(e,f) with e > d
                rm = (Sm - Hm(c, d)) % P
                for (e, f) in tab.get(rm, []):
                    if e > d and Hx(e, f) == r:
                        print("k=2 RELATION H(%d,%d) = H(%d,%d) + H(%d,%d)" % (a, b, c, d, e, f))
                        n2 += 1
print("# k=2: %d push-up relations with b<=%d, elements <=%d" % (n2, BMAX, DMAX))
