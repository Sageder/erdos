import sys, time
sys.path.insert(0,'/home/user/erdos/attempts/route-R16-tau')
from chains_tau import closure_sizes
for M in (10**3, 10**4, 3*10**4):
    t0=time.time(); s=closure_sizes(M)
    b=max(range(1,M+1),key=lambda u:s[u]); lim=max(4,M//10)
    b2=max(range(1,lim+1),key=lambda u:s[u])
    print(f'M={M:7d} max|Cl|={s[b]:6d} at u={b}; best start<=M/10: {s[b2]} at u={b2} [{time.time()-t0:.1f}s]',flush=True)
