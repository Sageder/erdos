"""r6lib.py — shared tools for route R6 (density / Szemerédi structure).

Conventions match /home/user/erdos/experiments/apcheck.py:
a permutation is a tuple/list `perm` with perm[i] = value at position i+1
(0-indexed lists, 1-indexed math positions).  pos[v] = 0-indexed position of v.

Everything here is exact combinatorics; no floating point in any assertion.
"""

import sys
from bisect import bisect_left, insort

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import (  # noqa: E402
    has_monotone_kap_brute,
    has_monotone_kap_general,
    has_monotone_kap_pos,
)

# ---------------------------------------------------------------- constructions


def reversed_blocks(ratio, num_blocks):
    """Permutation of [1 .. ratio^num_blocks - 1]: blocks [r^k, r^{k+1}) each
    listed in DECREASING value order, blocks in increasing order, k=0..num_blocks-1.
    ratio=2: the 'dyadic reversed' example; ratio=3: 'triadic reversed'."""
    seq = []
    for k in range(num_blocks):
        seq.extend(range(ratio ** (k + 1) - 1, ratio**k - 1, -1))
    return seq


# ------------------------------------------------------------------- statistics


def positions_of(perm):
    """pos[v] = 0-indexed position of value v (dict, works for general value sets)."""
    return {v: i for i, v in enumerate(perm)}


def lis_length(perm):
    """Length of longest strictly increasing subsequence (patience, O(n log n))."""
    tails = []
    for v in perm:
        j = bisect_left(tails, v)
        if j == len(tails):
            tails.append(v)
        else:
            tails[j] = v
    return len(tails)


def lds_length(perm):
    return lis_length([-v for v in perm])


def dec_patience_labels(perm):
    """ell[i] = length of the longest strictly DECREASING subsequence ending at
    position i (0-indexed).  Level sets of ell are the 'piles': each pile is a
    strictly increasing subsequence, and max(ell) = LDS.  O(n log n)."""
    # longest decreasing ending at i on perm == longest increasing ending at i on -perm
    tails = []  # tails[j] = max over incr. subseqs of length j+1 (on -perm) of last elt... use standard trick
    ell = []
    neg = [-v for v in perm]
    for v in neg:
        j = bisect_left(tails, v)
        if j == len(tails):
            tails.append(v)
        else:
            tails[j] = v
        ell.append(j + 1)
    return ell


def inc_patience_labels(perm):
    """ell[i] = length of longest strictly INCREASING subsequence ending at i."""
    tails = []
    ell = []
    for v in perm:
        j = bisect_left(tails, v)
        if j == len(tails):
            tails.append(v)
        else:
            tails[j] = v
        ell.append(j + 1)
    return ell


def piles(perm, orientation="dec"):
    """Partition of the VALUE set into piles = level sets of the patience label.
    orientation='dec': labels by longest decreasing subseq ending here; each pile
    is an increasing subsequence (in position order).  Returns list of lists of
    values, pile j at index j-1, values in position order."""
    ell = dec_patience_labels(perm) if orientation == "dec" else inc_patience_labels(perm)
    out = [[] for _ in range(max(ell, default=0))]
    for i, v in enumerate(perm):
        out[ell[i] - 1].append(v)
    return out


def records(perm):
    """Left-to-right maxima values, in position order (an increasing subsequence)."""
    out, m = [], 0
    for v in perm:
        if v > m:
            out.append(v)
            m = v
    return out


def lr_minima(perm):
    out, m = [], None
    for v in perm:
        if m is None or v < m:
            out.append(v)
            m = v
    return out


# ------------------------------------------------ orientation-specific checkers


