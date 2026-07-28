#!/usr/bin/env python3
"""
lib.py -- shared exact utilities for the "construction with prescribed p-adic
structure" attack.  EXACT INTEGER / RATIONAL ARITHMETIC ONLY.  No float occurs
in any verification path (the only floats are in reporting/diagnostic prints,
which are clearly marked and never feed back into a decision).
"""
from fractions import Fraction
from math import gcd


# ---------------------------------------------------------------- sieves
def primes_upto(N):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= N:
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
        i += 1
    return [i for i in range(2, N + 1) if s[i]]


def largest_prime_factor_sieve(N):
    """lpf[n] = largest prime factor of n, for 0 <= n <= N (lpf[0]=lpf[1]=1)."""
    lpf = list(range(N + 1))
    for i in range(2, N + 1):
        lpf[i] = 1
    for p in range(2, N + 1):
        if lpf[p] == 1:                       # p is prime
            for m in range(p, N + 1, p):
                lpf[m] = p
    lpf[0] = 1
    if N >= 1:
        lpf[1] = 1
    return lpf


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


# ---------------------------------------------------------------- legality
def runs(U):
    """maximal runs of a sorted list/set of integers."""
    U = sorted(U)
    out = []
    if not U:
        return out
    a = b = U[0]
    for x in U[1:]:
        if x == b + 1:
            b = x
        else:
            out.append((a, b))
            a = b = x
    out.append((a, b))
    return out


def is_legal(U):
    return all(b > a for (a, b) in runs(U))


def run_count(U):
    return len(runs(U))


def capacity(U):
    return sum((b - a + 1) // 2 for (a, b) in runs(U))


def exact_sum(U):
    """Exact rational sum of reciprocals; Fraction only."""
    s = Fraction(0)
    for n in U:
        s += Fraction(1, n)
    return s


def integer_check(U, target_num, target_den):
    """Independent integer-only re-check:  sum 1/n = a/b  <=>  b*sum(L/n) = a*L
    where L = lcm(U).  Uses no Fraction at all."""
    L = 1
    for n in U:
        L = L * n // gcd(L, n)
    s = 0
    for n in U:
        assert L % n == 0
        s += L // n
    return target_den * s == target_num * L


def verify_solution(U, target=Fraction(1), minelt=None):
    """Full exact verification.  Returns (ok, info-dict)."""
    U = sorted(U)
    info = {}
    info["distinct"] = (len(set(U)) == len(U))
    info["ge2"] = all(n >= 2 for n in U)
    info["legal"] = is_legal(U)
    info["sum"] = exact_sum(U)
    info["sum_ok"] = (info["sum"] == target)
    info["int_ok"] = integer_check(U, target.numerator, target.denominator)
    info["r"] = run_count(U)
    info["cap"] = capacity(U)
    info["min"] = U[0] if U else None
    info["max"] = U[-1] if U else None
    info["minelt_ok"] = True if minelt is None else (U[0] >= minelt)
    ok = (info["distinct"] and info["ge2"] and info["legal"] and info["sum_ok"]
          and info["int_ok"] and info["minelt_ok"])
    return ok, info
