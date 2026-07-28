"""Route R5 mining 4: window factorization structure of members.

For members n of S_k (k >= 3 fully; k = 2 on a random sample), factorize the
window elements n+1..n+k and report:
 W1. P(n) = max_j lpf(n+j) relative to sqrt(2n): distribution of
     u = log P / log sqrt(2n) (u <= 1 by the large-prime criterion) and of
     P/sqrt(2n).
 W2. Which slot j in 1..k carries the overall largest prime factor.
 W3. Window "shapes": exponent pattern signatures, counts of window elements
     that are perfect powers, twice-squares, 3-smooth, etc.
 W4. lpf of each slot separately (medians).
Exact integer factorization via sympy.factorint.
"""

import math
import sys
from collections import Counter

import numpy as np
from sympy import factorint

DATA = "/home/user/erdos/attempts/route-R5/data"


def load(k, tags):
    parts = []
    for t in tags:
        try:
            parts.append(np.loadtxt(f"{DATA}/S{k}_{t}.txt", dtype=np.int64).reshape(-1))
        except OSError:
            pass
    return np.unique(np.concatenate(parts)) if parts else np.zeros(0, np.int64)


def analyze(k, arr, label, sample_cap=None, seed=5):
    arr = arr[arr > 2 * k * k]
    if sample_cap and len(arr) > sample_cap:
        rng = np.random.default_rng(seed)
        arr = np.sort(rng.choice(arr, sample_cap, replace=False))
        label += f" (sample {sample_cap})"
    if len(arr) == 0:
        print(f"\n== k={k}: no members ==")
        return
    print(f"\n== k={k} {label}: {len(arr)} windows factorized ==")
    us, ratios, slot_of_max = [], [], []
    slot_lpf = {j: [] for j in range(1, k + 1)}
    shapes = Counter()
    specials = Counter()
    for n in arr.tolist():
        r = math.isqrt(2 * n)
        best_p, best_j = 0, 0
        shape = []
        for j in range(1, k + 1):
            f = factorint(n + j)
            lp = max(f)
            slot_lpf[j].append(lp)
            if lp > best_p:
                best_p, best_j = lp, j
            # shape signature: sorted exponent multiset size info
            exps = sorted(f.values(), reverse=True)
            shape.append(tuple(exps))
            if all(p in (2, 3) for p in f):
                specials[f"slot{j}:3smooth"] += 1
            if len(f) == 1 and exps[0] >= 2:
                specials[f"slot{j}:primepower"] += 1
            sq = math.isqrt(n + j)
            if sq * sq == n + j:
                specials[f"slot{j}:square"] += 1
            if (n + j) % 2 == 0:
                h = (n + j) // 2
                sq = math.isqrt(h)
                if sq * sq == h:
                    specials[f"slot{j}:2*square"] += 1
        us.append(math.log(best_p) / math.log(r) if r > 1 else 0)
        ratios.append(best_p / r)
        slot_of_max.append(best_j)
        shapes[tuple(shape)] += 1
    us = np.array(us)
    ratios = np.array(ratios)
    print(f" [W1] u = log(maxLPF)/log(sqrt(2n)): mean {us.mean():.4f}, "
          f"quantiles 10/50/90/99/100%: "
          f"{np.percentile(us, [10, 50, 90, 99, 100]).round(4).tolist()}")
    print(f"      P/sqrt(2n): quantiles 50/90/99/100%: "
          f"{np.percentile(ratios, [50, 90, 99, 100]).round(4).tolist()}; "
          f"frac > 0.5: {(ratios > 0.5).mean():.3f}, > 0.9: {(ratios > 0.9).mean():.4f}")
    cnt = Counter(slot_of_max)
    print(f" [W2] slot of max LPF: {dict(sorted(cnt.items()))} "
          f"(uniform would be {len(arr)/k:.0f} each)")
    med = {j: int(np.median(slot_lpf[j])) for j in slot_lpf}
    print(f" [W4] median lpf by slot: {med}")
    print(f" [W3] top 10 window shapes (tuple of exponent-multisets per slot):")
    for sh, c in shapes.most_common(10):
        print(f"      {c:>6}  {sh}")
    print(f" [W3] specials: {dict(sorted(specials.items()))}")


def main():
    tags = sys.argv[1:] or ["run1"]
    for k in [3, 4, 5, 6]:
        arr = load(k, tags)
        analyze(k, arr, "all members", sample_cap=20000)
    arr = load(2, tags)
    analyze(2, arr, "members", sample_cap=20000)


if __name__ == "__main__":
    main()
