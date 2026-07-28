#!/usr/bin/env python3
"""
min_isolated.py -- the requested DIAGNOSTIC.

For each N, compute
    m(N) := min over U subset [2,N] with sum_{n in U} 1/n = 1
            of #{ n in U : n-1 notin U and n+1 notin U }   (isolated points).
m(N)=0 exactly means a legal solution with max(U) <= N exists.

Universe used: prune(N, use_legality=False) -- the RULE A fixpoint, which is a
proved superset of every U subset [2,N] with reciprocal sum 1 (RULE B is NOT
used here: it is only valid when isolated points are forbidden).
"""
import sys, subprocess
sys.path.insert(0, '/home/user/erdos/attempts/route-C')
from prune import prune

BIN = '/home/user/erdos/attempts/route-C/dfs'
lo, hi = int(sys.argv[1]), int(sys.argv[2])
bmax = int(sys.argv[3]) if len(sys.argv) > 3 else 8

print(" N   |A|   m(N)   witness")
for N in range(lo, hi + 1):
    A = prune(N, use_legality=False)
    if not A:
        print(f"{N:3d}  {0:4d}    ---   (RULE A universe empty: no U at all)")
        continue
    got = None
    for b in range(0, bmax + 1):
        inp = f"{N} {b} 1\n{len(A)}\n{' '.join(map(str,A))}\n"
        r = subprocess.run([BIN], input=inp, capture_output=True, text=True)
        sols = [l for l in r.stdout.split('\n') if l.startswith('SOL')]
        if sols:
            got = (b, sols[0])
            break
    if got is None:
        print(f"{N:3d}  {len(A):4d}    >{bmax}")
    else:
        print(f"{N:3d}  {len(A):4d}    {got[0]}     {got[1][4:]}", flush=True)
