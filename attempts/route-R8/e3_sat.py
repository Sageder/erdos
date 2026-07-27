"""e3_sat.py — SAT search for within-block arrangements making the dyadic-block N-permutation
monotone-5-AP-free on the prefix [1 .. 2^(M+1)-1].

Model: macro order B_0 B_1 ... B_M (B_m = [2^m, 2^(m+1))).  Cross-block position order equals
value order (increasing).  Variables x_{u,v} (u<v, same block): "u placed before v".
Transitivity clauses within each block.  For each AP (t,d) with t+4d <= N:
  increasing clause: some consecutive same-block pair reversed  (if none: UNSAT clause -> the
      macro layout would be refuted; lemma L2 says among the last four terms two adjacent AP
      terms share a block, so the clause is nonempty unless the pair involves t itself etc.)
  decreasing clause: only if all 5 terms in one block: some consecutive pair in increasing order.
Also generalizes to k-APs via K parameter.

Outputs a satisfying tau_m per block, prints them, and independently verifies the assembled
permutation with the vectorized checker (exact).
"""

import sys
import os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "experiments"))
from fastcheck import has_kap_perm_np  # noqa: E402

from pysat.solvers import Cadical153  # noqa: E402
from pysat.formula import IDPool  # noqa: E402


def block_of(v):
    return v.bit_length() - 1


def solve_prefix(M, K=5, verbose=True, extra_assumptions=None, forbid=None):
    N = 2 ** (M + 1) - 1
    pool = IDPool()

    def var(u, v):
        """u < v, same block: positive literal means 'u before v'."""
        assert u < v and block_of(u) == block_of(v)
        return pool.id(("x", u, v))

    def before_lit(u, v):
        """literal expressing pos(u) < pos(v); None if cross-block (then it's the constant
        u < v)."""
        if block_of(u) == block_of(v):
            return var(u, v) if u < v else -var(v, u)
        return None  # constant: True iff u < v

    cnf = []
    # transitivity within each block
    for m in range(M + 1):
        blk = list(range(2 ** m, 2 ** (m + 1)))
        for a, b, c in combinations(blk, 3):
            # a<b<c. x_ab & x_bc -> x_ac ; ~x_ab & ~x_bc -> ~x_ac
            cnf.append([-var(a, b), -var(b, c), var(a, c)])
            cnf.append([var(a, b), var(b, c), -var(a, c)])

    unsat_ap = []
    for d in range(1, (N - 1) // (K - 1) + 1):
        for t in range(1, N - (K - 1) * d + 1):
            terms = [t + j * d for j in range(K)]
            # increasing: all consecutive pos comparisons '<' hold. cross pairs constant True.
            clause = []
            for j in range(K - 1):
                u, v = terms[j], terms[j + 1]
                lit = before_lit(u, v)
                if lit is not None:
                    clause.append(-lit)  # need some consecutive pair with pos(u)>pos(v)
            if not clause:
                unsat_ap.append((t, d, "inc"))
            else:
                cnf.append(clause)
            # decreasing: needs pos decreasing along increasing values read backwards:
            # pos(t) > pos(t+d) > ...; cross pairs make it False automatically.
            if block_of(terms[0]) == block_of(terms[-1]):
                clause = []
                for j in range(K - 1):
                    u, v = terms[j], terms[j + 1]
                    clause.append(before_lit(u, v))  # need some pos(u) < pos(v)
                cnf.append(clause)

    if unsat_ap:
        print(f"  M={M}: macro layout REFUTED outright; APs with no same-block consecutive "
              f"pair: {unsat_ap[:5]} ...")
        return None

    if forbid:
        for cl in forbid:
            cnf.append(cl)

    with Cadical153(bootstrap_with=cnf) as s:
        ok = s.solve(assumptions=extra_assumptions or [])
        if not ok:
            print(f"  M={M} K={K}: UNSAT  (no within-block arrangement exists for this macro)")
            return None
        model = set(l for l in s.get_model() if l > 0)

    taus = []
    for m in range(M + 1):
        blk = list(range(2 ** m, 2 ** (m + 1)))
        # sort block by the linear order defined by the model
        import functools

        def cmp(u, v):
            if u == v:
                return 0
            a, b = min(u, v), max(u, v)
            ub = var(a, b) in model  # a before b
            if (u < v) == ub:
                return -1
            return 1
        taus.append(sorted(blk, key=functools.cmp_to_key(cmp)))
    seq = [v for tau in taus for v in tau]
    assert sorted(seq) == list(range(1, N + 1))
    ok = not has_kap_perm_np(seq, K)
    if verbose:
        print(f"  M={M} K={K}: SAT; independent checker confirms 5-AP-free: {ok}")
        for m, tau in enumerate(taus):
            if m <= 6:
                print(f"    tau_{m}: {tau}")
    assert ok, "SAT model failed independent verification!"
    return taus


if __name__ == "__main__":
    for M in range(3, 8):
        solve_prefix(M, K=5)
