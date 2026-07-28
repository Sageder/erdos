#!/usr/bin/env python3
"""INDEPENDENT audit #3: (a) SP.9 at the TIGHT boundary of (H4);
(b) end-to-end Master Lemma part (1) & (2) by exact sampling at huge M;
(c) unconditional verification of the counting bounds |BadC_p|,|BadS_p| by EXHAUSTION
    at reachable M (bounds are proved without (H1)-(H4), so must hold there too)."""
import math, random
from fractions import Fraction
from sympy import primerange

random.seed(999)

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
def Lp_exact(M,p):
    """largest L with p^{5L} <= M^4, i.e. floor((4/5) log_p M) -- exact, bisection"""
    M4=M**4
    hi=1
    while pow(p,5*hi)<=M4: hi*=2
    lo=hi//2
    while lo<hi-1:
        mid=(lo+hi)//2
        if pow(p,5*mid)<=M4: lo=mid
        else: hi=mid
    return lo if pow(p,5*lo)<=M4 else 0

# ---------------- (a) SP.9 at the tight (H4) boundary ----------------
print("=== C1: SP.9 with (H4) satisfied as tightly as possible ===")
bad=0;n=0;minm=None
for k in [2,3,4,7,25]:
    for P in [2,3,5,29,257]:
        need=60*(2*k+math.log(2*k)/math.log(2)+3+1)   # t=3 minimal
        E=max(math.ceil(need),20)      # M = P^E  =>  log M / log P = E >= need exactly
        M=P**E
        while M<70000 or M**4<(4*k)**5: E+=1; M=P**E
        t=3
        assert M>=70000 and M**4>=(4*k)**5 and 2<=P and P**20<=M
        assert E>=60*(2*k+math.log(2*k)/math.log(2)+t+1)   # log M/log P = E exactly
        for q0 in [1, 2, P, 2**10*3**4, 720720]:
            if q0**10>M: continue
            for p in primerange(2,P+1):
                L=Lp_exact(M,p); e=vp(q0,p)
                lhs=theta(p)*Fraction(L-e,2)
                rhs=vp_fact(2*k,p)+vp(2*q0,p)+Jp(p,k)+t
                n+=1
                if lhs<rhs:
                    bad+=1;print("   FAIL",k,P,q0,p,float(lhs),rhs)
                minm=float(lhs-rhs) if minm is None else min(minm,float(lhs-rhs))
                if L-e<18: print("   NOTE Lambda<18:",k,P,q0,p,L-e)
print("  checks:",n," failures:",bad," min margin:",minm)
assert bad==0

