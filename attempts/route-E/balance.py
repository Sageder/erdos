#!/usr/bin/env python3
"""
balance.py -- the DOUBLING (scaling) map and its balance equation.

SET-UP (proved).  For a finite V subset Z_{>=2} split as V = B u G, define
    W := { 2n, 2n+1 : n in B }  u  { 2m-1, 2m : m in G }.
Then
  * every element of W is >= 2*min(V) - 1;
  * W is a disjoint union of blocks of length >= 2, i.e. LEGAL, provided the
    pairs are pairwise disjoint; the ONLY possible clash is 2n+1 = 2m-1, i.e.
    n in B and n+1 in G, so W is legal iff no n in B has n+1 in G;
  * using   1/(2n)+1/(2n+1) = 1/n - 1/(2n(2n+1))   and
            1/(2m-1)+1/(2m) = 1/m + 1/((2m-1)2m),
    sum_{x in W} 1/x  =  sum_{n in V} 1/n  -  sum_{n in B} c(2n) + sum_{m in G} c(2m-1),
    where c(k) := 1/(k(k+1)).
So W has the SAME sum as V iff the BALANCE EQUATION holds:

        sum_{n in B} c(2n)   =   sum_{m in G} c(2m-1) .                (BAL)

The left side ranges over EVEN arguments of c, the right side over ODD ones.
Hence the scaling map exists exactly when the following has a solution:

  (Q)  a set E of EVEN integers and a set O of ODD integers with
       sum_{k in E} 1/(k(k+1))  =  sum_{k in O} 1/(k(k+1)).

This script searches (Q) exhaustively in a range by meet-in-the-middle with a
64-bit modular fingerprint, followed by EXACT rational re-verification of every
candidate hit.

usage: python3 balance.py KMAX MAXTERMS
"""
import sys
from fractions import Fraction
from itertools import combinations

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60
MAXT = int(sys.argv[2]) if len(sys.argv) > 2 else 3
P = (1 << 61) - 1                     # Mersenne prime, larger than any k(k+1) here


def cmod(k):
    return pow(k * (k + 1) % P, P - 2, P)


evens = [k for k in range(2, KMAX + 1) if k % 2 == 0]
odds = [k for k in range(1, KMAX + 1) if k % 2 == 1]
print("# even arguments %d, odd arguments %d, up to %d terms per side" % (len(evens), len(odds), MAXT))

tab = {}
for t in range(1, MAXT + 1):
    for c in combinations(evens, t):
        s = 0
        for k in c:
            s = (s + cmod(k)) % P
        tab.setdefault(s, c)
print("# %d even-side fingerprints" % len(tab))

hits = []
for t in range(1, MAXT + 1):
    for c in combinations(odds, t):
        s = 0
        for k in c:
            s = (s + cmod(k)) % P
        if s in tab:
            E = tab[s]; O = c
            se = sum(Fraction(1, k * (k + 1)) for k in E)
            so = sum(Fraction(1, k * (k + 1)) for k in O)
            if se == so:
                hits.append((E, O, se))
print("# exact solutions of (Q) with k <= %d and <= %d terms per side: %d" % (KMAX, MAXT, len(hits)))
for E, O, s in hits[:40]:
    print("   even", E, " odd", O, " common value", s)
if not hits:
    print("   NONE")
