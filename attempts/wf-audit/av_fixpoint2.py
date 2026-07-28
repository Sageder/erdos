#!/usr/bin/env python3
"""
Recon-3: independent implementation of the STRONG p-adic fixpoint.

Rule A (re-derived here).  Let A be a set known to contain every solution
U (legal, U subseteq [2,N], sum 1/n = 1).  Fix a prime p, let
    e := max{ nu_p(n) : n in A },  C := { n in A : nu_p(n) = e },  e >= 1.
If U ∩ C != empty then max_{n in U} nu_p(n) = e, and multiplying sum 1/n = 1 by
p^e and reducing mod p (all other terms of U are in p Z_p after the multiplication)
gives  sum_{n in U∩C} (n/p^e)^{-1} = 0 (mod p).  Hence if NO nonempty subset of
{ (n/p^e)^{-1} mod p : n in C } sums to 0 mod p, then U ∩ C = empty and all of C
may be deleted from A.  (Testing only singletons recovers the classical
"two attainers" rule; testing all subsets by a mod-p DP is strictly stronger.)

Rule B (legality).  n in A with n-1, n+1 both absent from A can be deleted.

Both rules only delete, so iterating to a fixpoint is sound: the fixpoint still
contains every solution.  Empty fixpoint  ==>  no solution with max <= N.

This file is written from scratch (the DP and the driver), and it is used only to
CHECK the repository's claim "the fixpoint of [2,N] is empty for all N <= 76".
"""
import sys
from fractions import Fraction


def primes_upto(N):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= N:
        if s[i]:
            s[i * i:: i] = bytearray(len(s[i * i:: i]))
        i += 1
    return [i for i in range(2, N + 1) if s[i]]


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def has_nonempty_zero_subset(res, p):
    """exists nonempty T subseteq res (multiset of residues mod p) with sum = 0 mod p"""
    reach = set()          # residues attainable by a NONEMPTY subset
    for r in res:
        new = {r}
        for x in reach:
            new.add((x + r) % p)
        reach |= new
        if 0 in reach:
            return True
    return 0 in reach


def fixpoint(N, legality=True):
    A = set(range(2, N + 1))
    P = primes_upto(N)
    changed = True
    while changed:
        changed = False
        for p in P:
            while True:
                lev = {}
                e = 0
                for n in A:
                    if n % p == 0:
                        v = nu(n, p)
                        lev.setdefault(v, []).append(n)
                        e = max(e, v)
                if e == 0:
                    break
                C = lev[e]
                pe = p ** e
                res = [pow(n // pe, -1, p) for n in C]
                if has_nonempty_zero_subset(res, p):
                    break
                A -= set(C)
                changed = True
                if not A:
                    return A
        if legality:
            while True:
                hit = [n for n in A if (n - 1) not in A and (n + 1) not in A]
                if not hit:
                    break
                A -= set(hit)
                changed = True
    return A


if __name__ == "__main__":
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    lastempty = -1
    firstnonempty = None
    for N in range(2, hi + 1):
        A = fixpoint(N)
        if not A:
            lastempty = N
        elif firstnonempty is None:
            firstnonempty = N
        s = sum(Fraction(1, n) for n in A)
        flag = ""
        if N >= 70 or not A or N < 20:
            print("N=%3d  |fix|=%3d  sum=%.4f  %s" %
                  (N, len(A), float(s), sorted(A) if len(A) <= 40 else ""))
    print("largest N with EMPTY fixpoint :", lastempty)
    print("first N with NONEMPTY fixpoint:", firstnonempty)
