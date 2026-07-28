"""classsat.py — decide, by SAT, whether a CLASS ARCHITECTURE admits 4-AP-free
within-class orders on [1..N].

Setup.  A class function c : N -> Z with finite fibres is fixed (Lemma R20-1 guarantees
no 4-AP has a strictly monotone class sequence, so nothing is forced to die a priori).
The ordering is: classes in increasing index order, arbitrary linear order inside each
class.  The only freedom is the within-class orders; we ask SAT whether some choice is
monotone-4-AP-free on values [1..N].

Encoding.  x_{u,w} ("u before w") only for u < w in the SAME class; cross-class literals
are CONSTANTS.  Transitivity within classes is enforced lazily (CEGAR) exactly as in
experiments/profile_cegar.py: UNSAT at any round is UNSAT for the full system (adding
clauses only removes models); SAT is returned only when the implied tournament is acyclic,
and the decoded permutation is re-verified with the trusted checker.

UNSAT here is an IMPOSSIBILITY THEOREM for the class architecture at that N (modulo solver
correctness), covering EVERY choice of within-class orders — the analogue of route R1's
stage principle.
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R20-vlogv')
from apcheck import has_monotone_kap_pos
from pysat.solvers import Cadical195
from pysat.formula import IDPool
from profile_cegar import find_cycles
from constructions import cls_delay, cls_delay3, cls_block, v2, vp, logb


def solve_classes(N, c, max_rounds=200000, verbose=False):
    C = {v: c(v) for v in range(1, N + 1)}
    pool = IDPool()

    def var(u, w):                     # u < w, same class
        return pool.id(('x', u, w))

    TRUE, FALSE = 0, 1                 # sentinels

    def before_lit(u, w):
        """literal for 'u before w' with u < w; returns int literal or True/False."""
        if C[u] < C[w]:
            return True
        if C[u] > C[w]:
            return False
        return var(u, w)

    cl = []
    nfree = 0
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            lits = [before_lit(x + k * e, x + (k + 1) * e) for k in range(3)]
            # no increasing 4-AP: not all three "before"
            if all(l is not False for l in lits):
                cls_ = [-l for l in lits if l is not True]
                if not cls_:
                    return "FORCED-INC", (x, e), 0
                cl.append(cls_)
            # no decreasing 4-AP: not all three "after"
            if all(l is not True for l in lits):
                cls_ = [l for l in lits if l is not False]
                if not cls_:
                    return "FORCED-DEC", (x, e), 0
                cl.append(cls_)
    nfree = pool.top
    S = Cadical195(bootstrap_with=cl)
    rounds = 0
    while True:
        if not S.solve():
            S.delete()
            return "UNSAT", None, rounds
        model = set(S.get_model())

        def order_of(u, w):            # u < w
            if C[u] != C[w]:
                return C[u] < C[w]
            return var(u, w) in model

        cycs = find_cycles(order_of, N)
        if not cycs:
            import functools
            vals = list(range(1, N + 1))

            def cmp(u, w):
                if u == w:
                    return 0
                b = order_of(u, w) if u < w else (not order_of(w, u))
                return -1 if b else 1
            vals.sort(key=functools.cmp_to_key(cmp))
            S.delete()
            return "SAT", vals, rounds

        def lit_of(u, w):              # 'u before w' for arbitrary u != w, as a literal
            if u < w:
                r = before_lit(u, w)
                return r
            r = before_lit(w, u)
            if r is True:
                return False
            if r is False:
                return True
            return -r

        for cyc in cycs:
            L = len(cyc)
            for i in range(L):
                u, w, z = cyc[i], cyc[(i + 1) % L], cyc[(i + 2) % L]
                if len({u, w, z}) == 3:
                    a, b, d = lit_of(u, w), lit_of(w, z), lit_of(u, z)
                    if a is False or b is False or d is True:
                        continue
                    cc = []
                    if a is not True:
                        cc.append(-a)
                    if b is not True:
                        cc.append(-b)
                    if d is not False:
                        cc.append(d)
                    if cc:
                        S.add_clause(cc)
            cc = []
            ok = True
            for i in range(L):
                a = lit_of(cyc[i], cyc[(i + 1) % L])
                if a is False:
                    ok = False
                    break
                if a is not True:
                    cc.append(-a)
            if ok and cc:
                S.add_clause(cc)
        rounds += 1
        if verbose and rounds % 200 == 0:
            print(f"    [round {rounds}: {len(cycs)} cycles]", flush=True)
        if rounds > max_rounds:
            S.delete()
            return "UNKNOWN", None, rounds


FAMILIES = {
    'CLS(3,a)': cls_delay(3, lambda a: a),
    'CLS(4,a)': cls_delay(4, lambda a: a),
    'CLS(5,a)': cls_delay(5, lambda a: a),
    'CLS(6,a)': cls_delay(6, lambda a: a),
    'CLS(7,a)': cls_delay(7, lambda a: a),
    'CLS(3,2a)': cls_delay(3, lambda a: 2 * a),
    'CLS(4,2a)': cls_delay(4, lambda a: 2 * a),
    'BLK(3)': cls_block(3),
    'BLK(5)': cls_block(5),
}

if __name__ == "__main__":
    names = sys.argv[1].split(',') if len(sys.argv) > 1 else list(FAMILIES)
    Ns = [int(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else
                           ['60', '100', '160', '250', '400'])]
    for nm in names:
        c = FAMILIES[nm]
        for N in Ns:
            t0 = time.time()
            res, w, rounds = solve_classes(N, c)
            dt = time.time() - t0
            extra = ""
            if res == "SAT":
                assert sorted(w) == list(range(1, N + 1))
                assert not has_monotone_kap_pos(w, 4), "model is not an avoider!"
                pos = {v: i + 1 for i, v in enumerate(w)}
                mx = max(pos[v] / v for v in range(1, N + 1))
                extra = f" maxpos/v={mx:.2f}"
                with open(f"/home/user/erdos/attempts/route-R20-vlogv/cw_{nm}_{N}.txt", "w") as f:
                    f.write(repr(w))
            elif res.startswith("FORCED"):
                extra = f" at (x,e)={w}"
            print(f"{nm} N={N}: {res} ({dt:.0f}s, {rounds} rounds){extra}", flush=True)
            if res != "SAT":
                break
