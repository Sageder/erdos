"""route-F common utilities.  EXACT ARITHMETIC ONLY (fractions.Fraction / int).

A finite U subset of Z_{>=2} is LEGAL if it has no isolated point:
every n in U has n-1 in U or n+1 in U.
Sigma(U) = sum_{n in U} 1/n.
"""
from fractions import Fraction
from math import gcd


# ---------------------------------------------------------------- legality
def is_legal(U):
    """U: iterable of ints.  Returns True iff U is legal (and all elements >= 2)."""
    S = set(U)
    if len(S) != len(list(U)):
        return False
    if any(n < 2 for n in S):
        return False
    for n in S:
        if (n - 1) not in S and (n + 1) not in S:
            return False
    return True


def runs(U):
    """maximal runs of consecutive integers, as list of (start,end) inclusive."""
    S = sorted(set(U))
    out = []
    if not S:
        return out
    a = b = S[0]
    for n in S[1:]:
        if n == b + 1:
            b = n
        else:
            out.append((a, b))
            a = b = n
    out.append((a, b))
    return out


def sigma(U):
    """exact sum of reciprocals"""
    s = Fraction(0)
    for n in U:
        s += Fraction(1, n)
    return s


def run_count(U):
    return len(runs(U))


def capacity(U):
    return sum((b - a + 1) // 2 for a, b in runs(U))


# ---------------------------------------------------------------- factoring
def smallest_prime_factors(N):
    spf = list(range(N + 1))
    i = 2
    while i * i <= N:
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf


def factor(n, spf):
    f = {}
    while n > 1:
        p = spf[n]
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        f[p] = e
    return f


def is_smooth(n, P, spf):
    while n > 1:
        p = spf[n]
        if p > P:
            return False
        while n % p == 0:
            n //= p
    return True


# ---------------------------------------------------------------- misc
def lcm(a, b):
    return a // gcd(a, b) * b


def lcm_list(xs):
    r = 1
    for x in xs:
        r = lcm(r, x)
    return r
