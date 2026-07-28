#!/usr/bin/env python3
"""
scale_test.py -- test the DOUBLING (scaling) map on the known certificates.

THE LEMMA (proved algebra; the numeric consequences are re-checked below).
Let V be a finite set of integers >= 2 and B subset V, G := V \ B.  Put
    W := { 2n, 2n+1 : n in B }  u  { 2m-1, 2m : m in G }.
(i)   min W >= 2 min V - 1,  max W <= 2 max V + 1.
(ii)  The blocks are pairwise disjoint unless some n in B has n+1 in G (they
      would share 2n+1); if that never happens, W is a disjoint union of blocks
      of length >= 2, hence LEGAL.
(iii) sum_{x in W} 1/x = sum_{n in V} 1/n - sum_{n in B} c(2n) + sum_{m in G} c(2m-1),
      where c(k) := 1/(k(k+1)),
      because 1/(2n)+1/(2n+1) = 1/n - c(2n) and 1/(2m-1)+1/(2m) = 1/m + c(2m-1).
Hence  sum W = sum V  <=>  BALANCE:
      sum_{n in B} g(n) = sum_{n in V} h(n),
      g(n) := c(2n-1)+c(2n) = 2/(4n^2-1),  h(n) := c(2n-1) = 1/(2n(2n-1)).

This script decides, for each certificate V, whether an ADMISSIBLE B exists
(admissible = n in B and n+1 in V forces n+1 in B).  Meet-in-the-middle with a
64-bit modular fingerprint, then EXACT rational confirmation of every candidate.
"""
import sys, os
from fractions import Fraction
import verify as V_

P = (1 << 61) - 1


def gm(n):
    return 2 * pow((4 * n * n - 1) % P, P - 2, P) % P


def hm(n):
    return pow(2 * n * (2 * n - 1) % P, P - 2, P)


def g(n):
    return Fraction(2, 4 * n * n - 1)


def h(n):
    return Fraction(1, 2 * n * (2 * n - 1))


def admissible(Vset, B):
    for n in B:
        if n + 1 in Vset and n + 1 not in B:
            return False
    return True


def find_balanced(V):
    """all admissible B with sum_B g = sum_V h ; returns a list (possibly empty)"""
    V = sorted(V); k = len(V); Vs = set(V)
    H = sum(h(n) for n in V)
    Hm = 0
    for n in V:
        Hm = (Hm + hm(n)) % P
    a, b = V[:k // 2], V[k - k // 2:] if False else V[k // 2:]
    tab = {}
    for m in range(1 << len(a)):
        s = 0
        for i in range(len(a)):
            if m >> i & 1:
                s = (s + gm(a[i])) % P
        tab.setdefault(s, []).append(m)
    out = []
    for m2 in range(1 << len(b)):
        s2 = 0
        for i in range(len(b)):
            if m2 >> i & 1:
                s2 = (s2 + gm(b[i])) % P
        need = (Hm - s2) % P
        for m1 in tab.get(need, []):
            B = {a[i] for i in range(len(a)) if m1 >> i & 1} | {b[i] for i in range(len(b)) if m2 >> i & 1}
            if not admissible(Vs, B):
                continue
            if sum(g(n) for n in B) == H:
                out.append(B)
    return out


def double_image(V, B):
    W = []
    for n in sorted(V):
        W += [2 * n, 2 * n + 1] if n in B else [2 * n - 1, 2 * n]
    return sorted(set(W)), len(W) == len(set(W))


if __name__ == "__main__":
    cases = [
        ({5, 6, 14, 15, 17, 18, 20, 21, 22, 27, 28, 33, 34, 44, 45, 54, 55, 84, 85}, Fraction(1), "1 : max 85"),
        ({6, 7, 20, 21, 44, 45, 77, 78, 90, 91}, Fraction(1, 2), "1/2 : max 91"),
        ({9, 10, 13, 14, 39, 40, 44, 45, 77, 78, 104, 105}, Fraction(1, 2), "1/2 : max 105"),
        ({19, 20, 35, 36, 44, 45, 55, 56, 57, 65, 66, 76, 77, 104, 105}, Fraction(1, 3), "1/3 : max 105"),
        ({24, 25, 27, 28, 35, 36, 54, 55, 56, 77, 78, 90, 91, 99, 100}, Fraction(1, 3), "1/3 : max 100"),
        ({6, 7, 12, 13, 35, 36, 39, 40, 44, 45, 77, 78, 104, 105}, Fraction(2, 3), "2/3 : max 105"),
    ]
    for V, rho, name in cases:
        assert sum(Fraction(1, n) for n in V) == rho
        f = find_balanced(V)
        print("%-22s |V|=%2d sum=%-4s  admissible balanced B: %d" % (name, len(V), rho, len(f)))
        for B in f[:2]:
            W, ok = double_image(V, B)
            s = sum(Fraction(1, x) for x in W)
            good, msg = V_.check(W, s, minelt=2, quiet=True)
            print("     B=%s -> legal=%s sum=%s min=%d" % (sorted(B), good, s, min(W)))
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_2_105.txt")
    if os.path.exists(fn):
        tot = hit = 0
        for line in open(fn):
            if not line.startswith("SOL"):
                continue
            U = [int(x) for x in line.split()[1:]]
            tot += 1
            if find_balanced(U):
                hit += 1
        print("all 96 target-1 certificates in [2,105]: %d of %d admit a balanced doubling" % (hit, tot))
