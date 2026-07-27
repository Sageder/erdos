"""Core library for Erdős 727 experiments.

Claim tested here (module self-test): none — this is the shared library.
All functions use exact integer arithmetic. See calibrate.py for the calibration gate.

Definitions (PROBLEM.md):
  S_k = { n >= 1 : ((n+k)!)^2 | (2n)! }
  Digit criterion: n in S_k  <=>  for all primes p <= n+k: 2*s_p(n+k) - s_p(2n) >= 2k.
"""

from sympy import primerange, factorial, isprime


def s_p(m: int, p: int) -> int:
    """Sum of base-p digits of m."""
    s = 0
    while m:
        s += m % p
        m //= p
    return s


def nu_p_factorial(m: int, p: int) -> int:
    """Legendre: nu_p(m!) = (m - s_p(m)) / (p - 1)."""
    return (m - s_p(m, p)) // (p - 1)


def in_Sk_digit(n: int, k: int) -> bool:
    """Membership test via the digit criterion over all primes p <= n+k."""
    for p in primerange(2, n + k + 1):
        if 2 * s_p(n + k, p) - s_p(2 * n, p) < 2 * k:
            return False
    return True


def in_Sk_bigint(n: int, k: int) -> bool:
    """Ground-truth membership test via exact big-integer division."""
    return factorial(2 * n) % (factorial(n + k) ** 2) == 0


def failing_primes(n: int, k: int):
    """All primes p <= n+k violating the digit criterion."""
    return [p for p in primerange(2, n + k + 1)
            if 2 * s_p(n + k, p) - s_p(2 * n, p) < 2 * k]


def carries_add(a: int, b: int, p: int) -> int:
    """Number of carries when adding a + b in base p."""
    carries = 0
    carry = 0
    while a or b or carry:
        t = a % p + b % p + carry
        carry = 1 if t >= p else 0
        carries += carry
        a //= p
        b //= p
    return carries


def borrows_sub(a: int, b: int, p: int) -> int:
    """Number of borrows when computing a - b in base p (requires a >= b)."""
    assert a >= b
    borrows = 0
    borrow = 0
    while a or b:
        t = a % p - b % p - borrow
        borrow = 1 if t < 0 else 0
        borrows += borrow
        a //= p
        b //= p
    return borrows


def largest_prime_factor(m: int) -> int:
    from sympy import factorint
    return max(factorint(m)) if m > 1 else 1


import math
from sympy import sieve


def in_Sk_fast(n: int, k: int) -> bool:
    """Fast membership test, valid for n > 2k^2 (falls back to in_Sk_digit otherwise).

    Uses the large-prime criterion (PROBLEM.md): for p > max(sqrt(2n), 2k) the condition
    fails iff p has a multiple in (n, n+k], i.e. iff some window element n+1..n+k has a
    prime factor > sqrt(2n). For p <= sqrt(2n), checks the digit criterion directly.
    """
    if n <= 2 * k * k:
        return in_Sk_digit(n, k)
    r = math.isqrt(2 * n)  # floor sqrt(2n); primes p > r are "large" (and r >= 2k here)
    # window smoothness: every n+j (j=1..k) must be r-smooth
    for j in range(1, k + 1):
        m = n + j
        for p in sieve.primerange(2, r + 1):
            while m % p == 0:
                m //= p
            if m == 1:
                break
        if m > 1:
            return False
    # digit criterion at p <= r  (this includes all p <= 2k since r >= 2k)
    for p in sieve.primerange(2, r + 1):
        if 2 * s_p(n + k, p) - s_p(2 * n, p) < 2 * k:
            return False
    return True
