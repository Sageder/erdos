"""singleblock_xcheck.py — re-prove the single-block UNSATs (base 3 D_3, base 4 D_3)
with pysat/Glucose42 and an explicit boolean-transitivity encoding (independent of
CP-SAT's integer encoding).  Also re-confirm SAT at the preceding blocks."""

import sys
import time
from itertools import combinations
from pysat.solvers import Glucose42
from pysat.formula import IDPool

sys.path.insert(0, "/home/user/erdos/attempts/route-R3")
from singleblock import constraints_for_block


def solve_block_pysat(L, b):
    aps4, g3, forced = constraints_for_block(L, b)
    pool = IDPool()

    def lt(u, w):
        return pool.id(("lt", u, w)) if u < w else -pool.id(("lt", w, u))

    cls = []
    elems = list(range(L, b * L))
    for u, v, w in combinations(elems, 3):
        a, c, e = lt(u, v), lt(v, w), lt(u, w)
        cls.append([-a, -c, e])
        cls.append([a, c, -e])
    for (u, d) in aps4:
        t = [u + k * d for k in range(4)]
        cls.append([-lt(t[k], t[k + 1]) for k in range(3)])
        cls.append([lt(t[k], t[k + 1]) for k in range(3)])
    for (u, d) in g3:
        cls.append([-lt(u, u + d), -lt(u + d, u + 2 * d)])
    for (u, d, _) in forced:
        cls.append([-lt(u, u + d)])
    s = Glucose42(bootstrap_with=cls)
    ok = s.solve()
    s.delete()
    return "SAT" if ok else "UNSAT"


for (b, j) in ((3, 2), (3, 3), (4, 2), (4, 3)):
    L = b ** j
    t0 = time.time()
    st = solve_block_pysat(L, b)
    print(f"pysat base {b} D_{j}=[{L},{b*L}): {st} ({time.time()-t0:.1f}s)", flush=True)
