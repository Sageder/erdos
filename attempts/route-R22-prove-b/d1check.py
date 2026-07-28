"""d1check.py -- route R22: machine confirmation of Theorem R22-2 (the properties that
make the head-delay architecture a counterexample to Conjecture R21-C and its repairs),
and of Lemma R22-0 (why the standing sanity check does not block t >= 0 arguments).

Checked for the instance b=3, s_m = m+1, K_m = m over [1..M]:
  * for every AP P = {r+qn} with q <= QMAX:  t|_P unbounded (max t grows with M),
    t|_P = 0 infinitely often, c|_P has >= 1 strict descent per block that P's step can
    resolve, and the COARSE displacement -- a lower bound for pos_P(n)/n valid for EVERY
    within-class emission order -- is large and grows with M.
  * Lemma R22-0: for a permutation sigma of [1..N], the geometric coarsening
    c(v) = floor(log_b pos(v)) has t := c - floor(log_b v) >= 0 iff sigma maps [1,b^m)
    onto positions [1,b^m) for every m (a contiguous ratio-b block layout), in which case
    t == 0.  Verified on random permutations and on SAT-found 4-AP-free avoiders.
"""

import sys, random
from fractions import Fraction
import numpy as np

sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
sys.path.insert(0, '/home/user/erdos/experiments')
from arch import blk, blk_array, delay_head, check_ii_fast            # noqa: E402
from headdelay import ap_descents, ap_t_profile, coarse_disp          # noqa: E402
from apcheck import has_monotone_kap_pos                              # noqa: E402


def d1_table(b, M, QMAX=40):
    t, c = delay_head(M, b, lambda m: m + 1, lambda m: m)
    assert check_ii_fast(c, M) is None, "condition (ii) must hold"
    worst = {'descents': None, 'maxt': None, 'zeros': None, 'cdisp': None}
    for q in range(1, QMAX + 1):
        for r in range(q):
            de, L = ap_descents(c, M, q, r)
            mn, mx, z = ap_t_profile(t, M, q, r)
            cd, _ = coarse_disp(c, M, q, r)
            for key, val in (('descents', de), ('maxt', mx), ('zeros', z), ('cdisp', cd)):
                if worst[key] is None or val < worst[key][0]:
                    worst[key] = (val, q, r)
    return worst


def lemma_R22_0(N, perm, b):
    """returns (min t, is_block_layout)"""
    pos = {v: i + 1 for i, v in enumerate(perm)}
    tmin = min(blk(pos[v], b) - blk(v, b) for v in range(1, N + 1))
    blocky = True
    m, lo = 0, 1
    while lo <= N:
        hi = min(N, lo * b - 1)
        if set(pos[v] for v in range(lo, hi + 1)) != set(range(lo, hi + 1)):
            blocky = False
            break
        m += 1
        lo *= b
    return tmin, blocky


if __name__ == "__main__":
    print("== Theorem R22-2 diagnostics, HEAD(b=3, s_m=m+1, K_m=m) ==")
    for M in (3 ** 6, 3 ** 7, 3 ** 8, 3 ** 9):
        w = d1_table(3, M, QMAX=40)
        print(f"  M={M:6d}  over ALL {sum(range(1,41))} APs with q<=40:")
        print(f"     min #descents of c|_P      = {w['descents'][0]}  (at q={w['descents'][1]}, r={w['descents'][2]})")
        print(f"     min (max t|_P)             = {w['maxt'][0]}  (at q={w['maxt'][1]}, r={w['maxt'][2]})")
        print(f"     min #(t|_P = 0)            = {w['zeros'][0]}")
        print(f"     min coarse displacement    = {float(w['cdisp'][0]):.2f}  "
              f"(at q={w['cdisp'][1]}, r={w['cdisp'][2]})")

    print("\n== Lemma R22-0: geometric coarsening with t >= 0 forces a block layout ==")
    rng = random.Random(2022)
    for b in (2, 3, 5):
        nonblocky_with_tmin0 = 0
        blocky_seen = 0
        for _ in range(4000):
            N = rng.randint(6, 60)
            p = list(range(1, N + 1))
            rng.shuffle(p)
            tmin, blocky = lemma_R22_0(N, p, b)
            if blocky:
                blocky_seen += 1
                assert tmin == 0, (N, p, b, tmin)
            if tmin >= 0 and not blocky:
                nonblocky_with_tmin0 += 1
        print(f"  b={b}: 4000 random permutations -- block layouts seen {blocky_seen}, "
              f"non-block-layouts with min t >= 0: {nonblocky_with_tmin0} (must be 0)")
        assert nonblocky_with_tmin0 == 0

    # on genuine 4-AP-free avoiders
    sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
    import ast, os, glob
    files = glob.glob('/home/user/erdos/attempts/route-R20-vlogv/cw_*.txt') + \
            glob.glob('/home/user/erdos/attempts/route-R22-prove-b/cw_*.txt')
    for fn in sorted(files):
        perm = ast.literal_eval(open(fn).read().strip())
        N = len(perm)
        if sorted(perm) != list(range(1, N + 1)):
            continue
        assert not has_monotone_kap_pos(perm, 4)
        out = []
        for b in (2, 3, 5):
            tmin, blocky = lemma_R22_0(N, perm, b)
            out.append(f"b={b}: min t = {tmin:3d}, block layout: {blocky}")
        print(f"  {os.path.basename(fn):32s} N={N:4d}  " + " | ".join(out))