# ---------------- (b) end-to-end master lemma, exact sampling ----------------
print("=== C2: Master Lemma (1)+(2) end-to-end, exact, huge M ===")
def run_config(k,M,q0,a,P,t,nsamp,check_part2=False):
    primes=list(primerange(2,int(P)+1))
    Lps={p:Lp_exact(M,p) for p in primes}
    eps={p:vp(q0,p) for p in primes}
    # hypothesis check
    assert M>=70000 and M**4>=(4*k)**5, "H1"
    assert 1<=q0 and q0**10<=M, "H2"
    assert 2<=P and int(P)**20<=M, "H3"
    assert t>=3 and math.log(M)/math.log(P)>=60*(2*k+math.log(2*k)/math.log(2)+t+1)-1e-6,"H4"
    if check_part2:
        assert math.log(M)/math.log(P)>=120*(2*k+math.log(2*k)/math.log(2)+t+1)-1e-6
    good=0;viol=0;viol2=0
    lo=M+((a-M)%q0)
    for _ in range(nsamp):
        m=lo+q0*random.randint(0,(2*M-lo)//q0)
        ok=True
        for p in primes:
            L=Lps[p];e=eps[p]
            if not (Fraction(Xmask(m,p,e,L))>=theta(p)*Fraction(L-e,2)): ok=False;break
            if not (Vs(m,p,k)<=vp(2*q0,p)+Jp(p,k)+t): ok=False;break
        if ok:
            good+=1
            for p in primes:
                if kappa(m,p)<W(m,p,k): viol+=1
                if check_part2:
                    if Fraction(kappa(m,p)-W(m,p,k)) < Fraction(1,120)*Fraction(math.floor(1e6*math.log(M)/math.log(p))-1,10**6):
                        viol2+=1
    return good,nsamp,viol,viol2

def mkM(P,k,t,factor=60):
    E=math.ceil(factor*(2*k+math.log(2*k)/math.log(2)+t+1))
    E=max(E,20)
    M=P**E
    while M<70000 or M**4<(4*k)**5: E+=1;M=P**E
    return M,E

cfgs=[]
for (k,P,t,f,q0,a,ns) in [(2,13,3,60,1,0,600),(2,13,3,60,24,7,600),
                          (2,13,3,60,2**10*3**4,512,600),
                          (3,11,4,60,1,0,400),(3,11,4,60,30030,11,400),
                          (2,101,5,60,1,0,200),(5,251,3,60,1,0,150),
                          (2,13,3,120,1,0,300),(2,13,3,120,2**10*3**4,512,300),
                          (7,3,3,60,1,0,300),(2,2,3,60,1,0,300)]:
    M,E=mkM(P,k,t,f)
    cfgs.append((k,M,q0,a,P,t,ns,f==120,E))
for (k,M,q0,a,P,t,ns,p2,E) in cfgs:
    g,N,v,v2=run_config(k,M,q0,a,P,t,ns,p2)
    print(f"  k={k} logM/logP={E} digits(M)={len(str(M))} q0={q0} P={P} t={t}: |G|/N={g/N:.4f} "
          f"criterion-violations={v} gap-violations={v2}")
    assert v==0 and v2==0

# ---------------- (c) counting bounds by exhaustion ----------------
print("=== C3: |BadC_p| and |BadS_p| bounds by EXHAUSTION over [M,2M] ===")
def exhaust(M,q0,a,p,k,t,Luser=None):
    e=vp(q0,p); L=Luser if Luser is not None else Lp_exact(M,p)
    if L<e: return None
    Lam=L-e; mu=theta(p)*Lam
    AP=[m for m in range(M,2*M+1) if m%q0==a%q0]
    badC=[m for m in AP if Fraction(Xmask(m,p,e,L))<mu/2]
    badS=[m for m in AP if Vs(m,p,k)>vp(2*q0,p)+Jp(p,k)+t]
    boundC=(M+1)*math.exp(-float(mu)/8)/q0 + p**Lam
    boundS=(M+1)*p**(-t)/q0 + 2*k
    return len(badC),boundC,len(badS),boundS,Lam
bad=0;n=0
for M in [20000, 60000, 100000]:
    for q0,a in [(1,0),(2,1),(24,7),(1024,0),(105,4)]:
        for p in [2,3,5,7,13]:
            for k in [2,3,7]:
                for t in [3,4]:
                    r=exhaust(M,q0,a,p,k,t)
                    if r is None: continue
                    bc,BC,bs,BS,Lam=r; n+=1
                    if bc>BC: bad+=1;print("   BadC FAIL",M,q0,a,p,k,bc,BC)
                    if bs>BS: bad+=1;print("   BadS FAIL",M,q0,a,p,k,t,bs,BS)
print("  exhaustive counting checks:",n," failures:",bad)
assert bad==0
# stress BadS with small L / adversarial q0 divisible by p to high power
bad=0;n=0
for M in [30000,50000]:
    for q0 in [2**8,3**6,2**5*3**3,7**4]:
        for a in [0,1,q0//2]:
            for p in [2,3,5,7]:
                for k in [2,5,16]:
                    for t in [3,6]:
                        r=exhaust(M,q0,a,p,k,t)
                        if r is None: continue
                        bc,BC,bs,BS,Lam=r;n+=1
                        if bc>BC: bad+=1;print("  BadC FAIL",M,q0,a,p,k,bc,BC,Lam)
                        if bs>BS: bad+=1;print("  BadS FAIL",M,q0,a,p,k,t,bs,BS)
print("  adversarial-AP counting checks:",n," failures:",bad)
assert bad==0
