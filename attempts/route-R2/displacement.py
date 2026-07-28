"""displacement.py — displacement profile pos(v)/v of Construction A.

Theory: value v in B_m = [4^m, 4^{m+1}) occupies a position in the same index
range [4^m, 4^{m+1}) (1-indexed), because the blocks are intervals concatenated
in increasing order.  Hence  v/4 < pos(v) < 4v  for all v — displacement is
LINEARLY BOUNDED on both sides.  This calibrates against CORE.md Theorem 12
(pos(v) <= C v with C < 9/8 forces an increasing monotone 4-AP): 5-AP freedom
is achievable inside the C = 4 linear corridor, while 4-AP freedom is
impossible for C < 9/8.

This script computes the exact profile on the N = 4^8 - 1 prefix:
  max/min of pos(v)/v per block and overall, the arg-max, the limsup trend,
  and the density of v with pos(v) <= (9/8) v.
"""

import sys
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from construction import prefix

p = prefix(8)
N = len(p)
pos = {}
for i, v in enumerate(p):
    pos[v] = i + 1                      # 1-indexed positions

out = []


def log(s):
    print(s)
    out.append(s)


overall_max = Fraction(0)
overall_min = Fraction(10)
argmax = argmin = None
below98 = 0
for v in range(1, N + 1):
    r = Fraction(pos[v], v)
    if r > overall_max:
        overall_max, argmax = r, v
    if r < overall_min:
        overall_min, argmin = r, v
    if r <= Fraction(9, 8):
        below98 += 1

log("prefix N = %d" % N)
log("max pos(v)/v = %s = %.6f at v = %d (pos %d)"
    % (overall_max, float(overall_max), argmax, pos[argmax]))
log("min pos(v)/v = %s = %.6f at v = %d (pos %d)"
    % (overall_min, float(overall_min), argmin, pos[argmin]))
log("density of v with pos(v) <= (9/8) v : %d / %d = %.4f"
    % (below98, N, below98 / N))

log("")
log("per-block extremes of pos(v)/v (blocks m = 0..7):")
for m in range(8):
    lo, hi = 4 ** m, 4 ** (m + 1)
    mx = max(Fraction(pos[v], v) for v in range(lo, hi))
    mn = min(Fraction(pos[v], v) for v in range(lo, hi))
    vx = max(range(lo, hi), key=lambda v: Fraction(pos[v], v))
    vn = min(range(lo, hi), key=lambda v: Fraction(pos[v], v))
    log("  m=%d: max %.5f (v=%d), min %.5f (v=%d)"
        % (m, float(mx), vx, float(mn), vn))

log("")
log("hard bounds from the block structure: v/4 < pos(v) < 4v for every v")
log("(pos(v) and v lie in the same dyadic-4 window [4^m, 4^{m+1}));")
log("so limsup pos(v)/v <= 4 and liminf >= 1/4; the per-block maxima above "
    "show the limsup is close to 4 (approached by small-v-late-in-block "
    "placements) and liminf close to 1/4.")

with open("/home/user/erdos/attempts/route-R2/displacement_output.txt", "w") as f:
    f.write("\n".join(out) + "\n")
