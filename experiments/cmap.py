#!/usr/bin/env python3
"""
THE c-MAP FAMILY.

Fix c >= 3 and a finite set U of integers >= 1.  For n in U put
      beta^c_n  = {cn, cn+1},        gamma^c_n = {cn-1, cn}.
For c >= 3 the atoms of distinct n are pairwise DISJOINT whatever the colouring
(the blocks live inside [cn-1, cn+1] and c(n+1)-1 - (cn+1) = c-2 >= 1), so EVERY
one of the 2^{|U|} colourings is admissible -- unlike c = 2, where beta_n and
gamma_{n+1} share 2n+1.

The resulting set A is legal, has |U| atoms, hence cap(A) = |U| and r(A) <= |U|;
so A realises EXACTLY k = |U| blocks (splitting lemma).  Its sum is

    Sigma(A) = sum_{n in U} beta^c_n  +  sum_{n in G} (gamma^c_n - beta^c_n)
             = B_c(U) + sum_{n in G} 2/(c^2 n^2 - 1),
    B_c(U) := sum_{n in U} ( 1/(cn) + 1/(cn+1) ).

So A is a SOLUTION iff

        sum_{n in G} 2/(c^2 n^2 - 1)  =  1 - B_c(U)          (TARGET)

for some G subset U.  Taking U = [a, a+k-1] an interval gives, for each k, a
one-parameter family in a; TARGET is then a subset-sum with 2^k choices, decided
here exactly by meet-in-the-middle.

Everything exact (fractions.Fraction).
"""
import sys
from fractions import Fraction as F
from itertools import combinations


def Bc(U, c):
    return sum(F(1, c * n) + F(1, c * n + 1) for n in U)


def subset_sums(items):
    """dict: exact sum -> tuple of chosen items"""
    out = {F(0): ()}
    for it, val in items:
        new = {}
        for s, ch in out.items():
            t = s + val
            if t not in out and t not in new:
                new[t] = ch + (it,)
        out.update(new)
    return out


def solve(U, c):
    tgt = 1 - Bc(U, c)
    if tgt < 0:
        return None
    items = [(n, F(2, c * c * n * n - 1)) for n in U]
    h = len(items) // 2
    L = subset_sums(items[:h])
    R = subset_sums(items[h:])
    for s, ch in R.items():
        need = tgt - s
        if need in L:
            return L[need] + ch
    return None


def build(U, c, G):
    G = set(G); out = set()
    for n in U:
        out |= {c * n - 1, c * n} if n in G else {c * n, c * n + 1}
    return sorted(out)


def runs_of(U):
    U = sorted(U); out = []; cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1: cur.append(x)
        else: out.append(cur); cur = [x]
    out.append(cur); return out


if __name__ == "__main__":
    kmin = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 26
    cs = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [3, 4, 5, 6]
    hits = {}
    for k in range(kmin, kmax + 1):
        for c in cs:
            # H(a,a+k-1) ~ c/2  =>  a ~ k/(e^{c/2}-1);  scan generously
            import math
            a0 = max(1, int(k / (math.exp(c / 2) - 1)))
            for a in range(max(1, a0 - 12), a0 + 40):
                U = list(range(a, a + k))
                t = 1 - Bc(U, c)
                if t < 0: continue
                if t > sum(F(2, c * c * n * n - 1) for n in U): continue
                G = solve(U, c)
                if G is not None:
                    W = build(U, c, G)
                    s = sum(F(1, n) for n in W); S = set(W)
                    ok = s == 1 and all(n - 1 in S or n + 1 in S for n in W) and min(W) >= 2
                    L = [len(r) for r in runs_of(W)]
                    r, M = len(L), sum(x // 2 for x in L)
                    print(f"HIT k={k} c={c} a={a}: sum={s} legal={ok} r={r} cap={M} "
                          f"max={max(W)}  G={sorted(G)}")
                    sys.stdout.flush()
                    hits.setdefault(k, (c, a, W))
                    break
    print("\nk values hit:", sorted(hits))
