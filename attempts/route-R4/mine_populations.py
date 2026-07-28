"""mine_populations.py — structural mining of complete last-survivor populations
(deliverable 3).  No plotting libs available; produces text tables + ASCII scatter
into results/mining.txt.

Analyses per population file (survivors/*.txt with AVOIDER lines):
  - rigidity: values with forced positions across ALL survivors; the common skeleton;
  - displacement profile pi(v)/v: which values sit on the constraint wall;
  - LIS/LDS distribution;
  - block (cut) decomposition of a canonical (lexicographically first) survivor;
  - ASCII picture of the canonical survivor.
"""

import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mine import lis_len, blocks

HERE = os.path.dirname(os.path.abspath(__file__))


def load(fn):
    perms = []
    for line in open(fn):
        if line.startswith("AVOIDER"):
            perms.append(tuple(int(x) for x in line.split()[1:]))
    return sorted(set(perms))


def ascii_plot(perm, width=64):
    n = len(perm)
    print("    value-vs-position picture (row = position, col = value):")
    for i, v in enumerate(perm, 1):
        col = int((v - 0.5) / n * width)
        print(f"    {i:3d} |" + " " * col + "*")


def analyze(fn, out):
    perms = load(fn)
    if not perms:
        return
    n = len(perms[0])
    w = out.write
    w(f"\n=== {os.path.basename(fn)}: {len(perms)} survivors, N={n}\n")
    posmaps = [{v: i + 1 for i, v in enumerate(p)} for p in perms]
    common_vals = set(posmaps[0])
    for pm in posmaps[1:]:
        common_vals &= set(pm)
    forced = {}
    for v in sorted(common_vals):
        c = Counter(pm[v] for pm in posmaps)
        if len(c) == 1:
            forced[v] = next(iter(c))
    w(f"forced positions ({len(forced)}/{n} values rigid): "
      + " ".join(f"pi({v})={p}" for v, p in sorted(forced.items())) + "\n")
    # skeleton in position order
    inv = {p: v for v, p in forced.items()}
    skel = "".join((f"{inv[p]:>4}" if p in inv else "   .") for p in range(1, n + 1))
    w(f"skeleton (position order, . = free): {skel}\n")
    liss = [lis_len(p) for p in perms]
    ldss = [lis_len([-x for x in p]) for p in perms]
    w(f"LIS range {min(liss)}..{max(liss)}, LDS range {min(ldss)}..{max(ldss)}, "
      f"sqrt(N)={n ** 0.5:.1f}\n")
    p0 = perms[0]
    w(f"canonical survivor: {','.join(map(str, p0))}\n")
    w(f"cut-block sizes of canonical: {[len(b) for b in blocks(list(p0))]}\n")
    pm0 = {v: i + 1 for i, v in enumerate(p0)}
    vals0 = sorted(pm0)
    wall_hi = [v for v in vals0 if pm0[v] >= 2 * v - 1]
    wall_lo = [v for v in vals0 if 2 * pm0[v] <= v + 1]
    w(f"canonical: values with pi(v)>=2v-1 (late wall): {wall_hi}\n")
    w(f"canonical: values with pi(v)<=(v+1)/2 (early wall): {wall_lo}\n")
    ratios = sorted((pm0[v] / v, v) for v in vals0)
    w(f"canonical: min pi/v = {ratios[0][0]:.3f} at v={ratios[0][1]}, "
      f"max pi/v = {ratios[-1][0]:.3f} at v={ratios[-1][1]}\n")


if __name__ == "__main__":
    files = sys.argv[1:]
    outfn = os.path.join(HERE, "results", "mining.txt")
    with open(outfn, "w") as out:
        for fn in files:
            analyze(fn, out)
    print(open(outfn).read())
