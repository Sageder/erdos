"""lazy_calib.py — validate the lazy engine (used for big instances) against the
eager engine and against R1's published verdicts on small instances."""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_lazy, verify_witness_full

EXPECT = [
    ([2, 8, 22], 'SAT'), ([4, 16, 54], 'SAT'), ([4, 16, 56], 'UNSAT'),
    ([4, 16, 60], 'UNSAT'), ([4, 16, 68], 'SAT'), ([6, 20, 64], 'UNSAT'),
    ([8, 26, 76], 'SAT'), ([8, 26, 78], 'UNSAT'), ([8, 26, 80], 'UNSAT'),
    ([8, 26, 120], 'UNSAT'), ([8, 26, 130], 'SAT'), ([8, 26, 150], 'SAT'),
    ([8, 26, 160], 'UNSAT'), ([2, 8, 26, 100], 'UNSAT'), ([2, 8, 26, 120], 'UNSAT'),
    ([2, 8, 26, 130], 'SAT'), ([2, 8, 26, 140], 'SAT'), ([2, 8, 26, 160], 'UNSAT'),
    ([5, 25, 125], 'SAT'), ([8, 20, 100], 'UNSAT'), ([7, 20, 100], 'SAT'),
]

if __name__ == "__main__":
    ok = True
    for cuts, exp in EXPECT:
        s = CutSystem(cuts)
        t0 = time.time()
        r, w = solve_lazy(s, solver_name='cadical195', time_cap=2000)
        dt = time.time() - t0
        if r == 'SAT':
            verify_witness_full(cuts, list(w))
        m = "OK " if r == exp else "MISMATCH"
        if r != exp:
            ok = False
        print(f"{m} cuts={cuts} lazy={r} R1={exp} ({dt:.1f}s)", flush=True)
    print("LAZY CALIB", "ALL AGREE" if ok else "DISAGREEMENT", flush=True)
