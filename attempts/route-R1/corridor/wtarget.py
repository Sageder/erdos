"""wtarget.py -- targeted probe: can W = 11..14 be the first cut of a CHAIN-LEGAL
triple?  Concentrated on the U/W band 4.0-6.5 where the only known feasible
chain-legal triple (10,46,136) lives (U/W = 4.60), plus the shoulder.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_eager, solve_lazy, verify

def feas(cuts, tcap=900):
    n = cuts[-1] - cuts[-2]
    r, w = (solve_eager(cuts) if n <= 85 else solve_lazy(cuts, time_cap=tcap))
    if r == 'SAT':
        verify(cuts, w)
    return r

found = []
for W in (11, 12, 13, 14):
    Us = sorted({int(round(c * W)) for c in
                 (3.0, 3.5, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.5, 6.0, 6.5, 7.5, 9.0)})
    for U in Us:
        if U < 3 * W - 2:
            continue
        Vs = sorted({v for v in [3*U-2, 3*U-1, 3*U, 3*U+1, 3*U+2,
                                 int(3.3*U), int(4.0*U), int(4.6*U), int(4.8*U),
                                 int(5.0*U), int(5.3*U), int(5.6*U), int(6.0*U)]
                     if v >= 3*U-2 and v <= 700})
        for V in Vs:
            t = time.time()
            r = feas([W, U, V])
            mark = '*** SAT' if r == 'SAT' else '  ' + r
            print(f"{mark} ({W},{U},{V}) U/W={U/W:.2f} V/U={V/U:.2f} [{time.time()-t:.0f}s]",
                  flush=True)
            if r == 'SAT':
                found.append((W, U, V))
print("# FOUND chain-legal feasible triples with W>=11:", found, flush=True)
