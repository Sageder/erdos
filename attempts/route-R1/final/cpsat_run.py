"""cpsat_run.py — decide cut sets with the OR-Tools CP-SAT integer-rank model.

Different paradigm from the SAT/CEGAR engine: within-block order is carried by
integer rank variables with AllDifferent, so transitivity is structural and there is
no CEGAR loop at all.  Good for the instances where lazy transitivity stalls.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_cpsat, verify_witness_full

if __name__ == "__main__":
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 3000.0
    nw = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    for c in sys.argv[1].split(';'):
        cuts = [int(x) for x in c.split(',')]
        s = CutSystem(cuts)
        t0 = time.time()
        r, w = solve_cpsat(s, nworkers=nw, tlimit=tl)
        dt = time.time() - t0
        extra = ""
        if r == 'SAT':
            verify_witness_full(cuts, list(w))
            extra = " [witness verified with apcheck]"
        print(f"CPSAT cuts={cuts} -> {r} ({dt:.0f}s){extra}", flush=True)
        if r == 'SAT' and len(w) <= 60:
            print(f"   witness = {w}", flush=True)
