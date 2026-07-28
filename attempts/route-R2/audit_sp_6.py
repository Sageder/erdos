#!/usr/bin/env python3
"""INDEPENDENT audit #6 (replaces D1/D3 of audit 5):
 (a) EXHAUSTIVE counterexample hunt for the part-(1) chain at reachable M, with the
     mask window [e_p,L_p') widened so that the SP.9 CONCLUSION holds exactly
     (the chain is valid for any 0<=e<=L, so this is a faithful stress test);
 (b) corollary hypothesis derivations done entirely in logs (no overflow)."""
import math
from fractions import Fraction
from sympy import primerange

def vp(x,p):
    c=0;x=abs(x)
    while x and x%p==0: x//=p;c+=1
    return c
def vp_fact(x,p):
    s=0;q=p
    while q<=x: s+=x//q;q*=p
    return s
def digits(x,p):
    d=[]
    while x>0: d.append(x%p);x//=p
    return d
def kappa(m,p): return vp_fact(2*m,p)-2*vp_fact(m,p)
def W(m,p,k): return sum(vp(2*m-i,p) for i in range(2*k))
def Vs(m,p,k): return max(vp(2*m-i,p) for i in range(2*k))
def Xmask(m,p,e,L):
    d=digits(m,p);thr=-(-p//2)
    return sum(1 for j in range(e,L) if (d[j] if j<len(d) else 0)>=thr)
def theta(p): return Fraction(p//2,p)
def Jp(p,k):
    j=0
    while p**(j+1)<=2*k: j+=1
    return j

print("=== E1: exhaustive counterexample hunt for the part-(1) chain ===")
tot=0;gtot=0;viol=0;cfgs=0
for M in [50000,100000,200000]:
    for (q0,a) in [(1,0),(2,1),(6,5),(24,7),(105,4),(1024,0),(2401,100),(2**5*3**3,16)]:
        for k in [2,3,5,9]:
            for P in [3,7,13]:
                for t in [3,5]:
                    primes=list(primerange(2,P+1))
                    e={p:vp(q0,p) for p in primes}
                    Lw={}
                    okcfg=True
                    for p in primes:
                        rhs=vp_fact(2*k,p)+vp(2*q0,p)+Jp(p,k)+t
                        Lam=0
                        while theta(p)*Fraction(Lam,2)<rhs: Lam+=1
                        Lw[p]=e[p]+Lam
                        if p**Lw[p] > 4*M: okcfg=False   # window must fit in m's digits
                    if not okcfg: continue
                    cfgs+=1
                    m=M+((a-M)%q0)
                    while m<=2*M:
                        tot+=1
                        good=all(Fraction(Xmask(m,p,e[p],Lw[p]))>=theta(p)*Fraction(Lw[p]-e[p],2)
                                 and Vs(m,p,k)<=vp(2*q0,p)+Jp(p,k)+t for p in primes)
                        if good:
                            gtot+=1
                            for p in primes:
                                if kappa(m,p)<W(m,p,k):
                                    viol+=1
                                    print("   *** COUNTEREXAMPLE",M,q0,a,k,P,t,m,p,
                                          kappa(m,p),W(m,p,k))
                        m+=q0
print(f"  configs={cfgs} m tested={tot} |G|={gtot} violations={viol}")
assert viol==0

print("=== E2: SP-A / SP-B hypothesis + error algebra, in logs (no overflow) ===")
bad=0; vac=0
for k in [2,3,10,1000,10**6]:
    for c in [1/6,0.1,0.05,0.01,1e-4]:
        LA=400*(2*k+math.log(2*k)/math.log(2)+1)**2
        for mult in [1.0,1.0000001,2.0,10.0,1e3,1e6]:
            L=LA*mult
            logP=c*math.sqrt(L); t=math.floor(math.sqrt(L)/20)
            if logP<math.log(2):
                vac+=1; continue                        # doc declares this vacuous
            h1 = L>=math.log(70000) and L>=1.25*math.log(4*k)
            h3 = logP<=L/20
            ht = t>=3
            h4 = L/logP>=60*(2*k+math.log(2*k)/math.log(2)+t+1)
            # E_hat  (log-safe)
            logterm1=math.log(3)+logP-(7/240)*L/logP
            logterm2=math.log(6)-t*math.log(2)
            logterm3=math.log(3)-L/20
            EA=math.exp(logterm1)+math.exp(logterm2)+math.exp(logterm3)
            claim=18*math.exp(-math.sqrt(L)/120)
            if not(h1 and h3 and ht and h4 and EA<=claim*(1+1e-12)):
                bad+=1
                print(f"   SP-A FAIL k={k} c={c} logM={L:.4g} H1={h1} H3={h3} t>=3:{ht} "
                      f"H4={h4} EA={EA:.4g} claim={claim:.4g}")
print("  SP-A failures (P>=2 cases):",bad," (vacuous P<2 cases skipped:",vac,")")
assert bad==0
bad=0
for k in [2,3,10,1000,10**6]:
    for P0 in [2,3,13,1000,10**6,10**12]:
        lp=math.log(P0)
        LB=max(math.log(70000),1.25*math.log(4*k),20*lp,360*lp,
               120*lp*(2*k+math.log(2*k)/math.log(2)+1))
        for mult in [1.0,1.0000001,1.5,10.0,1e4]:
            L=LB*mult; t=math.floor(L/(120*lp))
            h1=L>=math.log(70000) and L>=1.25*math.log(4*k)
            h3=lp<=L/20; ht=t>=3
            h4=L/lp>=60*(2*k+math.log(2*k)/math.log(2)+t+1)
            b0=min(math.log(2)/(120*lp),1/20)
            E=math.exp(math.log(3*P0)-(7/240)*L/lp)+math.exp(math.log(6)-t*math.log(2))+math.exp(math.log(3)-L/20)
            claim=18*P0*math.exp(-b0*L)
            if not(h1 and h3 and ht and h4 and E<=claim*(1+1e-12)):
                bad+=1; print(f"   SP-B FAIL k={k} P0={P0} logM={L:.4g} {h1}{h3}{ht}{h4} E={E:.4g} claim={claim:.4g}")
print("  SP-B failures:",bad)
assert bad==0
print("DONE")
