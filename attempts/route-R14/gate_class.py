"""
R14 gate 3.  The explicit small-prime class (step L3 for k=2, P0=4).

Claim.  Q0 = 648 = 2^3 * 3^4,  c0 = 157  (c0 == 5 mod 8, c0 == 76 mod 81).
Then for EVERY n == c0 (mod Q0) with n >= 3:
   nu_2(n+1)=1, nu_2(n+2)=0, nu_3(n+1)=0, nu_3(n+2)=1,
   kappa_2(n) >= 2 = 2(nu_2(n+1)+nu_2(n+2)),
   kappa_3(n) >= 2 = 2(nu_3(n+1)+nu_3(n+2)).
So the p=2 and p=3 conditions of the k=2 criterion hold IDENTICALLY on the class, and
for n in this class,  n in S_2  <=>  the conditions at every prime l >= 5 hold.

Reason (a proof, the loop below is only a check):  n == 5 (mod 8) gives n+1 == 6 (mod 8),
so nu_2(n+1)=1, and n+2 odd, so nu_2(n+2)=0; the base-2 digits of n at positions 0 and 2
are 1, and in base 2 a digit 1 always produces a carry on doubling (2*1+c >= 2), so
kappa_2(n) = s_2(n) >= 2.   n == 76 (mod 81): 76 = 1 + 1*3 + 2*9 + 2*27, so n == 1 (mod 3)
(hence 3 | n+2, 3 does not divide n+1) and n+2 == 78 (mod 81) has nu_3 = 1; the base-3
digits of n at positions 2 and 3 are 2, and 2*2 = 4 >= 3 always carries, so kappa_3(n) >= 2.
"""
import numpy as np
from sympy import factorial
from pairlib import pair_data

Q0, c0 = 648, 157
assert c0 % 8 == 5 and c0 % 81 == 76


def vp(m, p):
    e = 0
    while m % p == 0:
        m //= p; e += 1
    return e


def carries(n, l):
    c = 0; carry = 0
    while n > 0:
        if 2 * (n % l) + carry >= l:
            carry = 1; c += 1
        else:
            carry = 0
        n //= l
    return c


bad = 0; N = 0; n = c0
while n < 5 * 10 ** 7:
    if n >= 3:
        N += 1
        v21, v22 = vp(n + 1, 2), vp(n + 2, 2)
        v31, v32 = vp(n + 1, 3), vp(n + 2, 3)
        if not (v21 == 1 and v22 == 0 and v31 == 0 and v32 == 1
                and carries(n, 2) >= 2 * (v21 + v22)
                and carries(n, 3) >= 2 * (v31 + v32)):
            bad += 1
            if bad < 5:
                print("   VIOLATION at n =", n, v21, v22, v31, v32, carries(n, 2), carries(n, 3))
    n += Q0
print("GATE 3: Q0=%d c0=%d ; %d values n == c0 (mod Q0) below 5*10^7 checked, violations %d"
      % (Q0, c0, N, bad))
assert bad == 0

# End-to-end: inside the class, "no large-prime failure" == membership in S_2.
X, y = 3 * 10 ** 6, 300
d = pair_data(X, y, P0=4)
nn = d['n']
sel = nn[nn % Q0 == c0]
good = sel[d['nfail_large'][sel] == 0]
print("smooth pairs (X=%d, y=%d): %d ; in the class: %d ; of those with no large-prime "
      "failure: %d" % (X, y, len(nn), len(sel), len(good)))
small = [int(v) for v in good if v <= 30000][:30]
for v in small:
    assert factorial(2 * v) % (factorial(v + 2) ** 2) == 0, v
print("GATE 3b PASS: %d such n (<=30000) verified in S_2 by exact factorial division: %s"
      % (len(small), small[:10]))
# every "good" n must in fact be in S_2 by the criterion:
assert (d['ok_small'][good]).all(), "class failed to force the small primes"
print("GATE 3c PASS: ok_small holds for all %d of them (the class does force p=2,3)." % len(good))

# The 8 certified members are all > 30000, so verify them by Legendre valuations instead
# of by forming the factorials.
from pairlib import primes_upto as _pu
def _leg(m, p):
    s = 0; q = p
    while q <= m:
        s += m // q; q *= p
    return s
if len(good):
    Pall = [int(p) for p in _pu(2 * int(good.max()))]
    for v in good:
        v = int(v)
        assert all(_leg(2*v, p) >= 2*_leg(v+2, p) for p in Pall if p <= 2*v), v
    print("GATE 3d PASS: all %d certified n verified: ((n+2)!)^2 | (2n)! by Legendre at every "
          "prime <= 2n.  n = %s" % (len(good), [int(v) for v in good]))
