"""dissect_D3.py — which sub-families of the base-3 D_3=[27,81) single-block system
are already contradictory?  Subset lattice + irreducible core over labeled groups.
Solver: pysat/Glucose42, transitivity encoding (as in singleblock_xcheck)."""

import sys
import time
from itertools import combinations
from pysat.solvers import Glucose42
from pysat.formula import IDPool

sys.path.insert(0, "/home/user/erdos/attempts/route-R3")
from singleblock import constraints_for_block

L, b = 27, 3
aps4, g3, forced = constraints_for_block(L, b)
g3_bot = [(u, d) for (u, d) in g3 if 1 <= u - d < L]
g3_top = [(u, d) for (u, d) in g3 if u + 3 * d >= b * L]
f1 = [(u, d) for (u, d, t) in forced if t == "F1"]
f2 = [(u, d) for (u, d, t) in forced if t == "F2"]
print(f"|4AP|={len(aps4)} |g3bot|={len(g3_bot)} |g3top|={len(g3_top)} "
      f"(overlap={len(set(g3_bot)&set(g3_top))}) |F1|={len(f1)} |F2|={len(f2)}")

pool = IDPool()
elems = list(range(L, b * L))


def lt(u, w):
    return pool.id(("lt", u, w)) if u < w else -pool.id(("lt", w, u))


base = []
for u, v, w in combinations(elems, 3):
    a, c, e = lt(u, v), lt(v, w), lt(u, w)
    base.append([-a, -c, e])
    base.append([a, c, -e])


def group_clauses(kind, item):
    if kind == "4AP":
        u, d = item
        t = [u + k * d for k in range(4)]
        return [[-lt(t[k], t[k + 1]) for k in range(3)],
                [lt(t[k], t[k + 1]) for k in range(3)]]
    if kind in ("g3bot", "g3top"):
        u, d = item
        return [[-lt(u, u + d), -lt(u + d, u + 2 * d)]]
    if kind in ("F1", "F2"):
        u, d = item
        return [[-lt(u, u + d)]]
    raise ValueError


FAM = {"4AP": aps4, "g3bot": g3_bot, "g3top": g3_top, "F1": f1, "F2": f2}


def solve_subset(kinds, want_core=False):
    s = Glucose42(bootstrap_with=base)
    sel = {}
    assum = []
    for kind in kinds:
        for item in FAM[kind]:
            a = pool.id(("sel", kind, item))
            sel[a] = (kind, item)
            for cl in group_clauses(kind, item):
                s.add_clause(cl + [-a])
            assum.append(a)
    ok = s.solve(assumptions=assum)
    core = None
    if not ok and want_core:
        core = [sel[a] for a in s.get_core()]
    s.delete()
    return ok, core


for kinds in (["4AP"], ["g3bot", "g3top"], ["F1", "F2"],
              ["g3bot", "g3top", "F1", "F2"],
              ["4AP", "F1", "F2"], ["4AP", "g3bot", "g3top"],
              ["g3bot", "F1", "F2"], ["g3top", "F1", "F2"],
              ["4AP", "g3bot", "g3top", "F1", "F2"]):
    t0 = time.time()
    ok, _ = solve_subset(kinds)
    print(f"{'+'.join(kinds):30s}: {'SAT' if ok else 'UNSAT'} ({time.time()-t0:.1f}s)",
          flush=True)

# irreducible core of the smallest UNSAT combination found above
print("\ncomputing irreducible core over all families...")
ok, core = solve_subset(["4AP", "g3bot", "g3top", "F1", "F2"], want_core=True)
assert not ok
core = list(core)
i = 0
while i < len(core):
    trial = core[:i] + core[i + 1:]
    s = Glucose42(bootstrap_with=base)
    assum = []
    for (kind, item) in trial:
        a = pool.id(("sel2", kind, item))
        for cl in group_clauses(kind, item):
            s.add_clause(cl + [-a])
        assum.append(a)
    ok = s.solve(assumptions=assum)
    s.delete()
    if not ok:
        core = trial
        i = 0
    else:
        i += 1
print(f"irreducible core: {len(core)} constraints")
from collections import Counter
print(Counter(k for (k, _) in core))
for (kind, (u, d)) in sorted(core, key=lambda t: (t[0], t[1][0] + 3 * t[1][1])):
    kmax = 4 if kind == "4AP" else 3
    print(f"  {kind:5s} u={u:2d} d={d:2d} terms={[u + k * d for k in range(kmax)]}")
