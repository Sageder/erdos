"""scan.py — broad explicit-rule scan over (class function) x (within-class comparator).

Each candidate is a genuine RULE: key(v) = (c(v), w(v)) with c of finite fibres, so the
induced order is a permutation of N of order type omega (CORE.md Lemma 1); its
value-restrictions to [1..M] are computed and checked exactly.

Output: minimal killing 4-AP (smallest largest-term) for each candidate = the failure
ledger of route R20.
"""
import sys
import numpy as np

sys.path.insert(0, '/home/user/erdos/attempts/route-R20-vlogv')
from framework import restrict, violations
from constructions import (cls_delay, cls_block, v2, logb, w_sigma, _sigma_key,
                           make_w_tau)


# ------------------------------------------------------------- within-class keys
def k_asc(v):
    return v


def k_desc(v):
    return -v


def k_sigma(v):
    return w_sigma(v)


def k_sigma_rev(v):
    return tuple(1 - x for x in w_sigma(v))


def make_k_revblocks(g, inner):
    """blocks [g^i, g^{i+1}) taken in DECREASING order, `inner` inside each."""
    def k(v):
        return (-logb(v, g), inner(v))
    return k


def make_k_blocks(g, inner):
    def k(v):
        return (logb(v, g), inner(v))
    return k


def k_bitrev(v):
    """reverse the binary digits of v (below the leading 1)."""
    s = bin(v)[3:]
    return int(s[::-1], 2) if s else 0


def k_oddpart_sigma(v):
    return (_sigma_key(v >> v2(v)), v2(v))


def k_v2_then_sigma(v):
    return (v2(v), w_sigma(v))


def k_negv2_then_sigma(v):
    return (-v2(v), w_sigma(v))


def k_T(v):
    """Theorem-14 order: blocks [3^i,3^{i+1}) increasing, DECREASING inside.
    No increasing monotone 4-AP on any subset."""
    return (logb(v, 3), -v)


def k_Trev(v):
    return (-logb(v, 3), v)


WITHIN = {
    'asc': k_asc,
    'desc': k_desc,
    'sigma': k_sigma,
    'sigma_rev': k_sigma_rev,
    'T(3)': k_T,
    'Trev(3)': k_Trev,
    'revblk2-sigma': make_k_revblocks(2, k_sigma),
    'revblk3-sigma': make_k_revblocks(3, k_sigma),
    'revblk5-sigma': make_k_revblocks(5, k_sigma),
    'revblk3-asc': make_k_revblocks(3, k_asc),
    'revblk2-asc': make_k_revblocks(2, k_asc),
    'blk3-desc': make_k_blocks(3, k_desc),
    'bitrev': k_bitrev,
    'oddpart-sigma': k_oddpart_sigma,
    'v2-sigma': k_v2_then_sigma,
    'negv2-sigma': k_negv2_then_sigma,
    'tau012': make_w_tau([(0, 1, 2)]),
    'tau120': make_w_tau([(1, 2, 0)]),
    'tau_alt': make_w_tau([(0, 1, 2), (1, 2, 0)]),
}

CLASSES = {}
for b in (3, 4, 5, 6, 7):
    CLASSES[f'CLS({b},a)'] = cls_delay(b, lambda a: a)
for b in (3, 5):
    CLASSES[f'CLS({b},2a)'] = cls_delay(b, lambda a: 2 * a)
CLASSES['BLK(3)'] = cls_block(3)
CLASSES['BLK(5)'] = cls_block(5)
CLASSES['FLAT'] = (lambda v: 0)          # no class structure at all (control)


if __name__ == "__main__":
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    res = []
    for cn, c in CLASSES.items():
        for wn, w in WITHIN.items():
            key = (lambda c=c, w=w: (lambda v: (c(v), w(v))))()
            perm = restrict(key, M)
            vio = violations(perm, 4)
            if not vio:
                res.append((10**9, cn, wn, "SURVIVES"))
            else:
                x, d, s = vio[0]
                res.append((x + 3 * d, cn, wn,
                            f"({x},{d},{s})  terms {x},{x+d},{x+2*d},{x+3*d}"))
    res.sort(reverse=True)
    print(f"# scan at M={M}: {len(res)} candidates, sorted by survival\n")
    for mt, cn, wn, info in res[:60]:
        tag = "SURVIVES to M" if mt == 10**9 else f"dies@{mt}"
        print(f"{cn:12s} x {wn:16s} {tag:16s} {info}")
