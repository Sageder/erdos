"""depth6_probe2.py — depth-6 probes on (i) the second depth-5 family [1,3,4,10,V5]
and (ii) LARGER V5 in the family [1,2,4,10,V5] (bigger top block = more room?)."""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_lazy, verify_witness_full


def feas(cuts, tcap=1500):
    s = CutSystem(list(cuts))
    t0 = time.time()
    r, w = solve_lazy(s, solver_name='cadical195', time_cap=tcap)
    if r == 'SAT':
        verify_witness_full(list(cuts), list(w))
        print(f"*** SAT {list(cuts)} ({time.time()-t0:.0f}s) [verified]", flush=True)
    else:
        print(f"    {r} {list(cuts)} ({time.time()-t0:.0f}s)", flush=True)
    return r


if __name__ == "__main__":
    for base in ([1, 3, 4, 10, 28], [1, 3, 4, 10, 40], [1, 3, 4, 10, 60],
                 [1, 3, 4, 10, 90]):
        V5 = base[-1]
        for V6 in sorted(set([3 * V5 - 2, 3 * V5 - 1, 3 * V5, 3 * V5 + 4, 4 * V5,
                              5 * V5, int(5.3 * V5), 6 * V5])):
            feas(base + [V6])
    for V5 in (120, 150, 200):
        base = [1, 2, 4, 10, V5]
        if feas(base) == 'UNSAT':
            continue
        for V6 in sorted(set([3 * V5 - 2, 3 * V5 - 1, 3 * V5, 3 * V5 + 4, 4 * V5,
                              int(5.3 * V5), 6 * V5])):
            feas(base + [V6])
    print("DEPTH6 PROBE2 DONE", flush=True)
