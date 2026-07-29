"""signsat.py — EXACT decision procedure for the "class + van der Corput sign vector"
architecture (Proposition W4-3).

ARCHITECTURE.  c : N -> Z>=0 with finite fibres; classes emitted in increasing index
order; inside class j the order is the base-2 level comparator with a free sign vector
s_j : levels -> {0,1}:   for u < w in class j,  u precedes w  iff  bit_l(u) = s_j(l),
where l = v_2(w-u).  (Linear order for every s_j; monotone-3-AP-free on every subset.)

EXACT CHARACTERIZATION.  For a 4-AP (t1,t2,t3,t4) with step d and l := v_2(d), the three
consecutive pairs all have difference d, so with beta := bit_l(t1) one has
bit_l(t1)=bit_l(t3)=beta and bit_l(t2)=bit_l(t4)=1-beta.  Put, for i=1,2,3,
    A_i = TRUE                      if c(t_i) < c(t_{i+1})
        = FALSE                     if c(t_i) > c(t_{i+1})
        = [bit_l(t_i) = s_{c(t_i)}(l)]   if c(t_i) = c(t_{i+1}).
Then the AP is increasing iff A1&A2&A3 and decreasing iff ~A1&~A2&~A3, so the
architecture is monotone-4-AP-free  IFF  for every 4-AP
        (~A1 | ~A2 | ~A3)   and   (A1 | A2 | A3).
This is a 2-clause-per-4-AP SAT problem over the variables s_j(l) -- exact, not merely
sufficient.  It subsumes Proposition W4-2's clauses (a),(b),(c) as special cases where the
clauses are satisfied by constants.

Every SAT model is decoded to an explicit permutation of [1..N] and re-scanned with apkit
(cross-validated against experiments/apcheck.py).  Two solvers on every instance.
"""
import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from pysat.formula import CNF
from pysat.solvers import Cadical153, Glucose4
from apkit import pos_from_order, find_4aps


def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def bit(v, l):
    return (v >> l) & 1


class SignSat:
    def __init__(self, cls, N):
        self.cls, self.N = cls, N
        self.var, self.nv = {}, 0

    def s(self, j, l):
        k = (j, l)
        if k not in self.var:
            self.nv += 1
            self.var[k] = self.nv
        return self.var[k]

    def build(self):
        cnf = CNF()
        cls, N = self.cls, self.N
        TRUE = None
        nconst_bad = 0
        for d in range(1, (N - 1) // 3 + 1):
            l = v2(d)
            for x in range(1, N - 3 * d + 1):
                t = [x + i * d for i in range(4)]
                lits = []
                const = []
                ok = True
                for i in range(3):
                    a, b = cls[t[i]], cls[t[i + 1]]
                    if a < b:
                        const.append(True)
                    elif a > b:
                        const.append(False)
                    else:
                        v = self.s(a, l)
                        lits.append(v if bit(t[i], l) == 1 else -v)
                        const.append(None)
                pos = [c for c in const if c is True]
                neg = [c for c in const if c is False]
                # clause 1: not all true  ->  if some const is False it's satisfied
                if not neg:
                    if not lits:
                        ok = False           # all const True: increasing 4-AP, unfixable
                    else:
                        cnf.append([-x_ for x_ in lits])
                # clause 2: not all false -> if some const is True it's satisfied
                if not pos:
                    if not lits:
                        ok = False           # all const False: decreasing 4-AP
                    else:
                        cnf.append(list(lits))
                if not ok:
                    nconst_bad += 1
        self.cnf = cnf
        self.hard_bad = nconst_bad
        return cnf

    def order_from_model(self, model):
        pos_set = set(m for m in model if m > 0)
        groups = {}
        for v in range(1, self.N + 1):
            groups.setdefault(self.cls[v], []).append(v)
        out = []
        for j in sorted(groups):
            def key(v, j=j):
                r = []
                for l in range(40):
                    sv = self.var.get((j, l))
                    sgn = 1 if (sv is not None and sv in pos_set) else 0
                    dg = bit(v, l)
                    r.append(dg if sgn == 0 else 1 - dg)
                return tuple(r)
            out.extend(sorted(groups[j], key=key))
        return out


def decide(cls, N, verbose=False, name=""):
    m = SignSat(cls, N)
    cnf = m.build()
    if m.hard_bad:
        return "UNSAT", {"reason": f"{m.hard_bad} 4-APs fixed by the class order alone",
                         "agree": True}
    out = {}
    with Cadical153(bootstrap_with=cnf) as s1:
        sat1 = s1.solve()
        model = s1.get_model() if sat1 else None
    with Glucose4(bootstrap_with=cnf) as s2:
        sat2 = s2.solve()
    out["agree"] = (sat1 == sat2)
    if sat1:
        order = m.order_from_model(model)
        pos = pos_from_order(order)
        hits = find_4aps(pos, N)
        out["recheck"] = "CLEAN" if not hits else "MODEL-BUG %r" % (hits[0],)
        out["disp"] = max((int(pos[v]) + 1) / v for v in range(1, N + 1))
    return ("SAT" if sat1 else "UNSAT"), out


def threshold(clsfn, lo=4, hi=1200):
    """minimal N with UNSAT; returns (last SAT N, first UNSAT N) or (hi, None)."""
    cls = clsfn(hi)
    v, _ = decide(cls, hi)
    if v == "SAT":
        return hi, None
    a, b = lo, hi
    while a + 1 < b:
        mid = (a + b) // 2
        v, _ = decide(clsfn(mid), mid)
        if v == "SAT":
            a = mid
        else:
            b = mid
    return a, b
