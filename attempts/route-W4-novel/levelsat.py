"""levelsat.py — is there ANY choice of per-level digit orders making a
"first differing level" comparator monotone-4-AP-free, in a given numeration system
and with a given level PRIORITY?

Model (literal, re-derived from the definition each run):
  * a numeration system assigns to v a finite digit list eps_0(v), eps_1(v), ...
  * a PRIORITY is a rule picking, from the nonempty finite set of levels where u and w
    differ, the level that decides the pair.  'lsd' = smallest, 'msd' = largest.
  * a per-level linear order <_k on that level's digit alphabet.
  * u < w  in the comparator  iff  eps_k(u) <_k eps_k(w) at the deciding level k.
This is a linear order for ANY choice of the <_k (lexicographic on a well-ordered index
set), so transitivity is free -- the only question is 4-AP-freeness.

SAT variables: y[k,a,b] = "digit a precedes digit b at level k" for a != b.
Clauses: antisymmetry + totality + transitivity per level, then for each 4-AP
(t1,t2,t3,t4) with deciding-level literals A = [t1<t2], B = [t2<t3], C = [t3<t4]:
    (~A | ~B | ~C)   and   (A | B | C)
which is exactly "the descent word along the progression avoids 111 and 000"
(CORE Lemma 11(a)).

Verification: every SAT model is decoded back into an explicit order on [1..N] and
re-scanned with the apkit checker (cross-validated against experiments/apcheck.py).
"""
import sys
from itertools import combinations

sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from pysat.formula import CNF
from pysat.solvers import Cadical153, Glucose4
from apkit import pos_from_key, find_4aps
from numeration import (base_digits, factorial_digits, zeck_digits, fibs_upto,
                        ostrowski_digits, ostrowski_denoms)


class LevelModel:
    def __init__(self, digitfn, N, priority="lsd"):
        self.N = N
        self.priority = priority
        self.dig = [None] * (N + 1)
        L = 0
        for v in range(1, N + 1):
            d = list(digitfn(v))
            while d and d[-1] == 0:
                d.pop()
            self.dig[v] = d
            L = max(L, len(d))
        self.L = L
        self.alpha = [set() for _ in range(L)]
        for v in range(1, N + 1):
            d = self.dig[v]
            for k in range(L):
                self.alpha[k].add(d[k] if k < len(d) else 0)
        self.var = {}
        self.nv = 0

    def digit(self, v, k):
        d = self.dig[v]
        return d[k] if k < len(d) else 0

    def decide_level(self, u, w):
        L = max(len(self.dig[u]), len(self.dig[w]))
        diffs = [k for k in range(L) if self.digit(u, k) != self.digit(w, k)]
        assert diffs, (u, w)
        return diffs[0] if self.priority == "lsd" else diffs[-1]

    def y(self, k, a, b):
        key = (k, a, b)
        if key not in self.var:
            self.nv += 1
            self.var[key] = self.nv
        return self.var[key]

    def build(self):
        cnf = CNF()
        for k in range(self.L):
            A = sorted(self.alpha[k])
            for a, b in combinations(A, 2):
                x, y = self.y(k, a, b), self.y(k, b, a)
                cnf.append([x, y])
                cnf.append([-x, -y])
            for a in A:
                for b in A:
                    for c in A:
                        if len({a, b, c}) == 3:
                            cnf.append([-self.y(k, a, b), -self.y(k, b, c),
                                        self.y(k, a, c)])
        seen = set()
        naps = 0
        for d in range(1, (self.N - 1) // 3 + 1):
            for x in range(1, self.N - 3 * d + 1):
                t = [x, x + d, x + 2 * d, x + 3 * d]
                lits = []
                for i in range(3):
                    u, w = t[i], t[i + 1]
                    k = self.decide_level(u, w)
                    lits.append(self.y(k, self.digit(u, k), self.digit(w, k)))
                naps += 1
                key = tuple(lits)
                if key in seen:
                    continue
                seen.add(key)
                cnf.append([-lits[0], -lits[1], -lits[2]])
                cnf.append([lits[0], lits[1], lits[2]])
        self.cnf = cnf
        self.naps = naps
        return cnf

    def decode(self, model):
        pos = set(l for l in model if l > 0)
        rank = []
        for k in range(self.L):
            A = sorted(self.alpha[k])
            sc = {a: sum(1 for b in A if b != a and self.y(k, b, a) in pos) for a in A}
            rank.append(sc)
        return rank

    def keyfn(self, rank):
        L = self.L

        def key(v):
            d = [self.digit(v, k) for k in range(L)]
            r = [rank[k].get(d[k], 0) for k in range(L)]
            return tuple(r) if self.priority == "lsd" else tuple(reversed(r))
        return key


def run(name, digitfn, N, priority="lsd", verbose=True):
    m = LevelModel(digitfn, N, priority)
    cnf = m.build()
    res = {}
    for Sol, tag in ((Cadical153, "cadical"), (Glucose4, "glucose")):
        with Sol(bootstrap_with=cnf) as s:
            sat = s.solve()
            res[tag] = sat
            if sat and tag == "cadical":
                model = s.get_model()
                rank = m.decode(model)
                pos, _ = pos_from_key(N, m.keyfn(rank))
                hits = find_4aps(pos, N)
                res["reverify"] = "CLEAN" if not hits else "MODEL-BUG %r" % (hits[0],)
    agree = res["cadical"] == res["glucose"]
    verdict = "SAT" if res["cadical"] else "UNSAT"
    if verbose:
        extra = res.get("reverify", "")
        print(f"{name:40s} pri={priority:3s} N={N:5d} L={m.L:2d} vars={m.nv:4d} "
              f"clauses={len(cnf.clauses):6d} 4APs={m.naps:8d} -> {verdict:5s} "
              f"(2 solvers agree: {agree}) {extra}")
    return verdict, res


if __name__ == "__main__":
    NS = [int(a) for a in sys.argv[1:]] or [200, 800, 3000]
    for N in NS:
        F = fibs_upto(N)
        cf_p = [2] * 40
        qp = ostrowski_denoms(cf_p, N)
        cf_t = [3] * 40
        qt = ostrowski_denoms(cf_t, N)
        cf_e = [1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, 10, 1, 1, 12, 1, 1, 14, 1, 1, 16]
        qe = ostrowski_denoms(cf_e, N)
        systems = [
            ("base 2", lambda v: base_digits(v, 2)),
            ("base 3", lambda v: base_digits(v, 3)),
            ("base 4", lambda v: base_digits(v, 4)),
            ("base 5", lambda v: base_digits(v, 5)),
            ("factorial base", factorial_digits),
            ("Zeckendorf (phi)", lambda v: zeck_digits(v, F)),
            ("Ostrowski sqrt2 [2,2,..]", lambda v: ostrowski_digits(v, cf_p, qp)),
            ("Ostrowski [3,3,..]", lambda v: ostrowski_digits(v, cf_t, qt)),
            ("Ostrowski e-like (unbdd)", lambda v: ostrowski_digits(v, cf_e, qe)),
        ]
        print(f"----- N = {N} -----")
        for nm, fn in systems:
            for pri in ("lsd", "msd"):
                try:
                    run(nm, fn, N, pri)
                except Exception as ex:
                    print(f"{nm:40s} pri={pri} N={N} ERROR {ex}")
        print()
