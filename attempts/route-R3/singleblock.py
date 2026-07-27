"""singleblock.py — decoupled single-block feasibility for contiguous base-b blocks.

For a block D = [L, bL) (L = b^j), the following constraints on its internal order are
NECESSARY for any contiguous base-b block ordering of N that avoids monotone 4-APs,
and involve NO other block's order (Lemma R in REPORT.md):

  (a) no monotone 4-AP with all four terms in D (both orientations);
  (b) no INCREASING 3-AP (u, u+d, u+2d) in D with  1 <= u-d < L  (bottom-grounded)
      or  u+3d >= bL  (top-grounded);
  (c) forced inversions (pair (u, u+d) in D must be placed w-before-u):
      F1: 1 <= u-d < L and u+2d >= bL;
      F2: u-2d >= 1, u-d < L, and block_b(u-2d) < block_b(u-d).

Scaling: multiplying by b embeds the system for [L,bL) into the one for [bL,b^2 L)
(restrict the big block's order to multiples of b), so UNSAT at D_j implies UNSAT at
every D_{j'}, j' >= j — hence kills ALL contiguous base-b orderings at one stroke.

This script decides (a)+(b)+(c) per block with CP-SAT and cross-checks with pysat.
"""

import sys
import time
from itertools import combinations
from ortools.sat.python import cp_model

sys.path.insert(0, "/home/user/erdos/attempts/route-R3")


def blockb(n, b):
    m, p = 0, b
    while p <= n:
        m += 1
        p *= b
    return m


def constraints_for_block(L, b):
    """Return (aps4, grounded3, forced_pairs) for D = [L, bL)."""
    top = b * L - 1
    aps4, g3, forced = [], [], []
    for d in range(1, (top - L) // 3 + 1):
        for u in range(L, top - 3 * d + 1):
            aps4.append((u, d))
    for d in range(1, (top - L) // 2 + 1):
        for u in range(L, top - 2 * d + 1):
            if (1 <= u - d < L) or (u + 3 * d >= b * L):
                g3.append((u, d))
    for d in range(1, top - L + 1):
        for u in range(L, top - d + 1):
            if 1 <= u - d < L and u + 2 * d >= b * L:
                forced.append((u, d, "F1"))
            elif u - 2 * d >= 1 and u - d < L and blockb(u - 2 * d, b) < blockb(u - d, b):
                forced.append((u, d, "F2"))
    return aps4, g3, forced


def solve_block(L, b, time_limit=600):
    aps4, g3, forced = constraints_for_block(L, b)
    model = cp_model.CpModel()
    n = b * L - L
    pos = {v: model.NewIntVar(0, n - 1, f"p{v}") for v in range(L, b * L)}
    model.AddAllDifferent(list(pos.values()))
    inv = {}

    def gi(u, w):
        if (u, w) not in inv:
            bb = model.NewBoolVar("")
            model.Add(pos[u] > pos[w]).OnlyEnforceIf(bb)
            model.Add(pos[u] < pos[w]).OnlyEnforceIf(bb.Not())
            inv[(u, w)] = bb
        return inv[(u, w)]

    for (u, d) in aps4:
        t = [u + k * d for k in range(4)]
        prs = [(t[k], t[k + 1]) for k in range(3)]
        model.AddBoolOr([gi(a, c) for (a, c) in prs])          # not increasing
        model.AddBoolOr([gi(a, c).Not() for (a, c) in prs])    # not decreasing
    for (u, d) in g3:
        t = [u, u + d, u + 2 * d]
        prs = [(t[0], t[1]), (t[1], t[2])]
        model.AddBoolOr([gi(a, c) for (a, c) in prs])          # not increasing
    for (u, d, _) in forced:
        model.Add(pos[u + d] < pos[u])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 4
    st = solver.Solve(model)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        order = sorted(range(L, b * L), key=lambda v: solver.Value(pos[v]))
        return "SAT", order, (len(aps4), len(g3), len(forced))
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None, (len(aps4), len(g3), len(forced))
    return "UNKNOWN", None, (len(aps4), len(g3), len(forced))


def main():
    for b, js in ((3, (1, 2, 3, 4)), (4, (1, 2, 3, 4)), (5, (1, 2, 3)), (8, (1, 2))):
        for j in js:
            L = b ** j
            t0 = time.time()
            st, order, sizes = solve_block(L, b, 900)
            print(f"base {b} block D_{j}=[{L},{b*L}): {st} "
                  f"(|4AP|={sizes[0]}, |g3|={sizes[1]}, |forced|={sizes[2]}) "
                  f"({time.time()-t0:.1f}s)", flush=True)
            if st == "SAT" and b * L - L <= 60:
                print("   order:", order, flush=True)
            if st == "UNSAT":
                break


if __name__ == "__main__":
    main()
