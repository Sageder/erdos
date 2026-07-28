"""plain_profile_cpsat.py — how far do PLAIN (both-orientation) monotone-4-AP-free
permutations of [1..N] survive under a linear displacement profile pos(v) <= C*v?

This is the decisive gate for CORE.md Lemma 6 on the NO side: every contiguous
geometric-block architecture of ratio r induces pos(v) <= r*v (roughly), so extinction
of the profile family at some C would kill all of them at once, while survival to large
N keeps them alive. Currently CERTIFIED plain extinction only reaches C = 1.5 (N = 22);
the asymmetric variant reaches C = 3 (N = 75).

Model: integer position variables pos[v] in [1, min(N, floor(C*v))], AllDifferent, and
for every (x, e) with x+3e <= N two forbidden monotone patterns, encoded with reified
comparison booleans shared between the two patterns (3 bools per AP window, 2 clauses).
No transitivity clauses are needed — this is why CP-SAT scales here where the order
encoding does not.

Any SAT model is decoded and re-verified with the trusted checker in apcheck.py.
UNSAT results are theorems only modulo solver correctness; anything load-bearing must be
re-confirmed by a second engine.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from ortools.sat.python import cp_model
from apcheck import has_monotone_kap_pos


def solve(N, C, timeout_s=600, workers=2):
    m = cp_model.CpModel()
    pos = {}
    for v in range(1, N + 1):
        ub = min(N, int(C * v))
        if ub < 1:
            return "UNSAT", None          # profile itself infeasible
        pos[v] = m.NewIntVar(1, ub, f"p{v}")
    m.AddAllDifferent(list(pos.values()))
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            b = []
            for k in range(3):
                u, w = x + k * e, x + (k + 1) * e
                z = m.NewBoolVar(f"a{x}_{e}_{k}")     # z <=> pos[u] < pos[w]  (ascent)
                m.Add(pos[u] < pos[w]).OnlyEnforceIf(z)
                m.Add(pos[u] > pos[w]).OnlyEnforceIf(z.Not())
                b.append(z)
            m.AddBoolOr([b[0].Not(), b[1].Not(), b[2].Not()])   # no increasing 4-AP
            m.AddBoolOr([b[0], b[1], b[2]])                     # no decreasing 4-AP
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = timeout_s
    s.parameters.num_search_workers = workers
    st = s.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        perm = [0] * N
        for v in range(1, N + 1):
            perm[s.Value(pos[v]) - 1] = v
        assert sorted(perm) == list(range(1, N + 1))
        assert not has_monotone_kap_pos(perm, 4), "solver returned a non-avoider!"
        assert all(s.Value(pos[v]) <= C * v for v in range(1, N + 1))
        return "SAT", perm
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


if __name__ == "__main__":
    Cs = [float(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else ["2", "3", "5"])]
    Ns = [int(x) for x in (sys.argv[2].split(",") if len(sys.argv) > 2 else
                           ["40", "60", "90", "130", "180", "250", "350", "500"])]
    tmo = float(sys.argv[3]) if len(sys.argv) > 3 else 600
    for C in Cs:
        for N in Ns:
            t0 = time.time()
            res, perm = solve(N, C, timeout_s=tmo)
            dt = time.time() - t0
            print(f"plain C={C} N={N}: {res} ({dt:.0f}s)", flush=True)
            if res == "UNSAT":
                print(f"   ==> EXTINCTION: no monotone-4-AP-free permutation of [1..{N}] "
                      f"has pos(v) <= {C}v for all v; inherited for all larger N "
                      f"(restriction principle).", flush=True)
                break
            if res == "UNKNOWN":
                print("   (timeout — inconclusive, stopping this C)", flush=True)
                break
