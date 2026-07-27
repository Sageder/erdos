"""localsat.py — Route R1: block-LOCAL sufficient conditions, decoupled via SAT.

For blocks-in-increasing-position-order with ratio r >= 3 geometric blocks
B_j = [s, rs), s = r^{j-1}, the global no-monotone-4-AP requirement decomposes into
cases A, B1, B1', B2, B3, B4 (pattern-completeness machine-checked in patterns.py).
Pushing every B2 obligation onto the LOWER block yields a per-block condition set
L(s, r) whose simultaneous satisfiability for all j is SUFFICIENT for the whole
construction:

 (L1) no monotone 4-AP inside the block;
 (L2) no increasing 3-AP (w, w+e, w+2e) inside with  1 <= w-e <= s-1  or  w+3e >= rs;
 (L3) every pair a < b in the block with 2b - a >= rs has b BEFORE a
      [kills B2 from below, and B3 = D3 is a sub-family];
 (L4) every pair (v, v+d) with v-d in [s/r, s-1] and v-2d in [1, s/r - 1] has
      v+d BEFORE v   [kills B4; empty for s = r (block 2)].

Claim tested: is L(r^{j-1}, r) satisfiable, for various r and j?  Exact SAT with full
transitivity encoding; witnesses re-verified independently.
"""

import sys
from itertools import combinations
sys.path.insert(0, "/home/user/erdos/attempts/route-R1")
from pysat.solvers import Cadical153


def local_constraints(s, r):
    """Returns (values, forced_inversions, forbidden_incr_3aps, block4aps).
    forced_inversions: set of (a,b) a<b meaning b must precede a.
    forbidden_incr_3aps: list of (w, w+e, w+2e) that must not appear in increasing
    position order. block4aps: list of quadruples (both orientations forbidden)."""
    lo, hi = s, r * s
    vals = list(range(lo, hi))
    inv = set()
    for a in range(lo, hi):
        for b in range(a + 1, hi):
            if 2 * b - a >= hi:
                inv.add((a, b))                              # L3
    if s > r or s == r:                                      # L4 needs previous block start s/r >= 1
        prev_lo = s // r
        if prev_lo >= 1 and s % r == 0:
            for v in range(lo, hi):
                for d in range(1, hi - v):
                    if prev_lo <= v - d <= s - 1 and 1 <= v - 2 * d <= prev_lo - 1:
                        inv.add((v, v + d))                  # L4 (v < v+d)
    bad3 = []
    for e in range(1, (hi - lo) // 2 + 1):
        for w in range(lo, hi - 2 * e):
            if (1 <= w - e <= s - 1) or (w + 3 * e >= hi):
                bad3.append((w, w + e, w + 2 * e))           # L2
    quads = []
    for e in range(1, (hi - lo - 1) // 3 + 1):
        for w in range(lo, hi - 3 * e):
            quads.append((w, w + e, w + 2 * e, w + 3 * e))   # L1
    return vals, inv, bad3, quads


def solve_local(s, r, verbose=True, extra_inv=(), forbid_decr3_with_room=False):
    vals, inv, bad3, quads = local_constraints(s, r)
    inv = set(inv) | set(extra_inv)
    lo, hi = s, r * s
    n = hi - lo
    vid = {}
    nxt = 1
    for a, b in combinations(vals, 2):
        vid[(a, b)] = nxt
        nxt += 1

    def lit(a, b):  # pos(a) < pos(b)
        return vid[(a, b)] if a < b else -vid[(b, a)]

    cls = []
    for (a, b) in inv:
        cls.append([-lit(a, b)])                             # b before a
    for (w, x, y) in bad3:
        cls.append([-lit(w, x), -lit(x, y)])
    for (w, x, y, z) in quads:
        cls.append([-lit(w, x), -lit(x, y), -lit(y, z)])
        cls.append([-lit(z, y), -lit(y, x), -lit(x, w)])
    if forbid_decr3_with_room:
        for e in range(1, n // 2 + 1):
            for w in range(lo, hi - 2 * e):
                if w - e >= 1 or w + 3 * e < r * hi:
                    cls.append([-lit(w + 2 * e, w + e), -lit(w + e, w)])
    for a in vals:
        for b in vals:
            for c in vals:
                if a != b and b != c and a != c:
                    cls.append([-lit(a, b), -lit(b, c), lit(a, c)])
    sol = Cadical153(bootstrap_with=cls)
    ok = sol.solve()
    if not ok:
        if verbose:
            print(f"  L(s={s}, r={r})  [block [{lo},{hi}), n={n}]  UNSAT")
        return None
    model = sol.get_model()
    val = {abs(l): (l > 0) for l in model}
    import functools
    def cmp(a, b):
        if a == b:
            return 0
        t = lit(a, b)
        before = val[t] if t > 0 else (not val[-t])
        return -1 if before else 1
    order = sorted(vals, key=functools.cmp_to_key(cmp))
    verify_local(order, s, r, inv, bad3, quads)
    if verbose:
        print(f"  L(s={s}, r={r})  [block [{lo},{hi}), n={n}]  SAT; witness verified")
    return order


def verify_local(order, s, r, inv, bad3, quads):
    pos = {v: i for i, v in enumerate(order)}
    assert sorted(order) == list(range(s, r * s))
    for (a, b) in inv:
        assert pos[b] < pos[a], ("inversion violated", a, b)
    for (w, x, y) in bad3:
        assert not (pos[w] < pos[x] < pos[y]), ("bad3 violated", w, x, y)
    for (w, x, y, z) in quads:
        ps = (pos[w], pos[x], pos[y], pos[z])
        assert not (ps[0] < ps[1] < ps[2] < ps[3]), ("incr 4-AP", w, x, y, z)
        assert not (ps[0] > ps[1] > ps[2] > ps[3]), ("decr 4-AP", w, x, y, z)


if __name__ == "__main__":
    import time
    for r in (3, 4, 5, 6):
        print(f"=== ratio r={r}")
        for j in range(1, 7):
            s = r ** (j - 1)
            n = (r - 1) * s
            if n > 400:
                print(f"  L(s={s}, r={r}) skipped (n={n} too big for full transitivity here)")
                continue
            t0 = time.time()
            w = solve_local(s, r, verbose=False)
            dt = time.time() - t0
            if w is None:
                print(f"  block j={j} [s={s}]: UNSAT   ({dt:.1f}s)")
            else:
                print(f"  block j={j} [s={s}]: SAT     ({dt:.1f}s)  order={w if n <= 24 else '(len %d)' % n}")
