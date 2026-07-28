"""CRUX EXPERIMENT: are the per-prime carry conditions equidistributed CONDITIONAL on
window smoothness?  (This is exactly the lemma any 'injection into Hildebrand' proof needs.)

Background (established in this project):
  n in S_k  <=>  for every prime ell | (n+1)...(n+k):  kappa_ell(n) >= 2 sum_j nu_ell(n+j),
  where kappa_ell(n) = #carries in n+n base ell.  For ell || n+j the demand is 2, digit 0
  (= ell - j) always carries, so the condition is "at least one more carry higher up",
  which for the top prime factor (2 digits) is exactly C_ell: d_1(n) >= (ell-1)/2.

Claims tested (k=2, n <= NMAX, window = {n+1, n+2}):
 (E1) UNCONDITIONAL first moment fails: the fraction of ALL n that have >= 1 failure at a
      prime ell <= sqrt(2n) is a positive constant (not o(1)) -- so no first-moment bound
      over all n can beat the rho(2)^2-thin smooth set.  Report that fraction.
 (E2) Conditional on the window being sqrt(2n)-smooth, measure per-prime pass rates
      P(cond holds at ell) bucketed by beta = log ell / log n, and compare with the
      independent-digit model prediction (1 - 2^-(D-1) with D = floor(log n/log ell) + 1).
 (E3) Independence across primes: compare P(all conditions hold | smooth window) with the
      product of the measured per-prime rates over the same population.
 (E4) The same, restricted to n in a fixed AP (to check no AP-obstruction), and restricted
      to stronger smoothness n^(1/3) (the regime a Hildebrand-type injection would use).
Deterministic; exact integer arithmetic.
"""
import sys, math
from collections import defaultdict
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import carries_add
from sympy import factorint

NMAX = 300000       # exhaustive range (exact factorization per n)
K = 2

def kappa(n, p):
    return carries_add(n, n, p)

def window_facts(n):
    """[(ell, e, j)] for all primes ell | (n+1)(n+2)."""
    out = []
    for j in (1, 2):
        for ell, e in factorint(n + j).items():
            out.append((ell, e, j))
    return out

def fails_at(n, facts):
    """list of (ell, e, beta) where the per-prime condition FAILS."""
    bad = []
    for ell, e, j in facts:
        # total demand at ell: 2 * sum over window of nu_ell
        dem = 2 * sum(f[1] for f in facts if f[0] == ell)
        if kappa(n, ell) < dem:
            bad.append((ell, e, math.log(ell) / math.log(max(n, 3))))
    return bad

def smooth_window(n, facts, thresh):
    return all(f[0] <= thresh for f in facts)

# ---------------- pass 1: unconditional + conditional statistics
tot = 0
uncond_fail = 0
sm_tot = sm_ok = 0
sm3_tot = sm3_ok = 0
ap_tot = ap_ok = 0
per_beta_pass = defaultdict(lambda: [0, 0])     # beta bucket -> [pass, total] (smooth pop)
prod_indep_num = 0.0
joint_pop = []

for n in range(10, NMAX + 1):
    facts = window_facts(n)
    bad = fails_at(n, facts)
    tot += 1
    if bad:
        uncond_fail += 1
    thr2 = math.isqrt(2 * n)
    thr3 = int(round((2 * n) ** (1.0 / 3)))
    if smooth_window(n, facts, thr2):
        sm_tot += 1
        ok = not bad
        sm_ok += ok
        joint_pop.append((n, facts, ok))
        if n % 24 == 7:
            ap_tot += 1
            ap_ok += ok
        badset = {b[0] for b in bad}
        for ell, e, j in facts:
            if ell < 50:
                continue
            beta = math.log(ell) / math.log(n)
            per_beta_pass[round(beta, 1)][1] += 1
            if ell not in badset:
                per_beta_pass[round(beta, 1)][0] += 1
    if smooth_window(n, facts, thr3):
        sm3_tot += 1
        sm3_ok += (not bad)

print(f"range n <= {NMAX}")
print(f"E1 UNCONDITIONAL failure fraction (any prime): {uncond_fail}/{tot} = "
      f"{100*uncond_fail/tot:.2f}%  -> first moment over all n is USELESS (constant, not o(1))")
print(f"    smooth-window density: {sm_tot}/{tot} = {100*sm_tot/tot:.3f}%  "
      f"(rho(2)^2 ~ 9.4% for independent)")
print(f"    membership | smooth window: {sm_ok}/{sm_tot} = {100*sm_ok/sm_tot:.2f}%")
print(f"    membership | n^(1/3)-smooth window: {sm3_ok}/{sm3_tot} = "
      f"{100*sm3_ok/max(sm3_tot,1):.2f}%")
print(f"    membership | smooth window AND n=7 mod 24: {ap_ok}/{ap_tot} = "
      f"{100*ap_ok/max(ap_tot,1):.2f}%  (AP-obstruction check)")

print("E2 per-prime pass rate | smooth window, by beta = log(ell)/log(n)  "
      "[observed vs independent-digit model 1-2^-(D-1), D=floor(1/beta)+1]:")
for b in sorted(per_beta_pass):
    ok_, t_ = per_beta_pass[b]
    if t_ < 40 or b <= 0:
        continue
    D = int(1.0 / b) + 1
    model = 1 - 2.0 ** (-(D - 1))
    print(f"    beta~{b}: observed {ok_}/{t_} = {ok_/t_:.3f}   model(D={D}) = {model:.3f}")

# E3 independence check on the smooth population
prod = 1.0
# estimate product of per-prime rates using measured rates, averaged over the population
import statistics
rate = {b: (v[0] / v[1]) for b, v in per_beta_pass.items() if v[1] >= 40}
pred = []
for n, facts, ok in joint_pop:
    q = 1.0
    for ell, e, j in facts:
        if ell < 50:
            continue
        b = round(math.log(ell) / math.log(n), 1)
        q *= rate.get(b, 0.9)
    pred.append(q)
print(f"E3 independence: observed P(all pass | smooth) = {sm_ok/sm_tot:.4f}; "
      f"product-model mean = {statistics.mean(pred):.4f} "
      f"(ratio {(sm_ok/sm_tot)/statistics.mean(pred):.3f}; ~1 means independent)")
