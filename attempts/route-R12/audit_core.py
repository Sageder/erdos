"""Independent audit toolkit for LADDER.md (route-R12).
Everything recomputed from scratch: no import of route-R12 code.
"""
from sympy import factorint, primerange, isprime


def nu(m, p):
    e = 0
    while m % p == 0:
        m //= p
        e += 1
    return e


def digits(m, b):
    d = []
    while m:
        d.append(m % b)
        m //= b
    return d


def sdig(m, b):
    return sum(digits(m, b))


def carries(a, b, base):
    """number of carries when adding a+b in given base (Kummer)."""
    c = 0
    carry = 0
    while a or b or carry:
        s = a % base + b % base + carry
        carry = 1 if s >= base else 0
        c += carry
        a //= base
        b //= base
    return c


def legendre(m, p):
    """nu_p(m!)"""
    s = 0
    q = p
    while q <= m:
        s += m // q
        q *= p
    return s


def in_S_direct(n, k):
    """DIRECT definition: ((n+k)!)^2 | (2n)!  via Legendre for every prime <= n+k."""
    if 2 * n < 2 * (n + k):
        pass
    for p in primerange(2, n + k + 1):
        if legendre(2 * n, p) < 2 * legendre(n + k, p):
            return False
    return True


def in_S_digitsum(n, k):
    """PROBLEM.md form: forall p: 2 s_p(n+k) - s_p(2n) >= 2k."""
    for p in primerange(2, n + k + 1):
        if 2 * sdig(n + k, p) - sdig(2 * n, p) < 2 * k:
            return False
    return True


def in_S_ladder_criterion(n, k):
    """LADDER.md Section 1: for every prime l | (n+1)...(n+k):
       c_l(n) >= 2 sum_j nu_l(n+j)."""
    prod_primes = set()
    for j in range(1, k + 1):
        prod_primes |= set(factorint(n + j).keys())
    for l in prod_primes:
        demand = 2 * sum(nu(n + j, l) for j in range(1, k + 1))
        if carries(n, n, l) < demand:
            return False
    return True


def in_S_product(n, k):
    """product form: prod_{j=n-k+1}^{n+k} j | C(2n, n+k), for n >= k."""
    from math import comb
    P = 1
    for j in range(n - k + 1, n + k + 1):
        P *= j
    return comb(2 * n, n + k) % P == 0
