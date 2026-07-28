"""satprobe.py — exact feasibility of block-structured orderings on [1..N] (CP-SAT).

Probe A (contiguous blocks, base b): is there ANY assignment of internal orders to the
blocks D_j = [b^j, b^{j+1}) (blocks placed contiguously in increasing order) such that
the resulting permutation of [1..N] has no monotone 4-AP?  Only within-block relative
order is free; cross-block relative order is fixed.  This is a NECESSARY condition for
any infinite contiguous-base-b-block ordering (restriction principle).

Probe B (g-separated dyadic blocks): positions are globally free EXCEPT
pos(u) < pos(w) whenever block2(w) >= block2(u) + g.  g=2 means adjacent dyadic blocks
may interleave arbitrarily but blocks two apart are separated.  Feasibility on [1..N] is
a necessary condition for any infinite ordering with that separation discipline.

Encoding: integer position variables + AllDifferent; per-4-AP breaking clauses over
reified pair-inversion booleans.  Both orientations handled exactly.
Verdicts are exact (SAT with a checked model, or UNSAT).
"""

import sys
import time
import numpy as np
from ortools.sat.python import cp_model

sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R3")
from apcheck import has_monotone_kap_pos
from orderings import find_mono4


def blockb(n, b):
    m, p = 0, b
    while p <= n:
        m += 1
        p *= b
    return m


def all_aps(N):
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            yield x, d


def probe_contiguous(b, N, time_limit=600):
    """Blocks D_j placed contiguously; internal orders free. Returns (status, perm|witness)."""
    blk = {v: blockb(v, b) for v in range(1, N + 1)}
    members = {}
    for v in range(1, N + 1):
        members.setdefault(blk[v], []).append(v)

    model = cp_model.CpModel()
    pos = {}
    for j, mem in members.items():
        for v in mem:
            pos[v] = model.NewIntVar(0, len(mem) - 1, f"p{v}")
        model.AddAllDifferent([pos[v] for v in mem])

    inv = {}  # (u,w) u<w same block -> Bool "w placed before u"

    def get_inv(u, w):
        if (u, w) not in inv:
            bvar = model.NewBoolVar(f"i{u}_{w}")
            model.Add(pos[u] > pos[w]).OnlyEnforceIf(bvar)
            model.Add(pos[u] < pos[w]).OnlyEnforceIf(bvar.Not())
            inv[(u, w)] = bvar
        return inv[(u, w)]

    n_ap = 0
    for x, d in all_aps(N):
        t = [x + k * d for k in range(4)]
        pairs = [(t[k], t[k + 1]) for k in range(3)]
        same = [p for p in pairs if blk[p[0]] == blk[p[1]]]
        # increasing orientation: cross-block pairs are increasing by construction
        if not same:
            return "UNSAT-forced", (x, d, t)
        model.AddBoolOr([get_inv(u, w) for (u, w) in same])
        # decreasing orientation: impossible unless all four in one block
        if blk[t[0]] == blk[t[3]]:
            model.AddBoolOr([get_inv(u, w).Not() for (u, w) in pairs])
        n_ap += 1

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 4
    st = solver.Solve(model)
    if st == cp_model.OPTIMAL or st == cp_model.FEASIBLE:
        # reconstruct permutation: blocks ascending, inside by pos
        perm = []
        for j in sorted(members):
            mem = sorted(members[j], key=lambda v: solver.Value(pos[v]))
            perm.extend(mem)
        assert sorted(perm) == list(range(1, N + 1))
        assert not find_mono4(perm), "model check failed!"
        assert not has_monotone_kap_pos(perm, 4) if N <= 600 else True
        return "SAT", perm
    if st == cp_model.INFEASIBLE:
        return "UNSAT", n_ap
    return "UNKNOWN", n_ap


