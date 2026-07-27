"""dfs_compare.py — matched one-sided vs two-sided extension search under surjectivity pressure.

Claim tested (exploratory, route R8): quantify how far monotone-k-AP-free assignments extend
  (a) one-sided: fill positions 1,2,3,... with distinct values from N, |value - pos| <= C,
      prune when a value becomes dead (all its allowed positions filled)     [order type omega]
  (b) two-sided: fill positions 0,+1,-1,+2,-2,... with distinct values from Z, |value-pos| <= C,
      prune dead values on both sides                                        [order type zeta]

The displacement bound |b(p)-p| <= C makes skipping any value fatal (dead-value pruning), so an
infinite completed search path would be a genuine bijection (one-sided: of N; two-sided: of Z)
with no monotone k-AP and displacement <= C.  Exhaustive extinction at depth D for bound C is a
theorem: "no k-AP-free bijection with displacement <= C exists" (one/two-sided resp.).
Exact integer arithmetic throughout.

Dead-value pruning correctness: filled positions always form a contiguous interval containing
the start, so value v is dead iff unused and [v-C, v+C] subset filled.  We check the newly
endangered value(s) each time the frontier advances; by induction this catches every death.
"""

import sys
from time import time

sys.setrecursionlimit(100000)


def new_kaps_through(posmap, k, v, p):
    """Would placing value v at position p create a monotone k-AP?  posmap: value -> position of
    already-placed values.  Enumerates all APs containing v (v in role r, one other placed value
    u in role s fixes d); checks all terms placed and positions strictly monotone.  Exact."""
    for u, pu in posmap.items():
        diff = v - u
        for r in range(k):          # role of v in x, x+d, ..., x+(k-1)d
            for s in range(k):      # role of u
                if r == s:
                    continue
                den = r - s
                if diff * den <= 0:
                    continue
                if diff % den != 0:
                    continue
                d = diff // den     # d >= 1
                x = v - r * d
                terms = [x + j * d for j in range(k)]
                ps = []
                ok = True
                for t in terms:
                    if t == v:
                        ps.append(p)
                    elif t in posmap:
                        ps.append(posmap[t])
                    else:
                        ok = False
                        break
                if not ok:
                    continue
                if all(ps[j] < ps[j + 1] for j in range(k - 1)) or \
                   all(ps[j] > ps[j + 1] for j in range(k - 1)):
                    return True
    return False


def dfs_one_sided(k, C, max_depth, node_budget):
    """Fill positions 1,2,...; values in N with |v - i| <= C.  Returns (best_depth, nodes,
    complete): complete=True <=> exhaustive extinction below max_depth within budget."""
    best = [0]
    nodes = [0]
    used = set()
    posmap = {}

    def rec(i):
        if i - 1 > best[0]:
            best[0] = i - 1
        if i - 1 >= max_depth or nodes[0] >= node_budget:
            return True
        w = i - C - 1              # newly dead value candidate at this depth
        if w >= 1 and w not in used:
            return False
        for v in range(max(1, i - C), i + C + 1):
            if v in used:
                continue
            nodes[0] += 1
            if new_kaps_through(posmap, k, v, i):
                continue
            used.add(v)
            posmap[v] = i
            hit = rec(i + 1)
            del posmap[v]
            used.discard(v)
            if hit:
                return True
        return False

    hit = rec(1)
    return best[0], nodes[0], not hit


def dfs_two_sided(k, C, max_depth, node_budget):
    """Fill positions 0, 1, -1, 2, -2, ...; values in Z with |v - p| <= C."""
    best = [0]
    nodes = [0]
    used = set()
    posmap = {}

    def pos_at(step):
        if step == 0:
            return 0
        q, r = divmod(step + 1, 2)
        return q if r == 0 else -q

    def rec(step):
        if step > best[0]:
            best[0] = step
        if step >= max_depth or nodes[0] >= node_budget:
            return True
        p = pos_at(step)
        # After placing at p the filled position interval is [-L, R] (zigzag order):
        if p > 0:
            L, R = p - 1, p      # after +q: [-(q-1), q]
        elif p < 0:
            L, R = -p, -p        # after -q: [-q, q]
        else:
            L, R = 0, 0
        # dead-value candidates when the frontier advances (see module docstring):
        cands = {R - C, -L + C}
        for v in range(p - C, p + C + 1):
            if v in used:
                continue
            nodes[0] += 1
            if new_kaps_through(posmap, k, v, p):
                continue
            used.add(v)
            posmap[v] = p
            dead = any(w not in used and (w - C) >= -L and (w + C) <= R
                       for w in cands)
            hit = rec(step + 1) if not dead else False
            del posmap[v]
            used.discard(v)
            if hit:
                return True
        return False

    hit = rec(0)
    return best[0], nodes[0], not hit


if __name__ == "__main__":
    ks = [3, 4]
    for k in ks:
        print(f"=== k = {k} ===")
        print("one-sided (N):")
        for C in range(1, 8):
            t0 = time()
            best, nodes, complete = dfs_one_sided(k, C, max_depth=3000,
                                                  node_budget=4_000_000)
            tag = "EXTINCT(exhaustive)" if complete else "budget/depth hit"
            print(f"  C={C}: depth {best:5d}  nodes {nodes:8d}  {tag}  [{time()-t0:.1f}s]",
                  flush=True)
        print("two-sided (Z):")
        for C in range(1, 8):
            t0 = time()
            best, nodes, complete = dfs_two_sided(k, C, max_depth=3000,
                                                  node_budget=4_000_000)
            tag = "EXTINCT(exhaustive)" if complete else "budget/depth hit"
            print(f"  C={C}: steps {best:5d}  nodes {nodes:8d}  {tag}  [{time()-t0:.1f}s]",
                  flush=True)
