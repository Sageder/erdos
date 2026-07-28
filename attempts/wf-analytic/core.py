"""
core.py -- exact primitives for the analytic (circle-method / transfer-matrix)
attack on the CRUX of Erdos 289.

EVERYTHING HERE IS EXACT: Python ints and fractions.Fraction only.
Floats appear only in *reporting* helpers whose names start with `report_`.

DEFINITIONS USED THROUGHOUT
---------------------------
* U subset of Z_{>=2} is LEGAL if it has no isolated point (every n in U has
  n-1 in U or n+1 in U).  Equivalently: the indicator string of U has no
  isolated 1.
* For a universe V (a set of integers), legal_count(V, T, N) counts the legal
  subsets of V, where legality is with respect to the ambient integers
  (so n in U, n+1 not in U, n-1 not in U is forbidden even if n-1 not in V).
* a(M) = number of legal subsets of a full interval of M consecutive integers.

TRANSFER-MATRIX AUTOMATON (used everywhere)
-------------------------------------------
Scan n = T, T+1, ..., N.  State after processing position n:
  0 : n not in U
  1 : n in U and still UNSATISFIED (n-1 not in U); position n+1 MUST be in U
  2 : n in U and satisfied (n-1 in U)
Transitions when processing position n (weight z if n is put into U):
  from 0 : out -> 0 ; in  -> 1  (weight z)
  from 1 : out FORBIDDEN ; in -> 2 (weight z)
  from 2 : out -> 0 ; in -> 2 (weight z)
Start state 0, accepting states {0,2}.
At z = 1 the matrix is  A = [[1,1,0],[0,0,1],[1,0,1]] (rows = from, cols = to),
whose characteristic polynomial is x^3 - 2x^2 + x - 1, spectral radius
lambda = 1.7548776662466927...
"""

from fractions import Fraction
from math import isqrt, gcd


# ---------------------------------------------------------------- basic sieve
def primes_upto(n):
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            sieve[p * p:: p] = bytearray(len(sieve[p * p:: p]))
    return [i for i in range(n + 1) if sieve[i]]


def smallest_prime_factor_table(n):
    spf = list(range(n + 1))
    for p in range(2, isqrt(n) + 1):
        if spf[p] == p:
            for m in range(p * p, n + 1, p):
                if spf[m] == m:
                    spf[m] = p
    return spf


def largest_prime_factor_table(n):
    """lpf[k] = largest prime factor of k, for 2 <= k <= n.  lpf[0]=lpf[1]=1."""
    lpf = [1] * (n + 1)
    for p in range(2, n + 1):
        if lpf[p] == 1:          # p is prime
            for m in range(p, n + 1, p):
                lpf[m] = p
    return lpf


def lcm_int(a, b):
    return a // gcd(a, b) * b


def lcm_list(xs):
    L = 1
    for x in xs:
        L = lcm_int(L, x)
    return L


def lcm_interval(a, b):
    """lcm(a, a+1, ..., b) as an exact integer (a >= 1)."""
    L = 1
    for x in range(a, b + 1):
        L = lcm_int(L, x)
    return L


# ------------------------------------------------- counting legal subsets
def legal_count_mask(allowed):
    """
    allowed: list of booleans, one per consecutive ambient position.
    Returns the exact number of legal subsets U of the allowed positions
    (legality w.r.t. the whole consecutive block of positions).
    """
    s0, s1, s2 = 1, 0, 0            # before the first position
    for ok in allowed:
        n0 = s0 + s2                # put nothing here
        n1 = s0 if ok else 0        # start a new run here
        n2 = (s1 + s2) if ok else 0 # continue a run
        if not ok:
            n1 = 0
            n2 = 0
            # state 1 (previous position unsatisfied) cannot be extended:
            # those partial configurations die.
        s0, s1, s2 = n0, n1, n2
    return s0 + s2


def legal_count_interval(M):
    """a(M): number of legal subsets of an interval of M consecutive integers."""
    return legal_count_mask([True] * M)


def legal_count_universe(T, N, in_V):
    """
    in_V: callable n -> bool.  Number of legal subsets of
    V = {n in [T,N] : in_V(n)}  (legality w.r.t. the ambient interval).
    """
    return legal_count_mask([in_V(n) for n in range(T, N + 1)])


# ------------------------------------------------- harmonic sums, exact
def H(a, b):
    """sum_{n=a}^{b} 1/n as an exact Fraction (empty sum = 0)."""
    s = Fraction(0)
    for n in range(a, b + 1):
        s += Fraction(1, n)
    return s


# ---------------------------------------------- Theorem C: forced smoothness
def forced_out_bound(T, N, p):
    """
    For a prime p with p*p > N, let alpha = ceil(T/p), beta = floor(N/p),
    Q = lcm(alpha..beta), Amax = sum_{j=alpha}^{beta} Q/j  (an integer).

    LEMMA (proved in THEORY.md, Thm C).  If U subset [T,N] has
    sum_{n in U} 1/n  p-integral (in particular if the sum is an integer, or
    any rational whose denominator is prime to p), and p*p > N, and
    p > Amax, then U contains no multiple of p.

    Returns (Amax, forced) where forced is True iff p > Amax.
    """
    assert p * p > N, "lemma needs p^2 > N so that nu_p(n) <= 1 on [T,N]"
    alpha = -((-T) // p)
    beta = N // p
    if beta < alpha:
        return (0, True)          # no multiples of p in [T,N] at all
    Q = lcm_interval(alpha, beta)
    Amax = 0
    for j in range(alpha, beta + 1):
        Amax += Q // j
    return (Amax, p > Amax)


def smoothness_threshold(T, N, verbose=False):
    """
    y(T,N) := the least y such that EVERY prime p > y with p*p > N is forced
    out by forced_out_bound.  Returns max(y, isqrt(N)) so that the resulting
    y is >= sqrt(N) (primes below sqrt(N) are never constrained by the lemma).

    CONSEQUENCE (Thm C): every U subset [T,N] with integer reciprocal sum
    consists of y-smooth numbers.
    """
    root = isqrt(N)
    y = root
    for p in primes_upto(N):
        if p <= root:
            continue
        Amax, forced = forced_out_bound(T, N, p)
        if not forced:
            y = p
            if verbose:
                print(f"    p={p} NOT forced out (Amax={Amax})")
    return y


# ---------------------------------------------- lcm of the smooth universe
def lcm_smooth_universe(T, N, y, lpf=None):
    """exact lcm of V = {n in [T,N] : largest prime factor <= y}."""
    if lpf is None:
        lpf = largest_prime_factor_table(N)
    L = 1
    for n in range(T, N + 1):
        if lpf[n] <= y:
            L = lcm_int(L, n)
    return L


def smooth_mask(T, N, y, lpf=None):
    if lpf is None:
        lpf = largest_prime_factor_table(N)
    return [lpf[n] <= y for n in range(T, N + 1)]


# ------------------------------------------------------------- reporting only
def report_log(x):
    """natural log of a possibly huge exact integer -- REPORTING ONLY."""
    import math
    if x <= 0:
        return float('-inf')
    b = x.bit_length()
    if b < 900:
        return math.log(x)
    shift = b - 800
    return math.log(x >> shift) + shift * math.log(2)
