"""mod1c_grid.py — decisive grid for Mod 1: block [c, C) with previous
boundary c' (previous block = [c', c)), inside any ratio->=4 block-major
interval chain  1 = b_0 < b_1 < ... (b_{j+1} >= 4 b_j), with (c', c, C)
consecutive boundaries.  Constraint system (all SOUND for such a chain):
  A4, D4, A3T, A3H, A2T  (chain-independent)  +  A2H(c')
UNSAT for a triple => NO internal order of [c,C) avoids monotone 4-APs in any
such chain, regardless of every other block's order.  (A2HH would only add
constraints, so UNSAT here is final for that triple.)

Then: MUS certificate for the canonical triple (4, 16, 64).
"""

import sys
import time

from pysat.formula import CNF
from pysat.solvers import Cadical195

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from mod1b_sweep_mus import build, solve_with, mus  # noqa: E402


if __name__ == "__main__":
    out = []

    def log(s):
        print(s, flush=True)
        out.append(s)

    log("=== grid: block [c,C) with previous boundary c' (A2H active) ===")
    results = {}
    for cp in [4, 5, 6, 7, 8, 10, 12, 16]:
        for rc in [4, 5, 6, 8]:
            c = cp * rc
            for rC in [4, 5, 6]:
                C = c * rC
                if C - c > 260:
                    continue
                hard, pats, nv = build(c, C, use_a2h_cp=cp)
                na2h = sum(1 for k, _, _ in pats if k == "A2H")
                t0 = time.time()
                sat = solve_with(hard, pats, nv)
                results[(cp, c, C)] = sat
                log("  c'=%3d c=%3d C=%4d size %3d  A2H=%3d : %s (%.1fs)"
                    % (cp, c, C, C - c, na2h,
                       "SAT" if sat else "UNSAT", time.time() - t0))

    n_unsat = sum(1 for v in results.values() if not v)
    log("")
    log("summary: %d/%d triples UNSAT" % (n_unsat, len(results)))

    log("")
    log("=== MUS certificate for (c'=4, c=16, C=64) ===")
    hard, pats, nv = build(16, 64, use_a2h_cp=4)
    t0 = time.time()
    core = mus(hard, pats, nv)
    log("MUS size %d (%.1fs):" % (len(core), time.time() - t0))
    for kind, t, _ in sorted(core, key=lambda p: (p[0], p[1])):
        log("   %-4s %s" % (kind, t))

    with open("/home/user/erdos/attempts/route-R2/mod1c_output.txt", "w") as f:
        f.write("\n".join(out) + "\n")
