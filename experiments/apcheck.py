"""apcheck.py — core monotone-AP checkers for Erdős 196 experiments.

Claim tested here: none (library). Conventions: values 1..N (or 1..infinity prefixes),
a permutation is given as a tuple/list `perm` with perm[i] = value at position i+1.
A monotone k-AP: positions i_1<...<i_k, values x, x+d, ..., x+(k-1)d (d>=1) read in
increasing OR decreasing value order along those positions.

Two independent implementations:
  - has_monotone_kap_brute: literal O(C(n,k)) definition scan (only for tiny n) — ground truth.
  - has_monotone_kap_pos:   position-array scan over (x,d): O(sum_d (N-(k-1)d)) = O(N^2/d ...),
    exact, fast enough for exhaustive counts.
For value-sets that are [1..N] complete permutations both are applicable.
"""

from itertools import combinations, permutations


def has_monotone_kap_brute(perm, k):
    """Ground truth by definition: scan all k-subsets of positions."""
    n = len(perm)
    for idxs in combinations(range(n), k):
        vals = [perm[i] for i in idxs]
        d = vals[1] - vals[0]
        if d == 0:
            continue
        if all(vals[j + 1] - vals[j] == d for j in range(k - 1)):
            return True
    return False


def has_monotone_kap_pos(perm, k):
    """Fast exact check for a permutation of [1..N] (values exactly 1..N).

    pos[v] = index of value v. A monotone k-AP exists iff for some x>=1, d>=1 with
    x+(k-1)d <= N the sequence pos[x], pos[x+d], ..., pos[x+(k-1)d] is strictly
    increasing or strictly decreasing.
    """
    n = len(perm)
    pos = [0] * (n + 1)
    for i, v in enumerate(perm):
        pos[v] = i
    for d in range(1, (n - 1) // (k - 1) + 1):
        top = n - (k - 1) * d
        for x in range(1, top + 1):
            ps = [pos[x + j * d] for j in range(k)]
            inc = all(ps[j] < ps[j + 1] for j in range(k - 1))
            if inc:
                return True
            dec = all(ps[j] > ps[j + 1] for j in range(k - 1))
            if dec:
                return True
    return False


def has_monotone_kap_general(seq, k):
    """Exact check for an arbitrary finite sequence of distinct positive integers
    (not necessarily a permutation of [1..N]) — scans APs among the value set.
    Used for position-prefixes of infinite constructions."""
    posmap = {v: i for i, v in enumerate(seq)}
    vals = sorted(posmap)
    vset = set(vals)
    m = len(vals)
    for ai in range(m):
        x = vals[ai]
        for bi in range(ai + 1, m):
            d = vals[bi] - x
            # need x, x+d, ..., x+(k-1)d all present
            terms = [x + j * d for j in range(k)]
            if not all(t in vset for t in terms):
                continue
            ps = [posmap[t] for t in terms]
            if all(ps[j] < ps[j + 1] for j in range(k - 1)):
                return True
            if all(ps[j] > ps[j + 1] for j in range(k - 1)):
                return True
    return False


def count_avoiders(n, k, checker=has_monotone_kap_pos):
    """Count permutations of [1..n] with NO monotone k-AP (exhaustive)."""
    return sum(1 for p in permutations(range(1, n + 1)) if not checker(p, k))


if __name__ == "__main__":
    import random

    # Cross-validate fast vs brute on random permutations and random sequences.
    rng = random.Random(196)
    for trial in range(3000):
        n = rng.randint(4, 9)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        for k in (3, 4):
            assert has_monotone_kap_brute(p, k) == has_monotone_kap_pos(p, k) == \
                has_monotone_kap_general(p, k), (p, k)
    for trial in range(1500):
        n = rng.randint(4, 9)
        vals = rng.sample(range(1, 40), n)
        for k in (3, 4):
            assert has_monotone_kap_brute(vals, k) == has_monotone_kap_general(vals, k), (vals, k)
    print("cross-validation OK: 3000 perms + 1500 general seqs, k in {3,4}")
