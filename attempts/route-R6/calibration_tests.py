"""calibration_tests.py — machine checks of the calibration examples for R6.

Claims tested:
  (A) DYADIC FAILURE: the reversed-dyadic-block permutation (blocks [2^k,2^{k+1})
      reversed) is NOT increasing-4-AP-free: (1,6,11,16) and (2,7,12,17) are
      increasing monotone 4-APs.  This CORRECTS the route brief, which called it
      "4-AP-free except for decreasing in-block APs".  Minimal failing prefix found.
  (B) TRIADIC SOUNDNESS: the reversed-triadic-block permutation T (blocks
      [3^k,3^{k+1}) reversed) has NO increasing monotone 4-AP on prefixes up to
      3^9-1 = 19682 values (machine), matching the proof in PROOFS.md (Lemma C).
      Its decreasing 4-APs exist and ALL lie inside single blocks (machine, K<=7).
  (C) Structure formulas for T: pi(v) = 3^{k+1}+3^k-1-v on block k; records
      = {3^{k+1}-1}; dec-patience label ell(v) = 3^{k+1}-v; pile j =
      {3^{m+1}-j : 3^{m+1}-j >= 3^m}; LDS(3^K-1) = 2*3^{K-1}; LIS(3^K-1) = K.
  (D) T satisfies every INCREASING-orientation R6 condition:
      T1-inc: LDS(x) * r4(x) >= x (x = 26, 80, 242; exact r4 by CP-SAT);
      T4: every value-window of length L has max displacement > (L-4)/6 (x<=728);
      T5: record values 3-AP-free (hence 4-AP-free);
      T2-inc: every dec-patience pile value set 3-AP-free (hence 4-AP-free);
      T3-inc: induced permutations on residue classes have no increasing 4-AP;
      increasing 3-APs exist at every scale ((3^k, 7*3^k, 13*3^k)).
  (E) T VIOLATES the decreasing-orientation condition LDS(x) <= r4(x)
      (LDS(26)=18 > r4(26); LDS(80)=54 > r4(80)) — as it must, since it is not
      a counterexample; this shows the decreasing-side tests have teeth.
"""

import sys

import numpy as np

sys.path.insert(0, "/home/user/erdos/attempts/route-R6")
from r6lib import (
    decr_4aps,
    incr_4aps,
    lds_length,
    lis_length,
    piles,
    r4_exact_cpsat,
    records,
    reversed_blocks,
    valueset_has_3ap,
)


