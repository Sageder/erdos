"""zcheck.py — monotone-AP checkers adapted to two-sided (Z-indexed) windows. Route R8.

Conventions (pinned):
  * A permutation of Z here means a bijection b : Z -> Z (positions Z, values Z), viewed as the
    doubly infinite sequence ..., b(-1), b(0), b(1), ....  [This is the Z-analogue object; it
    differs from our one-sided problem where a : N -> N with N = {1,2,3,...}.]
  * A monotone k-AP of b: positions p_1 < ... < p_k (in Z) and values forming an AP with
    common difference +-d (d >= 1), i.e. values read along increasing positions are
    x, x+d, ..., x+(k-1)d (increasing orientation) or x+(k-1)d, ..., x (decreasing).
  * Every monotone k-AP of b lies inside some finite centered window b[-m..m]; conversely any
    monotone k-AP of a window is one of b.  So checking growing centered windows is exact
    "no monotone k-AP up to window m" verification.

A finite window is a list of distinct integers (any sign).  These checkers do NOT assume
values are positive or form an interval.

Cross-validated below (__main__) against experiments/apcheck.py brute force on random
signed sequences.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                "experiments"))
from apcheck import has_monotone_kap_brute  # noqa: E402  (ground truth; sign-agnostic)


def has_monotone_kap_window(seq, k):
    """Exact check for a finite sequence of distinct integers (any sign).

    Scans all APs inside the value set: for each value pair (x, y), x < y, with y = x + d,
    tests whether x, x+d, ..., x+(k-1)d are all present with strictly increasing or strictly
    decreasing positions.  O(m^2 * k) with a dict.  Same logic as apcheck.has_monotone_kap_general
    but re-stated here for signed values (that implementation is in fact sign-agnostic; we keep
    an independent copy and cross-validate both against brute force)."""
    posmap = {v: i for i, v in enumerate(seq)}
    vals = sorted(posmap)
    vset = set(vals)
    m = len(vals)
    for ai in range(m):
        x = vals[ai]
        for bi in range(ai + 1, m):
            d = vals[bi] - x
            terms = [x + j * d for j in range(k)]
            if not all(t in vset for t in terms):
                continue
            ps = [posmap[t] for t in terms]
            if all(ps[j] < ps[j + 1] for j in range(k - 1)):
                return True
            if all(ps[j] > ps[j + 1] for j in range(k - 1)):
                return True
    return False


def find_monotone_kaps(seq, k, limit=None):
    """Return list of witnesses (value_tuple, position_tuple, orientation) of monotone k-APs
    in the finite sequence seq of distinct integers.  positions are 0-based indices into seq.
    orientation is +1 (values increase along positions) or -1.  If limit is not None, stop
    after that many witnesses."""
    posmap = {v: i for i, v in enumerate(seq)}
    vals = sorted(posmap)
    vset = set(vals)
    out = []
    m = len(vals)
    for ai in range(m):
        x = vals[ai]
        for bi in range(ai + 1, m):
            d = vals[bi] - x
            terms = [x + j * d for j in range(k)]
            if not all(t in vset for t in terms):
                continue
            ps = [posmap[t] for t in terms]
            if all(ps[j] < ps[j + 1] for j in range(k - 1)):
                out.append((tuple(terms), tuple(ps), +1))
            elif all(ps[j] > ps[j + 1] for j in range(k - 1)):
                out.append((tuple(terms[::-1]), tuple(ps[::-1]), -1))
            if limit is not None and len(out) >= limit:
                return out
    return out


def centered_window(bfunc, m):
    """Window [b(-m), ..., b(m)] of a Z-permutation given as a callable."""
    return [bfunc(p) for p in range(-m, m + 1)]


def covered_centered_interval(values):
    """Largest n >= 0 such that all of -n..n appear in values (surjectivity evidence for a
    claimed Z-bijection window).  Returns -1 if 0 is absent."""
    vset = set(values)
    if 0 not in vset:
        return -1
    n = 0
    while (n + 1) in vset and -(n + 1) in vset:
        n += 1
    return n


def covered_initial_interval(values):
    """Largest n >= 0 with all of 1..n present (for N-side prefixes)."""
    vset = set(values)
    n = 0
    while (n + 1) in vset:
        n += 1
    return n


if __name__ == "__main__":
    import random

    rng = random.Random(1958)
    # cross-validate window checker against literal brute force on signed sequences
    for trial in range(4000):
        n = rng.randint(4, 10)
        vals = rng.sample(range(-25, 26), n)
        for k in (3, 4, 5):
            got = has_monotone_kap_window(vals, k)
            ref = has_monotone_kap_brute(vals, k)
            assert got == ref, (vals, k, got, ref)
            wit = find_monotone_kaps(vals, k, limit=1)
            assert (len(wit) > 0) == got, (vals, k)
    # witness sanity: every reported witness really is a monotone k-AP
    for trial in range(500):
        n = rng.randint(6, 12)
        vals = rng.sample(range(-40, 41), n)
        for k in (3, 4):
            for terms, ps, orient in find_monotone_kaps(vals, k):
                assert len(set(terms)) == k
                dset = {terms[j + 1] - terms[j] for j in range(k - 1)}
                assert len(dset) == 1
                d = dset.pop()
                assert (d > 0) == (orient == +1) or (d < 0) == (orient == -1)
                assert all(ps[j] < ps[j + 1] for j in range(k - 1)) or \
                       all(ps[j] > ps[j + 1] for j in range(k - 1))
                assert all(vals[p] == t for p, t in zip(ps, terms))
    assert covered_centered_interval([0, 1, -1, 2, -2, 5]) == 2
    assert covered_centered_interval([1, -1]) == -1
    assert covered_initial_interval([2, 1, 3, 7]) == 3
    print("zcheck cross-validation OK: 4000 signed windows vs brute force, k in {3,4,5}; "
          "witness extraction consistent.")
