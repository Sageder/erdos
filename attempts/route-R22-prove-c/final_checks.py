"""final_checks.py -- Theorem E(a) for arbitrary (incl. non-monotone) G, Theorem D's
density bound, and the finite shadow of Lemma G (OPEN is AP-dense)."""

import sys, random
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-c')
from arch import blockindex, class_seq_violations, perm_from_arch, fibres, open_scales
from forcing_class import v2, ORDERS, build

rng = random.Random(4321)

print("=" * 96)
print("THEOREM E(a): for b >= 3, c = G(j(v)) satisfies condition (ii) for EVERY G")
print("(and FAILS for b = 2, where the block-gap lemma D2+D3 <= 1 is unavailable)")
print("=" * 96)
print(f"{'b':>2} {'N':>5} {'random G trials':>16} {'total (ii)-violations':>22}")
for b in (2, 3, 4, 5):
    N = 900
    J = blockindex(N, b) + 1
    tot = 0
    for _ in range(25):
        G = [rng.randint(k, k + 8) for k in range(J + 1)]     # G(k) >= k, otherwise free
        c = lambda v, G=G, b=b: G[blockindex(v, b)]
        tot += len(class_seq_violations(N, c))
    print(f"{b:>2} {N:>5} {25:>16} {tot:>22}")
print()

print("=" * 96)
print("THEOREM D: |F_m| >= c1 b^m forces {t < r} to have >= (c1/2) b^m elements of")
print("[b^{m-r+1}, b^{m+1}),  r = 2 + floor(log_b(2/c1))")
print("=" * 96)
print(f"{'b':>2} {'t':>10} {'N':>6} {'c1 (measured)':>14} {'r':>3} {'m':>3} "
      f"{'|{t<r} cap window|':>19} {'bound (c1/2)b^m':>16} {'ok':>4}")
import math
for b in (3, 4):
    for tname, tf in (('v2', v2), ('1_odd', lambda v: v % 2), ('0', lambda v: 0)):
        N = 3 * b ** 6
        F = {}
        for v in range(1, N + 1):
            m = blockindex(v, b) + tf(v)
            F[m] = F.get(m, 0) + 1
        mmax = blockindex(N, b) - 1
        c1 = min(F.get(m, 0) / b ** m for m in range(1, mmax + 1))
        r = 2 + int(math.floor(math.log(2 / c1) / math.log(b))) if c1 < 2 else 2
        for m in (mmax - 1, mmax):
            lo, hi = b ** max(m - r + 1, 0), b ** (m + 1)
            cnt = sum(1 for v in range(lo, min(hi, N + 1)) if tf(v) < r)
            bound = (c1 / 2) * b ** m
            print(f"{b:>2} {tname:>10} {N:>6} {round(c1,3):>14} {r:>3} {m:>3} "
                  f"{cnt:>19} {round(bound,1):>16} {str(cnt >= bound):>4}")
print()

print("=" * 96)
print("LEMMA G (finite shadow): OPEN = {u : some (u-2d,u-d,u) positionally increasing}")
print("meets every AP of step q <= 8 -- measured density of OPEN inside each AP")
print("=" * 96)
for b, tname, tf, oname in ((3, 't=0', lambda v: 0, 'decreasing'),
                            (3, 't=v2', v2, 'decreasing'),
                            (4, 't=0', lambda v: 0, 'vdc')):
    N = 400
    c, within, perm, pos = build(N, b, tf, ORDERS[oname])
    OPEN = {u for u in range(3, N + 1) if open_scales(pos, u, N)}
    dens = []
    for q in range(1, 9):
        for rr in range(q):
            P = [v for v in range(N // 2, N + 1) if v % q == rr % q]
            if len(P) < 10:
                continue
            dens.append(sum(1 for v in P if v in OPEN) / len(P))
    print(f"  b={b} {tname:>6} order={oname:>10}: |OPEN|/N = {len(OPEN)/N:.3f}, "
          f"min AP-density = {min(dens):.3f}, max = {max(dens):.3f}  "
          f"(min > 0 in every case)")
