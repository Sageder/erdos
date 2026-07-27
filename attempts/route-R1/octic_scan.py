"""N4: octic family n = w^8 - 2 calibration (Program K2 revision after quartic verdict).

Window {w^8-1, w^8}; w^8-1 = (w-1)(w+1)(w^2+1)(w^4+1). Sources and demands (Prop N):
  p^e || w    -> kappa_p((w/p^e)^8) >= 8e
  p^J || w-1  -> kappa_p(floor(m/p^J)) >= J   (danger: binomial digits of (ap+1)^8)
  p^J || w+1  -> same demand (alternating pattern, expected safe)
  p^J || w^2+1, w^4+1 -> same demand
Measures (for w in [WLO, WHI], among w^{theta}-smooth w, ignoring p <= P0):
  density; E per source; beta histograms; conditional fail rates by available digits.
"""
import sys, math
from collections import Counter, defaultdict
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import carries_add
from sympy import factorint

WLO, WHI = 300, 4200
P0 = 13
THETA = 0.42

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

def sources(w):
    return (('w', w), ('w-1', w - 1), ('w+1', w + 1),
            ('w2+1', w * w + 1), ('w4+1', w ** 4 + 1))

def analyze(w):
    m = w ** 8
    fails = []
    for p in (2, 3):
        if not cond_small(m, p):
            fails.append(('small%d' % p, p, 0, 0))
    for source, base in sources(w):
        for p, e in factorint(base).items():
            if p < 5:
                continue
            if source == 'w':
                J = 8 * e
                core = (w // p ** e) ** 8
            else:
                J = e
                core = m // p ** e
            ok = kappa(core, p) >= J
            Dav = max(0, int(math.log(max(core, 2)) / math.log(p)) + 1)
            if not ok:
                fails.append((source, p, J, Dav))
    return fails

def theta_smooth(w):
    return w == 1 or max(factorint(w)) <= w ** THETA

tot = hits = 0
s_tot = s_hits = eng_hits = 0
src_fail = Counter()
beta_hist = defaultdict(Counter)
Dfail = defaultdict(Counter)
Dseen = defaultdict(Counter)

for w in range(WLO, WHI + 1):
    sm = theta_smooth(w)
    fails = analyze(w)
    tot += 1
    hits += (not fails)
    if not sm:
        continue
    s_tot += 1
    s_hits += (not fails)
    big = [f for f in fails if not f[0].startswith('small') and f[1] > P0]
    eng_hits += (len(big) == 0)
    for s, p, J, D in big:
        src_fail[s] += 1
        beta_hist[s][round(math.log(p) / math.log(w), 1)] += 1
        Dfail[s][D] += 1
    m = w ** 8
    for source, base in sources(w):
        for p, e in factorint(base).items():
            if p <= P0:
                continue
            core = (w // p ** e) ** 8 if source == 'w' else m // p ** e
            Dav = max(0, int(math.log(max(core, 2)) / math.log(p)) + 1)
            Dseen[source][Dav] += 1

print(f"THETA={THETA} P0={P0} range=[{WLO},{WHI}]")
print(f"density overall: {hits}/{tot} = {100*hits/tot:.2f}%")
print(f"density among smooth w: {s_hits}/{s_tot} = {100*s_hits/s_tot:.2f}%")
print(f"density smooth + engineered proxy (ignore p<={P0}): {eng_hits}/{s_tot} = "
      f"{100*eng_hits/s_tot:.2f}%")
print(f"E[#failures per smooth w], p>{P0}: "
      f"{ {s: round(c/s_tot, 4) for s, c in src_fail.items()} }")
print(f"TOTAL E = {round(sum(src_fail.values())/s_tot, 4)}")
for s in beta_hist:
    print(f"beta hist {s}: {dict(sorted(beta_hist[s].items()))}")
print("conditional fail rates by available digits (source: D: fails/exposures, >=25 exp):")
for s in sorted(Dseen):
    row = {D: f"{Dfail[s][D]}/{c}" for D, c in sorted(Dseen[s].items()) if c >= 25}
    print(f"  {s}: {row}")
