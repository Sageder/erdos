"""Extra verification layers for the k=1 family.

V1: DIRECT factorial divisibility ((n+1)!)^2 | (2n)! by exact big-integer arithmetic
    for all family members with n <= 3000.
V2: fast per-prime test (R3 form, only primes dividing n+1) for all members q <= 3000.
V3: exact carry counts match the proof's prediction (exactly 2 at p; 2 at q, except a
    3rd carry at q occurs iff q = 3): documents that the proof accounts for every carry.
"""
from math import factorial
from sympy import factorint
from membership import carries
from family_test import family_pairs

# V1
cnt = 0
for q, p in family_pairs(60):
    n = p * q - 1
    if n <= 3000:
        assert factorial(2 * n) % (factorial(n + 1) ** 2) == 0, (q, p, n)
        cnt += 1
print(f"V1: direct ((n+1)!)^2 | (2n)! verified for {cnt} members (n <= 3000)")

# V2
def in_S1_fast(n):
    return all(carries(n, n, ell) >= 2 * e for ell, e in factorint(n + 1).items())

tot = 0
for q, p in family_pairs(3000):
    n = p * q - 1
    assert in_S1_fast(n), (q, p)
    tot += 1
print(f"V2: fast per-prime S_1 test passed for all {tot} members with q <= 3000 "
      f"(largest n = {max(p*q-1 for q,p in family_pairs(3000))})")

# V3
for q, p in family_pairs(300):
    n = p * q - 1
    cp = carries(n, n, p)
    cq = carries(n, n, q)
    assert cp == 2, (q, p, cp)
    expected_cq = 3 if q == 3 else 2
    assert cq == expected_cq, (q, p, cq)
print("V3: carry counts are EXACTLY 2 at p, and exactly 2 at q (3 when q=3): OK")
