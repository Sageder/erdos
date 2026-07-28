#!/usr/bin/env python3
r"""
ultable.py -- the unit-fraction LIFT table, two-phase.

Phase 1 (EXHAUSTIVE, gives rigorous NEGATIVES): for N = f*n, f in a small list,
run the deterministic exhaustive search for a legal S with min S >= T,
max S <= N, Sigma(S) = 1/n.  "NONE" is then a proved statement about that exact
window.
Phase 2 (RANDOMISED restarts, gives rigorous POSITIVES only): larger windows,
node budget per restart; a hit is a certificate (re-verified exactly), a miss
claims nothing.

usage: ultable.py nlo nhi ratio exhaust_factors random_factors budget seeds out
   e.g. ultable.py 2 14 2.0 4,6,9 14,20,30,45 400000 3 ul_r2.txt
"""
import sys
from fractions import Fraction
import liftscan as LS

nlo, nhi = int(sys.argv[1]), int(sys.argv[2])
ratio = float(sys.argv[3])
exf = [float(x) for x in sys.argv[4].split(",")]
rnf = [float(x) for x in sys.argv[5].split(",")]
budget = int(sys.argv[6]); nseed = int(sys.argv[7])
out = open(sys.argv[8], "w")
TMO = float(sys.argv[9]) if len(sys.argv) > 9 else 90.0

def emit(s):
    print(s, flush=True); out.write(s + "\n"); out.flush()

for n in range(nlo, nhi + 1):
    q = Fraction(1, n)
    T = int(-(-ratio * n // 1))
    done = False
    for f in exf:
        N = int(f * n)
        if N <= T + 2: continue
        st, sols, nodes, lb = LS.run(q, T, N, nsol=1, tmo=TMO)
        if st == "SOL":
            emit("n=%d T=%d N=%d(%.0fn) EXH-SOL Lbits=%d nodes=%d  %s"
                 % (n, T, N, f, lb, nodes, " ".join(map(str, sols[0]))))
            done = True; break
        emit("n=%d T=%d N=%d(%.0fn) %s Lbits=%d nodes=%d" % (n, T, N, f, st, lb, nodes))
    if done: continue
    for f in rnf:
        N = int(f * n)
        for sd in range(nseed):
            st, sols, nodes, lb = LS.run(q, T, N, nsol=1, budget=budget, seed=sd, tmo=TMO)
            if st == "SOL":
                emit("n=%d T=%d N=%d(%.0fn) RND-SOL seed=%d Lbits=%d nodes=%d  %s"
                     % (n, T, N, f, sd, lb, nodes, " ".join(map(str, sols[0]))))
                done = True; break
            emit("n=%d T=%d N=%d(%.0fn) rnd seed=%d %s Lbits=%d nodes=%d" % (n, T, N, f, sd, st, lb, nodes))
        if done: break
    if not done:
        emit("n=%d T=%d NO LIFT FOUND up to %.0fn" % (n, T, rnf[-1]))
