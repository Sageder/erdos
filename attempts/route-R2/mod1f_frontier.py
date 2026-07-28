"""mod1f_frontier.py — fixed-encoding frontier scan for the Mod-1 obstruction.
Incremental logging to mod1f_output.txt; per-solve conflict budget.
"""

import sys
import time

from pysat.formula import CNF
from pysat.solvers import Cadical195

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from mod1b_sweep_mus import build  # noqa: E402
from mod1d_mus import mus_deletion  # noqa: E402

LOG = "/home/user/erdos/attempts/route-R2/mod1f_output.txt"
open(LOG, "w").close()


def log(s):
    print(s, flush=True)
    with open(LOG, "a") as f:
        f.write(s + "\n")


def test(cp, c, C, with_a2h=True, budget=5 * 10 ** 6):
    hard, pats, nv = build(c, C, use_a2h_cp=cp if with_a2h else None)
    cnf = CNF(from_clauses=hard.clauses + [p[2] for p in pats])
    with Cadical195(bootstrap_with=cnf) as s:
        t0 = time.time()
        s.conf_budget(budget)
        r = s.solve_limited()
        return r, time.time() - t0, sum(1 for k, _, _ in pats if k == "A2H")


def fmt(r):
    return {True: "SAT", False: "UNSAT", None: "UNKNOWN(budget)"}[r]


log("=== pure ratio-4 triples (cp, 4cp, 16cp) ===")
first_unsat = None
for cp in range(4, 17):
    r, dt, na = test(cp, 4 * cp, 16 * cp)
    log("  c'=%3d c=%3d C=%4d size %3d A2H=%3d : %s (%.1fs)"
        % (cp, 4 * cp, 16 * cp, 12 * cp, na, fmt(r), dt))
    if r is False and first_unsat is None:
        first_unsat = (cp, 4 * cp, 16 * cp)

log("")
log("=== varying C at (16, 64, *) ===")
for C in [256, 320, 384]:
    r, dt, na = test(16, 64, C)
    log("  c'= 16 c= 64 C=%4d size %3d : %s (%.1fs)" % (C, C - 64, fmt(r), dt))

log("")
log("=== varying c at (16, *, 4c) ===")
for c in [64, 68, 72, 80, 96]:
    r, dt, na = test(16, c, 4 * c)
    log("  c'= 16 c=%3d C=%4d size %3d A2H=%3d: %s (%.1fs)"
        % (c, 4 * c, 3 * c, na, fmt(r), dt))

log("")
log("=== general triples with c' >= 16 ===")
for (cp, c, C) in [(17, 68, 272), (18, 72, 288), (20, 80, 320),
                   (16, 72, 288), (20, 96, 384)]:
    if C - c > 300:
        log("  c'=%3d c=%3d C=%4d : skipped (size %d)" % (cp, c, C, C - c))
        continue
    r, dt, na = test(cp, c, C)
    log("  c'=%3d c=%3d C=%4d size %3d A2H=%3d: %s (%.1fs)"
        % (cp, c, C, C - c, na, fmt(r), dt))

log("")
log("=== ablation: A2H dropped ===")
for (cp, c, C) in [(16, 64, 256), (20, 80, 320)]:
    r, dt, na = test(cp, c, C, with_a2h=False)
    log("  c=%3d C=%4d (no A2H): %s (%.1fs)" % (c, C, fmt(r), dt))

if first_unsat:
    cp, c, C = first_unsat
    log("")
    log("=== MUS for smallest ratio-4 UNSAT triple (%d,%d,%d) ===" % first_unsat)
    hard, pats, nv = build(c, C, use_a2h_cp=cp)
    t0 = time.time()
    core = mus_deletion(hard, pats, nv)
    kinds = {}
    for kind, t, _ in core:
        kinds[kind] = kinds.get(kind, 0) + 1
    log("MUS: %d pattern constraints (%.1fs), by kind: %s"
        % (len(core), time.time() - t0, kinds))
    for kind, t, _ in sorted(core, key=lambda p: (p[0], p[1])):
        log("   %-4s %s" % (kind, t))
log("")
log("DONE")
