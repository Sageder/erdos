"""sat_order.py — exact SAT decision of finite avoidance questions via ORDER encoding.

Variables: x[(u,w)] for values u < w <= N, meaning pos(u) < pos(w) ("u before w").
Transitivity clauses over all value triples make any model a linear order.
AP constraints are 3-literal clauses:
  - no increasing 4-AP (x,x+e,..):  (~x1 | ~x2 | ~x3) where xi = x[(x+(i-1)e, x+ie)]
  - no decreasing 4-AP:             ( x1 |  x2 |  x3)
  - no decreasing 3-AP:             ( y1 |  y2 ) with yi = x[(x+(i-1)e, x+ie)]
Optional pinning pos(v) <= C: cardinality constraint sum_{w != v} [w before v] <= C-1.

Modes:
  mode="both4"  : monotone-4-AP-free (the 196 object)
  mode="asym"   : no dec-3AP and no inc-4AP (ASYM.md target)
  mode="dec3inc4pin" etc. composed from flags.

Validated: models are decoded to permutations and re-checked with the trusted checker.
UNSAT results at (N, constraints) are theorems modulo solver correctness; for any
UNSAT that we USE, re-verify with a second solver.
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from pysat.solvers import Cadical195, Glucose42
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def build(N, inc4=True, dec4=True, dec3=False, pinning=None, pool=None):
    """Return (clauses, pool, var). pinning: dict value -> max position C."""
    pool = pool or IDPool()
    def var(u, w):
        assert u < w
        return pool.id(('x', u, w))
    cl = []
    # transitivity over value triples u < v < w
    for u in range(1, N + 1):
        for v in range(u + 1, N + 1):
            for w in range(v + 1, N + 1):
                a, b, c = var(u, v), var(v, w), var(u, w)
                cl.append([-a, -b, c])
                cl.append([a, b, -c])
    for e in range(1, (N - 1) // 2 + 1):
        for x in range(1, N - 2 * e + 1):
            y1, y2 = var(x, x + e), var(x + e, x + 2 * e)
            if dec3:
                cl.append([y1, y2])
            if x + 3 * e <= N:
                y3 = var(x + 2 * e, x + 3 * e)
                if inc4:
                    cl.append([-y1, -y2, -y3])
                if dec4:
                    cl.append([y1, y2, y3])
    if pinning:
        for v, C in pinning.items():
            # pos(v) = 1 + #{w != v : w before v} <= C
            lits = []
            for w in range(1, N + 1):
                if w == v:
                    continue
                lits.append(var(min(v, w), max(v, w)) * (1 if w < v else -1))
                # w < v: x[(w,v)] true means w before v -> literal +var
                # w > v: w before v means NOT x[(v,w)] -> literal -var
            enc = CardEnc.atmost(lits=lits, bound=C - 1, vpool=pool, encoding=EncType.seqcounter)
            cl.extend(enc.clauses)
    return cl, pool, var


def decode(model, N, var):
    mset = set(model)
    import functools
    vals = list(range(1, N + 1))
    def cmp(u, w):
        if u == w:
            return 0
        if u < w:
            return -1 if var(u, w) in mset else 1
        return 1 if var(w, u) in mset else -1
    vals.sort(key=functools.cmp_to_key(cmp))
    return vals   # permutation: value at position i


def solve(N, solver="cadical", **kw):
    cl, pool, var = build(N, **kw)
    S = Cadical195(bootstrap_with=cl) if solver == "cadical" else Glucose42(bootstrap_with=cl)
    sat = S.solve()
    if not sat:
        S.delete()
        return None, None
    perm = decode(S.get_model(), N, var)
    S.delete()
    return True, perm


def check_perm(perm, inc4=True, dec4=True, dec3=False, pinning=None):
    n = len(perm)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    for e in range(1, (n - 1) // 2 + 1):
        for x in range(1, n - 2 * e + 1):
            if dec3 and pos[x] > pos[x + e] > pos[x + 2 * e]:
                return False
            if x + 3 * e <= n:
                if inc4 and pos[x] < pos[x + e] < pos[x + 2 * e] < pos[x + 3 * e]:
                    return False
                if dec4 and pos[x] > pos[x + e] > pos[x + 2 * e] > pos[x + 3 * e]:
                    return False
    if pinning:
        for v, C in pinning.items():
            if pos[v] > C:
                return False
    return True


if __name__ == "__main__":
    import time
    which = sys.argv[1] if len(sys.argv) > 1 else "asym"
    if which == "asym":
        for N in (25, 30, 35, 40, 45, 50, 60, 70, 80, 100):
            t0 = time.time()
            sat, perm = solve(N, inc4=True, dec4=False, dec3=True)
            dt = time.time() - t0
            if sat:
                assert check_perm(perm, inc4=True, dec4=False, dec3=True)
                assert not has_monotone_kap_pos(perm, 4)  # implied full 4-AP-freeness
                print(f"asym N={N}: SAT ({dt:.1f}s)  perm head={perm[:16]}", flush=True)
            else:
                print(f"asym N={N}: UNSAT ({dt:.1f}s)  <-- EXTINCTION THEOREM (modulo solver)", flush=True)
                break
    elif which == "pin22":
        for N in (20, 30, 40, 60, 80, 100):
            t0 = time.time()
            sat, perm = solve(N, inc4=True, dec4=True, pinning={1: 1, 2: 2})
            dt = time.time() - t0
            if sat:
                assert check_perm(perm, pinning={1: 1, 2: 2})
                assert not has_monotone_kap_pos(perm, 4)
                print(f"pin(1->1,2->2) N={N}: SAT ({dt:.1f}s) head={perm[:12]}", flush=True)
            else:
                print(f"pin(1->1,2->2) N={N}: UNSAT ({dt:.1f}s) <-- FIN-type extinction at C=(1,2)", flush=True)
                break
    elif which == "plain":
        for N in (30, 50, 80, 120):
            t0 = time.time()
            sat, perm = solve(N, inc4=True, dec4=True)
            dt = time.time() - t0
            assert sat and not has_monotone_kap_pos(perm, 4)
            print(f"plain 4-AP-free N={N}: SAT ({dt:.1f}s)", flush=True)
