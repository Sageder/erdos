"""exception_branches.py — the ONLY (W,U,V) triples in the dead zone (U,3U-3] that
the 3-cut forced-chain argument does NOT kill are (W,U,V) = (1, U, U+1) with U odd
(geometry.py, checked for all U <= 200).  The exhaustive DFS in exhaust5.py prunes
with V_next >= 3*V_last - 2, so it would skip cut sequences that use such a step.
Because the exception needs W = 1, it can only occur at the very first step
(V1,V2,V3) = (1, odd, odd+1).  This script covers those branches.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_lazy, verify_witness_full

M = int(sys.argv[1]) if len(sys.argv) > 1 else 300


def feas(cuts, tcap=600):
    s = CutSystem(list(cuts))
    t0 = time.time()
    r, w = solve_lazy(s, solver_name='cadical195', time_cap=tcap)
    if r == 'SAT':
        verify_witness_full(list(cuts), list(w))
    print(f"  {r:9s} {list(cuts)} ({time.time()-t0:.0f}s)", flush=True)
    return r


if __name__ == "__main__":
    found = []
    for U in range(3, 60, 2):
        base = [1, U, U + 1]
        if 9 * (U + 1) - 8 > M:
            break
        if feas(base) == 'UNSAT':
            continue
        for V4 in range(3 * (U + 1) - 2, M + 1):
            if 3 * V4 - 2 > M:
                break
            if feas(base + [V4]) == 'UNSAT':
                continue
            for V5 in range(3 * V4 - 2, M + 1):
                if feas(base + [V4, V5]) != 'UNSAT':
                    found.append(base + [V4, V5])
                    print(f"*** DEPTH-5 FEASIBLE (exception branch): "
                          f"{base + [V4, V5]}", flush=True)
    print(f"# EXCEPTION BRANCHES DONE M={M}: {found}", flush=True)
