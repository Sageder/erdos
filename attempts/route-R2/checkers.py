"""checkers.py — vectorized exact monotone-AP checkers (numpy int64, exact),
cross-validated against the brute-force ground truth in experiments/apcheck.py
before use.  Run as a script to perform the cross-validation.

Conventions match apcheck.py: perm is a permutation of [1..N], perm[i] = value
at position i+1.  A monotone k-AP: positions p_1<...<p_k carrying values
x, x+d, ..., x+(k-1)d (d>=1) in ascending or descending value order.
"""

import sys

import numpy as np

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_brute, has_monotone_kap_pos  # noqa: E402


def _posarray(perm):
    perm = np.asarray(perm, dtype=np.int64)
    n = len(perm)
    pos = np.empty(n + 1, dtype=np.int64)
    pos[perm] = np.arange(n, dtype=np.int64)
    return n, pos


def find_monotone_kap(perm, k, orientation="both"):
    """Return one witness (x, d, 'inc'|'dec') or None.  Exact, O(N^2/1) int64."""
    n, pos = _posarray(perm)
    for d in range(1, (n - 1) // (k - 1) + 1):
        top = n - (k - 1) * d
        x = np.arange(1, top + 1, dtype=np.int64)
        P = [pos[x + j * d] for j in range(k)]
        inc = np.ones(top, dtype=bool)
        dec = np.ones(top, dtype=bool)
        for j in range(k - 1):
            inc &= P[j] < P[j + 1]
            dec &= P[j] > P[j + 1]
        if orientation == "inc":
            bad = inc
        elif orientation == "dec":
            bad = dec
        else:
            bad = inc | dec
        if bad.any():
            i = int(np.argmax(bad))
            return (int(x[i]), d, "inc" if inc[i] else "dec")
    return None


def enumerate_monotone_kaps(perm, k):
    """List ALL monotone k-APs as (x, d, orientation). Exact."""
    n, pos = _posarray(perm)
    out = []
    for d in range(1, (n - 1) // (k - 1) + 1):
        top = n - (k - 1) * d
        x = np.arange(1, top + 1, dtype=np.int64)
        P = [pos[x + j * d] for j in range(k)]
        inc = np.ones(top, dtype=bool)
        dec = np.ones(top, dtype=bool)
        for j in range(k - 1):
            inc &= P[j] < P[j + 1]
            dec &= P[j] > P[j + 1]
        for i in np.nonzero(inc)[0]:
            out.append((int(x[i]), d, "inc"))
        for i in np.nonzero(dec)[0]:
            out.append((int(x[i]), d, "dec"))
    return out


def _brute_oriented(perm, k, orientation):
    """Independent tiny ground truth for orientation-split checks."""
    from itertools import combinations
    n = len(perm)
    for idxs in combinations(range(n), k):
        vals = [perm[i] for i in idxs]
        d = vals[1] - vals[0]
        if d == 0 or not all(vals[j + 1] - vals[j] == d for j in range(k - 1)):
            continue
        if d > 0 and orientation in ("inc", "both"):
            return True
        if d < 0 and orientation in ("dec", "both"):
            return True
    return False


if __name__ == "__main__":
    import random

    rng = random.Random(20260727)
    trials = 4000
    for t in range(trials):
        n = rng.randint(5, 11)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        for k in (3, 4, 5):
            if n < k:
                continue
            gt = has_monotone_kap_brute(p, k)
            fast = has_monotone_kap_pos(p, k)
            mine = find_monotone_kap(p, k) is not None
            enum = len(enumerate_monotone_kaps(p, k)) > 0
            assert gt == fast == mine == enum, (p, k)
            for orient in ("inc", "dec"):
                bo = _brute_oriented(p, k, orient)
                fo = find_monotone_kap(p, k, orient) is not None
                eo = any(o == orient for (_, _, o) in
                         enumerate_monotone_kaps(p, k))
                assert bo == fo == eo, (p, k, orient)
    # also validate enumeration contents against a direct scan on a few perms
    for t in range(200):
        n = rng.randint(5, 10)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        pos = {v: i for i, v in enumerate(p)}
        for k in (3, 4):
            direct = set()
            for d in range(1, (n - 1) // (k - 1) + 1):
                for x in range(1, n - (k - 1) * d + 1):
                    ps = [pos[x + j * d] for j in range(k)]
                    if all(ps[j] < ps[j + 1] for j in range(k - 1)):
                        direct.add((x, d, "inc"))
                    if all(ps[j] > ps[j + 1] for j in range(k - 1)):
                        direct.add((x, d, "dec"))
            assert direct == set(enumerate_monotone_kaps(p, k)), (p, k)
    print("checkers cross-validation OK: %d random perms, k in {3,4,5}, "
          "both orientations, plus 200 full-enumeration comparisons" % trials)
