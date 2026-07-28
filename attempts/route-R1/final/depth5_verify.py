"""depth5_verify.py — INDEPENDENT re-decision of the depth-5 points, plus a scan
for a moved island.

Engines used (all on the independently written encoder cutsys.py):
  L1 = my lazy-transitivity CEGAR + cadical195
  L2 = my lazy-transitivity CEGAR + glucose42
Lazy UNSAT is SOUND: every clause fed to the solver is either an instance of
C1/C2 (necessary for the object) or a transitivity instance (valid for any linear
order), so the solved formula is a SUBSET of the true constraint system; UNSAT of
a subset implies UNSAT of the whole.
SAT results are re-verified end-to-end with the trusted checker apcheck.py.
"""
import sys, time, json
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_lazy, verify_witness_full


def decide(cuts, solvers=('cadical195',), time_cap=5400, verbose=True, window=None):
    out = {}
    for sname in solvers:
        s = CutSystem(cuts, window=window)
        t0 = time.time()
        r, w = solve_lazy(s, solver_name=sname, time_cap=time_cap, verbose=verbose,
                          tag=f"{cuts}/{sname}")
        dt = time.time() - t0
        out[sname] = (r, dt)
        if r == 'SAT' and window is None:
            # rebuild full witness sequence (blocks in order, in-block order from w)
            seq = list(w)
            verify_witness_full(cuts, seq)
            out['witness_verified'] = True
        print(f"cuts={cuts} window={window} [{sname}] -> {r} ({dt:.0f}s)", flush=True)
    return out


if __name__ == "__main__":
    which = sys.argv[1]
    solvers = tuple(sys.argv[2].split(',')) if len(sys.argv) > 2 else ('cadical195',)
    JOBS = {
        # (a) re-verify the published depth-5 UNSATs
        'reverify': [[2, 8, 26, 140, v] for v in (800, 780, 740, 760, 700)],
        'pure5': [[5, 25, 125, 625]],
        # (b) does the island MOVE?  wide V5 scan for prefix {2,8,26,140}
        'scan_wide': [[2, 8, 26, 140, v] for v in
                      (430, 460, 500, 560, 620, 660, 680, 850, 900, 950, 1000, 1100)],
        # (c) other depth-4 prefixes, island centres  (~[4.8,5.8] * V4)
        'other4': [[2, 8, 26, 130, v] for v in (630, 680, 730)] +
                  [[2, 8, 26, 150, v] for v in (720, 780, 840)],
        'pure5b': [[5, 25, 125, 600], [5, 25, 125, 650], [5, 25, 125, 700],
                   [5, 25, 125, 560], [5, 25, 125, 750]],
    }
    for cuts in JOBS[which]:
        decide(cuts, solvers=solvers)
    print(f"DONE {which}", flush=True)
