"""v5scan.py -- the window law after the prefix [1,2,4,10]: which V5 survive?
Lemma G forces V5 >= 3*10-2 = 28.  For each candidate V5 we run the horizon system
at M = 3*V5-2 (and, if that is SAT, at M = 5*V5) with a time cap; UNSAT excludes
V5 outright, SAT/TIME_CAP leaves it undecided at that horizon.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys

lo, hi, cap = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
PREF = (1, 2, 4, 10)
for V5 in range(lo, hi + 1):
    cuts = PREF + (V5,)
    res = []
    for M in (3 * V5 - 2, 5 * V5):
        t0 = time.time()
        S = wsys.Sys(cuts, M)
        v, o = wsys.solve_lazy(S, time_cap=cap)
        if v == 'GEOM_DEAD':
            v = 'UNSAT'
        res.append(f"M={M}:{v}[{time.time()-t0:.0f}s]")
        if v == 'UNSAT':
            break
    print(f"  V5={V5}: {' '.join(res)}", flush=True)
