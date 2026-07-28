"""framework.py — route R20 (v log v displacement) tooling.

Everything here is exact integer arithmetic.  The vectorised checker is cross-validated
against the trusted /home/user/erdos/experiments/apcheck.py (see self_test()).

Conventions (PROBLEM.md): a candidate infinite permutation is specified by an injective
KEY function key : N -> comparable, inducing the order v < w  iff  key(v) < key(w).
By CORE.md Lemma 1/Lemma 9 this is a permutation of N of order type omega as soon as
{w : key(w) < key(v)} is finite for every v; a sufficient certificate used throughout is
key(v) >= c*v/g(v) with g slowly growing (checked numerically, flagged when only measured).

The VALUE-RESTRICTION to [1..M] (PROBLEM.md restriction principle) is the list of
1..M sorted by key; its monotone 4-APs are monotone 4-APs of the infinite object, so
4-AP-freeness of all restrictions is equivalent to 4-AP-freeness of the whole.
"""

import sys
import numpy as np

sys.path.insert(0, '/home/user/erdos/experiments')


# ----------------------------------------------------------------- checkers
def pos_array(perm):
    """perm: list/array of values 1..M in position order -> pos[v] = 0-based position."""
    M = len(perm)
    pos = np.empty(M + 1, dtype=np.int64)
    pos[0] = -1
    a = np.asarray(perm, dtype=np.int64)
    pos[a] = np.arange(M, dtype=np.int64)
    return pos


def violations(perm, k=4, want_all=False):
    """Exact vectorised search for monotone k-APs of a permutation of [1..M].
    Returns a list of (x, d, orientation) with orientation in {'+','-'}.
    If want_all is False, returns the violations of MINIMAL largest term x+(k-1)d
    (a canonical 'first kill' set), else all of them."""
    M = len(perm)
    pos = pos_array(perm)
    out = []
    best = None
    for d in range(1, (M - 1) // (k - 1) + 1):
        top = M - (k - 1) * d
        if top < 1:
            break
        xs = np.arange(1, top + 1, dtype=np.int64)
        ps = [pos[xs + j * d] for j in range(k)]
        inc = np.ones(top, dtype=bool)
        dec = np.ones(top, dtype=bool)
        for j in range(k - 1):
            inc &= ps[j] < ps[j + 1]
            dec &= ps[j] > ps[j + 1]
        for sign, mask in (('+', inc), ('-', dec)):
            if mask.any():
                for x in xs[mask]:
                    x = int(x)
                    tot = x + (k - 1) * d
                    if want_all:
                        out.append((x, d, sign))
                    else:
                        if best is None or tot < best:
                            best, out = tot, [(x, d, sign)]
                        elif tot == best:
                            out.append((x, d, sign))
    return out


def is_free(perm, k=4):
    """Fast boolean: no monotone k-AP."""
    M = len(perm)
    pos = pos_array(perm)
    for d in range(1, (M - 1) // (k - 1) + 1):
        top = M - (k - 1) * d
        if top < 1:
            break
        xs = np.arange(1, top + 1, dtype=np.int64)
        ps = [pos[xs + j * d] for j in range(k)]
        inc = np.ones(top, dtype=bool)
        dec = np.ones(top, dtype=bool)
        for j in range(k - 1):
            inc &= ps[j] < ps[j + 1]
            dec &= ps[j] > ps[j + 1]
        if inc.any() or dec.any():
            return False
    return True


# ------------------------------------------------------- key -> restriction
def restrict(key, M):
    """Values 1..M sorted by key -> the value-restriction permutation of [1..M]."""
    vals = list(range(1, M + 1))
    vals.sort(key=key)
    return vals


def profile(perm):
    """pos(v) for the restriction; returns array indexed by value (1-based)."""
    pos = pos_array(perm)
    return pos[1:] + 1


def profile_report(key, M, sample=None):
    perm = restrict(key, M)
    p = profile(perm)
    vs = np.arange(1, M + 1)
    ratio = p / vs
    lg = np.log2(2 * vs)
    return {
        'max_ratio': float(ratio.max()), 'argmax_ratio': int(vs[ratio.argmax()]),
        'max_alpha': float((p / (vs * lg)).max()),
        'argmax_alpha': int(vs[(p / (vs * lg)).argmax()]),
    }


# ------------------------------------------------------------- self testing
def self_test():
    import random
    from apcheck import has_monotone_kap_pos, has_monotone_kap_brute
    rng = random.Random(2096)
    for _ in range(2000):
        n = rng.randint(4, 11)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        for k in (3, 4):
            a = has_monotone_kap_pos(p, k)
            b = not is_free(p, k)
            c = has_monotone_kap_brute(p, k)
            assert a == b == c, (p, k, a, b, c)
    # violation lists agree with a brute enumeration of all (x,d)
    for _ in range(400):
        n = rng.randint(6, 18)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        pos = {v: i for i, v in enumerate(p)}
        brute = []
        for d in range(1, (n - 1) // 3 + 1):
            for x in range(1, n - 3 * d + 1):
                q = [pos[x + j * d] for j in range(4)]
                if q[0] < q[1] < q[2] < q[3]:
                    brute.append((x, d, '+'))
                if q[0] > q[1] > q[2] > q[3]:
                    brute.append((x, d, '-'))
        assert sorted(violations(p, 4, want_all=True)) == sorted(brute), p
    print("framework self-test OK (2000 perms k=3,4 vs apcheck brute+pos; "
          "400 exact violation-set comparisons)")


if __name__ == "__main__":
    self_test()
