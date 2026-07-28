"""
Generalised covering-search over a POOL  Q(k) := { e >= emin : k*e + 1 is prime }.

WHY THIS IS THE RIGHT OBJECT.  Write E = {n >= 4 : n+1 prime} = Q(1) restricted to n >= 4.
Inside a covering system, suppose the classes chosen so far leave exactly the class 0 (mod d)
uncovered.  Any further modulus that is a multiple of d, say n = d*e, meets that class in the
class {y : y = c (mod e)} after the substitution x = d*y.  And d*e lies in E exactly when
d*e + 1 is prime, i.e. e in Q(d).  So:

    "cover the class 0 mod d using E-moduli divisible by d"
        <=>  "cover Z with distinct moduli from Q(d)".

Q(d) has density  (d/phi(d)) / log(d e)  around e, so for smooth d the pool is MUCH denser than
E itself -- this is the d/phi(d) enrichment.  The same statement in the halved world H uses
Q(2d).

This script decides, by exact SAT, whether Z/D can be covered by classes with DISTINCT moduli
drawn from Q(k) cap Div(D), and also the relaxed "cover Z/D except the single residue 0" variant.
UNSAT is a rigorous nonexistence statement for that (k, D); SAT yields a certificate which is
re-verified from scratch by a full sweep of Z/D.

CONCLUSION: printed per run; recorded in NOTES.md.
"""
import sys, time
from fractions import Fraction
from sympy import isprime
from pysat.formula import IDPool
from pysat.solvers import Cadical153


def pool_divisors(D, k, emin=2, forbid=()):
    ds = []
    i = 1
    while i * i <= D:
        if D % i == 0:
            for x in (i, D // i):
                if x >= emin and x not in ds and x not in forbid and isprime(k * x + 1):
                    ds.append(x)
        i += 1
    return sorted(ds)


def solve(D, mods, mode="full", verbose=True):
    pool = IDPool()
    X, cls = {}, []
    for n in mods:
        lo = 1 if mode == "hole" else 0
        for a in range(lo, n):
            X[(n, a)] = pool.id(('x', n, a))
    for n in mods:                      # at-most-one residue per modulus (sequential encoding)
        lo = 1 if mode == "hole" else 0
        lits = [X[(n, a)] for a in range(lo, n)]
        if len(lits) <= 1:
            continue
        s = [pool.id(('s', n, t)) for t in range(len(lits) - 1)]
        cls.append([-lits[0], s[0]])
        for t in range(1, len(lits) - 1):
            cls.append([-lits[t], s[t]])
            cls.append([-s[t - 1], s[t]])
            cls.append([-lits[t], -s[t - 1]])
        cls.append([-lits[-1], -s[-1]])
    start = 1 if mode == "hole" else 0
    for r in range(start, D):
        c = []
        for n in mods:
            a = r % n
            if mode == "hole" and a == 0:
                continue
            c.append(X[(n, a)])
        if not c:
            return "UNSAT-trivial", None
        cls.append(c)
    t0 = time.time()
    with Cadical153(bootstrap_with=cls) as s:
        ok = s.solve()
        dt = time.time() - t0
        if not ok:
            return f"UNSAT ({dt:.1f}s)", None
        model = set(l for l in s.get_model() if l > 0)
    chosen = sorted([(n, a) for (n, a) in X if X[(n, a)] in model])
    return f"SAT ({dt:.1f}s)", chosen


def verify(D, chosen, k, mode):
    """independent exact re-verification by a full sweep of Z/D."""
    seen = set()
    for (n, a) in chosen:
        assert D % n == 0, (n, D)
        assert isprime(k * n + 1), (k, n, "k*n+1 not prime")
        assert n not in seen, ("repeated modulus", n)
        seen.add(n)
        if mode == "hole":
            assert a % n != 0, ("class contains 0", n, a)
    cov = bytearray(D)
    for (n, a) in chosen:
        for r in range(a % n, D, n):
            cov[r] = 1
    return [r for r in range(D) if not cov[r]]


def run(D, k, mode="full", emin=2, forbid=(), quiet=False):
    mods = pool_divisors(D, k, emin, forbid)
    b = sum(Fraction(1, n) for n in mods)
    head = (f"k={k:<4} D={D:<10} pool|Div(D) = {len(mods):3d} moduli   budget = {float(b):.5f}"
            f"   mode={mode}")
    if float(b) <= 1.0 and mode == "full":
        print(head + "   -> UNSAT by budget")
        return "UNSAT-budget", None, float(b)
    verdict, chosen = solve(D, mods, mode)
    print(head + "   -> " + verdict)
    if chosen is not None:
        miss = verify(D, chosen, k, mode)
        cost = sum(Fraction(1, n) for (n, a) in chosen)
        exp = [] if mode == "full" else [0]
        assert miss == exp, ("VERIFICATION FAILED", miss[:10])
        print(f"     verified: uncovered = {miss}   #congruences = {len(chosen)}"
              f"   cost = {float(cost):.5f}")
        if not quiet:
            print("     " + "; ".join(f"{a} mod {n}" for (n, a) in chosen))
    return verdict, chosen, float(b)


if __name__ == "__main__":
    D = int(sys.argv[1]); k = int(sys.argv[2])
    mode = sys.argv[3] if len(sys.argv) > 3 else "full"
    emin = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    run(D, k, mode, emin)
