"""N1: verify Proposition N and Lemma O (route R1 PROGRAM.md) against brute force.

Claims:
 (PN) For k in {2,3}, all n with 2k^2 < n <= 3*10^4: membership n in S_k (digit criterion
      over all p <= n+k) EQUALS the Prop-N predicate:
        (a) forall p <= 2k: kappa_p(m) >= W'_p(m), and
        (b) forall p > 2k dividing some n+j (j=1..k): kappa_p(floor(m / p^J)) >= J,
            J = nu_p(n+j), m = n+k.
      (All other primes contribute no constraint.)
 (LO) Lemma O: for random (m, p, i, J) with p > 2k odd, i odd < 2k, p^J || 2m - i:
      doubling m base p has >= J carries among the lowest J digits.
"""
import sys, math, random
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import s_p, carries_add, in_Sk_digit
from sympy import primerange, factorint

random.seed(20260727)

def kappa(m, p):
    return carries_add(m, m, p)

def Wp(m, p, k):
    v = 0
    for i in range(0, 2 * k):
        x = 2 * m - i
        while x % p == 0:
            v += 1
            x //= p
    return v

def propN(n, k):
    m = n + k
    for p in primerange(2, 2 * k + 1):
        if kappa(m, p) < Wp(m, p, k):
            return False
    for j in range(1, k + 1):
        for p, J in factorint(n + j).items():
            if p > 2 * k:
                if carries_add(m // p**J, m // p**J, p) < J:
                    return False
    return True

bad = []
for k in (2, 3):
    for n in range(2 * k * k + 1, 30001):
        if propN(n, k) != in_Sk_digit(n, k):
            bad.append((n, k))
            if len(bad) > 5:
                break
print(f"PN Prop-N == brute force (k=2,3, n<=3e4): {'PASS' if not bad else 'FAIL ' + str(bad[:5])}",
      flush=True)

# LO
badO = 0
tests = 0
for _ in range(30000):
    k = random.randrange(1, 6)
    p = 5
    from sympy import prime
    p = prime(random.randrange(3, 2000))
    if p <= 2 * k:
        continue
    i = random.choice([1, 3, 5, 7])
    if i >= 2 * k or i >= p:
        continue
    J = random.randrange(1, 4)
    # build 2m == i mod p^J, 2m != i mod p^(J+1): m = (i + t*p^J)/2 for suitable t
    t = random.randrange(1, 1000)
    if t % p == 0:
        t += 1
    x = i + t * p ** J           # candidate 2m - it must be even? 2m = x requires x even
    if x % 2 == 1:
        x += p ** J if (p ** J) % 2 == 1 else 1  # make even keeping x == i mod p^J
        if (x - i) % p ** J != 0 or (x - i) % p ** (J + 1) == 0:
            continue
    m = x // 2
    # verify p^J || 2m - i
    from erdos727 import s_p as _
    v = 0
    y = 2 * m - i
    while y % p == 0:
        v += 1
        y //= p
    if v != J:
        continue
    tests += 1
    # carries among lowest J digits when doubling m
    carry = 0
    low_carries = 0
    mm = m
    for pos in range(J):
        d = mm % p
        s = 2 * d + carry
        carry = 1 if s >= p else 0
        low_carries += carry
        mm //= p
    if low_carries < J:
        badO += 1
print(f"LO Lemma O ({tests} valid random cases): {'PASS' if badO == 0 else f'FAIL {badO}'}",
      flush=True)
