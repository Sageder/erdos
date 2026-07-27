"""Membership criterion for S_k = {n >= 1 : ((n+k)!)^2 | (2n)!}, reimplemented from
PROBLEM.md: n in S_k  <=>  for all primes p <= n+k:  2*s_p(n+k) - s_p(2n) >= 2k.
Exact integer arithmetic only. Cross-checked against a direct factorial-valuation test.
"""
from sympy import primerange, isprime

def s_p(m, p):
    s = 0
    while m:
        s += m % p
        m //= p
    return s

def in_Sk(n, k):
    m = n + k
    for p in primerange(2, m + 1):
        if 2 * s_p(m, p) - s_p(2 * n, p) < 2 * k:
            return False
    return True

def failing_primes(n, k):
    """Return [(p, deficit)] for primes where the condition fails."""
    m = n + k
    out = []
    for p in primerange(2, m + 1):
        d = 2 * s_p(m, p) - s_p(2 * n, p)
        if d < 2 * k:
            out.append((p, d))
    return out

def nu_p_fact(m, p):
    """Legendre: nu_p(m!)."""
    v = 0
    q = p
    while q <= m:
        v += m // q
        q *= p
    return v

def in_Sk_direct(n, k):
    """Direct check via Legendre valuations (independent cross-check)."""
    m = n + k
    for p in primerange(2, m + 1):
        if nu_p_fact(2 * n, p) < 2 * nu_p_fact(m, p):
            return False
    return True

def carries(a, b, p):
    """Number of carries when adding a+b in base p (Kummer: = nu_p(C(a+b,a)))."""
    c = 0
    cnt = 0
    while a or b or c:
        t = a % p + b % p + c
        c = 1 if t >= p else 0
        cnt += c
        a //= p
        b //= p
    return cnt

if __name__ == "__main__":
    # Sanity gate 1: S_1 up to 441 (PROBLEM.md: 40 elements, starts 5,14,27,41,44,...)
    S1 = [n for n in range(1, 442) if in_Sk(n, 1)]
    print("S_1 up to 441:", S1)
    print("count:", len(S1))
    assert len(S1) == 40
    assert S1[:14] == [5, 14, 27, 41, 44, 65, 76, 90, 109, 125, 139, 152, 155, 169]

    # Cross-check the two implementations
    for n in range(1, 500):
        for k in (1, 2, 3):
            assert in_Sk(n, k) == in_Sk_direct(n, k), (n, k)
    print("digit-form == Legendre-form for n<500, k<=3: OK")

    # Sanity gate 2: S_2 starts at 208 with the listed elements
    S2 = []
    n = 1
    while len(S2) < 20:
        if in_Sk(n, 2):
            S2.append(n)
        n += 1
    print("S_2 first 20:", S2)
    assert S2 == [208, 458, 987, 1220, 1455, 1597, 1889, 2012, 2144, 2330,
                  2477, 2663, 2991, 3353, 3415, 3430, 3439, 3475, 3476, 3551]

    # Sanity gate 3: S_3 first entries
    S3 = []
    n = 1
    while len(S3) < 4:
        if in_Sk(n, 3):
            S3.append(n)
        n += 1
    print("S_3 first 4:", S3)
    assert S3 == [3475, 8174, 8175, 15195]
    print("ALL SANITY GATES PASSED")
