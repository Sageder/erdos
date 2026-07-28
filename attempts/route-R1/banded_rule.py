"""banded_rule.py — hand-built banded ratio-5 gadget rules, machine-checked.

Pure ratio-5 chain: blocks B_k = (5^{k-1}, 5^k], k = 1..K, in increasing position
order.  Rule family for a block (m, 5m]:
   segments in POSITION order:  S1 = (t1*m, t2*m], S2 = (t2*m, 5m], S3 = (p*m, t1*m],
   S4 = (m, p*m]      (mirrors the SAT witness banding: upper-middle, top, middle, bottom)
   with rational band edges (t1, t2, p) and a gadget from the sigma family per segment.
Machine check: build K blocks, restrict to M = 5^K - 1, exact vectorized 4-AP scan
(framework.monotone_4ap_violations).  A rule passing K = 6 blocks (M = 15624) meets
the 10^4 deliverable bar and would certify stages 1..6 of the chain.
"""

import sys
from fractions import Fraction as F
sys.path.insert(0, "/home/user/erdos/attempts/route-R1")
from framework import (gadget_sigma, gadget_sigma_reflect, gadget_sigma_revpos,
                       gadget_sigma_reflect_revpos, gadget_evens_first,
                       monotone_4ap_violations, restrict_to_M)

GADGETS = {'s': gadget_sigma, 'R': gadget_sigma_reflect, 'p': gadget_sigma_revpos,
           'B': gadget_sigma_reflect_revpos, 'e': gadget_evens_first}


def banded_block(m, t1, t2, p, gs):
    """Order of block (m, 5m] with band edges m < p*m < t1*m < t2*m <= 5m and
    gadget keys gs = (g1, g2, g3, g4) for segments S1..S4 (position order
    S1, S2, S3, S4 as in the docstring). Edges are Fractions; endpoints rounded."""
    e0, e1, e2, e3, e4 = m, int(m * p), int(m * t1), int(m * t2), 5 * m
    assert m <= e1 <= e2 <= e3 <= e4
    segs_pos_order = [(e2 + 1, e3 + 1), (e3 + 1, e4 + 1), (e1 + 1, e2 + 1), (e0 + 1, e1 + 1)]
    out = []
    for (lo, hi), g in zip(segs_pos_order, gs):
        if hi > lo:
            out.extend(GADGETS[g](lo, hi))
    assert sorted(out) == list(range(m + 1, 5 * m + 1)), (m, t1, t2, p)
    return out


def build_chain(K, t1, t2, p, gs, first_block=('s',)):
    """Blocks (5^{k-1}, 5^k] for k=1..K in order; block 1 = (1,5] uses sigma-family
    gadget directly (too small to band)."""
    seq = []
    seq.extend(GADGETS[first_block[0]](2, 6))    # values 2..5
    seq.insert(0, 1)                             # value 1 first (block (0,1]... put 1 at front)
    for k in range(2, K + 1):
        m = 5 ** (k - 1)
        seq.extend(banded_block(m, t1, t2, p, gs))
    return seq


def check_rule(K, t1, t2, p, gs, max_report=4):
    seq = build_chain(K, t1, t2, p, gs)
    M = 5 ** K - 1
    perm = restrict_to_M(seq, M)
    viol, total = monotone_4ap_violations(perm, max_report=max_report)
    return total, viol


if __name__ == "__main__":
    import itertools, time
    # stage 1: coarse sweep at K=3 (M=124) — cheap filter
    t0 = time.time()
    grid_t1 = [F(16, 5), F(17, 5), F(7, 2), F(18, 5)]      # ~3.2-3.6
    grid_t2 = [F(19, 5), F(4, 1), F(21, 5), F(22, 5)]      # ~3.8-4.4
    grid_p  = [F(9, 5), F(2, 1), F(11, 5), F(12, 5)]       # ~1.8-2.4
    best = []
    n_tested = 0
    for t1 in grid_t1:
        for t2 in grid_t2:
            if t2 <= t1:
                continue
            for p in grid_p:
                for gs in itertools.product('sRpBe', repeat=4):
                    n_tested += 1
                    tot, _ = check_rule(3, t1, t2, p, gs, max_report=0)
                    if tot == 0:
                        best.append((t1, t2, p, gs))
    print(f"K=3 sweep: {n_tested} rules tested, {len(best)} pass M=124 ({time.time()-t0:.0f}s)",
          flush=True)
    # stage 2: survivors at K=4 (M=624)
    surv4 = []
    for (t1, t2, p, gs) in best:
        tot, viol = check_rule(4, t1, t2, p, gs, max_report=0)
        if tot == 0:
            surv4.append((t1, t2, p, gs))
    print(f"K=4: {len(surv4)} of {len(best)} survive M=624", flush=True)
    for r in surv4[:20]:
        print("   K4-pass:", r, flush=True)
    # stage 3: survivors at K=5, K=6
    for K, M in ((5, 3124), (6, 15624)):
        nxt = []
        for (t1, t2, p, gs) in surv4:
            tot, viol = check_rule(K, t1, t2, p, gs, max_report=3)
            if tot == 0:
                nxt.append((t1, t2, p, gs))
            elif K == 5 and len(nxt) == 0 and len(viol):
                pass
        print(f"K={K}: {len(nxt)} survive M={M}", flush=True)
        for r in nxt[:10]:
            print(f"   K{K}-pass:", r, flush=True)
        surv4 = nxt
        if not surv4:
            break
    print("BANDED SEARCH DONE", flush=True)
