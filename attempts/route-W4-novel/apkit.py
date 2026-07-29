"""apkit.py — vectorized monotone-4-AP checker + order-type-omega diagnostics.

Conventions (PROBLEM.md governs): values are 1..N. `pos` is a length-(N+1) int array
with pos[v] = rank (0-indexed position) of value v.  A monotone 4-AP is x, x+d, x+2d,
x+3d (d>=1) whose positions are strictly increasing OR strictly decreasing.

Cross-validated against /home/user/erdos/experiments/apcheck.py in __main__.
"""
import numpy as np
import sys

sys.path.insert(0, "/home/user/erdos/experiments")


def pos_from_key(N, keyfn):
    """Order values 1..N by keyfn; return (pos array, value list in order)."""
    vals = sorted(range(1, N + 1), key=keyfn)
    pos = np.zeros(N + 1, dtype=np.int64)
    for i, v in enumerate(vals):
        pos[v] = i
    return pos, vals


def pos_from_order(order):
    """order = list of values in position order (a permutation of 1..N)."""
    N = len(order)
    pos = np.zeros(N + 1, dtype=np.int64)
    for i, v in enumerate(order):
        pos[v] = i
    return pos


def find_4aps(pos, N, want_all=False, dmax=None):
    """Return list of monotone 4-APs (x, d, 'inc'/'dec') among values 1..N.

    If want_all is False, returns at most the lexicographically-minimal one under
    the key (x+3d, d, x) -- i.e. the 4-AP with the smallest top value, tie-broken by
    smallest step.  Exact integer arithmetic throughout.
    """
    p = np.asarray(pos)
    hits = []
    dtop = (N - 1) // 3 if dmax is None else min(dmax, (N - 1) // 3)
    for d in range(1, dtop + 1):
        top = N - 3 * d
        if top < 1:
            break
        xs = np.arange(1, top + 1)
        p1 = p[xs]
        p2 = p[xs + d]
        p3 = p[xs + 2 * d]
        p4 = p[xs + 3 * d]
        inc = (p1 < p2) & (p2 < p3) & (p3 < p4)
        dec = (p1 > p2) & (p2 > p3) & (p3 > p4)
        for idx in np.nonzero(inc)[0]:
            hits.append((int(xs[idx]) + 3 * d, d, int(xs[idx]), "inc"))
        for idx in np.nonzero(dec)[0]:
            hits.append((int(xs[idx]) + 3 * d, d, int(xs[idx]), "dec"))
        if hits and not want_all:
            # cannot stop: a larger d could give a smaller top.  keep going but
            # we can bound: top >= 3d+1 so once 3*d+1 > best_top we may stop.
            best_top = min(h[0] for h in hits)
            if 3 * (d + 1) + 1 > best_top:
                break
    if not hits:
        return []
    hits.sort()
    return hits if want_all else [hits[0]]


def has_4ap(pos, N):
    return len(find_4aps(pos, N)) > 0


def survives_to(keyfn, Nmax, step=None, verbose=False):
    """Largest N (from a doubling ladder) at which value-restriction to [1..N] is
    4-AP-free; returns (last_good_N, first_failure or None)."""
    pos, _ = pos_from_key(Nmax, keyfn)
    hits = find_4aps(pos, Nmax)
    if not hits:
        return Nmax, None
    return hits[0][0] - 1, hits[0]


def omega_profile(keyfn, N, probes=None):
    """Diagnostic for order type omega.  pred_N(v) = #{w<=N : key(w)<key(v)}.
    For a genuine type-omega order this stabilizes in N for each fixed v.
    Returns dict v -> pred_N(v)."""
    pos, _ = pos_from_key(N, keyfn)
    if probes is None:
        probes = [1, 2, 3, 5, 8, 13]
    return {v: int(pos[v]) for v in probes if v <= N}


def max_displacement(keyfn, N):
    pos, _ = pos_from_key(N, keyfn)
    v = np.arange(1, N + 1)
    return float(np.max((pos[1:] + 1) / v))


if __name__ == "__main__":
    import random
    from apcheck import has_monotone_kap_pos, has_monotone_kap_brute

    rng = random.Random(19604)
    bad = 0
    for _ in range(4000):
        n = rng.randint(4, 11)
        perm = list(range(1, n + 1))
        rng.shuffle(perm)
        pos = pos_from_order(perm)
        mine = has_4ap(pos, n)
        theirs = has_monotone_kap_pos(perm, 4)
        if mine != theirs:
            bad += 1
            print("MISMATCH", perm, mine, theirs)
    # also verify the reported witness is genuine, and minimality of top value
    for _ in range(2000):
        n = rng.randint(6, 14)
        perm = list(range(1, n + 1))
        rng.shuffle(perm)
        pos = pos_from_order(perm)
        hits = find_4aps(pos, n)
        allhits = find_4aps(pos, n, want_all=True)
        if hits:
            top, d, x, orient = hits[0]
            ps = [int(pos[x + j * d]) for j in range(4)]
            assert x + 3 * d == top
            ok = all(ps[j] < ps[j + 1] for j in range(3)) if orient == "inc" else \
                all(ps[j] > ps[j + 1] for j in range(3))
            assert ok, (perm, hits[0])
            assert top == min(h[0] for h in allhits), (perm, hits, allhits[:3])
        else:
            assert not allhits
    # brute-force ground truth on tiny n
    for _ in range(1500):
        n = rng.randint(4, 9)
        perm = list(range(1, n + 1))
        rng.shuffle(perm)
        pos = pos_from_order(perm)
        assert has_4ap(pos, n) == has_monotone_kap_brute(perm, 4), perm
    print("apkit cross-validation OK (%d mismatches vs apcheck; brute-force agreed)" % bad)
