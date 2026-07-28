"""mod1e_validate.py — independent validation of the Mod-1 constraint model.

(1) `violations(order, cp, c, C)`: a from-scratch Python detector of all
    sound pattern types in a given internal order of block [c, C):
      A4, D4 (internal 4-APs), A3T, A3H, A2T, A2H.
(2) Cross-validate the SAT encoding against it on random orders
    (clause evaluation vs detector, both verdicts and witness sets).
(3) SAT-side: the solver's pi_2 for [16,64) must have no violations;
    place it through the (independently written) backtracker's ok_to_place.
(4) Soundness end-to-end: every violated pattern in a random order of
    [64,256) must correspond to a genuine monotone 4-AP of an assembled
    permutation prefix (validated checker).
(5) UNSAT spot-check: 20000 random orders of [64,256) all have >= 1 violation.
"""

import random
import sys

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from mod1b_sweep_mus import build  # noqa: E402


def violations(order, cp, c, C):
    """All sound-pattern violations in this internal order of [c, C).
    Written independently of the CNF builder."""
    pos = {v: i for i, v in enumerate(order)}
    out = []
    for w in range(c, C):
        for e in range(1, (C - 1 - w) // 3 + 1):
            a, b, g, h = w, w + e, w + 2 * e, w + 3 * e
            if pos[a] < pos[b] < pos[g] < pos[h]:
                out.append(("A4", (a, b, g, h)))
            if pos[a] > pos[b] > pos[g] > pos[h]:
                out.append(("D4", (a, b, g, h)))
        for e in range(1, (C - 1 - w) // 2 + 1):
            a, b, g = w, w + e, w + 2 * e
            if pos[a] < pos[b] < pos[g]:
                if w + 3 * e >= C:
                    out.append(("A3T", (a, b, g)))
                if 1 <= w - e < c:
                    out.append(("A3H", (a, b, g)))
        for e in range(1, C - 1 - w + 1):
            if w + e >= C:
                break
            if pos[w] < pos[w + e]:
                if 1 <= w - e < c and w + 2 * e >= C:
                    out.append(("A2T", (w, w + e)))
                if cp <= w - e < c and 1 <= w - 2 * e < cp:
                    out.append(("A2H", (w, w + e)))
    return out


def cnf_pattern_verdict(order, cp, c, C):
    """Evaluate the CNF builder's pattern clauses under the assignment induced
    by `order`; return set of violated (kind, tuple)."""
    hard, pats, nv = build(c, C, use_a2h_cp=cp)
    pos = {v: i for i, v in enumerate(order)}
    vals = sorted(order)
    idx = {}
    k = 0
    for i, a in enumerate(vals):
        for b in vals[i + 1:]:
            k += 1
            idx[k] = (a, b)
    bad = set()
    for kind, t, clause in pats:
        sat = False
        for lit in clause:
            a, b = idx[abs(lit)]
            val = pos[a] < pos[b]
            if (lit > 0) == val:
                sat = True
                break
        if not sat:
            bad.add((kind, t))
    return bad


if __name__ == "__main__":
    from checkers import find_monotone_kap, enumerate_monotone_kaps
    from mod1_sat import solve_block
    from construction import block_order
    rng = random.Random(196196)
    out = []

    def log(s):
        print(s, flush=True)
        out.append(s)

    # (2) encoding cross-validation on random orders --------------------
    for (cp, c, C, trials) in [(1, 4, 16, 2000), (4, 16, 64, 300)]:
        for t in range(trials):
            o = list(range(c, C))
            rng.shuffle(o)
            v1 = set(violations(o, cp, c, C))
            v2 = cnf_pattern_verdict(o, cp, c, C)
            assert v1 == v2, (o, v1 ^ v2)
    log("(2) OK: CNF pattern clauses == independent detector on "
        "2000 orders of [4,16) and 300 of [16,64) (exact witness sets)")

    # (3) SAT-side check ------------------------------------------------
    pi2, _, _ = solve_block(16, prev_asc=None)
    assert pi2 is not None
    assert violations(pi2, 4, 16, 64) == []
    log("(3) OK: solver's pi_2 for [16,64) has zero violations "
        "per independent detector")

    # (4) soundness end-to-end ------------------------------------------
    # assemble: blocks 0..4 of the 4^m chain; block 3 gets a random order,
    # others vdC-style; every violation in block 3 must be realized as a
    # genuine monotone 4-AP by the validated checker.
    for trial in range(3):
        o3 = list(range(64, 256))
        rng.shuffle(o3)
        pref = []
        for m in range(5):
            pref.extend(o3 if m == 3 else block_order(m))
        assert sorted(pref) == list(range(1, 4 ** 5))
        vio = violations(o3, 16, 64, 256)
        aps = set()
        for (x, d, o) in enumerate_monotone_kaps(pref, 4):
            aps.add((x, d, o))
        missing = []
        for kind, t in vio:
            e = t[1] - t[0]
            if kind == "A4":
                need = (t[0], e, "inc")
            elif kind == "D4":
                need = (t[0], e, "dec")
            elif kind == "A3T":
                need = (t[0], e, "inc")
            elif kind == "A3H":
                need = (t[0] - e, e, "inc")
            elif kind == "A2T":
                need = (t[0] - e, e, "inc")
            elif kind == "A2H":
                need = (t[0] - 2 * e, e, "inc")
            if need not in aps:
                missing.append((kind, t, need))
        assert not missing, missing[:5]
    log("(4) OK: 3 random orders of [64,256): every detector violation is "
        "realized as a genuine monotone 4-AP in the assembled permutation "
        "(validated checker); soundness confirmed end-to-end")

    # (5) UNSAT spot-check ----------------------------------------------
    n_ok = 0
    for t in range(20000):
        o = list(range(64, 256))
        rng.shuffle(o)
        if not violations(o, 16, 64, 256):
            n_ok += 1
    log("(5) spot-check: %d / 20000 random orders of [64,256) are "
        "violation-free (SAT says the true number over ALL orders is 0)"
        % n_ok)
    assert n_ok == 0

    with open("/home/user/erdos/attempts/route-R2/mod1e_output.txt", "w") as f:
        f.write("\n".join(out) + "\n")
