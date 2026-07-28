#!/usr/bin/env python3
"""INDEPENDENT audit #8: remaining PROBLEM.md counts (validating my criterion code),
plus the two remaining prose numbers in Sec.8 of LEMMA_SP.md."""
import math
from sympy import primerange, factorint

def sp_(x,p):
    s=0
    while x: s+=x%p; x//=p
    return s

def build(limit):
    sieve=[0]*(limit+1)
    for p in primerange(2,limit+1):
        for q in range(p,limit+1,p): sieve[q]=p     # largest prime factor
    return sieve

def members(k, N):
    """n in S_k for n<=N, using: small primes p<=sqrt(2n) by digit sums;
       large primes p>sqrt(2n): condition <=> no multiple of p in (n,n+k]
       <=> n+1..n+k are sqrt(2n)-smooth.  (valid once sqrt(2n) >= 2k)"""
    lpf=build(N+k+2)
    res=[]
    for n in range(max(k,1), N+1):
        r=math.isqrt(2*n)
        if r < 2*k:      # fall back to full check for tiny n
            ok=all(2*sp_(n+k,p)-sp_(2*n,p)>=2*k for p in primerange(2,n+k+1))
            if ok: res.append(n)
            continue
        smooth=all(lpf[n+j]<=r for j in range(1,k+1))
        if not smooth: continue
        if all(2*sp_(n+k,p)-sp_(2*n,p)>=2*k for p in primerange(2,r+1)):
            res.append(n)
    return res

S2=members(2,200000); print("|S_2 cap [1,2e5]| =",len(S2), " (PROBLEM.md: 1981)")
assert len(S2)==1981
S3=members(3,60000);  print("|S_3 cap [1,6e4]|  =",len(S3), " (PROBLEM.md: 41)")
assert len(S3)==41
S4=members(4,60000);  print("S_4 cap [1,6e4]    =",S4, " (PROBLEM.md: {8174, 51984})")
assert S4==[8174,51984]
print("criterion code validated against all four PROBLEM.md counts.")

# --- Sec.8 prose: "kappa_2(m) = s_2(m) ~ 10 at that scale" in AP m=0 mod 2^10 ---
q0=2**10; tot=0; s=0; mx=0
m=10**6+((0-10**6)%q0)
while m<=2*10**6:
    v=bin(m).count('1'); s+=v; mx=max(mx,v); tot+=1; m+=q0
print(f"\nAP m=0 mod 2^10, M=1e6: mean s_2(m) = {s/tot:.3f}, max = {mx}  "
      f"(doc says 'kappa_2(m)=s_2(m) ~ 10')")
