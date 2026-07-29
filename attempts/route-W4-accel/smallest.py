import sys,time; sys.path.insert(0,'/home/user/erdos/attempts/route-W4-accel')
import wsys
best=None
for W in range(2,14):
  for U in range(W+1, 3*W+4):
    for M in range(U+1, 4*U+1):
      S=wsys.Sys((W,U),M)
      v,_=wsys.solve_lazy(S,time_cap=60)
      if v in ('UNSAT','GEOM_DEAD'):
        print(f'  smallest-M death for ({W},{U}): M={M}  (|C|={M-U})',flush=True)
        if best is None or M<best[2]: best=(W,U,M)
        break
print('OVERALL SMALLEST M:',best,flush=True)
