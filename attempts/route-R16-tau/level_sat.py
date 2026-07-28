"""level_sat.py — LEVEL-FILTERED avoidance: how many base-3 levels can an omega-order
protect at once?

Motivation (REPORT.md sec. 6, "level decomposition"): every monotone 4-AP has a unique
critical level v = v3(d).  tau protects ALL levels simultaneously, by a rule that is
purely local to level v; its price is that predecessor sets become infinite.  A repair
must give up tau at every level (Prop R2), so the honest question is: how expensive is
protecting levels, one at a time, for an order of type omega?

Encoding: order variables x[(u,w)] = "u before w" for u<w<=N, full transitivity, plus
  - increasing clause  (~x1|~x2|~x3)  and decreasing clause (x1|x2|x3)
    ONLY for APs (x, x+d, x+2d, x+3d) with v3(d) in the allowed level set L;
  - optional displacement pinning pos(v) <= floor(C*v).
Every SAT model is decoded and RE-VERIFIED with an independent scan (no monotone 4-AP
at the allowed levels, and the profile bound).  UNSAT is re-run with a second solver.
"""

import sys
sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from pysat.solvers import Cadical195, Glucose42
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from taulib import v3


def build(N, levels, C=None, pool=None):
    pool = pool or IDPool()

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
    naps = 0
    for d in range(1, (N - 1) // 3 + 1):
        if levels is not None and v3(d) not in levels:
            continue
        for x in range(1, N - 3 * d + 1):
            y1, y2, y3 = var(x, x + d), var(x + d, x + 2 * d), var(x + 2 * d, x + 3 * d)
            cl.append([-y1, -y2, -y3])
            cl.append([y1, y2, y3])
            naps += 1
    if C is not None:
        for v in range(1, N + 1):
            cap = int(C * v)
            if cap >= N:
                continue
            lits = [(var(w, v) if w < v else -var(v, w)) for w in range(1, N + 1) if w != v]
            enc = CardEnc.atmost(lits=lits, bound=cap - 1, vpool=pool,
                                 encoding=EncType.seqcounter)
            cl.extend(enc.clauses)
    return cl, pool, var, naps


def decode(model, N, var):
    ms = set(l for l in model if l > 0)
    before = [[False] * (N + 2) for _ in range(N + 2)]
    for u in range(1, N + 1):
        for w in range(u + 1, N + 1):
            if var(u, w) in ms:
                before[u][w] = True
            else:
                before[w][u] = True
    order = sorted(range(1, N + 1), key=lambda v: sum(1 for w in range(1, N + 1)
                                                      if w != v and before[w][v]))
    return order


def reverify(order, N, levels, C):
    pos = {v: i + 1 for i, v in enumerate(order)}
    assert sorted(order) == list(range(1, N + 1))
    for d in range(1, (N - 1) // 3 + 1):
        if levels is not None and v3(d) not in levels:
            continue
        for x in range(1, N - 3 * d + 1):
            p = [pos[x + k * d] for k in range(4)]
            assert not (p[0] < p[1] < p[2] < p[3]), ("inc", x, d)
            assert not (p[0] > p[1] > p[2] > p[3]), ("dec", x, d)
    if C is not None:
        for v in range(1, N + 1):
            assert pos[v] <= int(C * v), ("profile", v, pos[v])
    return True


def solve(N, levels, C=None, solver="cadical", timeout=None):
    cl, pool, var, naps = build(N, levels, C)
    S = Cadical195(bootstrap_with=cl) if solver == "cadical" else Glucose42(bootstrap_with=cl)
    sat = S.solve()
    order = None
    if sat:
        order = decode(S.get_model(), N, var)
        reverify(order, N, levels, C)
    S.delete()
    return sat, order, naps


def threshold(levels, C, lo=4, hi=200, label=""):
    """Smallest N with UNSAT (binary-search-free upward scan with doubling)."""
    N = lo
    last_sat = None
    while N <= hi:
        sat, order, naps = solve(N, levels, C)
        if sat:
            last_sat = N
            N += 1
        else:
            # confirm with a second solver
            sat2, _, _ = solve(N, levels, C, solver="glucose")
            assert sat2 is False, "solver disagreement!"
            print(f"  {label} C={C} levels={levels}: SAT up to N={last_sat}, "
                  f"UNSAT at N={N} (both solvers)", flush=True)
            return N
    print(f"  {label} C={C} levels={levels}: SAT through N={hi} (no extinction found)",
          flush=True)
    return None


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--C", type=float, default=1.5)
    ap.add_argument("--hi", type=int, default=120)
    ap.add_argument("--levels", type=str, default="0|01|012|0123|all")
    a = ap.parse_args()
    specs = []
    for tok in a.levels.split("|"):
        specs.append((None, "all") if tok == "all" else (set(int(c) for c in tok), tok))
    for lv, nm in specs:
        threshold(lv, a.C, hi=a.hi, label=f"levels={nm}")
