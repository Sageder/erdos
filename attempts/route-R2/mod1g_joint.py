"""mod1g_joint.py — joint SAT over blocks 0,1,2 of the 4^m chain (values
1..63), with ALL constraints including the cross-block (2,2) couplings
(A2HH as clauses, not units).  Outcome either:
  SAT   -> a 63-prefix with no visible monotone 4-AP (completeness test), or
  UNSAT -> the chain already dies at block 2 jointly.
Blocks: [1,4), [4,16), [16,64); boundaries 1, 4, 16, 64; c' boundaries 0,1,4.
"""

import sys
import time

from pysat.formula import CNF
from pysat.solvers import Cadical195

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
sys.path.insert(0, "/home/user/erdos/experiments")

BOUNDS = [1, 4, 16, 64, 256]      # b_0..b_4 (b_4 only as "beyond" marker)


def block_of(v):
    for m in range(len(BOUNDS) - 1):
        if BOUNDS[m] <= v < BOUNDS[m + 1]:
            return m
    raise ValueError


def build_joint():
    idx = {}
    nv = 0
    blocks = [list(range(BOUNDS[m], BOUNDS[m + 1])) for m in range(3)]
    for vals in blocks:
        for i, a in enumerate(vals):
            for b in vals[i + 1:]:
                nv += 1
                idx[(a, b)] = nv

    def X(a, b):
        return idx[(a, b)] if a < b else -idx[(b, a)]

    def sameblock(*vs):
        return all(block_of(v) == block_of(vs[0]) for v in vs)

    cnf = CNF()
    # transitivity inside each block
    for vals in blocks:
        n = len(vals)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    a, b, d = vals[i], vals[j], vals[k]
                    cnf.append([-X(a, b), -X(b, d), X(a, d)])
                    cnf.append([X(a, b), X(b, d), -X(a, d)])

    # pattern constraints per block m with boundaries (c', c, C)
    for m in range(3):
        cp, c, C = (BOUNDS[m - 1] if m >= 1 else 0), BOUNDS[m], BOUNDS[m + 1]
        for w in range(c, C):
            e = 1
            while w + 3 * e < C:
                T = (w, w + e, w + 2 * e, w + 3 * e)
                cnf.append([-X(T[0], T[1]), -X(T[1], T[2]), -X(T[2], T[3])])
                cnf.append([X(T[0], T[1]), X(T[1], T[2]), X(T[2], T[3])])
                e += 1
            e = 1
            while w + 2 * e < C:
                if w + 3 * e >= C:                                # A3T
                    cnf.append([-X(w, w + e), -X(w + e, w + 2 * e)])
                if 1 <= w - e < c:                                # A3H
                    cnf.append([-X(w, w + e), -X(w + e, w + 2 * e)])
                e += 1
            e = 1
            while w + e < C:
                if 1 <= w - e < c and w + 2 * e >= C:             # A2T
                    cnf.append([-X(w, w + e)])
                if m >= 1 and cp <= w - e < c and 1 <= w - 2 * e < cp:  # A2H
                    cnf.append([-X(w, w + e)])
                # A2HH as coupling clause: heads (w-2e, w-e) in block m-1
                if m >= 1 and cp <= w - 2 * e and w - e < c \
                        and sameblock(w - 2 * e, w - e) \
                        and block_of(w - 2 * e) == m - 1:
                    cnf.append([-X(w - 2 * e, w - e), -X(w, w + e)])
                e += 1
    return cnf, idx, blocks


def decode(model, idx, blocks):
    model = set(l for l in model if l > 0)
    orders = []
    for vals in blocks:
        def nbefore(v):
            k = 0
            for u in vals:
                if u == v:
                    continue
                ab = (u, v) if u < v else (v, u)
                pos_uv = idx[ab] in model
                if (u < v) == pos_uv:
                    k += 1
            return k
        orders.append(sorted(vals, key=nbefore))
    return orders


if __name__ == "__main__":
    from apcheck import has_monotone_kap_pos
    cnf, idx, blocks = build_joint()
    with Cadical195(bootstrap_with=cnf) as s:
        t0 = time.time()
        sat = s.solve()
        dt = time.time() - t0
        print("joint blocks 0..2 (values 1..63): %s (%.1fs)"
              % ("SAT" if sat else "UNSAT", dt))
        lines = ["joint blocks 0..2 (values 1..63): %s"
                 % ("SAT" if sat else "UNSAT")]
        if sat:
            orders = decode(s.get_model(), idx, blocks)
            pref = [v for o in orders for v in o]
            assert sorted(pref) == list(range(1, 64))
            has4 = has_monotone_kap_pos(pref, 4)
            print("prefix:", pref)
            print("monotone 4-AP in 63-prefix (validated checker):", has4)
            lines.append("prefix: %s" % (pref,))
            lines.append("monotone 4-AP in 63-prefix: %s" % has4)
            assert not has4, "COMPLETENESS FAILURE: unpredicted 4-AP shape!"
            lines.append("COMPLETENESS TEST OK: all-constraints-satisfying "
                         "orders give a 4-AP-free 63-prefix")
            print(lines[-1])
    with open("/home/user/erdos/attempts/route-R2/mod1g_output.txt", "w") as f:
        f.write("\n".join(lines) + "\n")
