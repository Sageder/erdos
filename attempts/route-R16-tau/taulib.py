"""taulib.py — route R16-tau: independent library for the base-3 priority comparator tau.

Conventions: PROBLEM.md.  N = {1,2,...}.  A monotone 4-AP is (x, x+d, x+2d, x+3d), d>=1,
read in increasing OR decreasing value order along increasing positions.

Everything is exact integer arithmetic.  Every checker in here is cross-validated against
/home/user/erdos/experiments/apcheck.py (trusted, brute-force validated) in selfcheck().
"""

import sys
from itertools import permutations, combinations

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import (has_monotone_kap_pos, has_monotone_kap_brute,
                     has_monotone_kap_general)

# ------------------------------------------------------------------ digits


def v3(n):
    """3-adic valuation of n != 0."""
    assert n != 0
    n = abs(n)
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def dig3(n, l):
    return (n // 3 ** l) % 3


def top3(n):
    """Top base-3 level of n >= 1."""
    l = 0
    while 3 ** (l + 1) <= n:
        l += 1
    return l


# ------------------------------------------------------------------ tau comparator


class Tau:
    """Generalized base-3 priority comparator.

    prio(l, c) -> a tuple p of length 3, p[digit] = rank (lower rank = earlier).
    c = n mod 3**l is the shared low-digit context (context-free tau: ignore c).

    Order:  u before w  iff  at l = v3(w-u)  we have prio(l,c)[dig3(u,l)] < prio(l,c)[dig3(w,l)].
    """

    def __init__(self, prio=None, depth=24, name="tau"):
        self.prio = prio if prio is not None else (lambda l, c: (0, 1, 2))
        self.depth = depth
        self.name = name

    def key(self, n):
        """Lexicographic key (low level first) realizing the comparator as a sort key."""
        k = []
        m, c, p3 = n, 0, 1
        for l in range(self.depth):
            d = m % 3
            k.append(self.prio(l, c)[d])
            c += d * p3
            p3 *= 3
            m //= 3
        return tuple(k)

    def before(self, u, w):
        """True iff u precedes w (u != w)."""
        assert u != w
        l = v3(w - u)
        c = u % 3 ** l
        p = self.prio(l, c)
        return p[dig3(u, l)] < p[dig3(w, l)]

    def sort(self, values):
        return sorted(values, key=self.key)

    # ---- structure of the level-l priority
    def x123(self, l, c=0):
        """(x1,x2,x3) = digits sorted by prio(l,c); x1 first."""
        p = self.prio(l, c)
        return tuple(sorted((0, 1, 2), key=lambda d: p[d]))

    def delta_star(self, l, c=0):
        x1, x2, x3 = self.x123(l, c)
        return (x2 - x1) % 3


def prio_const(p):
    p = tuple(p)
    return lambda l, c: p


def prio_levels(ps):
    ps = [tuple(p) for p in ps]
    return lambda l, c: ps[l % len(ps)]


# ------------------------------------------------------------------ AP scanning


def mono4_witnesses(seq, cap=None, dfilter=None):
    """All monotone 4-APs of a finite sequence `seq` of DISTINCT positive integers.

    Returns list of (x, d, orient) with orient=+1 increasing, -1 decreasing.
    Only APs all four of whose terms are present in seq are reported.
    dfilter: optional predicate on d.
    """
    pos = {v: i for i, v in enumerate(seq)}
    vals = sorted(pos)
    vset = set(vals)
    out = []
    if not vals:
        return out
    hi = vals[-1]
    lo = vals[0]
    for d in range(1, (hi - lo) // 3 + 1):
        if dfilter is not None and not dfilter(d):
            continue
        for x in vals:
            if x + 3 * d > hi:
                continue
            t1, t2, t3 = x + d, x + 2 * d, x + 3 * d
            if t1 not in vset or t2 not in vset or t3 not in vset:
                continue
            p = (pos[x], pos[t1], pos[t2], pos[t3])
            if p[0] < p[1] < p[2] < p[3]:
                out.append((x, d, 1))
            elif p[0] > p[1] > p[2] > p[3]:
                out.append((x, d, -1))
            if cap and len(out) >= cap:
                return out
    return out


def first_mono4(seq, dfilter=None):
    """Witness with the smallest max-term, or None."""
    w = mono4_witnesses(seq, dfilter=dfilter)
    if not w:
        return None
    return min(w, key=lambda t: (t[0] + 3 * t[1], t[1]))


# ------------------------------------------------------------------ selfcheck


def selfcheck():
    import random
    rng = random.Random(20260728)

    # (0) mono4_witnesses agrees with the trusted checkers
    for _ in range(400):
        n = rng.randint(4, 9)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        assert (len(mono4_witnesses(p)) > 0) == has_monotone_kap_brute(p, 4) == \
            has_monotone_kap_pos(p, 4)
    for _ in range(400):
        n = rng.randint(4, 10)
        vals = rng.sample(range(1, 45), n)
        assert (len(mono4_witnesses(vals)) > 0) == has_monotone_kap_brute(vals, 4)
    for _ in range(150):
        n = rng.randint(20, 60)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        assert (len(mono4_witnesses(p)) > 0) == has_monotone_kap_pos(p, 4)

    # (1) Lemma T: context-free tau, all 6 constant priorities, kills 4-APs on [1..M]
    for p in permutations((0, 1, 2)):
        t = Tau(prio_const(p))
        seq = t.sort(range(1, 1500))
        assert not mono4_witnesses(seq), p
        assert not has_monotone_kap_general(seq[:400], 4)

    # (2) Lemma T with per-level priorities and with context-dependent priorities
    PERMS = list(permutations((0, 1, 2)))
    t = Tau(prio_levels([PERMS[rng.randrange(6)] for _ in range(9)]))
    assert not mono4_witnesses(t.sort(range(1, 2000)))
    tbl = {}

    def prio_rand(l, c):
        if (l, c) not in tbl:
            tbl[(l, c)] = PERMS[rng.randrange(6)]
        return tbl[(l, c)]
    t2 = Tau(prio_rand)
    assert not mono4_witnesses(t2.sort(range(1, 2000)))

    # (3) Lemma T on arbitrary SUBSETS (both comparators), via general checker
    for _ in range(200):
        S = rng.sample(range(1, 3000), rng.randint(30, 70))
        for tt in (t, t2, Tau(prio_const((2, 0, 1)))):
            assert not has_monotone_kap_general(tt.sort(S), 4)

    # (4) tau DOES contain monotone 3-APs (it must, DEGS77(a))
    seq = Tau().sort(range(1, 400))
    assert has_monotone_kap_general(seq, 3)

    # (5) before() consistent with key()
    for _ in range(3000):
        u = rng.randint(1, 10 ** 5)
        w = rng.randint(1, 10 ** 5)
        if u == w:
            continue
        for tt in (t, t2, Tau(prio_const((1, 2, 0)))):
            assert tt.before(u, w) == (tt.key(u) < tt.key(w)), (u, w)

    print("taulib selfcheck OK  "
          "[scanner vs apcheck brute+pos on 950 cases; Lemma T for 6 constant, "
          "per-level and context-dependent priorities on [1..2000] and 200 random "
          "subsets; 3-APs present; before()==key()]")


if __name__ == "__main__":
    selfcheck()
