"""
Q3 (and the underlying Erdos-289 question).  Exhaustive/heuristic search for

    rho = sum_{n in U} 1/n ,  U finite subset of [T, X],  U has no isolated point.

(Equivalently rho is a sum of pairwise disjoint blocks of length >= 2 with all
elements in [T,X]; see PROBLEM.md's "working reformulation".)

The search enumerates the MAXIMAL RUNS of U in increasing order, so each set is
produced exactly once.  Every arithmetic operation is exact (Fraction).

Rigorous prunes used (all proved in REPORT.md):
  * r must lie in (0, sum_{n=A}^{X} 1/n].
  * the next run [a,b] must satisfy 1/a+1/(a+1) <= r, so a >= amin(r).
  * DENOMINATOR PRUNE: for every prime power q = p^e || den(r), some element of
    U cap [A,X] must be divisible by p^e -- else v_p(r) > -e is impossible.
    (Proof: v_p(sum of 1/n over n in [A,X]) >= -max_n v_p(n).)
  * 2-ADIC PRUNE: let t = -v_2(r).  If t >= 1 then some remaining element is
    divisible by 2^t; so 2^t <= X.

Usage examples:
    python3 q3_search.py one 1 2 260 8         # rho=1, T=2, X=260, <=8 runs
    python3 q3_search.py one 1/20 7 4000 3
"""

import sys
from fractions import Fraction
from functools import lru_cache

from blocks import H, min_start_for_target, no_isolated, runs


# ------------------------------------------------------------------ helpers

@lru_cache(maxsize=None)
def tailsum(A, X):
    if A > X:
        return Fraction(0)
    s = Fraction(0)
    for n in range(A, X + 1):
        s += Fraction(1, n)
    return s


def prime_power_factors(m):
    out = []
    d = 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            out.append(d ** e)
        d += 1 if d == 2 else 2
    if m > 1:
        out.append(m)
    return out


def denom_feasible(r, A, X):
    """every prime power q||den(r) needs a multiple in [A,X]"""
    for q in prime_power_factors(r.denominator):
        if q > X:
            return False
        if (X // q) * q < A:
            return False
    return True


# ------------------------------------------------------------------- search

class Searcher:
    def __init__(self, X, maxruns, want=1, verbose=False):
        self.X = X
        self.maxruns = maxruns
        self.want = want
        self.found = []
        self.nodes = 0
        self.verbose = verbose

    def search(self, rho, T):
        self.found = []
        self.nodes = 0
        self._dfs(Fraction(rho), T, [], self.maxruns)
        return self.found

    def _dfs(self, r, A, chosen, budget):
        self.nodes += 1
        if r == 0:
            self.found.append(list(chosen))
            return len(self.found) >= self.want
        if budget == 0 or r < 0:
            return False
        if A > self.X:
            return False
        if r > tailsum(A, self.X):
            return False
        amin = max(A, min_start_for_target(r))
        if amin > self.X - 1:
            return False
        if not denom_feasible(r, amin, self.X):
            return False
        for a in range(amin, self.X):
            # cheap feasibility: even using everything from a on we cannot reach r
            if r > tailsum(a, self.X):
                return False
            h = Fraction(1, a)
            b = a
            while b < self.X:
                b += 1
                h += Fraction(1, b)
                if h > r:
                    break
                chosen.append((a, b))
                # next run must leave a gap of >=1  (runs are maximal)
                if self._dfs(r - h, b + 2, chosen, budget - 1):
                    chosen.pop()
                    return True
                chosen.pop()
        return False


def elements(sol):
    out = []
    for a, b in sol:
        out.extend(range(a, b + 1))
    return out


def verify(sol, rho, T):
    U = elements(sol)
    assert len(U) == len(set(U)), "overlap!"
    assert min(U) >= T, "below T"
    assert no_isolated(U), "isolated point"
    s = sum((Fraction(1, n) for n in U), Fraction(0))
    assert s == Fraction(rho), "sum mismatch %s" % s
    return True


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        rho = Fraction(sys.argv[2])
        T = int(sys.argv[3])
        X = int(sys.argv[4])
        mr = int(sys.argv[5])
        want = int(sys.argv[6]) if len(sys.argv) > 6 else 1
        S = Searcher(X, mr, want=want)
        sols = S.search(rho, T)
        print("rho=%s T=%d X=%d maxruns=%d  nodes=%d" % (rho, T, X, mr, S.nodes))
        for s in sols:
            verify(s, rho, T)
            print("   SOLUTION runs=%s  elements=%s" % (s, elements(s)))
        if not sols:
            print("   NO SOLUTION in this box")
