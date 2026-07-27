"""Verify the PROBLEM.md §per-prime identity chain (PROMPT §2), re-derived independently.

Claims tested (all must PASS):
 (I1) Legendre digit form: nu_p(m!) == (m - s_p(m))/(p-1) on random (m,p).
 (I2) criterion equivalence: [forall p: nu_p((2n)!) >= 2 nu_p((n+k)!)]
      == [forall p: 2 s_p(n+k) - s_p(2n) >= 2k]  (per-prime, not just aggregate).
 (I3) Kummer form A: carries((n+k)+(n-k), p) == nu_p(C(2n, n+k)); membership
      <=> forall p: carries((n+k)+(n-k),p) >= nu_p(prod_{j=n-k+1}^{n+k} j).
 (I4) Kummer form B: carries((n+k)+(n+k), p) == nu_p(C(2n+2k, n+k)); membership
      <=> forall p: carries >= nu_p(prod_{j=1}^{2k} (2n+j)).
 (I5) carries-vs-borrows identity: 2 s_p(m) - s_p(2m-2k) - 2k == (p-1)(c_p - b_p) + s_p(2k) - 2k,
      with c_p = carries(m+m,p), b_p = borrows(2m - 2k, p), m = n+k. On random triples.
 (I6) c_p == nu_p(C(2m,m)), b_p == nu_p(C(2m,2k)), and 2k - s_p(2k) == (p-1) nu_p((2k)!).
 (I7) product forms: n in S_k <=> prod_{j=n-k+1}^{n+k} j | C(2n,n+k)
                              <=> prod_{j=1}^{2k}(2n+j) | C(2n+2k,n+k)
                              <=> (2m)(2m-1)...(2m-2k+1) | C(2m,m), m=n+k  [exact bigint].
 (I8) large-prime criterion: for p > max(sqrt(2n), 2k), condition at p holds iff
      (n+k) mod p >= k, iff p has no multiple in (n, n+k].

Deterministic seed. Exact arithmetic only.
"""
import sys, random, math
sys.path.insert(0, '.')
from erdos727 import s_p, nu_p_factorial, carries_add, borrows_sub, in_Sk_bigint
from sympy import primerange, prime, factorial, binomial

random.seed(727)
ok = True


def nu_p_int(m, p):
    v = 0
    while m % p == 0:
        m //= p
        v += 1
    return v


def report(name, passed, detail=""):
    global ok
    print(f"{name}: {'PASS' if passed else 'FAIL ' + detail}", flush=True)
    ok &= passed


