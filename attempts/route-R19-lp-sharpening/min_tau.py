"""min_tau.py -- exact minimisation of  sum_j tau_j  over increasing-4-AP-free
permutations of [1..N].   tau_j = max_{v<=j} pos(v).

Why: (REPORT.md Prop 2) the CORE-Thm-12 ledger proves LP-inc(C) at board size N iff
   min { sum_j tau_j : sigma inc-4AP-free on [1..N] }  >  C * N(N+1)/2.
So  C_ledger(N) = 2*min_tau(N)/(N(N+1))  is the EXACT ceiling of every ledger-style
argument at board size N, and  limsup_N C_ledger(N)  is the ceiling of the method.

Mode 'free'  : no profile constraint (the honest ceiling of a profile-free demand bound).
Mode 'prof'  : additionally pos(v) <= floor(C v); then the ledger proves LP-inc(C) iff
               the profile-constrained min exceeds C*N(N+1)/2 (or the instance is UNSAT).

Exhaustive brute force cross-checks the CP-SAT optimum for N <= 10.
"""

import sys
from fractions import Fraction
from itertools import permutations

sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
from r19lib import has_inc_4ap, taus, triadic, pos_array

from ortools.sat.python import cp_model


def brute_min_tau(N):
    best = None
    arg = None
    for p in permutations(range(1, N + 1)):
        if has_inc_4ap(p):
            continue
        s = sum(taus(list(p))[1:])
        if best is None or s < best:
            best, arg = s, p
    return best, arg


def cpsat_min_tau(N, C=None, budget=300.0, workers=8, log=False):
    m = cp_model.CpModel()
    if C is None:
        ub = [N] * (N + 1)
    else:
        ub = [0] + [min(N, (C.numerator * v) // C.denominator) for v in range(1, N + 1)]
    pos = [None] + [m.NewIntVar(1, ub[v], f"p{v}") for v in range(1, N + 1)]
    m.AddAllDifferent(pos[1:])
    # no increasing 4-AP
    for e in range(1, (N - 1) // 3 + 1):
        for u in range(1, N - 3 * e + 1):
            bs = []
            for i in range(3):
                b = m.NewBoolVar("")
                m.Add(pos[u + (i + 1) * e] < pos[u + i * e]).OnlyEnforceIf(b)
                bs.append(b)
            m.AddBoolOr(bs)
    tau = [None] + [m.NewIntVar(1, N, f"t{j}") for j in range(1, N + 1)]
    m.Add(tau[1] == pos[1])
    for j in range(2, N + 1):
        m.AddMaxEquality(tau[j], [tau[j - 1], pos[j]])
    m.Minimize(sum(tau[1:]))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    s.parameters.max_time_in_seconds = budget
    s.parameters.log_search_progress = log
    st = s.Solve(m)
    if st == cp_model.OPTIMAL:
        perm = [0] * (N + 1)
        for v in range(1, N + 1):
            perm[s.Value(pos[v])] = v
        return "OPT", int(s.ObjectiveValue()), perm[1:]
    if st == cp_model.FEASIBLE:
        perm = [0] * (N + 1)
        for v in range(1, N + 1):
            perm[s.Value(pos[v])] = v
        return "UB", (int(s.ObjectiveValue()), int(s.BestObjectiveBound())), perm[1:]
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None, None
    return "UNKNOWN", None, None


def verify(perm, val):
    assert sorted(perm) == list(range(1, len(perm) + 1))
    assert not has_inc_4ap(perm), "witness has an increasing 4-AP!"
    assert sum(taus(perm)[1:]) == val, "objective mismatch"


if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or list(range(4, 15))
    print("N    min sum tau   gamma=min/N^2   C_ledger = 2*min/(N(N+1))   triadic sum tau")
    for N in Ns:
        if N <= 9:
            b, arg = brute_min_tau(N)
            st, val, perm = cpsat_min_tau(N)
            assert st == "OPT" and val == b, (N, st, val, b)
            verify(perm, val)
            tag = "brute==cpsat"
        else:
            st, val, perm = cpsat_min_tau(N, budget=300.0)
            if st == "OPT":
                verify(perm, val)
                tag = "cpsat OPT"
            elif st == "UB":
                val, lb = val
                verify(perm, val)
                tag = f"cpsat UB (lb={lb})"
            else:
                print(f"{N:3d}  {st}")
                continue
        tri = sum(taus(triadic(N))[1:])
        print(f"{N:3d}  {val:9d}   {val/N**2:.5f}      {2*val/(N*(N+1)):.5f}"
              f"                {tri:9d}   [{tag}]", flush=True)
