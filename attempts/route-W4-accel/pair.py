"""pair.py -- the 2-CUT-WITH-HORIZON system N(W,U,M).

KEY POINT.  With only the two cuts W < U known, every pair (e,d) with
    e in (W,U],   max(1,e-W) <= d <= e-1,   e+2d <= M
gives a FORCED INVERSION  (e+2d) < (e+d)  in position:
    x=e-d <= W  <  e = x+d <= U  <  x+2d = e+d,  so x,e,e+d is a positionally
    increasing 3-AP forced by the block layout, hence C1 forbids  e+d < e+2d.
This web lives entirely in the block (U,M] and grows with M.  If the resulting
system is UNSAT for some M, then NO monotone-4-AP-free permutation of N has BOTH
W and U as cuts -- a statement uniform over every possible continuation.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def run(W, U, M, cap=600, window=None):
    t0 = time.time()
    S = wsys.Sys((W, U), M, window=window)
    v, o = wsys.solve_lazy(S, time_cap=cap, tag=f"{W},{U},{M}")
    if v == 'GEOM_DEAD':
        v = 'UNSAT'
    if v == 'SAT' and window is None:
        wsys.verify((W, U), M, o)
        v = 'SAT(verified)'
    return v, time.time() - t0


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if which in ('all', 'E1'):
        print("## E1  N(10,28,M): does the PAIR {10,28} die at a larger horizon?")
        for M in (82, 90, 100, 120, 150, 200, 260):
            v, t = run(10, 28, M)
            print(f"   N(10,28,{M}) -> {v} [{t:.0f}s]", flush=True)
    if which in ('all', 'E1b'):
        print("## E1b control: N(8,28,M) (W=8 is below the measured 3-cut threshold)")
        for M in (82, 120, 200, 260):
            v, t = run(8, 28, M)
            print(f"   N(8,28,{M}) -> {v} [{t:.0f}s]", flush=True)
    if which in ('all', 'E3'):
        print("## E3  N(10,90,M): the mission's accelerating continuation")
        for M in (268, 300, 400):
            v, t = run(10, 90, M)
            print(f"   N(10,90,{M}) -> {v} [{t:.0f}s]", flush=True)
