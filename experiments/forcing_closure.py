"""forcing_closure.py — machine verification + measurement of the FORCING CLOSURE theorem.

THEOREM (inline, session 1). Let a be a monotone-4-AP-free permutation of N, pos = a^{-1}.
Define the forcing relation on values:  u --d--> u+d   whenever  u - 2d >= 1  and
   pos(u-2d) < pos(u-d) < pos(u)      ["u is OPEN at scale d"].
Then for every such d:  pos(u+d) < pos(u)   [else (u-2d,u-d,u,u+d) is an increasing 4-AP].
Hence the forward closure Cl(u) of {u} under the relation is contained in {u} u pred(u),
so |Cl(u)| <= pos(u), and in particular Cl(u) is FINITE for every u.
Equivalently: 196-YES <=> every 4-AP-free permutation admits an infinite forcing chain.

Checks here:
 (F1) On ALL monotone-4-AP-free permutations of [1..N], N <= 9: whenever u is open at d
      and u+d <= N, verify pos(u+d) < pos(u). (The finite shadow of the forcing step.)
 (F2) The bound |Cl_N(u)| <= pos(u) on those same boards (closure computed inside the
      board, i.e. only following edges whose head is <= N).
 (F3) Measurement on SAT-found avoiders (plain target) at larger N: distribution of
      closure sizes, max closure, and the ratio max|Cl(u)| / N. Growth here is the
      empirical signal for whether closures blow up (YES-side) or stay small (NO-side).
"""

import sys
from itertools import permutations
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos


def open_scales(pos, u, N):
    """d >= 1 with u-2d >= 1 and pos[u-2d] < pos[u-d] < pos[u]."""
    out = []
    d = 1
    while u - 2 * d >= 1:
        if pos[u - 2 * d] < pos[u - d] < pos[u]:
            out.append(d)
        d += 1
    return out


def closure(pos, u0, N):
    """Forward closure of u0 under u -> u+d for d an open scale of u, staying <= N."""
    seen = {u0}
    stack = [u0]
    while stack:
        u = stack.pop()
        for d in open_scales(pos, u, N):
            w = u + d
            if w <= N and w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def check_board(perm):
    """Returns (max closure size, max closure/pos ratio). Raises on F1/F2 violation."""
    N = len(perm)
    pos = [0] * (N + 1)
    for i, v in enumerate(perm):
        pos[v] = i + 1
    worst = 0
    for u in range(1, N + 1):
        for d in open_scales(pos, u, N):
            if u + d <= N:
                # F1: the forcing step
                assert pos[u + d] < pos[u], ("F1 VIOLATION", perm, u, d)
        cl = closure(pos, u, N)
        # F2: closure sits inside {u} u pred(u)
        for w in cl:
            if w != u:
                assert pos[w] < pos[u], ("F2 VIOLATION", perm, u, w)
        assert len(cl) <= pos[u], ("F2 SIZE VIOLATION", perm, u, len(cl), pos[u])
        worst = max(worst, len(cl))
    return worst


if __name__ == "__main__":
    # F1/F2 exhaustively on all avoiders up to N = 9
    for N in range(4, 10):
        cnt = 0
        worst = 0
        for p in permutations(range(1, N + 1)):
            if has_monotone_kap_pos(p, 4):
                continue
            cnt += 1
            worst = max(worst, check_board(list(p)))
        print(f"N={N}: {cnt} avoiders, F1+F2 PASS, max closure size = {worst}", flush=True)

    # F3: measurement on SAT witnesses
    from sat_order import solve
    print("\nF3 — closure statistics on SAT-found plain avoiders:")
    for N in (40, 60, 80, 100, 130, 160):
        sat, perm = solve(N, inc4=True, dec4=True)
        assert sat and not has_monotone_kap_pos(perm, 4)
        pos = [0] * (N + 1)
        for i, v in enumerate(perm):
            pos[v] = i + 1
        sizes = []
        opens = 0
        for u in range(1, N + 1):
            sc = open_scales(pos, u, N)
            if sc:
                opens += 1
            cl = closure(pos, u, N)
            for w in cl:
                if w != u:
                    assert pos[w] < pos[u], ("F2 VIOLATION on SAT witness", N, u, w)
            sizes.append(len(cl))
        sizes.sort()
        print(f"  N={N}: open values = {opens}/{N} ({100*opens/N:.0f}%), "
              f"closure sizes: median={sizes[N//2]}, p90={sizes[int(0.9*N)]}, max={sizes[-1]}",
              flush=True)
