"""N2: calibrate Program K2's first-moment budget on the quartic family n = z^4 - 2.

For z in [ZLO, ZHI]: test membership via Prop N (verified in verify_propN.py); attribute
every failure to its source (p<=3 engineered range; z / z-1 / z+1 / z^2+1 with prime p>=5).
Outputs:
 - overall density; density among sqrt-smooth z (P(z) <= sqrt(z)); density among
   sqrt-smooth z with no p<=P0 failure (P0 = 13; proxy for small-prime engineering);
 - E[#failures] per source among sqrt-smooth z (the budget table);
 - beta-histograms of failures per source (beta = log p / log z);
 - check: no failures from z^2+1 factors with gamma = log p / log(z^2) ... reported as
   a = (z^2+1)/p with a^2 < p (the auto-pass regime claim);
 - empirical P(fail | source, available digits D) vs Bin(D, 1/2) tail.
"""
import sys, math
from collections import Counter, defaultdict
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import carries_add
from sympy import factorint, primerange

ZLO, ZHI = 1000, 9000
P0 = 13

def kappa(m, p):
    return carries_add(m, m, p)

def cond_small(m, p, k=2):
    v = 0
    for i in range(0, 2 * k):
        x = 2 * m - i
        while x % p == 0:
            v += 1
            x //= p
    return kappa(m, p) >= v

def analyze(z):
    """Return list of failure records (source, p, J, D_avail) for n = z^4 - 2."""
    m = z ** 4
    fails = []
    for p in (2, 3):
        if not cond_small(m, p):
            fails.append(('small%d' % p, p, 0, 0))
    for source, base in (('z', z), ('z-1', z - 1), ('z+1', z + 1), ('z2+1', z * z + 1)):
        for p, e in factorint(base).items():
            if p < 5:
                continue
            if source == 'z':
                J = 4 * e
                core = (z // p ** e) ** 4
                ok = kappa(core, p) >= J
                Dav = max(0, int(math.log(core) / math.log(p)) + 1)
            else:
                J = e
                core = m // p ** J
                ok = kappa(core, p) >= J
                Dav = max(0, int(math.log(max(core, 2)) / math.log(p)) + 1)
            if not ok:
                fails.append((source, p, J, Dav))
    return fails

def is_sqrt_smooth(z):
    return max(factorint(z)) <= math.isqrt(z) + 1 if z > 1 else True

tot = hits = 0
smooth_tot = smooth_hits = 0
eng_tot = eng_hits = 0
src_fail_counts = Counter()          # among sqrt-smooth z: total failures per source
beta_hist = defaultdict(Counter)     # source -> beta bucket -> count (sqrt-smooth z)
Dfail = defaultdict(Counter)         # source -> D -> failures
Dseen = defaultdict(Counter)         # source -> D -> exposures (prime present)
auto_viol = []

for z in range(ZLO, ZHI + 1):
    fails = analyze(z)
    ok = not fails
    tot += 1
    hits += ok
    sm = is_sqrt_smooth(z)
    if sm:
        smooth_tot += 1
        smooth_hits += ok
        nosmall = all(not s.startswith('small') and p > P0 for s, p, _, _ in fails)
        # engineered proxy: ignore failures at p <= P0 entirely
        big_fails = [f for f in fails if not f[0].startswith('small') and f[1] > P0]
        eng_tot += 1
        eng_hits += (len(big_fails) == 0)
        for s, p, J, D in big_fails:
            src_fail_counts[s] += 1
            beta_hist[s][round(math.log(p) / math.log(z), 1)] += 1
            Dfail[s][D] += 1
    # auto-pass check for z^2+1 large factors
    for p, e in factorint(z * z + 1).items():
        if p >= 5 and e == 1:
            a = (z * z + 1) // p
            if a * a < p:  # claimed auto-pass regime
                m = z ** 4
                if kappa(m // p, p) < 1:
                    auto_viol.append((z, p))

# exposures for conditional rates (sqrt-smooth z only, p > P0)
for z in range(ZLO, ZHI + 1):
    if not is_sqrt_smooth(z):
        continue
    m = z ** 4
    for source, base in (('z', z), ('z-1', z - 1), ('z+1', z + 1), ('z2+1', z * z + 1)):
        for p, e in factorint(base).items():
            if p <= P0:
                continue
            if source == 'z':
                core = (z // p ** e) ** 4
            else:
                core = m // p ** e
            Dav = max(0, int(math.log(max(core, 2)) / math.log(p)) + 1)
            Dseen[source][Dav] += 1

print(f"density overall: {hits}/{tot} = {100*hits/tot:.2f}%")
print(f"density among sqrt-smooth z: {smooth_hits}/{smooth_tot} = {100*smooth_hits/smooth_tot:.2f}%")
print(f"density sqrt-smooth + engineered proxy (ignore p<={P0}): {eng_hits}/{eng_tot} = "
      f"{100*eng_hits/eng_tot:.2f}%")
print(f"E[#failures per sqrt-smooth z], p>{P0}, by source: "
      f"{ {s: round(c/smooth_tot, 4) for s, c in src_fail_counts.items()} }")
print(f"TOTAL E = {round(sum(src_fail_counts.values())/smooth_tot, 4)}")
for s in beta_hist:
    print(f"beta hist {s}: {dict(sorted(beta_hist[s].items()))}")
print(f"auto-pass violations (z2+1, a^2<p): {auto_viol[:5]} "
      f"{'PASS' if not auto_viol else 'FAIL'}")
print("conditional fail rates by available digits D (source: D: fails/exposures):")
for s in sorted(Dseen):
    row = {D: f"{Dfail[s][D]}/{c}" for D, c in sorted(Dseen[s].items()) if c >= 30}
    print(f"  {s}: {row}")
