from audit_core import *
from audit_Rk import cond_ii, smooth_part
from sympy import primerange
# PROBE 1: does cond (ii) really force c_l(n) >= 2 V_l for EVERY n satisfying it?
bad=[]
for k in (2,3,5):
    P0=2*k
    for n in range(1,150000):
        if not cond_ii(n,k,P0): continue
        for l in primerange(2,P0+1):
            V=sum(nu(n+j,l) for j in range(1,k+1))
            if carries(n,n,l) < 2*V: bad.append((k,l,n,carries(n,n,l),2*V))
print("PROBE1 cond(ii) => c_l>=2V_l  violations:",len(bad),bad[:5])

# PROBE 2: box  cs-1 < r <= 2cs-1  =>  sqrt(n+j) <= r < sqrt(2(n+j)) ?
import random
bad2=[]
for _ in range(200000):
    c=random.randint(1,20); s=random.randint(5,10**5); r=random.randint(c*s, 2*c*s-1)
    m=c*r*s
    if not (r*r<=m<2*r*r): bad2.append((c,r,s))
print("PROBE2 box => r^2 <= n+j < 2r^2 violations:",len(bad2),bad2[:3])
