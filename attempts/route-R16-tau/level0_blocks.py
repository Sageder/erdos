"""level0_blocks.py — the LEVEL-0 PROBLEM inside a contiguous base-3 block layout.

Level decomposition (REPORT.md sec. 6): a linear order on N is monotone-4-AP-free iff,
for every level v and context c, its restriction to {n = c mod 3^v} (rescaled) avoids
monotone 4-APs with 3 coprime to the step.  Call the latter the LEVEL-0 PROBLEM.

tau solves every instance of the level-0 problem by the residue-priority rule, at the
price of infinite predecessor sets (Prop R1).  Question: is the level-0 problem solvable
by an order of type omega AT ALL?  Here we test the cheapest omega architecture:
contiguous base-3 blocks D_j = [3^j, 3^{j+1}) listed in increasing order, with FREE
internal orders (this is R3 Lemma R's setting, restricted to APs with 3 not dividing d).
R3's Theorem B says the UNRESTRICTED version is UNSAT at D_3; we test the restricted one.

Encoding: order variables + transitivity on [1..N]; block contiguity forced by unit
clauses; AP clauses only for 3 ∤ d.  Models are re-verified independently.
"""

import sys
sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from pysat.solvers import Cadical195, Glucose42
from pysat.formula import IDPool
from taulib import v3


def blk(n):
    l = 0
    while 3 ** (l + 1) <= n:
        l += 1
    return l


def build(N, contiguous=True, dfilter=lambda d: d % 3 != 0):
    pool = IDPool()

    def var(u, w):
        assert u < w
        return pool.id(("x", u, w))
    cl = []
    for u in range(1, N + 1):
        for v in range(u + 1, N + 1):
            for w in range(v + 1, N + 1):
                a, b, c = var(u, v), var(v, w), var(u, w)
                cl.append([-a, -b, c])
                cl.append([a, b, -c])
    if contiguous:
        for u in range(1, N + 1):
            for w in range(u + 1, N + 1):
                if blk(u) < blk(w):
                    cl.append([var(u, w)])
    nap = 0
    for d in range(1, (N - 1) // 3 + 1):
        if not dfilter(d):
            continue
        for x in range(1, N - 3 * d + 1):
            y1, y2, y3 = var(x, x + d), var(x + d, x + 2 * d), var(x + 2 * d, x + 3 * d)
            cl.append([-y1, -y2, -y3])
            cl.append([y1, y2, y3])
            nap += 1
    return cl, pool, var, nap


def decode(model, N, var):
    ms = set(l for l in model if l > 0)
    cnt = {v: 0 for v in range(1, N + 1)}
    for u in range(1, N + 1):
        for w in range(u + 1, N + 1):
            if var(u, w) in ms:
                cnt[w] += 1
            else:
                cnt[u] += 1
    return sorted(range(1, N + 1), key=lambda v: cnt[v])


def reverify(order, N, contiguous, dfilter):
    pos = {v: i + 1 for i, v in enumerate(order)}
    assert sorted(order) == list(range(1, N + 1))
    if contiguous:
        for u in range(1, N + 1):
            for w in range(1, N + 1):
                if blk(u) < blk(w):
                    assert pos[u] < pos[w], ("contiguity", u, w)
    for d in range(1, (N - 1) // 3 + 1):
        if not dfilter(d):
            continue
        for x in range(1, N - 3 * d + 1):
            p = [pos[x + k * d] for k in range(4)]
            assert not (p[0] < p[1] < p[2] < p[3]) and not (p[0] > p[1] > p[2] > p[3]), (x, d)
    return True


def run(N, contiguous, dfilter, label):
    cl, pool, var, nap = build(N, contiguous, dfilter)
    S = Cadical195(bootstrap_with=cl)
    sat = S.solve()
    order = decode(S.get_model(), N, var) if sat else None
    S.delete()
    if sat:
        reverify(order, N, contiguous, dfilter)
    else:
        S2 = Glucose42(bootstrap_with=cl)
        assert S2.solve() is False, "solver disagreement"
        S2.delete()
    print(f"  {label} N={N:4d} ({nap} APs): {'SAT' if sat else 'UNSAT (2 solvers)'}",
          flush=True)
    return sat, order


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--lo", type=int, default=8)
    ap.add_argument("--hi", type=int, default=120)
    ap.add_argument("--free", action="store_true", help="drop block contiguity")
    a = ap.parse_args()
    cont = not a.free
    lab = "level0 + contig base-3 blocks" if cont else "level0 free"
    N = a.lo
    last = None
    while N <= a.hi:
        sat, order = run(N, cont, lambda d: d % 3 != 0, lab)
        if not sat:
            print(f"  => extinction at N={N} (last SAT {last})")
            break
        last = N
        if order and N in (26, 40, 80, 81, 100, 120):
            print("     model:", order)
        N += 1
    else:
        print(f"  => still SAT at N={a.hi}")
