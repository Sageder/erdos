"""MIRROR THEOREM verification: why 727 is the hard mirror image of 728/729/401.

With m = n + k, the 727 criterion is (verified elsewhere):
    n in S_k  <=>  prod_{i=0}^{2k-1} (2m - i)  |  C(2m, m),
i.e. for every prime p:  kappa_p(m) >= nu_p(prod_{i=0}^{2k-1}(2m-i)),  kappa_p = #carries in m+m.

The divisor slots split into three residue types for a prime power p^J dividing a slot:
  TYPE A  (m = -i mod p^J, i >= 1 small): base-p digits of m are (p-i, p-1, ..., p-1):
          ALL >= ceil(p/2)  ==>  J carries FREE.        [this is the 728/729/401 situation:
          their divisors are (m+1)...(m+k), i.e. p^J | m+i]
  TYPE B  (2m = i mod p^J, i odd): m = (p^J + i)/2 mod p^J, digits ((p+i)/2, (p-1)/2, ...):
          ALL >= ceil(p/2) for p odd  ==>  J carries FREE.   [727's odd slots 2m-1, 2m-3, ...]
  TYPE C  (m = i mod p^J, i >= 0 small): digits (i, 0, 0, ..., 0): ALL SMALL
          ==>  ZERO carries from positions < J; the J carries must come from positions >= J.
          [727's even slots 2m-2i = 2(m-i)  <=>  p^J | m-i  --- THE DIFFICULTY]

Claims tested:
 (M1) the criterion/product form (re-verified independently here);
 (M2) TYPE A: p^J || m+i, 1 <= i <= k, p > 2k  ==> at least J carries among positions < J;
 (M3) TYPE B: p^J || 2m-i, i odd, p > 2k odd  ==> at least J carries among positions < J;
 (M4) TYPE C: p^J || m-i, 0 <= i <= k-1, p > 2k, i < p  ==> ZERO carries among positions < J
      (so all J carries must come from positions >= J);
 (M5) CONSEQUENCE (necessity of smoothness): if p^J || m-i (type C) and p^{2J} > 2m then
      n not in S_k. Verified by exhaustive counterexample search.
Exact integer arithmetic; deterministic.
"""
import sys, math
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import carries_add, in_Sk_digit
from sympy import primerange, factorint, binomial

def digits(x, p):
    d = []
    while x:
        d.append(x % p)
        x //= p
    return d

def low_carries(m, p, J):
    """number of carries in m+m among digit positions 0..J-1 (carry-in 0 at position 0)."""
    c = 0
    carry = 0
    mm = m
    for _ in range(J):
        d = mm % p
        s = 2 * d + carry
        carry = 1 if s >= p else 0
        c += carry
        mm //= p
    return c

ok = True

# M1: product form re-verification (independent of erdos727.in_Sk_*)
bad = []
for k in (2, 3, 4):
    for n in range(k, 400):
        m = n + k
        prod = 1
        for i in range(2 * k):
            prod *= (2 * m - i)
        form = binomial(2 * m, m) % prod == 0
        direct = in_Sk_digit(n, k)
        if form != direct:
            bad.append((n, k, form, direct))
print(f"M1 product form == digit criterion (k=2,3,4; n<400): {'PASS' if not bad else 'FAIL '+str(bad[:3])}")
ok &= not bad

# M2/M3/M4: the three residue types
badA = badB = badC = 0
nA = nB = nC = 0
for k in (2, 3, 5):
    for p in primerange(2 * k + 1, 400):
        for J in (1, 2, 3):
            if p ** J > 10 ** 7:
                continue
            for i in range(0, k + 1):
                # TYPE A: m == -i mod p^J, i >= 1
                if i >= 1:
                    for base in range(3):
                        m = (p ** J - i) + base * p ** J * 7 + p ** J * 3
                        if m <= 0 or (m + i) % p ** J or ((m + i) % p ** (J + 1) == 0):
                            continue
                        nA += 1
                        if low_carries(m, p, J) < J:
                            badA += 1
                # TYPE C: m == i mod p^J, 0 <= i <= k-1
                if i <= k - 1:
                    for base in range(3):
                        m = i + base * p ** J * 5 + p ** J * 2
                        if (m - i) % p ** J or ((m - i) % p ** (J + 1) == 0):
                            continue
                        nC += 1
                        if low_carries(m, p, J) != 0:
                            badC += 1
            # TYPE B: 2m == i mod p^J, i odd
            for i in (1, 3, 5):
                if i >= 2 * k or i >= p:
                    continue
                inv2 = pow(2, -1, p ** J)
                r = (i * inv2) % p ** J
                for base in range(3):
                    m = r + (base + 2) * p ** J
                    if (2 * m - i) % p ** J or ((2 * m - i) % p ** (J + 1) == 0):
                        continue
                    nB += 1
                    if low_carries(m, p, J) < J:
                        badB += 1
print(f"M2 TYPE A (m=-i): {nA} cases, violations {badA}: {'PASS' if not badA else 'FAIL'}")
print(f"M3 TYPE B (2m=odd): {nB} cases, violations {badB}: {'PASS' if not badB else 'FAIL'}")
print(f"M4 TYPE C (m=+i): {nC} cases, nonzero-low-carry {badC}: {'PASS' if not badC else 'FAIL'}")
ok &= (badA == 0 and badB == 0 and badC == 0)

# M5: smoothness necessity via type C
viol = []
for k in (2, 3):
    for n in range(2 * k * k + 1, 40000):
        m = n + k
        killed = False
        for i in range(0, k):
            J = 0
            x = m - i
            for p, e in factorint(x).items():
                if p > 2 * k and p ** (2 * e) > 2 * m:
                    killed = True
                    break
            if killed:
                break
        if killed and in_Sk_digit(n, k):
            viol.append((n, k))
print(f"M5 type-C smoothness necessity (k=2,3; n<4e4): violations {viol[:3]}: "
      f"{'PASS' if not viol else 'FAIL'}")
ok &= not viol

print("MIRROR THEOREM:", "ALL PASS" if ok else "FAILURE")
