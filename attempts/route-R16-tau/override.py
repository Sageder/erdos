"""override.py — the OVERRIDE CALCULUS for tau-repairs, and a battery of explicit
override schedules generated to 10^4-10^5 and checked for monotone 4-APs.

THE CALCULUS (proved in REPORT.md sec. 5; verified here).
Let tau be a base-3 priority comparator and let `<` be ANY linear order on N.  For a
pair {u,w} say the pair is OVERRIDDEN if `<` disagrees with tau on it.  Fix a 4-AP
A = (x, x+d, x+2d, x+3d), let v = v3(d), and let P1,P2,P3 be its three adjacent pairs.
All three are decided by tau at level v (the four terms agree below level v), and the
level-v digits run a,a+delta,a+2delta,a.  Hence the tau-sign word s = (s1,s2,s3) always
contains a '+' and a '-'; write S+ = {k : s_k=+}, S- = {k : s_k=-}.  Then

    A is an INCREASING monotone 4-AP of `<`   <=>   O ∩ {P1,P2,P3} = S-
    A is a DECREASING monotone 4-AP of `<`    <=>   O ∩ {P1,P2,P3} = S+

so in particular: **if 0 or 3 of the AP's adjacent pairs are overridden, A is safe.**
Exactly one of |S+|,|S-| equals 1 (delta = delta* gives |S-|=1, delta = 2delta* gives
|S+|=1), so every 4-AP has a unique "minority slot".

Consequence (design rule): damage is confined to APs on which the override schedule is
*inhomogeneous* -- it overrides some but not all of the three adjacent pairs.
"""

import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from taulib import Tau, prio_const, prio_levels, v3, dig3, mono4_witnesses, first_mono4


# ---------------------------------------------------------------- generic order object

class KeyOrder:
    """A linear order on N given by an injective key function."""

    def __init__(self, key, name):
        self.key = key
        self.name = name

    def perm(self, M):
        return sorted(range(1, M + 1), key=self.key)

    def before(self, u, w):
        return self.key(u) < self.key(w)


def graded_tau(g, t, name):
    """lex(g, tau-key, n) — order type omega whenever {n : g(n) <= K} is finite."""
    return KeyOrder(lambda n: (g(n),) + t.key(n) + (n,), name)


# ---------------------------------------------------------------- calculus verification

def override_set(order, t, x, d):
    """Which of the 3 adjacent pairs of the AP (x,d) are overridden (1-indexed)."""
    T = [x + k * d for k in range(4)]
    o = set()
    for k in (1, 2, 3):
        u, w = T[k - 1], T[k]
        if order.before(u, w) != t.before(u, w):
            o.add(k)
    return o


def tau_signs(t, x, d):
    T = [x + k * d for k in range(4)]
    return tuple(1 if t.before(T[k - 1], T[k]) else -1 for k in (1, 2, 3))


