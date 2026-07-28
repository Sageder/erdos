"""dratcert.py — theorem-grade certificate for: Sigma_3 (base 3, D_3=[27,81)) is UNSAT.

Pipeline:
 1. Emit the CNF (order variables + transitivity + constraint clauses) as DIMACS
    (sigma3_base3.cnf).  Same constraint generator as singleblock.py (shared code).
 2. Run Cadical (pysat Cadical103) with DRUP proof logging; save sigma3_base3.drat.
 3. Verify the proof with an INDEPENDENT, self-contained RUP+deletion checker
    implemented below (no solver trust): each proof clause must follow from the
    accumulated formula by reverse unit propagation; deletions honored; the proof
    must derive the empty clause.  The checker is exact and fails loudly on any
    step it cannot certify (incl. any non-RUP/RAT step).
Result printed at the end; artifacts left in this directory.
"""

import sys
from itertools import combinations

sys.path.insert(0, "/home/user/erdos/attempts/route-R3")
from singleblock import constraints_for_block

L, b = 27, 3


def build_cnf():
    aps4, g3, forced = constraints_for_block(L, b)
    elems = list(range(L, b * L))
    idx = {}

    def var(u, w):  # u<w
        if (u, w) not in idx:
            idx[(u, w)] = len(idx) + 1
        return idx[(u, w)]

    def lt(u, w):
        return var(u, w) if u < w else -var(w, u)

    cls = []
    for u, v, w in combinations(elems, 3):
        a, c, e = lt(u, v), lt(v, w), lt(u, w)
        cls.append([-a, -c, e])
        cls.append([a, c, -e])
    for (u, d) in aps4:
        t = [u + k * d for k in range(4)]
        cls.append([-lt(t[k], t[k + 1]) for k in range(3)])
        cls.append([lt(t[k], t[k + 1]) for k in range(3)])
    for (u, d) in g3:
        cls.append([-lt(u, u + d), -lt(u + d, u + 2 * d)])
    for (u, d, _) in forced:
        cls.append([-lt(u, u + d)])
    return cls, len(idx)


def write_dimacs(cls, nv, path):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {len(cls)}\n")
        for c in cls:
            f.write(" ".join(map(str, c)) + " 0\n")


# ---------------- independent RUP + deletion checker ----------------

class RupChecker:
    """Clause database with two-watched-literal unit propagation.
    check_rup(clause): assume negation, propagate; certified iff conflict."""

    def __init__(self, clauses):
        self.clauses = []      # list of lists (active ones referenced by watches)
        self.watches = {}      # literal -> set of clause indices watching it
        self.active = []
        self.units = []
        self.unit_cis = []     # indices of clauses of length <= 1 (incl. inactive)
        for c in clauses:
            self.add_clause(list(c))

    def _watch(self, lit, ci):
        self.watches.setdefault(lit, set()).add(ci)

    def add_clause(self, c):
        ci = len(self.clauses)
        self.clauses.append(c)
        self.active.append(True)
        if len(c) == 0:
            self.units.append(None)  # empty clause: formula already UNSAT
        elif len(c) == 1:
            self.units.append(c[0])
        else:
            self._watch(c[0], ci)
            self._watch(c[1], ci)
            self.units.append(0)
        return ci

    def delete_clause(self, c):
        # linear scan over candidate indices via watches (or full scan fallback)
        key = sorted(c)
        cand = None
        pools = [self.watches.get(c[0], set()), self.watches.get(-c[0], set())] \
            if c else []
        seen = set()
        for pool in pools:
            for ci in pool:
                if self.active[ci] and sorted(self.clauses[ci]) == key:
                    cand = ci
                    break
            if cand is not None:
                break
        if cand is None:
            for ci in range(len(self.clauses)):
                if self.active[ci] and sorted(self.clauses[ci]) == key:
                    cand = ci
                    break
        if cand is not None:
            self.active[cand] = False
        # deleting a clause not present is harmless (weakens the db)

    def propagate(self, assumed):
        """assumed: iterable of literals set true. Returns True iff conflict reached."""
        val = {}
        trail = []

        def set_lit(l):
            if val.get(l) is True:
                return None          # already true: nothing to do
            if val.get(l) is False:
                return "conflict"    # already false: conflict
            val[l] = True
            val[-l] = False
            trail.append(l)
            return None

        for l in assumed:
            r = set_lit(l)
            if r == "conflict":
                return True
        for ci, u in enumerate(self.units):
            if not self.active[ci]:
                continue
            c = self.clauses[ci]
            if len(c) == 0:
                return True
            if len(c) == 1:
                r = set_lit(c[0])
                if r == "conflict":
                    return True
        head = 0
        while head < len(trail):
            l = trail[head]
            head += 1
            falsified = -l
            for ci in list(self.watches.get(falsified, ())):
                if not self.active[ci]:
                    continue
                c = self.clauses[ci]
                # find replacement watch
                w1, w2 = c[0], c[1]
                other = w2 if w1 == falsified else w1
                repl = None
                for lit in c:
                    if lit != falsified and lit != other and val.get(lit) is not False:
                        repl = lit
                        break
                if repl is not None:
                    # move watch
                    if c[0] == falsified:
                        c[0] = repl
                    else:
                        c[1] = repl
                    self.watches[falsified].discard(ci)
                    self._watch(repl, ci)
                    continue
                # no replacement: clause is unit or conflicting on `other`
                if val.get(other) is True:
                    continue
                if val.get(other) is False:
                    return True
                r = set_lit(other)
                if r == "conflict":
                    return True
        return False

    def check_rup(self, c):
        return self.propagate([-l for l in c])


def verify(cnf, proof_lines):
    ck = RupChecker(cnf)
    n_add = n_del = 0
    for ln in proof_lines:
        ln = ln.strip()
        if not ln or ln.startswith("c"):
            continue
        if ln.startswith("d "):
            lits = list(map(int, ln[2:].split()))
            assert lits[-1] == 0
            ck.delete_clause(lits[:-1])
            n_del += 1
            continue
        lits = list(map(int, ln.split()))
        assert lits[-1] == 0
        c = lits[:-1]
        if not ck.check_rup(c):
            return False, f"non-RUP step after {n_add} additions: {c[:8]}..."
        ck.add_clause(c)
        n_add += 1
        if not c:
            return True, f"empty clause derived after {n_add} additions, {n_del} deletions"
    return False, "proof ended without empty clause"


def main():
    cls, nv = build_cnf()
    write_dimacs(cls, nv, "/home/user/erdos/attempts/route-R3/sigma3_base3.cnf")
    print(f"CNF: {nv} vars, {len(cls)} clauses")

    from pysat.solvers import Cadical103
    s = Cadical103(bootstrap_with=cls, with_proof=True)
    ok = s.solve()
    assert not ok, "expected UNSAT"
    proof = s.get_proof()
    s.delete()
    with open("/home/user/erdos/attempts/route-R3/sigma3_base3.drat", "w") as f:
        f.write("\n".join(proof) + "\n")
    print(f"Cadical103: UNSAT, proof with {len(proof)} lines saved")

    good, msg = verify(cls, proof)
    print(("DRAT/RUP VERIFIED: " if good else "VERIFY FAILED: ") + msg)
    assert good


if __name__ == "__main__":
    main()
