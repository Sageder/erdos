"""finite_tests.py — machine-test the R6 necessary conditions on ALL monotone-
4-AP-free permutations of [1..N] (exhaustive), N = 3..MAXN.

Claims tested (finite shadows of PROOFS.md T1-T6; each MUST hold for every
avoider, else the corresponding lemma/proof is wrong):

  T1  LIS*LDS >= N;  LIS <= r4(N);  LDS <= r4(N).
      (LIS<=r4: increasing orientation; LDS<=r4: decreasing orientation.)
  T2  dec-patience piles: partition values, #piles == LDS, each pile increasing,
      each pile's VALUE SET 4-AP-free; interlock: every element of pile j>=2 has
      an earlier, larger element in pile j-1.  Dual (inc-patience / Mirsky):
      #piles == LIS, piles decreasing, value sets 4-AP-free.
  T3  for every modulus m>=2 and residue c, the subsequence of values in the AP
      class {c, c+m, c+2m, ...}, renormalized by v -> (v-c)/m + 1, is again a
      monotone-4-AP-free permutation of an initial segment.
  T4  for every value-window I=[u, u+L-1] within [1..N]:
      6 * max_{v in I} |pi(v)-v| > L-4   (pi = 1-indexed position).
  T5  the left-to-right-maxima value set is 4-AP-free.
  T6  forced extension: for every increasing monotone 3-AP (x, x+d, x+2d):
      pi(x+3d) < pi(x+2d) if x+3d <= N, and pi(x-d) > pi(x) if x-d >= 1;
      mirror for decreasing 3-APs.

Also reports extremal statistics (tightness data for REPORT.md).
"""

import sys
from itertools import permutations

sys.path.insert(0, "/home/user/erdos/attempts/route-R6")
from r6lib import (
    has_monotone_kap_pos,
    lis_length,
    lds_length,
    piles,
    records,
    r4_exact_small,
    valueset_has_4ap,
)

MAXN = int(sys.argv[1]) if len(sys.argv) > 1 else 9
MINN = int(sys.argv[2]) if len(sys.argv) > 2 else 3
EXPECT4 = {3: 6, 4: 22, 5: 102, 6: 564, 7: 3336, 8: 22266, 9: 168864}

R4 = {n: r4_exact_small(n) for n in range(1, MAXN + 1)}
print("exact r4 table:", R4, flush=True)


def check_perm(p, n, stats):
    pos = [0] * (n + 1)  # 1-indexed positions
    for i, v in enumerate(p):
        pos[v] = i + 1

    # ---- T1
    L_inc, L_dec = lis_length(p), lds_length(p)
    assert L_inc * L_dec >= n, ("T1 product", p)
    assert L_inc <= R4[n], ("T1 LIS<=r4", p)
    assert L_dec <= R4[n], ("T1 LDS<=r4", p)
    stats["min_prod"] = min(stats.get("min_prod", 10**9), L_inc * L_dec)
    stats["max_LIS"] = max(stats.get("max_LIS", 0), L_inc)
    stats["max_LDS"] = max(stats.get("max_LDS", 0), L_dec)

    # ---- T2
    ps = piles(p, "dec")
    assert len(ps) == L_dec, ("T2 count", p)
    seen = sorted(v for pile in ps for v in pile)
    assert seen == list(range(1, n + 1)), ("T2 partition", p)
    for j, pile in enumerate(ps):
        assert all(pile[i] < pile[i + 1] for i in range(len(pile) - 1)), ("T2 inc", p)
        assert not valueset_has_4ap(pile), ("T2 pile 4AP", p, pile)
        if j >= 1:
            prev = ps[j - 1]
            for v in pile:
                assert any(pos[w] < pos[v] and w > v for w in prev), ("T2 interlock", p, j + 1, v)
    psm = piles(p, "inc")
    assert len(psm) == L_inc, ("T2 dual count", p)
    for pile in psm:
        assert all(pile[i] > pile[i + 1] for i in range(len(pile) - 1)), ("T2 dual dec", p)
        assert not valueset_has_4ap(pile), ("T2 dual pile 4AP", p, pile)

    # ---- T3
    for m in range(2, n + 1):
        for c in range(1, m + 1):
            cls = [(v - c) // m + 1 for v in p if v % m == c % m]
            if len(cls) >= 4:
                assert not has_monotone_kap_pos(cls, 4), ("T3", p, m, c)

    # ---- T4
    disp = [abs(pos[v] - v) for v in range(1, n + 1)]  # disp[v-1]
    for u in range(1, n + 1):
        mx = 0
        for L in range(1, n - u + 2):
            mx = max(mx, disp[u + L - 2])
            assert 6 * mx > L - 4, ("T4", p, u, L, mx)
    # tightness: minimal over windows-max-disp for each L across avoiders
    for L in range(1, n + 1):
        best = min(max(disp[u - 1 : u + L - 1]) for u in range(1, n - L + 2))
        d = stats.setdefault("T4tight", {})
        d[L] = min(d.get(L, 10**9), best)

    # ---- T5
    rec = records(p)
    assert not valueset_has_4ap(rec), ("T5", p, rec)
    stats["max_rec"] = max(stats.get("max_rec", 0), len(rec))

    # ---- T6
    for d in range(1, (n - 1) // 2 + 1):
        for x in range(1, n - 2 * d + 1):
            p0, p1, p2 = pos[x], pos[x + d], pos[x + 2 * d]
            if p0 < p1 < p2:  # increasing 3-AP
                if x + 3 * d <= n:
                    assert pos[x + 3 * d] < p2, ("T6 inc up", p, x, d)
                if x - d >= 1:
                    assert pos[x - d] > p0, ("T6 inc down", p, x, d)
            if p0 > p1 > p2:  # decreasing 3-AP (values read x+2d, x+d, x along positions)
                if x + 3 * d <= n:
                    assert pos[x + 3 * d] > p2, ("T6 dec up", p, x, d)
                if x - d >= 1:
                    assert pos[x - d] < p0, ("T6 dec down", p, x, d)


for n in range(MINN, MAXN + 1):
    stats = {}
    cnt = 0
    for p in permutations(range(1, n + 1)):
        if has_monotone_kap_pos(p, 4):
            continue
        cnt += 1
        check_perm(p, n, stats)
    if n in EXPECT4:
        assert cnt == EXPECT4[n], (n, cnt, EXPECT4[n])
    print(
        f"N={n}: avoiders={cnt}  ALL T1-T6 PASS.  r4={R4[n]}  "
        f"min(LIS*LDS)={stats['min_prod']} (N={n})  max LIS={stats['max_LIS']} "
        f"max LDS={stats['max_LDS']}  max #records={stats['max_rec']}",
        flush=True,
    )
    tight = stats["T4tight"]
    print(f"      T4 tightness: min over avoiders of (min over windows len L of max disp): "
          f"{[(L, tight[L]) for L in sorted(tight)]}", flush=True)

print("FINITE TESTS COMPLETE: all conditions hold on every 4-AP-free permutation, "
      f"N={MINN}..{MAXN}; counts match calibration where known.", flush=True)
