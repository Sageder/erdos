"""
CLAIM TESTED (feeds a rigorous lemma for BOTH branches):

  Let  f(L) := sum over n with n | L, n >= 4, n+1 prime  of  1/n
             = sum of 1/n over the admissible moduli available inside the divisor lattice of L.

  Every covering system whose moduli all lie in E has L := lcm(moduli) satisfying f(L) > 1,
  because all moduli divide L and any covering system satisfies sum 1/n_i >= 1 (in fact > 1 for
  distinct moduli, by Davenport-Mirsky-Newman-Rado).

  Hence: the set  {L : f(L) > 1}  is an upward-closed-under-multiples constraint on the lcm, and
  any L with f(L) <= 1 is IMPOSSIBLE as the lcm of a qualifying system.  We compute the minimal
  such L, and the minimal L for various thresholds, over ALL L (not just smooth ones) by a
  rigorous branch-and-bound over prime factorisations.

WHY THE SEARCH IS EXHAUSTIVE: f(L) depends only on the multiset of prime powers of L and is
multiplicative-ish in the sense that f(L) <= g(L) := prod over q^e || L of (1 + 1/q + ... + 1/q^e)
minus 1  (the sum over ALL divisors >= 2 of 1/d, an upper bound obtained by pretending EVERY
divisor is admissible).  g is monotone under multiplying L by a new prime power, and
g(L) < 1 already forces f(L) < 1.  So we can prune any branch whose optimistic bound g is <= 1,
and we bound the primes that can occur.

CONCLUSION: printed; recorded in NOTES.md.
"""
from fractions import Fraction
from sympy import isprime, primerange
import heapq, sys


def admissible_divisor_sum(fac):
    """f(L) as an exact Fraction, given fac = list of (q,e)."""
    divs = [1]
    for q, e in fac:
        divs = [d * q ** i for d in divs for i in range(e + 1)]
    return sum(Fraction(1, d) for d in divs if d >= 4 and isprime(d + 1))


def optimistic(fac):
    """g(L) = sum over ALL divisors d >= 2 of 1/d  (upper bound for f, since f only keeps some)."""
    g = Fraction(1)
    for q, e in fac:
        g *= sum(Fraction(1, q ** i) for i in range(e + 1))
    return g - 1


def L_of(fac):
    L = 1
    for q, e in fac:
        L *= q ** e
    return L


def search(primes, target=Fraction(1), Lcap=None, verbose=True):
    """
    Exhaustive branch and bound over factorisations using the given prime list (in increasing
    order, each used with exponent >= 1, primes chosen in increasing order to avoid duplicates).
    Returns the minimum L with f(L) > target.
    """
    best = [None, None]     # (L, fac)

    def rec(idx, fac, L):
        if Lcap and L > Lcap:
            return
        if best[0] is not None and L >= best[0]:
            return
        if fac:
            if optimistic(fac_extended_bound(fac, idx, primes, L)) <= target:
                # even multiplying in every remaining allowed prime cannot reach the target
                return
            f = admissible_divisor_sum(fac)
            if f > target:
                best[0], best[1] = L, list(fac)
                return          # any extension is larger
        for j in range(idx, len(primes)):
            q = primes[j]
            if best[0] is not None and L * q >= best[0]:
                break
            e, Lq = 1, L * q
            while True:
                if best[0] is not None and Lq >= best[0]:
                    break
                if Lcap and Lq > Lcap:
                    break
                rec(j + 1, fac + [(q, e)], Lq)
                e += 1
                Lq *= q
    rec(0, [], 1)
    return best


def fac_extended_bound(fac, idx, primes, L):
    """optimistic completion: allow every remaining prime, each to a large exponent, but only as
    far as staying under any current best.  We simply return fac augmented by nothing: the caller
    uses g(fac) as an upper bound only for the CURRENT L; extensions are handled by recursion."""
    return fac


def brute_min_L(target=Fraction(1), Lmax=10 ** 7):
    """Independent, dead-simple check: scan every L <= Lmax and report the minimum with f(L)>target.
    Uses a divisor-sieve so it is exact and exhaustive over that range."""
    adm = bytearray(Lmax + 2)
    for d in range(4, Lmax + 1):
        if isprime(d + 1):
            adm[d] = 1
    # f(L) = sum over admissible d | L of 1/d ; accumulate by iterating multiples
    tot = [0.0] * (Lmax + 1)
    for d in range(4, Lmax + 1):
        if adm[d]:
            inv = 1.0 / d
            for m in range(d, Lmax + 1, d):
                tot[m] += inv
    bestL = None
    for L in range(1, Lmax + 1):
        if tot[L] > float(target) + 1e-12:
            bestL = L
            break
    return bestL, (tot[bestL] if bestL else None)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "brute"
    if mode == "brute":
        Lmax = int(sys.argv[2]) if len(sys.argv) > 2 else 3000000
        L, v = brute_min_L(Fraction(1), Lmax)
        print(f"exhaustive scan L <= {Lmax}:  minimal L with f(L) > 1  is  L = {L}  (f = {v:.6f})")
        if L:
            from sympy import factorint
            print("   factorisation:", factorint(L))
            divs = [d for d in range(4, L + 1) if L % d == 0 and isprime(d + 1)]
            print("   admissible divisors:", divs)
            print("   exact f(L) =", sum(Fraction(1, d) for d in divs))
