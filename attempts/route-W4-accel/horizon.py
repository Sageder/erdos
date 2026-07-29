"""horizon.py -- the HORIZON-EXTENDED cut system for a whole cut set.

For a cut set S = {V_1<...<V_k} and horizon M >= V_k, the system is
   blocks [1,V_1],(V_1,V_2],...,(V_{k-1},V_k],(V_k,M]  laid out in this order,
   C1 : no monotone 4-AP among [1..M] (both orientations),
   C2 : forbid x < x+d < x+2d whenever x+2d <= V_k and x+3d > M.
It is NECESSARY for every monotone-4-AP-free permutation of N whose cut set
contains S, and it is MONOTONE in M.  Route R1 used only M = V_k; taking M > V_k
is strictly stronger and needs NO guess about the next cut.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def test(cuts, M, cap=900, verbose=True):
    t0 = time.time()
    S = wsys.Sys(cuts, M)
    v, o = wsys.solve_lazy(S, time_cap=cap, tag=f"{cuts}@{M}")
    if v == 'GEOM_DEAD':
        v = 'UNSAT'
    if v == 'SAT':
        wsys.verify(cuts, M, o)
        v = 'SAT*'
    if verbose:
        print(f"   S={list(cuts)} M={M} -> {v} [{time.time()-t0:.0f}s]", flush=True)
    return v


if __name__ == '__main__':
    job = sys.argv[1]
    if job == 'chain90':
        print("## the mission's depth-5 accelerating survivors, HORIZON-EXTENDED")
        for V5 in (28, 90, 91, 92):
            for M in (V5, int(1.5 * V5), 2 * V5, 3 * V5 - 2):
                if test((1, 2, 4, 10, V5), M) == 'UNSAT':
                    break
    elif job == 'w10':
        print("## pair {10,U}: push the horizon")
        for U in (31, 34, 40, 46):
            for M in (3 * U - 2, 4 * U, 5 * U, 6 * U, 8 * U):
                if test((10, U), M) in ('UNSAT', 'TIME_CAP'):
                    break
    elif job == 'v5map':
        print("## which V5 continue [1,2,4,10] once the horizon is extended?")
        for V5 in range(28, 141):
            r = test((1, 2, 4, 10, V5), 3 * V5 - 2, cap=400, verbose=False)
            print(f"   V5={V5} M={3*V5-2}: {r}", flush=True)
