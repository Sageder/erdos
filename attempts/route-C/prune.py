#!/usr/bin/env python3
"""
prune.py -- strengthened necessary-condition pruning of the universe [2,N].

CLAIM TESTED / TOOL PROVIDED
---------------------------
Let U be finite, U subset [2,N], sum_{n in U} 1/n = 1, and (optionally) U has no
isolated point.  We iteratively delete integers of [2,N] that provably cannot
belong to any such U.  Two deletion rules, both proved below.

RULE A (p-adic top-level rule; strengthening of the "two attainers" prune).
  Fix a prime p and let A be the current allowed set.  Put
      e := max { nu_p(n) : n in A },     C := { n in A : nu_p(n) = e }.
  Suppose U subset A is a solution and U ∩ C != empty.  Then
      e = max_{n in U} nu_p(n)  (since U subset A and C is the top level of A),
  and writing n = p^e m (p ∤ m) for n in U ∩ C,
      sum_{n in U} 1/n  =  p^{-e} * ( sum_{n in U∩C} 1/m_n )  +  (terms of nu_p >= -(e-1)).
  For the total to have nu_p >= 0 (it equals 1) we need
      sum_{n in U∩C} 1/m_n  ==  0   (mod p).                                (*)
  Hence: if NO subset T subset C with |T| >= 1 satisfies (*), then every solution
  has U ∩ C = empty, so all of C may be deleted.  (|T| = 1 never satisfies (*)
  because 1/m is a unit mod p; so effectively |T| >= 2.  This is exactly the
  classical "two attainers" rule when we only test |T| = 1, and strictly stronger
  when we test all T.)

RULE B (legality rule).  If U has no isolated point and n in U then n-1 in U or
  n+1 in U.  So if n is allowed but both n-1 and n+1 are deleted (or out of
  range), n can never lie in a legal solution: delete n.

Both rules are monotone (they only delete), so iterating to a fixpoint is sound.

CONSEQUENCE USED LATER: if a legal solution has max(U) = N then both N and N-1
must survive the fixpoint computed on the ambient range [2,N].  This is a cheap
per-N necessary test.

Exact integer arithmetic only (modular inverses, Fractions).  No floats.
"""
import sys
from functools import lru_cache


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


def exists_zero_subset(residues, p, forced=()):
    """Is there a subset T of `residues` (units mod p) with T superset of
    `forced` (indices given as residues already included), T nonempty, and
    sum(T) == 0 mod p?

    Implemented as an exact DP over residues mod p: the reachable-set has at
    most p elements, so the cost is O(len(residues)*p) -- polynomial, complete,
    no size cap.  `forced` is a list of residues that must be included.
    """
    base = 0
    for r in forced:
        base = (base + r) % p
    nonempty0 = len(forced) > 0
    # reach: dict residue -> True if attainable (starting from base, adding a
    # subset of `residues`).  We track separately whether the total selection is
    # nonempty; base already nonempty if forced nonempty.
    reach_e = {base}            # attainable using NO optional element
    reach_n = set()             # attainable using at least one optional element
    for r in residues:
        add = set()
        for x in reach_e:
            add.add((x + r) % p)
        for x in reach_n:
            add.add((x + r) % p)
        reach_n |= add
    if 0 in reach_n:
        return True
    if nonempty0 and 0 in reach_e:
        return True
    return False


def prune(N, use_legality=True, verbose=False, force=(), target=None):
    """Return the set of survivors in [2,N].

    force: a set of integers ASSUMED to lie in U (e.g. {N, N-1} when we look for
    a legal solution with max(U) = N).  Then, at a top level C of a prime p with
    C ∩ force != empty, we know U ∩ C != empty, so the valid subset T must in
    addition CONTAIN C ∩ force.  If none exists the whole configuration is
    infeasible and we return None.  force also strengthens RULE B (a forced n
    with only one surviving neighbour forces that neighbour into U).
    """
    from fractions import Fraction
    if target is None:
        target = Fraction(1)
    P = primes_upto(N)
    allowed = bytearray(N + 1)
    for n in range(2, N + 1):
        allowed[n] = 1
    # precompute nu_p tables
    nutab = {}
    for p in P:
        t = [0] * (N + 1)
        q = p
        while q <= N:
            for m in range(q, N + 1, q):
                t[m] += 1
            q *= p
        nutab[p] = t

    force = set(force)
    for n in force:
        if not (2 <= n <= N):
            return None

    changed = True
    while changed:
        changed = False
        # ---- RULE A ----
        for p in P:
            t = nutab[p]
            while True:
                e = 0
                for n in range(2, N + 1):
                    if allowed[n] and t[n] > e:
                        e = t[n]
                # v = nu_p(target).  nu_p(sum)=v forces max_{n in U} nu_p(n) >= -v,
                # and a level e > -v must CANCEL mod p (sum of 1/m == 0 mod p),
                # while the level e = -v must NOT cancel (any single element does,
                # so no deletion is possible there).
                vt = 0
                tn, td = target.numerator, target.denominator
                while tn % p == 0:
                    tn //= p; vt += 1
                while td % p == 0:
                    td //= p; vt -= 1
                if e <= -vt:
                    if e < -vt:
                        return None      # cannot reach valuation v at p
                    break
                pe = p ** e
                C = [n for n in range(2, N + 1) if allowed[n] and t[n] == e]
                Cf = [n for n in C if n in force]
                opt = [pow(n // pe, -1, p) for n in C if n not in force]
                fr = [pow(n // pe, -1, p) for n in Cf]
                if exists_zero_subset(opt, p, forced=fr):
                    break
                if Cf:
                    return None          # forced elements sit on an impossible level
                for n in C:
                    allowed[n] = 0
                changed = True
                if verbose:
                    print(f"  RULE A p={p} e={e} deletes {C}")
        # ---- RULE B ----
        if use_legality:
            while True:
                hit = []
                for n in range(2, N + 1):
                    if not allowed[n]:
                        continue
                    left = n - 1 >= 2 and allowed[n - 1]
                    right = n + 1 <= N and allowed[n + 1]
                    if not left and not right:
                        hit.append(n)
                if not hit:
                    break
                if force & set(hit):
                    return None
                for n in hit:
                    allowed[n] = 0
                changed = True
                if verbose:
                    print(f"  RULE B deletes {hit}")
        if any(not allowed[n] for n in force):
            return None
    surv = [n for n in range(2, N + 1) if allowed[n]]
    return surv


def report(N, use_legality=True):
    surv = prune(N, use_legality)
    if surv is None:
        surv = []
    S = set(surv)
    banned = [n for n in range(2, N + 1) if n not in S]
    from fractions import Fraction
    tot = sum(Fraction(1, n) for n in surv)
    pairs = sum(1 for n in surv if n + 1 in S)
    return dict(N=N, nsurv=len(surv), banned=banned, total=tot, pairs=pairs,
                topok=(N in S and N - 1 in S), surv=surv)


if __name__ == "__main__":
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    print("N  #surv  maxOK  sum(1/n) over survivors (float approx)  #consec-pairs   banned")
    for N in range(lo, hi + 1):
        r = report(N)
        print(f"{N:4d} {r['nsurv']:5d}  {'Y' if r['topok'] else 'n'}   "
              f"{float(r['total']):8.4f}  {r['pairs']:4d}   {r['banned']}")
