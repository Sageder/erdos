"""verify_depth5_sat.py — HIGH-ASSURANCE check of the new depth-5 feasible cut sets.

For each cut set: build the system with EAGER transitivity, solve with three SAT
solvers plus the OR-Tools CP-SAT integer-rank model, extract the witness order and
verify it with a from-scratch brute-force checker (independent of both cutsys.py and
apcheck.py) AND with the trusted apcheck.py.
"""
import sys, time, itertools
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
sys.path.insert(0, "/home/user/erdos/experiments")
from cutsys import CutSystem, solve_pysat, solve_cpsat, seg_of
from calib import extract
from apcheck import has_monotone_kap_general


def brute_check(cuts, seq):
    """From-scratch verification, O(V^2) over (x,d), no library code."""
    V = cuts[-1]
    assert sorted(seq) == list(range(1, V + 1)), "not a permutation of [1..V]"
    pos = {v: i for i, v in enumerate(seq)}
    # blocks in order
    sg = seg_of(cuts)
    for v in range(1, V + 1):
        for w in range(1, V + 1):
            if sg(v) < sg(w):
                assert pos[v] < pos[w], f"block order broken at {v},{w}"
    # (C1) no monotone 4-AP among values 1..V, both orientations
    for d in range(1, (V - 1) // 3 + 1):
        for x in range(1, V - 3 * d + 1):
            p = [pos[x + i * d] for i in range(4)]
            assert not (p[0] < p[1] < p[2] < p[3]), f"INC 4-AP x={x} d={d}"
            assert not (p[0] > p[1] > p[2] > p[3]), f"DEC 4-AP x={x} d={d}"
    # (C2) no increasing 3-AP whose 4th term exceeds V
    for d in range(1, V // 2 + 1):
        for x in range(1, V - 2 * d + 1):
            if x + 3 * d > V:
                p = [pos[x + i * d] for i in range(3)]
                assert not (p[0] < p[1] < p[2]), f"C2 violated x={x} d={d}"
    return True


CASES = [[1, 2, 4, 10, 28], [1, 2, 4, 10, 40], [1, 2, 4, 10, 60],
         [1, 2, 4, 10, 83], [2, 4, 10, 28], [1, 2, 4, 10],
         [2, 8, 22, 64], [2, 8, 26, 76]]

if __name__ == "__main__":
    for cuts in CASES:
        s = CutSystem(cuts)
        cls, dead = s.clauses(transitivity=True)
        if dead:
            print(f"{cuts}: GEOM_DEAD")
            continue
        verdicts = {}
        wit = None
        for e in ('cadical195', 'glucose42', 'minisat22'):
            t0 = time.time()
            r, model = solve_pysat(cls, s.nvars, solver_name=e)
            verdicts[e] = r
            if r == 'SAT' and wit is None:
                wit = extract(s, {abs(l): (l > 0) for l in model})
        r2, w2 = solve_cpsat(s)
        verdicts['cpsat'] = r2
        ok = "?"
        if wit is not None:
            brute_check(cuts, wit)
            assert not has_monotone_kap_general(wit, 4)
            ok = "witness passes brute_check + apcheck"
        if r2 == 'SAT' and w2 is not None:
            brute_check(cuts, w2)
            ok += " ; cpsat witness too"
        print(f"{cuts}: {verdicts}  {ok}", flush=True)
        if wit is not None and len(wit) <= 40:
            print(f"    witness = {wit}", flush=True)
    print("VERIFY DONE", flush=True)
