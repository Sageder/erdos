"""
H_pair.py -- Route H, part (a)+(b):  exhaustive enumeration of candidate DISJOINT PAIRS.

CLAIM TESTED.  For a given Y, is there a pair of disjoint sets A, B ⊆ M := R(Y) that both
survive every necessary condition proved in FINDINGS.md?  If the enumeration is empty, then
there is no covering system of Z with distinct moduli all in E and all <= 2Y.

Necessary conditions imposed on EACH of A and B (all proved in FINDINGS.md §1-§4):
   (C1) 1 < budget < kappa := budget(M) - 1        [DMNR + disjointness]
   (C2) Lemma L8: coprime m1,m2 in the set  =>  m1*m2 >= 1/delta,  delta = budget - 1
   (C3) Lemma L5: for every prime q, |A_q| = 0 or |A_q| >= q
   (C4) Lemma L10b: for every prime power q^t with D_t = {m in A : q^t | m} nonempty,
        budget(D_t) >= q*(1/min(D_t) - delta)
   (C5) Lemma L10 balance: {1/m : m in A_q} splits into q parts all within delta of the mean
and jointly:
   (C6) A and B disjoint, so budget(A) + budget(B) <= budget(M).

The search is a 3-way DFS (each modulus -> A, B or unused) over M in decreasing 1/m order,
with symmetry breaking (the largest used modulus-reciprocal goes to A).

CONCLUSION: printed per Y: number of surviving pairs, and the surviving candidate sets.
"""
import sys
from fractions import Fraction
from math import gcd
from sympy import factorint
from H_reduce import H_upto, reduce_set, budget, lcm_of


def prime_powers(M):
    pp = set()
    for m in M:
        for p, e in factorint(m).items():
            for t in range(1, e + 1):
                pp.add(p ** t)
    return sorted(pp)


def check_set(A, Delta, primes, pps, need_balance=True):
    """All single-set necessary conditions.  A is a sorted list."""
    b = sum(Fraction(1, m) for m in A)
    if b <= 1:
        return False
    d = b - 1
    if d > Delta:
        return False
    # (C2)
    for i, x in enumerate(A):
        for y in A[i + 1:]:
            if gcd(x, y) == 1 and Fraction(1, x * y) > d:
                return False
    # (C3)
    for q in primes:
        c = sum(1 for m in A if m % q == 0)
        if 0 < c < q:
            return False
    # (C4)
    for pk in pps:
        q = min(factorint(pk))
        D = [m for m in A if m % pk == 0]
        if not D:
            continue
        if sum(Fraction(1, m) for m in D) < q * (Fraction(1, min(D)) - d):
            return False
    # (C5)
    if need_balance:
        for q in primes:
            vals = [Fraction(1, m) for m in A if m % q == 0]
            if vals and not balance_ok(vals, q, d):
                return False
    return True


def balance_ok(vals, q, delta):
    tot = sum(vals)
    tgt = tot / q
    lo, hi = tgt - delta, tgt + delta
    if lo < 0:
        lo = Fraction(0)
    vals = sorted(vals, reverse=True)
    n = len(vals)
    suf = [Fraction(0)] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + vals[i]
    parts = [Fraction(0)] * q

    def rec(i):
        if i == n:
            return all(lo <= p <= hi for p in parts)
        need = sum((lo - p) for p in parts if p < lo)
        if need > suf[i]:
            return False
        seen = set()
        for j in range(q):
            if parts[j] in seen:
                continue
            seen.add(parts[j])
            if parts[j] + vals[i] <= hi:
                parts[j] += vals[i]
                if rec(i + 1):
                    parts[j] -= vals[i]
                    return True
                parts[j] -= vals[i]
        return False
    return rec(0)


def analyse(Y, report=12, verbose=True):
    M0 = H_upto(Y)
    M, _ = reduce_set(M0)
    bM = budget(M)
    kappa = bM - 1
    Delta = kappa - 1
    if verbose:
        print("=" * 78)
        print("Y=%d  |R|=%d  budget(R)=%.9f  kappa=%.9f  Delta=%.9f  1/Delta=%s"
              % (Y, len(M), float(bM), float(kappa), float(Delta),
                 ("%.3f" % float(1 / Delta)) if Delta > 0 else "inf"))
    if kappa <= 1:
        if verbose:
            print("  budget(R) <= 2 => no disjoint pair.  PROVED: no E-covering with moduli <= %d" % (2 * Y))
        return 0, []
    primes = sorted({p for m in M for p in factorint(m)})
    pps = prime_powers(M)
    Ms = sorted(M, key=lambda m: -Fraction(1, m))
    n = len(Ms)
    rec_ = [Fraction(1, m) for m in Ms]
    suf = [Fraction(0)] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + rec_[i]

    pairs = []
    stats = {"nodes": 0, "leaves": 0}

    def conflict(x, S, d_upper):
        for y in S:
            if gcd(x, y) == 1 and Fraction(1, x * y) > d_upper:
                return True
        return False

    def rec(i, A, bA, B, bB, started):
        stats["nodes"] += 1
        if bA > kappa or bB > kappa:
            return
        if bA + suf[i] <= 1 or bB + suf[i] <= 1:
            return
        if i == n:
            stats["leaves"] += 1
            if bA > 1 and bB > 1:
                if check_set(sorted(A), Delta, primes, pps) and check_set(sorted(B), Delta, primes, pps):
                    pairs.append((sorted(A), sorted(B)))
            return
        m = Ms[i]
        # -> A
        if not conflict(m, A, Delta):
            A.append(m); rec(i + 1, A, bA + rec_[i], B, bB, True); A.pop()
        # -> B  (symmetry: only if A already nonempty)
        if started and not conflict(m, B, Delta):
            B.append(m); rec(i + 1, A, bA, B, bB + rec_[i], started); B.pop()
        # unused
        rec(i + 1, A, bA, B, bB, started)

    rec(0, [], Fraction(0), [], Fraction(0), False)
    if verbose:
        print("  DFS nodes=%d  leaves=%d  surviving disjoint pairs: %d"
              % (stats["nodes"], stats["leaves"], len(pairs)))
        for (A, B) in pairs[:report]:
            print("     A=%s (%.6f)\n     B=%s (%.6f)" %
                  (A, float(budget(A)), B, float(budget(B))))
        if len(pairs) > report:
            print("     ... %d more" % (len(pairs) - report))
        if not pairs:
            print("  ==> PROVED: no E-covering with all moduli <= %d" % (2 * Y))
    return len(pairs), pairs


if __name__ == "__main__":
    Ys = [int(x) for x in sys.argv[1:]] or [128, 140, 150, 165, 170, 190, 200]
    for Y in Ys:
        analyse(Y)
        sys.stdout.flush()
