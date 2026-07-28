"""FIRST-MOMENT OBSTRUCTION (exact version): failure density vs smooth density.

CORRECTION (2026-07-28): an earlier version of this script used the proxy "kappa_p(W) = 0"
with W = (n+j)/p for the failure event.  The EXACT failure event at a prime p || (n+j) is
    kappa_p(n) < 2 nu_p(n+j),
equivalently (n = p(W-1) + (p-j), so digit 0 gives one carry and passes carry 1 upward):
    doubling (W-1) in base p WITH CARRY-IN 1 produces no carry.
This script uses the exact condition kappa_p(n) < 2 nu_p(n+j) directly.

Definitions (k = 2, window {n+1, n+2}):
  F(u) := density{ n : some prime p with 4 < p <= n^{1/u} and kappa_p(n) < 2 nu_p(n+j) }
  S(u) := density{ n : n+1 and n+2 both n^{1/u}-smooth }

Claim tested: F(u) ~ c 2^{-u}/u while S(u) <= rho(u) ~ u^{-u}, so S(u)/F(u) -> 0 and no
unconditional first-moment/union bound over all n can produce a member of S_2 at ANY
threshold u.  (Proof of the asymptotic statement is in DRAFT.tex, Prop. 5.1; this script
supplies the small-u numbers, where the asymptotics are not yet decisive.)
"""
import sys, math
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import carries_add
from sympy import factorint

NMAX = 200000

def rho(u, steps=20000):
    """Dickman rho by the standard integral recursion (reference values only)."""
    if u <= 1:
        return 1.0
    vals = [1.0] * (steps + 1)
    for idx in range(1, steps + 1):
        t = 1.0 + idx * (u - 1) / steps
        h = (u - 1) / steps
        v = t - h / 2
        vv = v - 1
        if vv <= 1:
            r = 1.0
        else:
            j = int((vv - 1) / (u - 1) * steps)
            r = vals[min(j, steps)]
        vals[idx] = max(0.0, vals[idx - 1] - h * r / v)
    return vals[-1]

US = [2.0, 2.5, 3.0, 4.0, 5.0]
fail_cnt = {u: 0 for u in US}
smooth_cnt = {u: 0 for u in US}

for n in range(100, NMAX + 1):
    facts = []
    for j in (1, 2):
        for p, e in factorint(n + j).items():
            facts.append((p, e, j))
    ln = math.log(n)
    maxp = max(f[0] for f in facts)
    # exact per-prime failure: kappa_p(n) < 2 * (total window valuation at p)
    fails = []
    for p, e, j in facts:
        if p <= 4:
            continue
        dem = 2 * sum(f[1] for f in facts if f[0] == p)
        if carries_add(n, n, p) < dem:
            fails.append(p)
    for u in US:
        thresh = math.exp(ln / u)
        if maxp <= thresh:
            smooth_cnt[u] += 1
        if any(p <= thresh for p in fails):
            fail_cnt[u] += 1

tot = NMAX - 99
print(f"EXACT failure condition kappa_p(n) < 2 nu_p(window); n <= {NMAX}")
print(f"{'u':>5} {'F(u)':>10} {'2^-u/u*c':>10} {'S(u)':>10} {'rho(u)^2':>12} {'rho(u)':>10} {'S/F':>9}")
for u in US:
    F = fail_cnt[u] / tot
    S = smooth_cnt[u] / tot
    r1 = rho(u)
    ratio = (S / F) if F > 0 else float('inf')
    print(f"{u:>5} {F:>10.5f} {2**-u/u*2.77:>10.5f} {S:>10.5f} {r1*r1:>12.6f} {r1:>10.6f} {ratio:>9.4f}")
print()
print("S/F decreasing to 0 => the unconditional first moment can never beat the smooth set.")
