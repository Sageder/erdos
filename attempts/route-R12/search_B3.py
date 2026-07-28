"""Find first Lemma R_3 structural solutions (B_3 nonemptiness evidence).
Conditions per window element n+j = c_j r_j s_j (j=1,2,3): r,s prime, r != s,
c s - 1 < r <= 2 c s - 1, (c r mod s) >= (s+1)/2, r,s > 6.
c_1 = 1, c_2 = 2 (n even), c_3 in {1,3,9,27}. Checkpointed, resumable."""
import sys, os
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import in_Sk_fast
from sympy import factorint

def bp(M, c, j):
    f = factorint(M)
    if len(f) != 2 or any(e != 1 for e in f.values()):
        return None
    s, r = sorted(f)
    if s <= 6 or r == s:
        return None
    if not (c*s - 1 < r <= 2*c*s - 1):
        return None
    if (c*r) % s < (s+1)//2:
        return None
    if not (2*(s-j) >= s and 2*(r-j) >= r):
        return None
    return (s, r)

CKPT = '/home/user/erdos/attempts/route-R12/search_B3.ckpt'
start = 20
if os.path.exists(CKPT):
    start = int(open(CKPT).read().split()[0])
hits = []
for n in range(start + (start % 2), 3*10**7, 2):
    if n % 200000 == 0:
        open(CKPT, 'w').write(f"{n} hits={hits}")
        print(f"progress n={n} hits={len(hits)}", flush=True)
    a = bp(n + 1, 1, 1)
    if not a:
        continue
    b = bp((n + 2)//2, 2, 2)
    if not b:
        continue
    m3, c3 = n + 3, 1
    while m3 % 3 == 0:
        m3 //= 3
        c3 *= 3
    c = bp(m3, c3, 3)
    if not c:
        continue
    mem = in_Sk_fast(n, 3)
    hits.append((n, mem))
    print(f"HIT n={n} n+1={a} n+2=2*{b} n+3={c3}*{c} in_S3={mem}", flush=True)
print("DONE", hits, flush=True)
