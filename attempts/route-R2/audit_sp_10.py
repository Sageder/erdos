#!/usr/bin/env python3
"""INDEPENDENT audit #10: decisive EXACT tests of the two counting bounds.
 (A) |BadS_p| computed EXACTLY at astronomically large M by CRT (the 2k classes are
     pairwise disjoint), compared with the proved bound (M+1)p^{-t}/q0 + 2k.
 (B) |BadC_p| and |BadS_p| by full EXHAUSTION over [M,2M] at reachable M
     (both bounds are proved without (H1)-(H4), so they must hold there too)."""
import math
from fractions import Fraction
from sympy import primerange

def vp(x,p):
    c=0;x=abs(x)
    while x and x%p==0: x//=p;c+=1
    return c
def sp_(x,p):
    s=0
    while x: x,r=divmod(x,p); s+=r
    return s
def vpf(x,p): return (x-sp_(x,p))//(p-1)
def digs(x,p):
    d=[]
    while x: x,r=divmod(x,p); d.append(r)
    return d
def Vs(m,p,k): return max(vp(2*m-i,p) for i in range(2*k))
def Xmask(m,p,e,L):
    d=digs(m,p); thr=-(-p//2)
    return sum(1 for j in range(e,min(L,len(d))) if d[j]>=thr)
def theta(p): return Fraction(p//2,p)
def Jp(p,k):
    j=0
    while p**(j+1)<=2*k: j+=1
    return j
def count_class(M,Q,c):
    """#{x in [M,2M] : x = c mod Q}, exact"""
    c%=Q
    first=M+((c-M)%Q)
    return 0 if first>2*M else (2*M-first)//Q+1

print("=== G-A: EXACT |BadS_p| at large M vs the proved bound ===")
bad=0; n=0; worst=0.0
for M in [2**200, 2**500, 10**300, 3**400]:
    for q0 in [1,2,24,1024,2**10*3**4,720720,2**30,3**20]:
        if q0**10>M: continue
        for a in [0,1,q0-1,q0//3]:
            a%=q0
            for k in [2,3,4,8,20,200]:
                for p in [2,3,5,7,11,13,23,31,127]:
                    for t in [3,4,6,10]:
                        e=vp(q0,p); T=vp(2*q0,p)+Jp(p,k)+t+1
                        exact=0
                        if p==2:
                            # i = 2i', 0<=i'<k ; 2^T | 2m-i  <=>  m = i' mod 2^{T-1}
                            Lam=T-1
                            for ip in range(k):
                                if (ip-a) % (p**min(e,Lam)) != 0: continue
                                if Lam<e:
                                    # class mod p^Lam coarser than the AP's p-part:
                                    # AP already inside it iff compatible; then all of AP
                                    exact+=count_class(M,q0,a); continue
                                Q=q0*p**(Lam-e)
                                # unique r mod p^Lam is ip ; combine with a mod q0
                                # find x = a mod q0, x = ip mod p^Lam  (consistent, checked)
                                # CRT: modulus q0*p^{Lam-e}
                                x=None
                                q_=q0//p**e
                                # solve x = ip mod p^Lam and x = a mod q_
                                # (p^Lam, q_) coprime
                                inv=pow(p**Lam % q_, -1, q_) if q_>1 else 0
                                if q_>1:
                                    tt=((a-ip)%q_)*inv % q_
                                    x=ip+p**Lam*tt
                                else:
                                    x=ip
                                assert x%q0==a%q0 and x%(p**Lam)==ip%(p**Lam)
                                exact+=count_class(M,Q,x)
                        else:
                            inv2=pow(2,-1,p**T)
                            for i in range(2*k):
                                r=(i*inv2)%(p**T)
                                if (r-a)%(p**min(e,T))!=0: continue
                                Q=q0*p**(T-e)
                                q_=q0//p**e
                                if q_>1:
                                    inv=pow(p**T % q_, -1, q_)
                                    tt=((a-r)%q_)*inv % q_
                                    x=r+p**T*tt
                                else:
                                    x=r
                                assert x%q0==a%q0 and x%(p**T)==r
                                exact+=count_class(M,Q,x)
                        bound=(M+1)*Fraction(1,p**t)/q0 + 2*k
                        n+=1
                        if exact>bound:
                            bad+=1
                            print("  *** BadS BOUND VIOLATED",M.bit_length(),q0,a,k,p,t,exact,float(bound))
                        else:
                            worst=max(worst, float(Fraction(exact)/bound) if bound>0 else 0)
print(f"  exact BadS checks: {n}  violations: {bad}   worst exact/bound ratio: {worst:.4f}")
assert bad==0

print("=== G-B: EXHAUSTIVE |BadC_p|, |BadS_p| over all of [M,2M] at reachable M ===")
def Lp_small(M,p):
    L=0
    while p**(5*(L+1))<=M**4: L+=1
    return L
bad=0;n=0
for M in [20000,50000,100000]:
    for (q0,a) in [(1,0),(2,1),(6,5),(24,7),(105,4),(1024,0),(2401,100),(2**5*3**3,16),(3**6,4)]:
        for p in [2,3,5,7,13]:
            for k in [2,3,7,16]:
                for t in [3,4,6]:
                    e=vp(q0,p); L=Lp_small(M,p)
                    if L<e: continue
                    Lam=L-e; mu=theta(p)*Lam
                    bc=0;bs=0;tot=0
                    m=M+((a-M)%q0)
                    while m<=2*M:
                        tot+=1
                        if Fraction(Xmask(m,p,e,L))<mu/2: bc+=1
                        if Vs(m,p,k)>vp(2*q0,p)+Jp(p,k)+t: bs+=1
                        m+=q0
                    BC=(M+1)*math.exp(-float(mu)/8)/q0 + p**Lam
                    BS=float((M+1)*Fraction(1,p**t)/q0 + 2*k)
                    n+=1
                    if bc>BC: bad+=1; print("  *** BadC VIOLATED",M,q0,a,p,k,bc,BC)
                    if bs>BS: bad+=1; print("  *** BadS VIOLATED",M,q0,a,p,k,t,bs,BS)
print(f"  exhaustive checks: {n}  violations: {bad}")
assert bad==0
print("DONE")