def verify_calculus(order, t, M):
    """Check the calculus against the direct positional test, for all APs in [1..M]."""
    perm = order.perm(M)
    pos = {v: i for i, v in enumerate(perm)}
    bad = 0
    for d in range(1, (M - 1) // 3 + 1):
        for x in range(1, M - 3 * d + 1):
            T = [x + k * d for k in range(4)]
            p = [pos[v] for v in T]
            inc = p[0] < p[1] < p[2] < p[3]
            dec = p[0] > p[1] > p[2] > p[3]
            s = tau_signs(t, x, d)
            O = override_set(order, t, x, d)
            Sm = {k for k in (1, 2, 3) if s[k - 1] == -1}
            Sp = {k for k in (1, 2, 3) if s[k - 1] == 1}
            assert len(Sm) in (1, 2) and len(Sp) in (1, 2), (x, d, s)
            if inc != (O == Sm) or dec != (O == Sp):
                bad += 1
                if bad < 4:
                    print("   CALCULUS MISMATCH", x, d, s, O, inc, dec)
    return bad


# ---------------------------------------------------------------- candidate schedules

def cuts_grading(cuts):
    """g(n) = index j with cuts[j] <= n < cuts[j+1]; cuts strictly increasing, cuts[0]=1,
    extended geometrically by the last ratio."""
    cs = list(cuts)

    def g(n):
        c = cs
        while c[-1] <= n:
            r = max(2, c[-1] // c[-2])
            c.append(c[-1] * r)
        lo, hi = 0, len(c) - 1
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if c[mid] <= n:
                lo = mid
            else:
                hi = mid
        return lo
    return g


def digitcount_grading(target=2, weights=None):
    """g(n) = sum over levels of w_l * [dig_l(n) == target]  (+ a tiebreak on size)."""
    def g(n):
        s, l = 0, 0
        m = n
        while m:
            if m % 3 == target:
                s += (weights[l] if weights else 1)
            m //= 3
            l += 1
        return s
    return g


def taurank_grading(base=3):
    """g(n) = number of base-3 digits of n (= the geometric block index)."""
    def g(n):
        l = 0
        while base ** (l + 1) <= n:
            l += 1
        return l
    return g


if __name__ == "__main__":
    tnat = Tau(prio_const((0, 1, 2)))
    trev = Tau(prio_const((2, 1, 0)))
    talt = Tau(prio_levels([(0, 1, 2), (2, 1, 0)]))

    print("=== 1. override calculus verified against direct positional test ===")
    tests = [
        (graded_tau(taurank_grading(), tnat, "blocks 3^k + tau"), tnat),
        (graded_tau(cuts_grading([1, 2, 4, 10, 90]), tnat, "cuts[1,2,4,10,90] + tau"), tnat),
        (graded_tau(digitcount_grading(2), trev, "count(digit=2) + tau_rev"), trev),
        (KeyOrder(lambda n: n, "value order"), tnat),
        (KeyOrder(lambda n: (-n,), "reverse value order"), trev),
    ]
    for o, t in tests:
        b = verify_calculus(o, t, 120)
        print(f"   {o.name:<34} mismatches={b}")

    print()
    print("=== 2. explicit override schedules, checked on [1..M] ===")
    M = 10000
    cands = []
    cands.append(graded_tau(taurank_grading(), tnat, "B: blocks [3^k,3^{k+1}) + tau"))
    cands.append(graded_tau(taurank_grading(), trev, "B: blocks + tau_rev"))
    cands.append(graded_tau(taurank_grading(), talt, "B: blocks + tau_alt"))
    for cs in ([1, 2, 4, 10, 90], [1, 2, 4, 10, 91], [1, 2, 4, 10, 92],
               [1, 2, 5, 14, 60], [1, 3, 9, 30, 200]):
        cands.append(graded_tau(cuts_grading(cs), tnat, f"C: cuts{cs} + tau"))
        cands.append(graded_tau(cuts_grading(cs), trev, f"C: cuts{cs} + tau_rev"))
    for tgt in (0, 1, 2):
        cands.append(graded_tau(digitcount_grading(tgt), tnat, f"D: #dig=={tgt} + tau"))
        cands.append(graded_tau(digitcount_grading(tgt), trev, f"D: #dig=={tgt} + tau_rev"))
    # weighted digit counts (superlinear displacement)
    for w in ([2 ** l for l in range(30)], [l + 1 for l in range(30)],
              [3 ** l for l in range(30)]):
        cands.append(graded_tau(digitcount_grading(2, w), tnat,
                                f"D: weighted #dig==2 w={w[:4]}.. + tau"))
    # triadic reversed blocks (Thm 14) with tau inside instead of decreasing
    cands.append(KeyOrder(lambda n: (taurank_grading()(n), -n), "T: blocks + decreasing (Thm14)"))
    cands.append(KeyOrder(lambda n: (taurank_grading()(n),) + tuple(-a for a in tnat.key(n)),
                          "T: blocks + reverse-tau"))

    for o in cands:
        p = o.perm(1200)
        w = first_mono4(p)
        if w is None:
            p = o.perm(M)
            w = first_mono4(p)
            tag = f"CLEAN to {M}" if w is None else f"dies at max-term {w[0]+3*w[1]}"
        else:
            tag = f"dies at max-term {w[0]+3*w[1]}"
        extra = "" if w is None else f"  witness x={w[0]} d={w[1]} {'inc' if w[2]==1 else 'dec'}"
        print(f"   {o.name:<44} {tag}{extra}")
