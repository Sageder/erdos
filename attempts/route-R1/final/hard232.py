"""hard232.py — settle the single undecided depth-6 point {1,2,4,10,40,232}
and map its neighbourhood.  Eager transitivity on the top block (192 values,
~7e6 clauses) removes the CEGAR loop entirely."""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_pysat, solve_lazy, verify_witness_full
from calib import extract

MODE = sys.argv[1]

if MODE == 'nbhd':
    for V6 in (226, 228, 230, 231, 233, 234, 236, 240, 250, 260, 280):
        cuts = [1, 2, 4, 10, 40, V6]
        s = CutSystem(cuts)
        t0 = time.time()
        r, w = solve_lazy(s, solver_name='cadical195', time_cap=1800)
        if r == 'SAT':
            verify_witness_full(cuts, list(w))
        print(f"{r:9s} {cuts} ({time.time()-t0:.0f}s)", flush=True)

elif MODE == 'eager':
    cuts = [int(x) for x in sys.argv[2].split(',')]
    s = CutSystem(cuts)
    t0 = time.time()
    cls, dead = s.clauses(transitivity=True)
    print(f"# {cuts}: {s.nvars} vars, {len(cls)} clauses, built in "
          f"{time.time()-t0:.0f}s", flush=True)
    r, model = solve_pysat(cls, s.nvars, solver_name='cadical195')
    print(f"EAGER {cuts} -> {r} ({time.time()-t0:.0f}s)", flush=True)
    if r == 'SAT':
        w = extract(s, {abs(l): (l > 0) for l in model})
        verify_witness_full(cuts, w)
        print(f"*** WITNESS VERIFIED: {w}", flush=True)
