#!/usr/bin/env python3
"""
Claim tested: existence of finite U subset of Z_{>=2} with sum_{n in U} 1/n = 1
and NO ISOLATED POINTS (every n in U has n-1 in U or n+1 in U).

Such a U is exactly the union of a system of disjoint blocks of length >= 2.
If U has maximal runs of lengths L_1..L_r then U realises exactly the block
counts k with r <= k <= M := sum_i floor(L_i/2)   (splitting lemma).

Exact arithmetic only (fractions.Fraction).  Deterministic DFS.
"""
import sys
from fractions import Fraction


def runs_of(U):
    U = sorted(U)
    runs, cur = [], [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append(cur)
            cur = [x]
    runs.append(cur)
    return runs


def profile(U):
    R = runs_of(U)
    L = [len(x) for x in R]
    return len(R), sum(l // 2 for l in L), L


def search(N, cap=200000, want=None):
    """All U subset [2,N], sum 1/n = 1, no isolated points.  want: stop after this many."""
    tail = [Fraction(0)] * (N + 3)
    for n in range(N, 1, -1):
        tail[n] = tail[n + 1] + Fraction(1, n)

    sols = []
    nodes = 0
    ONE = Fraction(1)

    def dfs(pos, rem, runlen, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > cap:
            raise KeyboardInterrupt
        if rem == 0:
            if runlen != 1:
                sols.append(tuple(chosen))
                if want and len(sols) >= want:
                    raise KeyboardInterrupt
            return
        if pos > N:
            return
        if rem > tail[pos]:
            return
        # include pos
        f = Fraction(1, pos)
        if f <= rem:
            chosen.append(pos)
            dfs(pos + 1, rem - f, runlen + 1, chosen)
            chosen.pop()
        elif runlen == 1:
            return  # forced to include but cannot
        # exclude pos (only legal if we are not in the middle of a length-1 run)
        if runlen != 1:
            dfs(pos + 1, rem, 0, chosen)

    try:
        dfs(2, ONE, 0, [])
    except KeyboardInterrupt:
        pass
    return sols, nodes


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 3000000
    sols, nodes = search(N, cap=cap)
    print(f"N={N}  nodes={nodes}  solutions={len(sols)}")
    # verify every solution independently, exactly
    ks = {}
    for U in sols:
        assert sum(Fraction(1, n) for n in U) == Fraction(1), U
        assert min(U) >= 2
        r, M, L = profile(U)
        for k in range(r, M + 1):
            ks.setdefault(k, U)
    print("achievable block counts k:", sorted(ks))
    for k in sorted(ks):
        U = ks[k]
        r, M, L = profile(U)
        print(f"  k={k}: runs={L} (r={r},M={M})  U={list(U)}")
