"""sat_enum.py — enumerate multiple avoiders at a fixed (N, cls, C) via CaDiCaL with
blocking clauses (each found permutation is excluded by negating its x-variable set).
Every witness re-verified by apcheck. Writes AVOIDER lines to stdout.
usage: python3 sat_enum.py N cls num den k [round]
"""

import sys
from fractions import Fraction

from pysat.solvers import Cadical153

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos

sys.path.insert(0, "/home/user/erdos/attempts/route-R4")


def build_and_enum(N, cls, C, k, rnd="f"):
    # rebuild the same encoding as pysat_check.solve, but keep the solver for enumeration
    import pysat_check as pc
    # inline rebuild (copy of solve up to solving)
    num, den = C.numerator, C.denominator
    lo = [1] * (N + 1)
    hi = [N] * (N + 1)
    for v in range(1, N + 1):
        if cls in ("A", "C"):
            h = -((-num * v) // den) if rnd == "c" else (num * v) // den
            hi[v] = min(N, h)
        if cls in ("B", "C"):
            lo[v] = den * (v - 1) // num + 1 if rnd == "c" else -((-v * den) // num)
        if cls == "D" and v <= N // 2:
            hi[v] = min(N, 2 * v)
    nv = 0
    def new():
        nonlocal nv
        nv += 1
        return nv
    TRUE, FALSE = "T", "F"
    yv = {}
    for v in range(1, N + 1):
        for p in range(0, N + 1):
            yv[(v, p)] = FALSE if p < lo[v] else (TRUE if p >= hi[v] else new())
    xv = {}
    for v in range(1, N + 1):
        for p in range(lo[v], hi[v] + 1):
            xv[(v, p)] = new()
    cls_list = []
    def addc(*lits):
        out = []
        for sign, lit in lits:
            if lit == TRUE:
                if sign > 0:
                    return
                continue
            if lit == FALSE:
                if sign < 0:
                    return
                continue
            out.append(sign * lit)
        cls_list.append(out)
    Y = lambda v, p: yv[(v, p)]
    for v in range(1, N + 1):
        for p in range(lo[v], hi[v]):
            addc((-1, Y(v, p)), (1, Y(v, p + 1)))
        for p in range(lo[v], hi[v] + 1):
            x = xv[(v, p)]
            addc((-1, x), (1, Y(v, p)))
            addc((-1, x), (-1, Y(v, p - 1)))
            addc((1, x), (-1, Y(v, p)), (1, Y(v, p - 1)))
    for p in range(1, N + 1):
        vs = [v for v in range(1, N + 1) if lo[v] <= p <= hi[v]]
        addc(*[(1, xv[(v, p)]) for v in vs])
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                addc((-1, xv[(vs[i], p)]), (-1, xv[(vs[j], p)]))
    aps = []
    for d in range(1, (N - 1) // 3 + 1):
        for x0 in range(1, N - 3 * d + 1):
            aps.append((x0, x0 + d, x0 + 2 * d, x0 + 3 * d))
    B = {}
    for t in aps:
        for (u, w) in ((t[0], t[1]), (t[1], t[2]), (t[2], t[3])):
            if (u, w) in B:
                continue
            b = new()
            B[(u, w)] = b
            for p in range(0, N + 1):
                addc((-1, Y(u, p)), (1, Y(w, p)), (1, b))
                addc((-1, Y(w, p)), (1, Y(u, p)), (-1, b))
    for t0, t1, t2, t3 in aps:
        cls_list.append([-B[(t0, t1)], -B[(t1, t2)], -B[(t2, t3)]])
        cls_list.append([B[(t0, t1)], B[(t1, t2)], B[(t2, t3)]])

    out = []
    with Cadical153(bootstrap_with=cls_list) as s:
        for _ in range(k):
            if not s.solve():
                break
            model = set(l for l in s.get_model() if l > 0)
            perm = [0] * N
            block = []
            for (v, p), x in xv.items():
                if x in model:
                    perm[p - 1] = v
                    block.append(-x)
            assert sorted(perm) == list(range(1, N + 1))
            assert not has_monotone_kap_pos(perm, 4)
            out.append(perm)
            s.add_clause(block)
    return out


if __name__ == "__main__":
    N = int(sys.argv[1]); cls = sys.argv[2]
    C = Fraction(int(sys.argv[3]), int(sys.argv[4]))
    k = int(sys.argv[5])
    rnd = sys.argv[6] if len(sys.argv) > 6 else "f"
    perms = build_and_enum(N, cls, C, k, rnd)
    print(f"# {len(perms)} avoiders N={N} cls={cls} C={C} round={rnd}")
    for p in perms:
        print("AVOIDER " + " ".join(map(str, p)))
