"""blockalone_cp.py — same isolated-block death test as blockalone.py but with CP-SAT
(integer positions + AllDifferent), which scales to blocks of several hundred values
where the order-encoded CNF's transitivity triangles blow up.

Usage:  python3 blockalone_cp.py <cutspec> <j> [time_limit] [workers]
   cutspec: "geom:R:DEPTH" or a comma separated cut list.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from ortools.sat.python import cp_model                   # noqa: E402
from apcheck import has_monotone_kap_general              # noqa: E402
from blocks import constraints                            # noqa: E402


def decide(cuts, j, time_limit=600.0, workers=4):
    N = min(2 * cuts[j + 1] + 2, cuts[-1] - 1)
    C = constraints(cuts, N)
    assert not C['fatal'], "unavoidable [1+1+1+1]"
    vals = list(range(cuts[j], cuts[j + 1]))
    n = len(vals)
    idx = {v: i for i, v in enumerate(vals)}
    m = cp_model.CpModel()
    p = [m.NewIntVar(0, n - 1, f"p{v}") for v in vals]
    m.AddAllDifferent(p)
    bc = {}

    def before(u, w):
        if (u, w) in bc:
            return bc[(u, w)]
        b = m.NewBoolVar("")
        m.Add(p[idx[u]] < p[idx[w]]).OnlyEnforceIf(b)
        m.Add(p[idx[u]] > p[idx[w]]).OnlyEnforceIf(b.Not())
        bc[(u, w)] = b
        return b

    nu = nn = n4 = 0
    for (jj, u, w) in C['inv']:
        if jj == j:
            m.Add(p[idx[w]] < p[idx[u]]); nu += 1
    for (jj, a, e) in C['noinc3']:
        if jj == j:
            m.AddBoolOr([before(a, a + e).Not(), before(a + e, a + 2 * e).Not()]); nn += 1
    for (jj, a, e) in C['no4']:
        if jj == j:
            l1, l2, l3 = before(a, a + e), before(a + e, a + 2 * e), before(a + 2 * e, a + 3 * e)
            m.AddBoolOr([l1.Not(), l2.Not(), l3.Not()])
            m.AddBoolOr([l1, l2, l3]); n4 += 1
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_search_workers = workers
    t0 = time.time()
    st = s.Solve(m)
    dt = time.time() - t0
    stat = dict(n=n, inv=nu, noinc3=nn, no4=n4, ctx_N=N)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        order = sorted(vals, key=lambda v: s.Value(p[idx[v]]))
        assert not has_monotone_kap_general(order, 4)
        return "SAT", dt, stat, order
    if st == cp_model.INFEASIBLE:
        return "UNSAT", dt, stat, None
    return "UNKNOWN", dt, stat, None


if __name__ == "__main__":
    spec = sys.argv[1]
    j = int(sys.argv[2])
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600.0
    nw = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    if spec.startswith("geom:"):
        parts = spec.split(":")
        r, depth = int(parts[1]), int(parts[2]) if len(parts) > 2 else j + 3
        cuts = [r ** k for k in range(depth + 1)]
    else:
        cuts = [int(t) for t in spec.split(",")]
    st, dt, stat, order = decide(cuts, j, tl, nw)
    print(f"cuts={cuts} block {j} = [{cuts[j]}..{cuts[j+1]-1}] size={stat['n']} "
          f"(inv={stat['inv']} noinc3={stat['noinc3']} no4={stat['no4']}, ctx N={stat['ctx_N']}): "
          f"{st} ({dt:.1f}s)", flush=True)
    if order:
        import json
        with open(f"blockorder_{spec.replace(':','_').replace(',','_')}_{j}.json", "w") as f:
            json.dump(order, f)
