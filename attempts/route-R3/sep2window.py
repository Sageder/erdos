"""sep2window.py — decoupled window system for 2-SEPARATED dyadic orderings.

Discipline: pos(u) < pos(w) whenever block2(w) >= block2(u) + 2 (adjacent dyadic
blocks may interleave arbitrarily).  For the window U_m = B_m ∪ B_{m+1} =
[2^m, 2^{m+2}) the relative order of window elements is unconstrained by the
discipline, while every value < 2^{m-1} precedes and every value >= 2^{m+3} follows
the whole window.  Necessary constraints on the window order (any monotone-4-AP-free
2-separated ordering must satisfy them):

  (a) no monotone 4-AP with all four terms in U_m (both orientations);
  (b) no increasing 3-AP (u, u+d, u+2d) ⊆ U_m with 1 <= u-d < 2^{m-1}
      (bottom-grounded) or u+3d >= 2^{m+3} (top-grounded);
  (c) forced inversions of pairs (u, u+d) ⊆ U_m:
      F1: 1 <= u-d < 2^{m-1} and u+2d >= 2^{m+3};
      F2: u-2d >= 1, u-d < 2^{m-1}, block2(u-2d) <= block2(u-d) - 2.

Scaling: multiplication by 2 embeds the U_m system into the U_{m+1} system
(thresholds double, block gaps preserved), so UNSAT at m propagates to all m' >= m
and hence kills every 2-separated dyadic ordering of N.

Decided by CP-SAT; cross-checked by Cadical/Glucose + (on UNSAT) DRUP proof with the
independent RUP checker of dratcert.py.
"""

import sys
import time
from itertools import combinations
from ortools.sat.python import cp_model

sys.path.insert(0, "/home/user/erdos/attempts/route-R3")


def block2(n):
    return n.bit_length() - 1


def window_constraints(m):
    L, R = 1 << m, 1 << (m + 2)
    lo, hi = 1 << (m - 1), 1 << (m + 3)
    aps4, g3, forced = [], [], []
    for d in range(1, (R - 1 - L) // 3 + 1):
        for u in range(L, R - 3 * d):
            aps4.append((u, d))
    for d in range(1, (R - 1 - L) // 2 + 1):
        for u in range(L, R - 2 * d):
            if (1 <= u - d < lo) or (u + 3 * d >= hi):
                g3.append((u, d))
    for d in range(1, R - L):
        for u in range(L, R - d):
            if 1 <= u - d < lo and u + 2 * d >= hi:
                forced.append((u, d))
            elif u - 2 * d >= 1 and u - d < lo and block2(u - 2 * d) <= block2(u - d) - 2:
                forced.append((u, d))
    return L, R, aps4, g3, forced


def solve_window(m, time_limit=1500):
    L, R, aps4, g3, forced = window_constraints(m)
    model = cp_model.CpModel()
    pos = {v: model.NewIntVar(0, R - L - 1, f"p{v}") for v in range(L, R)}
    model.AddAllDifferent(list(pos.values()))
    inv = {}

    def gi(u, w):
        if (u, w) not in inv:
            bb = model.NewBoolVar("")
            model.Add(pos[u] > pos[w]).OnlyEnforceIf(bb)
            model.Add(pos[u] < pos[w]).OnlyEnforceIf(bb.Not())
            inv[(u, w)] = bb
        return inv[(u, w)]

    for (u, d) in aps4:
        t = [u + k * d for k in range(4)]
        prs = [(t[k], t[k + 1]) for k in range(3)]
        model.AddBoolOr([gi(a, c) for (a, c) in prs])
        model.AddBoolOr([gi(a, c).Not() for (a, c) in prs])
    for (u, d) in g3:
        model.AddBoolOr([gi(u, u + d), gi(u + d, u + 2 * d)])
    for (u, d) in forced:
        model.Add(pos[u + d] < pos[u])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 3
    st = solver.Solve(model)
    sizes = (len(aps4), len(g3), len(forced))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        order = sorted(range(L, R), key=lambda v: solver.Value(pos[v]))
        return "SAT", order, sizes
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None, sizes
    return "UNKNOWN", None, sizes


def pysat_check(m):
    from pysat.solvers import Cadical103
    L, R, aps4, g3, forced = window_constraints(m)
    idx = {}

    def var(u, w):
        if (u, w) not in idx:
            idx[(u, w)] = len(idx) + 1
        return idx[(u, w)]

    def lt(u, w):
        return var(u, w) if u < w else -var(w, u)

    cls = []
    elems = list(range(L, R))
    for u, v, w in combinations(elems, 3):
        a, c, e = lt(u, v), lt(v, w), lt(u, w)
        cls.append([-a, -c, e])
        cls.append([a, c, -e])
    for (u, d) in aps4:
        t = [u + k * d for k in range(4)]
        cls.append([-lt(t[k], t[k + 1]) for k in range(3)])
        cls.append([lt(t[k], t[k + 1]) for k in range(3)])
    for (u, d) in g3:
        cls.append([-lt(u, u + d), -lt(u + d, u + 2 * d)])
    for (u, d) in forced:
        cls.append([-lt(u, u + d)])
    s = Cadical103(bootstrap_with=cls, with_proof=True)
    ok = s.solve()
    proof = None if ok else s.get_proof()
    s.delete()
    return ("SAT" if ok else "UNSAT"), cls, proof


if __name__ == "__main__":
    for m in (3, 4, 5, 6):
        t0 = time.time()
        st, order, sizes = solve_window(m, 1800)
        print(f"sep2 window U_{m}=[{1<<m},{1<<(m+2)}): {st} "
              f"(|4AP|={sizes[0]},|g3|={sizes[1]},|forced|={sizes[2]}) "
              f"({time.time()-t0:.1f}s)", flush=True)
        if st == "UNSAT":
            st2, cls, proof = pysat_check(m)
            print(f"  pysat cross-check: {st2}, proof lines: "
                  f"{len(proof) if proof else '-'}", flush=True)
            if st2 == "UNSAT":
                from dratcert import verify
                good, msg = verify(cls, proof)
                print(f"  RUP verification: {'OK' if good else 'FAIL'} — {msg}",
                      flush=True)
                open(f"sep2_U{m}.drat", "w").write("\n".join(proof) + "\n")
            break
        if st == "UNKNOWN":
            break
