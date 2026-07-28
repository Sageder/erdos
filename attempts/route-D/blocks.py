"""
Core library for route-D: structure theory of block sums H(a,b) = sum_{n=a}^b 1/n.

ALL arithmetic here is exact (fractions.Fraction / Python ints). No floats
appear on any verification path.

Conventions (from PROBLEM.md):
  * a block is [a,b] = {a,a+1,...,b} with b > a >= 2, so length k = b-a+1 >= 2.
  * H(a,b) = sum_{n=a}^b 1/n.
  * two blocks are disjoint iff their integer intervals are disjoint
    (adjacent blocks [a,b],[b+1,c] ARE disjoint and count as two blocks).
  * B(T) = { sum_i H(a_i,b_i) : blocks pairwise disjoint, all elements >= T }.

Key lemma used everywhere (Kuerschak / PROBLEM.md B1):

  LEMMA 2ADIC.  Let k = b-a+1 >= 2 and let 2^t be the largest power of two
  dividing some element of [a,b].  Then t >= 1, the multiple of 2^t in [a,b]
  is unique, and  v_2(H(a,b)) = -t  exactly.
  Consequently  t = -v_2(H(a,b))  is *determined by the value* H(a,b),
  and since any 2^(t+1) consecutive integers contain a multiple of 2^(t+1),
       k <= 2^(t+1) - 1.
"""

from fractions import Fraction
from functools import lru_cache
import math

# ---------------------------------------------------------------- basic sums


def _sum_frac(a, b):
    """(num,den) with num/den = sum_{n=a}^{b} 1/n, by binary splitting (no gcds)."""
    if b - a < 8:
        num, den = 0, 1
        for n in range(a, b + 1):
            num, den = num * n + den, den * n
        return num, den
    m = (a + b) >> 1
    n1, d1 = _sum_frac(a, m)
    n2, d2 = _sum_frac(m + 1, b)
    return n1 * d2 + n2 * d1, d1 * d2


def H(a, b):
    """Exact block sum sum_{n=a}^{b} 1/n as a Fraction."""
    assert 1 <= a <= b
    num, den = _sum_frac(a, b)
    return Fraction(num, den)


def v2(x):
    """2-adic valuation of a nonzero Fraction."""
    assert x != 0
    n, d = x.numerator, x.denominator
    t = 0
    while n % 2 == 0:
        n //= 2
        t += 1
    while d % 2 == 0:
        d //= 2
        t -= 1
    return t


def v2_int(n):
    t = 0
    while n % 2 == 0:
        n //= 2
        t += 1
    return t


