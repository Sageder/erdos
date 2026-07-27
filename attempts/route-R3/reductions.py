"""Numerically falsify/confirm the structural reductions BEFORE proving them.

Claim R1: n in S_1  <=>  (n+1)^2 | C(2n,n).
Claim R2: n in S_2  <=>  ((n+1)(n+2))^2 | C(2n,n).
Claim R3 (per-prime, k=1): n in S_1 <=> for every prime p | n+1:
         carries_p(n+n) >= 2*nu_p(n+1).   (primes not dividing n+1 impose nothing)
Claim R4 (per-prime, k=2): n in S_2 <=> for every prime p | (n+1)(n+2):
         carries_p(n+n) >= 2*nu_p(n+1) + 2*nu_p(n+2).
Claim R5: carries_p(n+n) = nu_p(C(2n,n)) = (2*s_p(n) - s_p(2n))/(p-1).
"""
from sympy import binomial, factorint
from membership import in_Sk, s_p, carries

def nu(m, p):
    v = 0
    while m % p == 0:
        v += 1
        m //= p
    return v

N = 3000
for n in range(1, N + 1):
    C = binomial(2 * n, n)
    # R1
    r1 = (C % (n + 1) ** 2 == 0)
    assert r1 == in_Sk(n, 1), ("R1 fails", n)
    # R2
    r2 = (C % ((n + 1) * (n + 2)) ** 2 == 0)
    assert r2 == in_Sk(n, 2), ("R2 fails", n)
    # R3
    r3 = all(carries(n, n, p) >= 2 * e for p, e in factorint(n + 1).items())
    assert r3 == in_Sk(n, 1), ("R3 fails", n)
    # R4
    f = factorint(n + 1)
    g = factorint(n + 2)
    allp = set(f) | set(g)
    r4 = all(carries(n, n, p) >= 2 * f.get(p, 0) + 2 * g.get(p, 0) for p in allp)
    assert r4 == in_Sk(n, 2), ("R4 fails", n)
    # R5 on a few primes
    if n <= 300:
        for p in (2, 3, 5, 7, 11, 13):
            lhs = carries(n, n, p)
            num = 2 * s_p(n, p) - s_p(2 * n, p)
            assert num % (p - 1) == 0
            assert lhs == num // (p - 1) == nu(C, p), ("R5 fails", n, p)
print(f"R1-R5 all confirmed for n <= {N}")
