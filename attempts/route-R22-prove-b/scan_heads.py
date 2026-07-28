"""scan_heads.py -- how robust is the early death of head-delay architectures?

For a grid of (b, s_m, K_m) the eager encoding (3 solvers must agree) is run at increasing
N to locate the first UNSAT, i.e. the board size at which NO within-class order avoids
monotone 4-APs.  Also reports the same for route R20's CLS(b,a) controls.
"""

import sys
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
sys.path.insert(0, '/home/user/erdos/experiments')
from eager import build_cnf, decode, head_class                       # noqa: E402
from arch import blk, v2                                             # noqa: E402
from apcheck import has_monotone_kap_pos                             # noqa: E402
from pysat.solvers import Solver                                     # noqa: E402


def verdict(N, cf, solvers=('cadical195', 'glucose4', 'minisat22')):
    cnf, vid, forced = build_cnf(N, cf)
    if forced:
        return forced[0]
    vs = []
    for s in solvers:
        with Solver(name=s, bootstrap_with=cnf) as S:
            sat = S.solve()
            mdl = S.get_model() if sat else None
        vs.append('SAT' if sat else 'UNSAT')
        if sat:
            perm = decode(N, cf, mdl, vid)
            assert not has_monotone_kap_pos(perm, 4)
    assert len(set(vs)) == 1, ("SOLVERS DISAGREE", N, vs)
    return vs[0]


def first_unsat(cf, lo=8, hi=400):
    """smallest N in [lo,hi] with UNSAT (assumes monotone: SAT is downward closed)."""
    if verdict(hi, cf) == 'SAT':
        return None
    a, b = lo, hi
    while a < b:
        mid = (a + b) // 2
        if verdict(mid, cf) == 'SAT':
            a = mid + 1
        else:
            b = mid
    return a


if __name__ == "__main__":
    rows = []
    for b in (3, 4, 5, 6, 7):
        for slab, s in (("m+1", lambda m: m + 1),
                        ("2m+2", lambda m: 2 * m + 2),
                        ("1", lambda m: 1)):
            for klab, K in (("m", lambda m: m), ("1", lambda m: 1), ("2^m", lambda m: 2 ** m)):
                cf = head_class(b, s, K)
                n = first_unsat(cf, 8, 400)
                rows.append((b, slab, klab, n))
                print(f"HEAD b={b} s={slab:5s} K={klab:4s}: first UNSAT N = {n}", flush=True)
    print()
    for b in (3, 4, 5, 6):
        cf = lambda v, b=b: blk(v, b) + v2(v)
        n = first_unsat(cf, 8, 400)
        print(f"CLS({b},a)  [route R20 control]      : first UNSAT N = {n}", flush=True)
    cf0 = lambda v: blk(v, 3)
    print(f"BLK(3) pure block layout (t==0)      : first UNSAT N = {first_unsat(cf0, 8, 400)}")
    cf0 = lambda v: blk(v, 5)
    print(f"BLK(5) pure block layout (t==0)      : first UNSAT N = {first_unsat(cf0, 8, 400)}")
