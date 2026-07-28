"""Route R5 mining 5: base-p digit motifs of n+k, members vs controls.

Claims examined:
 M1. For p in {2,3,5,7,11,13}: mean s_p(n+k) and mean margin
     D_p = 2 s_p(n+k) - s_p(2n) - 2k for members vs (a) all n in a control
     range, (b) step-(a) survivors (smooth windows) in the same range.
 M2. Digit histogram of n+k base p (all positions pooled) members vs control.
 M3. Low-digit structure: distribution of (n+k) mod p and floor((n+k)/p) mod p.
 M4. Margin distribution: how tight is the digit condition at each p?
     (fraction of members with D_p = 0, i.e. zero slack.)
"""

import sys
import numpy as np

DATA = "/home/user/erdos/attempts/route-R5/data"
sys.path.insert(0, "/home/user/erdos/attempts/route-R5")
from sievelib import spvec, primes_upto, rough_rem, isqrt_vec
import math


def load(k, tags):
    parts = []
    for t in tags:
        try:
            parts.append(np.loadtxt(f"{DATA}/S{k}_{t}.txt", dtype=np.int64).reshape(-1))
        except OSError:
            pass
    return np.unique(np.concatenate(parts)) if parts else np.zeros(0, np.int64)


def digit_hist(vals, p):
    h = np.zeros(p, dtype=np.int64)
    a = vals.copy()
    while a.max(initial=0) > 0:
        h += np.bincount(a % p, minlength=p)
        a //= p
    return h


def survivors_in(L, R, k):
    ps = primes_upto(math.isqrt(R + k) + 1)
    rem = rough_rem(L + 1, R - 1 + k, ps)
    nvals = np.arange(L, R, dtype=np.int64)
    thr = isqrt_vec(2 * nvals)
    winmax = rem[0:R - L].copy()
    for j in range(2, k + 1):
        np.maximum(winmax, rem[j - 1:j - 1 + R - L], out=winmax)
    return nvals[winmax <= thr]


def main():
    tags = sys.argv[1:] or ["run1"]
    PRIMES = [2, 3, 5, 7, 11, 13]
    for k in [2, 3]:
        arr = load(k, tags)
        if len(arr) < 100:
            continue
        # control range: top half-decade of data
        X = int(arr[-1])
        L = X // 10
        mem = arr[arr >= L]
        rng = np.random.default_rng(727 + k)
        ctrl = np.sort(rng.integers(L, X, len(mem)))  # seeded uniform control
        # survivors control on a subrange
        SL, SR = L, min(L + 5 * 10**6, X)
        surv = survivors_in(SL, SR, k)
        print(f"\n== k={k}: members in [{L},{X}]: {len(mem)}; control {len(ctrl)}; "
              f"survivors in [{SL},{SR}): {len(surv)} ==")
        print(f"{'p':>3} {'E s_p(n+k) mem':>15} {'ctrl':>8} {'surv':>8} "
              f"{'E D_p mem':>10} {'ctrl':>8} {'surv':>8} {'P(D_p=0) mem':>13} {'P(D<0) surv':>12}")
        for p in PRIMES:
            def stats(v):
                s1 = spvec(v + k, p)
                D = 2 * s1 - spvec(2 * v, p) - 2 * k
                return s1.mean(), D.mean(), (D == 0).mean(), (D < 0).mean()
            m1, mD, mz, _ = stats(mem)
            c1, cD, _, _ = stats(ctrl)
            s1m, sD, _, sneg = stats(surv)
            print(f"{p:>3} {m1:>15.3f} {c1:>8.3f} {s1m:>8.3f} "
                  f"{mD:>10.3f} {cD:>8.3f} {sD:>8.3f} {mz:>13.4f} {sneg:>12.4f}")
        print(" [M2] pooled digit histograms of n+k (ratio member/control):")
        for p in [3, 5, 7]:
            hm = digit_hist(mem + k, p).astype(float)
            hc = digit_hist(ctrl + k, p).astype(float)
            hm /= hm.sum(); hc /= hc.sum()
            print(f"   p={p}: member {np.round(hm,4).tolist()} vs control "
                  f"{np.round(hc,4).tolist()}  ratio {np.round(hm/hc,3).tolist()}")
        print(" [M3] last two base-p digits of n+k, member enrichment ratio:")
        for p in [2, 3, 5]:
            d0 = (mem + k) % p
            d1 = ((mem + k) // p) % p
            joint = np.bincount(d1 * p + d0, minlength=p * p).astype(float)
            c0 = (ctrl + k) % p
            c1_ = ((ctrl + k) // p) % p
            cj = np.bincount(c1_ * p + c0, minlength=p * p).astype(float)
            cj[cj == 0] = 1
            rat = (joint / joint.sum()) / (cj / cj.sum())
            print(f"   p={p} (d1,d0) ratios: "
                  f"{[ (i//p, i%p, round(float(r),3)) for i, r in enumerate(rat)]}")


if __name__ == "__main__":
    main()