# I1
bad = []
for _ in range(3000):
    m = random.randrange(1, 10**7)
    p = prime(random.randrange(1, 100))
    v = 0
    q = m
    while q:
        q //= p
        v += q
    # recompute Legendre floor-sum directly
    fs = sum(m // p**i for i in range(1, 40) if p**i <= m)
    if not (nu_p_factorial(m, p) == fs):
        bad.append((m, p))
report("I1 Legendre digit form", not bad, str(bad[:3]))

# I2 per-prime equivalence
bad = []
for _ in range(2000):
    n = random.randrange(1, 5000)
    k = random.randrange(1, 7)
    p = prime(random.randrange(1, 200))
    lhs = nu_p_factorial(2 * n, p) >= 2 * nu_p_factorial(n + k, p)
    rhs = 2 * s_p(n + k, p) - s_p(2 * n, p) >= 2 * k
    if lhs != rhs:
        bad.append((n, k, p))
report("I2 per-prime digit equivalence", not bad, str(bad[:3]))

# I3 + I4 Kummer forms
bad3, bad4 = [], []
for _ in range(1500):
    n = random.randrange(10, 3000)
    k = random.randrange(1, 6)
    if n <= k:
        continue
    p = prime(random.randrange(1, 150))
    c_lo = carries_add(n + k, n - k, p)
    if c_lo != nu_p_int(binomial(2 * n, n + k), p):
        bad3.append(('kummerA', n, k, p))
    prod_win = 1
    for j in range(n - k + 1, n + k + 1):
        prod_win *= j
    lhsA = c_lo >= nu_p_int(prod_win, p)
    memA = nu_p_factorial(2 * n, p) >= 2 * nu_p_factorial(n + k, p)
    if lhsA != memA:
        bad3.append(('critA', n, k, p))
    c_hi = carries_add(n + k, n + k, p)
    if c_hi != nu_p_int(binomial(2 * n + 2 * k, n + k), p):
        bad4.append(('kummerB', n, k, p))
    prod_top = 1
    for j in range(1, 2 * k + 1):
        prod_top *= 2 * n + j
    lhsB = c_hi >= nu_p_int(prod_top, p)
    if lhsB != memA:
        bad4.append(('critB', n, k, p))
report("I3 Kummer form A (low addition)", not bad3, str(bad3[:3]))
report("I4 Kummer form B (doubling)", not bad4, str(bad4[:3]))

# I5 + I6 carries-vs-borrows
bad5, bad6 = [], []
for _ in range(20000):
    n = random.randrange(10, 10**6)
    k = random.randrange(1, 8)
    p = prime(random.randrange(1, 300))
    m = n + k
    c = carries_add(m, m, p)
    b = borrows_sub(2 * m, 2 * k, p)
    lhs = 2 * s_p(m, p) - s_p(2 * m - 2 * k, p) - 2 * k
    rhs = (p - 1) * (c - b) + s_p(2 * k, p) - 2 * k
    if lhs != rhs:
        bad5.append((n, k, p))
    if c != nu_p_int(binomial(2 * m, m), p) or b != nu_p_int(binomial(2 * m, 2 * k), p) \
       or 2 * k - s_p(2 * k, p) != (p - 1) * nu_p_factorial(2 * k, p):
        bad6.append((n, k, p))
report("I5 carries-vs-borrows identity (2e4 random triples)", not bad5, str(bad5[:3]))
report("I6 c=nu(C(2m,m)), b=nu(C(2m,2k)), Legendre-(2k)", not bad6, str(bad6[:3]))

# I7 product forms (exact bigint, small range)
bad = []
for k in range(1, 5):
    for n in range(k, 260):
        m = n + k
        mem = in_Sk_bigint(n, k)
        pw = 1
        for j in range(n - k + 1, n + k + 1):
            pw *= j
        f1 = binomial(2 * n, n + k) % pw == 0
        pt = 1
        for j in range(1, 2 * k + 1):
            pt *= 2 * n + j
        f2 = binomial(2 * n + 2 * k, n + k) % pt == 0
        pt2 = 1
        for i in range(0, 2 * k):
            pt2 *= 2 * m - i
        f3 = binomial(2 * m, m) % pt2 == 0
        if not (mem == f1 == f2 == f3):
            bad.append((n, k, mem, f1, f2, f3))
report("I7 product forms (bigint, k<=4, n<260)", not bad, str(bad[:3]))

# I8 large-prime criterion
bad = []
for _ in range(20000):
    n = random.randrange(50, 10**6)
    k = random.randrange(1, 8)
    lo = max(math.isqrt(2 * n), 2 * k)
    # pick a random prime in (lo, n+k]
    for _try in range(10):
        p = prime(random.randrange(1, 80000))
        if lo < p <= n + k:
            break
    else:
        continue
    cond = 2 * s_p(n + k, p) - s_p(2 * n, p) >= 2 * k
    r = (n + k) % p
    pred = r >= k
    mult = any((n + j) % p == 0 for j in range(1, k + 1))
    if cond != pred or pred == mult:
        bad.append((n, k, p, cond, pred, mult))
report("I8 large-prime criterion", not bad, str(bad[:3]))

print("IDENTITIES:", "ALL PASS" if ok else "FAILURE")
