"""
A_combinatorial.py

CLAIM TESTED: for a given L, is the *parity-split bookkeeping alone* already contradictory?
That is: forget the residues entirely and ask only whether the moduli D_E(L) can be split
into two disjoint families M_0, M_1 (the classes with even / with odd residue) obeying

  (C1) GLOBAL density      sum_{n in M_0 u M_1} 1/n  >  1
  (C2) HALF density        sum_{n in M_c} 2/n > 1     for c = 0,1
                           (Lemma A1: M_c must cover one whole parity class; strict by
                            Davenport-Mirsky-Newman-Rado)
  (C3) OVERLAP  (Lemma A2) for every T subset M_c whose halved moduli m = n/2 are PAIRWISE
                           COPRIME,
                              sum_{m in T} 1/m - 1 + prod_{m in T} (1 - 1/m)  <=  X_c
                           where X_c = sum_{n in M_c} 2/n - 1 is the excess of half c.
                           Combined with (C2) for the OTHER half and disjointness,
                              X_c  <  2 B_E(L) - 2 ,
                           which for the tight L is a very small number.

If this bookkeeping is infeasible then NO covering system with distinct moduli in E has
lcm dividing L -- a proof that needs no search over residues at all.

Method: a small SAT instance over 2|D_E(L)| Booleans P[n][c] = "n is used in half c",
with (C3) as clauses and (C1),(C2) handled EXACTLY by CEGAR: whenever the solver returns a
split whose exact reciprocal sums violate a density requirement, the (valid) clause
"half c must use some modulus outside the returned set" is added and the solve repeats.
Termination is guaranteed because each refinement clause removes at least one model.

CONCLUSION: printed per L.  "INFEASIBLE" = proof of UNSAT for that L.
"""
import sys, os
from fractions import Fraction
from itertools import combinations
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import D_E, budget
from A_sat_cover import overlap_sets, minimal_hitting_sets


def analyse(L, verbose=True, smax=5, pool=22, mode="full"):
    d = D_E(L)
    B = budget(d)
    glob = Fraction(1) if mode == "full" else Fraction(L - 1, L)
    # relaxed mode: the uncovered residue 0 is EVEN, so the odd half is still a full
    # covering while the even half may miss one point of Z/(L/2); both excess bounds
    # loosen by exactly 2/L.
    slack = Fraction(0) if mode == "full" else Fraction(2, L)
    half = [Fraction(1, 2) - slack / 2, Fraction(1, 2)]
    if B <= glob:
        return "UNSAT(density)", None
    k = len(d)
    hm = [n // 2 for n in d]
    Xbound = 2 * B - 2 + slack              # strict upper bound on each half's excess

    from pysat.solvers import Solver
    s = Solver(name="cadical153")
    # P[i][c] : modulus d[i] used in half c
    def P(i, c):
        return 2 * i + c + 1
    for i in range(k):
        s.add_clause([-P(i, 0), -P(i, 1)])

    # (C3) overlap clauses
    T_sets = overlap_sets(hm, Xbound, pool=pool, smax=smax, maxsets=20000)
    pos = {m: i for i, m in enumerate(hm)}
    for T in T_sets:
        for c in (0, 1):
            s.add_clause([-P(pos[m], c) for m in T])
    if verbose:
        print(f"  L={L}: |D_E|={k}, B_E={float(B):.6f}, excess bound {float(Xbound):.6f}, "
              f"{len(T_sets)} overlap clauses")

    # (C1)/(C2) seeded with minimal hitting-set clauses, then refined exactly by CEGAR.
    idx = {n: i for i, n in enumerate(d)}
    for S in minimal_hitting_sets(d, B - glob, smax=4, pool=min(k, 26)):
        s.add_clause([P(idx[n], c) for n in S for c in (0, 1)])
    for c in (0, 1):
        for S in minimal_hitting_sets(d, B - half[c], smax=6, pool=min(k, 18),
                                      maxsets=4000):
            s.add_clause([P(idx[n], c) for n in S])

    def maximalise(M, cap):
        """Grow M by the largest available moduli while its 1/n-sum stays <= cap.
        The blocking clause built from a MAXIMAL such set is much stronger."""
        M = set(M)
        tot = budget(sorted(M))
        for n in reversed(d):
            if n in M:
                continue
            if tot + Fraction(1, n) <= cap:
                M.add(n)
                tot += Fraction(1, n)
        return M

    rounds = 0
    while True:
        rounds += 1
        if not s.solve():
            return "INFEASIBLE", rounds
        model = set(l for l in s.get_model() if l > 0)
        M = [[], []]
        for i, n in enumerate(d):
            for c in (0, 1):
                if P(i, c) in model:
                    M[c].append(n)
        bad = False
        for c in (0, 1):
            if budget(M[c]) <= half[c]:        # half c fails (C2)
                Mx = maximalise(M[c], half[c])
                s.add_clause([P(i, c) for i, n in enumerate(d) if n not in Mx])
                bad = True
        if budget(M[0] + M[1]) <= glob:        # (C1)
            Mx = maximalise(M[0] + M[1], glob)
            s.add_clause([P(i, c) for i, n in enumerate(d) if n not in Mx
                          for c in (0, 1)])
            bad = True
        if not bad:
            return "FEASIBLE", (rounds, sorted(M[0]), sorted(M[1]))
        if rounds > 200000:
            return "GAVE-UP", rounds


if __name__ == "__main__":
    Ls = [int(x) for x in sys.argv[1:]]
    if not Ls:
        Ls = [55440, 65520, 100800, 110880, 131040, 151200, 166320, 181440, 196560,
              201600, 205920, 221760, 226800, 231840, 241920, 257040, 262080, 277200,
              302400, 308880, 327600, 332640, 342720, 347760, 360360, 362880, 378000,
              388080, 393120]
    MODE = os.environ.get("A_MODE", "full")
    nproved = 0
    for L in Ls:
        v, info = analyse(L, mode=MODE)
        if v == "INFEASIBLE":
            nproved += 1
            print(f"  ==> L={L}: PROVED UNSAT combinatorially "
                  f"(no residue search needed), {info} CEGAR rounds")
        elif v == "FEASIBLE":
            r, M0, M1 = info
            print(f"  ==> L={L}: bookkeeping feasible after {r} rounds; e.g.")
            print(f"        M0 = {M0}")
            print(f"        M1 = {M1}")
        else:
            print(f"  ==> L={L}: {v}")
        sys.stdout.flush()
    print(f"\n{nproved} / {len(Ls)} values of L proved UNSAT by bookkeeping alone")
