"""apdisp.py — AP-restriction displacement measurement (route R21).

Definitions (PROBLEM.md / CORE.md Corollary 26 conventions).
For a permutation sigma of [1..N] (list `perm`, perm[i] = value at position i+1) and an
arithmetic progression P = {r+q, r+2q, ...} intersected with [1..N], let
p_1 < p_2 < ... < p_L be its elements in VALUE order, and

    pos_P(n) := #{ m : p_m is positioned at or before p_n }      (rank of p_n inside P)

The *relative displacement of P* is  disp(P) := max_{n<=L} pos_P(n)/n, and its
*window / tail* refinements are  disp(P; n0, n1) := max_{n0<=n<=n1} pos_P(n)/n.
Design principle D1 (CORE Corollary 26) asks, for an infinite witness, that
sup_n pos_P(n)/n = infinity for EVERY infinite AP P.

Exact rational arithmetic only: displacements are returned as Fraction.

Cross-validation (see __main__): the fast rank computation is checked against a literal
O(L^2) definition scan on random permutations, and the 4-AP checker used everywhere in
this route is `apcheck.has_monotone_kap_pos` (the trusted, brute-force-validated one).
"""

from fractions import Fraction
import sys

sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute  # noqa: E402


def ap_elements(N, q, r):
    """Elements of the AP {r+q, r+2q, ...} inside [1..N], in increasing value order."""
    out = []
    n = 1
    while r + q * n <= N:
        out.append(r + q * n)
        n += 1
    return out


def all_aps(N, qmax, min_len=1):
    """All APs r+q*N with 1<=q<=qmax, 0<=r<q (so every residue class once), listed as
    (q, r, elements). Note r ranges over 0..q-1, which enumerates every residue class
    mod q exactly once; the smallest element is r+q in [1..q]."""
    out = []
    for q in range(1, qmax + 1):
        for r in range(0, q):
            el = ap_elements(N, q, r)
            if len(el) >= min_len:
                out.append((q, r, el))
    return out


def ranks_in_subset(pos, elements):
    """pos: dict value->position (1-based). Returns [rank of elements[n] inside the
    subset], 1-based, in the order of `elements` (which must be value-sorted)."""
    order = sorted(range(len(elements)), key=lambda i: pos[elements[i]])
    rank = [0] * len(elements)
    for k, i in enumerate(order):
        rank[i] = k + 1
    return rank


def ranks_in_subset_slow(pos, elements):
    """Literal definition, O(L^2). Ground truth for cross-validation."""
    return [1 + sum(1 for w in elements if pos[w] < pos[v]) for v in elements]


def displacement(pos, elements, n_lo=1, n_hi=None):
    """max_{n_lo<=n<=n_hi} rank(n)/n as an exact Fraction, plus the argmax index."""
    rk = ranks_in_subset(pos, elements)
    L = len(elements)
    n_hi = L if n_hi is None else min(n_hi, L)
    best, arg = Fraction(0), None
    for n in range(n_lo, n_hi + 1):
        val = Fraction(rk[n - 1], n)
        if val > best:
            best, arg = val, n
    return best, arg


def pos_of(perm):
    return {v: i + 1 for i, v in enumerate(perm)}


def ap_uniformity(perm, qmax=8, theta=Fraction(0)):
    """min over APs (q<=qmax) of disp(P; n>=theta*|P|).  theta=0 -> plain displacement.
    Returns (minvalue, (q,r), argmax_index) with the minimising AP."""
    N = len(perm)
    pos = pos_of(perm)
    worst, who, argn = None, None, None
    for q, r, el in all_aps(N, qmax, min_len=1):
        n_lo = max(1, int(theta * len(el)))
        d, a = displacement(pos, el, n_lo=n_lo)
        if worst is None or d < worst:
            worst, who, argn = d, (q, r), a
    return worst, who, argn


def ap_report(perm, qmax=8):
    """Full table: for each AP, its length and displacement (plain and tail-half)."""
    N = len(perm)
    pos = pos_of(perm)
    rows = []
    for q, r, el in all_aps(N, qmax):
        d_all, a_all = displacement(pos, el)
        d_tail, a_tail = displacement(pos, el, n_lo=max(1, len(el) // 2))
        rows.append((q, r, len(el), d_all, a_all, d_tail, a_tail))
    return rows


if __name__ == "__main__":
    import random
    rng = random.Random(21196)

    # (1) rank computation: fast vs literal definition
    for _ in range(2000):
        N = rng.randint(4, 40)
        perm = list(range(1, N + 1))
        rng.shuffle(perm)
        pos = pos_of(perm)
        q = rng.randint(1, 8)
        r = rng.randrange(q)
        el = ap_elements(N, q, r)
        if not el:
            continue
        assert ranks_in_subset(pos, el) == ranks_in_subset_slow(pos, el)

    # (2) sanity: identity permutation has displacement exactly 1 on every AP
    for N in (20, 50, 121):
        perm = list(range(1, N + 1))
        u, who, _ = ap_uniformity(perm, qmax=8)
        assert u == 1, (N, u, who)

    # (3) sanity: fully reversed permutation -> pos_P(1) = L, displacement = L
    for N in (20, 50):
        perm = list(range(N, 0, -1))
        pos = pos_of(perm)
        for q, r, el in all_aps(N, 8):
            d, a = displacement(pos, el)
            assert d == Fraction(len(el), 1) and a == 1, (N, q, r, d, a)

    # (4) the trusted 4-AP checker agrees with brute force on small boards
    for _ in range(400):
        N = rng.randint(4, 8)
        perm = list(range(1, N + 1))
        rng.shuffle(perm)
        assert has_monotone_kap_pos(perm, 4) == has_monotone_kap_brute(perm, 4)

    print("apdisp.py cross-validation OK "
          "(2000 rank checks vs literal definition; identity/reversal sanity; "
          "400 4-AP checker agreements with brute force)")
