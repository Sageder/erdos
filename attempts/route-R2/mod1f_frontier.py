"""mod1f_frontier.py — fixed-encoding frontier scan for the Mod-1 obstruction.

Question: for which consecutive-boundary triples (c', c, C) (previous block
[c',c), this block [c,C)) does the SOUND constraint system
    A4 + D4 + A3T + A3H + A2T + A2H(c')
become unsatisfiable?  In any block-major interval chain with all ratios >= 4,
the 4th block onward always has c' >= 16, c >= 4c', C >= 4c.

Also: ablation — same triples with A2H dropped (chain-independent system).
Finally: MUS certificate for the smallest UNSAT triple found.
"""

import sys
import time

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from mod1b_sweep_mus import build, solve_with  # noqa: E402
from mod1d_mus import mus_deletion  # noqa: E402

out = []


def log(s):
    print(s, flush=True)
    out.append(s)


def test(cp, c, C, with_a2h=True):
    hard, pats, nv = build(c, C, use_a2h_cp=cp if with_a2h else None)
    t0 = time.time()
    sat = solve_with(hard, pats, nv)
    return sat, time.time() - t0, sum(1 for k, _, _ in pats if k == "A2H")


log("=== pure ratio-4 triples (cp, 4cp, 16cp): find the UNSAT threshold ===")
first_unsat = None
for cp in range(4, 17):
    sat, dt, na = test(cp, 4 * cp, 16 * cp)
    log("  c'=%3d c=%3d C=%4d size %3d A2H=%3d : %s (%.1fs)"
        % (cp, 4 * cp, 16 * cp, 12 * cp, na, "SAT" if sat else "UNSAT", dt))
    if not sat and first_unsat is None:
        first_unsat = (cp, 4 * cp, 16 * cp)

log("")
log("=== varying C at (16, 64, *) ===")
for C in [256, 320, 384, 448]:
    sat, dt, na = test(16, 64, C)
    log("  c'= 16 c= 64 C=%4d size %3d : %s (%.1fs)"
        % (C, C - 64, "SAT" if sat else "UNSAT", dt))

log("")
log("=== varying c at (16, *, 4c) ===")
for c in [64, 68, 72, 80, 96, 112, 128]:
    sat, dt, na = test(16, c, 4 * c)
    log("  c'= 16 c=%3d C=%4d size %3d A2H=%3d: %s (%.1fs)"
        % (c, 4 * c, 3 * c, na, "SAT" if sat else "UNSAT", dt))

log("")
log("=== general triples with c' >= 16 (4th-block region of any chain) ===")
for (cp, c, C) in [(17, 68, 272), (18, 72, 288), (20, 80, 320), (24, 96, 384),
                   (16, 72, 288), (16, 96, 384), (20, 96, 384), (16, 128, 512),
                   (32, 128, 512)]:
    if C - c > 400:
        log("  c'=%3d c=%3d C=%4d : skipped (size %d too large)"
            % (cp, c, C, C - c))
        continue
    sat, dt, na = test(cp, c, C)
    log("  c'=%3d c=%3d C=%4d size %3d A2H=%3d: %s (%.1fs)"
        % (cp, c, C, C - c, na, "SAT" if sat else "UNSAT", dt))

log("")
log("=== ablation: A2H dropped (chain-independent system only) ===")
for (cp, c, C) in [(16, 64, 256), (24, 96, 384)]:
    sat, dt, na = test(cp, c, C, with_a2h=False)
    log("  c=%3d C=%4d (no A2H): %s (%.1fs)"
        % (c, C, "SAT" if sat else "UNSAT", dt))

if first_unsat:
    cp, c, C = first_unsat
    log("")
    log("=== MUS certificate for smallest ratio-4 UNSAT triple (%d,%d,%d) ==="
        % first_unsat)
    hard, pats, nv = build(c, C, use_a2h_cp=cp)
    t0 = time.time()
    core = mus_deletion(hard, pats, nv)
    log("minimal unsatisfiable subset: %d pattern constraints (%.1fs), "
        "verified minimal:" % (len(core), time.time() - t0))
    kinds = {}
    for kind, t, _ in core:
        kinds[kind] = kinds.get(kind, 0) + 1
    log("  by kind: %s" % kinds)
    for kind, t, _ in sorted(core, key=lambda p: (p[0], p[1])):
        log("   %-4s %s" % (kind, t))

with open("/home/user/erdos/attempts/route-R2/mod1f_output.txt", "w") as f:
    f.write("\n".join(out) + "\n")
