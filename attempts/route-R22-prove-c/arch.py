"""arch.py -- class-architecture engine + forcing tools for route R22-C.

Conventions (PROBLEM.md governs).  A CLASS ARCHITECTURE on [1..N] is given by
  * a class function c : [1..N] -> Z_{>=0}   (finite fibres automatic on a finite board),
  * for each class index m, a linear order  <_m  on the fibre F_m = c^{-1}(m).
The induced permutation lists F_0 (in order <_0), then F_1, then F_2, ...
So   pos(v) < pos(w)   iff   c(v) < c(w)   or  ( c(v) == c(w) and v <_{c(v)} w ).

Everything is exact integer arithmetic.  The monotone-4-AP checker used here is
apcheck.has_monotone_kap_general / _pos (trusted, brute-force validated); a fast
violation *enumerator* is provided and cross-validated against it.
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import (has_monotone_kap_brute, has_monotone_kap_pos,
                     has_monotone_kap_general)


# ---------------------------------------------------------------- architectures

def blockindex(v, b):
    """j(v) = floor(log_b v), exact integer arithmetic (no floats)."""
    assert v >= 1
    j, p = 0, 1
    while p * b <= v:
        p *= b
        j += 1
    return j


def perm_from_arch(N, c, within):
    """within[m] = list of the values of fibre m in the chosen within-class order.
    Returns perm (list, perm[i] = value at position i+1) and pos array."""
    order = []
    for m in sorted(within):
        order.extend(within[m])
    assert sorted(order) == list(range(1, N + 1)), "not a permutation of [1..N]"
    pos = [0] * (N + 1)
    for i, v in enumerate(order):
        pos[v] = i + 1
    return order, pos


def fibres(N, c, key=None):
    """dict m -> sorted list of values with c(v)=m."""
    F = {}
    for v in range(1, N + 1):
        F.setdefault(c(v), []).append(v)
    if key is not None:
        for m in F:
            F[m] = sorted(F[m], key=key)
    return F


# ------------------------------------------------------- monotone-4-AP scanning

def ap4_violations(pos, N, orientation='both'):
    """All (x,d) with x+3d <= N whose positions are strictly monotone.
    Returns list of (x, d, 'inc'/'dec'). Fast O(N^2/3) scan."""
    out = []
    d = 1
    while x_ok := (1 + 3 * d <= N):
        for x in range(1, N - 3 * d + 1):
            p0, p1, p2, p3 = pos[x], pos[x + d], pos[x + 2 * d], pos[x + 3 * d]
            if p0 < p1 < p2 < p3:
                if orientation in ('both', 'inc'):
                    out.append((x, d, 'inc'))
            elif p0 > p1 > p2 > p3:
                if orientation in ('both', 'dec'):
                    out.append((x, d, 'dec'))
        d += 1
    return out


def class_seq_violations(N, c):
    """Condition (ii) violations: 4-APs whose CLASS sequence is strictly monotone."""
    out = []
    d = 1
    while 1 + 3 * d <= N:
        for x in range(1, N - 3 * d + 1):
            a, bb, cc, dd = c(x), c(x + d), c(x + 2 * d), c(x + 3 * d)
            if a < bb < cc < dd:
                out.append((x, d, 'inc'))
            elif a > bb > cc > dd:
                out.append((x, d, 'dec'))
        d += 1
    return out


# ------------------------------------------------------------------- forcing

def open_scales(pos, u, N):
    """d >= 1 with u-2d >= 1 and pos[u-2d] < pos[u-d] < pos[u]  (Theorem 16)."""
    return [d for d in range(1, (u - 1) // 2 + 1)
            if pos[u - 2 * d] < pos[u - d] < pos[u]]


def antiopen_scales(pos, u, N):
    """d >= 1 with u-2d >= 1 and pos[u-2d] > pos[u-d] > pos[u]  (dual forcing)."""
    return [d for d in range(1, (u - 1) // 2 + 1)
            if pos[u - 2 * d] > pos[u - d] > pos[u]]


def closure(pos, u0, N):
    """Forward closure under u -> u+d for open scales d, staying <= N."""
    seen, stack = {u0}, [u0]
    while stack:
        u = stack.pop()
        for d in open_scales(pos, u, N):
            w = u + d
            if w <= N and w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


# --------------------------------------------------------------- self-tests

if __name__ == "__main__":
    import random
    rng = random.Random(22196)

    # (1) ap4_violations cross-validated against the trusted checkers.
    bad = 0
    for _ in range(4000):
        n = rng.randint(4, 9)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        pos = [0] * (n + 1)
        for i, v in enumerate(p):
            pos[v] = i + 1
        mine = len(ap4_violations(pos, n)) > 0
        ref1 = has_monotone_kap_brute(p, 4)
        ref2 = has_monotone_kap_pos(p, 4)
        ref3 = has_monotone_kap_general(p, 4)
        assert ref1 == ref2 == ref3
        if mine != ref1:
            bad += 1
    print("ap4_violations vs apcheck (3 impls), 4000 random perms n=4..9: mismatches =", bad)

    # exact violation-SET comparison against a literal enumeration
    from itertools import combinations
    for _ in range(600):
        n = rng.randint(5, 11)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        pos = [0] * (n + 1)
        for i, v in enumerate(p):
            pos[v] = i + 1
        mine = set(ap4_violations(pos, n))
        lit = set()
        for idxs in combinations(range(n), 4):
            vals = [p[i] for i in idxs]
            d = vals[1] - vals[0]
            if d != 0 and all(vals[j + 1] - vals[j] == d for j in range(3)):
                if d > 0:
                    lit.add((vals[0], d, 'inc'))
                else:
                    lit.add((vals[3], -d, 'dec'))
        assert mine == lit, (p, mine ^ lit)
    print("ap4_violations exact violation-set match vs literal enumeration: 600/600 OK")

    # (2) blockindex exactness
    for b in (2, 3, 4, 5, 10):
        for v in range(1, 5000):
            j = blockindex(v, b)
            assert b ** j <= v < b ** (j + 1)
    print("blockindex exact on v<=5000, b in {2,3,4,5,10}: OK")

    # (3) architecture <-> permutation consistency
    N = 200
    b = 3
    c = lambda v: blockindex(v, b)
    F = fibres(N, c)
    within = {m: sorted(F[m], reverse=True) for m in F}   # triadic reversed blocks
    perm, pos = perm_from_arch(N, c, within)
    for v in range(1, N + 1):
        for w in range(1, N + 1):
            if v == w:
                continue
            exp = (c(v) < c(w)) or (c(v) == c(w) and within[c(v)].index(v) < within[c(w)].index(w))
            assert (pos[v] < pos[w]) == exp
    print("architecture->permutation order law verified pairwise at N=200: OK")
