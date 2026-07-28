"""scan.py — FULL-INTEGER scan of the next cut after a fixed feasible prefix.

R1 sampled the next-cut axis on a coarse grid (steps of 10-20).  The depth-4 data
shows the feasible set can be a SINGLE integer (e.g. {2,8,22,64} is SAT while 65 is
UNSAT), so a coarse grid can miss corridors entirely.  This scans every integer.

usage:  python3 scan.py "2,8,22,64" LO HI [solver]
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_lazy, verify_witness_full

if __name__ == "__main__":
    prefix = [int(x) for x in sys.argv[1].split(',')]
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    solver = sys.argv[4] if len(sys.argv) > 4 else 'cadical195'
    tcap = float(sys.argv[5]) if len(sys.argv) > 5 else 1200.0
    print(f"# scan prefix={prefix} next in [{lo},{hi}] solver={solver}", flush=True)
    sats = []
    for V in range(lo, hi + 1):
        cuts = prefix + [V]
        s = CutSystem(cuts)
        t0 = time.time()
        r, w = solve_lazy(s, solver_name=solver, time_cap=tcap)
        dt = time.time() - t0
        if r == 'SAT':
            verify_witness_full(cuts, list(w))
            sats.append(V)
            print(f"SAT   {cuts}  ({dt:.1f}s)  [witness verified]", flush=True)
        elif r == 'UNSAT':
            print(f"unsat {cuts}  ({dt:.1f}s)", flush=True)
        else:
            print(f"{r} {cuts}  ({dt:.1f}s)", flush=True)
    print(f"# SCAN DONE prefix={prefix} range=[{lo},{hi}] SAT points: {sats}", flush=True)
