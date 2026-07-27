"""Candidate family F = { n = pq - 1 : q < p odd primes, (3q+1)/2 <= p <= 2q - 1 }.

Claim F1: F is a subset of S_1.
Claim F2 (proof skeleton, to be verified digit by digit):
  - base-p digits of n are (q-1, p-1)  [i.e. n = (q-1)p + (p-1)], giving exactly the
    carries: pos0 always, pos1 iff p <= 2q-1;
  - base-q digits of n are (1, r-1, q-1) with r = p - q, giving carries: pos0 always
    (q>=3), pos1 iff r >= (q+1)/2 i.e. p >= (3q+1)/2;
  - nu_p(n+1) = nu_q(n+1) = 1, and no other prime divides n+1.
Claim F3 (Nagura step): for every prime q with 17 <= q, there exists a prime p in
  [(3q+1)/2, 2q-1]  (check numerically far out; also record small-q exceptions).
"""
from sympy import primerange, isprime, nextprime
from membership import in_Sk, carries, failing_primes

def family_pairs(qmax):
    for q in primerange(3, qmax + 1):
        lo = (3 * q + 1 + 1) // 2  # ceil((3q+1)/2); q odd => 3q+1 even, so = (3q+1)/2
        assert (3 * q + 1) % 2 == 0
        lo = (3 * q + 1) // 2
        hi = 2 * q - 1
        for p in primerange(lo, hi + 1):
            yield q, p

# F1 + F2
count = 0
for q, p in family_pairs(400):
    n = p * q - 1
    # F2: digit structure base p
    assert n == (q - 1) * p + (p - 1)
    assert 0 <= q - 1 < p
    cp = carries(n, n, p)
    assert cp >= 2, (q, p, cp)
    # F2: digit structure base q
    r = p - q
    assert 1 <= r <= q - 1
    assert n == 1 * q * q + (r - 1) * q + (q - 1)
    assert 0 <= r - 1 < q
    cq = carries(n, n, q)
    assert cq >= 2, (q, p, cq)
    # F1: full membership by the PROBLEM.md criterion over ALL primes
    assert in_Sk(n, 1), (q, p, n, failing_primes(n, 1))
    count += 1
print(f"F1,F2 verified: all {count} family members with q <= 400 are in S_1")

# Sharpness of the interval: does p = 2q+1 (just above) or p just below (3q+1)/2 fail?
sharp_hi = sharp_lo = 0
for q in primerange(3, 400):
    p = 2 * q + 1
    if isprime(p):
        n = p * q - 1
        if not in_Sk(n, 1):
            sharp_hi += 1
    # largest prime p' < (3q+1)/2 with p' > q
    from sympy import prevprime
    try:
        p2 = prevprime((3 * q + 1) // 2)
    except ValueError:
        p2 = None
    if p2 is not None and p2 > q:
        n2 = p2 * q - 1
        if not in_Sk(n2, 1):
            sharp_lo += 1
print(f"boundary p=2q+1 failures: {sharp_hi} (interval upper end is sharp if >0)")
print(f"boundary p<(3q+1)/2 failures: {sharp_lo} (lower end sharp-ish if >0)")

# F3: Nagura coverage
missing = []
for q in primerange(3, 200000):
    lo = (3 * q + 1) // 2
    hi = 2 * q - 1
    p = nextprime(lo - 1)
    if p > hi:
        missing.append(q)
print("primes q < 2*10^5 with NO valid p:", missing)

# first few members, for the writeup
mem = sorted(set(p * q - 1 for q, p in family_pairs(60)))
print("first family members:", mem[:15])
