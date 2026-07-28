"""blockalone.py — ISOLATED-BLOCK death certificates for layered architectures.

For a cut sequence, the constraints that live entirely inside one block B_j are
   [4]      no monotone 4-AP inside B_j (both orientations)
   [3+1]/[1+3]  certain 3-APs inside B_j must not be positionally increasing
   [inv]    certain pairs inside B_j must be inverted  ([1+1+2], [1+2+1], [2+1+1])
Dropping the inter-block [2+2] disjunctions can only make the problem EASIER, so

        isolated block B_j UNSAT  ==>  the whole layered architecture is infeasible.

This gives cheap, localized death certificates and tells us WHICH scale kills a cut
sequence.  Constraints for B_j are complete once N >= 2*c_{j+1} (blocks.py, scale
confinement), which is what this script uses.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from pysat.solvers import Cadical195, Glucose42          # noqa: E402
from pysat.formula import IDPool                          # noqa: E402
from apcheck import has_monotone_kap_general              # noqa: E402
from blocks import constraints, blk_of                    # noqa: E402


def block_cnf(cuts, j):
    N = min(2 * cuts[j + 1] + 2, cuts[-1] - 1)
    C = constraints(cuts, N)
    assert not C['fatal'], "unavoidable [1+1+1+1] for these cuts"
    vals = list(range(cuts[j], cuts[j + 1]))
    pool = IDPool()

    def x(u, w):
        return pool.id(('x', u, w))

    def lt(u, w):
        return x(u, w) if u < w else -x(w, u)

    cl = []
    n = len(vals)
    for ai in range(n):
        for bi in range(ai + 1, n):
            for ci in range(bi + 1, n):
                u, v_, w = vals[ai], vals[bi], vals[ci]
                a, b, c = x(u, v_), x(v_, w), x(u, w)
                cl.append([-a, -b, c])
                cl.append([a, b, -c])
    nu = nn = n4 = 0
    for (jj, u, w) in C['inv']:
        if jj == j:
            cl.append([-lt(u, w)]); nu += 1
    for (jj, a, e) in C['noinc3']:
        if jj == j:
            cl.append([-lt(a, a + e), -lt(a + e, a + 2 * e)]); nn += 1
    for (jj, a, e) in C['no4']:
        if jj == j:
            l1, l2, l3 = lt(a, a + e), lt(a + e, a + 2 * e), lt(a + 2 * e, a + 3 * e)
            cl.append([-l1, -l2, -l3]); cl.append([l1, l2, l3]); n4 += 1
    return cl, pool, vals, lt, dict(n=n, inv=nu, noinc3=nn, no4=n4)


def decide(cuts, j, solver="cadical", verify=True):
    cl, pool, vals, lt, stat = block_cnf(cuts, j)
    S = Cadical195(bootstrap_with=cl) if solver == "cadical" else Glucose42(bootstrap_with=cl)
    t0 = time.time()
    sat = S.solve()
    dt = time.time() - t0
    order = None
    if sat and verify:
        model = set(S.get_model())
        import functools

        def cmp(u, w):
            if u == w:
                return 0
            lit = lt(u, w)
            before = (lit in model) if lit > 0 else (-lit not in model)
            return -1 if before else 1
        order = sorted(vals, key=functools.cmp_to_key(cmp))
        assert not has_monotone_kap_general(order, 4), "block order has an internal 4-AP"
    S.delete()
    return ("SAT" if sat else "UNSAT"), dt, stat, order


def geom_cuts(r, depth):
    return [r ** k for k in range(depth + 1)]


if __name__ == "__main__":
    maxsize = int(sys.argv[1]) if len(sys.argv) > 1 else 320
    print("ratio  block  values          size   inv  noinc3   no4   verdict   secs")
    for r in (3, 4, 5, 6, 7, 8, 10, 12, 16):
        for j in range(1, 8):
            cuts = geom_cuts(r, j + 3)
            n = cuts[j + 1] - cuts[j]
            if n > maxsize:
                print(f"{r:5d} {j:6d}  [{cuts[j]}..{cuts[j+1]-1}]  size={n} > {maxsize}: skipped")
                break
            st, dt, stat, order = decide(cuts, j)
            print(f"{r:5d} {j:6d}  [{cuts[j]}..{cuts[j+1]-1}]  {stat['n']:5d} "
                  f"{stat['inv']:5d} {stat['noinc3']:6d} {stat['no4']:6d}   {st:6s} {dt:7.1f}",
                  flush=True)
            if st == "UNSAT":
                break
