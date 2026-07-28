"""forcing_tools.py — route R18 instrumentation for the FORCING DIGRAPH (CORE.md Thm 16).

Conventions (PROBLEM.md): a finite board is a permutation `perm` of [1..N] given as the
list of VALUES in position order; pos[v] = 1-based position of value v.

Definitions (Thm 16):
  u is OPEN at scale d   iff  u-2d >= 1 and pos[u-2d] < pos[u-d] < pos[u]
                          (i.e. (u-2d,u-d,u) is a positionally increasing 3-AP;
                           equivalently u is the TOP of an increasing monotone 3-AP).
  forcing edge  u --d--> u+d  (a forcing TARGET has an "inc-step" in Lemma 8's language).
  Cl_N(u) = forward closure inside the board (only edges with head <= N).
  h_N(u)  = length (#edges) of the longest forcing path out of u inside the board.
  u is CLOSED iff it has no open scale (a SINK of the forcing digraph).

Everything here is cross-validated in __main__ against
  - experiments/apcheck.py (trusted brute-force AP checker), and
  - experiments/forcing_closure.py (the existing closure routine),
  - and a literal-definition brute force over position triples.
"""

import sys
from itertools import combinations, permutations

sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute  # noqa: E402


# ---------------------------------------------------------------- basic objects

def positions(perm):
    """pos[v] = 1-based position of value v; perm is a permutation of [1..N]."""
    N = len(perm)
    pos = [0] * (N + 2)
    for i, v in enumerate(perm):
        pos[v] = i + 1
    return pos


