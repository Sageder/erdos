"""verify2.py -- second solver AND second encoding for every load-bearing UNSAT."""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys

CASES = [((10, 28), 82), ((1, 2, 4, 10, 28), 82), ((8, 26, 76), 152),
         ((2, 8, 26, 76), 152), ((10, 28, 82), 82), ((1, 2, 4, 10, 33), 97),
         ((1, 2, 4, 10, 34), 100), ((11, 31), 124), ((12, 34), 136),
         ((20, 58), 172), ((30, 88), 262)]
for cuts, M in CASES:
    print(f"## {list(cuts)} @M={M}", flush=True)
    for eng in ('cadical195', 'glucose42', 'minisat22'):
        t0 = time.time()
        S = wsys.Sys(cuts, M)
        try:
            v, _ = wsys.solve_eager(S, solver=eng)
        except MemoryError:
            v = 'MEMORY'
        print(f"    eager/{eng}: {v} [{time.time()-t0:.0f}s]", flush=True)
    t0 = time.time()
    S = wsys.Sys(cuts, M)
    v, _ = wsys.solve_cpsat(S, tlimit=900)
    print(f"    cpsat-ranks: {v} [{time.time()-t0:.0f}s]", flush=True)
