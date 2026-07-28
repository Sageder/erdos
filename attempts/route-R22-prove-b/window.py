"""window.py -- eager exact encoding of a class architecture over an ARBITRARY finite
value set (not necessarily an interval).

Only 4-APs whose four terms all lie in the set are constrained -- which is exactly right:
deleting values from a valid architecture leaves a valid sub-architecture, so UNSAT on a
subset is an impossibility statement for the whole architecture.

Transitivity is needed only for triples inside one class (a third value in a strictly
lower/higher class relates consistently to both members of any same-class pair), so the
encoding is exact.
"""

import itertools, functools, sys
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_general                          # noqa: E402


def build_cnf_set(vals, cfun):
    vals = sorted(vals)
    vset = set(vals)
    C = {v: cfun(v) for v in vals}
    vid = {}

    def var(u, w):
        k = (u, w)
        if k not in vid:
            vid[k] = len(vid) + 1
        return vid[k]

    byclass = {}
    for v in vals:
        byclass.setdefault(C[v], []).append(v)
    for j, mem in byclass.items():
        for u, w in itertools.combinations(sorted(mem), 2):
            var(u, w)

    def before(u, w):                    # u < w
        if C[u] < C[w]:
            return True
        if C[u] > C[w]:
            return False
        return var(u, w)

    cnf = []
    lo, hi = vals[0], vals[-1]
    for e in range(1, (hi - lo) // 3 + 1):
        for x in range(lo, hi - 3 * e + 1):
            terms = [x + k * e for k in range(4)]
            if not all(tt in vset for tt in terms):
                continue
            lits = [before(terms[k], terms[k + 1]) for k in range(3)]
            if all(l is not False for l in lits):
                cl = [-l for l in lits if l is not True]
                if not cl:
                    return None, None, ('FORCED-INC', x, e)
                cnf.append(cl)
            if all(l is not True for l in lits):
                cl = [l for l in lits if l is not False]
                if not cl:
                    return None, None, ('FORCED-DEC', x, e)
                cnf.append(cl)
    for j, mem in byclass.items():
        mem = sorted(mem)
        for u, w, z in itertools.combinations(mem, 3):
            a, b, d = var(u, w), var(w, z), var(u, z)
            cnf.append([-a, -b, d])
            cnf.append([a, b, -d])
    return cnf, vid, None


def decode_set(vals, cfun, model, vid):
    vals = sorted(vals)
    C = {v: cfun(v) for v in vals}
    ms = set(model)

    def order_of(u, w):
        if C[u] != C[w]:
            return C[u] < C[w]
        return vid[(u, w)] in ms

    def cmp(u, w):
        if u == w:
            return 0
        bb = order_of(u, w) if u < w else (not order_of(w, u))
        return -1 if bb else 1
    return sorted(vals, key=functools.cmp_to_key(cmp))


def verdict_set(vals, cfun, solvers=('cadical195', 'glucose4')):
    from pysat.solvers import Solver
    cnf, vid, forced = build_cnf_set(vals, cfun)
    if forced:
        return 'UNSAT', forced
    outs = []
    for s in solvers:
        with Solver(name=s, bootstrap_with=cnf) as S:
            sat = S.solve()
            mdl = S.get_model() if sat else None
        outs.append('SAT' if sat else 'UNSAT')
        if sat:
            seq = decode_set(vals, cfun, mdl, vid)
            assert not has_monotone_kap_general(seq, 4), "model is not an avoider!"
    assert len(set(outs)) == 1, ("SOLVERS DISAGREE", outs)
    return outs[0], None
