"""verify_unsat.py — SECOND ENGINE for the layered-architecture UNSAT results.

jointsat.py decides layered feasibility with CP-SAT (integer positions + AllDifferent).
Here the same question is re-decided with a completely different encoding and solver:
an ORDER-ENCODED CNF (one boolean per intra-block pair + transitivity triangles) fed to
CaDiCaL (and optionally Glucose).  Agreement of the two engines is the standard
cross-check demanded by the lab rules.

The constraint list comes from blocks.constraints(), which was cross-validated against
apcheck.has_monotone_kap_pos on 600 random (cuts, block-orders) instances.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from pysat.solvers import Cadical195, Glucose42          # noqa: E402
from pysat.formula import IDPool                          # noqa: E402
from apcheck import has_monotone_kap_pos                  # noqa: E402
from blocks import constraints, blk_of, check_orders, assemble  # noqa: E402


def cnf(cuts, N):
    C = constraints(cuts, N)
    assert not C['fatal'], "cut sequence has an unavoidable 1+1+1+1 pattern"
    B = blk_of(cuts, N)
    blocks = {}
    for v in range(1, N + 1):
        blocks.setdefault(B[v], []).append(v)
    pool = IDPool()

    def x(u, w):                      # u < w ; true iff u is positioned before w
        assert u < w and B[u] == B[w]
        return pool.id(('x', u, w))

    def lt(u, w):                     # literal "u before w" for u != w in same block
        return x(u, w) if u < w else -x(w, u)

    cl = []
    for j, vals in blocks.items():    # transitivity inside each block
        n = len(vals)
        for ai in range(n):
            for bi in range(ai + 1, n):
                for ci in range(bi + 1, n):
                    u, v_, w = vals[ai], vals[bi], vals[ci]
                    a, b, c = x(u, v_), x(v_, w), x(u, w)
                    cl.append([-a, -b, c])
                    cl.append([a, b, -c])
    for (j, u, w) in C['inv']:
        cl.append([-lt(u, w)])
    for (j, a, e) in C['noinc3']:
        cl.append([-lt(a, a + e), -lt(a + e, a + 2 * e)])
    for (j, a, e) in C['no4']:
        l1, l2, l3 = lt(a, a + e), lt(a + e, a + 2 * e), lt(a + 2 * e, a + 3 * e)
        cl.append([-l1, -l2, -l3])
        cl.append([l1, l2, l3])
    for (lo, hi) in C['pair22']:
        cl.append([-lt(lo[1], lo[2]), -lt(hi[1], hi[2])])
    return cl, pool, blocks, lt


def run(cuts, N, solver="cadical"):
    cl, pool, blocks, lt = cnf(cuts, N)
    S = Cadical195(bootstrap_with=cl) if solver == "cadical" else Glucose42(bootstrap_with=cl)
    t0 = time.time()
    sat = S.solve()
    dt = time.time() - t0
    out = dict(status="SAT" if sat else "UNSAT", secs=dt, nclauses=len(cl))
    if sat:
        model = set(S.get_model())
        import functools
        orders = {}
        for j, vals in blocks.items():
            def cmp(u, w):
                if u == w:
                    return 0
                lit = lt(u, w)
                before = (lit in model) if lit > 0 else (-lit not in model)
                return -1 if before else 1
            orders[j] = sorted(vals, key=functools.cmp_to_key(cmp))
        perm = assemble(cuts, N, orders)
        assert not check_orders(cuts, N, orders)
        assert not has_monotone_kap_pos(perm, 4)
        out['perm'] = perm
    S.delete()
    return out


if __name__ == "__main__":
    spec, N = sys.argv[1], int(sys.argv[2])
    solver = sys.argv[3] if len(sys.argv) > 3 else "cadical"
    if spec.startswith("geom:"):
        r = int(spec.split(":")[1])
        cuts = [1]
        while cuts[-1] <= N:
            cuts.append(cuts[-1] * r)
    else:
        cuts = [int(t) for t in spec.split(",")]
        if cuts[-1] <= N:
            cuts.append(N + 1)
    res = run(cuts, N, solver)
    print(f"[{solver}] cuts={[c for c in cuts if c <= N]} N={N}: {res['status']} "
          f"({res['secs']:.1f}s, {res['nclauses']} clauses)", flush=True)
