#!/usr/bin/env python3
"""Exact combination step: choose at most one gadget from each pool so that the
values c_i/D add up to the target rho exactly.

Each pool file has lines "c n1 n2 ...".  The windows must be pairwise separated
(checked here).  We solve  sum_i c_i = rho*D  exactly by meet in the middle over
integers (numpy int64) --- no float, no rounding.

usage: combine.py D rho keep_per_pool out.txt pool1 pool2 ...
"""
import sys
import numpy as np
from fractions import Fraction


def load(fn, keep):
    P = {}
    for line in open(fn):
        t = line.split()
        P[int(t[0])] = [int(v) for v in t[1:]]
    cs = sorted(P)
    if len(cs) > keep:               # keep an evenly spread subsample
        idx = [round(i * (len(cs) - 1) / (keep - 1)) for i in range(keep)]
        cs = sorted(set(cs[i] for i in idx))
    return [(c, P[c]) for c in cs]


def build(pools, target, tail_max):
    """all achievable partial sums <= target, pruned by the remaining capacity"""
    sums = np.zeros(1, dtype=np.int64)
    codes = np.zeros(1, dtype=np.int64)
    mult = 1
    for k, pool in enumerate(pools):
        vals = np.array([0] + [c for c, _ in pool], dtype=np.int64)
        idxs = np.arange(len(vals), dtype=np.int64)
        s = (sums[:, None] + vals[None, :]).ravel()
        c = (codes[:, None] + mult * idxs[None, :]).ravel()
        lo = target - tail_max[k]
        m = (s <= target) & (s >= lo)
        sums, codes = s[m], c[m]
        mult *= len(vals)
        if len(sums) > 60_000_000:
            raise SystemExit("half too large (%d)" % len(sums))
    return sums, codes, mult


def decode(code, pools):
    out = []
    for pool in pools:
        n = len(pool) + 1
        i = code % n
        code //= n
        out.append(None if i == 0 else pool[i - 1])
    return out


def main():
    D = int(sys.argv[1]); rho = Fraction(sys.argv[2])
    keeps = [int(t) for t in sys.argv[3].split(",")]
    outfn = sys.argv[4]
    split = None
    files = sys.argv[5:]
    if files and files[0].startswith("split="):
        split = int(files[0][6:]); files = files[1:]
    if len(keeps) == 1:
        keeps = keeps * len(files)
    tgt = rho * D
    assert tgt.denominator == 1, "rho*D must be an integer"
    tgt = int(tgt)
    pools = [load(f, k) for f, k in zip(files, keeps)]
    for f, p in zip(files, pools):
        print("%-12s %5d values, c in [%d,%d]  (sum range [%.5f,%.5f])"
              % (f, len(p), p[0][0], p[-1][0], p[0][0] / D, p[-1][0] / D))
    h = split if split is not None else (len(pools) + 1) // 2
    A, B = pools[:h], pools[h:]
    # tail capacities
    maxc = [p[-1][0] for p in pools]
    tailA = [sum(maxc[k + 1:]) for k in range(len(pools))][:h]
    capA = sum(maxc[:h])
    tailB = [sum(maxc[h + k + 1:]) + capA for k in range(len(B))]
    sa, ca, _ = build(A, tgt, tailA)
    sb, cb, _ = build(B, tgt, tailB)
    print("half sizes: %d  %d" % (len(sa), len(sb)))
    o = np.argsort(sa, kind="stable")
    sa, ca = sa[o], ca[o]
    need = tgt - sb
    pos = np.searchsorted(sa, need)
    pos = np.clip(pos, 0, len(sa) - 1)
    hit = sa[pos] == need
    n = int(hit.sum())
    print("hits: %d" % n)
    if n == 0:
        return 1
    j = int(np.nonzero(hit)[0][0])
    pa, pb = int(ca[pos[j]]), int(cb[j])
    chosen = decode(pa, A) + decode(pb, B)
    U = []
    tot = Fraction(0)
    for item in chosen:
        if item is None:
            continue
        c, V = item
        U += V
        tot += Fraction(c, D)
    assert tot == rho, (tot, rho)
    U = sorted(U)
    with open(outfn, "w") as g:
        g.write(" ".join(map(str, U)) + "\n")
    print("wrote %s: %d elements, min %d, max %d, sum %s"
          % (outfn, len(U), U[0], U[-1], tot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
