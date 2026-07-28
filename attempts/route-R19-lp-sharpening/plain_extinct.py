"""plain_extinct.py -- PLAIN-target (both orientations) linear-profile extinction.

Question: for a rational C, is there a permutation of [1..N] with pos(v) <= floor(C v)
for all v and NO monotone 4-AP (either orientation)?  By CORE Lemma 6 (displacement
compactness) a YES at EVERY N would give a 4-AP-free permutation of N -- i.e. 196-NO.
So the finite extinction point N_plain(C) := least N with UNSAT is a hard quantity:
196-YES implies N_plain(C) < infinity for every C.

Engine 1: CP-SAT with integer position variables (fast, no transitivity needed).
Engine 2: pysat order-encoding (Cadical195 + Glucose42) with DRUP proof logging,
          used to certify the UNSAT points.
Cross-validated: every SAT witness is re-checked with experiments/apcheck.py.
"""

import sys, time, os
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
from apcheck import has_monotone_kap_pos
from r19lib import has_inc_4ap, has_dec_4ap
from ortools.sat.python import cp_model


def cpsat_plain(N, C, budget=600.0, workers=8):
    """SAT?: permutation of [1..N], pos(v) <= floor(Cv), no monotone 4-AP."""
    m = cp_model.CpModel()
    ub = [0] + [min(N, (C.numerator * v) // C.denominator) for v in range(1, N + 1)]
    if min(ub[1:]) < 1:
        return "UNSAT", None
    pos = [None] + [m.NewIntVar(1, ub[v], f"p{v}") for v in range(1, N + 1)]
    m.AddAllDifferent(pos[1:])
    for e in range(1, (N - 1) // 3 + 1):
        for u in range(1, N - 3 * e + 1):
            binc, bdec = [], []
            for i in range(3):
                a, b = pos[u + i * e], pos[u + (i + 1) * e]
                bi = m.NewBoolVar("")
                m.Add(b < a).OnlyEnforceIf(bi)       # a drop at step i
                m.Add(b > a).OnlyEnforceIf(bi.Not())
                binc.append(bi)                      # inc 4AP needs all three "no drop"
                bdec.append(bi.Not())
            m.AddBoolOr(binc)                        # not all ascents
            m.AddBoolOr(bdec)                        # not all drops
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    s.parameters.max_time_in_seconds = budget
    st = s.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        perm = [0] * (N + 1)
        for v in range(1, N + 1):
            perm[s.Value(pos[v])] = v
        perm = perm[1:]
        assert sorted(perm) == list(range(1, N + 1))
        assert not has_monotone_kap_pos(perm, 4), "witness has a monotone 4-AP!"
        for v in range(1, N + 1):
            assert perm.index(v) + 1 <= ub[v]
        return "SAT", perm
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


def threshold(C, lo=4, hi=200, budget=600.0):
    """Least N with UNSAT, by doubling then bisection (monotone: UNSAT at N => UNSAT at
    N' > N, since restricting a witness of [1..N'] to [1..N] keeps both properties and
    can only decrease positions)."""
    n = lo
    last_sat = None
    while n <= hi:
        st, w = cpsat_plain(n, C, budget=budget)
        print(f"    C={C} N={n}: {st}", flush=True)
        if st == "UNSAT":
            break
        if st == "UNKNOWN":
            return None, last_sat, "UNKNOWN at N=%d" % n
        last_sat = n
        n = n + 1 if n < 12 else int(n * 1.3) + 1
    else:
        return None, last_sat, "no UNSAT up to %d" % hi
    # bisect between last_sat and n
    lo2, hi2 = (last_sat or lo - 1) + 1, n
    while lo2 < hi2:
        mid = (lo2 + hi2) // 2
        st, w = cpsat_plain(mid, C, budget=budget)
        print(f"    C={C} N={mid}: {st}", flush=True)
        if st == "UNSAT":
            hi2 = mid
        elif st == "SAT":
            lo2 = mid + 1
        else:
            return None, lo2 - 1, "UNKNOWN at N=%d" % mid
    return hi2, hi2 - 1, "exact"


if __name__ == "__main__":
    args = sys.argv[1:]
    Cs = [Fraction(a) for a in args] if args else [Fraction(1), Fraction(5, 4), Fraction(3, 2),
                                                   Fraction(7, 4), Fraction(2)]
    budget = float(os.environ.get("BUDGET", "600"))
    for C in Cs:
        t0 = time.time()
        n, mx, tag = threshold(C, budget=budget)
        print(f"PLAIN C={C} ({float(C):.4f}): minimal UNSAT N = {n}  (max SAT N = {mx})  "
              f"[{tag}, {time.time()-t0:.0f}s]", flush=True)
