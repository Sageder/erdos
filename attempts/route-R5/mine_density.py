"""Route R5 mining 1: density, gaps, adjacent pairs.

Claims examined (all descriptive statistics on exact member lists):
 D1. Counting-function fit: is |S_k cap [1,X]| ~ c_k X (linear) or X^alpha?
     Report counts at decades, local densities per decade, and log-log slope.
 D2. Nearest-member gap distribution vs n: max gap per decade, mean gap.
 D3. Adjacent pairs (n, n+1) both members; also runs of length >= 3.
     Note: n and n+1 both in S_k means window overlap of k-1 smooth numbers.
"""

import sys
import numpy as np

DATA = "/home/user/erdos/attempts/route-R5/data"


def load(k, tags):
    parts = []
    for t in tags:
        try:
            parts.append(np.loadtxt(f"{DATA}/S{k}_{t}.txt", dtype=np.int64).reshape(-1))
        except OSError:
            pass
    if not parts:
        return np.zeros(0, dtype=np.int64)
    arr = np.unique(np.concatenate(parts))
    return arr


def decade_stats(arr, lo=100, hi=None):
    """Rows: [X, count<=X, density in (X/10,X], maxgap in (X/10,X], meangap]"""
    if hi is None:
        hi = int(arr[-1]) + 1
    rows = []
    X = lo
    while X <= hi:
        c = int(np.searchsorted(arr, X, side="right"))
        c_prev = int(np.searchsorted(arr, X // 10, side="right"))
        seg = arr[c_prev:c]
        if len(seg) >= 2:
            g = np.diff(seg)
            rows.append((X, c, (c - c_prev) / (X - X // 10),
                         int(g.max()), float(g.mean())))
        else:
            rows.append((X, c, (c - c_prev) / (X - X // 10), None, None))
        X *= 10
    return rows


def main():
    ks = [2, 3, 4, 5, 6]
    tags = sys.argv[1:] or ["run1"]
    print(f"tags: {tags}")
    for k in ks:
        arr = load(k, tags)
        if len(arr) == 0:
            print(f"\n== k={k}: no members found ==")
            continue
        print(f"\n== k={k}: {len(arr)} members, min={arr[0]}, max={arr[-1]} ==")
        print(f"{'X':>12} {'count':>9} {'dens/decade':>12} {'maxgap':>8} {'meangap':>10}")
        for X, c, d, mg, avg in decade_stats(arr):
            mgs = str(mg) if mg is not None else "-"
            avgs = f"{avg:.1f}" if avg is not None else "-"
            print(f"{X:>12} {c:>9} {d:>12.6f} {mgs:>8} {avgs:>10}")
        # log-log slope over top two decades
        top = arr[-1]
        if len(arr) > 50:
            Xs = np.geomspace(max(1000, top / 100), top, 20)
            cs = np.searchsorted(arr, Xs.astype(np.int64), side="right")
            mask = cs > 0
            if mask.sum() >= 5:
                sl, ic = np.polyfit(np.log(Xs[mask]), np.log(cs[mask]), 1)
                print(f"log-log slope of count function over [{Xs[0]:.0f},{top}]: "
                      f"{sl:.4f} (1.0 = linear growth), c_k est = count/X = "
                      f"{len(arr)/top:.6f}")
        # adjacent pairs and runs
        d = np.diff(arr)
        pairs = int((d == 1).sum())
        # run lengths
        runs = []
        i = 0
        while i < len(arr):
            j = i
            while j + 1 < len(arr) and arr[j + 1] == arr[j] + 1:
                j += 1
            if j > i:
                runs.append((int(arr[i]), j - i + 1))
            i = j + 1
        maxrun = max((r for _, r in runs), default=1)
        print(f"adjacent pairs (n,n+1): {pairs}; maximal-run length: {maxrun}; "
              f"runs of len>=3: {[(s, r) for s, r in runs if r >= 3][:20]}")
        exp_pairs = (len(arr) ** 2) / arr[-1] if arr[-1] else 0
        print(f"  naive independent-density expectation of pairs ~ count^2/X = "
              f"{exp_pairs:.1f} -> enrichment factor {pairs/exp_pairs:.2f}"
              if exp_pairs else "")


if __name__ == "__main__":
    main()
