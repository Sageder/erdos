#!/usr/bin/env python3
"""
verify_certs.py -- independent exact re-verification of every certificate this
attack produced.  Imports nothing from the search code.

certs.txt line format:
    LIFT <u> <v> <T> : n1 n2 ...      claims: legal, min >= T, sum = u/v
    SOL  : n1 n2 ...                  claims: legal, sum = 1

Uses fractions.Fraction; cross-checks with sympy.Rational and with the pure
integer identity  sum_n (L/n) == L*u/v  where L = lcm of the elements.
"""
import sys
from fractions import Fraction
from math import gcd
try:
    import sympy
except Exception:
    sympy = None


def legal(S):
    s = set(S)
    return all((n - 1 in s) or (n + 1 in s) for n in s)


def runs(S):
    S = sorted(S); out, cur = [], [S[0]]
    for x in S[1:]:
        if x == cur[-1] + 1: cur.append(x)
        else: out.append(cur); cur = [x]
    out.append(cur); return out


def check(S, u, v, T):
    assert len(S) == len(set(S)), "repeated element"
    assert min(S) >= T, "min %d < %d" % (min(S), T)
    assert all(n >= 2 for n in S)
    assert legal(S), "isolated point"
    q = sum(Fraction(1, n) for n in S)
    assert q == Fraction(u, v), "sum %s != %s/%s" % (q, u, v)
    if sympy is not None:
        assert sum(sympy.Rational(1, n) for n in S) == sympy.Rational(u, v)
    L = 1
    for n in S:
        L = L // gcd(L, n) * n
    L = L // gcd(L, v) * v
    assert sum(L // n for n in S) * v == L * u, "integer identity failed"
    R = runs(S)
    return len(S), min(S), max(S), len(R), sum(len(r) // 2 for r in R)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "certs.txt"
    ok = 0
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        head, _, body = line.partition(":")
        f = head.split()
        S = [int(x) for x in body.split()]
        if f[0] == "LIFT":
            u, v, T = int(f[1]), int(f[2]), int(f[3])
        elif f[0] == "SOL":
            u, v, T = 1, 1, 2
        else:
            continue
        m, mn, mx, r, cap = check(S, u, v, T)
        ok += 1
        print("OK  %-5s sum=%d/%d  |S|=%3d min=%4d max=%5d runs=%3d cap=%3d"
              % (f[0], u, v, m, mn, mx, r, cap))
    print("verified %d certificates" % ok)
