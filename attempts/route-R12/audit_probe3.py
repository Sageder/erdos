from audit_core import *
from audit_Rk import smooth_part, cond_ii, lemmaRk_hyp
from sympy import primerange, isprime, factorint

# (A) diagnose k=3,P0=4 false positive 110287 (P0<2k)
n=110287;k=3
print("A) n=110287,k=3: window",[ (n+j,factorint(n+j)) for j in (1,2,3)])
for l in (5,):
    print("   l=5 divides n+3 (j=3): need l>=2j=6 -> 2(l-j)=%d < l=%d : NO carry at pos0"%(2*(5-3),5),
          " c_5(n)=",carries(n,n,5)," demand=",2*sum(nu(n+j,5) for j in range(1,4)))

# (B) does full Lemma R_k imply R''' (remark (i))?
def Rppp(n,k,P0):
    for l in primerange(2,P0+1):
        if carries(n,n,l) < 2*sum(nu(n+j,l) for j in range(1,k+1)): return False
    for j in range(1,k+1):
        for l,e in factorint(n+j).items():
            if l<=P0: continue
            if e!=1: return False
            if ((n+j)//l-1)%l < (l-1)//2: return False
    return True
bad=[]
for n in (1512186,2880636):
    print("B) full-R_2 hit",n,": in S_2?",in_S_ladder_criterion(n,2)," R'''(P0=4)?",Rppp(n,2,4),
          " r^2<=2n at both large primes?",all(p*p<=2*n for j in (1,2) for p in factorint(n+j) if p>4))

# (C) Lemma R_2 restricted to the canonical class c1=1,c2=2 (n=0 mod 4, 3|n), no cond(ii)
cnt=0;fp=[];hits=[]
S=1500
for s in primerange(5,S):
    for r in range(s+ (s+1)//2, 2*s):
        if not isprime(r) or r==s: continue
        if (r%s)<(s+1)//2: continue
        n=r*s-1
        if n%4!=0 or n%3!=0: continue          # c1=1, c2=2, 3 coprime to window
        c2,u2=smooth_part(n+2,4)
        if c2!=2: continue
        f=factorint(u2)
        if sum(f.values())!=2 or len(f)!=2: continue
        p1,p2=sorted(f); ok=False
        for R,Sp in ((p1,p2),(p2,p1)):
            if R>4 and Sp>max(4,2) and 2*Sp-1 < R <= 4*Sp-1 and (2*R)%Sp>=(Sp+1)//2: ok=True
        if not ok: continue
        cnt+=1; hits.append(n)
        if not in_S_ladder_criterion(n,2): fp.append(n)
print("C) canonical class c1=1,c2=2, s<=%d, NO cond(ii): #=%d  in-S_2 failures=%d %s"%(S,cnt,len(fp),fp[:6]))
print("   hits:",sorted(hits)[:30])
# with cond (ii)
cnt2=[h for h in hits if cond_ii(h,2,4)]
print("   of these, satisfying cond(ii): %d -> %s"%(len(cnt2),cnt2))
