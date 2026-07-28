"""plain_thresholds.py — minimal UNSAT N for the PLAIN 196 target (no monotone 4-AP,
both orientations) under profile pos(v) <= ceil(C*v). Compare with asym thresholds
(8, 14, 20, 34, 56 for C = 1, 1.25, 1.5, 2, 2.5). Plain is weaker-constrained, so
N_plain(C) >= N_asym(C); question is whether extinction happens at all for each C.
"""
import sys, time, math
sys.path.insert(0, '/home/user/erdos/experiments')
from sat_order import build
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

def solve_profile_frac(N, C):
    cl, pool, var = build(N, inc4=True, dec4=True, dec3=False)
    for v in range(1, N + 1):
        bound = math.ceil(C * v)
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

if __name__ == "__main__":
    results = {}
    for C in (1.0, 1.25, 1.5, 2.0, 2.5, 3.0):
        N = 8; last_sat = None
        while True:
            t0 = time.time(); sat = solve_profile_frac(N, C); dt = time.time() - t0
            if sat:
                last_sat = N; N += max(1, N // 8)
            else:
                lo, hi = (last_sat or 7), N
                while hi - lo > 1:
                    mid = (lo + hi) // 2
                    if solve_profile_frac(mid, C): lo = mid
                    else: hi = mid
                results[C] = hi
                print(f"plain C={C}: minimal UNSAT N = {hi}  (max SAT N = {lo})", flush=True)
                break
            if dt > 300 or N > 500:
                print(f"plain C={C}: still SAT at N={last_sat}, stopping", flush=True)
                results[C] = None
                break
    print("RESULTS:", results)
    