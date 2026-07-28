"""pysat_check.py — third independent engine (CDCL SAT via python-sat / CaDiCaL).

Encoding (different from both fast2's backtracking and CP-SAT's integer model):
  - order encoding y[v,p] = [pos(v) <= p] for p in [lo(v)..hi(v)-1] (y at hi(v) == True,
    y below lo(v) == False, folded in as constants);
  - step variables x[v,p] = [pos(v) == p] channeled to y;
  - exactly-one value per position (pairwise AMO + ALO clause);
  - pair-order variables B[u,w] (u<w) with two-sided linking so that in EVERY model
    B[u,w] <=> pos(u) < pos(w);
  - for each 4-AP (t0..t3) in [1..N]: clauses (~B01 | ~B12 | ~B23) and (B01 | B12 | B23).
SAT model => witness permutation (re-verified by the validated apcheck checker);
UNSAT => no avoider under the constraint class.
Usage: python3 pysat_check.py N cls num den
"""

import sys
from fractions import Fraction

from pysat.solvers import Cadical153

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos


def solve(N, cls, C, rnd="f"):
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
    yv = {}                      # (v,p) -> literal or constant
    for v in range(1, N + 1):
        for p in range(0, N + 1):
            if p < lo[v]:
                yv[(v, p)] = FALSE
            elif p >= hi[v]:
                yv[(v, p)] = TRUE
            else:
                yv[(v, p)] = new()
    xv = {}
    for v in range(1, N + 1):
        for p in range(lo[v], hi[v] + 1):
            xv[(v, p)] = new()

    cls_list = []

    def Y(v, p):
        return yv[(v, p)]

    def addc(*lits):
        out = []
        for sign, lit in lits:
            if lit == TRUE:
                if sign > 0:
                    return          # clause satisfied
                continue            # -True dropped
            if lit == FALSE:
                if sign < 0:
                    return
                continue
            out.append(sign * lit)
        cls_list.append(out)

    # y monotone: y[v,p] -> y[v,p+1]
    for v in range(1, N + 1):
        for p in range(lo[v], hi[v]):
            addc((-1, Y(v, p)), (1, Y(v, p + 1)))
    # channel x
    for v in range(1, N + 1):
        for p in range(lo[v], hi[v] + 1):
            x = xv[(v, p)]
            addc((-1, x), (1, Y(v, p)))
            addc((-1, x), (-1, Y(v, p - 1)))
            addc((1, x), (-1, Y(v, p)), (1, Y(v, p - 1)))
    # positions: exactly one value
    for p in range(1, N + 1):
        vs = [v for v in range(1, N + 1) if lo[v] <= p <= hi[v]]
        addc(*[(1, xv[(v, p)]) for v in vs])
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                addc((-1, xv[(vs[i], p)]), (-1, xv[(vs[j], p)]))

    # 4-APs and pair-order variables
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
                # pos(u)<=p & pos(w)>p -> B ; pos(w)<=p & pos(u)>p -> ~B
                addc((-1, Y(u, p)), (1, Y(w, p)), (1, b))
                addc((-1, Y(w, p)), (1, Y(u, p)), (-1, b))
    for t0, t1, t2, t3 in aps:
        b1, b2, b3 = B[(t0, t1)], B[(t1, t2)], B[(t2, t3)]
        cls_list.append([-b1, -b2, -b3])
        cls_list.append([b1, b2, b3])

    with Cadical153(bootstrap_with=[c for c in cls_list if c is not None]) as s:
        sat = s.solve()
        if not sat:
            return "UNSAT", None
        model = set(l for l in s.get_model() if l > 0)
        perm = [0] * N
        for (v, p), x in xv.items():
            if x in model:
                perm[p - 1] = v
        assert sorted(perm) == list(range(1, N + 1)), "bad model"
        assert not has_monotone_kap_pos(perm, 4), "SAT produced bad witness!"
        return "SAT", perm


if __name__ == "__main__":
    N = int(sys.argv[1]); cls = sys.argv[2]
    C = Fraction(int(sys.argv[3]), int(sys.argv[4]))
    rnd = sys.argv[5] if len(sys.argv) > 5 else "f"
    status, perm = solve(N, cls, C, rnd)
    line = f"PYSAT N={N} cls={cls} C={C.numerator}/{C.denominator} status={status}"
    if perm:
        line += " example=" + ",".join(map(str, perm))
    print(line)
