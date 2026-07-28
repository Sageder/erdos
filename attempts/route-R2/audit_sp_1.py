#!/usr/bin/env python3
"""INDEPENDENT audit script #1 for LEMMA_SP.md.  Written from scratch by the auditor.
Exact integer arithmetic only.  No import of verify_sp.py."""
import math, random
from fractions import Fraction
from sympy import primerange, factorial, binomial, primepi

random.seed(20260728)

# ---------- primitives (written from scratch) ----------
def vp(x, p):
    """nu_p(x) for x != 0"""
    assert x != 0
    c = 0
    x = abs(x)
    while x % p == 0:
        x //= p; c += 1
    return c

def sp(x, p):
    s = 0
    while x > 0:
        s += x % p; x //= p
    return s

def vp_fact(x, p):
    """Legendre, by direct summation of floors"""
    s = 0; q = p
    while q <= x:
        s += x // q
        q *= p
    return s

def digits(x, p):
    d = []
    while x > 0:
        d.append(x % p); x //= p
    return d

def kappa(m, p):
    """nu_p(binom(2m,m)) computed by Legendre floors (independent of Kummer)"""
    return vp_fact(2*m, p) - 2*vp_fact(m, p)

def W(m, p, k):
    return sum(vp(2*m - i, p) for i in range(2*k))

def V(m, p, k):
    return max(vp(2*m - i, p) for i in range(2*k))

def carries(m, p):
    """count carries in base-p addition m+m, by the explicit recursion"""
    a = digits(m, p); c = 0; C = 0
    for aj in a:
        s = 2*aj + c
        c = 1 if s >= p else 0
        C += c
    return C

# ---------- T-A1: criterion implementations vs PROBLEM.md sanity data ----------
def in_Sk_direct(n, k):
    """literal ((n+k)!)^2 | (2n)!  by prime valuations over all p <= n+k"""
    if 2*n < 2*(n+k):
        pass
    for p in primerange(2, n+k+1):
        if vp_fact(2*n, p) < 2*vp_fact(n+k, p):
            return False
    return True

def in_Sk_digit(n, k):
    """forall p: 2 s_p(n+k) - s_p(2n) >= 2k"""
    for p in primerange(2, n+k+1):
        if 2*sp(n+k, p) - sp(2*n, p) < 2*k:
            return False
    return True

def in_Sk_kappaW(n, k):
    """forall p: kappa_p(m) >= W_p(m), m = n+k  (the LEMMA_SP form)"""
    m = n + k
    if n < k:
        return None
    for p in primerange(2, 2*m+1):
        if kappa(m, p) < W(m, p, k):
            return False
    return True

def in_Sk_product(n, k):
    """prod_{j=n-k+1}^{n+k} j | binom(2n, n+k)"""
    if n < k: return None
    num = 1
    for j in range(n-k+1, n+k+1):
        num *= j
    return binomial(2*n, n+k) % num == 0

def in_Sk_bruteforce(n, k):
    """literal factorial divisibility (only for tiny n)"""
    return factorial(2*n) % (factorial(n+k)**2) == 0

print("=== A1: criterion implementations agree + match PROBLEM.md data ===")
# tiny brute-force cross check
for k in (1,2,3):
    for n in range(k, 60):
        a = in_Sk_direct(n,k); b = in_Sk_digit(n,k); c = in_Sk_kappaW(n,k)
        d = in_Sk_product(n,k); e = bool(in_Sk_bruteforce(n,k))
        assert a==b==c==d==e, (n,k,a,b,c,d,e)
print("  brute force vs 4 implementations: OK (k=1,2,3; n<60)")

S1 = [n for n in range(1, 442) if in_Sk_direct(n,1)]
print("  S_1 prefix:", S1[:14], " count<=441:", len(S1))
assert S1[:14] == [5,14,27,41,44,65,76,90,109,125,139,152,155,169], S1[:14]
assert len(S1) == 40, len(S1)
print("  S_1 matches PROBLEM.md (prefix + 40 elements up to 441): OK")

S2 = [n for n in range(1, 3600) if in_Sk_direct(n,2)]
print("  S_2 prefix:", S2[:20])
assert S2[0] == 208
assert S2[:20] == [208,458,987,1220,1455,1597,1889,2012,2144,2330,2477,2663,2991,
                   3353,3415,3430,3439,3475,3476,3551], S2[:20]
print("  S_2 matches PROBLEM.md prefix: OK")

S3 = [n for n in range(1, 19300) if in_Sk_direct(n,3)]
print("  S_3 prefix:", S3[:8])
assert S3[:8] == [3475,8174,8175,15195,16168,18682,18743,19290], S3[:8]
print("  S_3 matches PROBLEM.md prefix: OK")

