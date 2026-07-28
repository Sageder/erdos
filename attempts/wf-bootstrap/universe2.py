#!/usr/bin/env python3
"""
universe2.py -- same PROVED fixpoint as route-E's universe.py (RULE A p-adic +
RULE B legality), rewritten to scan only the multiples of each prime instead of
the whole window.  Cross-checked against universe.py in xcheck.py.

RULE A.  Fix a prime p, let v_p = nu_p(rho), e = max{nu_p(n) : n allowed},
C = {n allowed : nu_p(n) = e}.  If e < -v_p there is no solution.  If e > -v_p
then any solution U meeting C must satisfy sum_{n in U∩C} 1/(n/p^e) == 0 mod p;
if no nonempty subset of C satisfies that congruence, all of C can be deleted.
RULE B.  An allowed n whose both neighbours are not allowed lies in no legal
subset, so delete it.
Both rules only delete elements lying in no legal solution => the fixpoint is
sound.
"""
from fractions import Fraction


def primes_upto(N):
    sieve = bytearray([1]) * (N + 1)
    sieve[0:2] = b"\x00\x00"
    i = 2
    while i * i <= N:
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(sieve[i * i:: i]))
        i += 1
    return [i for i in range(2, N + 1) if sieve[i]]


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p; e += 1
    return e


def exists_zero_subset(residues, p):
    reach = 0            # bitmask over Z/p of residues hit by a nonempty subset
    for r in residues:
        r %= p
        new = ((reach << r) | (reach >> (p - r))) & ((1 << p) - 1)
        reach |= new | (1 << r)
        if reach & 1:
            return True
    return bool(reach & 1)


def build(T, N, rho, banned=()):
    P = primes_upto(N)
    allowed = bytearray(N + 2)
    banned = set(banned)
    for n in range(T, N + 1):
        if n not in banned:
            allowed[n] = 1
    num, den = rho.numerator, rho.denominator
    vp = {p: nu(num, p) - nu(den, p) for p in P}
    # multiples of p in [T,N] with their valuations
    mult = {}
    for p in P:
        lst = []
        start = ((T + p - 1) // p) * p
        for n in range(start, N + 1, p):
            lst.append((n, nu(n, p)))
        mult[p] = lst
    changed = True
    while changed:
        changed = False
        for p in P:
            lst = mult[p]
            if not lst:
                continue
            while True:
                e = -1
                for n, x in lst:
                    if allowed[n] and x > e:
                        e = x
                if e < 0:
                    e = 0            # no allowed multiple of p at all
                if e <= -vp[p]:
                    if e < -vp[p]:
                        return None
                    break
                pe = p ** e
                C = [n for n, x in lst if allowed[n] and x == e]
                res = [pow((n // pe) % p, -1, p) for n in C]
                if exists_zero_subset(res, p):
                    break
                for n in C:
                    allowed[n] = 0
                changed = True
        while True:
            hit = [n for n in range(T, N + 1) if allowed[n]
                   and not (n - 1 >= T and allowed[n - 1])
                   and not (n + 1 <= N and allowed[n + 1])]
            if not hit:
                break
            for n in hit:
                allowed[n] = 0
            changed = True
    U = [n for n in range(T, N + 1) if allowed[n]]
    return U if U else None


def lcm_of(univ, rho):
    from math import gcd
    L = 1
    for n in univ:
        L = L // gcd(L, n) * n
    d = rho.denominator
    L = L // gcd(L, d) * d
    return L
