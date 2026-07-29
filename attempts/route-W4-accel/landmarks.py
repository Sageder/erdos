"""landmarks.py -- do route-R1's landmark cut sets survive the HORIZON test?
R1 certified these as SAT at their own top level (M = V_k).  The horizon system
N(S;M) with M > V_k is strictly stronger and needs no guess about the next cut.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys

SETS = [((8, 26, 76), "R1 shoulder"), ((2, 8, 26, 76), "R1 shoulder, depth 4"),
        ((5, 25, 125), "R1 pure ratio-5 geometric"),
        ((8, 26, 130), "R1 ratio-5 island"),
        ((8, 28, 140), "R1 island"),
        ((2, 8, 26, 140), "R1 island, depth 4"),
        ((1, 5, 6, 16, 46), "depth-5 set found by the R1 audit"),
        ((1, 7, 8, 22, 64), "depth-5 set found by the R1 audit"),
        ((4, 16, 68), "R1 window-law SAT point"),
        ((1, 2, 4, 10, 40), "R1/final depth-5 witness")]

for cuts, tag in SETS:
    Vk = cuts[-1]
    print(f"## {list(cuts)}  ({tag})", flush=True)
    for m in (1.0, 1.5, 2.0, 3.0, 4.0, 5.0):
        M = int(m * Vk) - (2 if m == 3.0 else 0)
        if M < Vk:
            continue
        t0 = time.time()
        S = wsys.Sys(cuts, M)
        v, o = wsys.solve_lazy(S, time_cap=1200)
        if v == 'GEOM_DEAD':
            v = 'UNSAT'
        if v == 'SAT':
            wsys.verify(cuts, M, o); v = 'SAT*'
        print(f"     M={M}: {v} [{time.time()-t0:.0f}s]", flush=True)
        if v in ('UNSAT', 'TIME_CAP'):
            break
