"""sat.py -- SAT encoding of "monotone k-AP-free permutation of [1..N]" plus
the head-window invariant m_k^{(K)}(N).

Order variables: y[u][v] (u<v) is TRUE iff p(u) < p(v)  (u occurs before v).
Total order axioms on triples u<v<w:
    (~y_uv | ~y_vw |  y_uw)     forbids the cycle u<v<w<u
    ( y_uv |  y_vw | ~y_uw)     forbids the cycle u>v>w>u
AP axioms (Prop 1 of REPORT.md): a monotone K-AP with base x, difference d exists
iff the K-1 consecutive signs sign(p(x+(j+1)d) - p(x+jd)) are all equal.  So for
each (x,d) with x+(K-1)d <= N forbid "all +" and "all -":
    (~y_1 | ~y_2 | ... )   and   (y_1 | y_2 | ...)
where y_j is the variable for the pair (x+(j-1)d, x+jd).

Head-window constraint "the first k values are all <= M":
    for every v > M:  #{u <= M : p(u) < p(v)} >= k.
"""

import sys
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

sys.path.insert(0, '/home/user/erdos/experiments')


def build_cnf(N, K=4):
    pool = IDPool()

    def y(u, v):                      # p(u) < p(v)
        assert u != v
        return pool.id(('y', u, v)) if u < v else -pool.id(('y', v, u))

    cnf = CNF()
    for u in range(1, N + 1):
        for v in range(u + 1, N + 1):
            for w in range(v + 1, N + 1):
                a, b, c = y(u, v), y(v, w), y(u, w)
                cnf.append([-a, -b, c])
                cnf.append([a, b, -c])
    naps = 0
    for d in range(1, (N - 1) // (K - 1) + 1):
        for x in range(1, N - (K - 1) * d + 1):
            lits = [y(x + j * d, x + (j + 1) * d) for j in range(K - 1)]
            cnf.append([-l for l in lits])
            cnf.append(list(lits))
            naps += 1
    return cnf, pool, y, naps


def head_window_cnf(N, M, k, pool, y):
    """CNF forcing: the first k values in position order are all <= M."""
    extra = CNF()
    for v in range(M + 1, N + 1):
        lits = [y(u, v) for u in range(1, M + 1)]
        enc = CardEnc.atleast(lits=lits, bound=k, vpool=pool,
                              encoding=EncType.seqcounter)
        extra.extend(enc.clauses)
    return extra


def model_to_perm(model, N, y):
    """Decode a model into the permutation (values in position order)."""
    val = set(l for l in model if l > 0)

    def before(u, v):
        lit = y(u, v)
        return (lit in val) if lit > 0 else (-lit not in val)

    import functools
    order = sorted(range(1, N + 1),
                   key=functools.cmp_to_key(lambda u, v: -1 if before(u, v) else 1))
    return order


def solve(N, K=4, M=None, k=None, solver='cd15', return_perm=True):
    """Is there a monotone-K-AP-free permutation of [1..N] whose first k values
    are all <= M?  (M=None: no head constraint.)  Returns perm or None."""
    cnf, pool, y, _ = build_cnf(N, K)
    if M is not None:
        cnf.extend(head_window_cnf(N, M, k, pool, y).clauses)
    with Solver(name=solver, bootstrap_with=cnf.clauses) as s:
        if not s.solve():
            return None
        return model_to_perm(s.get_model(), N, y) if return_perm else True


def m_k(N, k, K=4, lo=None, hi=None, solver='cd15', verbose=False):
    """m_k^{(K)}(N) = min over monotone-K-AP-free perms of [1..N] of max of the
    first k values.  Returns (value, witness_perm)."""
    cnf, pool, y, _ = build_cnf(N, K)
    base = cnf.clauses
    lo = lo or k
    hi = hi or N
    best = None
    M = lo
    while M <= hi:
        c = CNF(from_clauses=base)
        c.extend(head_window_cnf(N, M, k, pool, y).clauses)
        with Solver(name=solver, bootstrap_with=c.clauses) as s:
            ok = s.solve()
            if ok:
                best = (M, model_to_perm(s.get_model(), N, y))
                break
        if verbose:
            print(f"   N={N} k={k}: M={M} UNSAT", flush=True)
        M += 1
    return best