def incr_4aps(seq, limit=None):
    """All (x,d) with x,x+d,x+2d,x+3d in the value set and positions strictly
    increasing (increasing-orientation monotone 4-APs).  seq = arbitrary distinct
    positive ints in position order."""
    posmap = positions_of(seq)
    vmax = max(posmap)
    found = []
    for d in range(1, (vmax - 1) // 3 + 1):
        for x in range(1, vmax - 3 * d + 1):
            t = (x, x + d, x + 2 * d, x + 3 * d)
            if all(v in posmap for v in t):
                p = [posmap[v] for v in t]
                if p[0] < p[1] < p[2] < p[3]:
                    found.append((x, d))
                    if limit and len(found) >= limit:
                        return found
    return found


def decr_4aps(seq, limit=None):
    """All (x,d) with x+3d,x+2d,x+d,x read at strictly increasing positions
    (decreasing-orientation monotone 4-APs)."""
    posmap = positions_of(seq)
    vmax = max(posmap)
    found = []
    for d in range(1, (vmax - 1) // 3 + 1):
        for x in range(1, vmax - 3 * d + 1):
            t = (x, x + d, x + 2 * d, x + 3 * d)
            if all(v in posmap for v in t):
                p = [posmap[v] for v in t]
                if p[0] > p[1] > p[2] > p[3]:
                    found.append((x, d))
                    if limit and len(found) >= limit:
                        return found
    return found


def valueset_has_4ap(vals):
    """Does the SET of values contain a 4-term AP (positions ignored)?"""
    vset = set(vals)
    vs = sorted(vset)
    for i, x in enumerate(vs):
        for y in vs[i + 1 :]:
            d = y - x
            if x + 3 * d > vs[-1]:
                break
            if y + d in vset and y + 2 * d in vset:
                return True
    return False


def valueset_has_3ap(vals):
    vset = set(vals)
    vs = sorted(vset)
    for i, x in enumerate(vs):
        for y in vs[i + 1 :]:
            d = y - x
            if x + 2 * d > vs[-1]:
                break
            if y + d in vset:
                return True
    return False


# --------------------------------------------------------------------- r_4(N)


def r4_exact_small(n):
    """Exact max size of a 4-AP-free subset of [1..n], brute force (n <= ~24)."""
    aps = []
    for d in range(1, (n - 1) // 3 + 1):
        for x in range(1, n - 3 * d + 1):
            aps.append((x, x + d, x + 2 * d, x + 3 * d))
    best = [0]

    def rec(v, chosen_mask, count):
        if count + (n - v + 1) <= best[0]:
            return
        if v > n:
            best[0] = max(best[0], count)
            return
        # try taking v
        ok = True
        for a, b, c, e in aps:
            if e == v and (chosen_mask >> a) & 1 and (chosen_mask >> b) & 1 and (chosen_mask >> c) & 1:
                ok = False
                break
        if ok:
            rec(v + 1, chosen_mask | (1 << v), count + 1)
        rec(v + 1, chosen_mask, count)

    rec(1, 0, 0)
    return best[0]


def r4_exact_cpsat(n):
    """Exact r_4(n) via CP-SAT (for larger n)."""
    from ortools.sat.python import cp_model

    m = cp_model.CpModel()
    xs = [m.NewBoolVar(f"x{v}") for v in range(n + 1)]
    for d in range(1, (n - 1) // 3 + 1):
        for x in range(1, n - 3 * d + 1):
            m.AddBoolOr(
                [xs[x].Not(), xs[x + d].Not(), xs[x + 2 * d].Not(), xs[x + 3 * d].Not()]
            )
    m.Maximize(sum(xs[1:]))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4
    status = solver.Solve(m)
    assert status == cp_model.OPTIMAL, status
    return int(solver.ObjectiveValue())


# -------------------------------------------------------- enumeration utilities


def four_ap_free_perms(n):
    """Yield all monotone-4-AP-free permutations of [1..n]."""
    from itertools import permutations

    for p in permutations(range(1, n + 1)):
        if not has_monotone_kap_pos(p, 4):
            yield p


if __name__ == "__main__":
    # self-checks
    import random

    rng = random.Random(196)
    for _ in range(300):
        n = rng.randint(4, 9)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        # LIS/LDS against brute force
        from itertools import combinations

        def brute_lis(q, sign):
            best = 1
            for r in range(2, len(q) + 1):
                any_r = False
                for idx in combinations(range(len(q)), r):
                    vals = [q[i] * sign for i in idx]
                    if all(vals[j] < vals[j + 1] for j in range(r - 1)):
                        any_r = True
                        break
                if any_r:
                    best = r
                else:
                    break
            return best

        assert lis_length(p) == brute_lis(p, 1), p
        assert lds_length(p) == brute_lis(p, -1), p
        # patience labels: piles are increasing subsequences; count = LDS
        ps = piles(p, "dec")
        assert len(ps) == lds_length(p), p
        assert sorted(sum(ps, [])) == sorted(p)
        for pile in ps:
            assert all(pile[i] < pile[i + 1] for i in range(len(pile) - 1)), (p, pile)
        psm = piles(p, "inc")
        assert len(psm) == lis_length(p), p
        for pile in psm:
            assert all(pile[i] > pile[i + 1] for i in range(len(pile) - 1)), (p, pile)
        # orientation checkers vs global checker
        both = bool(incr_4aps(p, 1)) or bool(decr_4aps(p, 1))
        assert both == has_monotone_kap_pos(p, 4), p
    # r4 brute vs cpsat
    for n in range(1, 17):
        a, b = r4_exact_small(n), r4_exact_cpsat(n)
        assert a == b, (n, a, b)
    print("r6lib self-checks OK (LIS/LDS/piles/orientation checkers/r4 cross-validated)")
