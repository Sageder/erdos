#!/usr/bin/env python3
"""
Recon-3: audit of the CRUX ==> YES reduction (the "chaining" of the intervals
[r(U), cap(U)]).

Nothing here is a proof of anything about Erdos 289; it measures the quantities
the chaining argument silently assumes to be controlled:

  * how often r(U) = cap(U) (a SINGLETON interval: such a solution certifies
    exactly one value of k);
  * the ratio r/cap as a function of min(U) -- the argument needs it bounded
    away from 1 for the far-out solutions, not for the near ones;
  * what the coverage looks like if one only uses solutions with min(U) >= T
    (i.e. exactly the objects CRUX provides);
  * whether run lengths >= 4 (the only source of interval length) survive when
    min(U) grows.
"""
from fractions import Fraction
import statistics, sys

ALLSOLS = "/home/user/erdos/experiments/ALLSOLS.txt"


def runs(v):
    out, i = [], 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[j] + 1:
            j += 1
        out.append(j - i + 1)
        i = j + 1
    return out


def main():
    sols = []
    for line in open(ALLSOLS):
        p = line.split()
        if p and p[0] == "SOL":
            v = [int(x) for x in p[1:]]
            L = runs(v)
            sols.append((v, len(L), sum(x // 2 for x in L), min(v), max(v), L))

    print("total solutions:", len(sols))
    print()
    print("  T  #sols(min>=T)  coverage of union[r,cap]   holes  singleton-frac  max run len")
    for T in [2, 10, 20, 30, 35, 40, 45, 48, 50]:
        sel = [s for s in sols if s[3] >= T]
        if not sel:
            print("  %2d  none" % T); continue
        cov = set()
        for (_, r, c, _, _, _) in sel:
            cov.update(range(r, c + 1))
        lo, hi = min(cov), max(cov)
        holes = [k for k in range(lo, hi + 1) if k not in cov]
        sing = sum(1 for s in sel if s[1] == s[2]) / len(sel)
        mrl = max(max(s[5]) for s in sel)
        print("  %2d  %10d      [%d..%d]              %-22s %.3f          %d"
              % (T, len(sel), lo, hi, str(holes[:8]) + ("..." if len(holes) > 8 else ""), sing, mrl))

    print()
    print("ratio r/cap by min(U) band:")
    for lo, hi in [(2, 9), (10, 19), (20, 29), (30, 39), (40, 50)]:
        sel = [s for s in sols if lo <= s[3] <= hi]
        if not sel:
            continue
        rr = [s[1] / s[2] for s in sel]
        print("   min(U) in [%2d,%2d]: n=%6d  min r/cap=%.4f  median=%.4f  frac(r==cap)=%.3f"
              % (lo, hi, len(sel), min(rr), statistics.median(rr),
                 sum(1 for s in sel if s[1] == s[2]) / len(sel)))

    print()
    print("run-length distribution overall:")
    from collections import Counter
    c = Counter()
    for s in sols:
        c.update(s[5])
    tot = sum(c.values())
    for L in sorted(c):
        print("   L=%2d : %8d  (%.4f)" % (L, c[L], c[L] / tot))

    print()
    print("interval length cap-r distribution:")
    c2 = Counter(s[2] - s[1] for s in sols)
    for d in sorted(c2):
        print("   cap-r=%2d : %8d" % (d, c2[d]))

    print()
    print("solutions with the largest min(U):")
    sel = sorted(sols, key=lambda s: -s[3])[:12]
    for (v, r, cp, mn, mx, L) in sel:
        print("   min=%3d max=%3d |U|=%3d r=%3d cap=%3d  runs=%s" % (mn, mx, len(v), r, cp, L))


if __name__ == "__main__":
    main()
