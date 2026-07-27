"""cpsat_check.py — independent second engine (Google OR-tools CP-SAT).

Decides: does a monotone-4-AP-free permutation of [1..N] exist under constraint class
cls with C = num/den?  Completely different formulation and solver from fast/fast2:
  - integer variables pos[v] in [lo(v), hi(v)], AllDifferent;
  - for every ordered pair (u,w), u<w, that occurs as a consecutive pair of some 4-AP
    inside [1..N], a Boolean b[u,w] reified as pos[u] < pos[w];
  - for every 4-AP (t0,t1,t2,t3) = (x, x+d, x+2d, x+3d) with x>=1, d>=1, x+3d<=N:
      NOT(b[t0,t1] & b[t1,t2] & b[t2,t3])      (no increasing monotone 4-AP)
      NOT(!b[t0,t1] & !b[t1,t2] & !b[t2,t3])   (no decreasing monotone 4-AP)
Usage: python3 cpsat_check.py N cls num den [timelimit_s] [workers]
Prints CPSAT N=... cls=... C=... status=FEASIBLE/INFEASIBLE/UNKNOWN [example=...]
Any FEASIBLE example is re-verified in-process by the validated apcheck checker.
"""

import sys
from fractions import Fraction

from ortools.sat.python import cp_model

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos


def build_and_solve(N, cls, C, timelimit=None, workers=2):
    num, den = C.numerator, C.denominator
    m = cp_model.CpModel()
    lo = [0] * (N + 1)
    hi = [0] * (N + 1)
    for v in range(1, N + 1):
        l, h = 1, N
        if cls in ("A", "C"):
            h = min(N, (num * v) // den)
        if cls in ("B", "C"):
            l = -((-v * den) // num)
        if cls == "D" and v <= N // 2:
            h = min(N, 2 * v)
        lo[v], hi[v] = l, h
    pos = {v: m.NewIntVar(lo[v], hi[v], f"pos{v}") for v in range(1, N + 1)}
    m.AddAllDifferent(list(pos.values()))

    aps = []
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            aps.append((x, x + d, x + 2 * d, x + 3 * d))
    pairs = {}
    for t in aps:
        for u, w in ((t[0], t[1]), (t[1], t[2]), (t[2], t[3])):
            if (u, w) not in pairs:
                b = m.NewBoolVar(f"b{u}_{w}")
                m.Add(pos[u] < pos[w]).OnlyEnforceIf(b)
                m.Add(pos[u] > pos[w]).OnlyEnforceIf(b.Not())
                pairs[(u, w)] = b
    for t0, t1, t2, t3 in aps:
        b1, b2, b3 = pairs[(t0, t1)], pairs[(t1, t2)], pairs[(t2, t3)]
        m.AddBoolOr([b1.Not(), b2.Not(), b3.Not()])
        m.AddBoolOr([b1, b2, b3])

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = 196
    if timelimit:
        solver.parameters.max_time_in_seconds = timelimit
    st = solver.Solve(m)
    if st == cp_model.OPTIMAL or st == cp_model.FEASIBLE:
        perm = [0] * N
        for v in range(1, N + 1):
            perm[solver.Value(pos[v]) - 1] = v
        assert sorted(perm) == list(range(1, N + 1))
        assert not has_monotone_kap_pos(perm, 4), "CP-SAT produced a bad witness!"
        return "FEASIBLE", perm
    if st == cp_model.INFEASIBLE:
        return "INFEASIBLE", None
    return "UNKNOWN", None


if __name__ == "__main__":
    N = int(sys.argv[1]); cls = sys.argv[2]
    C = Fraction(int(sys.argv[3]), int(sys.argv[4]))
    tl = float(sys.argv[5]) if len(sys.argv) > 5 else None
    wk = int(sys.argv[6]) if len(sys.argv) > 6 else 2
    status, perm = build_and_solve(N, cls, C, tl, wk)
    line = f"CPSAT N={N} cls={cls} C={C.numerator}/{C.denominator} status={status}"
    if perm:
        line += " example=" + ",".join(map(str, perm))
    print(line)
