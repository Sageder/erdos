"""mod1d_mus.py — clean deletion-based MUS for the (c'=4, c=16, C=64) block
obstruction, plus a quick completion of the grid at larger c'.
The MUS is then re-verified: (i) still UNSAT; (ii) every proper subset SAT.
"""

import sys
import time

from pysat.formula import CNF
from pysat.solvers import Cadical195

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from mod1b_sweep_mus import build, solve_with  # noqa: E402


def mus_deletion(hard, pats, nv):
    top = nv
    sel = []
    cnf = CNF(from_clauses=list(hard.clauses))
    for (kind, t, clause) in pats:
        top += 1
        sel.append(top)
        cnf.append(clause + [-top])
    s = Cadical195(bootstrap_with=cnf)
    assert not s.solve(assumptions=sel)
    core = set(s.get_core())
    S = [i for i in range(len(pats)) if sel[i] in core]
    i = 0
    while i < len(S):
        cand = S[:i] + S[i + 1:]
        if s.solve(assumptions=[sel[j] for j in cand]):
            i += 1                       # necessary, keep
        else:
            S = cand                     # redundant, drop (i stays)
    # final verification of minimality and unsatisfiability
    assert not s.solve(assumptions=[sel[j] for j in S])
    for i in range(len(S)):
        assert s.solve(assumptions=[sel[j] for j in S[:i] + S[i + 1:]])
    s.delete()
    return [pats[j] for j in S]


if __name__ == "__main__":
    out = []

    def log(x):
        print(x, flush=True)
        out.append(x)

    log("=== finishing grid: larger c' (small sizes only) ===")
    for cp, c, C in [(7, 28, 112), (8, 32, 128), (10, 40, 160),
                     (12, 48, 192), (16, 64, 256)]:
        hard, pats, nv = build(c, C, use_a2h_cp=cp)
        t0 = time.time()
        sat = solve_with(hard, pats, nv)
        log("  c'=%3d c=%3d C=%4d : %s (%.1fs)"
            % (cp, c, C, "SAT" if sat else "UNSAT", time.time() - t0))

    log("")
    log("=== MUS for (c'=4, c=16, C=64) ===")
    hard, pats, nv = build(16, 64, use_a2h_cp=4)
    t0 = time.time()
    core = mus_deletion(hard, pats, nv)
    log("minimal unsatisfiable subset, %d pattern constraints (%.1fs); "
        "verified minimal (every proper subset satisfiable):"
        % (len(core), time.time() - t0))
    for kind, t, _ in sorted(core, key=lambda p: (p[0], p[1])):
        log("   %-4s %s" % (kind, t))

    with open("/home/user/erdos/attempts/route-R2/mod1d_output.txt", "w") as f:
        f.write("\n".join(out) + "\n")
