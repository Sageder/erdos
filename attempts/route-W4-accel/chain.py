"""chain.py -- horizon-extended test of whole cut sets (stronger than any pair test,
because every pair of DISTINCT blocks below the top contributes forced relations)."""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def go(cuts, M, cap=2400, relax=False):
    S = wsys.Sys(cuts, M, window=((cuts[-1] + 1, M) if relax else None))
    t0 = time.time()
    v, o = wsys.solve_lazy(S, time_cap=cap)
    if v == 'GEOM_DEAD':
        v = 'UNSAT'
    if v == 'SAT' and not relax:
        wsys.verify(cuts, M, o)
        v = 'SAT*'
    print(f"   {list(cuts)} @M={M}{' TOP' if relax else ''} -> {v} "
          f"[{time.time()-t0:.0f}s]", flush=True)
    return v


if __name__ == '__main__':
    job = sys.argv[1]
    if job == 'a90':
        print("## [1,2,4,10,V5] accelerating survivors, horizon extended")
        for V5 in (90, 91, 92):
            for M in (180, 224, 268, 320, 400):
                if go((1, 2, 4, 10, V5), M) in ('UNSAT', 'TIME_CAP'):
                    break
    elif job == 'a90top':
        print("## same, TOP relaxation (cheaper, UNSAT still sound)")
        for V5 in (90, 91, 92):
            for M in (268, 360, 450, 540):
                if go((1, 2, 4, 10, V5), M, relax=True) in ('UNSAT', 'TIME_CAP'):
                    break
    elif job == 'v5':
        print("## which V5 survive the horizon test after [1,2,4,10]?")
        for V5 in range(28, 121):
            r = go((1, 2, 4, 10, V5), 3 * V5 - 2, cap=600)
            if r != 'UNSAT':
                r2 = go((1, 2, 4, 10, V5), 5 * V5, cap=900)
    elif job == 'one':
        cuts = tuple(int(x) for x in sys.argv[2].split(','))
        M = int(sys.argv[3])
        go(cuts, M, cap=5000, relax=(len(sys.argv) > 4))