def probe_separated(g, N, time_limit=1200, b=2):
    """Blocks base-b; hard: pos(u)<pos(w) if block(w)>=block(u)+g; else free."""
    blk = {v: blockb(v, b) for v in range(1, N + 1)}
    model = cp_model.CpModel()
    pos = {v: model.NewIntVar(0, N - 1, f"p{v}") for v in range(1, N + 1)}
    model.AddAllDifferent(list(pos.values()))
    # separation constraints (only needed between consecutive "levels": enforce
    # transitively-reduced form: for each v, and each w with blk(w) == blk(v)+g, ... —
    # simplest exact form: max pos of block j < min pos of block j' for j' >= j+g.
    # Encode via per-block min/max variables.
    members = {}
    for v in range(1, N + 1):
        members.setdefault(blk[v], []).append(v)
    js = sorted(members)
    bmin, bmax = {}, {}
    for j in js:
        bmin[j] = model.NewIntVar(0, N - 1, f"mn{j}")
        bmax[j] = model.NewIntVar(0, N - 1, f"mx{j}")
        model.AddMinEquality(bmin[j], [pos[v] for v in members[j]])
        model.AddMaxEquality(bmax[j], [pos[v] for v in members[j]])
    # completeness: bmax[j] < bmin[j'] for j' in {j+g, j+g+1} implies, by induction
    # along chains of +g/+(g+1) steps (every offset >= g is reachable since g>=1 and
    # bmin[j'] <= bmax[j']), separation for ALL j' >= j+g.
    for j in js:
        for off in (g, g + 1):
            if j + off in bmin:
                model.Add(bmax[j] < bmin[j + off])

    inv = {}

    def get_inv(u, w):
        if (u, w) not in inv:
            bvar = model.NewBoolVar(f"i{u}_{w}")
            model.Add(pos[u] > pos[w]).OnlyEnforceIf(bvar)
            model.Add(pos[u] < pos[w]).OnlyEnforceIf(bvar.Not())
            inv[(u, w)] = bvar
        return inv[(u, w)]

    for x, d in all_aps(N):
        t = [x + k * d for k in range(4)]
        pairs = [(t[k], t[k + 1]) for k in range(3)]
        free = [p for p in pairs if blk[p[1]] - blk[p[0]] < g]
        if not free:
            return "UNSAT-forced", (x, d, t)
        model.AddBoolOr([get_inv(u, w) for (u, w) in free])
        if all(blk[p[1]] - blk[p[0]] < g for p in pairs):
            model.AddBoolOr([get_inv(u, w).Not() for (u, w) in pairs])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 4
    st = solver.Solve(model)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        perm = sorted(range(1, N + 1), key=lambda v: solver.Value(pos[v]))
        assert sorted(perm) == list(range(1, N + 1))
        assert not find_mono4(perm), "model check failed!"
        # verify the separation discipline explicitly on the model
        posmap = {v: i for i, v in enumerate(perm)}
        for u in range(1, N + 1):
            for w in range(1, N + 1):
                if blk[w] >= blk[u] + g:
                    assert posmap[u] < posmap[w], ("separation violated", u, w)
        return "SAT", perm
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


def main():
    out = []

    def run(tag, fn, *a, **k):
        t0 = time.time()
        st, data = fn(*a, **k)
        dt = time.time() - t0
        line = f"{tag}: {st}  ({dt:.1f}s)"
        if st == "UNSAT-forced":
            line += f"  forced AP {data}"
        print(line, flush=True)
        out.append((tag, st, data if st in ("SAT", "UNSAT-forced") else None))
        return st, data

    run("A base2 N=30", probe_contiguous, 2, 30)
    run("A base3 N=242", probe_contiguous, 3, 242)
    run("A base4 N=255", probe_contiguous, 4, 255)
    st3, d3 = run("A base3 N=728", probe_contiguous, 3, 728, 1200)
    if st3 == "SAT":
        np.save("/home/user/erdos/attempts/route-R3/sat_base3_728.npy", np.array(d3))
    st4, d4 = run("A base4 N=1023", probe_contiguous, 4, 1023, 1200)
    if st4 == "SAT":
        np.save("/home/user/erdos/attempts/route-R3/sat_base4_1023.npy", np.array(d4))
    stB, dB = run("B dyadic g=2 N=511", probe_separated, 2, 511, 1800)
    if stB == "SAT":
        np.save("/home/user/erdos/attempts/route-R3/sat_sep2_511.npy", np.array(dB))


if __name__ == "__main__":
    main()
