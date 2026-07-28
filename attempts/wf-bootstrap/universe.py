#!/usr/bin/env python3
"""
universe.py -- build the pruned universe for a window [T,N] and a rational
target rho = u/v, and report its size and the bit length of L = lcm(universe).

PRUNING RULES (all PROVED; each only deletes elements that provably lie in no
legal U subset [T,N] with sum_{n in U} 1/n = rho).

Let A be the current allowed set (initially [T,N]) and suppose U subset A is a
legal solution.

RULE A (p-adic).  Fix a prime p, put v_p := nu_p(rho), e := max{nu_p(n):n in A},
C := {n in A : nu_p(n) = e}, and suppose U ∩ C != empty.  Then
max_{n in U} nu_p(n) = e and, writing n = p^e m_n on C,
      sum_{n in U} 1/n = p^{-e} * (sum_{n in U∩C} 1/m_n)  +  (terms with nu_p >= 1-e).
  * If e < -v_p : impossible, no U at all meets A (return None).
  * If e > -v_p : we need nu_p(sum) = v_p > -e, so the leading term must vanish
    mod p:   sum_{n in U∩C} 1/m_n == 0 (mod p).   If NO nonempty subset of C has
    this property, then U ∩ C = empty and all of C may be deleted.
    (Subsets of size 1 never work: 1/m is a unit.  So |C| = 1 always deletes.)
  * If e == -v_p : no deletion (a single attainer is fine).

RULE B (legality).  If n in A survives but both n-1 and n+1 are outside A then n
is isolated in every U subset A, so delete n.

Iterate to a fixpoint.  Monotone => sound.

Exact arithmetic only.

usage: python3 universe.py T N u v
"""
import sys
from fractions import Fraction


def primes_upto(N):
    sieve = bytearray([1]) * (N + 1)
    sieve[0:2] = b"\x00\x00"
    i = 2
    while i * i <= N:
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(sieve[i * i:: i]))
        i += 1
    return [i for i in range(2, N + 1) if sieve[i]]


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def exists_zero_subset(residues, p):
    """Is there a NONEMPTY subset of the multiset `residues` (units mod p)
    summing to 0 mod p?  Exact DP over Z/p, complete."""
    if not residues:
        return False
    reach = set()          # residues attainable by a nonempty subset
    for r in residues:
        add = {(x + r) % p for x in reach}
        add.add(r % p)
        reach |= add
        if 0 in reach:
            return True
    return 0 in reach


def build(T, N, rho, verbose=False, smoothB=0):
    """smoothB > 0: treat all primes p <= smoothB as FREE, i.e. impose no
    condition at all on nu_p(sum).  This is the correct universe for the
    'gadget' search, where we only require the denominator of the sum to be
    smoothB-smooth.  (Formally: v_p = -infinity for p <= smoothB.)"""
    P = primes_upto(N)
    allowed = bytearray(N + 2)
    for n in range(T, N + 1):
        allowed[n] = 1
    vp = {}
    for p in P:
        if p <= smoothB:
            vp[p] = None          # free prime: never delete
        else:
            vp[p] = nu(rho.numerator, p) - nu(rho.denominator, p)
    changed = True
    while changed:
        changed = False
        for p in P:
            if vp[p] is None:
                continue
            while True:
                e = -1
                for n in range(T, N + 1):
                    if allowed[n]:
                        x = nu(n, p)
                        if x > e:
                            e = x
                if e < 0:
                    return None          # empty universe
                if e < -vp[p]:
                    return None          # cannot reach the required valuation
                if e == -vp[p]:
                    break
                pe = p ** e
                C = [n for n in range(T, N + 1) if allowed[n] and nu(n, p) == e]
                res = [pow((n // pe) % p, -1, p) for n in C]
                if exists_zero_subset(res, p):
                    break
                for n in C:
                    allowed[n] = 0
                changed = True
                if verbose:
                    print("  RULE A p=%d e=%d deletes %s" % (p, e, C))
        while True:
            hit = [n for n in range(T, N + 1) if allowed[n]
                   and not (n - 1 >= T and allowed[n - 1])
                   and not (n + 1 <= N and allowed[n + 1])]
            if not hit:
                break
            for n in hit:
                allowed[n] = 0
            changed = True
            if verbose:
                print("  RULE B deletes %s" % hit)
    return [n for n in range(T, N + 1) if allowed[n]]



def build_with_banned(T, N, rho, banned, smoothB=0):
    """Same fixpoint as build(), but with a set of integers deleted a priori.
    Deleting elements is always sound (it only shrinks the search space), so any
    system found inside the result is still a genuine legal system."""
    P = primes_upto(N)
    allowed = bytearray(N + 2)
    for n in range(T, N + 1):
        if n not in banned:
            allowed[n] = 1
    vp = {}
    for p in P:
        if p <= smoothB:
            vp[p] = None
        else:
            vp[p] = nu(rho.numerator, p) - nu(rho.denominator, p)
    changed = True
    while changed:
        changed = False
        for p in P:
            if vp[p] is None:
                continue
            while True:
                e = -1
                for n in range(T, N + 1):
                    if allowed[n]:
                        x = nu(n, p)
                        if x > e:
                            e = x
                if e < 0:
                    return None
                if e <= -vp[p]:
                    break
                pe = p ** e
                C = [n for n in range(T, N + 1) if allowed[n] and nu(n, p) == e]
                res = [pow((n // pe) % p, -1, p) for n in C]
                if exists_zero_subset(res, p):
                    break
                for n in C:
                    allowed[n] = 0
                changed = True
        while True:
            hit = [n for n in range(T, N + 1) if allowed[n]
                   and not (n - 1 >= T and allowed[n - 1])
                   and not (n + 1 <= N and allowed[n + 1])]
            if not hit:
                break
            for n in hit:
                allowed[n] = 0
            changed = True
    return [n for n in range(T, N + 1) if allowed[n]]


def lcm_of(univ, rho):
    from math import gcd
    L = 1
    for n in univ:
        L = L // gcd(L, n) * n
    # make sure denominator of rho divides L
    d = rho.denominator
    L = L // gcd(L, d) * d
    return L


def report(T, N, rho):
    U = build(T, N, rho)
    if U is None:
        print("T=%4d N=%5d rho=%-6s  UNIVERSE EMPTY (no solution)" % (T, N, rho))
        return None
    L = lcm_of(U, rho)
    tot = sum(Fraction(1, n) for n in U)
    npairs = sum(1 for n in U if n + 1 in set(U))
    print("T=%4d N=%5d rho=%-6s  |univ|=%4d  maxsum=%s ~ %.4f  Lbits=%d  adjacent-pairs=%d"
          % (T, N, rho, len(U), "", float(tot), L.bit_length(), npairs))
    return U


if __name__ == "__main__":
    T = int(sys.argv[1]); N = int(sys.argv[2])
    u = int(sys.argv[3]); v = int(sys.argv[4])
    rho = Fraction(u, v)
    U = build(T, N, rho, verbose=("-v" in sys.argv))
    if U is None:
        print("empty universe")
        sys.exit(0)
    L = lcm_of(U, rho)
    tot = sum(Fraction(1, n) for n in U)
    print("T=%d N=%d rho=%s" % (T, N, rho))
    print("universe size %d, L has %d bits, total available sum = %s" % (len(U), L.bit_length(), tot))
    print("universe:", U)
