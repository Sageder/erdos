"""asym_pos2.py — decide R11's fate empirically: pin ONLY pos(2) <= B in the asym
target (no dec-3AP + no inc-4AP) and scan N for extinction. If every B dies at finite
N(B), then (by restriction) any infinite asym witness would need pos(2) unbounded —
impossible — so NO infinite asym witness exists and route R11 is dead.
Also runs the plain-target analogue (FIN(2)-for-196 probe) for contrast.
"""
import sys, time, math
sys.path.insert(0, '/home/user/erdos/experiments')
from sat_order import build
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

def pin2_sat(N, B, dec3, inc4, dec4):
    cl, pool, var = build(N, inc4=inc4, dec4=dec4, dec3=dec3)
    lits = []
    for w in range(1, N + 1):
        if w == 2: continue
        lits.append(var(min(2, w), max(2, w)) * (1 if w < 2 else -1))
    enc = CardEnc.atmost(lits=lits, bound=B - 1, vpool=pool, encoding=EncType.seqcounter)
    cl.extend(enc.clauses)
    S = Cadical195(bootstrap_with=cl); sat = S.solve(); S.delete()
    return sat

for label, flags in [("asym", dict(dec3=True, inc4=True, dec4=False)),
                     ("plain", dict(dec3=False, inc4=True, dec4=True))]:
    for B in (5, 10, 20, 40):
        N = 24; last = None
        while True:
            t0 = time.time(); sat = pin2_sat(N, B, **flags); dt = time.time() - t0
            if sat:
                last = N; N += max(2, N // 6)
            else:
                lo, hi = (last or 23), N
                while hi - lo > 1:
                    mid = (lo + hi) // 2
                    if pin2_sat(mid, B, **flags): lo = mid
                    else: hi = mid
                print(f"{label} pos(2)<={B}: EXTINCT at N={hi} (max SAT {lo})", flush=True)
                break
            if dt > 240 or N > 420:
                print(f"{label} pos(2)<={B}: still SAT at N={last} (stopped)", flush=True)
                break
