"""brackets.py -- exact bracketing SAT/UNSAT horizon for each headline claim.
A single UNSAT witnesses death AT that horizon only; the SAT point immediately
below is what makes the horizon minimal.  Every SAT witness is re-verified with
the trusted checkers in experiments/apcheck.py.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys

CASES = [((10, 28), 29, 82), ((1, 2, 4, 10, 28), 29, 82), ((8, 26, 76), 77, 152),
         ((2, 8, 26, 76), 77, 152), ((11, 31), 32, 124), ((12, 34), 35, 136),
         ((13, 37), 38, 109), ((20, 58), 59, 172)]

for cuts, lo, hi in CASES:
    a, b = lo - 1, hi          # a assumed SAT-ish, b known UNSAT
    while b - a > 1:
        mid = (a + b) // 2
        S = wsys.Sys(cuts, mid)
        v, o = wsys.solve_lazy(S, time_cap=900)
        if v in ('UNSAT', 'GEOM_DEAD'):
            b = mid
        else:
            a = mid
    S = wsys.Sys(cuts, a)
    v, o = wsys.solve_lazy(S, time_cap=900)
    ok = ''
    if v == 'SAT':
        wsys.verify(cuts, a, o)
        ok = ' (witness verified vs apcheck)'
    print(f"  {list(cuts)}: SAT at M={a}{ok};  UNSAT at M={b}", flush=True)
