import sys
sys.path.insert(0,'/home/user/erdos/attempts/route-R18-bounded-closure')
from blockalone_cp import decide
print("ratio block   values            size   inv  noinc3   no4  verdict  secs", flush=True)
for r in (3,4,5,6,7,8,10,12,16,24,32):
    for j in range(1,7):
        cuts=[r**k for k in range(j+4)]
        n=cuts[j+1]-cuts[j]
        if n>1600:
            print(f"{r:5d} {j:5d}  [{cuts[j]}..{cuts[j+1]-1}] size={n}: SKIP", flush=True); break
        st,dt,stat,order=decide(cuts,j,time_limit=900.0,workers=2)
        print(f"{r:5d} {j:5d}  [{cuts[j]}..{cuts[j+1]-1}] {stat['n']:6d} {stat['inv']:6d} {stat['noinc3']:6d} {stat['no4']:6d}  {st:7s} {dt:7.1f}", flush=True)
        if st!="SAT": break
