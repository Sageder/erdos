#!/usr/bin/env python3
"""INDEPENDENT audit #9 (fast, exact): Master Lemma parts (1) and (2) end-to-end at
   M that GENUINELY satisfies (H1)-(H4), plus a broad sweep gated on SP.9's conclusion.
   Uses Legendre in the digit-sum form nu_p(x!) = (x - s_p(x))/(p-1) (cross-validated
   against the floor-sum form in audit_sp_1.py) so big-M work is near-linear."""
import math,random,sys
from fractions import Fraction
from sympy import primerange
random.seed(31337)

def sp_(x,p):
    s=0
    while x: x,r=divmod(x,p); s+=r
    return s
def digs(x,p):
    d=[]
    while x: x,r=divmod(x,p); d.append(r)
    return d
def vp(x,p):
    c=0;x=abs(x)
    while x and x%p==0: x//=p;c+=1
    return c
def vpf(x,p):        # Legendre, digit-sum form
    return (x-sp_(x,p))//(p-1)
def kappa(m,p): return (2*sp_(m,p)-sp_(2*m,p))//(p-1)
def W(m,p,k): return sum(vp(2*m-i,p) for i in range(2*k))
def Vs(m,p,k): return max(vp(2*m-i,p) for i in range(2*k))
def theta(p): return Fraction(p//2,p)
def Jp(p,k):
    j=0
    while p**(j+1)<=2*k: j+=1
    return j
def Lp(M,p):
    """floor((4/5) log_p M): largest L with p^{5L} <= M^4, exact"""
    M4=M**4; hi=1
    while pow(p,5*hi)<=M4: hi*=2
    lo,h=hi//2,hi
    while lo<h-1:
        mid=(lo+h)//2
        if pow(p,5*mid)<=M4: lo=mid
        else: h=mid
    return lo
def Xmask(m,p,e,L):
    d=digs(m,p); thr=-(-p//2)
    return sum(1 for j in range(e,min(L,len(d))) if d[j]>=thr)

print("=== F1: end-to-end at (H1)-(H4)-COMPLIANT M  (M = P^E, E = ceil(f*(2k+log2 2k+t+1))) ===")
def run(k,P,t,q0,a,ns,f=60):
    E=max(math.ceil(f*(2*k+math.log(2*k)/math.log(2)+t+1)),20)
    M=P**E
    while M<70000 or M**4<(4*k)**5: E+=1; M=P**E
    # exact hypothesis audit
    assert M>=70000 and M**4>=(4*k)**5,"H1"
    assert 1<=q0 and q0**10<=M,"H2"
    assert 2<=P and P**20<=M,"H3"
    assert t>=3 and E>=f*(2*k+math.log(2*k)/math.log(2)+t+1),"H4"
    primes=list(primerange(2,P+1))
    L={p:Lp(M,p) for p in primes}; e={p:vp(q0,p) for p in primes}
    thr_ok=all(theta(p)*Fraction(L[p]-e[p],2)>=vpf(2*k,p)+vp(2*q0,p)+Jp(p,k)+t for p in primes)
    lam_ok=all(L[p]-e[p]>=18 for p in primes)
    lo=M+((a-M)%q0); span=(2*M-lo)//q0
    g=0;v=0;v2=0
    for _ in range(ns):
        m=lo+q0*random.randint(0,span)
        good=True
        for p in primes:
            if Fraction(Xmask(m,p,e[p],L[p]))<theta(p)*Fraction(L[p]-e[p],2): good=False;break
            if Vs(m,p,k)>vp(2*q0,p)+Jp(p,k)+t: good=False;break
        if good:
            g+=1
            for p in primes:
                d=kappa(m,p)-W(m,p,k)
                if d<0:
                    v+=1; print("  *** COUNTEREXAMPLE to part (1)",k,P,t,q0,a,m,p,d)
                if f>=120:
                    # part (2): surplus >= (1/120) log M / log p = E*log P/(120 log p)
                    if Fraction(d) < Fraction(E,120)*Fraction(math.floor(1e9*math.log(P)/math.log(p)),10**9):
                        v2+=1; print("  *** COUNTEREXAMPLE to part (2)",k,P,t,q0,a,m,p,d)
    print(f"  k={k:>3} P={P:>4} t={t} q0={q0:<10} E={E:<5} digits(M)={len(str(M)):<6}"
          f" SP.9-ok={thr_ok} Lam>=18:{lam_ok}  |G|/N={g}/{ns}  part1-viol={v} part2-viol={v2}")
    sys.stdout.flush()
    return v+v2

tot=0
for (k,P,t,q0,a,ns,f) in [
    (2,13,3,1,0,400,60), (2,13,3,24,7,400,60), (2,13,3,2**10*3**4,512,400,60),
    (3,11,4,1,0,300,60), (3,11,4,30030,11,300,60),
    (2,2,3,1,0,400,60),  (2,3,3,1,0,400,60),   (7,3,3,1,0,250,60),
    (2,101,5,1,0,150,60),(5,251,3,1,0,120,60),
    (2,13,3,1,0,250,120),(2,13,3,2**10*3**4,512,250,120),
    (3,7,3,2**20,7,200,120),
]:
    tot+=run(k,P,t,q0,a,ns,f)
print("  TOTAL violations:",tot); assert tot==0

print("=== F2: broad sweep gated on SP.9's conclusion (many k, q0, P, t) ===")
tot=0;cfg=0;skip=0;mt=0;gt=0
rate_fail=0; rate_n=0
for bits in [400,900,1800]:
    M=2**bits
    for k in [2,3,4,8,20,50,200]:
        for q0 in [1,2,24,1024,2**10*3**4,720720,2**30]:
            if q0**10>M: continue
            a=random.randrange(q0)
            for P in [2,3,7,13,31,127]:
                for t in [3,6]:
                    primes=list(primerange(2,P+1))
                    e={p:vp(q0,p) for p in primes}; L={p:Lp(M,p) for p in primes}
                    if any(L[p]<e[p] for p in primes): skip+=1;continue
                    if not all(theta(p)*Fraction(L[p]-e[p],2)
                               >=vpf(2*k,p)+vp(2*q0,p)+Jp(p,k)+t for p in primes):
                        skip+=1;continue
                    cfg+=1
                    lo=M+((a-M)%q0); span=(2*M-lo)//q0; N=120
                    nb={p:0 for p in primes}; nsp={p:0 for p in primes}
                    for _ in range(N):
                        m=lo+q0*random.randint(0,span); mt+=1; good=True
                        for p in primes:
                            if Fraction(Xmask(m,p,e[p],L[p]))<theta(p)*Fraction(L[p]-e[p],2):
                                nb[p]+=1; good=False
                            if Vs(m,p,k)>vp(2*q0,p)+Jp(p,k)+t:
                                nsp[p]+=1; good=False
                        if good:
                            gt+=1
                            for p in primes:
                                if kappa(m,p)<W(m,p,k):
                                    tot+=1
                                    print("  *** COUNTEREXAMPLE",bits,k,q0,a,P,t,m,p)
                    for p in primes:
                        mu=float(theta(p)*(L[p]-e[p]))
                        rc=math.exp(-mu/8)+q0*float(p)**(L[p]-e[p])/(M+1)
                        rs=float(p)**(-t)+2*k*q0/(M+1)
                        rate_n+=2
                        if nb[p]/N>rc+4*math.sqrt(max(rc,1e-12)/N): rate_fail+=1;print("   badC-rate>bound",p,nb[p]/N,rc)
                        if nsp[p]/N>rs+4*math.sqrt(max(rs,1e-12)/N): rate_fail+=1;print("   badS-rate>bound",p,nsp[p]/N,rs)
print(f"  configs={cfg} skipped={skip} m tested={mt} |G|={gt} criterion violations={tot}")
print(f"  empirical rates exceeding the PROVED per-prime bounds (+4 sigma): {rate_fail} of {rate_n}")
assert tot==0
print("DONE")
