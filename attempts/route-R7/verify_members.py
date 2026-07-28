#!/usr/bin/env python3
"""Calibration gate for route R7.

Exact membership test for S_k = { n >= 1 : ((n+k)!)^2 | (2n)! }, implemented
three independent ways, cross-checked against the sanity data in PROBLEM.md:

  (i)   direct digit criterion: forall primes p <= n+k: 2 s_p(n+k) - s_p(2n) >= 2k
  (ii)  exact factorial divisibility with big integers (small n only)
  (iii) product form: prod_{j=1}^{2k} (2n+j) | binom(2n+2k, n+k)

All arithmetic exact (python ints / sympy).
"""
import sympy
from sympy import primerange, factorial, binomial

def s_p(m, p):
    s = 0
    while m:
        s += m % p
        m //= p
    return s

def in_Sk_digits(n, k):
    m = n + k
    for p in primerange(2, m + 1):
        if 2 * s_p(m, p) - s_p(2 * n, p) < 2 * k:
            return False
    return True

def in_Sk_factorial(n, k):
    return (factorial(2 * n) % (factorial(n + k) ** 2)) == 0

def in_Sk_product(n, k):
    prod = 1
    for j in range(1, 2 * k + 1):
        prod *= 2 * n + j
    return binomial(2 * n + 2 * k, n + k) % prod == 0

def main():
    ok = True
    # --- k=1 sanity: 40 elements up to 441, starting 5,14,27,...
    s1 = [n for n in range(1, 442) if in_Sk_digits(n, 1)]
    expect_s1_head = [5, 14, 27, 41, 44, 65, 76, 90, 109, 125, 139, 152, 155, 169]
    print("k=1 head:", s1[:14])
    assert s1[:14] == expect_s1_head, "k=1 head mismatch"
    assert len(s1) == 40, f"k=1 count {len(s1)} != 40"
    # cross-check with factorial form on a few
    for n in s1[:5] + [6, 7, 13, 15]:
        assert in_Sk_factorial(n, 1) == (n in s1)
    print("k=1 OK: 40 elements up to 441, heads match, factorial cross-check OK")

    # --- k=2 sanity
    s2 = [n for n in range(1, 3600) if in_Sk_digits(n, 2)]
    expect_s2_head = [208, 458, 987, 1220, 1455, 1597, 1889, 2012, 2144, 2330,
                      2477, 2663, 2991, 3353, 3415, 3430, 3439, 3475, 3476, 3551]
    print("k=2 head:", s2[:20])
    assert s2[:20] == expect_s2_head, "k=2 head mismatch"
    assert min(s2) == 208
    for n in [208, 458, 987]:
        assert in_Sk_factorial(n, 2) and in_Sk_product(n, 2)
    assert not in_Sk_factorial(207, 2) and not in_Sk_product(100, 2)
    print("k=2 OK: heads match, 208/458/987 verified by all three methods")

    # --- k=3 sanity
    s3 = [n for n in range(1, 20000) if in_Sk_digits(n, 3)]
    expect_s3_head = [3475, 8174, 8175, 15195, 16168, 18682, 18743, 19290]
    print("k=3 head:", s3[:8])
    assert s3[:8] == expect_s3_head, "k=3 head mismatch"
    assert in_Sk_product(3475, 3)
    print("k=3 OK")

    # --- k=4 sanity
    s4 = [n for n in range(1, 60001) if in_Sk_digits(n, 4)]
    print("k=4 up to 6e4:", s4)
    assert s4 == [8174, 51984], "k=4 mismatch"
    assert in_Sk_product(8174, 4)
    print("k=4 OK")

    print("ALL CALIBRATION CHECKS PASSED")

if __name__ == "__main__":
    main()
