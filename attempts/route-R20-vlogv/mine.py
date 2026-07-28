import sys, ast, math
sys.path.insert(0,'/home/user/erdos/attempts/route-R20-vlogv')
from constructions import v2, logb
fn = sys.argv[1]
perm = ast.literal_eval(open(fn).read())
N = len(perm); pos = {v:i+1 for i,v in enumerate(perm)}
print(f"# {fn}: N={N}")
print("order:", perm[:40], "...")
# profile
rat = sorted(((pos[v]/v, v) for v in range(1,N+1)), reverse=True)[:10]
print("largest pos(v)/v :", [(v, round(r,2), f"v2={v2(v)}") for r,v in rat])
# is the delay correlated with v2?
import statistics
for a in range(0,7):
    S=[pos[v]/v for v in range(1,N+1) if v2(v)==a]
    if S: print(f"  v2={a}: n={len(S)} mean pos/v={statistics.mean(S):.2f} max={max(S):.2f}")
# 'grounded' and 'record' spines
rec=[v for v in range(1,N+1) if all(pos[w]>pos[v] for w in range(v+1,N+1))]
gr=[v for v in range(1,N+1) if all(pos[w]<pos[v] for w in range(1,v))]
print("records (Lambda):", rec[:20])
print("grounded (Gamma):", gr[:20])
# coarse structure: for dyadic blocks, position window
for k in range(0, 9):
    B=[v for v in range(2**k, min(2**(k+1), N+1))]
    if not B: break
    ps=[pos[v] for v in B]
    print(f"  dyadic block [{2**k},{min(2**(k+1),N+1)-1}]: pos range [{min(ps)},{max(ps)}] median {sorted(ps)[len(ps)//2]}")
