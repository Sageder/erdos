"""muscert.py — independent verification + minimal certificate for the base-3 result.

Claim (from CP-SAT, satprobe.py): there is NO assignment of internal orders to the
contiguous base-3 blocks D_j = [3^j, 3^{j+1}) making [1..87] monotone-4-AP-free,
while [1..86] is possible.

This file re-proves UNSAT(87) with a DIFFERENT solver stack (pysat / Glucose or
Minisat) and a DIFFERENT encoding (pure boolean order variables + explicit
transitivity), then extracts and greedily minimizes an unsatisfiable core of APs:
a finite list of APs such that block-contiguity + "break each listed AP" is already
contradictory.  The core is then re-verified by brute CP-SAT on just those APs.
"""

import sys
import time
from itertools import combinations

from pysat.solvers import Glucose42
from pysat.formula import IDPool

sys.path.insert(0, "/home/user/erdos/attempts/route-R3")


def blockb(n, b):
    m, p = 0, b
    while p <= n:
        m += 1
        p *= b
    return m


def build(N, b=3):
    blk = {v: blockb(v, b) for v in range(1, N + 1)}
    members = {}
    for v in range(1, N + 1):
        members.setdefault(blk[v], []).append(v)
    pool = IDPool()

    def lt(u, w):  # literal: "u placed before w" (same block, u<w numerically)
        assert blk[u] == blk[w] and u < w
        return pool.id(("lt", u, w))

    clauses = []  # transitivity: for u<v<w same block: lt(u,v)&lt(v,w)->lt(u,w); and contrapositive chain
    for j, mem in members.items():
        for u, v, w in combinations(mem, 3):
            a, c, e = lt(u, v), lt(v, w), lt(u, w)
            clauses.append([-a, -c, e])
            clauses.append([a, c, -e])

    ap_groups = []  # (x, d, list-of-clauses)
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            t = [x + k * d for k in range(4)]
            pairs = [(t[k], t[k + 1]) for k in range(3)]
            same = [p for p in pairs if blk[p[0]] == blk[p[1]]]
            g = []
            # increasing: need some same-block adjacent pair inverted (w before u)
            g.append([-lt(u, w) for (u, w) in same])  # empty list = empty clause = forced
            if blk[t[0]] == blk[t[3]]:
                g.append([lt(u, w) for (u, w) in pairs])
            ap_groups.append((x, d, g))
    return clauses, ap_groups, pool


def solve_with_groups(base_clauses, groups, pool, want_core=False):
    s = Glucose42(bootstrap_with=base_clauses)
    assum = []
    sel = {}
    for (x, d, g) in groups:
        a = pool.id(("sel", x, d))
        sel[a] = (x, d)
        for cl in g:
            s.add_clause(cl + [-a])
        assum.append(a)
    ok = s.solve(assumptions=assum)
    core = None
    if not ok and want_core:
        core = [sel[a] for a in s.get_core()]
    s.delete()
    return ok, core


def main():
    t0 = time.time()
    base, groups, pool = build(86)
    ok86, _ = solve_with_groups(base, groups, pool)
    print(f"pysat base3 N=86: {'SAT' if ok86 else 'UNSAT'} ({time.time()-t0:.1f}s)")
    assert ok86

    t0 = time.time()
    base, groups, pool = build(87)
    ok87, core = solve_with_groups(base, groups, pool, want_core=True)
    print(f"pysat base3 N=87: {'SAT' if ok87 else 'UNSAT'} ({time.time()-t0:.1f}s), "
          f"initial core: {len(core)} APs")
    assert not ok87

    # greedy core minimization (delete one AP at a time if still UNSAT)
    core = list(core)
    i = 0
    while i < len(core):
        trial = core[:i] + core[i + 1:]
        gsub = [g for g in groups if (g[0], g[1]) in set(trial)]
        ok, newcore = solve_with_groups(base, gsub, pool, want_core=True)
        if not ok:
            core = newcore if newcore is not None and len(newcore) < len(trial) else trial
            i = 0 if (newcore is not None and len(newcore) < len(trial)) else i
        else:
            i += 1
    print(f"minimal (irreducible) core: {len(core)} APs")
    for (x, d) in sorted(core, key=lambda t: (t[0] + 3 * t[1], t[1])):
        t = [x + k * d for k in range(4)]
        print(f"  x={x:3d} d={d:3d} terms={t} blocks={[blockb(v,3) for v in t]}")

    # re-verify the core with CP-SAT (third check)
    from ortools.sat.python import cp_model
    coreset = set(core)
    blk = {v: blockb(v, 3) for v in range(1, 88)}
    members = {}
    for v in range(1, 88):
        members.setdefault(blk[v], []).append(v)
    model = cp_model.CpModel()
    pos = {}
    for j, mem in members.items():
        for v in mem:
            pos[v] = model.NewIntVar(0, len(mem) - 1, f"p{v}")
        model.AddAllDifferent([pos[v] for v in mem])
    inv = {}

    def gi(u, w):
        if (u, w) not in inv:
            bb = model.NewBoolVar("")
            model.Add(pos[u] > pos[w]).OnlyEnforceIf(bb)
            model.Add(pos[u] < pos[w]).OnlyEnforceIf(bb.Not())
            inv[(u, w)] = bb
        return inv[(u, w)]

    for (x, d) in coreset:
        t = [x + k * d for k in range(4)]
        pairs = [(t[k], t[k + 1]) for k in range(3)]
        same = [p for p in pairs if blk[p[0]] == blk[p[1]]]
        model.AddBoolOr([gi(u, w) for (u, w) in same])
        if blk[t[0]] == blk[t[3]]:
            model.AddBoolOr([gi(u, w).Not() for (u, w) in pairs])
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 120
    st = solver.Solve(model)
    assert st == cp_model.INFEASIBLE, "CP-SAT re-verification of core failed!"
    print("core re-verified UNSAT by CP-SAT (independent 3rd check)")


if __name__ == "__main__":
    main()
