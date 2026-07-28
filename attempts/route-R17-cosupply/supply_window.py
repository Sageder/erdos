"""supply_window.py — R17.  Exact window analysis of the SUPPLY configuration.

Setup.  Lemma 16.1 (supply) hands us, at a prescribed value w and modulus m, SOME
step e with (w, w+e, w+2e) positionally increasing.  Then u := w+2e is OPEN at scale
e and the forcing step gives u+e = w+3e  prec  u.  A forcing CHAIN needs w+3e to be
open too.  Question (mission): at which scales f CAN w+2e and w+3e be open, and which
of those are consistent with 4-AP-freeness?

Method.  Order-encoded SAT over permutations of the window [1..N] (variables
x[(p,q)] = "pos(p) < pos(q)" for p<q, plus transitivity, plus the 4-AP clauses).
Restriction principle: the restriction of ANY 4-AP-free permutation of N to [1..N] is
a 4-AP-free permutation of [1..N] realising the same relative order, and every
condition below mentions only values <= N.  Hence:
    UNSAT on the window  ==>  the configuration is impossible in EVERY 4-AP-free
                              permutation of N   (a theorem, modulo solver soundness)
    SAT on the window    ==>  not excluded by values <= N alone (no conclusion).
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
from pysat.solvers import Cadical195, Glucose42
from pysat.formula import IDPool
from apcheck import has_monotone_kap_pos


class Win:
    def __init__(self, N):
        self.N = N
        self.pool = IDPool()
        self.cl = []
        for u in range(1, N + 1):
            for v in range(u + 1, N + 1):
                for w in range(v + 1, N + 1):
                    a, b, c = self.v(u, v), self.v(v, w), self.v(u, w)
                    self.cl.append([-a, -b, c])
                    self.cl.append([a, b, -c])
        for e in range(1, (N - 1) // 3 + 1):
            for x in range(1, N - 3 * e + 1):
                y1 = self.v(x, x + e)
                y2 = self.v(x + e, x + 2 * e)
                y3 = self.v(x + 2 * e, x + 3 * e)
                self.cl.append([-y1, -y2, -y3])   # no increasing 4-AP
                self.cl.append([y1, y2, y3])      # no decreasing 4-AP

    def v(self, u, w):
        assert u < w
        return self.pool.id(('x', u, w))

    def lit(self, p, q):
        """literal for 'p prec q' (pos(p) < pos(q)), p != q."""
        return self.v(p, q) if p < q else -self.v(q, p)

    def chain(self, seq):
        """list of literals asserting seq[0] prec seq[1] prec ... (all in range)."""
        return [self.lit(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]

    def inrange(self, seq):
        return all(1 <= t <= self.N for t in seq)

    def solve(self, extra):
        S = Cadical195(bootstrap_with=self.cl + extra)
        r = S.solve()
        model = set(S.get_model()) if r else None
        S.delete()
        return r, model

    def decode(self, model):
        import functools
        vals = list(range(1, self.N + 1))
        def cmp(u, w):
            if u == w:
                return 0
            if u < w:
                return -1 if self.v(u, w) in model else 1
            return 1 if self.v(w, u) in model else -1
        vals.sort(key=functools.cmp_to_key(cmp))
        return vals


def open_scales_constraints(W, u, f):
    """literals asserting 'u is open at scale f' = (u-2f prec u-f prec u)."""
    seq = [u - 2 * f, u - f, u]
    if not W.inrange(seq):
        return None
    return W.chain(seq)


def sink_clauses(W, u, rules=('U1',)):
    """clauses asserting u is a SINK of the given rule set inside the window."""
    out = []
    N = W.N
    if 'U1' in rules:
        for d in range(1, (u - 1) // 2 + 1):
            l = W.chain([u - 2 * d, u - d, u])
            out.append([-l[0], -l[1]])
    if 'U2' in rules:
        d = 1
        while u + 3 * d <= N:
            l = W.chain([u + d, u + 2 * d, u + 3 * d])
            out.append([-l[0], -l[1]])
            d += 1
    if 'D1' in rules:
        d = 1
        while u + 2 * d <= N:
            if u - d >= 1:
                l = W.chain([u + 2 * d, u + d, u])
                out.append([-l[0], -l[1]])
            d += 1
    if 'D2' in rules:
        for d in range(1, (u - 1) // 3 + 1):
            l = W.chain([u - d, u - 2 * d, u - 3 * d])
            out.append([-l[0], -l[1]])
    return out


def analyse(w, e, pad=2):
    """Given the supply configuration (w, w+e, w+2e) increasing, report for
    u1 = w+2e and u2 = w+3e which open-scales f are SAT / UNSAT on the window."""
    N = w + 3 * e + pad * e
    W = Win(N)
    base = W.chain([w, w + e, w + 2 * e])
    base = [[l] for l in base]
    res = {}
    for name, u in (("w+2e", w + 2 * e), ("w+3e", w + 3 * e)):
        sat_f, unsat_f = [], []
        for f in range(1, (u - 1) // 2 + 1):
            c = open_scales_constraints(W, u, f)
            if c is None:
                continue
            r, _ = W.solve(base + [[l] for l in c])
            (sat_f if r else unsat_f).append(f)
        res[name] = (sat_f, unsat_f)
    # can w+3e be a G-sink / a G*-sink?
    rG, _ = W.solve(base + sink_clauses(W, w + 3 * e, ('U1',)))
    rGs, _ = W.solve(base + sink_clauses(W, w + 3 * e, ('U1', 'U2', 'D1', 'D2')))
    return N, res, rG, rGs


if __name__ == "__main__":
    print("Window analysis of the supply configuration (w, w+e, w+2e) increasing.")
    print("UNSAT scales are THEOREMS (impossible in every 4-AP-free permutation of N).\n")
    for w in (1, 2, 3):
        for e in (2, 3, 4, 6, 8):
            N, res, rG, rGs = analyse(w, e)
            s1, u1 = res["w+2e"]
            s2, u2 = res["w+3e"]
            print(f"w={w} e={e} (window N={N}):")
            print(f"   u=w+2e={w+2*e}: open-scales SAT {s1}   UNSAT {u1}")
            print(f"   u=w+3e={w+3*e}: open-scales SAT {s2}   UNSAT {u2}")
            print(f"   w+3e can be a G-sink: {rG}     w+3e can be a G*-sink: {rGs}", flush=True)
