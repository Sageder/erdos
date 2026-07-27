"""verify_unsat_asym.py — INDEPENDENT verification of the two extinction results:
  (E1) no permutation of [1..45] with {no dec-3AP, no inc-4AP} and pos(v) <= 2v ∀v
  (E2) no permutation of [1..80] with {no dec-3AP, no inc-4AP} and pos(v) <= 3v ∀v
First found UNSAT by CaDiCaL on the order encoding (asym_linear_profile.py).
Here: OR-tools CP-SAT with a DIRECT positional model (position variables per value,
AllDifferent, per-AP reified pattern forbidding) — different solver, different encoding.
Also re-checks the boundary SAT cases (44 resp. ~60) to confirm the model agrees on
the positive side.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from ortools.sat.python import cp_model


def solve_cpsat(N, C, timeout_s=3600):
    m = cp_model.CpModel()
    pos = {v: m.NewIntVar(1, min(N, C * v), f"p{v}") for v in range(1, N + 1)}
    m.AddAllDifferent(list(pos.values()))
    for e in range(1, (N - 1) // 2 + 1):
        for x in range(1, N - 2 * e + 1):
            # no dec-3AP: NOT(pos[x] > pos[x+e] > pos[x+2e])
            b1 = m.NewBoolVar(f"d{x}_{e}_1")   # pos[x] > pos[x+e]
            b2 = m.NewBoolVar(f"d{x}_{e}_2")   # pos[x+e] > pos[x+2e]
            m.Add(pos[x] > pos[x + e]).OnlyEnforceIf(b1)
            m.Add(pos[x] < pos[x + e]).OnlyEnforceIf(b1.Not())
            m.Add(pos[x + e] > pos[x + 2 * e]).OnlyEnforceIf(b2)
            m.Add(pos[x + e] < pos[x + 2 * e]).OnlyEnforceIf(b2.Not())
            m.AddBoolOr([b1.Not(), b2.Not()])
            if x + 3 * e <= N:
                b3 = m.NewBoolVar(f"d{x}_{e}_3")
                m.Add(pos[x + 2 * e] > pos[x + 3 * e]).OnlyEnforceIf(b3)
                m.Add(pos[x + 2 * e] < pos[x + 3 * e]).OnlyEnforceIf(b3.Not())
                # no inc-4AP: NOT(~b1 & ~b2 & ~b3)
                m.AddBoolOr([b1, b2, b3])
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = timeout_s
    s.parameters.num_search_workers = 4
    st = s.Solve(m)
    if st == cp_model.OPTIMAL or st == cp_model.FEASIBLE:
        perm = [0] * N
        for v in range(1, N + 1):
            perm[s.Value(pos[v]) - 1] = v
        return "SAT", perm
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


if __name__ == "__main__":
    from asym_strategy import violates
    for (N, C) in [(44, 2), (45, 2), (79, 3), (80, 3)]:
        t0 = time.time()
        res, perm = solve_cpsat(N, C)
        dt = time.time() - t0
        extra = ""
        if perm:
            assert not violates(tuple(perm)), "model returned an invalid witness!"
            posmap = {v: i + 1 for i, v in enumerate(perm)}
            assert all(posmap[v] <= C * v for v in range(1, N + 1))
            extra = " (witness re-verified)"
        print(f"(N={N}, C={C}): {res}{extra}  [{dt:.1f}s]", flush=True)
