"""Route R5 calibration gate for the segmented sieve.

Claims tested:
 C1. block_members reproduces PROBLEM.md tables: S_2 up to 2e5 (first 20 elements
     and count 1981), S_3 up to 6e4 (first 8 elements, count 41 to 6e4),
     S_4 cap [1,6e4] = {8174, 51984}.
 C2. block_members agrees with experiments.erdos727.in_Sk_fast on random n
     samples in [10^6, 10^6+10^4] for k=2,3.
 C3. Kill-rate profile: for k=2 survivors in a 10^6-range, distribution of the
     killing prime; writes kill_order_k2.json (primes sorted by measured kills,
     descending) for use as scan order (speed only, not correctness).
Falsification protocol: C1/C2 are exact comparisons; any mismatch aborts.
"""

import json
import math
import sys
import time

sys.path.insert(0, "/home/user/erdos/attempts/route-R5")
sys.path.insert(0, "/home/user/erdos/experiments")

import numpy as np

from erdos727 import in_Sk_digit, in_Sk_fast
from sievelib import block_members, primes_upto, rough_rem, spvec, isqrt_vec

KS = [2, 3, 4, 5, 6]
SMALL_N_CUTOFF = 200  # handle n <= cutoff by direct digit check (need n > 2k^2 = 72)


def members_upto(N, ks):
    """Reference-driver: exact S_k cap [1, N] using direct check below cutoff
    and block_members above."""
    out = {k: [] for k in ks}
    for n in range(1, SMALL_N_CUTOFF + 1):
        for k in ks:
            if in_Sk_digit(n, k):
                out[k].append(n)
    ps = primes_upto(math.isqrt(N + max(ks)) + 1)
    pd = primes_upto(math.isqrt(2 * N) + 1)
    res = block_members(SMALL_N_CUTOFF + 1, N + 1, ks, ps, pd)
    for k in ks:
        out[k] = np.array(out[k] + res[k].tolist(), dtype=np.int64)
    return out


def main():
    t0 = time.time()
    # ---- C1: PROBLEM.md tables ----
    res = members_upto(200000, KS)
    S2 = res[2]
    exp20 = [208, 458, 987, 1220, 1455, 1597, 1889, 2012, 2144, 2330, 2477,
             2663, 2991, 3353, 3415, 3430, 3439, 3475, 3476, 3551]
    assert S2[:20].tolist() == exp20, ("C1 FAIL S2 first20", S2[:20].tolist())
    assert len(S2) == 1981, ("C1 FAIL |S2 cap 2e5|", len(S2))
    S3 = res[3][res[3] <= 60000]
    assert S3[:8].tolist() == [3475, 8174, 8175, 15195, 16168, 18682, 18743, 19290], \
        ("C1 FAIL S3 first8", S3[:8].tolist())
    assert len(S3) == 41, ("C1 FAIL |S3 cap 6e4|", len(S3))
    S4 = res[4][res[4] <= 60000]
    assert S4.tolist() == [8174, 51984], ("C1 FAIL S4", S4.tolist())
    print("C1 PASS: PROBLEM.md tables reproduced exactly "
          f"(|S2|=1981, S3 first8 ok, S4 cap 6e4 = [8174, 51984])")
    print(f"  also: |S3 cap 2e5| = {len(res[3])}, |S4 cap 2e5| = {len(res[4])}, "
          f"|S5 cap 2e5| = {len(res[5])}, |S6 cap 2e5| = {len(res[6])}")

    # ---- C2: agreement with in_Sk_fast on a block at 10^6 ----
    L, R = 10**6, 10**6 + 10**4
    ps = primes_upto(math.isqrt(R + 6) + 1)
    pd = primes_upto(math.isqrt(2 * (R - 1)) + 1)
    res2 = block_members(L, R, [2, 3], ps, pd)
    rng = np.random.default_rng(727)
    sample = rng.integers(L, R, 300)
    for k in (2, 3):
        mem = set(res2[k].tolist())
        # every claimed member verified, plus random non-members
        for n in res2[k].tolist():
            assert in_Sk_fast(int(n), k), ("C2 FAIL member", n, k)
        for n in sample.tolist():
            assert in_Sk_fast(int(n), k) == (n in mem), ("C2 FAIL sample", n, k)
    print(f"C2 PASS: block [1e6,1e6+1e4) agrees with in_Sk_fast "
          f"(members k=2: {len(res2[2])}, k=3: {len(res2[3])}; 300 random n each)")

    # ---- C3: kill profile on [1e6, 2e6) for k=2 ----
    L, R = 10**6, 2 * 10**6
    k = 2
    ps = primes_upto(math.isqrt(R + 6) + 1)
    pd = primes_upto(math.isqrt(2 * (R - 1)) + 1)
    t1 = time.time()
    rem = rough_rem(L + 1, R - 1 + k, ps)
    nvals = np.arange(L, R, dtype=np.int64)
    thr = isqrt_vec(2 * nvals)
    winmax = np.maximum(rem[0:R - L], rem[1:R - L + 1])
    surv = nvals[winmax <= thr]
    t2 = time.time()
    print(f"C3: survivors k=2 in [1e6,2e6): {len(surv)} "
          f"(density {len(surv)/(R-L):.4f}); rough sieve {t2-t1:.2f}s")
    # ascending-order kill counts
    alive = surv
    kills = []
    for p in pd.tolist():
        good = 2 * spvec(alive + k, p) - spvec(2 * alive, p) >= 2 * k
        kills.append((p, int(len(alive) - good.sum())))
        alive = alive[good]
    t3 = time.time()
    print(f"C3: members k=2 in [1e6,2e6): {len(alive)}; digit stage {t3-t2:.2f}s "
          f"(ascending order)")
    kills_sorted = sorted(kills, key=lambda t: -t[1])
    print("C3: top-20 killing primes (p, kills):", kills_sorted[:20])
    tot = sum(c for _, c in kills)
    csum, need = 0, []
    for p, c in kills_sorted:
        csum += c
        need.append(p)
        if csum >= 0.99 * tot:
            break
    print(f"C3: {len(need)} primes account for 99% of {tot} kills")
    with open("/home/user/erdos/attempts/route-R5/kill_order_k2.json", "w") as f:
        json.dump([p for p, _ in kills_sorted], f)
    # timing with sorted order
    from sievelib import load_kill_order
    ko = load_kill_order("/home/user/erdos/attempts/route-R5/kill_order_k2.json", pd)
    t4 = time.time()
    alive2 = surv
    for idx in ko:
        if len(alive2) == 0:
            break
        p = int(pd[idx])
        good = 2 * spvec(alive2 + k, p) - spvec(2 * alive2, p) >= 2 * k
        alive2 = alive2[good]
    t5 = time.time()
    assert np.array_equal(np.sort(alive2), np.sort(alive)), "C3 order-independence FAIL"
    print(f"C3: digit stage with kill-order {t5-t4:.2f}s (same members: order-independent OK)")
    print(f"total calibration time {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