def incr_4ap_first_np(perm):
    """First (x,d) increasing 4-AP of a permutation of [1..n], numpy-fast; None if none."""
    n = len(perm)
    pos = np.empty(n + 1, dtype=np.int64)
    pos[np.array(perm)] = np.arange(n)
    for d in range(1, (n - 1) // 3 + 1):
        top = n - 3 * d
        if top < 1:
            break
        p1 = pos[1 : top + 1]
        p2 = pos[1 + d : top + d + 1]
        p3 = pos[1 + 2 * d : top + 2 * d + 1]
        p4 = pos[1 + 3 * d : top + 3 * d + 1]
        hit = (p1 < p2) & (p2 < p3) & (p3 < p4)
        if hit.any():
            return (int(np.argmax(hit)) + 1, d)
    return None


# ---------------------------------------------------------------- (A) dyadic fails
print("== (A) dyadic reversed blocks ==")
minimal = None
for npref in range(4, 32):
    dy_full = reversed_blocks(2, 5)
    pref = dy_full[:npref]
    aps = incr_4aps(pref, limit=1)
    if aps and minimal is None:
        minimal = (npref, aps[0])
print("minimal failing prefix length:", minimal[0], " first increasing 4-AP (x,d):", minimal[1])
dy = reversed_blocks(2, 5)
aps = incr_4aps(dy, limit=5)
assert (1, 5) in aps and (2, 5) in aps, aps
posd = {v: i + 1 for i, v in enumerate(dy)}
print("increasing 4-APs in dyadic[1..31]:", aps)
print("  (1,6,11,16) at positions", [posd[v] for v in (1, 6, 11, 16)])
print("  (2,7,12,17) at positions", [posd[v] for v in (2, 7, 12, 17)])
print("A CONFIRMED: dyadic-reversed is NOT increasing-4-AP-free (route brief corrected).")

# ------------------------------------------------------------- (B) triadic sound
print("\n== (B) triadic reversed blocks ==")
for K in range(2, 10):
    tri = reversed_blocks(3, K)
    assert sorted(tri) == list(range(1, 3**K)), K  # permutation of [1..3^K-1]
    assert incr_4ap_first_np(tri) is None, ("increasing 4-AP found!", K)
print("no increasing 4-AP for prefixes 3^K-1, K=2..9 (up to 19682 values)")
for K in range(3, 8):
    tri = reversed_blocks(3, K)
    dec = decr_4aps(tri)
    assert dec, K  # decreasing 4-APs exist


    def blk(v):
        b = 0
        while 3 ** (b + 1) <= v:
            b += 1
        return b

    for (x, d) in dec:
        bs = {blk(x), blk(x + d), blk(x + 2 * d), blk(x + 3 * d)}
        assert len(bs) == 1, ("cross-block decreasing 4-AP!", K, x, d)
print("all decreasing 4-APs lie inside single blocks (K=3..7); they do exist (in-block).")

# ------------------------------------------------------------- (C) structure
print("\n== (C) structure formulas ==")
K = 8
tri = reversed_blocks(3, K)
pos = {v: i + 1 for i, v in enumerate(tri)}
for v in range(1, 3**K):
    k = 0
    while 3 ** (k + 1) <= v:
        k += 1
    assert pos[v] == 3 ** (k + 1) + 3**k - 1 - v, v
assert records(tri) == [3 ** (k + 1) - 1 for k in range(K)]
ps = piles(tri, "dec")
assert len(ps) == lds_length(tri) == 2 * 3 ** (K - 1)
for j, pile in enumerate(ps, start=1):
    expect = [3 ** (m + 1) - j for m in range(K) if 3 ** (m + 1) - j >= 3**m]
    assert pile == expect, (j, pile[:5], expect[:5])
assert lis_length(tri) == K
print(f"pi(v), records, piles, LDS=2*3^(K-1)={2*3**(K-1)}, LIS=K={K}: all verified for K={K}")

# ------------------------------------------------------- (D)+(E) R6 conditions
print("\n== (D)/(E) R6 conditions on triadic ==")
r4 = {x: r4_exact_cpsat(x) for x in (26, 80, 242)}
print("exact r4:", r4)
for K, x in ((3, 26), (4, 80), (5, 242)):
    tri = reversed_blocks(3, K)
    ld, li = lds_length(tri), lis_length(tri)
    assert ld * r4[x] >= x, ("T1-inc fails?!", x)          # increasing-side: MUST hold
    assert li <= r4[x], ("LIS<=r4 fails?!", x)             # increasing-side: MUST hold
    print(f"x={x}: LDS={ld}, LIS={li}, r4={r4[x]}: LDS*r4={ld*r4[x]}>=x OK; LIS<=r4 OK; "
          f"LDS<=r4 {'HOLDS' if ld <= r4[x] else 'VIOLATED (expected: not a counterexample)'}")
assert lds_length(reversed_blocks(3, 3)) > r4[26]
assert lds_length(reversed_blocks(3, 4)) > r4[80]

# T4 windows on prefix of 728 values
K = 6
tri = reversed_blocks(3, K)
n = 3**K - 1
pos = [0] * (n + 1)
for i, v in enumerate(tri):
    pos[v] = i + 1
disp = [abs(pos[v] - v) for v in range(1, n + 1)]
for u in range(1, n + 1):
    mx = 0
    for L in range(1, n - u + 2):
        mx = max(mx, disp[u + L - 2])
        assert 6 * mx > L - 4, ("T4", u, L, mx)
print(f"T4 (window displacement) verified for all windows in [1..{n}]")

# T5 records
recs = records(reversed_blocks(3, 9))
assert not valueset_has_3ap(recs)
print("T5: records {3^(k+1)-1} are 3-AP-free (K=9 prefix)")

# T2-inc piles 3-AP-free
for pile in piles(reversed_blocks(3, 7), "dec"):
    assert not valueset_has_3ap(pile)
print("T2-inc: all dec-patience pile value sets 3-AP-free (K=7 prefix)")

# T3-inc: induced on residue classes, increasing side only
K = 8
tri = reversed_blocks(3, K)
for (c, m) in ((1, 2), (2, 2), (1, 3), (2, 3), (3, 3), (2, 5)):
    cls = [(v - c) // m + 1 for v in tri if v % m == c % m]
    assert sorted(cls) == list(range(1, len(cls) + 1)), (c, m)
    assert incr_4ap_first_np(cls) is None, ("T3-inc", c, m)
print("T3-inc: induced class permutations have no increasing 4-AP (6 classes, K=8)")

# increasing 3-APs at every scale
tri = reversed_blocks(3, 9)
pos = {v: i for i, v in enumerate(tri)}
for k in range(0, 7):
    x = 3**k
    trip = (x, 7 * x, 13 * x)
    assert pos[trip[0]] < pos[trip[1]] < pos[trip[2]], (k, trip)
print("increasing 3-APs (3^k, 7*3^k, 13*3^k) verified for k=0..6")

print("\nCALIBRATION TESTS COMPLETE.")
