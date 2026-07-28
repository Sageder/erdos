"""N5: hexadecic family n = s^16 - 2 calibration (after PROOF_SKELETON budget analysis).

Window {s^16-1, s^16}; s^16-1 = (s-1)(s+1)(s^2+1)(s^4+1)(s^8+1). Demands (Prop N):
  p^e || s      -> kappa_p((s/p^e)^16) >= 16e
  p^J || s-1 etc -> kappa_p(floor(m/p^J)) >= J
Family: s in [SLO, SHI], theta-smooth with theta = 1/2 (P(s) <= sqrt(s)).
Report: density, per-source E (p > P0), beta hists, D-conditional rates,
and the RELATIVE budget lines (failure counts / smooth base).
"""
import sys, math
from collections import Counter, defaultdict
sys.path.insert(0, '/home/user/erdos/experiments')
from erdos727 import carries_add
from sympy import factorint

SLO, SHI = 300, 1400
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

def sources(s):
    return (('s', s), ('s-1', s - 1), ('s+1', s + 1), ('s2+1', s * s + 1),
            ('s4+1', s ** 4 + 1), ('s8+1', s ** 8 + 1))

def analyze(s):
    m = s ** 16
    fails = []
    for p in (2, 3):
        if not cond_small(m, p):
            fails.append(('small%d' % p, p, 0, 0))
    for source, base in sources(s):
        for p, e in factorint(base).items():
            if p < 5:
                continue
            if source == 's':
                J = 16 * e
                core = (s // p ** e) ** 16
            else:
                J = e
                core = m // p ** e
            ok = kappa(core, p) >= J
            Dav = max(0, int(math.log(max(core, 2)) / math.log(p)) + 1)
            if not ok:
                fails.append((source, p, J, Dav))
    return fails

def smooth(s):
    return s == 1 or max(factorint(s)) ** 2 <= s

tot = hits = s_tot = s_hits = eng_hits = 0
src_fail = Counter()
beta_hist = defaultdict(Counter)
Dfail = defaultdict(Counter)
Dseen = defaultdict(Counter)

for s in range(SLO, SHI + 1):
    sm = smooth(s)
    fails = analyze(s)
    tot += 1
    hits += (not fails)
    if not sm:
        continue
    s_tot += 1
    s_hits += (not fails)
    big = [f for f in fails if not f[0].startswith('small') and f[1] > P0]
    eng_hits += (len(big) == 0)
    for src, p, J, D in big:
        src_fail[src] += 1
        beta_hist[src][round(math.log(p) / math.log(s), 1)] += 1
        Dfail[src][D] += 1
    m = s ** 16
    for src, base in sources(s):
        for p, e in factorint(base).items():
            if p <= P0:
                continue
            core = (s // p ** e) ** 16 if src == 's' else m // p ** e
            Dav = max(0, int(math.log(max(core, 2)) / math.log(p)) + 1)
            Dseen[src][Dav] += 1

print(f"range=[{SLO},{SHI}] theta=1/2 P0={P0}")
print(f"density overall: {hits}/{tot} = {100*hits/tot:.2f}%")
print(f"density among smooth s: {s_hits}/{s_tot} = {100*s_hits/s_tot:.2f}%")
print(f"density smooth+engineered proxy: {eng_hits}/{s_tot} = {100*eng_hits/s_tot:.2f}%")
print(f"E per smooth s by source: { {k: round(v/s_tot, 4) for k, v in src_fail.items()} }")
print(f"TOTAL E = {round(sum(src_fail.values())/s_tot, 4)}")
for src in beta_hist:
    print(f"beta hist {src}: {dict(sorted(beta_hist[src].items()))}")
print("conditional fail rates (source: D: fails/exposures, >=20 exp):")
for src in sorted(Dseen):
    row = {D: f"{Dfail[src][D]}/{c}" for D, c in sorted(Dseen[src].items()) if c >= 20}
    print(f"  {src}: {row}")
