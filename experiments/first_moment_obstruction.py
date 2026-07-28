"""FIRST-MOMENT OBSTRUCTION: measure failure-density vs smooth-density as functions of u.

Reformulation (MIRROR.md): for p || m - i (type C, p > 2k), the 727 condition at p is exactly
    kappa_p(W) >= 1   where W = (m-i)/p,
i.e. the cofactor W must have SOME base-p digit >= ceil(p/2).  Failure = "W has all base-p
digits < p/2" (a carry-free-doubling number base p).

Claim tested (the obstruction):
  F(u) := density{ n : some prime p <= n^{1/u} with p || (n+j), cofactor digit-poor }  ~ c 2^{-u}
  S(u) := density{ n : n+1 and n+2 both n^{1/u}-smooth }                               ~ rho(u)^2
and S(u)/F(u) -> 0, so for EVERY u no unconditional first-moment/union bound over all n can
exhibit a member of S_2: the failures must be counted INSIDE the smooth set.
Measured exhaustively for n <= NMAX at u = 2, 2.5, 3, 4, 5.
"""
import sys, math
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import carries_add
from sympy import factorint

NMAX = 200000

def digit_poor(W, p):
    """True iff every base-p digit of W is < ceil(p/2)  (i.e. kappa_p(W) == 0)."""
    return carries_add(W, W, p) == 0

# Dickman rho by numerical integration (for reference values only)
def rho(u, steps=20000):
    if u <= 1:
        return 1.0
    us = [1.0 + i * (u - 1) / steps for i in range(steps + 1)]
    vals = [1.0] * (steps + 1)
    for idx in range(1, steps + 1):
        t = us[idx]
        # rho(t) = 1 - int_1^t rho(v-1)/v dv  ; integrate incrementally
        h = us[idx] - us[idx - 1]
        # midpoint of rho(v-1)/v
        v = t - h / 2
        vv = v - 1
        if vv <= 1:
            r = 1.0
        else:
            j = int((vv - 1) / (u - 1) * steps)
            r = vals[min(j, steps)]
        vals[idx] = vals[idx - 1] - h * r / v
        if vals[idx] < 0:
            vals[idx] = 0.0
    return vals[-1]

US = [2.0, 2.5, 3.0, 4.0, 5.0]
fail_cnt = {u: 0 for u in US}
smooth_cnt = {u: 0 for u in US}

for n in range(100, NMAX + 1):
    m2 = n + 2                       # k = 2, window {n+1, n+2}, m = n+2
    facts = []
    for j in (1, 2):
        for p, e in factorint(n + j).items():
            facts.append((p, e, j))
    ln = math.log(n)
    maxp = max(f[0] for f in facts)
    for u in US:
        thresh = math.exp(ln / u)
        if maxp <= thresh:
            smooth_cnt[u] += 1
        # failure at some prime p <= n^{1/u} with p || (n+j)  (type C, cofactor digit-poor)
        bad = False
        for p, e, j in facts:
            if p > thresh or p <= 4:
                continue
            if e != 1:
                continue
            W = (n + j) // p
            if digit_poor(W, p):
                bad = True
                break
        if bad:
            fail_cnt[u] += 1

tot = NMAX - 99
print(f"n <= {NMAX};  F(u) = failure density at primes p <= n^(1/u);  S(u) = smooth-pair density")
print(f"{'u':>5} {'F(u)':>10} {'2^-u':>10} {'S(u)':>10} {'rho(u)^2':>12} {'S/F':>10}")
for u in US:
    F = fail_cnt[u] / tot
    S = smooth_cnt[u] / tot
    r = rho(u) ** 2
    ratio = (S / F) if F > 0 else float('inf')
    print(f"{u:>5} {F:>10.5f} {2**-u:>10.5f} {S:>10.5f} {r:>12.6f} {ratio:>10.4f}")
print()
print("Interpretation: S/F < 1 for every u means the unconditional first moment can never")
print("beat the smooth density -- failures must be counted inside the smooth set.")
