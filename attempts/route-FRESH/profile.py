"""profile.py -- the profile reformulation (Theorem 3 of REPORT.md).

For a permutation a of  N  put  n_L := max_{v<=L} p(v)  (time by which [1..L] is
all placed).  n_. is non-decreasing, n_L >= L, finite for every L.

THEOREM (proved in REPORT.md).  A monotone-K-AP-free permutation of  N  exists
  <=>  there is a finite non-decreasing profile (n_L)_{L>=1}, n_L >= L, such that
       for EVERY N there is a monotone-K-AP-free permutation sigma of [1..N] with
       rank_sigma(v) <= n_v  for all v <= N.
(=>) restrict.  (<=) Koenig on the finitely-branching restriction tree of
profile-respecting permutations; the profile bound forces every rank to
stabilise, i.e. order type omega.

So: compute, for each N, the lexicographically minimal profile prefix
(n_1,...,n_{L0}).  It is lex-non-decreasing in N.  If any coordinate -> oo the
answer to Erdos 196 is YES.  If the whole prefix stabilises, that is a blueprint
for a counterexample.

Incremental encoding: one ITotalizer per value v over the literals
{ y(u,v) : u != v } (which count the predecessors of v), so rank(v) <= n is the
single assumption -tot[v].rhs[n-1].
"""

from pysat.formula import CNF
from pysat.card import ITotalizer
from pysat.solvers import Solver
from sat import build_cnf, model_to_perm


class ProfileSolver:
    def __init__(self, N, K=4, L0=None, solver='cd15'):
        self.N, self.K = N, K
        self.L0 = L0 or N
        cnf, pool, y, _ = build_cnf(N, K)
        self.y = y
        top = pool.top
        self.tot = {}
        clauses = list(cnf.clauses)
        for v in range(1, self.L0 + 1):
            lits = [y(u, v) for u in range(1, N + 1) if u != v]
            it = ITotalizer(lits=lits, ubound=N - 1, top_id=top)
            top = it.top_id
            self.tot[v] = it
            clauses.extend(it.cnf.clauses)
        self.S = Solver(name=solver, bootstrap_with=clauses)

    def assumptions(self, prof):
        """prof: dict v -> n meaning rank(v) <= n."""
        a = []
        for v, n in prof.items():
            if n < self.N:
                a.append(-self.tot[v].rhs[n - 1])
        return a

    def sat(self, prof):
        return self.S.solve(assumptions=self.assumptions(prof))

    def perm(self):
        return model_to_perm(self.S.get_model(), self.N, self.y)

    def lexmin_profile(self, L0=None, verbose=False):
        """Lexicographically minimal (n_1,...,n_{L0}); n_v >= v enforced implicitly."""
        L0 = L0 or self.L0
        prof = {}
        for v in range(1, L0 + 1):
            n = max(v, prof.get(v - 1, 1))
            while True:
                prof[v] = n
                if self.sat(prof):
                    break
                n += 1
                if n > self.N:
                    prof[v] = None
                    return prof
            if verbose:
                print(f"      n_{v} = {n}", flush=True)
        return prof

    def close(self):
        self.S.delete()
        for it in self.tot.values():
            it.delete()
