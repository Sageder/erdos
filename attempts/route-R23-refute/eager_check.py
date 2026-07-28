"""eager_check.py -- independent re-verification of the class-order UNSATs.

Second ENCODING (eager O(N^3) transitivity, no CEGAR) and second/third SOLVER, for the
within-class-order feasibility question of classorder.py.  Project standard: every UNSAT
relied on must be reproduced by a second solver AND a second encoding.
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R23-refute')
from pysat.solvers import Cadical195, Glucose42
from pysat.formula import IDPool
from classorder import classes_of
from halfblock import W3
from verify import W1


def eager(c, N):
    pool = IDPool()
    def var(u, w):
        return pool.id(('x', u, w))
    def lit(u, w):
        return var(u, w) if u < w else -var(w, u)
    cl = []
    for u in range(1, N + 1):
        for w in range(u + 1, N + 1):
            if c[u] < c[w]:
                cl.append([lit(u, w)])
            elif c[u] > c[w]:
                cl.append([lit(w, u)])
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            a = [lit(x + k * e, x + (k + 1) * e) for k in range(3)]
            cl.append([-a[0], -a[1], -a[2]])
            cl.append([a[0], a[1], a[2]])
    for u in range(1, N + 1):
        for w in range(u + 1, N + 1):
            for z in range(w + 1, N + 1):
                cl.append([-lit(u, w), -lit(w, z), lit(u, z)])
                cl.append([lit(u, w), lit(w, z), -lit(u, z)])
    return cl


if __name__ == "__main__":
    cases = [("W3 b=3 h=2  N=60", 3, 60, lambda N, b: W3(N, b, lambda M: 2)),
             ("W3 b=3 h=M+2 N=60", 3, 60, lambda N, b: W3(N, b, lambda M: M + 2)),
             ("W3 b=5 h=2  N=90", 5, 90, lambda N, b: W3(N, b, lambda M: 2)),
             ("W1 b=4 h=1  N=90", 4, 90, lambda N, b: W1(N, b, lambda M: 1)[0]),
             ("W3 b=4 h=2  N=130", 4, 130, lambda N, b: W3(N, b, lambda M: 2))]
    for tag, b, N, mk in cases:
        c = classes_of(mk(N, b), N, b)
        cl = eager(c, N)
        t0 = time.time()
        r1 = Cadical195(bootstrap_with=cl).solve()
        r2 = Glucose42(bootstrap_with=cl).solve()
        print(f"{tag}: eager encoding ({len(cl)} clauses) cadical={'SAT' if r1 else 'UNSAT'} "
              f"glucose={'SAT' if r2 else 'UNSAT'}  ({time.time()-t0:.0f}s)", flush=True)
