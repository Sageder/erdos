"""toprelax.py — verify R1's depth-5 island UNSATs via the TOP-BLOCK RELAXATION.

Keep only the clauses of the full system all of whose free literals are order
variables of the top block (V_{k-1}, V_k]; cross-block order is a layout constant, so
those clauses become units/binaries/ternaries on top-block variables.  Dropping the
remaining clauses can only make the system easier, so UNSAT of this relaxation
implies UNSAT of the full stage system, hence: no monotone-4-AP-free permutation of N
has all of V_1..V_k as cuts.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_lazy

if __name__ == "__main__":
    for c in sys.argv[1].split(';'):
        cuts = [int(x) for x in c.split(',')]
        win = (cuts[-2] + 1, cuts[-1])
        s = CutSystem(cuts, window=win)
        t0 = time.time()
        r, w = solve_lazy(s, solver_name='cadical195', time_cap=3000, verbose=True,
                          tag=f"top{cuts}")
        print(f"TOPRELAX cuts={cuts} window={win} -> {r} ({time.time()-t0:.0f}s)"
              + ("   [=> FULL SYSTEM UNSAT]" if r == 'UNSAT' else
                 "   [inconclusive: relaxation is satisfiable]"), flush=True)
