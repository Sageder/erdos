"""jointsat.py — EXACT decision of "is there a 4-AP-free LAYERED permutation of [1..N]
for this cut sequence?", using the (cross-validated) block decomposition of blocks.py
inside one CP-SAT model.  Unlike blocksat.py's greedy "seq" mode this is not conditional
on choices made in lower blocks, so UNSAT here is a genuine death certificate for the cut
sequence (modulo CP-SAT correctness; SAT results are re-verified with apcheck).

Model: one IntVar per value giving its position INSIDE its block, AllDifferent per block.
Cross-block comparisons are determined by the block order, so only intra-block pairs need
reified booleans -- which is why this scales far past a global order-encoded SAT model.
"""

import sys, time, json
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from ortools.sat.python import cp_model                     # noqa: E402
from apcheck import has_monotone_kap_pos                    # noqa: E402
from blocks import constraints, blk_of, check_orders, assemble  # noqa: E402


def geom_cuts(r, top):
    c = [1]
    while c[-1] <= top:
        c.append(c[-1] * r)
    return c


def joint(cuts, N, time_limit=300.0, workers=4, hint_orders=None, log=False):
    C = constraints(cuts, N)
    if C['fatal']:
        return dict(status="FATAL", detail=C['fatal'][:3])
    B = blk_of(cuts, N)
    blocks = {}
    for v in range(1, N + 1):
        blocks.setdefault(B[v], []).append(v)
    m = cp_model.CpModel()
    p = {}
    for j, vals in blocks.items():
        n = len(vals)
        for v in vals:
            p[v] = m.NewIntVar(0, n - 1, f"p{v}")
        m.AddAllDifferent([p[v] for v in vals])
    bc = {}

    def before(u, w):
        if (u, w) in bc:
            return bc[(u, w)]
        b = m.NewBoolVar(f"b{u}_{w}")
        m.Add(p[u] < p[w]).OnlyEnforceIf(b)
        m.Add(p[u] > p[w]).OnlyEnforceIf(b.Not())
        bc[(u, w)] = b
        return b

    for (j, u, w) in C['inv']:
        m.Add(p[w] < p[u])
    for (j, a, e) in C['noinc3']:
        m.AddBoolOr([before(a, a + e).Not(), before(a + e, a + 2 * e).Not()])
    for (j, a, e) in C['no4']:
        l1, l2, l3 = before(a, a + e), before(a + e, a + 2 * e), before(a + 2 * e, a + 3 * e)
        m.AddBoolOr([l1.Not(), l2.Not(), l3.Not()])
        m.AddBoolOr([l1, l2, l3])
    for (lo, hi) in C['pair22']:
        m.AddBoolOr([before(lo[1], lo[2]).Not(), before(hi[1], hi[2]).Not()])
    if hint_orders:
        for j, o in hint_orders.items():
            for i, v in enumerate(o):
                if v in p:
                    m.AddHint(p[v], i)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_search_workers = workers
    s.parameters.log_search_progress = log
    t0 = time.time()
    st = s.Solve(m)
    dt = time.time() - t0
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        orders = {j: sorted(vals, key=lambda v: s.Value(p[v])) for j, vals in blocks.items()}
        perm = assemble(cuts, N, orders)
        bad = check_orders(cuts, N, orders)
        assert not bad, bad
        assert not has_monotone_kap_pos(perm, 4), "TRUSTED CHECKER DISAGREES"
        return dict(status="SAT", secs=dt, orders=orders, perm=perm)
    if st == cp_model.INFEASIBLE:
        return dict(status="UNSAT", secs=dt)
    return dict(status="UNKNOWN", secs=dt)


if __name__ == "__main__":
    # CLI:  python3 jointsat.py <cutspec> <N> <time_limit>
    #   cutspec: "geom:R" or comma separated cut list "1,3,9,27"
    spec = sys.argv[1]
    N = int(sys.argv[2])
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 300.0
    if spec.startswith("geom:"):
        r = int(spec.split(":")[1])
        cuts = geom_cuts(r, N)
    else:
        cuts = [int(x) for x in spec.split(",")]
        if cuts[-1] <= N:
            cuts.append(N + 1)
    nw = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    res = joint(cuts, N, time_limit=tl, workers=nw)
    print(f"cuts={[c for c in cuts if c <= N]} N={N}: {res['status']} ({res.get('secs',0):.1f}s)",
          flush=True)
    if res['status'] == "SAT":
        tag = spec.replace(":", "").replace(",", "_")
        with open(f"witness_{tag}_N{N}.json", "w") as f:
            json.dump(dict(cuts=cuts, N=N, perm=res['perm']), f)
        print("  witness saved")
