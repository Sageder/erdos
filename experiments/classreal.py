"""classreal.py — is a candidate class function REALIZABLE?

Condition (ii) (no strictly monotone class sequence along any 4-AP) is NECESSARY for a
class architecture to be monotone-4-AP-free, but NOT sufficient: values sharing a class are
ordered freely, and those free orders must themselves avoid monotone 4-APs.

Given c : [1..N] -> Z>=0 (classes emitted in increasing index order), we ask SAT whether
ANY choice of within-class orders yields a monotone-4-AP-free permutation. Cross-class
comparisons are forced by the class index; same-class comparisons are Boolean variables
with lazy transitivity (CEGAR), the engine validated in experiments/profile_cegar.py.

UNSAT here is an impossibility theorem for that class function, quantified over all
within-class orders -- the same logical shape as route R1's stage certificates.
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from profile_cegar import find_cycles
from pysat.solvers import Cadical195
from pysat.formula import IDPool


def realizable(c, N, max_rounds=100000):
    pool = IDPool()
    def var(u, w): return pool.id(('x', u, w))          # u < w, same class
    def before(u, w):
        """literal (or True/False) for 'u positioned before w'."""
        if c[u] != c[w]: return c[u] < c[w]
        return var(u, w) if u < w else -var(w, u)
    cl = []
    for d in range(1, N // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            u = [x + i * d for i in range(4)]
            for sgn in (True, False):
                lits, forced = [], True
                for i in range(3):
                    b = before(u[i], u[i + 1]) if sgn else before(u[i + 1], u[i])
                    if b is True: continue
                    if b is False: forced = False; break
                    lits.append(b)
                if forced:
                    cl.append([-l for l in lits])       # empty clause => UNSAT (correct)
    S = Cadical195(bootstrap_with=cl); rounds = 0
    while True:
        if not S.solve(): S.delete(); return False, None, rounds
        model = set(S.get_model())
        def order_of(u, w):
            if c[u] != c[w]: return c[u] < c[w]
            return var(u, w) in model
        cy = find_cycles(order_of, N)
        if not cy:
            import functools
            vals = sorted(range(1, N + 1), key=functools.cmp_to_key(
                lambda u, w: 0 if u == w else (-1 if (order_of(u, w) if u < w else not order_of(w, u)) else 1)))
            S.delete(); return True, vals, rounds
        for cyc in cy:
            L = len(cyc)
            for i in range(L):
                a, b2, e = cyc[i], cyc[(i+1) % L], cyc[(i+2) % L]
                if len({a, b2, e}) == 3:
                    la, lb, lc = before(a, b2), before(b2, e), before(a, e)
                    lits = [x for x in (-la if la is not True and la is not False else None,
                                        -lb if lb is not True and lb is not False else None,
                                        lc if lc is not True and lc is not False else None) if x is not None]
                    if lits: S.add_clause(lits)
        rounds += 1
        if rounds > max_rounds: S.delete(); return None, None, rounds
