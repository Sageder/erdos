"""mod1_sat.py — Modification idea 1 via SAT (exact, complete per block).

Encoding for internal order of block [c, 4c): boolean var x_{ab} (a<b values)
means "a is placed before b".  Clauses:
  transitivity  : for a<b<c forbid both 3-cycles.
  A4  (asc 4AP) : (~x_{w,w+e} | ~x_{w+e,w+2e} | ~x_{w+2e,w+3e})
  D4  (desc 4AP): ( x_{w,w+e} |  x_{w+e,w+2e} |  x_{w+2e,w+3e})
  A3T/A3H       : (~x_{w,w+e} | ~x_{w+e,w+2e})   when tail/head exists
  A2T/A2H       : unit (~x_{u,u+e})               when head(+tail) exist
  A2HH (seq.)   : unit (~x_{u,u+e}) when heads (u-3e,u-2e) ascend in pi_{m-1}
Any model is decoded to an order and INDEPENDENTLY re-verified by the
validated monotone-4-AP checker on the concatenated prefix.
"""

import sys
import time

from pysat.formula import CNF
from pysat.solvers import Cadical195

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")


def build_cnf(c, prev_asc=None):
    C = 4 * c
    cp = c // 4 if c >= 4 else 0
    vals = list(range(c, C))
    idx = {}
    nv = 0
    for i, a in enumerate(vals):
        for b in vals[i + 1:]:
            nv += 1
            idx[(a, b)] = nv          # var: a before b

    def X(a, b):
        """literal for 'a before b' (a != b)."""
        return idx[(a, b)] if a < b else -idx[(b, a)]

    cnf = CNF()
    n = len(vals)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, d = vals[i], vals[j], vals[k]
                cnf.append([-X(a, b), -X(b, d), X(a, d)])
                cnf.append([X(a, b), X(b, d), -X(a, d)])

    stats = dict(A4=0, D4=0, A3T=0, A3H=0, A2T=0, A2H=0, A2HH=0)
    for w in vals:
        e = 1
        while w + 3 * e < C:
            cnf.append([-X(w, w + e), -X(w + e, w + 2 * e),
                        -X(w + 2 * e, w + 3 * e)])
            cnf.append([X(w, w + e), X(w + e, w + 2 * e),
                        X(w + 2 * e, w + 3 * e)])
            stats["A4"] += 1
            stats["D4"] += 1
            e += 1
        e = 1
        while w + 2 * e < C:
            if w + 3 * e >= C:                                   # A3T
                cnf.append([-X(w, w + e), -X(w + e, w + 2 * e)])
                stats["A3T"] += 1
            if 1 <= w - e < c:                                   # A3H
                cnf.append([-X(w, w + e), -X(w + e, w + 2 * e)])
                stats["A3H"] += 1
            e += 1
        e = 1
        while w + e < C:
            if 1 <= w - e < c and w + 3 * e >= C:                # A2T
                cnf.append([-X(w, w + e)])
                stats["A2T"] += 1
            if cp <= w - e < c and 1 <= w - 2 * e < cp:          # A2H
                cnf.append([-X(w, w + e)])
                stats["A2H"] += 1
            if prev_asc is not None and cp >= 1 \
                    and cp <= w - 2 * e and w - e < c \
                    and (w - 2 * e, w - e) in prev_asc:          # A2HH
                cnf.append([-X(w, w + e)])
                stats["A2HH"] += 1
            e += 1
    return cnf, idx, vals, stats


def solve_block(c, prev_asc=None):
    cnf, idx, vals, stats = build_cnf(c, prev_asc)
    with Cadical195(bootstrap_with=cnf) as s:
        t0 = time.time()
        sat = s.solve()
        dt = time.time() - t0
        if not sat:
            return None, stats, dt
        model = set(l for l in s.get_model() if l > 0)
    # decode: count, for each value, how many others precede it
    order = sorted(vals, key=lambda v: sum(
        1 for u in vals if u != v and
        ((idx[(u, v)] in model) if u < v else (idx[(v, u)] not in model))))
    return order, stats, dt


def asc_pairs(order):
    p = {v: i for i, v in enumerate(order)}
    return frozenset((a, b) for a in order for b in order
                     if a < b and p[a] < p[b])


if __name__ == "__main__":
    from checkers import find_monotone_kap
    out = []

    def log(s):
        print(s, flush=True)
        out.append(s)

    log("=== Stage 1: block-independent constraints (A2HH off) ===")
    indep_sat = {}
    for m, c in enumerate([1, 4, 16, 64]):
        order, stats, dt = solve_block(c, prev_asc=None)
        indep_sat[m] = order
        log("block m=%d [%d,%d) size %d: %s  (%.1fs)  constraints=%s"
            % (m, c, 4 * c, 3 * c, "SAT" if order else "UNSAT", dt,
               {k: v for k, v in stats.items() if v}))
        if order:
            log("   pi_%d = %s" % (m, order))

    log("")
    log("=== Stage 2: sequential (A2HH on, feeding ascending pairs) ===")
    orders = []
    prev = None
    for m, c in enumerate([1, 4, 16, 64]):
        order, stats, dt = solve_block(c, prev_asc=prev if m > 0 else frozenset())
        log("block m=%d: %s (%.1fs), A2HH units: %d"
            % (m, "SAT" if order else "UNSAT", dt, stats["A2HH"]))
        if order is None:
            break
        orders.append(order)
        prev = asc_pairs(order)

    if orders:
        pref = [v for o in orders for v in o]
        n = len(pref)
        assert sorted(pref) == list(range(1, n + 1))
        w = find_monotone_kap(pref, 4)
        log("")
        log("independent recheck of concatenated prefix N=%d with validated "
            "4-AP checker: %s" % (n, "NO monotone 4-AP" if w is None
                                  else "FOUND %r <-- MODEL WRONG" % (w,)))
        w5 = find_monotone_kap(pref, 5)
        log("  (5-AP check on same prefix: %s)"
            % ("none" if w5 is None else repr(w5)))
        with open("/home/user/erdos/attempts/route-R2/mod1_prefix.txt", "w") as f:
            f.write(" ".join(map(str, pref)) + "\n")
        log("prefix written to mod1_prefix.txt")

    with open("/home/user/erdos/attempts/route-R2/mod1_sat_output.txt", "w") as f:
        f.write("\n".join(out) + "\n")
