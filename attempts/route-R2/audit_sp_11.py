#!/usr/bin/env python3
"""INDEPENDENT audit #11: broad randomized counterexample hunt for Master Lemma part (1),
gated on SP.9's exact conclusion.  Rate diagnostics done in LOG space with a Poisson
(not Gaussian) tail criterion, since the bad events are extremely rare."""
import math,random,sys
from fractions import Fraction
from sympy import primerange
random.seed(20260728)

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
def vpf(x,p): return (x-sp_(x,p))//(p-1)
def kappa(m,p): return (2*sp_(m,p)-sp_(2*m,p))//(p-1)
def W(m,p,k): return sum(vp(2*m-i,p) for i in range(2*k))
def Vs(m,p,k): return max(vp(2*m-i,p) for i in range(2*k))
def theta(p): return Fraction(p//2,p)
def Jp(p,k):
    j=0
    while p**(j+1)<=2*k: j+=1
    return j
def Lp(M,p):
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

tot=0;cfg=0;skip=0;mt=0;gt=0
flagC=0;flagS=0;pairs=0
for bits in [400,900,1800]:
    M=2**bits; logM1=math.log(M+1)
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
                                    print("  *** COUNTEREXAMPLE",bits,k,q0,a,P,t,m,p);sys.stdout.flush()
                    # proved per-prime rate bounds, in log space
                    for p in primes:
                        pairs+=1
                        mu=float(theta(p)*(L[p]-e[p]))
                        lrc=max(-mu/8, math.log(q0)+(L[p]-e[p])*math.log(p)-logM1)+math.log(2)
                        rc=math.exp(lrc) if lrc>-700 else 0.0
                        lrs=max(-t*math.log(p), math.log(2*k*q0)-logM1)+math.log(2)
                        rs=math.exp(lrs)
                        # Poisson upper tail: P(Bin(N,rate) >= obs) small?
                        def ptail(obs,rate):
                            lam=N*rate; s=0.0
                            for j in range(obs):
                                s+=math.exp(-lam+j*math.log(lam) - math.lgamma(j+1)) if lam>0 else (1.0 if j==0 else 0)
                            return max(0.0,1-s)
                        if nb[p]>0 and ptail(nb[p],rc)<1e-6: flagC+=1;print("   C-tail",bits,k,q0,P,t,p,nb[p],rc)
                        if nsp[p]>0 and ptail(nsp[p],rs)<1e-6: flagS+=1;print("   S-tail",bits,k,q0,P,t,p,nsp[p],rs)
print(f"configs={cfg} skipped={skip} m tested={mt} |G|={gt} criterion violations={tot}")
print(f"prime-config pairs={pairs};  Poisson-implausible BadC excesses={flagC}, BadS excesses={flagS}")
assert tot==0
print("DONE")
