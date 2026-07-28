"""shoulder.py — the corridor R1 never pushed: the ratio-3 SHOULDER.

R1's window law after cuts (V1,V2):  geometry-dead (V2, 3V2-3], then a thin SAT
"shoulder" starting at 3V2-2, then an UNSAT notch ~[3.2,4.35]V2, then the SAT island
~[4.8,5.8]V2.  R1 pushed only the ISLAND to depth 4/5 (V4 ~ 140, V5 ~ 700-800).
The shoulder is MUCH cheaper to iterate (ratio 3 instead of 5), so deep shoulder
chains are within reach: 2,8,22,64,190,568...

Every verdict here uses the independent encoder cutsys.py; SAT witnesses are
re-verified end-to-end with experiments/apcheck.py.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_lazy, verify_witness_full

CACHE = {}


def feas(cuts, time_cap=2400, solver='cadical195', verbose=False):
    key = tuple(cuts)
    if key in CACHE:
        return CACHE[key][0]
    s = CutSystem(list(cuts))
    t0 = time.time()
    r, w = solve_lazy(s, solver_name=solver, time_cap=time_cap, verbose=verbose,
                      tag=str(list(cuts)))
    dt = time.time() - t0
    if r == 'SAT':
        verify_witness_full(list(cuts), list(w))
    CACHE[key] = (r, dt, w if r == 'SAT' else None)
    print(f"  cuts={list(cuts)} -> {r} ({dt:.0f}s)", flush=True)
    return r


if __name__ == "__main__":
    job = sys.argv[1]

    if job == 'depth4_shoulder':
        # shoulder V4 = 3*V3-2 and neighbours, for several depth-3 SAT prefixes
        for pre in ([2, 8, 22], [2, 8, 26], [2, 8, 30], [2, 8, 36], [4, 12, 34],
                    [2, 26, 76], [8, 26, 76]):
            V3 = pre[-1]
            print(f"--- prefix {pre}: shoulder base 3V3-2 = {3*V3-2}", flush=True)
            for V4 in (3 * V3 - 2, 3 * V3 - 1, 3 * V3, 3 * V3 + 2, 3 * V3 + 6,
                       3 * V3 + 12):
                feas(pre + [V4])

    elif job == 'depth5_shoulder':
        cands = [c for c in sys.argv[2].split(';')]
        for c in cands:
            cuts = [int(x) for x in c.split(',')]
            V = cuts[-1]
            print(f"--- prefix {cuts}: shoulder base {3*V-2}", flush=True)
            for V5 in (3 * V - 2, 3 * V - 1, 3 * V, 3 * V + 2, 3 * V + 6, 3 * V + 12):
                feas(cuts + [V5])

    elif job == 'custom':
        for c in sys.argv[2].split(';'):
            cuts = [int(x) for x in c.split(',')]
            feas(cuts, verbose=True)

    print(f"DONE {job}", flush=True)
