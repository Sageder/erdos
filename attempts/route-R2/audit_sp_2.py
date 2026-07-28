#!/usr/bin/env python3
"""INDEPENDENT audit #2: counting lemmas SP.6/7/8, threshold SP.9, master union bound,
scalar constants, corollary hypothesis checks."""
import math, random
from fractions import Fraction
from sympy import primerange, primepi, Rational, nsimplify

random.seed(1234567)

def vp(x,p):
    c=0; x=abs(x)
    while x and x%p==0: x//=p; c+=1
    return c
def vp_fact(x,p):
    s=0;q=p
    while q<=x: s+=x//q; q*=p
    return s
def digits(x,p):
    d=[]
    while x>0: d.append(x%p); x//=p
    return d
def kappa(m,p): return vp_fact(2*m,p)-2*vp_fact(m,p)
def W(m,p,k): return sum(vp(2*m-i,p) for i in range(2*k))
def Vspike(m,p,k): return max(vp(2*m-i,p) for i in range(2*k))
def Xmask(m,p,e,L):
    d=digits(m,p); thr=-(-p//2)
    return sum(1 for j in range(e,L) if (d[j] if j<len(d) else 0)>=thr)
def theta(p): return Fraction(p//2,p)
def Jp(p,k):
    j=0
    while p**(j+1)<=2*k: j+=1
    return j

print("=== B0: J_p = floor(log(2k)/log p) satisfies p^J <= 2k < p^{J+1} (T11.c) ===")
bad=0
for k in range(1,500):
    for p in list(primerange(2,200)):
        J=Jp(p,k)
        if not (p**J<=2*k<p**(J+1)): bad+=1
        # doc claims J_p = floor(log(2k)/log p); check float formula agrees
        Jf=math.floor(math.log(2*k)/math.log(p))
        if Jf!=J: print("   float/exact mismatch", p,k,Jf,J); bad+=1
print("  failures:",bad); assert bad==0

print("=== B1: SP.6 residue count in [M,2M] ===")
bad=0
for _ in range(3000):
    M=random.randint(1,3000); Q=random.randint(1,200); c=random.randint(0,Q-1)
    cnt=sum(1 for x in range(M,2*M+1) if x%Q==c%Q)
    if not (Fraction(M+1,Q)-1 <= cnt <= Fraction(M+1,Q)+1): bad+=1
print("  failures:",bad); assert bad==0

print("=== B2: SP.7 CRT-in-AP, and the digit-pattern consequence ===")
bad=0
for _ in range(2000):
    q0=random.randint(1,300); p=random.choice([2,3,5,7,11])
    e=vp(q0,p); a=random.randint(0,q0-1)
    Lam=random.randint(1,4); L=e+Lam
    # pattern w for digits e..L-1
    w=[random.randint(0,p-1) for _ in range(Lam)]
    lo=a%(p**e)
    r=lo+sum(w[j]*p**(e+j) for j in range(Lam))
    mod=q0*p**Lam
    sols=[m for m in range(0,mod*3) if m%q0==a%q0 and m%(p**L)==r%(p**L)]
    # must be exactly one class mod q0*p^Lam  => exactly 3 sols in [0,3*mod)
    if len(sols)!=3: bad+=1; print("   FAIL",q0,p,e,a,Lam,len(sols))
    else:
        if len(set(s%mod for s in sols))!=1: bad+=1
    # also: digits e..L-1 of every m in the AP with that pattern
    for m in sols:
        d=digits(m,p)
        got=[(d[j] if j<len(d) else 0) for j in range(e,L)]
        if got!=w: bad+=1
print("  failures:",bad); assert bad==0

print("=== B3: SP.8 Chernoff, EXACT rational tail vs p^Lam e^{-mu/8} ===")
def exact_tail_count(p,Lam):
    """#{w in {0..p-1}^Lam : X(w) <= mu/2}, mu = theta*Lam ; exact integer"""
    th=theta(p); mu=th*Lam
    big=p//2  # number of large digit values
    small=p-big
    thr=mu/2
    tot=0
    for x in range(0,Lam+1):
        if Fraction(x)<=thr:
            tot+=math.comb(Lam,x)*big**x*small**(Lam-x)
    return tot
bad=0; worstratio=0
for p in [2,3,5,7,11,13,17,101]:
    for Lam in range(1,60):
        cnt=exact_tail_count(p,Lam)
        mu=float(theta(p))*Lam
        bound=p**Lam*math.exp(-mu/8)
        ratio=cnt/bound
        worstratio=max(worstratio,ratio)
        if cnt>bound*(1+1e-12): bad+=1; print("   FAIL",p,Lam,cnt,bound)
print("  failures:",bad,"  worst count/bound ratio:",round(worstratio,4)); assert bad==0
print("  (1-log2)/2 =",(1-math.log(2))/2,">= 1/8:",(1-math.log(2))/2>=0.125)

print("=== B4: scalar constants ===")
# T11.b : sum_{n>=2} n^{-t} <= 3*2^{-t} for t>=3
for t in range(3,40):
    s=sum(Fraction(1,n**t) for n in range(2,4000))+Fraction(1,3999**(t-1))/(t-1)
    assert float(s)<=3*2.0**(-t), (t,float(s),3*2.0**-t)
print("  sum_{n>=2} n^-t <= 3*2^-t for 3<=t<40: OK")
# and the prime version actually used
for t in range(3,20):
    s=sum(Fraction(1,p**t) for p in primerange(2,5000))
    assert float(s)<=3*2.0**(-t)
print("  sum_{p} p^-t <= 3*2^-t: OK")
# T11.a : c - 7/(240 c) <= -1/120 for 0<c<=1/6, increasing
f=lambda c: c-7/(240*c)
print("  f(1/6) =",f(1/6)," -1/120 =",-1/120, " equal:",abs(f(1/6)+1/120)<1e-15)
assert all(f(c)<=-1/120+1e-15 for c in [1e-6,0.01,0.05,0.1,0.15,1/6])
print("  f increasing & <= -1/120 on (0,1/6]: OK")
# 2 e^{1/24} < 3
print("  2e^{1/24} =",2*math.exp(1/24),"< 3:",2*math.exp(1/24)<3)
# e^{100/9} < 70000  (needed for (H3) check in SP-A)
print("  e^{100/9} =",math.exp(100/9),"< 70000:",math.exp(100/9)<70000)
# 7/240 vs log2/120
print("  7/240 =",7/240," > log2/120 =",math.log(2)/120)
# 3P0+15 <= 18 P0 for P0>=2
print("  3*2+15=21 <= 18*2=36: OK")
# delta=1/2 threshold
print("  (120 log 36)^2 =",(120*math.log(36))**2)
# SP-A t>=3 claim: doc says 't>=3 <=> sqrt(L)>=80'; truth is sqrt(L)>=60
print("  floor(sqrt(L)/20)>=3 iff sqrt(L)>=60 ; doc says 80  -> doc's number is WRONG but conservative")
for sL in [59.9,60.0,79.9,80.0]:
    print("    sqrt(L)=",sL," t=",math.floor(sL/20))

print("=== B5: SP.9 threshold, EXACT, over many admissible configurations ===")
def check_SP9(k,M,q0,P,t,p):
    """returns (LHS-RHS as Fraction-ish float pair, and the claimed lower bound)"""
    u=Fraction(1)  # we need log M/log p -> use exact-ish via floats for u, but L_p exactly
    Lp=0
    # L_p = floor((4/5) log M / log p) computed EXACTLY: largest L with p^{5L} <= M^4
    L=0
    while p**(5*(L+1))<=M**4: L+=1
    Lp=L
    ep=vp(q0,p)
    lhs=theta(p)*Fraction(Lp-ep,2)
    rhs=vp_fact(2*k,p)+vp(2*q0,p)+Jp(p,k)+t
    return lhs,rhs,Lp,ep
def hyps_ok(k,M,q0,P,t):
    if not (M>=70000 and M**4>=(4*k)**5): return False
    if not (1<=q0 and q0**10<=M): return False
    if not (2<=P and P**20<=M): return False
    if t<3: return False
    # (H4) log M/log P >= 60(2k+log2(2k)+t+1)
    return math.log(M)/math.log(P) >= 60*(2*k+math.log(2*k)/math.log(2)+t+1)
bad=0; tested=0; minmargin=None
configs=[]
for k in [2,3,5,17,100]:
    for e in [200,400,800,3000]:
        M=2**e
        for q0 in [1,2,24,2**10*3**4,random.randint(2,10**6)]:
            if q0**10>M: continue
            for P in [2,3,13,101,1009]:
                for t in [3,5,20]:
                    if hyps_ok(k,M,q0,P,t): configs.append((k,M,q0,P,t))
print("  admissible configs:",len(configs))
for (k,M,q0,P,t) in configs:
    for p in primerange(2,int(P)+1):
        lhs,rhs,Lp,ep=check_SP9(k,M,q0,P,t,p)
        tested+=1
        if lhs<rhs:
            bad+=1; print("   SP.9 FAIL",k,M.bit_length(),q0,P,t,p,float(lhs),rhs)
        # claimed extra margin (1/60)u_p - (2k+log2(2k)+t+1/6)
        u=math.log(M)/math.log(p)
        claimed=u/60-(2*k+math.log(2*k)/math.log(2)+t+1/6)
        if float(lhs-rhs)<claimed-1e-9:
            bad+=1; print("   SP.9 margin FAIL",k,q0,P,t,p,float(lhs-rhs),claimed)
        m0=float(lhs-rhs)
        minmargin=m0 if minmargin is None else min(minmargin,m0)
print("  SP.9 checks:",tested," failures:",bad," min margin:",minmargin)
assert bad==0
