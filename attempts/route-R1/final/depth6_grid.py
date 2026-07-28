"""depth6_grid.py — is there ANY feasible 6-element cut set?

The depth-5 corridor found here is {1,2,4,10,V5} with V5 in [28, >=98].  For a
sample of V5 we test V6 across the whole plausible range: the shoulder 3V5-2 and its
neighbours, the notch, the island ~[4.8,5.8]V5, and beyond.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_lazy, verify_witness_full

def feas(cuts, tcap=900):
    s = CutSystem(list(cuts))
    t0 = time.time()
    r, w = solve_lazy(s, solver_name='cadical195', time_cap=tcap)
    dt = time.time() - t0
    if r == 'SAT':
        verify_witness_full(list(cuts), list(w))
        print(f"*** SAT {list(cuts)} ({dt:.0f}s) [witness verified]", flush=True)
    else:
        print(f"    {r} {list(cuts)} ({dt:.0f}s)", flush=True)
    return r

if __name__ == "__main__":
    V5s = [int(x) for x in sys.argv[1].split(',')]
    for V5 in V5s:
        base = [1, 2, 4, 10, V5]
        pts = sorted(set([3 * V5 - 2, 3 * V5 - 1, 3 * V5, 3 * V5 + 3, 3 * V5 + 8,
                          int(3.5 * V5), 4 * V5, int(4.5 * V5), 5 * V5,
                          int(5.3 * V5), int(5.8 * V5), 6 * V5, 7 * V5]))
        print(f"--- V5={V5}: {len(pts)} candidate V6", flush=True)
        for V6 in pts:
            feas(base + [V6])
    print("DEPTH6 GRID DONE", flush=True)
