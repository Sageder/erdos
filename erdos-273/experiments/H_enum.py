"""
H_enum.py -- Route H, part (a):  enumerate the minimal candidate families.

Necessary conditions used (each PROVED in FINDINGS.md; each verified numerically in
H_lemma_check2.py before use):

  (N0) [parity equivalence]  An E-covering with all moduli <= 2Y  <=>  two DISJOINT covering
       sets A,B inside H ∩ [2,Y].
  (N1) [Lemma L5 / reduction R]  WLOG A,B ⊆ M := R(Y).
  (N2) [Davenport-Mirsky-Newman-Rado]  budget(A) > 1 and budget(B) > 1 (strict, distinct moduli).
       With A,B ⊆ M disjoint:  1 < budget(A) <= budget(M) - 1 =: kappa, and same for B.
       Write delta = budget(A) - 1 <= kappa - 1.
  (N3) [Lemma L8, "coprime pair"]  if m1,m2 in A are COPRIME then 1/(m1 m2) <= delta,
       i.e. m1*m2 >= 1/delta >= 1/(kappa-1).   (their classes always meet, and the
       multiply-covered set has density exactly delta)
  (N4) [Lemma L5 again, applied to A itself]  for every prime q: |A_q| = 0 or |A_q| >= q.
  (N5) [Lemma L10, Fourier balance]  for every prime q, with
       c_j = sum{1/m : m in A, q|m, a_m ≡ j mod q},  one has  sum_j (c_j - cbar)^2 <=
       ((q-1)/q) delta^2 where cbar = budget(A_q)/q.  Necessary consequence used here:
       the multiset {1/m : m in A_q} must admit a partition into q parts whose sums all lie
       within delta of budget(A_q)/q.

The script enumerates ALL subsets A ⊆ M satisfying (N2)+(N3)+(N4) [+(N5) as a filter],
and reports the minimal ones.  If the list is empty, no two disjoint covering sets exist in
H ∩ [2,Y]  ==>  no E-covering with all moduli <= 2Y.

CONCLUSION: printed per Y.
"""
from fractions import Fraction
from math import gcd
from sympy import factorint
import sys, itertools

from H_reduce import H_upto, reduce_set, budget, lcm_of


def conflict_graph(M, thr):
    """pairs (m1,m2), coprime, with m1*m2 < thr  -- forbidden to coexist."""
    bad = {m: set() for m in M}
    for i, a in enumerate(M):
        for b in M[i + 1:]:
            if gcd(a, b) == 1 and Fraction(1, a * b) > thr:
                bad[a].add(b)
                bad[b].add(a)
    return bad


def balance_feasible(vals, q, delta):
    """Can the multiset vals (Fractions 1/m) be split into q parts with every part sum
    within delta of (sum/q)?  Exact DP over achievable part-sums is expensive; we use the
    exact necessary test for the LARGEST element and a greedy/DP feasibility check."""
    tot = sum(vals)
    target = tot / q
    lo, hi = target - delta, target + delta
    if lo < 0:
        lo = Fraction(0)
    # necessary: the largest element must fit in a part of size <= hi
    if any(v > hi for v in vals):
        return False
    # exact search: assign elements (largest first) to parts, prune on overflow
    vals = sorted(vals, reverse=True)
    n = len(vals)
    suffix = [Fraction(0)] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + vals[i]
    parts = [Fraction(0)] * q

    def rec(i):
        if i == n:
            return all(lo <= p <= hi for p in parts)
        # prune: parts still below lo need suffix
        need = sum((lo - p) for p in parts if p < lo)
        if need > suffix[i]:
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


def enumerate_candidates(Y, use_balance=True, verbose=True, cap_report=40):
    M = H_upto(Y)
    R, _ = reduce_set(M)
    bM = budget(R)
    kappa = bM - 1
    if kappa <= 1:
        if verbose:
            print("Y=%d : budget(R)=%s <= 2  => NO two disjoint covering sets (budget alone)"
                  % (Y, bM))
        return [], R, bM, kappa
    thr = kappa - 1          # delta <= thr
    bad = conflict_graph(R, thr)
    n = len(R)
    R = sorted(R)
    idx = {m: i for i, m in enumerate(R)}
    recip = [Fraction(1, m) for m in R]
    suffix = [Fraction(0)] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + recip[i]
    primes = sorted({p for m in R for p in factorint(m)})
    results = []
    nodes = [0]

    def rec(i, cur, bud):
        nodes[0] += 1
        if bud > kappa:
            return
        if bud + suffix[i] <= 1:
            return
        if i == n:
            if bud > 1:
                results.append(list(cur))
            return
        # include R[i] if compatible
        m = R[i]
        if all(x not in bad[m] for x in cur):
            cur.append(m)
            rec(i + 1, cur, bud + recip[i])
            cur.pop()
        rec(i + 1, cur, bud)

    rec(0, [], Fraction(0))
    # post-filters
    kept = []
    for A in results:
        d = budget(A) - 1
        ok = True
        for q in primes:
            Aq = [m for m in A if m % q == 0]
            if 0 < len(Aq) < q:
                ok = False
                break
        if ok and use_balance:
            for q in primes:
                Aq = [m for m in A if m % q == 0]
                if not Aq:
                    continue
                if not balance_feasible([Fraction(1, m) for m in Aq], q, d):
                    ok = False
                    break
        if ok:
            kept.append(A)
    # minimal elements
    kept_sets = [frozenset(a) for a in kept]
    minimal = [a for a in kept_sets if not any(b < a for b in kept_sets)]
    if verbose:
        print("Y=%-5d |R|=%-3d budget(R)=%.6f  kappa=%.6f  delta<=%.6f  1/delta>=%.2f"
              % (Y, n, float(bM), float(kappa), float(thr), float(1 / thr) if thr > 0 else -1))
        print("   subset-DFS nodes=%d   sets with (N2)+(N3): %d   after (N4)+(N5): %d   minimal: %d"
              % (nodes[0], len(results), len(kept), len(minimal)))
        for a in sorted(minimal, key=lambda s: (len(s), sorted(s)))[:cap_report]:
            print("      %s   budget=%.6f" % (sorted(a), float(budget(sorted(a)))))
        if len(minimal) > cap_report:
            print("      ... (%d more)" % (len(minimal) - cap_report))
    return kept, R, bM, kappa


if __name__ == "__main__":
    Ys = [int(x) for x in sys.argv[1:]] or [128, 140, 150, 165, 170, 190, 200, 210, 225, 250, 260, 300]
    for Y in Ys:
        enumerate_candidates(Y)
        print()
