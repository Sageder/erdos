"""lp_threshold.py — the LP-inc threshold C*_inc: SAT scan + UNSAT certificates.

Definitions (see PROOFS.md section 7).  LP-inc(C) := "every permutation a of N with
pos(v) <= C*v for all v contains an INCREASING monotone 4-AP".
CORE.md Theorem 12 proves LP-inc(C) for all C < 9/8.  Route R6's triadic example
disproves LP-inc(C) for all C >= 3 (pos(v) <= 3v-1, no increasing 4-AP).

Bridge to finite objects (PROOFS.md Prop 7.2): an infinite witness at C exists
iff for EVERY N there is a permutation of [1..N] with pos(v) <= floor(C*v) and no
increasing 4-AP.  Hence a single UNSAT at (C, N) proves LP-inc(C') for all C' <= C,
rigorously modulo the CP-SAT solver's UNSAT answer (machine-assisted, flagged as such).

This script:
  1. for each N in SCAN_NS, finds min-grid C (grid k/24) with a SAT witness;
  2. emits UNSAT certificates for the largest grid C that is UNSAT at each N;
  3. cross-validates each SAT witness (checker from r6lib: really no increasing 4-AP,
     really pos(v) <= floor(C*v)).
"""

import sys
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/attempts/route-R6")
from r6lib import incr_4aps
from ortools.sat.python import cp_model


def solve_lp_inc(n, C, budget=120.0):
    """SAT: exists permutation of [1..n], pos(v) <= floor(C v), no increasing 4-AP.
    Returns (status_str, witness_or_None). C is a Fraction."""
    m = cp_model.CpModel()
    pos = [None] + [
        m.NewIntVar(1, min(n, (C.numerator * v) // C.denominator), f"p{v}")
        for v in range(1, n + 1)
    ]
    m.AddAllDifferent(pos[1:])
    for e in range(1, (n - 1) // 3 + 1):
        for u in range(1, n - 3 * e + 1):
            bs = []
            for i in range(3):
                b = m.NewBoolVar(f"b{u}_{e}_{i}")
                m.Add(pos[u + (i + 1) * e] < pos[u + i * e]).OnlyEnforceIf(b)
                bs.append(b)
            m.AddBoolOr(bs)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 2
    s.parameters.max_time_in_seconds = budget
    st = s.Solve(m)
    if st == cp_model.OPTIMAL or st == cp_model.FEASIBLE:
        posv = [0] + [s.Value(pos[v]) for v in range(1, n + 1)]
        perm = [0] * (n + 1)
        for v in range(1, n + 1):
            perm[posv[v]] = v
        return "SAT", perm[1:]
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


def verify_witness(perm, C):
    """Independent check: perm (list, perm[i]=value at position i+1) has no increasing
    4-AP and pos(v) <= floor(C v)."""
    n = len(perm)
    assert sorted(perm) == list(range(1, n + 1))
    posv = {v: i + 1 for i, v in enumerate(perm)}
    for v in range(1, n + 1):
        assert posv[v] <= (C.numerator * v) // C.denominator, (v, posv[v])
    assert not incr_4aps(perm, limit=1), "increasing 4-AP present!"


GRID = [Fraction(24 + k, 24) for k in range(0, 49)]  # 1, 25/24, ..., 3

if __name__ == "__main__":
    SCAN_NS = [int(x) for x in sys.argv[1:]] or [12, 16, 20, 24, 28, 32, 40, 48]
    print("grid step 1/24; per-solve budget 120 s", flush=True)
    for n in SCAN_NS:
        # binary search on the grid: find least SAT index
        lo, hi = 0, len(GRID) - 1  # GRID[hi]=3 must be SAT (triadic restriction exists)
        st3, w3 = solve_lp_inc(n, GRID[hi])
        assert st3 == "SAT", (n, "C=3 should be SAT")
        verify_witness(w3, GRID[hi])
        results = {hi: "SAT"}
        while lo < hi:
            mid = (lo + hi) // 2
            st, w = solve_lp_inc(n, GRID[mid])
            results[mid] = st
            if st == "SAT":
                verify_witness(w, GRID[mid])
                hi = mid
            elif st == "UNSAT":
                lo = mid + 1
            else:  # UNKNOWN: treat as SAT-side to stay conservative in the report
                print(f"  N={n}: C={GRID[mid]} UNKNOWN (budget)", flush=True)
                hi = mid
        cmin = GRID[hi]
        # largest UNSAT below, if adjacent probe was made; re-probe to be sure
        cert = None
        if hi > 0:
            st, _ = solve_lp_inc(n, GRID[hi - 1])
            if st == "UNSAT":
                cert = GRID[hi - 1]
        print(
            f"N={n}: min grid C with SAT witness = {cmin} = {float(cmin):.4f}; "
            f"largest adjacent UNSAT C = {cert} "
            f"[UNSAT at (C,N) proves LP-inc(C'), all C'<=C, machine-assisted]",
            flush=True,
        )
    print("SCAN COMPLETE", flush=True)
