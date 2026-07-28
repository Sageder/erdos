#!/usr/bin/env python3
"""
run_dfs.py N_lo N_hi [budget]

For every N in [N_lo,N_hi] that passes the cheap RULE A+B necessary test
(N and N-1 both survive the fixpoint), run the exhaustive DFS over the pruned
universe looking for U with sum 1/n = 1, max(U)=N and at most `budget` isolated
points.  budget=0 is the legal case.

For budget=0 the universe is prune(N, use_legality=True) (RULE B sound).
For budget>0 RULE B is NOT sound, so we use prune(N, use_legality=False).
"""
import sys, subprocess, time
sys.path.insert(0, '/home/user/erdos/attempts/route-C')
from prune import prune

lo, hi = int(sys.argv[1]), int(sys.argv[2])
budget = int(sys.argv[3]) if len(sys.argv) > 3 else 0
BIN = '/home/user/erdos/attempts/route-C/dfs'

tot_nodes = 0
for N in range(lo, hi + 1):
    A = prune(N, use_legality=(budget == 0))
    if A is None:
        A = []
    S = set(A)
    if not (N in S and N - 1 in S) and budget == 0:
        continue
    if budget > 0 and N not in S:
        continue
    inp = f"{N} {budget} 1000000\n{len(A)}\n{' '.join(map(str,A))}\n"
    t0 = time.time()
    r = subprocess.run([BIN], input=inp, capture_output=True, text=True)
    out = r.stdout.strip().split('\n')
    sols = [l for l in out if l.startswith('SOL')]
    # keep only those with max = N
    sols = [l for l in sols if int(l.split()[-1]) == N]
    last = out[-1]
    nodes = int(last.split('nodes=')[1].split()[0]) if 'nodes=' in last else -1
    tot_nodes += nodes
    print(f"N={N:5d} |A|={len(A):4d} nodes={nodes:14d} sols(max=N)={len(sols):6d} "
          f"t={time.time()-t0:7.2f}s", flush=True)
    for l in sols[:5]:
        print("   ", l, flush=True)
print("TOTAL nodes", tot_nodes)
