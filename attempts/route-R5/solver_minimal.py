"""solver_minimal.py — forcing-cascade solver for route R5 (Erdős 196, YES side).

Model.  Let a be a hypothetical monotone-4-AP-free permutation of ℕ.  By the 3-AP
forcing theorem (proof_3ap.md) increasing 3-APs exist; by well-ordering we may extract
one that is MINIMAL for various well-founded measures.  Fix such a minimal increasing
3-AP (x, x+d, x+2d), pos(x) = i < pos(x+d) = j < pos(x+2d) = k.

A "window" is a finite set OFF of integer offsets c, representing values x + c·u where
u = d (grid windows, offsets are multiples of the grid unit 1 <-> value step d) or
u = 1 (interval windows; then d is the concrete integer given by the base triple).
Every arithmetic progression among offsets corresponds to a genuine AP of values, for
EVERY admissible x, d.  The unknown is only the relative POSITION ORDER of the window
values, i.e. a linear order on OFF.  Encoded in SAT with boolean o(a,b) = "value x+a·u
sits at an earlier position than x+b·u", plus transitivity.

Constraint families (each VALID = a true consequence for the infinite permutation,
under the stated case assumptions; quantifier bookkeeping in REPORT.md):

  blocked4 : for every 4-term AP inside OFF, positions are not monotone.       [always]
  base     : P(x) < P(x+d) < P(x+2d) for the chosen minimal triple.            [always]
  kmin     : no increasing 3-AP inside the window ends strictly before P(x+2d).
             [valid when the base triple is chosen with minimal top POSITION]
  stepmin_lt(s): no increasing 3-AP inside the window has value-step < s.
             [valid when the base triple is chosen with minimal STEP d = s,
              interval windows only — grid windows see only multiples of d]
  topvalmin: no increasing 3-AP inside the window has top VALUE < x+2d.
             [valid when the base triple minimizes the top value]

Window existence caveat: offsets c < 0 assume x > |c|·u (case assumption, reported per
run).  Absolute windows [1..W] instead pin x, d concretely and need no assumption.

If any configuration is UNSAT, the corresponding minimality case is refuted for every
4-AP-free permutation — an actual step toward YES.  If SAT, we compute the BACKBONE
(all forced order relations) = the complete list of positional facts forced by the
cascade at this window size.
"""

from itertools import combinations
from pysat.solvers import Glucose42


def aps_within(offsets, length):
    """All arithmetic progressions of given length inside the offset set."""
    S = set(offsets)
    out = []
    for a in offsets:
        for b in offsets:
            if b <= a:
                continue
            e = b - a
            terms = [a + t * e for t in range(length)]
            if all(t in S for t in terms):
                out.append(tuple(terms))
    return out


class OrderSAT:
    def __init__(self, offsets):
        self.off = sorted(offsets)
        self.idx = {c: t for t, c in enumerate(self.off)}
        n = len(self.off)
        self.n = n
        self.varmap = {}
        ctr = [0]

        def var(a, b):  # boolean: P_a < P_b   (a, b offsets, a != b)
            if (a, b) in self.varmap:
                return self.varmap[(a, b)]
            if (b, a) in self.varmap:
                return -self.varmap[(b, a)]
            ctr[0] += 1
            self.varmap[(a, b)] = ctr[0]
            return ctr[0]

        self.var = var
        self.clauses = []
        # transitivity: (a<b & b<c) -> a<c  for all ordered triples of distinct offsets
        for a, b, c in combinations(self.off, 3):
            for (p, q, r) in [(a, b, c), (a, c, b), (b, a, c)]:
                # p<q & q<r -> p<r ; enumerating the 3 essentially distinct patterns
                self.clauses.append([-var(p, q), -var(q, r), var(p, r)])
                self.clauses.append([var(p, q), var(q, r), -var(p, r)])
        self.n_trans = len(self.clauses)

    def add_blocked4(self):
        for q in aps_within(self.off, 4):
            a, b, c, d = q
            v = self.var
            self.clauses.append([-v(a, b), -v(b, c), -v(c, d)])   # not increasing
            self.clauses.append([-v(d, c), -v(c, b), -v(b, a)])   # not decreasing

    def add_base(self, tri):
        a, b, c = tri
        self.clauses.append([self.var(a, b)])
        self.clauses.append([self.var(b, c)])

    def add_kmin(self, top):
        # no window 3-AP (a,b,c) with P_a<P_b<P_c and P_c<P_top
        for a, b, c in aps_within(self.off, 3):
            if c == top:
                continue
            v = self.var
            self.clauses.append([-v(a, b), -v(b, c), -v(c, top)])

    def add_stepmin_lt(self, s):
        for a, b, c in aps_within(self.off, 3):
            if b - a < s:
                v = self.var
                self.clauses.append([-v(a, b), -v(b, c)])

    def add_topvalmin(self, topval):
        for a, b, c in aps_within(self.off, 3):
            if c < topval:
                v = self.var
                self.clauses.append([-v(a, b), -v(b, c)])

    def solve(self, assumptions=()):
        with Glucose42(bootstrap_with=self.clauses) as s:
            return s.solve(assumptions=list(assumptions))

    def backbone(self):
        """Return list of forced relations (a,b) meaning P_a < P_b in EVERY model."""
        forced = []
        with Glucose42(bootstrap_with=self.clauses) as s:
            if not s.solve():
                return None
            for (a, b), v in list(self.varmap.items()):
                if not s.solve(assumptions=[-v]):
                    forced.append((a, b))
                elif not s.solve(assumptions=[v]):
                    forced.append((b, a))
        return forced

    def one_model(self):
        with Glucose42(bootstrap_with=self.clauses) as s:
            if not s.solve():
                return None
            model = set(l for l in s.get_model() if l > 0)
            order = sorted(self.off,
                           key=lambda c: sum(1 for b in self.off if b != c and
                                             self._lt(model, b, c)))
            return order  # offsets listed in position order

    def _lt(self, model, a, b):
        if (a, b) in self.varmap:
            return self.varmap[(a, b)] in model
        return -self.varmap[(b, a)] not in model and self.varmap[(b, a)] not in model


