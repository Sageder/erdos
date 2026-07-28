import sys, time
sys.path.insert(0,'/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from profile import ProfileSolver
K=4
print("Q(L,N): is there a 4-AP-free perm of [1..N] whose first L values are exactly [1..L]?")
print("  (Q(L,N) true  <=>  nu_L(N)=L.   nu_L(N)->oo for one L would prove Erdos196=YES.)")
for N in (32,48,64,96,128):
    row=[]
    t0=time.time()
    ps=ProfileSolver(N,K=K,L0=min(20,N))
    for L in range(2,min(21,N)):
        ok = ps.sat({v:L for v in range(1,L+1)})
        row.append((L,'Y' if ok else 'n'))
        if ok:
            p=ps.perm(); assert not has_monotone_kap_pos(p,K); assert sorted(p[:L])==list(range(1,L+1))
    ps.close()
    print(f"  N={N:4d}: "+" ".join(f"{L}:{c}" for L,c in row)+f"   ({time.time()-t0:.0f}s)", flush=True)
