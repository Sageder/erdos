"""framework.py — Route R1: recursive block constructions for Erdős 196 (NO-side).

Claim tested here: none (library). Conventions match /home/user/erdos/PROBLEM.md:
values are 1,2,3,...; a construction is a sequence a(1), a(2), ... . We build finite
position-prefixes that contain the complete value set [1..M] and check monotone 4-AP
freeness of the value-restriction to [1..M] (restriction principle: any monotone 4-AP
of the infinite permutation with all values <= M shows up in this finite check).

Block ansatz: value set partitioned into intervals ("blocks") B_1=[s_1,s_2), B_2=[s_2,s_3),...
with s_1=1. Each block gets a gadget permutation of its interval; blocks are laid out in
positions according to an interleaving (a permutation of block indices with finite
displacement => order type omega is automatic).

Checker: vectorized numpy over (x,d); cross-validated below against the trusted
apcheck.has_monotone_kap_pos / _brute on random small permutations.
"""

import sys
import numpy as np

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute  # trusted

sys.setrecursionlimit(100000)

# ---------------------------------------------------------------- block partitions

def blocks_equal(size, nblocks):
    return [(1 + i * size, 1 + (i + 1) * size) for i in range(nblocks)]

def blocks_geometric(r, nblocks):
    """B_j = [r^{j-1}, r^j) for j=1..nblocks (so s_j = r^{j-1})."""
    return [(r ** j, r ** (j + 1)) for j in range(nblocks)]

def blocks_factorial(nblocks):
    """s_j = j! : B_j = [j!, (j+1)!)."""
    import math
    return [(math.factorial(j), math.factorial(j + 1)) for j in range(1, nblocks + 1)]

# ---------------------------------------------------------------- gadgets
# A gadget takes (lo, hi) (half-open value interval) and returns the values in
# position order (a list). All exact integer arithmetic.

