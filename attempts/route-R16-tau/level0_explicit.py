"""level0_explicit.py — hunt for an EXPLICIT order of type omega solving the LEVEL-0
PROBLEM (no monotone 4-AP whose common difference is coprime to 3).

Architecture: contiguous base-3 blocks D_j = [3^j, 3^{j+1}) listed in increasing j
(order type omega, pos(v) <= 3v-1), with an explicit internal rule.  SAT says SOME
internal orders work up to N = 300; this script asks whether a simple closed-form rule
does.  All candidates are checked on [1..M] for monotone 4-APs with 3 not dividing d,
and (as a control) for monotone 4-APs at ALL d.
"""

import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from taulib import Tau, prio_const, prio_levels, v3, dig3, first_mono4


def blk(n):
    l = 0
    while 3 ** (l + 1) <= n:
        l += 1
    return l


def taukey(n, prio=(0, 1, 2), depth=20, start=0):
    k = []
    m = n // 3 ** start
    for _ in range(depth):
        k.append(prio[m % 3])
        m //= 3
    return tuple(k)


CANDS = {
    "blocks + tau": lambda n: (blk(n),) + taukey(n),
    "blocks + tau_rev": lambda n: (blk(n),) + taukey(n, (2, 1, 0)),
    "blocks + tau(alt by j)": lambda n: (blk(n),) + taukey(n, (0, 1, 2) if blk(n) % 2 == 0
                                                          else (2, 1, 0)),
    "blocks + decreasing": lambda n: (blk(n), -n),
    "blocks + increasing": lambda n: (blk(n), n),
    "blocks + tau_from_lvl1 then dig0": lambda n: (blk(n),) + taukey(n, start=1) + (n % 3,),
    "blocks + tau_from_lvl1 then dig0 rev": lambda n: (blk(n),) + taukey(n, start=1) + (-(n % 3),),
    "blocks + (dig0 prio, decreasing)": lambda n: (blk(n), n % 3, -n),
    "blocks + (dig0 prio rev, decreasing)": lambda n: (blk(n), -(n % 3), -n),
    "blocks + (dig0 prio, increasing)": lambda n: (blk(n), n % 3, n),
    "blocks + (dig0 alt by j, decreasing)": lambda n: (blk(n), (n % 3) * (1 if blk(n) % 2 == 0
                                                                         else -1), -n),
    "blocks + tau_rev_from_lvl1 then dig0": lambda n: (blk(n),) + taukey(n, (2, 1, 0), start=1)
    + (n % 3,),
}


def fast_scan(perm, coprime3_only):
    """First monotone 4-AP (smallest max-term) of a permutation of [1..M], numpy."""
    import numpy as np
    M = len(perm)
    pos = np.empty(M + 1, dtype=np.int64)
    pos[np.asarray(perm, dtype=np.int64)] = np.arange(M, dtype=np.int64)
    best = None
    for d in range(1, (M - 1) // 3 + 1):
        if coprime3_only and d % 3 == 0:
            continue
        top = M - 3 * d
        if top < 1:
            break
        p0 = pos[1:top + 1]
        p1 = pos[1 + d:top + d + 1]
        p2 = pos[1 + 2 * d:top + 2 * d + 1]
        p3 = pos[1 + 3 * d:top + 3 * d + 1]
        inc = (p0 < p1) & (p1 < p2) & (p2 < p3)
        dec = (p0 > p1) & (p1 > p2) & (p2 > p3)
        for orient, mask in ((1, inc), (-1, dec)):
            nz = np.nonzero(mask)[0]
            if nz.size:
                x = int(nz[0]) + 1
                cand = (x, d, orient)
                if best is None or x + 3 * d < best[0] + 3 * best[1]:
                    best = cand
        if best is not None and 3 * d >= best[0] + 3 * best[1]:
            break
    return best


if __name__ == "__main__":
    M = 20000
    for name, key in CANDS.items():
        perm = sorted(range(1, M + 1), key=key)
        w0 = fast_scan(perm, True)
        wa = fast_scan(perm, False)
        s0 = "CLEAN(3∤d)" if w0 is None else (f"3∤d dies x={w0[0]} d={w0[1]} "
                                             f"{'inc' if w0[2] == 1 else 'dec'} "
                                             f"top={w0[0]+3*w0[1]}")
        sa = "clean(all d)" if wa is None else (f"all-d dies top={wa[0]+3*wa[1]}")
        print(f"  {name:<40} {s0:<38} | {sa}")
