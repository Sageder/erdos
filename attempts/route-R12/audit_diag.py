from audit_core import *
from audit_Rk import smooth_part, cond_ii, lemmaRk_hyp
from sympy import primerange, factorint
for n in (26791,124930):
    k=2;P0=4
    print("n=",n,"n+1=",n+1,factorint(n+1),"n+2=",n+2,factorint(n+2))
    for l in (2,3):
        v=[nu(n+j,l) for j in range(1,k+1)];V=sum(v);D=1+max(v)
        print("  l=",l,"v=",v,"V=",V,"D=",D,"c_l(n)=",carries(n,n,l),"demand=",2*V,
              "digits n base l:",digits(n,l)[:D+2*V+2], "cond_ii-window",list(range(D,D+2*V+1)))
    print("  in S_2?",in_S_ladder_criterion(n,2))
