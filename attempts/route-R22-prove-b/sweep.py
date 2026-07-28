"""sweep.py -- route R22: parameter sweep for the head-delay architecture, plus the
sharpness probes that pin down exactly which hypotheses condition (ii) needs.

Every run reports: (ii) verdict over ALL 4-APs with largest term <= M (exact integer
arithmetic), the fibre ratios |F_j|/b^j, and the Lemma B1 budget identity.
"""

import sys, time
import numpy as np

sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
from arch import (blk_array, check_ii_fast, count_ii_violations, delay_head,
                  fibre_sizes, budget_identity_check)                      # noqa: E402


def seg_delay(M, b, s_of_m, K_of_m, where='head'):
    """t = K_m on a length-s_m segment of B_m placed at `where`."""
    t = np.zeros(M + 1, dtype=np.int64)
    m, lo = 0, 1
    while lo <= M:
        hi_full = lo * b - 1
        hi = min(M, hi_full)
        s = min(s_of_m(m), hi_full - lo + 1)
        if where == 'head':
            a, z = lo, lo + s - 1
        elif where == 'tail':
            a, z = hi_full - s + 1, hi_full
        else:                                   # interior
            a = (lo + hi_full) // 2
            z = a + s - 1
        a, z = max(a, lo), min(z, hi)
        if a <= z:
            t[a:z + 1] = K_of_m(m)
        m += 1
        lo *= b
    c = blk_array(M, b) + t
    c[0] = 0
    return t, c


def report(tag, b, M, t, c):
    t0 = time.time()
    w = check_ii_fast(c, M)
    fs = fibre_sizes(c, M)
    J = 0
    while b ** (J + 2) - 1 <= M:
        J += 1
    rat = [float(int(fs[j]) / b ** j) for j in range(J + 1)]
    bud = budget_identity_check(t, b, M)
    print(f"{tag:44s} b={b} M={M:7d}  (ii) "
          f"{'HOLDS ' if w is None else 'FAILS ' + str(w):46s}"
          f" fibre-ratio min={min(rat):.3f} max={max(rat):.3f}"
          f"  B1={'ok' if all(x[3] for x in bud) else 'MISMATCH'}  [{time.time()-t0:.0f}s]")
    return w is None


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else 'main'

    if which == 'main':
        cases = [
            # (b, M, s_of_m, K_of_m, label)
            (3, 3 ** 9,  lambda m: m + 1,             lambda m: m,       "HEAD s=m+1        K=m"),
            (3, 3 ** 9,  lambda m: 3 ** (m // 2),     lambda m: m,       "HEAD s=3^(m/2)    K=m"),
            (3, 3 ** 9,  lambda m: max(1, 3 ** m),    lambda m: 2 * m,   "HEAD s=3^m        K=2m"),
            (3, 3 ** 9,  lambda m: m + 1,             lambda m: m * m,   "HEAD s=m+1        K=m^2"),
            (3, 3 ** 9,  lambda m: m + 1,             lambda m: 2 ** m,  "HEAD s=m+1        K=2^m"),
            (4, 4 ** 7,  lambda m: m + 1,             lambda m: m,       "HEAD s=m+1        K=m"),
            (5, 5 ** 6,  lambda m: m + 1,             lambda m: m,       "HEAD s=m+1        K=m"),
            (7, 7 ** 5,  lambda m: m + 1,             lambda m: m,       "HEAD s=m+1        K=m"),
        ]
        allok = True
        for b, M, s, K, lab in cases:
            t, c = delay_head(M, b, s, K)
            allok &= report(lab, b, M, t, c)
        print("\nall (ii) verdicts HOLD" if allok else "\nsome case FAILED")

    elif which == 'sharp':
        b, M = 3, 3 ** 9
        s = lambda m: m + 1
        # segment position
        for where in ('head', 'tail', 'interior'):
            t, c = seg_delay(M, b, s, lambda m: m, where)
            report(f"seg={where:8s} K=m", b, M, t, c)
        # K non-monotone: gap 1 vs gap 2
        for gap in (1, 2, 3):
            t, c = delay_head(M, b, s, lambda m, g=gap: max(1, 40 - g * m))
            report(f"HEAD K decreasing by {gap} per block", b, M, t, c)
        # K non-decreasing but with a single dip of size 2 at m=5
        Kd = lambda m: (m if m != 5 else 2)
        t, c = delay_head(M, b, s, Kd)
        report("HEAD K=m with a dip K_5=2", b, M, t, c)
        # b = 2 (block-gap lemma needs b>=3)
        t, c = delay_head(2 ** 13, 2, lambda m: m + 1, lambda m: m)
        report("HEAD s=m+1 K=m  (b=2, outside hypothesis)", 2, 2 ** 13, t, c)

    elif which == 'big':
        b = int(sys.argv[2]); M = int(sys.argv[3])
        t, c = delay_head(M, b, lambda m: m + 1, lambda m: m)
        report("HEAD s=m+1 K=m  (large M)", b, M, t, c)

    elif which == 'kmono':
        # Does (K_m) non-decreasing actually matter?  The blocking case is
        # (j1,j2,j3) = (k,k+1,k+1) with x+d in H_k, x+2d in H_{k+1}: it needs
        # x <= 2 b^k + 2 s_k - b^{k+1} - 2, so it is vacuous unless s_k is LARGE.
        b, M = 3, 3 ** 9
        for slab, s in (("s=m+1", lambda m: m + 1),
                        ("s=3^m", lambda m: max(1, 3 ** m)),
                        ("s=(3^m*3)//2", lambda m: max(1, (3 ** m * 3) // 2))):
            for klab, K in (("K=m (incr)", lambda m: m),
                            ("K=40-2m (decr)", lambda m: max(1, 40 - 2 * m)),
                            ("K=40-5m (decr)", lambda m: max(1, 40 - 5 * m))):
                t, c = delay_head(M, b, s, K)
                report(f"{slab:14s} {klab}", b, M, t, c)
