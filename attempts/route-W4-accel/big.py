"""big.py -- large-U pair tests with CP-SAT (integer ranks) on the TOP relaxation.
Second encoding as well as a second engine: transitivity is implicit in the rank
model, so an UNSAT here is independent of the lazy-CEGAR machinery.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def topcp(W, U, M, tl=1800, workers=4):
    S = wsys.Sys((W, U), M, window=(U + 1, M))
    t0 = time.time()
    v, o = wsys.solve_cpsat(S, tlimit=tl, nworkers=workers)
    print(f"   cpsat TOP({W},{U},{M}) -> {v} [{time.time()-t0:.0f}s]", flush=True)
    return v


def toplazy(W, U, M, cap=1800):
    S = wsys.Sys((W, U), M, window=(U + 1, M))
    t0 = time.time()
    v, o = wsys.solve_lazy(S, time_cap=cap)
    if v == 'GEOM_DEAD':
        v = 'UNSAT'
    print(f"   lazy  TOP({W},{U},{M}) -> {v} [{time.time()-t0:.0f}s]", flush=True)
    return v


if __name__ == '__main__':
    job = sys.argv[1]
    if job == 'p1090':
        print("## pair (10,90): the mission's accelerating continuation")
        for M in (268, 300, 360, 450):
            if topcp(10, 90, M) == 'UNSAT':
                break
    elif job == 'verify':
        print("## second-engine/second-encoding verification of load-bearing UNSATs")
        for (W, U, M) in [(10, 28, 82), (10, 31, 155), (10, 34, 170),
                          (10, 22, 160), (10, 26, 76)]:
            topcp(W, U, M, tl=1200)
            for eng in ('glucose42', 'minisat22'):
                S = wsys.Sys((W, U), M, window=(U + 1, M))
                t0 = time.time()
                v, _ = wsys.solve_lazy(S, time_cap=1200, solver=eng)
                print(f"   lazy/{eng} TOP({W},{U},{M}) -> {v} "
                      f"[{time.time()-t0:.0f}s]", flush=True)
    elif job == 'cp':
        W, U, M = map(int, sys.argv[2:5])
        topcp(W, U, M)
