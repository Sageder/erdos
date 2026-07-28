"""
CLAIM TESTED: for a given L, is there a covering system of Z whose moduli are DISTINCT divisors
of L lying in E = {n >= 4 : n+1 prime}?   Two variants:

  mode "full" : cover every residue of Z/L.
  mode "hole" : cover every residue of Z/L EXCEPT 0, and require every chosen class to avoid 0
                (i.e. residue a with a != 0 mod n).  This is the natural building block of a
                recursive construction: the leftover is then exactly the single class 0 mod L,
                which can be attacked recursively with moduli that are multiples of L.
                By translation invariance, fixing the hole at 0 is WLOG.

Encoding: x[n][a] = "class a mod n is used".  At-most-one residue per modulus (sequential /
ladder encoding, linear size) enforces the distinct-moduli convention.  One coverage clause per
residue.  Translation symmetry is broken in "full" mode by forcing the smallest USED modulus to
have residue 0 (valid because the solution set is invariant under a global shift).

Exactness: SAT result is exact (UNSAT = rigorous nonexistence for that L and that variant).
Any SAT model is re-verified from scratch by verify_solution() in exact integer arithmetic.

CONCLUSION: printed per run; recorded in NOTES.md.
"""
import sys, time
from fractions import Fraction
from sympy import isprime
from pysat.formula import IDPool
from pysat.solvers import Cadical153


def admissible_divisors(L, world="E"):
    ds = []
    i = 1
    while i * i <= L:
        if L % i == 0:
            for x in (i, L // i):
                ok = (x >= 4 and isprime(x + 1)) if world == "E" else (x >= 2 and isprime(2 * x + 1))
                if ok and x not in ds:
                    ds.append(x)
        i += 1
    return sorted(ds)


def build(L, mods, mode):
    pool = IDPool()
    X = {}
    cls = []
    for n in mods:
        lo = 1 if mode == "hole" else 0
        for a in range(lo, n):
            X[(n, a)] = pool.id(('x', n, a))
    # at-most-one residue per modulus, sequential encoding
    for n in mods:
        lo = 1 if mode == "hole" else 0
        lits = [X[(n, a)] for a in range(lo, n)]
        if len(lits) <= 1:
            continue
        s = [pool.id(('s', n, k)) for k in range(len(lits) - 1)]
        cls.append([-lits[0], s[0]])
        for k in range(1, len(lits) - 1):
            cls.append([-lits[k], s[k]])
            cls.append([-s[k - 1], s[k]])
            cls.append([-lits[k], -s[k - 1]])
        cls.append([-lits[-1], -s[-1]])
    # "used" indicators + translation symmetry break (full mode only)
    if mode == "full":
        U = {}
        for n in mods:
            U[n] = pool.id(('u', n))
            lits = [X[(n, a)] for a in range(n)]
            cls.append([-U[n]] + lits)
            for l in lits:
                cls.append([U[n], -l])
        for i, n in enumerate(mods):
            cls.append([-U[n]] + [U[m] for m in mods[:i]] + [X[(n, 0)]])
    # coverage
    start = 1 if mode == "hole" else 0
    for r in range(start, L):
        c = []
        for n in mods:
            a = r % n
            if mode == "hole" and a == 0:
                continue
            c.append(X[(n, a)])
        if not c:
            return None, None, None, r      # residue r provably uncoverable
        cls.append(c)
    return pool, X, cls, None


def verify_solution(L, chosen, mode):
    """independent exact re-verification: sweep the full period."""
    seen = set()
    for (n, a) in chosen:
        assert n >= 4 and isprime(n + 1), f"modulus {n} not of the form p-1 with p>=5 prime"
        assert L % n == 0
        assert n not in seen, f"modulus {n} repeated"
        seen.add(n)
    covered = bytearray(L)
    for (n, a) in chosen:
        for r in range(a % n, L, n):
            covered[r] = 1
    miss = [r for r in range(L) if not covered[r]]
    return miss


def run(L, mode="full", world="E", timeout_note=""):
    mods = admissible_divisors(L, world)
    budget = sum(Fraction(1, n) for n in mods)
    print(f"L = {L}   world={world}  mode={mode}  #moduli={len(mods)}  "
          f"budget={budget} = {float(budget):.6f}")
    print("   moduli:", mods)
    if float(budget) <= 1.0 and mode == "full":
        print("   RESULT: UNSAT by the budget bound alone (sum 1/n <= 1).")
        return "UNSAT-budget", None
    pool, X, cls, bad = build(L, mods, mode)
    if bad is not None:
        print(f"   RESULT: UNSAT — residue {bad} cannot be covered by any admissible class.")
        return "UNSAT-trivial", None
    print(f"   vars={pool.top}  clauses={len(cls)}")
    t0 = time.time()
    with Cadical153(bootstrap_with=cls) as s:
        sat = s.solve()
        el = time.time() - t0
        if not sat:
            print(f"   RESULT: UNSAT  ({el:.1f}s)  -> rigorous: no covering with distinct "
                  f"E-divisors of {L}" + (" leaving exactly the class 0" if mode == "hole" else ""))
            return "UNSAT", None
        model = set(l for l in s.get_model() if l > 0)
    chosen = sorted([(n, a) for (n, a) in X if X[(n, a)] in model])
    print(f"   RESULT: SAT  ({el:.1f}s)   {len(chosen)} congruences")
    for (n, a) in chosen:
        print(f"        {a} mod {n}")
    cost = sum(Fraction(1, n) for (n, a) in chosen)
    print("   cost sum 1/n =", cost, "=", float(cost))
    if mode == "full":
        miss = verify_solution(L, chosen, mode)
        print("   INDEPENDENT VERIFICATION: uncovered residues mod L:", len(miss))
        assert not miss, miss[:20]
    else:
        miss = verify_solution(L, chosen, mode)
        print("   INDEPENDENT VERIFICATION: uncovered residues mod L:", miss[:5],
              "count =", len(miss))
        assert miss == [0], miss[:20]
    return "SAT", chosen


if __name__ == "__main__":
    L = int(sys.argv[1])
    mode = sys.argv[2] if len(sys.argv) > 2 else "full"
    world = sys.argv[3] if len(sys.argv) > 3 else "E"
    run(L, mode, world)
