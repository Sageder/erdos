"""lowprofile.py -- route R22 next-step probe: the LOWER profile pos(v) >= gamma*v.

WHY.  A delay-only class architecture (c = floor(log_b v) + t with t >= 0) with a
geometric fibre design |F_j| >= c1 b^j satisfies, for every value v,

    pos(v) > S_{c(v)-1} >= S_{m(v)-1} >= c1 (b^{m(v)} - 1)/(b-1) >= c1 (v/b - 1)/(b-1),

i.e.  pos(v) >= gamma v - O(1)  with  gamma = c1 / (b(b-1))  (gamma = 1/b when the fibres
are full blocks).  So the whole delay-only family lives inside the LOWER-profile family
{ pos(v) >= gamma v }.  Unlike the upper profiles studied so far (CORE Remark 17), this
family is NOT hit by the coarsening triviality of Remark 31(b): by Lemma R22-0 the
geometric coarsening of a finite avoider satisfies t >= 0 only for ratio-b block layouts.

WHAT.  Extinction thresholds N*(gamma) := least N with no monotone-4-AP-free permutation
of [1..N] satisfying pos(v) >= ceil(gamma v) for all v.  Exact integer model in CP-SAT;
every SAT model is re-verified with the trusted experiments/apcheck.py, and every UNSAT
relied on is re-checked with a second encoding (SAT over order variables + cardinality).
"""

import sys, time
from fractions import Fraction
from ortools.sat.python import cp_model

sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos                              # noqa: E402


def solve_lower(N, gamma, time_limit=120.0, workers=8):
    """gamma is a Fraction.  Returns ('SAT', perm) / ('UNSAT', None) / ('UNKNOWN', None)."""
    mdl = cp_model.CpModel()
    lows = [0] * (N + 1)
    p = [None] * (N + 1)
    for v in range(1, N + 1):
        lo = -(-(gamma.numerator * v) // gamma.denominator)      # ceil(gamma v)
        lo = max(1, min(lo, N))
        lows[v] = lo
        p[v] = mdl.NewIntVar(lo, N, f"p{v}")
    mdl.AddAllDifferent(p[1:])
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            ys = []
            for k in range(3):
                u, w = x + k * e, x + (k + 1) * e
                y = mdl.NewBoolVar(f"y{u}_{w}")
                mdl.Add(p[u] < p[w]).OnlyEnforceIf(y)
                mdl.Add(p[u] > p[w]).OnlyEnforceIf(y.Not())
                ys.append(y)
            mdl.AddBoolOr([y.Not() for y in ys])
            mdl.AddBoolOr(ys)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_search_workers = workers
    st = s.Solve(mdl)
    if st == cp_model.INFEASIBLE:
        return 'UNSAT', None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        pos = {v: s.Value(p[v]) for v in range(1, N + 1)}
        perm = [0] * N
        for v, i in pos.items():
            perm[i - 1] = v
        assert sorted(perm) == list(range(1, N + 1)), "positions not a permutation"
        assert all(pos[v] >= lows[v] for v in range(1, N + 1))
        assert not has_monotone_kap_pos(perm, 4), "model is not an avoider!"
        return 'SAT', perm
    return 'UNKNOWN', None


if __name__ == "__main__":
    gammas = [Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2),
              Fraction(3, 5), Fraction(2, 3), Fraction(3, 4)]
    Ns = [int(x) for x in (sys.argv[1].split(',') if len(sys.argv) > 1 else
                           ['20', '40', '60', '90', '130'])]
    for g in gammas:
        line = f"gamma={str(g):>4s}: "
        for N in Ns:
            t0 = time.time()
            r, perm = solve_lower(N, g, time_limit=90.0)
            line += f" N={N}:{r}({time.time()-t0:.0f}s)"
            if r != 'SAT':
                break
        print(line, flush=True)