def run(name, offsets, base, kmin=False, stepmin=None, topvalmin=None,
        blocked=True, show_backbone=True, note=""):
    S = OrderSAT(offsets)
    if blocked:
        S.add_blocked4()
    S.add_base(base)
    if kmin:
        S.add_kmin(base[2])
    if stepmin is not None:
        S.add_stepmin_lt(stepmin)
    if topvalmin is not None:
        S.add_topvalmin(topvalmin)
    sat = S.solve()
    print(f"[{name}] offsets={offsets[0]}..{offsets[-1]} (n={len(offsets)}) "
          f"base={base} kmin={kmin} stepmin={stepmin} topvalmin={topvalmin} "
          f"=> {'SAT' if sat else 'UNSAT'}  {note}")
    if sat and show_backbone:
        bb = S.backbone()
        ax = set()
        # axioms we already know: base relations + their transitive hull is small;
        # just report everything, flagging the base ones.
        base_rel = {(base[0], base[1]), (base[1], base[2]), (base[0], base[2])}
        extra = [r for r in bb if r not in base_rel]
        print(f"    backbone: {len(bb)} forced relations, "
              f"{len(extra)} beyond the base triple:")
        for a, b in sorted(extra):
            print(f"      P({a:+d}) < P({b:+d})")
        m = S.one_model()
        print(f"    sample model (position order of offsets): {m}")
    return sat


if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    if which in ("all", "grid"):
        print("=== E1: d-grid windows, offsets m (value x+m*d), valid for EVERY d>=1 "
              "===")
        run("grid.kmin.M9", list(range(0, 10)), (0, 1, 2), kmin=True)
        run("grid.kmin.M12", list(range(0, 13)), (0, 1, 2), kmin=True,
            show_backbone=False)
        run("grid.kmin.neg4.M9", list(range(-4, 10)), (0, 1, 2), kmin=True,
            note="[assumes x > 4d]")

    if which in ("all", "interval"):
        print("=== E2: interval windows (unit=1), base step d concrete ===")
        run("int.d1.kmin.C10", list(range(0, 11)), (0, 1, 2), kmin=True)
        run("int.d1.kmin.A4C8", list(range(-4, 9)), (0, 1, 2), kmin=True,
            note="[assumes x > 4]")
        run("int.d2.kmin+stepmin.C12", list(range(0, 13)), (0, 2, 4), kmin=True,
            stepmin=2, note="[case: minimal STEP is 2, lex (d,k) minimal]")
        run("int.d2.kmin+stepmin.neg", list(range(-4, 13)), (0, 2, 4), kmin=True,
            stepmin=2, note="[assumes x > 4]", show_backbone=False)
        run("int.d3.kmin+stepmin.C15", list(range(0, 16)), (0, 3, 6), kmin=True,
            stepmin=3, note="[case: minimal STEP is 3]", show_backbone=False)
        run("int.d1.topvalmin.A6C8", list(range(-6, 9)), (0, 1, 2), kmin=True,
            topvalmin=2, note="[minimal top value AND then minimal top position; "
            "assumes x > 6]")

    if which in ("all", "absolute"):
        print("=== E3: absolute windows [1..W]: base pinned at concrete (x,d), "
              "boundary effects included ===")
        W = 12
        offs = list(range(1, W + 1))     # offsets ARE values here (x pinned = value)
        n_unsat = 0
        for d in range(1, (W - 1) // 2 + 1):
            for x in range(1, W - 2 * d + 1):
                sat = run(f"abs.x{x}.d{d}", offs, (x, x + d, x + 2 * d), kmin=True,
                          show_backbone=False)
                n_unsat += (0 if sat else 1)
        print(f"absolute windows: {n_unsat} UNSAT cases out of the box "
              f"(UNSAT would refute minimal triple = (x,d) globally)")
