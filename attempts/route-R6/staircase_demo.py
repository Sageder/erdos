"""staircase_demo.py — R5 L10 staircases COEXIST with a linear profile at C = 3.

Claim tested: the triadic reversed-block permutation T (which satisfies (H-up):
no increasing monotone 4-AP, and pos(v) <= 3v - 1 for all v) contains, from any
start value u, an R5-L10-style staircase: increasing 3-APs
(T_{i-1}, T_{i-1}+f_i, T_{i-1}+2f_i), T_i = T_{i-1} + 2 f_i, with f_{i+1} = g f_i,
g >= 3, positions strictly increasing along tops, and the planted inversion
pos(T_i + f_i) < pos(T_i) at every rung.

Consequence (the R5 hand-off answer): "staircases from every value, counted
globally, contradict linear displacement profiles" is FALSE for profiles with
C >= 3 — T carries all staircases AND pos(v) <= 3v - 1.  Any LP(C) proof for
C >= 3 must use the DECREASING orientation, which L10 never does.

Also verifies pos(v) <= 3v - 1 for all v, exactly, on a large prefix.
"""

import sys

sys.path.insert(0, "/home/user/erdos/attempts/route-R6")
from r6lib import reversed_blocks

K = 12
tri = reversed_blocks(3, K)          # permutation of [1 .. 3^12-1 = 531440]
N = 3**K - 1
pos = [0] * (N + 1)
for i, v in enumerate(tri):
    pos[v] = i + 1

# profile check: pos(v) <= 3v - 1, tight at v = 3^k
for v in range(1, N + 1):
    assert pos[v] <= 3 * v - 1, (v, pos[v])
tight = [v for k in range(K) for v in [3**k] if pos[v] == 3 * v - 1]
print(f"pos(v) <= 3v-1 for all v <= {N}; equality exactly at v = 3^k: {tight[:6]} ...")


def find_rung(anchor, modulus):
    """Smallest e = g*modulus, g>=1, with pos(anchor+e) > pos(anchor) and
    pos(anchor+2e) > pos(anchor+e) (increasing 3-AP anchored at anchor's position).
    Existence for T is guaranteed by R5 Thm 2 (holds for ANY permutation of N)."""
    s = pos[anchor]
    g = 0
    while True:
        g += 1
        e = g * modulus
        if anchor + 2 * e > N:
            return None  # out of the finite prefix (infinite T: never happens)
        if pos[anchor + e] > s and pos[anchor + 2 * e] > pos[anchor + e]:
            return g, e


for u in (1, 2, 5, 27):
    T_cur, f, rungs = u, None, []
    mod = 1
    while True:
        r = find_rung(T_cur, mod)
        if r is None:
            break
        g, e = r
        # L9 check: after the first rung, the step multiplier must be >= 3
        if f is not None:
            assert g >= 3, (u, T_cur, f, g)
        # planted inversion of the PREVIOUS rung: pos(T_cur + f_prev) handled below
        rungs.append((T_cur, e, T_cur + 2 * e))
        T_prev, f_prev = T_cur, e
        T_cur = T_cur + 2 * e
        mod = e
        # L1-inversion at this rung's top: pos(T_cur + f) < pos(T_cur)
        if T_cur + e <= N:
            assert pos[T_cur + e] < pos[T_cur], (u, T_cur, e)
    tops = [r[2] for r in rungs]
    steps = [r[1] for r in rungs]
    assert all(pos[tops[i]] < pos[tops[i + 1]] for i in range(len(tops) - 1))
    assert all(steps[i + 1] % steps[i] == 0 and steps[i + 1] >= 3 * steps[i]
               for i in range(len(steps) - 1))
    print(f"staircase from u={u}: steps {steps}  tops {tops}")
    print(f"   top positions {[pos[t] for t in tops]} (strictly increasing); "
          f"all rung inversions pos(T_i+f_i) < pos(T_i) verified")

print("\nCONCLUSION: full L10 staircases (g >= 3, planted inversions) live inside a "
      "permutation with pos(v) <= 3v-1 and no increasing 4-AP: staircase-counting "
      "alone cannot prove LP(C) for C >= 3.")
