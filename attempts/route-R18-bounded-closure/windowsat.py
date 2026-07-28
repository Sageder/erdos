"""windowsat.py — WINDOW RELAXATION: cheap death certificates for very large blocks.

For a block B_j and a window W = [w1, w2] inside it, keep only the intra-block
constraints all of whose values lie in W and forget the rest.  This is a RELAXATION, so

        window UNSAT  ==>  block UNSAT  ==>  the whole layered architecture is infeasible.

Because |W| can be kept around 150-250 the order-encoded CNF stays small even when the
block itself has thousands of values.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from pysat.solvers import Cadical195, Glucose42          # noqa: E402
from pysat.formula import IDPool                          # noqa: E402
from blocks import constraints                            # noqa: E402


def window_cnf(cuts, j, w1, w2, C=None):
    if C is None:
        N = min(2 * cuts[j + 1] + 2, cuts[-1] - 1)
        C = constraints(cuts, N)
        assert not C['fatal']
    vals = list(range(w1, w2 + 1))
    inW = set(vals)
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
                cl.append([-a, -b, c]); cl.append([a, b, -c])
    cnt = dict(inv=0, noinc3=0, no4=0)
    for (jj, u, w) in C['inv']:
        if jj == j and u in inW and w in inW:
            cl.append([-lt(u, w)]); cnt['inv'] += 1
    for (jj, a, e) in C['noinc3']:
        if jj == j and a in inW and a + 2 * e in inW:
            cl.append([-lt(a, a + e), -lt(a + e, a + 2 * e)]); cnt['noinc3'] += 1
    for (jj, a, e) in C['no4']:
        if jj == j and a in inW and a + 3 * e in inW:
            l1, l2, l3 = lt(a, a + e), lt(a + e, a + 2 * e), lt(a + 2 * e, a + 3 * e)
            cl.append([-l1, -l2, -l3]); cl.append([l1, l2, l3]); cnt['no4'] += 1
    return cl, cnt, n


def decide(cuts, j, w1, w2, solver="cadical", C=None):
    cl, cnt, n = window_cnf(cuts, j, w1, w2, C)
    S = Cadical195(bootstrap_with=cl) if solver == "cadical" else Glucose42(bootstrap_with=cl)
    t0 = time.time()
    sat = S.solve()
    dt = time.time() - t0
    S.delete()
    return ("SAT" if sat else "UNSAT"), dt, cnt, n


if __name__ == "__main__":
    spec = sys.argv[1]
    j = int(sys.argv[2])
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 180
    nwin = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    if spec.startswith("geom:"):
        parts = spec.split(":")
        r = int(parts[1]); depth = int(parts[2]) if len(parts) > 2 else j + 3
        cuts = [r ** k for k in range(depth + 1)]
    else:
        cuts = [int(t) for t in spec.split(",")]
    lo, hi = cuts[j], cuts[j + 1] - 1
    N = min(2 * cuts[j + 1] + 2, cuts[-1] - 1)
    C = constraints(cuts, N)
    assert not C['fatal']
    size = hi - lo + 1
    print(f"cuts={cuts} block {j}=[{lo}..{hi}] size={size}, windows of width {width}",
          flush=True)
    if width >= size:
        starts = [lo]
    else:
        starts = [lo + k * (size - width) // max(1, nwin - 1) for k in range(nwin)]
    for w1 in sorted(set(starts)):
        w2 = min(hi, w1 + width - 1)
        st, dt, cnt, n = decide(cuts, j, w1, w2, C=C)
        print(f"   window [{w1}..{w2}] (n={n}, inv={cnt['inv']} noinc3={cnt['noinc3']} "
              f"no4={cnt['no4']}): {st} ({dt:.1f}s)", flush=True)
        if st == "UNSAT":
            print("   => BLOCK DEAD (window relaxation UNSAT) => architecture infeasible",
                  flush=True)
            break
