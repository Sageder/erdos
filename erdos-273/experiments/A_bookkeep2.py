"""
A_bookkeep2.py   -- strengthened residue-free obstruction for Erdos 273.

CLAIM TESTED: for a given L, decide whether the parity-split bookkeeping can be satisfied,
using the CONDITIONAL form of the overlap lemma (strictly stronger than A_combinatorial.py).

Setting (Lemma A1).  A covering system with distinct moduli in E, all dividing L, is the
same thing as two DISJOINT sets M_0, M_1 of H-moduli (m = n/2, m | Lh = L/2, 2m+1 prime),
each of which supports a covering of Z/Lh.

Lemma A2 (overlap).  For a covering family with moduli M and any T subset M whose elements
are PAIRWISE COPRIME,
        sum_{m in M} 1/m  -  1   >=   f(T) := sum_{m in T} 1/m - 1 + prod_{m in T}(1-1/m).
Proof: g(S) = sum_{m in S} 1/m - density(union) is monotone in S; g(M) = sum - 1 because
the union is all of Z; and for pairwise coprime T the union density is exactly
1 - prod (1 - 1/m) by CRT, whatever the residues are.

CONDITIONAL USE (this is the new part).  Fix a half c.  For every pairwise coprime
T subset M_c we get the *modulus-set-dependent* lower bound
        sum_{m in M_c} 1/m  >=  1 + f(T).
So the pair (T inside half c) forces half c to be RICH.  Encoded lazily: when the master
returns a candidate split whose half c contains such a T but is too poor, we add the valid
clause
        (some m in T is NOT in half c)  OR  (half c uses some modulus outside M'),
where M' is a maximal set with sum_{M'} 1/m < 1 + f(T).

Together with the global density bound (sum over all used > 1) and the plain half bound
(sum over each half > 1, strict by Davenport-Mirsky-Newman-Rado) this is decided exactly by
CEGAR.  INFEASIBLE  ==>  no covering system with distinct moduli in E has lcm dividing L,
with NO search over residues.

CONCLUSION: printed per L.
"""
import sys, os, time
from fractions import Fraction
from itertools import combinations
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import D_E, D_H, budget
from A_sat_cover import overlap_sets, minimal_hitting_sets


def f_of(T):
    s = sum(Fraction(1, m) for m in T)
    pr = Fraction(1)
    for m in T:
        pr *= Fraction(m - 1, m)
    return s - 1 + pr


def best_T(M, smax=4, pool=16):
    """Pairwise-coprime T subset M maximising f(T) (searched among the pool smallest)."""
    M = sorted(M)[:pool]
    best, bf = None, Fraction(-1)
    for size in range(2, smax + 1):
        for T in combinations(M, size):
            if not all(gcd(a, b) == 1 for a, b in combinations(T, 2)):
                continue
            v = f_of(T)
            if v > bf:
                bf, best = v, T
    return best, bf


def analyse(L, budget_s=600, verbose=True):
    Lh = L // 2
    D = D_H(Lh)
    assert [2 * m for m in D] == D_E(L)
    B = budget(D)                       # = B_H(Lh)
    k = len(D)
    if B <= 2:
        return "UNSAT(density)", 0
    from pysat.solvers import Solver
    s = Solver(name="cadical153")
    idx = {m: i for i, m in enumerate(D)}

    def P(i, c):
        return 2 * i + c + 1

    for i in range(k):
        s.add_clause([-P(i, 0), -P(i, 1)])
    for T in overlap_sets(D, B - 2, pool=min(k, 20), smax=4, maxsets=2000):
        for c in (0, 1):
            s.add_clause([-P(idx[m], c) for m in T])
    for S in minimal_hitting_sets(D, B - 1, smax=4, pool=min(k, 16), maxsets=250):
        for c in (0, 1):
            s.add_clause([P(idx[m], c) for m in S])

    def maximalise(M, cap):
        M = set(M)
        tot = budget(sorted(M)) if M else Fraction(0)
        for m in reversed(D):
            if m in M:
                continue
            if tot + Fraction(1, m) < cap:
                M.add(m)
                tot += Fraction(1, m)
        return M

    t0 = time.time()
    rounds = 0
    while True:
        if time.time() - t0 > budget_s:
            return "TIMEOUT", rounds
        rounds += 1
        if not s.solve():
            return "INFEASIBLE", rounds
        model = set(l for l in s.get_model() if l > 0)
        M = [[], []]
        for i, m in enumerate(D):
            for c in (0, 1):
                if P(i, c) in model:
                    M[c].append(m)
        bad = False
        for c in (0, 1):
            need = Fraction(1)
            T, ft = best_T(M[c]) if len(M[c]) >= 2 else (None, Fraction(-1))
            if T is not None and ft > 0:
                need = 1 + ft
            if budget(M[c]) < need or budget(M[c]) <= 1:
                cap = max(need, Fraction(1) + Fraction(1, 10 ** 9))
                Mx = maximalise(M[c], cap)
                cl = [P(i, c) for i, m in enumerate(D) if m not in Mx]
                if T is not None and budget(M[c]) >= 1:
                    cl = cl + [-P(idx[m], c) for m in T]
                s.add_clause(cl)
                bad = True
        if budget(M[0] + M[1]) <= 2:
            Mx = maximalise(M[0] + M[1], Fraction(2))
            s.add_clause([P(i, c) for i, m in enumerate(D) if m not in Mx
                          for c in (0, 1)])
            bad = True
        if not bad:
            return "FEASIBLE", (rounds, sorted(M[0]), sorted(M[1]))


if __name__ == "__main__":
    Ls = [int(x) for x in sys.argv[1:]] or [55440, 110880, 166320, 221760, 262080,
                                            277200, 327600, 332640, 388080, 393120]
    nproved = 0
    for L in Ls:
        t = time.time()
        v, info = analyse(L)
        if v == "INFEASIBLE":
            nproved += 1
            print(f"  ==> L={L}: PROVED UNSAT by strengthened bookkeeping "
                  f"({info} rounds, {time.time()-t:.1f}s)")
        elif v == "FEASIBLE":
            r, M0, M1 = info
            print(f"  ==> L={L}: still feasible after {r} rounds "
                  f"({time.time()-t:.1f}s); e.g. (H-moduli)")
            print(f"        M0 = {M0}\n        M1 = {M1}")
        else:
            print(f"  ==> L={L}: {v} ({info} rounds)")
        sys.stdout.flush()
    print(f"\n{nproved} / {len(Ls)} proved UNSAT by strengthened bookkeeping alone")
