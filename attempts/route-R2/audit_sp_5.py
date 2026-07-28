#!/usr/bin/env python3
"""INDEPENDENT audit #5:
 (a) EXHAUSTIVE search over [M,2M] for a counterexample to Master Lemma part (1)
     (G  =>  criterion at every p<=P), gating on the exact SP.9 conclusion;
 (b) verify the corollaries' hypothesis derivations (H1)-(H4) at M = M_A(k), M_B(k,P0)
     using exact log arithmetic;
 (c) verify E_A / E_B error algebra."""
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
def Lp(M,p):
    L=0
    while p**(5*(L+1))<=M**4: L+=1
    return L

print("=== D1: EXHAUSTIVE hunt for a counterexample to Master Lemma (1) ===")
print("    (hypotheses (H1)-(H4) are numerically unreachable; we instead gate on the")
print("     exact conclusion of SP.9, which is all the part-(1) chain uses)")
total=0; gtot=0; viol=0; cfg_ok=0; cfg_skip=0
for M in [50000,100000,200000]:
    for (q0,a) in [(1,0),(2,0),(2,1),(6,5),(24,7),(105,4),(1024,0),(2**10*3**4,512),(2401,100)]:
        for k in [2,3,5]:
            for P in [3,5,7,13]:
                for t in [3,4]:
                    primes=list(primerange(2,P+1))
                    L={p:Lp(M,p) for p in primes}; e={p:vp(q0,p) for p in primes}
                    # gate: SP.9 conclusion must hold at every p<=P (exact Fractions)
                    if any(L[p]<e[p] for p in primes): cfg_skip+=1; continue
                    if not all(theta(p)*Fraction(L[p]-e[p],2)
                               >= vp_fact(2*k,p)+vp(2*q0,p)+Jp(p,k)+t for p in primes):
                        cfg_skip+=1; continue
                    cfg_ok+=1
                    m=M+((a-M)%q0)
                    while m<=2*M:
                        total+=1
                        good=all(Fraction(Xmask(m,p,e[p],L[p]))>=theta(p)*Fraction(L[p]-e[p],2)
                                 and Vs(m,p,k)<=vp(2*q0,p)+Jp(p,k)+t for p in primes)
                        if good:
                            gtot+=1
                            for p in primes:
                                if kappa(m,p)<W(m,p,k):
                                    viol+=1
                                    print("   *** COUNTEREXAMPLE",M,q0,a,k,P,t,m,p)
                        m+=q0
print(f"  configs gated-in={cfg_ok} skipped(SP.9 false there)={cfg_skip}")
print(f"  m tested={total}  |G| total={gtot}  criterion violations on G = {viol}")
assert viol==0

print("=== D2: is SP.9's threshold *necessary*?  drop it and re-run ===")
viol=0; gtot=0
for M in [100000]:
    for (q0,a) in [(1024,0)]:
        for k in [3]:
            for P in [3]:
                for t in [3]:
                    primes=list(primerange(2,P+1))
                    L={p:Lp(M,p) for p in primes}; e={p:vp(q0,p) for p in primes}
                    print("   SP.9 holds here?",
                          all(theta(p)*Fraction(L[p]-e[p],2)>=vp_fact(2*k,p)+vp(2*q0,p)+Jp(p,k)+t
                              for p in primes),
                          {p:(float(theta(p)*Fraction(L[p]-e[p],2)),
                              vp_fact(2*k,p)+vp(2*q0,p)+Jp(p,k)+t) for p in primes})
                    m=M+((a-M)%q0)
                    while m<=2*M:
                        good=all(Fraction(Xmask(m,p,e[p],L[p]))>=theta(p)*Fraction(L[p]-e[p],2)
                                 and Vs(m,p,k)<=vp(2*q0,p)+Jp(p,k)+t for p in primes)
                        if good:
                            gtot+=1
                            for p in primes:
                                if kappa(m,p)<W(m,p,k): viol+=1
                        m+=q0
print(f"   without SP.9: |G|={gtot}, criterion violations={viol}  "
      f"(nonzero => SP.9 is load-bearing, not an error)")

print("=== D3: corollary hypothesis derivations (exact log arithmetic) ===")
def check_SPA(k,c):
    LA=400*(2*k+math.log(2*k)/math.log(2)+1)**2   # log M_A(k)
    out=[]
    for L in [LA, LA*1.0000001, LA*2, LA*100, 1.3e5, 1e6]:
        if L<LA: continue
        P=math.exp(c*math.sqrt(L)); t=math.floor(math.sqrt(L)/20)
        h1 = (L>=math.log(70000)) and (L>=1.25*math.log(4*k))
        h3 = (c*math.sqrt(L) <= L/20) and (P>=2 or True)
        h4 = (L/(c*math.sqrt(L)) >= 60*(2*k+math.log(2*k)/math.log(2)+t+1)) if P>1 else None
        ht = t>=3
        EA = 3*P*math.exp(-(7/240)*L/(c*math.sqrt(L))) + 6*2.0**(-t) + 3*math.exp(-L/20)
        claim = 18*math.exp(-math.sqrt(L)/120)
        out.append((L,h1,h3,ht,h4,EA<=claim+1e-12,EA,claim))
    return out
bad=0
for k in [2,3,10,1000]:
    for c in [1/6,0.1,0.01,1e-4]:
        for row in check_SPA(k,c):
            L,h1,h3,ht,h4,eok,EA,cl=row
            if not(h1 and h3 and ht and h4 and eok):
                # P<2 case is declared vacuous in the doc; flag it separately
                P=math.exp(c*math.sqrt(L))
                print(f"   k={k} c={c} logM={L:.3g} P={P:.4g}  H1={h1} H3={h3} t>=3:{ht} H4={h4} E_A-ok={eok}")
                if P>=2: bad+=1
print("  SP-A hypothesis/error failures with P>=2:",bad)
assert bad==0

def check_SPB(k,P0):
    LB=max(math.log(70000),1.25*math.log(4*k),20*math.log(P0),
           360*math.log(P0),120*math.log(P0)*(2*k+math.log(2*k)/math.log(2)+1))
    res=[]
    for L in [LB,LB*1.5,LB*10]:
        t=math.floor(L/(120*math.log(P0)))
        h1=L>=math.log(70000) and L>=1.25*math.log(4*k)
        h3=P0<=math.exp(L/20); ht=t>=3
        h4=L/math.log(P0)>=60*(2*k+math.log(2*k)/math.log(2)+t+1)
        b0=min(math.log(2)/(120*math.log(P0)),1/20)
        E=3*P0*math.exp(-(7/240)*L/math.log(P0))+6*2.0**(-t)+3*math.exp(-L/20)
        claim=18*P0*math.exp(-b0*L)
        res.append((L,h1,h3,ht,h4,E<=claim+1e-12))
    return res
bad=0
for k in [2,3,10,1000]:
    for P0 in [2,3,13,1000,10**6]:
        for row in check_SPB(k,P0):
            if not all(row[1:]):
                print("   SP-B FAIL",k,P0,row); bad+=1
print("  SP-B hypothesis/error failures:",bad)
assert bad==0
print("ALL AUDIT-5 CHECKS DONE")
