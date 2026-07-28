"""drup_check.py -- self-contained forward DRAT proof checker (RUP + RAT-on-pivot).

Checks that every added lemma of the proof is either a reverse-unit-propagation
consequence of the current clause database, or has the resolution-asymmetric-tautology
property on its first literal (the DRAT pivot), and that the empty clause is finally
derived.  This is strictly stronger certification than "two solvers agree": the
refutation is re-derived independently of either solver's search.

Deletions are APPLIED, i.e. this checks the DRAT trace exactly as emitted.
Cadical's proofs contain genuine RAT lemmas (bounded variable elimination), so the
RAT branch is exercised; the count of RAT lemmas is reported.
"""

import sys


def parse(path):
    steps = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line[0] == "d":
                lits = [int(x) for x in line[1:].split()]
                assert lits[-1] == 0
                steps.append(("d", tuple(lits[:-1])))
            else:
                lits = [int(x) for x in line.split()]
                assert lits[-1] == 0
                steps.append(("a", tuple(lits[:-1])))
    return steps


class DB:
    def __init__(self, clauses):
        self.clauses = {}
        self.next_id = 0
        self.occ = {}
        for c in clauses:
            self.add(tuple(c))

    def add(self, c):
        i = self.next_id
        self.next_id += 1
        self.clauses[i] = c
        for l in c:
            self.occ.setdefault(l, set()).add(i)
        return i

    def remove(self, c):
        # remove one clause equal (as a multiset of literals, order-insensitive) to c
        cs = frozenset(c)
        if not c:
            return False
        for i in list(self.occ.get(c[0], ())):
            if frozenset(self.clauses[i]) == cs:
                for l in self.clauses[i]:
                    self.occ[l].discard(i)
                del self.clauses[i]
                return True
        return False

    def propagate(self, assign):
        """Unit propagation from `assign` (dict lit->True meaning literal satisfied).
        Returns True if a conflict is derived."""
        trail = [l for l in assign]
        qi = 0
        while qi < len(trail):
            l = trail[qi]; qi += 1
            for i in list(self.occ.get(-l, ())):
                c = self.clauses.get(i)
                if c is None:
                    continue
                unassigned = None
                sat = False
                cnt = 0
                for m in c:
                    if m in assign:
                        sat = True
                        break
                    if -m in assign:
                        continue
                    cnt += 1
                    unassigned = m
                    if cnt > 1:
                        break
                if sat:
                    continue
                if cnt == 0:
                    return True
                if cnt == 1:
                    assign[unassigned] = True
                    trail.append(unassigned)
        return False


def is_rup(db, c):
    assign = {}
    for l in c:
        if l in assign:
            continue
        if -l in assign:          # c is a tautology
            return True
        assign[-l] = True
    return db.propagate(assign)


def is_rat(db, c):
    """DRAT: RAT on the pivot = first literal of c."""
    if not c:
        return False
    p = c[0]
    cs = set(c)
    for i in list(db.occ.get(-p, ())):
        d = db.clauses.get(i)
        if d is None:
            continue
        res = list(cs | (set(d) - {-p}))
        if any(-x in cs or -x in set(d) - {-p} for x in res):
            # tautological resolvent: fine
            taut = False
            rs = set(res)
            for x in rs:
                if -x in rs:
                    taut = True
                    break
            if taut:
                continue
        if not is_rup(db, tuple(res)):
            return False
    return True


def check(clauses, proof_path, verbose=True):
    db = DB(clauses)
    steps = parse(proof_path)
    n_add = n_del = n_rat = 0
    for k, (kind, c) in enumerate(steps):
        if kind == "d":
            db.remove(c)
            n_del += 1
            continue
        n_add += 1
        if not is_rup(db, c):
            if not is_rat(db, c):
                return False, f"lemma #{k} {c} is neither RUP nor RAT"
            n_rat += 1
        db.add(c)
        if not c:
            if verbose:
                print(f"  empty clause derived at step {k} "
                      f"({n_add} additions of which {n_rat} RAT, {n_del} deletions checked)")
            return True, "OK: empty clause is RUP"
    # some emitters omit the final empty clause; check that it is RUP now
    if not db.propagate({}):
        return False, "proof ended without deriving the empty clause (and {} is not RUP)"
    if verbose:
        print(f"  final formula propagates to conflict "
              f"({n_add} additions of which {n_rat} RAT, {n_del} deletions checked)")
    return True, "OK: empty clause RUP at end of proof"


if __name__ == "__main__":
    from fractions import Fraction
    sys.path.insert(0, "/home/user/erdos/experiments")
    sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
    from certify_unsat import instance
    for a in sys.argv[1:]:
        spec, path = a.split("=")
        C_s, N_s = spec.split("@")
        C, N = Fraction(C_s), int(N_s)
        cl, pool, var, pin = instance(N, C)
        ok, msg = check(cl, path)
        print(f"C={C} N={N}: DRUP check -> {ok}  ({msg})", flush=True)
