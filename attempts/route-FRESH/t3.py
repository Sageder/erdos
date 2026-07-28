import sys, time
from sat import m_k
print("K=4 (the open case): m_k(N) = min over 4-AP-free perms of [1..N] of max of first k values")
print("  (non-decreasing in N; BOUNDED for every k if a 4-AP-free omega-permutation exists)")
for k in (2,3,4,5,6,8):
    for N in (8,12,16,24,32,40,48,56,64):
        t=time.time(); r=m_k(N,k,K=4)
        print(f"  k={k} N={N}: m_k={r[0]}  ({time.time()-t:.1f}s) head={r[1][:k]}", flush=True)
