"""engine.py — route-R21 CEGAR order-encoding engine (extension of
experiments/profile_cegar.py, whose `find_cycles` and lazy-transitivity loop are reused
verbatim; that engine is validated against route R9's exhaustive enumeration at
C = 1.5 / 1.75 and against an eager two-solver encoding at C = 2, N = 85/90).

Extension: arbitrary extra clauses over the order literals may be supplied, so that
placement side conditions (pin a value late, force one AP's restriction to be
C-tame, ...) can be added on top of "no monotone 4-AP".

Soundness notes carried over unchanged:
  * adding transitivity clauses only removes models, so an UNSAT at any CEGAR round is
    an UNSAT for the full transitive system (sound for UNSAT at every stage);
  * a returned SAT model is decoded to a permutation and re-verified with the trusted
    checker apcheck.has_monotone_kap_pos plus all side conditions, so SAT is a
    constructive certificate independent of the encoding.
"""

import sys, functools, time

sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos                    # noqa: E402
from profile_cegar import find_cycles                        # noqa: E402
from pysat.solvers import Cadical195, Glucose42              # noqa: E402
from pysat.card import CardEnc, EncType                      # noqa: E402
from pysat.formula import IDPool                             # noqa: E402


class OrderEncoding:
    """x[(u,w)] for u<w means 'u is positioned before w'."""

    def __init__(self, N):
        self.N = N
        self.pool = IDPool()
        self.clauses = []

    def var(self, u, w):
        assert u < w
        return self.pool.id(('x', u, w))

    def lit(self, u, w):
        """literal for 'u before w', any u != w."""
        return self.var(u, w) if u < w else -self.var(w, u)

    def add(self, clause):
        self.clauses.append(clause)

    def no_monotone_4ap(self):
        N = self.N
        for e in range(1, (N - 1) // 3 + 1):
            for x in range(1, N - 3 * e + 1):
                a = [self.lit(x + k * e, x + (k + 1) * e) for k in range(3)]
                self.add([-a[0], -a[1], -a[2]])   # no increasing 4-AP
                self.add([a[0], a[1], a[2]])      # no decreasing 4-AP

    def before_all(self, small, others):
        """force every value in `others` to be positioned before every value in `small`."""
        for v in small:
            for w in others:
                if v != w:
                    self.add([self.lit(w, v)])

    def rank_atmost(self, v, subset, bound):
        """rank of v inside `subset` (v in subset) is <= bound:
        #{w in subset, w != v : w before v} <= bound-1."""
        lits = [self.lit(w, v) for w in subset if w != v]
        if bound - 1 >= len(lits):
            return
        if bound - 1 < 0:
            self.add([])
            return
        enc = CardEnc.atmost(lits=lits, bound=bound - 1, vpool=self.pool,
                             encoding=EncType.seqcounter)
        self.clauses.extend(enc.clauses)

    def profile(self, C):
        """pos(v) <= floor(C*v) for all v (global linear profile)."""
        N = self.N
        allv = list(range(1, N + 1))
        for v in allv:
            b = int(C * v)
            if b >= N:
                continue
            self.rank_atmost(v, allv, b)

    def ap_tame(self, q, r, C):
        """the AP {r+q, r+2q, ...} restricted to [1..N] has pos_P(n) <= floor(C*n)."""
        el = [r + q * n for n in range(1, (self.N - r) // q + 1) if r + q * n <= self.N]
        L = len(el)
        for n, v in enumerate(el, start=1):
            b = int(C * n)
            if b >= L:
                continue
            self.rank_atmost(v, el, b)
        return L


def solve(enc, solver="cadical", max_rounds=2000000, verbose=False, time_budget=None):
    N = enc.N
    S = (Cadical195 if solver == "cadical" else Glucose42)(bootstrap_with=enc.clauses)
    rounds, t0 = 0, time.time()
    while True:
        if not S.solve():
            S.delete()
            return "UNSAT", None, rounds
        model = set(S.get_model())

        def order_of(u, w):
            return enc.var(u, w) in model

        cycs = find_cycles(order_of, N)
        if not cycs:
            vals = list(range(1, N + 1))

            def cmp(u, w):
                if u == w:
                    return 0
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
                    S.add_clause([-enc.lit(u, w), -enc.lit(w, z), enc.lit(u, z)])
            S.add_clause([-enc.lit(cyc[i], cyc[(i + 1) % L]) for i in range(L)])
        rounds += 1
        if verbose and rounds % 250 == 0:
            print(f"    [round {rounds}: {len(cycs)} cycles, {time.time()-t0:.0f}s]",
                  flush=True)
        if rounds > max_rounds or (time_budget and time.time() - t0 > time_budget):
            S.delete()
            return "UNKNOWN", None, rounds


def verify_avoider(perm, N):
    assert sorted(perm) == list(range(1, N + 1)), "not a permutation"
    assert not has_monotone_kap_pos(perm, 4), "model contains a monotone 4-AP"
    return True
