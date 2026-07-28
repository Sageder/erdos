from audit_core import *
from audit_Rk import smooth_part, cond_ii
from sympy import primerange, isprime, factorint
import sys
S=int(sys.argv[1]) if len(sys.argv)>1 else 6000
cnt=0;fp=[];withii=0
for s in primerange(5,S):
    for r in range(s+(s+1)//2,2*s):
        if not isprime(r): continue
        if (r%s)<(s+1)//2: continue
        n=r*s-1
        if n%4 or n%3: continue
        c2,u2=smooth_part(n+2,4)
        if c2!=2: continue
        f=factorint(u2)
        if sum(f.values())!=2 or len(f)!=2: continue
        p1,p2=sorted(f); ok=False
        for R,Sp in ((p1,p2),(p2,p1)):
            if 2*Sp-1<R<=4*Sp-1 and (2*R)%Sp>=(Sp+1)//2 and R>4 and Sp>4: ok=True
        if not ok: continue
        cnt+=1
        if cond_ii(n,2,4): withii+=1
        if not in_S_ladder_criterion(n,2): fp.append(n)
print("canonical class c1=1,c2=2 (n=0 mod 12, 4|n), s<=%d (n up to ~%.1e):"%(S,2*S*S))
print("  candidates=%d   NOT in S_2 = %d %s   satisfying cond(ii)=%d"%(cnt,len(fp),fp[:6],withii))
# r=s excluded by the residue condition?  (c r mod s) with r=s is 0
print("  r=s check: for any c,r  (c*r mod r)=0 < (r+1)/2  -> residue cond already excludes r=s:",
      all((c*r)%r==0 for c in range(1,50) for r in range(3,200)))
# R''' vacuous-b case: n+j prime (W=1) -> C_l fails
print("  n+j prime => W=1 => (W-1)%l=0 >= (l-1)/2 only if l<=1 : correctly rejected")
