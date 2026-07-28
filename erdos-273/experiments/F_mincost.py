"""
F_mincost.py  --  Route F (efficiency / budget) for Erdos problem 273.

CLAIM TESTED
------------
For a fixed modulus-bound L and a fixed "world" W of admissible moduli
(W = all integers, or W = E = {p-1 : p>=5 prime}, or W = H = {m : 2m+1 prime}),
determine EXACTLY

    mu(L, W) := min { sum_i 1/n_i : a_1 mod n_1, ..., a_k mod n_k is a covering
                      system of Z, the n_i are PAIRWISE DISTINCT, 1 < n_i,
                      n_i | L, n_i in W }.

Key exact reformulation used by the solver (all integer arithmetic):
   every chosen class a mod d (d | L) meets exactly L/d residues mod L, so
        sum_i 1/n_i  =  ( sum_i L/n_i ) / L  =  ( L + Waste ) / L,
   where  Waste := sum_i (L/n_i)  -  L  =  sum_{r mod L} (mult(r) - 1)  >= 0
   is the total multiplicity excess.  Hence
        mu(L,W) = 1 + X(L,W)/L,  X(L,W) := min Waste  (a NON-NEGATIVE INTEGER).
   Waste is monotone non-decreasing along any DFS that adds classes one at a
   time (adding a mod d increases sum L/n_i by L/d and the covered count by at
   most L/d), so "current waste" is a valid branch-and-bound lower bound.

METHOD: iterative deepening on Wmax = 0,1,2,...  DFS that always branches on
the SMALLEST uncovered residue r (any covering must contain a class a = r mod d
for some unused admissible d, so the branching is complete), prunes as soon as
current waste exceeds Wmax, and also prunes on the residual reciprocal budget.
Exact: Python ints as L-bit bitmasks, fractions.Fraction for reporting.

CONCLUSION: see F_mincost_run.py / FINDINGS.md.  (A value X(L,W) produced here
is a THEOREM ABOUT THAT L AND THAT W ONLY.)
"""
from fractions import Fraction
from math import gcd
import sys

# ---------------------------------------------------------------- primality
def _is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def divisors(L):
    ds, i = [], 1
    while i * i <= L:
        if L % i == 0:
            ds.append(i)
            if i != L // i:
                ds.append(L // i)
        i += 1
    return sorted(ds)


WORLDS = {
    # name : predicate on the modulus n
    "ALL": lambda n: n > 1,
    "E":   lambda n: n >= 4 and _is_prime(n + 1),          # n = p-1, p>=5 prime
    "H":   lambda n: n >= 2 and _is_prime(2 * n + 1),      # 2n+1 prime
}


# ---------------------------------------------------------------- the solver
class MinCover:
    """Exact minimiser of the multiplicity excess Waste."""

    def __init__(self, L, world="ALL", extra_filter=None, verbose=False):
        self.L = L
        self.full = (1 << L) - 1
        pred = WORLDS[world]
        ds = [d for d in divisors(L) if d > 1 and pred(d)]
        if extra_filter is not None:
            ds = [d for d in ds if extra_filter(d)]
        self.ds = ds                      # ascending
        self.nd = len(ds)
        self.cnt = [L // d for d in ds]   # residues mod L covered by one class
        # base masks: bits at 0, d, 2d, ...
        self.base = []
        for d in ds:
            m = 0
            for j in range(0, L, d):
                m |= 1 << j
            self.base.append(m)
        self.budget = sum(Fraction(1, d) for d in ds)
        self.verbose = verbose
        self.nodes = 0

    def feasible_at_all(self):
        """Necessary condition: total reciprocal budget of the world >= 1."""
        return self.budget >= 1

    # ---- DFS with waste bound
    def _dfs(self, covered, ncov, used, waste, chosen, wmax, budget_left):
        self.nodes += 1
        if self.nodes % 2000000 == 0 and self.verbose:
            print(f"      ... {self.nodes//1000000}M nodes, depth {len(chosen)}",
                  flush=True)
        if ncov == self.L:
            self.solution = list(chosen)
            self.best_waste = waste
            return True
        # residual budget prune: still need to cover L-ncov residues
        if budget_left * self.L < self.L - ncov:
            return False
        t = ~covered & self.full
        r = (t & -t).bit_length() - 1        # smallest uncovered residue
        for i in range(self.nd):
            if used >> i & 1:
                continue
            d = self.ds[i]
            m = self.base[i] << (r % d)
            ov = (m & covered).bit_count()
            nw = waste + ov
            if nw > wmax:
                continue
            chosen.append((d, r % d))
            if self._dfs(covered | m, ncov + self.cnt[i] - ov, used | (1 << i),
                         nw, chosen, wmax, budget_left - Fraction(1, d)):
                return True
            chosen.pop()
        return False

    def solve(self, wmax_cap=None, verbose=None):
        """Iterative deepening on the waste.  Returns (X, system) or (None,None)."""
        if verbose is not None:
            self.verbose = verbose
        if not self.feasible_at_all():
            return None, None
        cap = wmax_cap if wmax_cap is not None else self.L  # trivial cap
        for wmax in range(0, cap + 1):
            self.nodes = 0
            self.solution = None
            if self._dfs(0, 0, 0, 0, [], wmax, self.budget):
                return self.best_waste, self.solution
            if self.verbose:
                print(f"    Wmax={wmax}: infeasible ({self.nodes} nodes)",
                      flush=True)
        return None, None


# ---------------------------------------------------------------- verifier
def verify(L, system, world=None, require_divides=None):
    """Independent exhaustive check of a covering system mod L.
    system = list of (n, a).  Returns dict of checks (all must be True)."""
    mods = [n for n, a in system]
    ok = {}
    ok["distinct"] = len(set(mods)) == len(mods)
    ok["all>1"] = all(n > 1 for n in mods)
    if require_divides is not None:
        ok["divides_L"] = all(require_divides % n == 0 for n in mods)
    if world is not None:
        ok["in_world"] = all(WORLDS[world](n) for n in mods)
    cover = bytearray(L)
    mult = 0
    for n, a in system:
        for x in range(a % n, L, n):
            cover[x] += 1
            mult += 1
    ok["covers_all_residues_mod_L"] = all(c >= 1 for c in cover)
    s = sum(Fraction(1, n) for n in system and mods)
    ok["sum_reciprocals"] = s
    ok["waste"] = mult - L
    ok["consistent"] = (s == Fraction(L + mult - L, L)) and (
        s - 1 == Fraction(mult - L, L))
    return ok


if __name__ == "__main__":
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    world = sys.argv[2] if len(sys.argv) > 2 else "ALL"
    mc = MinCover(L, world, verbose=True)
    print(f"L={L} world={world} moduli={mc.ds} budget={float(mc.budget):.4f}")
    X, sol = mc.solve()
    print("X =", X, "system =", sol)
    if sol:
        print(verify(L, sol, world, L))
