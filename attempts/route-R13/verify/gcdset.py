from math import gcd
import sys
# find k-element sets n_1<...<n_k with gcd(n_i,n_j)=n_j-n_i for all i<j,
# and additionally Q0 | n_i/(n_j-n_i) for all i<j  (class-compatibility condition)
def extend(cur, L, k, Q0, out):
    if len(cur)==k:
        out.append(tuple(cur)); return True
    start = cur[-1]+1 if cur else 1
    for b in range(start, L):
        ok=True
        for a in cur:
            g=b-a
            if a % g or (a//g) % Q0: ok=False; break
            if gcd(a,b)!=g: ok=False; break
        if ok:
            cur.append(b)
            if extend(cur,L,k,Q0,out): return True
            cur.pop()
    return False
for Q0 in (1,2,3,4,6):
    for k in (2,3,4,5):
        out=[]
        extend([],4000,k,Q0,out)
        print("Q0=%d k=%d ->"%(Q0,k), out[0] if out else "NONE up to 4000")
