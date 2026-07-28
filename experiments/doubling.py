#!/usr/bin/env python3
"""
CLAIM TESTED: the "atom doubling" map.

For a finite set V of integers >= 2 and a colouring sigma : V -> {beta, gamma},
put   beta_n = {2n, 2n+1},  gamma_n = {2n-1, 2n}.  For distinct n the atoms are
disjoint EXCEPT that beta_n and gamma_{n+1} both contain 2n+1.  Hence a colouring
is admissible iff inside every maximal run of V the gammas come first:
sigma is a PREFIX colouring of each run.  Then

    A_sigma(V) := union of the atoms          is LEGAL,
    |A_sigma(V)| = 2|V|,  cap(A_sigma(V)) = |V|,
    r(A_sigma(V)) = (#runs of V) + (#proper prefixes used),
    Sigma(A_sigma(V)) = Sigma(V) + sum_{n in G} 1/(2n(2n-1)) - sum_{n in B} 1/(2n(2n+1))
                      = Sigma(V) + sum_{n in G} 2/(4n^2-1) - Delta_V,
      Delta_V := sum_{n in V} 1/(2n(2n+1)),   and  2/(4n^2-1) = 1/(2n-1) - 1/(2n+1)
      telescopes over a prefix [u,c]:  sum = 1/(2u-1) - 1/(2c+1).

So if V is a solution (Sigma(V)=1), A_sigma(V) is a solution iff
      sum_j ( 1/(2u_j-1) - 1/(2c_j+1) )  =  Delta_V                       (BALANCE)
over the runs [u_j,v_j] of V with prefix end c_j in {u_j-1 (empty), u_j, ..., v_j}.

If BALANCE is solvable, the map DOUBLES the capacity (cap = |V|) while adding at
most one run per run of V, so iterating gives capacity -> infinity with run count
growing only linearly: that would settle the problem.

This script tests BALANCE exhaustively over every admissible colouring of every
known solution.  Exact arithmetic only.
"""
import sys
from fractions import Fraction as F
from itertools import product


def runs_of(U):
    U = sorted(U); out = []; cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1: cur.append(x)
        else: out.append(cur); cur = [x]
    out.append(cur); return out


def test(V):
    """return list of admissible prefix colourings satisfying BALANCE"""
    R = runs_of(V)
    Delta = sum(F(1, 2 * n * (2 * n + 1)) for n in V)
    # per run, the possible telescoped contributions
    opts = []
    for run in R:
        u, v = run[0], run[-1]
        o = [(None, F(0))]                      # empty prefix
        for c in range(u, v + 1):
            o.append((c, F(1, 2 * u - 1) - F(1, 2 * c + 1)))
        opts.append(o)
    sols = []
    for combo in product(*opts):
        if sum(x[1] for x in combo) == Delta:
            sols.append([x[0] for x in combo])
    return sols, Delta, R


def build(V, prefix_ends):
    R = runs_of(V); out = set()
    for run, c in zip(R, prefix_ends):
        for n in run:
            if c is not None and n <= c: out |= {2 * n - 1, 2 * n}
            else: out |= {2 * n, 2 * n + 1}
    return sorted(out)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "attempts/route-C/allsols_le105.txt"
    tot = 0; found = 0
    for ln in open(path):
        if not ln.startswith("SOL"): continue
        V = [int(x) for x in ln.split()[1:]]
        assert sum(F(1, n) for n in V) == 1
        nopts = 1
        for run in runs_of(V): nopts *= len(run) + 1
        if nopts > 4_000_000:
            print(f"  skip (too many colourings: {nopts})"); continue
        tot += 1
        sols, Delta, R = test(V)
        if sols:
            found += 1
            print(f"*** BALANCE SOLVED for V={V}")
            print(f"    Delta={Delta}  colourings={sols[:3]}")
            W = build(V, sols[0])
            s = sum(F(1, n) for n in W); S = set(W)
            print(f"    -> W (|W|={len(W)}) sum={s} legal={all(n-1 in S or n+1 in S for n in W)}")
            print(f"    runs={[len(r) for r in runs_of(W)]}")
    print(f"\ntested {tot} solutions as index sets; BALANCE solvable for {found}")