def max_pow2_in_block(a, b):
    """t such that 2^t is the largest power of 2 dividing some element of [a,b]."""
    t = 0
    while True:
        q = 1 << (t + 1)
        # is there a multiple of 2^(t+1) in [a,b]?
        if (b // q) * q >= a:
            t += 1
        else:
            break
    return t


# --------------------------------------------- complete single-block solver


_PI_TAB = None


def _pi(n):
    """pi(n) = number of primes <= n  (cached sieve, grows on demand)."""
    global _PI_TAB
    if _PI_TAB is None or len(_PI_TAB) <= n:
        M = max(1024, 2 * n + 10)
        sieve = bytearray([1]) * (M + 1)
        sieve[0:2] = b"\x00\x00"
        i = 2
        while i * i <= M:
            if sieve[i]:
                sieve[i * i:: i] = bytearray(len(sieve[i * i:: i]))
            i += 1
        tab = [0] * (M + 1)
        c = 0
        for i in range(M + 1):
            c += sieve[i]
            tab[i] = c
        _PI_TAB = tab
    return _PI_TAB[n]


def _has_mult(a, b, q):
    """is there a multiple of q in [a,b]?"""
    return (b // q) * q >= a


def lcm_bitlen_bound(D):
    """
    Rigorous upper bound for log_2 lcm(1,...,D).
    Rosser-Schoenfeld (1962), Thm 12:  psi(x) < 1.03883 x  for all x > 0,
    and log lcm(1..D) = psi(D).  Hence log_2 lcm(1..D) < 1.03883 D / log 2
    < 1.49883 D.  We return ceil of that, +1 for safety.
    """
    return (149883 * D) // 100000 + 2


def blocks_with_sum(r, cmin=2, kcap=None, stats=None):
    """
    COMPLETE enumeration of all blocks [c,d] (length >= 2, c >= cmin) with
    H(c,d) == r, for a given positive rational r.

    Completeness proof (see LEMMA 2ADIC):
      * every block sum has v_2 <= -1, so if v_2(r) >= 0 there is no block.
      * t := -v_2(r) >= 1 is forced, hence the length k satisfies
            k <= 2^(t+1) - 1.
      * k/d <= H(c,d) = r <= k/c gives  k/r - k + 1 <= c <= k/r.
    So for each admissible k only <= k values of c must be tested.  Finite.

    Extra (rigorous) prunes, purely for speed:
      * every element of the block is <= D := kmax/r + kmax, so
        den(r) | lcm(1..D); we reject early if den(r) is too big for that
        (Rosser-Schoenfeld bound on psi).
      * the block must contain a multiple of 2^t and none of 2^(t+1).

    kcap: optional additional cap on k (setting it destroys completeness).
    """
    r = Fraction(r)
    if r <= 0:
        return []
    t = -v2(r)
    if t < 1:
        return []
    kmax = (1 << (t + 1)) - 1
    if kcap is not None:
        kmax = min(kmax, kcap)
    num, den = r.numerator, r.denominator
    # largest element that can occur
    D = (kmax * den) // num + kmax + 1
    if den.bit_length() > lcm_bitlen_bound(D):
        if stats is not None:
            stats["lcm_pruned"] = stats.get("lcm_pruned", 0) + 1
        return []
    if stats is not None:
        stats["scanned"] = stats.get("scanned", 0) + 1
    # odd prime-power constraints: if p^e || den(r) then some element of the
    # block must be divisible by p^e  (else v_p(H) > -e).
    oddq = []
    m = den
    while m % 2 == 0:
        m //= 2
    for p in (3, 5, 7, 11, 13, 17, 19, 23):
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            pe = p ** e
            if pe > D:
                return []
            oddq.append(pe)
    q = 1 << t
    q2 = q << 1
    out = []
    for k in range(2, kmax + 1):
        hi = (k * den) // num                      # floor(k/r)
        lo = max(cmin, hi - k + 1, 2)
        if lo > hi:
            continue
        dmax = hi + k
        # per-k lcm bound: den(r) | lcm(c..d) | lcm(1..dmax)
        if den.bit_length() > lcm_bitlen_bound(dmax):
            continue
        if any(pe > dmax for pe in oddq):
            continue
        # ---- ROUGH-PART bound (Lemma Q1 P3/P4 applied to the block) ------
        #   2^t * R | den(r)   with R = prod of k-rough parts >= C(d,k)/d^pi(k)
        #   and C(d,k) >= (d/k)^k.   So  den * k^k * d^pi(k) >= 2^t * d^k
        #   must hold for the smallest admissible d.
        dlo = lo + k - 1
        pik = _pi(k)
        if den * pow(k, k) * pow(dmax, pik) < (1 << t) * pow(dlo, k):
            continue
        # ---- integer-only 2-adic alignment filter ------------------------
        # [c,c+k-1] must contain a multiple of q=2^t and none of q2=2^(t+1).
        # Since k <= q2-1 the block meets at most one odd multiple mu of q.
        cand = []
        mu0 = ((lo + k - 1) // q) * q              # largest mult of q that is <= c+k-1 for c=lo
        for mu in (mu0, mu0 + q, mu0 + 2 * q):
            if mu == 0 or (mu // q) % 2 == 0:
                continue                           # mu divisible by q2
            c1 = max(lo, mu - k + 1, mu - q + 1)
            c2 = min(hi, mu, mu + q - k)
            if c1 <= c2:
                cand.append((c1, c2))
        if not cand:
            continue
        # ---- exact test on the (few) surviving c ------------------------
        for (c1, c2) in cand:
            h = None
            for c in range(c1, c2 + 1):
                d = c + k - 1
                if oddq and any(not _has_mult(c, d, pe) for pe in oddq):
                    h = None
                    continue
                if h is None:
                    h = H(c, d)
                else:
                    h = h - Fraction(1, c - 1) + Fraction(1, d)
                if h < r:
                    break                          # H(c,d) strictly decreasing in c
                if h == r:
                    assert _has_mult(c, d, q) and not _has_mult(c, d, q2)
                    out.append((c, d))
                    break
    return out


# ------------------------------------------------------------- misc helpers


def min_start_for_target(r):
    """
    Least a such that H(a,a+1) = 1/a + 1/(a+1) <= r.
    Any block whose sum is <= r must start at some a >= this value.
    (Because H(a,b) >= 1/a + 1/(a+1) for every block.)
    """
    r = Fraction(r)
    # solve (2a+1)/(a(a+1)) <= r  <=>  r a^2 + (r-2) a - 1 >= 0
    a = max(2, int(2 / float(r)) - 3)
    while Fraction(1, a) + Fraction(1, a + 1) > r:
        a += 1
    while a > 2 and Fraction(1, a - 1) + Fraction(1, a) <= r:
        a -= 1
    return a


@lru_cache(maxsize=None)
def tail(A, X):
    """sum_{n=A}^{X} 1/n as a Fraction (cached)."""
    if A > X:
        return Fraction(0)
    return H(A, X)


def runs(U):
    """maximal runs of a sorted iterable of ints"""
    U = sorted(U)
    out = []
    if not U:
        return out
    s = p = U[0]
    for n in U[1:]:
        if n == p + 1:
            p = n
        else:
            out.append((s, p))
            s = p = n
    out.append((s, p))
    return out


def no_isolated(U):
    return all(e > s for s, e in runs(U))


def check_representation(U, rho, T):
    """Exact verification that U certifies rho in B(T)."""
    U = sorted(set(U))
    assert len(U) == len(list(U)), "duplicates"
    if U and U[0] < T:
        return False, "element below T"
    if not no_isolated(U):
        return False, "isolated point"
    s = sum((Fraction(1, n) for n in U), Fraction(0))
    if s != Fraction(rho):
        return False, "sum %s != %s" % (s, Fraction(rho))
    return True, "ok: %d blocks-runs %s" % (len(runs(U)), runs(U))
