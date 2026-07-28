#!/usr/bin/env python3
"""INDEPENDENT audit #4: reproduce every numerical claim made in prose in LEMMA_SP.md
Section 7 (remarks) and Section 8 (density calibration)."""
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
def kappa(m,p): return vp_fact(2*m,p)-2*vp_fact(m,p)
def W(m,p,k): return sum(vp(2*m-i,p) for i in range(2*k))
def Vs(m,p,k): return max(vp(2*m-i,p) for i in range(2*k))
def Jp(p,k):
    j=0
    while p**(j+1)<=2*k: j+=1
    return j
def s2(x):
    return bin(x).count('1')

k=3; P0=13; primes=list(primerange(2,P0+1))
print("primes:",primes)

def density(M,q0=1,a=0,verbose=True):
    tot=0; ok=0; perprime={p:0 for p in primes}
    m=M+((a-M)%q0)
    while m<=2*M:
        tot+=1
        good=True
        for p in primes:
            if kappa(m,p)<W(m,p,k):
                perprime[p]+=1; good=False
        if good: ok+=1
        m+=q0
    return ok,tot,perprime

for M in [10**5,10**6]:
    ok,tot,pp=density(M)
    union=sum(pp.values())/tot
    print(f"M=10^{round(math.log10(M))} q0=1 : density(i)={ok/tot:.4f}  union-sum of per-prime failure rates={union:.4f}")
    print("     per-prime failure rates:",{p:round(pp[p]/tot,4) for p in primes})

ok,tot,pp=density(10**6,24,7)
print(f"AP m=7 mod 24, M=10^6 : density(i)={ok/tot:.4f}  (|AP|={tot})")

ok,tot,pp=density(10**6,2**10,0)
print(f"AP m=0 mod 2^10, M=10^6 : density(i)={ok/tot:.4f}  (|AP|={tot})")
print("     per-prime failure rates:",{p:round(pp[p]/tot,4) for p in primes})

# remark 7.2 / sec.8 claim: "demand at p=2 is >= 11 + nu_2((2k)!)" in that AP
print("\n-- check the prose claim  W_2(m) >= 11 + nu_2((2k)!)  for m = 0 mod 2^10, k=3 --")
nu=vp_fact(2*k,2)
print("   nu_2((2k)!) = nu_2(6!) =",nu,"  so claim is W_2 >= 11+%d = %d"%(nu,11+nu))
vals=set()
m=10**6+((0-10**6)%2**10)
cnt=0;fail=0
while m<=2*10**6:
    w=W(m,2,k); vals.add(w)
    if w<11+nu: fail+=1
    cnt+=1; m+=2**10
print("   observed W_2 values:",sorted(vals),"  #m with W_2 < 11+nu_2((2k)!):",fail,"of",cnt)
print("   min W_2 =",min(vals),"  (nu_2(2m)>=11 always: TRUE by nu_2(2m)=1+nu_2(m)>=11)")

# spike rate (ii) in that AP with t = ? -- doc says 'rate 0.044' (T8.4). try t=3,4,5
print("\n-- spike-condition (ii) failure rate in AP m=0 mod 2^10, M=10^6, k=3 --")
q0=2**10
for t in [3,4,5,6]:
    m=10**6+((0-10**6)%q0); cnt=0; badspike=0
    while m<=2*10**6:
        cnt+=1
        for p in primes:
            if Vs(m,p,k)>vp(2*q0,p)+Jp(p,k)+t:
                badspike+=1; break
        m+=q0
    print(f"   t={t}: spike-failure rate = {badspike/cnt:.4f}")

# also plain interval spike rates
print("\n-- spike-condition failure rate, q0=1, M=10^6, k=3 --")
for t in [3,4,5]:
    cnt=0;badspike=0
    for m in range(10**6,2*10**6+1):
        cnt+=1
        for p in primes:
            if Vs(m,p,k)>vp(2,p)+Jp(p,k)+t: badspike+=1;break
    print(f"   t={t}: rate={badspike/cnt:.4f}")

# E_A(M) vacuity claim
print("\n-- E_A(M) = 18 exp(-sqrt(log M)/120) at reachable M --")
for M in [10**6,2**64,2**200,10**60,10**1000]:
    L=math.log(M); print(f"   M~1e{L/math.log(10):.0f}: E_A={18*math.exp(-math.sqrt(L)/120):.4f}")
print("   E_A < 1 needs sqrt(log M) > 120 log 18 = %.1f  => log M > %.4g"%(120*math.log(18),(120*math.log(18))**2))
print("   M_A(k=2) = exp(400*(4+2+1)^2) = exp(%d)"%(400*49))
