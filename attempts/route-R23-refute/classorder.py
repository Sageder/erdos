"""classorder.py -- does a class architecture admit a monotone-4-AP-free within-class order?

Condition (ii) is only NECESSARY for a class architecture c to be a 196 counterexample: it
kills the 4-APs whose class sequence is strictly monotone.  The remaining 4-APs must be
killed by the (free) order inside each class.  This script decides, for a given class
function c on [1..N], whether SOME choice of within-class orders makes the whole listing
monotone-4-AP-free.

Engine: the order encoding of experiments/profile_cegar.py (x_{u,w} = "u before w",
lazy transitivity via CEGAR) with the profile cardinality constraints replaced by unit
clauses c(u) < c(w) => u before w.  SAT models are decoded and re-verified with the
TRUSTED checker experiments/apcheck.py; UNSAT is re-verified with a second solver.
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R23-refute')
from apcheck import has_monotone_kap_pos
from profile_cegar import find_cycles
from pysat.solvers import Cadical195, Glucose42
from pysat.formula import IDPool
from cond2 import blk


def solve_classorder(c, N, max_rounds=200000, verbose=False, second_solver=True):
    """c: list with c[v] for v in 1..N."""
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

    S = Cadical195(bootstrap_with=cl)
    rounds = 0
    extra = []
    while True:
        if not S.solve():
            S.delete()
            if second_solver:
                S2 = Glucose42(bootstrap_with=cl + extra)
                ok2 = S2.solve(); S2.delete()
                return ("UNSAT" if not ok2 else "DISAGREE"), None, rounds
            return "UNSAT", None, rounds
        model = set(S.get_model())
        def order_of(u, w):
            return var(u, w) in model
        cycs = find_cycles(order_of, N)
        if not cycs:
            import functools
            vals = list(range(1, N + 1))
            def cmp(u, w):
                if u == w: return 0
                before = order_of(u, w) if u < w else (not order_of(w, u))
                return -1 if before else 1
            vals.sort(key=functools.cmp_to_key(cmp))
            S.delete()
            return "SAT", vals, rounds
        for cyc in cycs:
            L = len(cyc)
            for i in range(L):
                u, w, z = cyc[i], cyc[(i + 1) % L], cyc[(i + 2) % L]
                if len({u, w, z}) == 3:
                    C3 = [-lit(u, w), -lit(w, z), lit(u, z)]
                    S.add_clause(C3); extra.append(C3)
            C = [-lit(cyc[i], cyc[(i + 1) % L]) for i in range(L)]
            S.add_clause(C); extra.append(C)
        rounds += 1
        if verbose and rounds % 500 == 0:
            print(f"    [round {rounds}: {len(cycs)} cycles]", flush=True)
        if rounds > max_rounds:
            S.delete()
            return "UNKNOWN", None, rounds


def classes_of(t, N, b):
    return [0] + [blk(v, b) + t[v] for v in range(1, N + 1)]


def check(tag, c, N, verbose=False):
    t0 = time.time()
    res, perm, rounds = solve_classorder(c, N, verbose=verbose)
    dt = time.time() - t0
    if res == "SAT":
        assert sorted(perm) == list(range(1, N + 1))
        assert not has_monotone_kap_pos(perm, 4), "solver model is NOT an avoider"
        pos = {v: i + 1 for i, v in enumerate(perm)}
        for u in range(1, N + 1):
            for w in range(1, N + 1):
                if c[u] < c[w]:
                    assert pos[u] < pos[w], "class order violated"
    print(f"  {tag}: {res}  ({dt:.0f}s, {rounds} cegar rounds)", flush=True)
    return res, perm
