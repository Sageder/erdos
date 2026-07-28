import sys, time
sys.path.insert(0,'/home/user/erdos/attempts/route-R20-vlogv')
sys.path.insert(0,'/home/user/erdos/experiments')
from classsat import solve_classes, FAMILIES
from apcheck import has_monotone_kap_pos
names = sys.argv[1].split('|')
Ns = [int(x) for x in sys.argv[2].split(',')]
for nm in names:
    c = FAMILIES[nm]
    for N in Ns:
        t0=time.time(); res,w,rounds = solve_classes(N,c); dt=time.time()-t0
        extra=""
        if res=="SAT":
            assert sorted(w)==list(range(1,N+1)) and not has_monotone_kap_pos(w,4)
            pos={v:i+1 for i,v in enumerate(w)}
            extra=f" maxpos/v={max(pos[v]/v for v in range(1,N+1)):.2f}"
            open(f"cw_{nm}_{N}.txt","w").write(repr(w))
        elif res.startswith("FORCED"):
            extra=f" at (x,e)={w}"
        print(f"{nm} N={N}: {res} ({dt:.0f}s, {rounds} rounds){extra}", flush=True)
        if res!="SAT": break
