"""escape_check.py -- concrete demonstration of Proposition W-B.

Route R5's Generic Escape reply (REPORT.md sec.4) answers a supply probe at anchor u
with a step e > 2*(max X - min X) and appends, at the far position end,
n0 = u-e, n1 = u+e, n3 = u+3e, n2 = u+2e.  The resulting object is an ACTUAL finite
monotone-4-AP-free linear order on the named value set.

Consequence (Proposition W-B): every rule that is valid on all finite 4-AP-free orders
-- which is exactly what W1..W7 are, and what all of the commissioned candidate classes
(a) record-record, (b) record-grounded, (c) consecutive records, (e) staircase rungs
are -- is automatically satisfied by that witness, so adding it to the store cannot
make the position inconsistent.  This script exhibits the witness and checks it.

Λ / Γ here are computed RELATIVE TO THE NAMED SET (that is the strongest form in which
a finite store can assert record/grounded-hood).
"""
import sys, random
sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_general


def spines(seq):
    """records and grounded values of a finite sequence of distinct integers."""
    pos = {v: i for i, v in enumerate(seq)}
    rec, mx = set(), -10**9
    for v in seq:
        if v > mx:
            rec.add(v)
            mx = v
    gnd, mp = set(), -1
    for v in sorted(pos):
        if pos[v] > mp:
            gnd.add(v)
            mp = pos[v]
    return pos, rec, gnd


def wrules_hold(seq):
    """check every W-rule on the finite order `seq` (values need only be present)."""
    pos, L, G = spines(seq)
    S = set(seq)

    def P(v):
        return pos[v]
    for w in L:
        for g in G:
            if g <= w:
                continue
            D = g - w
            if D % 3 == 0:
                s = D // 3
                if w + s in S and w + 2 * s in S and not P(w + 2 * s) < P(w + s):
                    return "W1", (w, g)
            if D % 2 == 0:
                s = D // 2
                if w + s in S and not (P(w) < P(w + s) < P(g)):
                    return "W2", (w, g)
                if g + s in S and w + s in S and not P(g + s) < P(g):
                    return "W2a", (w, g)
                if w - s in S and w + s in S and not P(w) < P(w - s):
                    return "W2b", (w, g)
    for g in G:
        for g2 in G:
            if g2 <= g:
                continue
            D = g2 - g
            if D % 2 == 0 and g - D // 2 in S and g + D // 2 in S:
                if not P(g + D // 2) < P(g):
                    return "W3", (g, g2)
            if g2 < 2 * g and 2 * g - g2 in S and 2 * g2 - g in S:
                if not P(2 * g2 - g) < P(g2):
                    return "W5", (g, g2)
    for w in L:
        for w2 in L:
            if w2 <= w:
                continue
            D = w2 - w
            if D % 2 == 0 and w + D // 2 in S and w2 + D // 2 in S:
                if not P(w2) < P(w + D // 2):
                    return "W4", (w, w2)
            if 2 * w2 - w in S and 3 * w2 - 2 * w in S:
                if not P(3 * w2 - 2 * w) < P(2 * w2 - w):
                    return "W6", (w, w2)
            if 2 * w - w2 in S and 2 * w2 - w in S:
                if not P(w) < P(2 * w - w2):
                    return "W6b", (w, w2)
    for g in G:
        for w in L:
            if g < w < 2 * g and 2 * g - w in S and 2 * w - g in S:
                if not P(w) < P(g):
                    return "W7", (g, w)
    return None


if __name__ == '__main__':
    rng = random.Random(196)
    bad = 0
    trials = 0
    for t in range(4000):
        # a small consistent store: a random 4-AP-free order on a random value set
        vals = rng.sample(range(1, 26), rng.randint(3, 6))
        rng.shuffle(vals)
        if has_monotone_kap_general(vals, 4):
            continue
        X = list(vals)
        D = max(X) - min(X)
        u = rng.choice(X)
        g = rng.randint(1, 3)
        e = g * (2 * D + rng.randint(1, 5))          # e > 2D, as in Generic Escape
        n0, n1, n2, n3 = u - e, u + e, u + 2 * e, u + 3 * e
        new = ([n0] if n0 >= 1 else []) + [n1, n3, n2]
        seq = X + new
        if len(set(seq)) != len(seq):
            continue
        trials += 1
        assert not has_monotone_kap_general(seq, 4), ("escape gadget has a 4-AP!", seq)
        r = wrules_hold(seq)
        if r:
            bad += 1
            print("W-rule violated by the escape witness:", r, seq)
    print(f"{trials} Generic-Escape replies built; all are monotone-4-AP-free; "
          f"W-rule violations: {bad}")