def _sigma(n):
    """Parity recursion: 3-AP-free permutation of [1..n] (verified in experiments/)."""
    if n <= 1:
        return [1] * n
    odds = [2 * y - 1 for y in _sigma((n + 1) // 2)]
    evens = [2 * y for y in _sigma(n // 2)]
    return odds + evens

def gadget_sigma(lo, hi):
    n = hi - lo
    return [lo - 1 + v for v in _sigma(n)]

def gadget_sigma_revpos(lo, hi):
    return gadget_sigma(lo, hi)[::-1]

def gadget_sigma_reflect(lo, hi):
    """Value reflection v -> lo+hi-1-v applied to sigma layout."""
    n = hi - lo
    return [hi - v for v in _sigma(n)]          # hi - v = lo + (n - v) + (lo... ) check: v in 1..n -> hi-v in lo..hi-1

def gadget_sigma_reflect_revpos(lo, hi):
    return gadget_sigma_reflect(lo, hi)[::-1]

def gadget_identity(lo, hi):
    return list(range(lo, hi))

def gadget_reverse(lo, hi):
    return list(range(hi - 1, lo - 1, -1))

def gadget_evens_first(lo, hi):
    """Evens-first parity recursion (mirror of sigma's odds-first)."""
    n = hi - lo
    def tau(n):
        if n <= 1:
            return [1] * n
        evens = [2 * y for y in tau(n // 2)]
        odds = [2 * y - 1 for y in tau((n + 1) // 2)]
        return evens + odds
    return [lo - 1 + v for v in tau(n)]

def gadget_tophalf_first(lo, hi):
    """Coarse inversion: top half (recursively) then bottom half (recursively)."""
    n = hi - lo
    if n <= 1:
        return list(range(lo, hi))
    mid = lo + n // 2
    return gadget_tophalf_first(mid, hi) + gadget_tophalf_first(lo, mid)

def gadget_tophalf_sigma(lo, hi):
    """Top half in sigma order, then bottom half in sigma order (one coarse level only)."""
    n = hi - lo
    if n <= 1:
        return list(range(lo, hi))
    mid = lo + n // 2
    return gadget_sigma(mid, hi) + gadget_sigma(lo, mid)

# ---------------------------------------------------------------- assembly

def build_sequence(blocks, gadget_for_block, block_position_order=None):
    """blocks: list of (lo,hi). gadget_for_block: j (0-based) -> gadget fn.
    block_position_order: permutation of range(len(blocks)) giving the order blocks
    appear in positions (default: identity). Returns the value sequence (list)."""
    nb = len(blocks)
    order = list(range(nb)) if block_position_order is None else list(block_position_order)
    assert sorted(order) == list(range(nb)), "interleaving must be a permutation of blocks"
    seq = []
    for j in order:
        lo, hi = blocks[j]
        g = gadget_for_block(j)(lo, hi)
        assert sorted(g) == list(range(lo, hi)), f"gadget for block {j} not a perm of [{lo},{hi})"
        seq.extend(g)
    return seq

def restrict_to_M(seq, M):
    """Values 1..M in position order; asserts all of 1..M present (restriction principle)."""
    sub = [v for v in seq if v <= M]
    assert sorted(sub) == list(range(1, M + 1)), "prefix does not contain all of 1..M"
    return sub

# ---------------------------------------------------------------- fast checker

def monotone_4ap_violations(perm, max_report=50, collect=True):
    """perm: permutation of [1..M] (list). Returns list of violations
    (x, d, orient) with orient '+' (increasing) or '-' (decreasing), sorted by
    (x+3d, d, x) i.e. minimal witnesses first; at most max_report entries, but the
    RETURNED count in the second slot is exact. Vectorized over x for each d."""
    M = len(perm)
    pos = np.empty(M + 2, dtype=np.int64)
    pos[np.asarray(perm, dtype=np.int64)] = np.arange(M, dtype=np.int64)
    viol = []
    total = 0
    for d in range(1, (M - 1) // 3 + 1):
        top = M - 3 * d
        if top < 1:
            break
        p1 = pos[1:top + 1]
        p2 = pos[1 + d:top + d + 1]
        p3 = pos[1 + 2 * d:top + 2 * d + 1]
        p4 = pos[1 + 3 * d:top + 3 * d + 1]
        inc = (p1 < p2) & (p2 < p3) & (p3 < p4)
        dec = (p1 > p2) & (p2 > p3) & (p3 > p4)
        ni, nd = int(inc.sum()), int(dec.sum())
        total += ni + nd
        if collect and (ni or nd):
            for x in (np.nonzero(inc)[0] + 1):
                viol.append((int(x), d, '+'))
            for x in (np.nonzero(dec)[0] + 1):
                viol.append((int(x), d, '-'))
    viol.sort(key=lambda t: (t[0] + 3 * t[1], t[1], t[0]))
    return viol[:max_report], total

def has_monotone_4ap_np(perm):
    _, total = monotone_4ap_violations(perm, max_report=0, collect=False)
    return total > 0

def monotone_4ap_violations_general(seq, max_report=50):
    """Exact scan of ALL monotone 4-APs among an arbitrary set of distinct positive
    values given in position order (need not be a permutation of [1..M]).
    Vectorized like monotone_4ap_violations, with masking for absent values.
    Cross-validated against apcheck.has_monotone_kap_general in _selfcheck."""
    seq = list(seq)
    Vmax = max(seq)
    pos = np.full(Vmax + 2, -1, dtype=np.int64)
    pos[np.asarray(seq, dtype=np.int64)] = np.arange(len(seq), dtype=np.int64)
    viol = []
    total = 0
    for d in range(1, (Vmax - 1) // 3 + 1):
        top = Vmax - 3 * d
        if top < 1:
            break
        p1 = pos[1:top + 1]
        p2 = pos[1 + d:top + d + 1]
        p3 = pos[1 + 2 * d:top + 2 * d + 1]
        p4 = pos[1 + 3 * d:top + 3 * d + 1]
        present = (p1 >= 0) & (p2 >= 0) & (p3 >= 0) & (p4 >= 0)
        inc = present & (p1 < p2) & (p2 < p3) & (p3 < p4)
        dec = present & (p1 > p2) & (p2 > p3) & (p3 > p4)
        ni, nd = int(inc.sum()), int(dec.sum())
        total += ni + nd
        if max_report and (ni or nd):
            for x in (np.nonzero(inc)[0] + 1):
                viol.append((int(x), d, '+'))
            for x in (np.nonzero(dec)[0] + 1):
                viol.append((int(x), d, '-'))
    viol.sort(key=lambda t: (t[0] + 3 * t[1], t[1], t[0]))
    return viol[:max_report], total

# ---------------------------------------------------------------- case classification

def block_index_of(blocks, v):
    for j, (lo, hi) in enumerate(blocks):
        if lo <= v < hi:
            return j
    return None

def classify_ap(blocks, x, d):
    """Block pattern of the 4-AP values x, x+d, x+2d, x+3d, plus a case label
    for the blocks-in-increasing-order geometry (A, B1, B1', B2, B3, B4, other)."""
    bs = tuple(block_index_of(blocks, x + k * d) for k in range(4))
    if None in bs:
        return bs, '?'
    b1, b2, b3, b4 = bs
    if b1 == b2 == b3 == b4:
        lab = 'A'
    elif b1 == b2 == b3 and b4 == b3 + 1:
        lab = 'B1'
    elif b2 == b3 == b4 and b1 < b2:
        lab = "B1'"
    elif b1 == b2 and b3 == b4 == b2 + 1:
        lab = 'B2'
    elif b1 < b2 and b2 == b3 and b4 == b3 + 1:
        lab = 'B3'
    elif b1 < b2 and b3 == b4 == b2 + 1:
        lab = 'B4'
    else:
        lab = 'other'
    return bs, lab

# ---------------------------------------------------------------- self-validation

def _selfcheck():
    import random
    rng = random.Random(196)
    for _ in range(800):
        n = rng.randint(4, 40)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        fast = has_monotone_4ap_np(p)
        trusted = has_monotone_kap_pos(p, 4)
        assert fast == trusted, (p,)
        if n <= 9:
            assert fast == has_monotone_kap_brute(p, 4), (p,)
    # general checker vs trusted general checker on random value sets
    from apcheck import has_monotone_kap_general
    for _ in range(400):
        n = rng.randint(4, 12)
        vals = rng.sample(range(1, 60), n)
        _, tot = monotone_4ap_violations_general(vals, max_report=0)
        assert (tot > 0) == has_monotone_kap_general(vals, 4), vals
    # violation list correctness on a couple of tiny hand cases
    v, t = monotone_4ap_violations([1, 2, 3, 4])
    assert v == [(1, 1, '+')] and t == 1
    v, t = monotone_4ap_violations([4, 3, 2, 1])
    assert v == [(1, 1, '-')] and t == 1
    v, t = monotone_4ap_violations([1, 5, 3, 7, 2, 6, 4, 8])  # sigma_8: 3-AP-free
    assert t == 0
    # gadget sanity
    for g in (gadget_sigma, gadget_sigma_revpos, gadget_sigma_reflect,
              gadget_sigma_reflect_revpos, gadget_evens_first, gadget_tophalf_first):
        out = g(5, 21)
        assert sorted(out) == list(range(5, 21)), g.__name__
    print("framework selfcheck OK (checker cross-validated on 800 perms; gadgets are perms)")

if __name__ == "__main__":
    _selfcheck()
