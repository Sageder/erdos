"""blocks.py — BLOCK DECOMPOSITION of monotone-4-AP-freeness for layered permutations,
read off from the forcing relation (CORE.md Thm 16).

SETUP.  Fix cuts 1 = c_0 < c_1 < c_2 < ... (c_j -> infinity).  Blocks B_j = [c_j, c_{j+1}).
A *layered* permutation of N lists B_0, then B_1, then B_2, ... ; inside B_j the values
appear in an arbitrary order pi_j.  (Order type omega is automatic.)  blk(v) = j iff v in B_j.

THEOREM R18.4 (block decomposition).  A layered permutation is monotone-4-AP-free iff for
every AP (x, x+d, x+2d, x+3d), d >= 1, the corresponding condition below holds, where the
four terms are grouped into maximal runs sharing a block (the grouping is a composition of
4 because blocks are intervals and the terms increase):

  [4]      all four in B_j        : pi_j has no increasing AND no decreasing 4-AP on them
  [3+1]    x,x+d,x+2d in B_j      : (x,x+d,x+2d) NOT positionally increasing in pi_j
  [1+3]    x+d,x+2d,x+3d in B_k   : (x+d,x+2d,x+3d) NOT positionally increasing in pi_k
  [2+2]    x,x+d in B_j; x+2d,x+3d in B_k (k>j)
                                  : NOT( x before x+d  AND  x+2d before x+3d )
  [2+1+1]  x,x+d in B_j; x+2d in B_k; x+3d in B_l (j<k<l)   : x+d before x   (INVERSION)
  [1+2+1]  x in B_j; x+d,x+2d in B_k; x+3d in B_l (j<k<l)   : x+2d before x+d (INVERSION)
  [1+1+2]  x in B_j; x+d in B_k; x+2d,x+3d in B_l (j<k<l)   : x+3d before x+2d (INVERSION)
  [1+1+1+1] four distinct blocks  : IMPOSSIBLE TO SATISFY (an increasing 4-AP always) --
                                    the cut sequence itself must exclude this pattern.

Proof.  Blocks are value-intervals listed in increasing order, so for values u < w:
blk(u) < blk(w) => pos(u) < pos(w), and blk(u) = blk(w) => order decided by pi.
DECREASING orientation: positions increase while values decrease; values decreasing forces
blk weakly decreasing, positions increasing forces blk weakly increasing, hence all four
terms share one block -- covered by [4].
INCREASING orientation: pos(x)<pos(x+d)<pos(x+2d)<pos(x+3d) holds iff each same-block run
is positionally increasing in its pi (cross-block comparisons are automatic).  Negating
this for each composition gives exactly the displayed lines; for the composition 1+1+1+1
there is no same-block run at all, so the increasing 4-AP is unconditional.  QED

SCALE CONFINEMENT (ratio >= 3 cuts, i.e. c_{j+1} >= 3 c_j for all j):
  * [1+1+1+1] impossible: x+d in B_k, x+3d in B_l with l >= k+2 gives
    3 c_{k+1} <= c_{k+2} <= x+3d < 3(x+d) < 3 c_{k+1}, absurd.
  * [2+1+1] impossible already for ratio >= 2: x,x+d in B_j gives d < c_{j+1}-c_j, and
    x+3d >= c_{j+2} >= r c_{j+1} while x+3d < 3c_{j+1} - 2c_j = (3r-2)c_j; r^2 <= 3r-2
    forces r < 2.
  * [2+2] and [1+1+2] only ever involve ADJACENT blocks (k = j+1, l = k+1), same algebra.
So for ratio >= 3 the constraint graph is a CHAIN: everything is intra-block except the
disjunctive [2+2] links between consecutive blocks.

FORCING READING (why this is the Thm 16 view).  In a layered permutation every forcing
edge u --d--> u+d stays inside one block (blk(u+d) >= blk(u) because u+d > u, and
pos(u+d) < pos(u) forces blk(u+d) <= blk(u)).  [1+1+2] is exactly "u = x+2d is open at
scale d by a cross-block increasing 3-AP, so its forced target x+3d must precede it";
[1+2+1] is exactly "x+d must not be open at scale d, because its forced target x+3d
lives in a higher block and therefore cannot precede it".
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from apcheck import has_monotone_kap_pos, has_monotone_kap_general  # noqa: E402


# --------------------------------------------------------------------- constraints

def blk_of(cuts, N):
    """blk[v] for v in 1..N-1 given cuts = [1=c0, c1, c2, ...] (c_last > N)."""
    b = [0] * (N + 1)
    j = 0
    for v in range(1, N + 1):
        while j + 1 < len(cuts) and v >= cuts[j + 1]:
            j += 1
        b[v] = j
    return b


def constraints(cuts, N):
    """Enumerate every AP (x,x+d,x+2d,x+3d) with x+3d <= N and classify it.

    Returns dict with keys:
      'inv'   : set of (block, u, w) pairs u<w that MUST be inverted (w before u)
      'noinc3': set of (block, a, e)   -- (a,a+e,a+2e) inside that block must NOT be
                                          positionally increasing
      'no4'   : set of (block, a, e)   -- all four inside; forbid both orientations
      'pair22': list of ((j,x,x+d), (k,x+2d,x+3d)) disjunctive [2+2] constraints
      'fatal' : list of APs realising [1+1+1+1] (unsatisfiable by any pi)
    """
    B = blk_of(cuts, N)
    inv, noinc3, no4, pair22, fatal = set(), set(), set(), [], []
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            t = (x, x + d, x + 2 * d, x + 3 * d)
            g = [B[y] for y in t]
            # maximal runs sharing a block
            runs = []
            for i, y in enumerate(t):
                if runs and g[i] == runs[-1][0]:
                    runs[-1][1].append(y)
                else:
                    runs.append((g[i], [y]))
            shape = tuple(len(r[1]) for r in runs)
            if shape == (4,):
                no4.add((g[0], x, d))
            elif shape == (3, 1):
                noinc3.add((g[0], x, d))
            elif shape == (1, 3):
                noinc3.add((g[1], x + d, d))
            elif shape == (2, 2):
                pair22.append(((g[0], x, x + d), (g[2], x + 2 * d, x + 3 * d)))
            elif shape == (2, 1, 1):
                inv.add((g[0], x, x + d))
            elif shape == (1, 2, 1):
                inv.add((g[1], x + d, x + 2 * d))
            elif shape == (1, 1, 2):
                inv.add((g[2], x + 2 * d, x + 3 * d))
            elif shape == (1, 1, 1, 1):
                fatal.append(t)
            else:
                raise AssertionError(shape)
    return dict(inv=inv, noinc3=noinc3, no4=no4, pair22=pair22, fatal=fatal)


def check_orders(cuts, N, orders):
    """orders[j] = list of the values of B_j in position order.  Return list of violated
    constraints (empty == the assembled layered permutation is 4-AP-free)."""
    C = constraints(cuts, N)
    pos = {}
    for j, o in orders.items():
        for i, v in enumerate(o):
            pos[v] = i
    bad = []
    if C['fatal']:
        bad.append(('fatal', C['fatal'][0]))
    for (j, u, w) in C['inv']:
        if pos[u] < pos[w]:
            bad.append(('inv', j, u, w))
    for (j, a, e) in C['noinc3']:
        if pos[a] < pos[a + e] < pos[a + 2 * e]:
            bad.append(('noinc3', j, a, e))
    for (j, a, e) in C['no4']:
        p = [pos[a + i * e] for i in range(4)]
        if p[0] < p[1] < p[2] < p[3] or p[0] > p[1] > p[2] > p[3]:
            bad.append(('no4', j, a, e))
    for (lo, hi) in C['pair22']:
        if pos[lo[1]] < pos[lo[2]] and pos[hi[1]] < pos[hi[2]]:
            bad.append(('pair22', lo, hi))
    return bad


def assemble(cuts, N, orders):
    """Concatenate block orders into a permutation of [1..N] (values in position order)."""
    out = []
    for j in sorted(orders):
        out.extend(orders[j])
    assert sorted(out) == list(range(1, N + 1)), "orders do not tile [1..N]"
    return out


# --------------------------------------------------------------- cross-validation

def _crossvalidate():
    import random
    rng = random.Random(2718)
    tested = 0
    for _ in range(600):
        # random cut sequence, random N
        cuts = [1]
        while cuts[-1] < 40:
            cuts.append(cuts[-1] + rng.randint(1, 9))
        N = rng.randint(8, cuts[-1] - 1)
        cuts = [c for c in cuts if c <= N] + [N + 1]
        B = blk_of(cuts, N)
        orders = {}
        for v in range(1, N + 1):
            orders.setdefault(B[v], []).append(v)
        for j in orders:
            rng.shuffle(orders[j])
        perm = assemble(cuts, N, orders)
        bad = check_orders(cuts, N, orders)
        truth = has_monotone_kap_pos(perm, 4)
        assert (len(bad) > 0) == truth, (cuts, N, orders, bad, truth)
        tested += 1
    print(f"BLOCK DECOMPOSITION CROSS-VALIDATED on {tested} random (cuts, block-orders) "
          f"pairs against apcheck.has_monotone_kap_pos: constraint-violation <=> 4-AP.")


if __name__ == "__main__":
    _crossvalidate()
    print()
    for r in (2, 3, 4, 5):
        cuts = [1]
        while cuts[-1] <= 400:
            cuts.append(cuts[-1] * r)
        N = cuts[-2] - 1
        C = constraints(cuts, N)
        print(f"ratio {r}: cuts={cuts[:-1]} N={N}  #inv={len(C['inv'])} "
              f"#noinc3={len(C['noinc3'])} #no4={len(C['no4'])} #2+2={len(C['pair22'])} "
              f"#fatal(1+1+1+1)={len(C['fatal'])}")
