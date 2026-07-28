"""shallow_scan.py — FINlin(K) probe (upgraded FIN criterion; CORE.md Lemma 7 variant).

SHALLOW(K, c, N) [plain target]: exists monotone-4-AP-free permutation of [1..N] with
pos(v) <= ceil(c*v) for ALL v <= K (no constraint on v > K).
FINlin(K) := for every c there is N with no such permutation (extinction). For any
fixed K, FINlin(K) implies 196-YES by the Lemma 7 pigeonhole (for each c some v <= K
has pos_a(v) > c*v >= c; pigeonhole over the K values gives pos_a(v*) unbounded).

Scan: K in {8, 15}; c in {2, 3, 4, 6}; N grows until UNSAT (extinction; inherited
upward by restriction) or SAT persists past the compute limit.
"""

import sys, math, time
sys.path.insert(0, '/home/user/erdos/experiments')
from sat_order import build
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def shallow_sat(N, K, c, dec3=False, inc4=True, dec4=True):
    cl, pool, var = build(N, inc4=inc4, dec4=dec4, dec3=dec3)
    for v in range(1, K + 1):
        bound = math.ceil(c * v)
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
    for K in (8, 15):
        for c in (2, 3, 4, 6):
            N = max(3 * K, 24)
            last_sat, verdict = None, None
            while True:
                t0 = time.time()
                sat = shallow_sat(N, K, c)
                dt = time.time() - t0
                if sat:
                    last_sat = N
                    N += max(2, N // 6)
                else:
                    lo, hi = (last_sat or N - 1), N
                    if last_sat is None:
                        # never saw SAT; walk down for the exact frontier
                        while N > 4 and not shallow_sat(N - 1, K, c):
                            N -= 1
                        verdict = f"EXTINCT from N={N} (never SAT in scan range)"
                        break
                    while hi - lo > 1:
                        mid = (lo + hi) // 2
                        if shallow_sat(mid, K, c):
                            lo = mid
                        else:
                            hi = mid
                    verdict = f"EXTINCT at N={hi} (max SAT N={lo})"
                    break
                if dt > 300 or N > 400:
                    verdict = f"still SAT at N={last_sat} (stopped: {'slow' if dt > 300 else 'cap'})"
                    break
            print(f"plain SHALLOW K={K} c={c}: {verdict}", flush=True)
