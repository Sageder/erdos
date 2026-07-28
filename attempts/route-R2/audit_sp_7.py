#!/usr/bin/env python3
"""INDEPENDENT audit #7: broad randomized sweep of Master Lemma part (1) and of the
per-prime bad-set bounds, at M large enough that the SP.9 CONCLUSION genuinely holds
with the lemma's own L_p = floor((4/5) log M / log p).  Exact integer arithmetic."""
import math,random
from fractions import Fraction
from sympy import primerange
random.seed(4242)

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
    M4=M**4; hi=1
    while pow(p,5*hi)<=M4: hi*=2
    lo,hi2=hi//2,hi
    while lo<hi2-1:
        mid=(lo+hi2)//2
        if pow(p,5*mid)<=M4: lo=mid
        else: hi2=mid
    return lo

tot=0; gt=0; viol=0; cfgs=0; skipped=0
rates=[]
for bits in [200,400,800,1600]:
    M=2**bits
    for k in [2,3,4,8,20,50]:
        for q0 in [1,2,24,1024,2**10*3**4,720720,2**20]:
            if q0**10>M: continue
            a=random.randrange(q0)
            for P in [2,3,7,13,31,127]:
                for t in [3,6]:
                    primes=list(primerange(2,P+1))
                    e={p:vp(q0,p) for p in primes}; L={p:Lp(M,p) for p in primes}
                    if any(L[p]<e[p] for p in primes): skipped+=1; continue
                    if not all(theta(p)*Fraction(L[p]-e[p],2)
                               >= vp_fact(2*k,p)+vp(2*q0,p)+Jp(p,k)+t for p in primes):
                        skipped+=1; continue
                    cfgs+=1
                    lo=M+((a-M)%q0); span=(2*M-lo)//q0
                    nb={p:0 for p in primes}; ns={p:0 for p in primes}; N=300
                    for _ in range(N):
                        m=lo+q0*random.randint(0,span); tot+=1
                        good=True
                        for p in primes:
                            if Fraction(Xmask(m,p,e[p],L[p]))<theta(p)*Fraction(L[p]-e[p],2):
                                nb[p]+=1; good=False
                            if Vs(m,p,k)>vp(2*q0,p)+Jp(p,k)+t:
                                ns[p]+=1; good=False
                        if good:
                            gt+=1
                            for p in primes:
                                if kappa(m,p)<W(m,p,k):
                                    viol+=1
                                    print("  *** COUNTEREXAMPLE",bits,k,q0,a,P,t,m,p,kappa(m,p),W(m,p,k))
                    for p in primes:
                        mu=float(theta(p)*(L[p]-e[p]))
                        # proved per-prime rates (relative to |AP| ~ (M+1)/q0):
                        rc=math.exp(-mu/8)+q0*float(p)**(L[p]-e[p])/(M+1)
                        rs=float(p)**(-t)+2*k*q0/(M+1)
                        rates.append((nb[p]/N<=rc+4*math.sqrt(max(rc,1e-9)/N),
                                      ns[p]/N<=rs+4*math.sqrt(max(rs,1e-9)/N),
                                      p,nb[p]/N,rc,ns[p]/N,rs))
print(f"configs={cfgs} skipped={skipped} m tested={tot} |G|={gt} criterion violations={viol}")
assert viol==0
badc=sum(1 for r in rates if not r[0]); bads=sum(1 for r in rates if not r[1])
print(f"empirical BadC rate above proved bound (+4 sigma): {badc} of {len(rates)}")
print(f"empirical BadS rate above proved bound (+4 sigma): {bads} of {len(rates)}")
for r in rates:
    if not (r[0] and r[1]): print("   ", r)
print("DONE")
