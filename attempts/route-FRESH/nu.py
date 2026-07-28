"""nu.py -- the invariant nu_L(N).

nu_L(N) := min over monotone-K-AP-free permutations sigma of [1..N] of
           max_{v<=L} rank_sigma(v)      (the time by which all of [1..L] is placed).

FACTS (proved in REPORT.md):
  * nu_L(N) is non-decreasing in N  (delete the value N: ranks only drop).
  * If a monotone-K-AP-free permutation a of  N  exists then nu_L(N) <= n_L :=
    max_{v<=L} p(v) < oo  for EVERY N.  So nu_L(.) bounded for every L.
  * Hence: if nu_L(N) -> oo for a single L, every permutation of N has a
    monotone K-AP.
Encoding: rank(v) <= n  <=>  #{u != v : p(u)<p(v)} <= n-1.
"""
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
from sat import build_cnf, model_to_perm

def nu(L, N, K=4, solver='cd15', nmax=None, verbose=False):
    cnf, pool, y, _ = build_cnf(N, K)
    base = cnf.clauses
    nmax = nmax or N
    for n in range(L, nmax+1):
        c = CNF(from_clauses=base)
        for v in range(1, L+1):
            lits = [y(u,v) for u in range(1,N+1) if u != v]
            enc = CardEnc.atmost(lits=lits, bound=n-1, vpool=pool, encoding=EncType.seqcounter)
            c.extend(enc.clauses)
        with Solver(name=solver, bootstrap_with=c.clauses) as S:
            if S.solve():
                return n, model_to_perm(S.get_model(), N, y)
        if verbose: print(f"    L={L} N={N} n={n} UNSAT", flush=True)
    return None, None
