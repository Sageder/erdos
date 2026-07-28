"""mine.py — structural mining of surviving avoiders (deliverable 3).

For a given avoider file (avoiders/<cls>_<num>_<den>.txt), takes the largest-N avoiders
and reports:
  - displacement statistics: pi(v)-v distribution, max |pi(v)-v|, max pi(v)/v, min pi(v)/v;
  - longest increasing / decreasing subsequence lengths (LIS/LDS) vs N;
  - block decomposition: maximal intervals of positions whose value set is an interval
    of values (complete blocks); reports the block size sequence;
  - where small values sit; inversion count; count of monotone 3-APs (they are allowed);
  - self-similarity probe: Kendall-tau-style comparison of first-half pattern vs whole.
Output: text to stdout; optionally a plot per file into results/.
"""

import bisect
import os
import sys
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos


def lis_len(seq):
    tails = []
    for v in seq:
        i = bisect.bisect_left(tails, v)
        if i == len(tails):
            tails.append(v)
        else:
            tails[i] = v
    return len(tails)


def blocks(perm):
    """Maximal cut decomposition: positions split at i whenever {perm[0..i-1]} = {1..i}."""
    n = len(perm)
    out = []
    mx = 0
    last = 0
    for i, v in enumerate(perm, start=1):
        mx = max(mx, v)
        if mx == i:
            out.append(perm[last:i])
            last = i
    return out


def count_mono3(perm):
    n = len(perm)
    pos = {v: i for i, v in enumerate(perm)}
    c = 0
    for d in range(1, (n - 1) // 2 + 1):
        for x in range(1, n - 2 * d + 1):
            p = (pos[x], pos[x + d], pos[x + 2 * d])
            if p[0] < p[1] < p[2] or p[0] > p[1] > p[2]:
                c += 1
    return c


def analyze(perm, label=""):
    n = len(perm)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    disp = [pos[v] - v for v in range(1, n + 1)]
    ratio = [pos[v] / v for v in range(1, n + 1)]
    lis = lis_len(perm)
    lds = lis_len([-v for v in perm])
    bl = blocks(perm)
    blsizes = [len(b) for b in bl]
    inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
    m3 = count_mono3(perm)
    print(f"--- {label} N={n}")
    print(f"  perm = {','.join(map(str, perm))}")
    print(f"  max pi(v)-v = {max(disp)}, min = {min(disp)}, "
          f"max pi/v = {max(ratio):.3f}, min pi/v = {min(ratio):.3f}")
    print(f"  LIS = {lis}, LDS = {lds}  (N^0.5 = {n ** 0.5:.1f})")
    print(f"  blocks (cut decomposition) sizes = {blsizes}")
    print(f"  inversions = {inv} ({inv / (n * (n - 1) / 2):.2f} of max), monotone 3-APs = {m3}")
    print(f"  positions of 1..8: {[pos.get(v) for v in range(1, min(9, n + 1))]}")
    return {"N": n, "lis": lis, "lds": lds, "blsizes": blsizes, "m3": m3,
            "maxdisp": max(disp), "mindisp": min(disp)}


def load(fn):
    out = []
    for line in open(fn):
        line = line.strip()
        if not line:
            continue
        parts = dict(p.split("=", 1) for p in line.split())
        out.append((int(parts["N"]), [int(x) for x in parts["perm"].split(",")],
                    parts.get("how", "?")))
    return out


if __name__ == "__main__":
    fn = sys.argv[1]
    top = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    entries = load(fn)
    entries.sort(key=lambda e: e[0])
    for N, perm, how in entries[-top:]:
        analyze(perm, label=f"{os.path.basename(fn)} how={how}")
