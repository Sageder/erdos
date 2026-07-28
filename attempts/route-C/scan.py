#!/usr/bin/env python3
"""
scan.py -- for each N, run the RULE A + RULE B fixpoint on [2,N] and report:
   nsurv       size of the pruned universe
   topok       whether BOTH N and N-1 survive (necessary for a legal U with
               max(U)=N, since max(U)=N forces N,N-1 in U)
   forced      whether prune(N, force={N,N-1}) is feasible (stronger test)
   sum         total reciprocal mass of survivors (must be >= 1 for a solution)
Writes a machine-readable table to scan_<lo>_<hi>.txt.
"""
import sys
from fractions import Fraction
sys.path.insert(0, '/home/user/erdos/attempts/route-C')
from prune import prune

lo = int(sys.argv[1]); hi = int(sys.argv[2])
out = open(f"/home/user/erdos/attempts/route-C/scan_{lo}_{hi}.txt", "w")
cands = []
for N in range(lo, hi + 1):
    surv = prune(N, True)
    if surv is None:
        surv = []
    S = set(surv)
    topok = (N in S and N - 1 in S)
    forced_ok = False
    if topok:
        f = prune(N, True, force={N, N - 1})
        forced_ok = f is not None
        nf = len(f) if f else 0
    else:
        nf = 0
    tot = sum(Fraction(1, n) for n in surv)
    line = f"{N} {len(surv)} {int(topok)} {int(forced_ok)} {nf} {float(tot):.5f}"
    print(line); out.write(line + "\n"); out.flush()
    if forced_ok:
        cands.append(N)
out.write("# candidates: " + " ".join(map(str, cands)) + "\n")
out.close()
print("CANDIDATES (topok and force-feasible):", cands)
