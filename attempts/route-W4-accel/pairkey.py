"""pairkey.py -- targeted pair tests for the accelerating corridor."""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def test(W, U, M, cap=900):
    t0 = time.time()
    S = wsys.Sys((W, U), M)
    v, o = wsys.solve_lazy(S, time_cap=cap, tag=f"{W},{U},{M}")
    if v == 'GEOM_DEAD':
        v = 'UNSAT'
    if v == 'SAT':
        wsys.verify((W, U), M, o)
        v = 'SAT*'
    print(f"   N({W},{U},{M}) -> {v} [{time.time()-t0:.0f}s]", flush=True)
    return v


if __name__ == '__main__':
    job = sys.argv[1]
    if job == 'a':
        print("## the accelerating chain's own pairs, horizon sweep")
        for (W, U) in [(4, 10), (10, 90), (4, 90), (2, 90), (10, 28)]:
            for M in (3 * U - 2, 4 * U, 5 * U, 6 * U):
                if test(W, U, M) == 'UNSAT':
                    break
    if job == 'b':
        print("## W-sweep at U=90 and U=46: where is the pair threshold?")
        for U in (46, 90):
            for W in range(6, 20):
                r = test(W, U, 3 * U - 2)
                if r == 'UNSAT':
                    print(f"   -> first dead W at U={U} is {W}", flush=True)
                    break
    if job == 'c':
        print("## does a dead pair stay dead as U grows?  W=10 fixed")
        for U in (28, 31, 34, 40, 46, 55, 64, 80, 100):
            test(10, U, 3 * U - 2)
    if job == 'd':
        print("## W=11,12,13 at their own 3U-2 horizons and beyond")
        for W in (11, 12, 13, 14, 16):
            for U in (3 * W, 4 * W):
                for M in (3 * U - 2, 4 * U):
                    if test(W, U, M) == 'UNSAT':
                        break
