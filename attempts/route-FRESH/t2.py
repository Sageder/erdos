import sys, time
from sat import m_k
print("K=3 (monotone 3-AP-free; DEGS says impossible on N -> m_k must blow up)")
for k in (2,3,4):
    row=[]
    for N in (8,12,16,20,24,28,32,40,48):
        t=time.time(); r=m_k(N,k,K=3); row.append((N,r[0]))
        print(f"  k={k} N={N}: m_k={r[0]}  ({time.time()-t:.1f}s) head={r[1][:k]}", flush=True)