# ---------- T-A2: SP.0 identity ----------
print("=== A2: SP.0 identity  nu_p((2n)!) - 2 nu_p((n+k)!) = kappa_p(m) - W_p(m) ===")
bad = 0
for _ in range(4000):
    k = random.randint(1, 12)
    m = random.randint(k, 40000)
    n = m - k
    p = random.choice(list(primerange(2, 200)))
    lhs = vp_fact(2*n, p) - 2*vp_fact(n+k, p)
    rhs = kappa(m, p) - W(m, p, k)
    if lhs != rhs:
        bad += 1; print("   FAIL", k, m, p, lhs, rhs)
print("  SP.0 failures in 4000 random instances:", bad)
assert bad == 0

# also the boundary m = k (n = 0)
for k in range(1, 8):
    for p in list(primerange(2, 30)):
        m = k; n = 0
        lhs = vp_fact(0, p) - 2*vp_fact(k, p)
        rhs = kappa(m, p) - W(m, p, k)
        assert lhs == rhs, (k, p, lhs, rhs)
print("  SP.0 at boundary m=k (n=0): OK")

# ---------- T-A3: SP.K Kummer, SP.1 ----------
print("=== A3: SP.K (kappa = carries) and SP.1 (kappa_2 = s_2) ===")
bad = 0
for _ in range(4000):
    m = random.randint(1, 10**7)
    p = random.choice(list(primerange(2, 300)))
    if kappa(m, p) != carries(m, p): bad += 1
    if (2*sp(m,p) - sp(2*m,p)) % (p-1) != 0: bad += 1
    if kappa(m,p) != (2*sp(m,p) - sp(2*m,p))//(p-1): bad += 1
for m in range(1, 5000):
    if kappa(m,2) != sp(m,2): bad += 1
print("  failures:", bad); assert bad == 0

# ---------- T-A4: SP.2 and its exact refinement ----------
print("=== A4: SP.2  W_p(m) <= nu_p((2k)!) + V_p(m)  and refinement ===")
bad = 0; tight = 0; tot = 0
for _ in range(6000):
    k = random.randint(1, 20)
    m = random.randint(k, 10**6)
    p = random.choice(list(primerange(2, 120)))
    w = W(m,p,k); v = V(m,p,k); b = vp_fact(2*k, p)
    tot += 1
    if w > b + v: bad += 1; print("   SP.2 FAIL", k,m,p,w,b,v)
    if w == b + v: tight += 1
    # refinement W = nu_p(binom(2m,2k)) + nu_p((2k)!)
    ref = vp_fact(2*m, p) - vp_fact(2*m-2*k, p) - vp_fact(2*k,p) + vp_fact(2*k,p)
    assert w == vp_fact(2*m,p) - vp_fact(2*m-2*k,p), (k,m,p)
    assert w == (vp_fact(2*m,p)-vp_fact(2*m-2*k,p)-vp_fact(2*k,p)) + vp_fact(2*k,p)
print("  SP.2 failures:", bad, " (tight in", tight, "of", tot, "cases)")
assert bad == 0
# exhaustive small check
bad = 0
for k in range(1, 9):
    for p in list(primerange(2, 40)):
        for m in range(k, 3000):
            if W(m,p,k) > vp_fact(2*k,p) + V(m,p,k): bad += 1
print("  SP.2 exhaustive small (k<=8,p<40,m<3000) failures:", bad); assert bad==0

# ---------- T-A5: SP.3 masked forced carries ----------
print("=== A5: SP.3  kappa_p(m) >= X_p^{[e,L)}(m) ===")
def Xmask(m, p, e, L):
    d = digits(m, p)
    thr = -(-p//2)  # ceil(p/2)
    return sum(1 for j in range(e, L) if (d[j] if j < len(d) else 0) >= thr)
bad = 0
for _ in range(6000):
    m = random.randint(1, 10**9)
    p = random.choice(list(primerange(2, 200)))
    L = random.randint(0, 20); e = random.randint(0, L)
    if kappa(m,p) < Xmask(m,p,e,L): bad += 1
print("  failures:", bad); assert bad == 0

# theta counts
print("=== A5b: theta(p) = #large/p, large = {a : a >= ceil(p/2)} ===")
for p in list(primerange(2,60)):
    thr = -(-p//2)
    cnt = len([a for a in range(p) if a >= thr])
    assert cnt == p//2, (p, cnt)
    assert Fraction(cnt,p) >= Fraction(1,3), p
print("  #large = floor(p/2) and theta >= 1/3 for all p < 60: OK  (theta(3)=1/3 exactly)")
