#!/usr/bin/env python3
"""
verify_prune.py -- correctness tests for prune.py.

CLAIM TESTED:  RULE A never deletes an element of a genuine solution of
sum_{n in U} 1/n = 1 (with U subset [2,N]);  RULE B never deletes an element of a
genuine LEGAL solution.

Method:
 (T1) brute-force ALL U subset [2,M] with sum 1/n = 1 for small M (M <= 24 via
      exact DFS), then check every such U survives prune(N=M, use_legality=False).
 (T2) independent re-implementation of the fixpoint (different code path, sets +
      Fractions) and comparison of the survivor sets for 2 <= N <= 90.
 (T3) sanity: the classical solutions {2,3,10,15}, {3,4,5,6,20}, {2,3,7,42},
      {2,4,6,12}, ... survive prune(use_legality=False) with N = max.
"""
import sys
from fractions import Fraction
from itertools import combinations
sys.path.insert(0, '/home/user/erdos/attempts/route-C')
from prune import prune, primes_upto, nu


# ---------- brute force all reciprocal-1 subsets of [2,M] ----------
def all_solutions(M):
    res = []
    ns = list(range(2, M + 1))

    def rec(i, rem, cur):
        if rem == 0:
            res.append(list(cur))
            return
        if i >= len(ns):
            return
        # bound: remaining max sum
        if rem > sum(Fraction(1, n) for n in ns[i:]):
            return
        if rem < 0:
            return
        for j in range(i, len(ns)):
            n = ns[j]
            if Fraction(1, n) > rem:
                continue
            cur.append(n)
            rec(j + 1, rem - Fraction(1, n), cur)
            cur.pop()
    rec(0, Fraction(1), [])
    return res


# ---------- independent fixpoint implementation (sets + Fractions) ----------
def prune_ref(N, use_legality=True):
    P = primes_upto(N)
    A = set(range(2, N + 1))
    while True:
        before = len(A)
        for p in P:
            while True:
                if not A:
                    break
                e = max(nu(n, p) for n in A)
                if e == 0:
                    break
                pe = p ** e
                C = sorted(n for n in A if nu(n, p) == e)
                # brute force all nonempty subsets (C is small in practice)
                if len(C) > 22:
                    break   # give up (keep) -- matches "cannot certify" policy
                found = False
                for r in range(1, len(C) + 1):
                    for T in combinations(C, r):
                        s = sum(Fraction(pe, n) for n in T)
                        # s is a p-integral rational; test s == 0 mod p
                        num, den = s.numerator, s.denominator
                        assert den % p != 0
                        if num % p == 0:
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
                A -= set(C)
        if use_legality:
            while True:
                bad = {n for n in A if (n - 1) not in A and (n + 1) not in A}
                if not bad:
                    break
                A -= bad
        if len(A) == before:
            break
    return sorted(A)


if __name__ == "__main__":
    print("=== T3: classical solutions survive RULE-A-only pruning ===")
    classics = [[2, 3, 10, 15], [3, 4, 5, 6, 20], [2, 3, 7, 42], [2, 4, 6, 12],
                [2, 4, 5, 20], [2, 3, 8, 24], [2, 3, 9, 18], [2, 3, 12, 12]]
    for U in classics:
        if len(set(U)) != len(U):
            continue
        assert sum(Fraction(1, n) for n in U) == 1, U
        M = max(U)
        s = set(prune(M, use_legality=False))
        missing = [n for n in U if n not in s]
        print(f"  U={U} max={M}: missing after RULE A = {missing}  "
              f"{'OK' if not missing else '*** FAIL ***'}")

    print("=== T1: exhaustive check for all solutions with max <= 24 ===")
    for M in range(2, 25):
        sols = all_solutions(M)
        sols = [U for U in sols if max(U) == M]
        if not sols:
            continue
        s = set(prune(M, use_legality=False))
        bad = [U for U in sols if any(n not in s for n in U)]
        print(f"  M={M}: {len(sols)} solutions with max=M; violations={len(bad)}"
              + (f"  e.g. {bad[0]}" if bad else ""))
        assert not bad, bad

    print("=== T2: independent reimplementation agrees, 2<=N<=90 ===")
    for N in range(2, 91):
        a = prune(N, True)
        b = prune_ref(N, True)
        if a != b:
            print(f"  *** MISMATCH at N={N}: {a} vs {b}")
            break
    else:
        print("  all agree (legality on)")
    for N in range(2, 91):
        a = prune(N, False)
        b = prune_ref(N, False)
        if a != b:
            print(f"  *** MISMATCH (no legality) at N={N}: {a} vs {b}")
            break
    else:
        print("  all agree (legality off)")
