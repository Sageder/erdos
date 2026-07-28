#!/usr/bin/env python3
"""
Recon-3: brute-force verification of the REFORMULATION on a complete finite
universe.  Nothing is assumed: block systems are enumerated directly from the
definition, legal sets are enumerated directly from the definition, and the two
descriptions are compared for EVERY rational target q and every k.

Universe [2,M] (default M=20).
  LHS(q) = { k : exist k pairwise disjoint blocks, each of length >= 2, inside
                 [2,M], with total reciprocal sum q }
  RHS(q) = union over legal U subseteq [2,M] with sum q of [r(U), cap(U)]
The reformulation says LHS(q) = RHS(q) for every q.
"""
from fractions import Fraction
from itertools import combinations
import sys
from collections import defaultdict


def all_block_systems(M):
    """enumerate every set of pairwise disjoint blocks [a,b] (b>a) inside [2,M];
    yields (k, sum) — done by DFS over the leftmost free position."""
    res = defaultdict(set)          # sum -> set of k

    def rec(pos, k, s):
        res[s].add(k)
        for a in range(pos, M + 1):
            for b in range(a + 1, M + 1):
                ns = s + sum(Fraction(1, n) for n in range(a, b + 1))
                rec(b + 1, k + 1, ns)
    rec(2, 0, Fraction(0))
    return res


def all_legal(M):
    """enumerate every legal U subseteq [2,M]; yields (sum, r, cap)"""
    out = []
    n = M - 1
    for mask in range(1 << n):
        v = [i + 2 for i in range(n) if (mask >> i) & 1]
        if not v:
            continue
        s = set(v)
        if any((x - 1) not in s and (x + 1) not in s for x in v):
            continue
        # runs
        L, i = [], 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[j + 1] == v[j] + 1:
                j += 1
            L.append(j - i + 1)
            i = j + 1
        out.append((sum(Fraction(1, x) for x in v), len(L), sum(x // 2 for x in L)))
    return out


def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    sysd = all_block_systems(M)
    legal = all_legal(M)
    rhs = defaultdict(set)
    for (s, r, cap) in legal:
        rhs[s].update(range(r, cap + 1))
    lhs = {q: (ks - {0}) for q, ks in sysd.items()}
    lhs = {q: ks for q, ks in lhs.items() if ks}
    print("universe [2,%d]" % M)
    print("distinct sums realised by block systems :", len(lhs))
    print("distinct sums realised by legal sets    :", len(rhs))
    bad = []
    for q in set(lhs) | set(rhs):
        if lhs.get(q, set()) != rhs.get(q, set()):
            bad.append((q, sorted(lhs.get(q, set()))[:6], sorted(rhs.get(q, set()))[:6]))
    print("targets where LHS != RHS                :", len(bad))
    for b in bad[:10]:
        print("   MISMATCH", b)
    if not bad:
        print("REFORMULATION VERIFIED EXHAUSTIVELY on [2,%d] for every target q." % M)


if __name__ == "__main__":
    main()
