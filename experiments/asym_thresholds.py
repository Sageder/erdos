"""asym_thresholds.py — find, for each C, the minimal N where the asym target
(no dec-3AP + no inc-4AP) with profile pos(v) <= ceil(C*v) goes UNSAT.
Monotone in N (restriction-hereditary), so linear scan upward from the last known SAT.
Output: table C -> N_extinct (exact), for growth-shape analysis.
"""

import sys, time, math
sys.path.insert(0, '/home/user/erdos/experiments')
from sat_order import build, decode, check_perm
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def solve_profile_frac(N, C):
    cl, pool, var = build(N, inc4=True, dec4=False, dec3=True)
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
    for C in (1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
        N = 8
        last_sat = None
        while True:
            t0 = time.time()
            sat = solve_profile_frac(N, C)
            dt = time.time() - t0
            if sat:
                last_sat = N
                N += max(1, N // 8)
            else:
                # bisect between last_sat and N for exact threshold
                lo, hi = (last_sat or 7), N
                while hi - lo > 1:
                    mid = (lo + hi) // 2
                    if solve_profile_frac(mid, C):
                        lo = mid
                    else:
                        hi = mid
                results[C] = hi
                print(f"C={C}: minimal UNSAT N = {hi}  (max SAT N = {lo})", flush=True)
                break
            if dt > 240 or N > 400:
                print(f"C={C}: still SAT at N={last_sat}, stopping (slow/large)", flush=True)
                break
    print("RESULTS:", results)
