"""map3.py -- exhaustive map of TRIPLE feasibility (W,U,V) for V <= VMAX.

By Lemma S monotonicity, {W,U,V} infeasible => every cut set containing it is
infeasible.  So the triple map controls every in-order block construction:
if Cut(a) is infinite, EVERY triple of its cuts must be feasible.

Output lines:  W U V  SAT/UNSAT/GEOMDEAD
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_eager, verify

VMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60

def main():
    t0 = time.time()
    sat_by_w = {}
    n = 0
    for V in range(4, VMAX + 1):
        for U in range(2, (V + 2) // 3 + 1):
            if V < 3 * U - 2:
                continue
            for W in range(1, U):
                r, info = solve_eager([W, U, V])
                n += 1
                if r == 'SAT':
                    verify([W, U, V], info)
                    sat_by_w.setdefault(W, []).append((U, V))
                    print(f"SAT   {W:3d} {U:3d} {V:4d}", flush=True)
    print(f"# tested {n} triples with V <= {VMAX} in {time.time()-t0:.0f}s")
    print("# max W with a feasible triple, per W:")
    for W in sorted(sat_by_w):
        pts = sat_by_w[W]
        print(f"#   W={W:3d}: {len(pts)} feasible (U,V); U range "
              f"{min(p[0] for p in pts)}..{max(p[0] for p in pts)}")
    if sat_by_w:
        print(f"# LARGEST FIRST CUT with a feasible triple (V<={VMAX}): {max(sat_by_w)}")

if __name__ == "__main__":
    main()
