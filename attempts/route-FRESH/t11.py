import sys, time
sys.path.insert(0,'/home/user/erdos/experiments')
from core import Builder
from math import factorial
def count(N,K=4):
    # DFS over prefixes using the incremental blocking engine (K=4 only)
    b=Builder(N); tot=0
    def rec(depth):
        nonlocal tot
        if depth==N: tot+=1; return
        for v in range(1,N+1):
            if b.can_append(v):
                b.append(v); rec(depth+1); b.pop()
    rec(0); return tot
for N in range(4,12):
    t=time.time(); c=count(N)
    print(f"N={N}: {c} monotone-4-AP-free perms  = {c/factorial(N):.4f} * N!   ({time.time()-t:.1f}s)", flush=True)
