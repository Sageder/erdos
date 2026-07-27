"""power_profile.py — probe survival under superlinear profiles pos(v) <= ceil(D * v**1.5),
for the asym target and the plain target. If the ~8C^2 law for linear profiles reflects
a true displacement requirement pos(v) ~ v^{3/2}, then v^{1.5} profiles with adequate D
should survive far beyond linear ones.
"""
import sys, time, math
sys.path.insert(0, '/home/user/erdos/experiments')
from sat_order import build
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

def solve_pow(N, D, p, dec3, inc4, dec4):
    cl, pool, var = build(N, inc4=inc4, dec4=dec4, dec3=dec3)
    for v in range(1, N + 1):
        bound = math.ceil(D * v**p)
        if bound >= N:
            continue
        lits = []
        for w in range(1, N + 1):
            if w == v:
                continue
            lits.append(var(min(v, w), max(v, w)) * (1 if w < v else -1))
        enc = CardEnc.atmost(lits=lits, bound=bound - 1, vpool=pool, encoding=EncType.seqcounter)
        cl.extend(enc.clauses)
    S = Cadical195(bootstrap_with=cl)
    sat = S.solve()
    S.delete()
    return sat

for label, dec3, inc4, dec4 in [("asym", True, True, False), ("plain", False, True, True)]:
    for D in (1.0, 2.0):
        for N in (40, 60, 90, 130, 180, 240):
            t0 = time.time()
            sat = solve_pow(N, D, 1.5, dec3, inc4, dec4)
            dt = time.time() - t0
            print(f"{label} D={D} v^1.5: N={N}: {'SAT' if sat else 'UNSAT'} ({dt:.1f}s)", flush=True)
            if not sat or dt > 300:
                break
