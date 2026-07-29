"""screen1.py — numeration-system comparator screen (Zeckendorf / Ostrowski / factorial).

For each candidate ORDER on N (given by a sort key) we report
  * the minimal monotone 4-AP of the value-restriction to [1..N]  (None = survives)
  * the omega-diagnostic pos_N(v) for small v at two board sizes (a type-omega order has
    these STABILIZE; an LSD comparator has them grow linearly in N)
  * max displacement max_v pos(v)/v on the board.
Everything exact; the 4-AP scan is apkit, cross-validated against experiments/apcheck.py.
"""
import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from apkit import pos_from_key, find_4aps
from numeration import (base_digits, factorial_digits, zeck_digits, fibs_upto,
                        ostrowski_digits, ostrowski_denoms)

PAD = (0,) * 64


def lsd_key(digitfn, rankfn=None):
    """compare at the SMALLEST differing level: lexicographic on the LSD-first list."""
    def key(v):
        d = digitfn(v)
        if rankfn is not None:
            d = [rankfn(k, c) for k, c in enumerate(d)]
        return tuple(d) + PAD
    return key


def msd_key(digitfn, rankfn=None, maxlen=64):
    """compare at the LARGEST differing level: pad to fixed length, reverse, lex."""
    def key(v):
        d = digitfn(v)
        if rankfn is not None:
            d = [rankfn(k, c) for k, c in enumerate(d)]
        d = list(d) + [0] * (maxlen - len(d))
        return tuple(reversed(d))
    return key


def report(name, key, N, probes=(1, 2, 3, 5)):
    pos, _ = pos_from_key(N, key)
    hits = find_4aps(pos, N)
    posH, _ = pos_from_key(N // 3, key)
    om = {v: (int(posH[v]) + 1, int(pos[v]) + 1) for v in probes}
    disp = max((int(pos[v]) + 1) / v for v in range(1, N + 1))
    if hits:
        top, d, x, orient = hits[0]
        ap = f"KILLED by ({x},{x+d},{x+2*d},{x+3*d}) d={d} {orient}"
    else:
        ap = f"4-AP-FREE to N={N}"
    print(f"{name:44s} | {ap:48s} | pos@N/3,N {om} | maxdisp {disp:.1f}")
    return hits


if __name__ == "__main__":
    N = 4000
    F = fibs_upto(N)
    cf_g = [1] * 40
    qg = ostrowski_denoms(cf_g, N)
    cf_p = [2] * 30
    qp = ostrowski_denoms(cf_p, N)
    cf_e = [1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, 10, 1, 1, 12, 1, 1, 14]  # e-like
    qe = ostrowski_denoms(cf_e, N)

    zd = lambda v: zeck_digits(v, F)
    pd = lambda v: ostrowski_digits(v, cf_p, qp)
    ed = lambda v: ostrowski_digits(v, cf_e, qe)
    fd = factorial_digits

    print("=== controls: base-b LSD comparators (known to kill; known NOT type omega) ===")
    report("base-3 LSD (0<1<2)", lsd_key(lambda v: base_digits(v, 3)), N)
    b4rank = {0: 0, 1: 1, 3: 2, 2: 3}
    report("base-4 LSD (0<1<3<2)", lsd_key(lambda v: base_digits(v, 4),
                                           lambda k, c: b4rank[c]), N)
    print()
    print("=== Zeckendorf / Fibonacci numeration ===")
    report("Zeckendorf LSD (0<1 every level)", lsd_key(zd), N)
    report("Zeckendorf LSD (alternating level order)",
           lsd_key(zd, lambda k, c: c if k % 2 == 0 else 1 - c), N)
    report("Zeckendorf LSD (all levels reversed)", lsd_key(zd, lambda k, c: 1 - c), N)
    report("Zeckendorf MSD (0<1)", msd_key(zd), N)
    report("Zeckendorf MSD (alternating)",
           msd_key(zd, lambda k, c: c if k % 2 == 0 else 1 - c), N)
    print()
    print("=== Ostrowski numeration, alpha = sqrt(2)-1  (cf [2,2,2,...]) ===")
    report("Ostrowski-Pell LSD (natural digit order)", lsd_key(pd), N)
    report("Ostrowski-Pell LSD (0<2<1)",
           lsd_key(pd, lambda k, c: {0: 0, 2: 1, 1: 2}[c]), N)
    report("Ostrowski-Pell MSD", msd_key(pd), N)
    print()
    print("=== Ostrowski numeration, unbounded partial quotients ===")
    report("Ostrowski-e LSD (natural)", lsd_key(ed), N)
    print()
    print("=== factorial base (mixed radix, growing) ===")
    report("factorial LSD (natural digit order)", lsd_key(fd), N)

    def fact_rank(k, c):
        b = k + 2                      # level k has digits 0..k+1
        # order 0,1,3,2,... -- swap 2 and 3 when available (the b=4 trick)
        if b >= 4:
            r = {0: 0, 1: 1, 3: 2, 2: 3}
            if c in r:
                return r[c]
            return c
        return c
    report("factorial LSD (0<1<3<2 per level)", lsd_key(fd, fact_rank), N)
