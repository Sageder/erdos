"""fastcheck.py — vectorized exact monotone k-AP checkers for large finite sequences.

has_kap_perm_np: for a permutation of [1..N] (values exactly 1..N), numpy scan over (d, x).
has_kap_vals_np: for an arbitrary finite set of distinct integers (any sign) given as a
    sequence: scans all (x, d) pairs with x, x+d in the value set via a dict; still exact,
    O(n^2) worst case but with numpy inner loop over d only when profitable -- here we keep a
    dict-based exact version optimized with sorted arrays; used for two-sided windows.
Cross-validated against apcheck brute force in __main__.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                "experiments"))
from apcheck import has_monotone_kap_brute  # noqa: E402


def has_kap_perm_np(perm, k):
    """Exact monotone k-AP check for a permutation of [1..N]. Returns bool."""
    n = len(perm)
    pos = np.empty(n + 1, dtype=np.int64)
    pos[np.asarray(perm, dtype=np.int64)] = np.arange(n, dtype=np.int64)
    maxd = (n - 1) // (k - 1)
    for d in range(1, maxd + 1):
        top = n - (k - 1) * d
        cols = [pos[1 + j * d: top + j * d + 1] for j in range(k)]
        inc = np.ones(top, dtype=bool)
        dec = np.ones(top, dtype=bool)
        for j in range(k - 1):
            inc &= cols[j] < cols[j + 1]
            dec &= cols[j] > cols[j + 1]
        if inc.any() or dec.any():
            return True
    return False


def find_kaps_perm_np(perm, k, limit=10):
    """Witnesses ((x,d,orient)) of monotone k-APs for a permutation of [1..N]."""
    n = len(perm)
    pos = np.empty(n + 1, dtype=np.int64)
    pos[np.asarray(perm, dtype=np.int64)] = np.arange(n, dtype=np.int64)
    out = []
    maxd = (n - 1) // (k - 1)
    for d in range(1, maxd + 1):
        top = n - (k - 1) * d
        cols = [pos[1 + j * d: top + j * d + 1] for j in range(k)]
        inc = np.ones(top, dtype=bool)
        dec = np.ones(top, dtype=bool)
        for j in range(k - 1):
            inc &= cols[j] < cols[j + 1]
            dec &= cols[j] > cols[j + 1]
        for x0 in np.nonzero(inc)[0]:
            out.append((int(x0) + 1, d, +1))
            if len(out) >= limit:
                return out
        for x0 in np.nonzero(dec)[0]:
            out.append((int(x0) + 1, d, -1))
            if len(out) >= limit:
                return out
    return out


def has_kap_vals_np(seq, k):
    """Exact monotone k-AP check for a sequence of distinct integers (any sign).

    Maps values to their ranks; scans all value pairs (as x and x+d) using dict lookups.
    Exact but O(n^2 k); for n up to ~6000 acceptable."""
    posmap = {v: i for i, v in enumerate(seq)}
    vals = sorted(posmap)
    vset = posmap
    n = len(vals)
    for ai in range(n):
        x = vals[ai]
        for bi in range(ai + 1, n):
            d = vals[bi] - x
            t = x + 2 * d
            ok = True
            terms = [x, x + d]
            for j in range(2, k):
                tj = x + j * d
                if tj not in vset:
                    ok = False
                    break
                terms.append(tj)
            if not ok:
                continue
            ps = [posmap[t] for t in terms]
            if all(ps[j] < ps[j + 1] for j in range(k - 1)) or \
               all(ps[j] > ps[j + 1] for j in range(k - 1)):
                return True
    return False


if __name__ == "__main__":
    import random
    rng = random.Random(7)
    for trial in range(2500):
        n = rng.randint(5, 10)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        for k in (3, 4, 5):
            ref = has_monotone_kap_brute(p, k)
            assert has_kap_perm_np(p, k) == ref, (p, k)
            assert (len(find_kaps_perm_np(p, k, limit=1)) > 0) == ref, (p, k)
        vals = rng.sample(range(-30, 31), n)
        for k in (3, 4, 5):
            assert has_kap_vals_np(vals, k) == has_monotone_kap_brute(vals, k), (vals, k)
    print("fastcheck cross-validation OK (2500 random perms + signed value sets, k in 3..5)")
