"""eager.py -- independent EAGER re-verification of the class-architecture UNSATs.

Second encoding (not CEGAR) and second/third solver, per the project's verification
standard.

Encoding.  For a class function c on [1..N]: 'u before w' is a CONSTANT whenever
c(u) != c(w) (classes are emitted in increasing index order), and a Boolean variable
x_{u,w} (u<w) when c(u) == c(w).  Transitivity is needed ONLY for triples lying in a
single class: if a triple meets two different classes, the two cross-class relations are
already consistent with the total order on classes, so no transitivity clause can be
violated.  (Proof: with z in a class strictly below/above the class of u,w, the relations
z<u, z<w (resp. u<z, w<z) hold simultaneously, which is transitively consistent with
either value of x_{u,w}.)  So the eager encoding is EXACT.

Constraints: for every 4-AP (x, x+e, x+2e, x+3e) inside [1..N], forbid all three
consecutive 'before' relations (increasing) and all three 'after' relations (decreasing).

A SAT model is decoded and re-verified with the trusted experiments/apcheck.py.
"""

import sys, time, itertools
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
from apcheck import has_monotone_kap_pos                             # noqa: E402
from arch import blk                                                 # noqa: E402


def build_cnf(N, cfun):
    C = {v: cfun(v) for v in range(1, N + 1)}
    vid = {}

    def var(u, w):                      # u < w, same class
        k = (u, w)
        if k not in vid:
            vid[k] = len(vid) + 1
        return vid[k]

    def before(u, w):                   # u < w
        if C[u] < C[w]:
            return True
        if C[u] > C[w]:
            return False
        return var(u, w)

    # make sure all same-class variables exist (needed for transitivity)
    byclass = {}
    for v in range(1, N + 1):
        byclass.setdefault(C[v], []).append(v)
    for j, mem in byclass.items():
        for u, w in itertools.combinations(sorted(mem), 2):
            var(u, w)

    cnf = []
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            lits = [before(x + k * e, x + (k + 1) * e) for k in range(3)]
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

    # transitivity inside each class (both directions of the triple)
    for j, mem in byclass.items():
        mem = sorted(mem)
        for u, w, z in itertools.combinations(mem, 3):
            a, b, d = var(u, w), var(w, z), var(u, z)
            cnf.append([-a, -b, d])          # u<w & w<z -> u<z
            cnf.append([a, b, -d])           # w<u & z<w -> z<u
    return cnf, vid, None


def decode(N, cfun, model, vid):
    import functools
    C = {v: cfun(v) for v in range(1, N + 1)}
    ms = set(model)

    def order_of(u, w):                 # u < w
        if C[u] != C[w]:
            return C[u] < C[w]
        return vid[(u, w)] in ms

    def cmp(u, w):
        if u == w:
            return 0
        b = order_of(u, w) if u < w else (not order_of(w, u))
        return -1 if b else 1
    return sorted(range(1, N + 1), key=functools.cmp_to_key(cmp))


def run(N, cfun, tag, solvers=('cadical195', 'glucose4', 'minisat22')):
    from pysat.solvers import Solver
    cnf, vid, forced = build_cnf(N, cfun)
    if forced:
        print(f"{tag} N={N}: {forced[0]} at (x,e)=({forced[1]},{forced[2]})")
        return forced[0]
    verdicts = []
    for sname in solvers:
        t0 = time.time()
        with Solver(name=sname, bootstrap_with=cnf) as S:
            sat = S.solve()
            mdl = S.get_model() if sat else None
        dt = time.time() - t0
        v = 'SAT' if sat else 'UNSAT'
        verdicts.append(v)
        extra = ""
        if sat:
            perm = decode(N, cfun, mdl, vid)
            assert sorted(perm) == list(range(1, N + 1))
            good = not has_monotone_kap_pos(perm, 4)
            extra = f"  (model re-verified 4-AP-free: {good})"
            assert good
        print(f"{tag} N={N} [{sname}]: {v} ({dt:.1f}s, {len(cnf)} clauses, "
              f"{len(vid)} vars){extra}", flush=True)
    assert len(set(verdicts)) == 1, ("SOLVERS DISAGREE", tag, N, verdicts)
    return verdicts[0]


def head_class(b, s_of_m, K_of_m):
    def c(v):
        m = blk(v, b)
        return m + (K_of_m(m) if v < b ** m + s_of_m(m) else 0)
    return c


if __name__ == "__main__":
    cases = [
        ("HEAD(3,s=m+1,K=m)", head_class(3, lambda m: m + 1, lambda m: m), [60, 90, 95, 100]),
        ("HEAD(3,s=m+1,K=1)", head_class(3, lambda m: m + 1, lambda m: 1), [60, 100]),
        ("HEAD(3,s=2m+2,K=m)", head_class(3, lambda m: 2 * m + 2, lambda m: m), [60, 100]),
        ("HEAD(5,s=m+1,K=m)", head_class(5, lambda m: m + 1, lambda m: m), [100, 160]),
        # controls: route R20's certified verdicts
        ("CLS(3,a) [R20 control]", lambda v: blk(v, 3) + (lambda n: len(bin(n)) - len(bin(n).rstrip('0')))(v), [160, 250]),
    ]
    for tag, cf, Ns in cases:
        for N in Ns:
            run(N, cf, tag)
