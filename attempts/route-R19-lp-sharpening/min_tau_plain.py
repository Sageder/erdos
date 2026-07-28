"""min_tau_plain.py -- the ledger ceiling for the PLAIN (both-orientation) target.

Same reduction as min_tau.py: the CORE-Thm-12 ledger
    N(N+1)/2 = sum_w pos(w) <= C * sum_w m(w) = C*(N + N^2 - sum_j tau_j)
uses NO orientation assumption, so it applies verbatim to plain avoiders.  Its exact
ceiling at board size N is
    C_ledger(N) = N(N+1) / (2 (N^2 + N - S(N))),
    S(N) = min { sum_j tau_j : sigma a monotone-4-AP-free permutation of [1..N] }.
Since the plain class is smaller than the increasing-only class, S_plain >= S_inc and
the plain ledger ceiling is at least the increasing-only one.
"""

import sys, os
from fractions import Fraction
from itertools import permutations

sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
from apcheck import has_monotone_kap_pos
from r19lib import taus, triadic, has_inc_4ap, has_dec_4ap
from ortools.sat.python import cp_model


def brute(N):
    best = None
    for p in permutations(range(1, N + 1)):
        if has_monotone_kap_pos(p, 4):
            continue
        s = sum(taus(list(p))[1:])
        if best is None or s < best:
            best = s
    return best


def cpsat(N, budget=300.0, workers=8):
    m = cp_model.CpModel()
    pos = [None] + [m.NewIntVar(1, N, f"p{v}") for v in range(1, N + 1)]
    m.AddAllDifferent(pos[1:])
    for e in range(1, (N - 1) // 3 + 1):
        for u in range(1, N - 3 * e + 1):
            binc, bdec = [], []
            for i in range(3):
                a, b = pos[u + i * e], pos[u + (i + 1) * e]
                bi = m.NewBoolVar("")
                m.Add(b < a).OnlyEnforceIf(bi)
                m.Add(b > a).OnlyEnforceIf(bi.Not())
                binc.append(bi)
                bdec.append(bi.Not())
            m.AddBoolOr(binc)
            m.AddBoolOr(bdec)
    tau = [None] + [m.NewIntVar(1, N, f"t{j}") for j in range(1, N + 1)]
    m.Add(tau[1] == pos[1])
    for j in range(2, N + 1):
        m.AddMaxEquality(tau[j], [tau[j - 1], pos[j]])
    m.Minimize(sum(tau[1:]))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    s.parameters.max_time_in_seconds = budget
    st = s.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        perm = [0] * (N + 1)
        for v in range(1, N + 1):
            perm[s.Value(pos[v])] = v
        perm = perm[1:]
        assert not has_monotone_kap_pos(perm, 4)
        assert sum(taus(perm)[1:]) == int(s.ObjectiveValue())
        return ("OPT" if st == cp_model.OPTIMAL else "UB",
                int(s.ObjectiveValue()), int(s.BestObjectiveBound()), perm)
    return ("UNSAT" if st == cp_model.INFEASIBLE else "UNKNOWN", None, None, None)


def C_ledger(N, S):
    return Fraction(N * (N + 1), 2 * (N * N + N - S))


if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or [8, 12, 16, 20, 24, 28, 32, 36, 40]
    budget = float(os.environ.get("BUDGET", "300"))
    print("PLAIN target.  N   min sum tau   gamma   C_ledger(N) (exact)")
    for N in Ns:
        st, val, lb, perm = cpsat(N, budget=budget)
        if st == "UNKNOWN":
            print(f"{N:3d}  UNKNOWN"); continue
        if N <= 9:
            assert val == brute(N), (N, val, brute(N))
        rng = "" if st == "OPT" else f"  [UB only; lb={lb} -> C_ledger >= {float(C_ledger(N,lb)):.4f}]"
        print(f"{N:3d}  {val:8d}   {val/N**2:.5f}   {float(C_ledger(N,val)):.5f} = {C_ledger(N,val)}"
              f"   [{st}]{rng}", flush=True)