def open_scales(pos, u):
    """All d >= 1 with u-2d >= 1 and pos[u-2d] < pos[u-d] < pos[u]. Board-independent
    (openness only involves values <= u, so it is preserved by restriction)."""
    out = []
    for d in range(1, (u - 1) // 2 + 1):
        if pos[u - 2 * d] < pos[u - d] < pos[u]:
            out.append(d)
    return out


def forcing_digraph(perm):
    """Return (edges, succ) with edges = list of (u, d, u+d) for in-board targets."""
    N = len(perm)
    pos = positions(perm)
    succ = {u: [] for u in range(1, N + 1)}
    edges = []
    for u in range(1, N + 1):
        for d in open_scales(pos, u):
            w = u + d
            if w <= N:
                succ[u].append(w)
                edges.append((u, d, w))
    return edges, succ


def closures_and_heights(perm):
    """Return (cl_size, height, open_flag, out_deg) arrays indexed by value 1..N.

    open_flag[u] = True iff u has at least one open scale d with u-2d >= 1
                   (regardless of whether the target u+d is inside the board).
    height/closure are computed INSIDE the board (edges with head <= N only).
    """
    N = len(perm)
    pos = positions(perm)
    succ = {u: [] for u in range(1, N + 1)}
    open_flag = [False] * (N + 2)
    out_deg = [0] * (N + 2)
    for u in range(1, N + 1):
        sc = open_scales(pos, u)
        if sc:
            open_flag[u] = True
        for d in sc:
            w = u + d
            if w <= N:
                succ[u].append(w)
        out_deg[u] = len(succ[u])
    # values only increase along edges -> process in decreasing value order (DAG order)
    height = [0] * (N + 2)
    reach = [None] * (N + 2)
    for u in range(N, 0, -1):
        s = {u}
        h = 0
        for w in succ[u]:
            s |= reach[w]
            h = max(h, 1 + height[w])
        reach[u] = s
        height[u] = h
    cl_size = [0] * (N + 2)
    for u in range(1, N + 1):
        cl_size[u] = len(reach[u])
    return cl_size, height, open_flag, out_deg, reach


def board_stats(perm):
    """Summary dict for a board."""
    N = len(perm)
    cl, ht, op, od, reach = closures_and_heights(perm)
    pos = positions(perm)
    n_open = sum(1 for u in range(1, N + 1) if op[u])
    return dict(
        N=N,
        n_open=n_open,
        frac_open=n_open / N,
        max_height=max(ht[1:N + 1]),
        max_closure=max(cl[1:N + 1]),
        mean_closure=sum(cl[1:N + 1]) / N,
        n_edges=sum(od[1:N + 1]),
        W_holds=all(ht[u] <= 1 for u in range(1, N + 1)),
        argmax_height=max(range(1, N + 1), key=lambda u: ht[u]),
    )


def verify_theorem16(perm):
    """Re-verify Thm 16 (a) forcing step and (b) Cl(u)\\{u} subset pred(u), |Cl(u)|<=pos(u).
    Only valid on boards with no monotone 4-AP; raises AssertionError otherwise."""
    N = len(perm)
    pos = positions(perm)
    cl, ht, op, od, reach = closures_and_heights(perm)
    for u in range(1, N + 1):
        for d in open_scales(pos, u):
            if u + d <= N:
                assert pos[u + d] < pos[u], ("F1 violation", perm, u, d)
        for w in reach[u]:
            if w != u:
                assert pos[w] < pos[u], ("F2 violation", perm, u, w)
        assert cl[u] <= pos[u], ("F2 size violation", perm, u, cl[u], pos[u])
    return True


# ------------------------------------------------- independent brute-force oracle

def open_scales_brute(perm, u):
    """Literal definition: scan all position triples i<j<k whose values are an
    increasing 3-AP with top value u. Returns the set of scales d."""
    N = len(perm)
    out = set()
    for i, j, k in combinations(range(N), 3):
        a, b, c = perm[i], perm[j], perm[k]
        if c != u:
            continue
        if b - a >= 1 and c - b == b - a:
            out.add(b - a)
    return out


def closure_brute(perm, u0):
    """BFS closure using the brute-force open-scale oracle."""
    N = len(perm)
    seen = {u0}
    stack = [u0]
    while stack:
        u = stack.pop()
        for d in open_scales_brute(perm, u):
            w = u + d
            if w <= N and w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def height_brute(perm, u0, memo=None):
    N = len(perm)
    if memo is None:
        memo = {}
    if u0 in memo:
        return memo[u0]
    h = 0
    for d in open_scales_brute(perm, u0):
        w = u0 + d
        if w <= N:
            h = max(h, 1 + height_brute(perm, w, memo))
    memo[u0] = h
    return h


# --------------------------------------------------------------- cross-validation

def _crossvalidate():
    import random
    rng = random.Random(1918)
    # (1) fast open_scales / closure / height vs literal brute force, random boards
    for _ in range(400):
        n = rng.randint(4, 9)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        pos = positions(p)
        cl, ht, op, od, reach = closures_and_heights(p)
        for u in range(1, n + 1):
            assert set(open_scales(pos, u)) == open_scales_brute(p, u), (p, u)
            assert reach[u] == closure_brute(p, u), (p, u)
            assert ht[u] == height_brute(p, u), (p, u)
            assert op[u] == (len(open_scales_brute(p, u)) > 0)
    # (2) closure agrees with experiments/forcing_closure.py
    import forcing_closure as FC
    for _ in range(300):
        n = rng.randint(4, 10)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        posFC = [0] * (n + 1)
        for i, v in enumerate(p):
            posFC[v] = i + 1
        cl, ht, op, od, reach = closures_and_heights(p)
        for u in range(1, n + 1):
            assert reach[u] == FC.closure(posFC, u, n), (p, u)
    # (3) Thm 16 verification on ALL 4-AP-free boards for N <= 8
    tot = 0
    for n in range(4, 9):
        for p in permutations(range(1, n + 1)):
            if has_monotone_kap_pos(p, 4):
                continue
            tot += 1
            verify_theorem16(list(p))
    # (4) the trusted checker itself agrees with the brute one on random boards
    for _ in range(300):
        n = rng.randint(4, 8)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        assert has_monotone_kap_pos(p, 4) == has_monotone_kap_brute(p, 4)
    print(f"CROSS-VALIDATION OK: open/closure/height vs literal brute force (400 boards); "
          f"closure vs experiments/forcing_closure.py (300 boards); Thm16 re-verified on "
          f"{tot} 4-AP-free boards N<=8; apcheck fast==brute (300 boards).")


if __name__ == "__main__":
    _crossvalidate()
