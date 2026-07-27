"""mod1b_sweep_mus.py — robustness sweep + minimal unsatisfiable core for the
Mod-1 obstruction.

Part 1 (sweep): for general block [c, C) inside ANY block-major interval
scheme, the following constraints are SOUND (each violation produces a real
monotone 4-AP, using only: values < c sit at earlier positions, values >= C at
later positions):
    A4, D4, A3T (tail w+3e >= C), A3H (head 1 <= w-e < c),
    A2T (head 1 <= u-e < c and tail u+2e >= C).
(A2H/A2HH additionally use the position of the previous boundary; dropping
them only RELAXES the system, so UNSAT still refutes.)  We solve this sound
subsystem for a grid of (c, C) to map where the scheme dies.

Part 2 (MUS): deletion-based minimal unsatisfiable subset of the pattern
constraints for the smallest UNSAT block, over always-kept transitivity
clauses, giving a human-checkable certificate.
"""

import sys
import time

from pysat.formula import CNF
from pysat.solvers import Cadical195

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")


def build(c, C, use_a2h_cp=None):
    """CNF for block [c, C); returns (hard transitivity CNF, pattern list).
    pattern list entries: (kind, tuple-of-values, clause)."""
    vals = list(range(c, C))
    idx = {}
    nv = 0
    for i, a in enumerate(vals):
        for b in vals[i + 1:]:
            nv += 1
            idx[(a, b)] = nv

    def X(a, b):
        return idx[(a, b)] if a < b else -idx[(b, a)]

    hard = CNF()
    n = len(vals)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, d = vals[i], vals[j], vals[k]
                hard.append([-X(a, b), -X(b, d), X(a, d)])
                hard.append([X(a, b), X(b, d), -X(a, d)])

    pats = []
    for w in vals:
        e = 1
        while w + 3 * e < C:
            t = (w, w + e, w + 2 * e, w + 3 * e)
            pats.append(("A4", t, [-X(t[0], t[1]), -X(t[1], t[2]),
                                   -X(t[2], t[3])]))
            pats.append(("D4", t, [X(t[0], t[1]), X(t[1], t[2]),
                                   X(t[2], t[3])]))
            e += 1
        e = 1
        while w + 2 * e < C:
            if w + 3 * e >= C:
                pats.append(("A3T", (w, w + e, w + 2 * e),
                             [-X(w, w + e), -X(w + e, w + 2 * e)]))
            if 1 <= w - e < c:
                pats.append(("A3H", (w, w + e, w + 2 * e),
                             [-X(w, w + e), -X(w + e, w + 2 * e)]))
            e += 1
        e = 1
        while w + e < C:
            if 1 <= w - e < c and w + 3 * e >= C:
                pats.append(("A2T", (w, w + e), [-X(w, w + e)]))
            if use_a2h_cp is not None:
                cp = use_a2h_cp
                if cp <= w - e < c and 1 <= w - 2 * e < cp:
                    pats.append(("A2H", (w, w + e), [-X(w, w + e)]))
            e += 1
    return hard, pats, nv


def solve_with(hard, pats, nv):
    cnf = CNF(from_clauses=hard.clauses + [p[2] for p in pats])
    with Cadical195(bootstrap_with=cnf) as s:
        return s.solve()


def mus(hard, pats, nv):
    """Deletion-based MUS over pattern constraints (transitivity always kept),
    using one selector literal per pattern and solving under assumptions."""
    top = nv
    sel = []
    cnf = CNF(from_clauses=list(hard.clauses))
    for i, (kind, t, clause) in enumerate(pats):
        top += 1
        sel.append(top)
        cnf.append(clause + [-top])          # selector => clause
    with Cadical195(bootstrap_with=cnf) as s:
        assert not s.solve(assumptions=sel), "not UNSAT with all patterns?!"
        core = set(s.get_core())
        keep = [i for i in range(len(pats)) if sel[i] in core]
        # deletion loop on the core
        i = 0
        while i < len(keep):
            trial = keep[:i] + keep[i + 1:]
            if s.solve(assumptions=[sel[j] for j in trial]):
                i += 1                        # needed
            else:
                new_core = set(s.get_core())
                keep = [j for j in trial if sel[j] in new_core]
                i = 0 if len(keep) < len(trial) else i
                keep = trial if len(keep) == 0 else keep
        return [pats[j] for j in keep]


if __name__ == "__main__":
    out = []

    def log(s):
        print(s, flush=True)
        out.append(s)

    log("=== Part 1: sweep of the SOUND chain-independent system on [c, C) ===")
    log("(UNSAT means: in ANY block-major interval scheme having [c,C) as a")
    log(" block, every internal order of it forces a monotone 4-AP)")
    for c in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 24, 32, 48, 64]:
        for r in [4, 5, 6]:
            C = r * c
            if C - c > 340:
                continue
            hard, pats, nv = build(c, C)
            t0 = time.time()
            sat = solve_with(hard, pats, nv)
            log("  [c=%3d, C=%3d) size %3d ratio %d: %s (%.1fs)"
                % (c, C, C - c, r, "SAT" if sat else "UNSAT",
                   time.time() - t0))

    log("")
    log("=== Part 2: minimal unsatisfiable core for [16,64), chain 4^m ===")
    hard, pats, nv = build(16, 64, use_a2h_cp=4)
    m = mus(hard, pats, nv)
    log("MUS size: %d pattern constraints" % len(m))
    for kind, t, _ in sorted(m):
        log("   %-4s %s" % (kind, t))

    log("")
    log("=== Part 2b: MUS for smallest chain-independent UNSAT block ===")
    # find smallest c with UNSAT at ratio 4 without A2H, then extract MUS
    for c in range(4, 65):
        hard, pats, nv = build(c, 4 * c)
        if not solve_with(hard, pats, nv):
            log("smallest chain-independent UNSAT: [c=%d, C=%d)" % (c, 4 * c))
            m = mus(hard, pats, nv)
            log("MUS size: %d pattern constraints" % len(m))
            for kind, t, _ in sorted(m):
                log("   %-4s %s" % (kind, t))
            break

    with open("/home/user/erdos/attempts/route-R2/mod1b_output.txt", "w") as f:
        f.write("\n".join(out) + "\n")
