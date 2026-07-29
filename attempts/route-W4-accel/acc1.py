"""acc1.py -- (i) confirm the depth-5 accelerating survivors, (ii) map the feasible
V5 window after the prefix [1,2,4,10], (iii) reduce each survivor to its top triple.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def decide(cuts, M=None, cap=900):
    S = wsys.Sys(cuts, M)
    n = (M or cuts[-1])
    v, o = (wsys.solve_eager(S) if n <= 110 else wsys.solve_lazy(S, time_cap=cap))
    if v == 'GEOM_DEAD':
        return 'UNSAT', None
    if v == 'SAT':
        wsys.verify(cuts, n, o)
    return v, o


if __name__ == '__main__':
    print("# depth-5 accelerating survivors claimed by the mission")
    for V5 in (28, 40, 88, 89, 90, 91, 92, 93, 100):
        t0 = time.time()
        v, _ = decide((1, 2, 4, 10, V5))
        print(f"  [1,2,4,10,{V5}] -> {v} [{time.time()-t0:.0f}s]", flush=True)

    print("# full feasible V5 window after [1,2,4,10]  (V5 >= 3*10-2 = 28)")
    feas, infeas = [], []
    for V5 in range(28, 121):
        v, _ = decide((1, 2, 4, 10, V5))
        (feas if v == 'SAT' else infeas).append(V5)
    print(f"  SAT   V5: {feas}")
    print(f"  UNSAT V5: {infeas}")

    print("# is the top triple alone responsible?  (4,10,V5) and (10,V5,.)")
    for V5 in feas[:6] + feas[-6:]:
        v3, _ = decide((4, 10, V5))
        print(f"  (4,10,{V5}) -> {v3}", flush=True)
