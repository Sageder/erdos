"""
G_11_minlattice.py -- Route G, step 11: the SMALLEST lattices that support the two halves.

CLAIMS TESTED (exact SAT decisions; every SAT model is re-verified by an exhaustive sweep):
  (a) smallest M such that D_H(M) = {m | M : 2m+1 prime, m>=2} supports a covering system of Z
      with distinct moduli   ("one parity class can be done");
  (b) smallest M such that D_H(M)\\{2} supports one  ("the hard half", least modulus >= 3;
      this is a NECESSARY condition for an E-covering with lcm dividing 2M, by Corollary 3).
For every M in range with reciprocal budget > 1 we run the exact decision.

CONCLUSION: recorded in the route-G report.
"""
import sys
from fractions import Fraction
from sympy import divisors, isprime
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

def DH(M):
    return [d for d in divisors(M) if d >= 2 and isprime(2*d+1)]

def decide(L, pool, budget_seconds=None):
    pool = sorted(pool)
    if sum(Fraction(1, m) for m in pool) <= 1:
        return False, None, "density"
    vp = IDPool(); var = {}
    for m in pool:
        for a in range(m):
            var[(m, a)] = vp.id(("x", m, a))
    cnf = CNF()
    for r in range(L):
        cnf.append([var[(m, r % m)] for m in pool])
    for m in pool:
        lits = [var[(m, a)] for a in range(m)]
        if len(lits) <= 12:
            for i in range(len(lits)):
                for j in range(i+1, len(lits)):
                    cnf.append([-lits[i], -lits[j]])
        else:
            cnf.extend(CardEnc.atmost(lits=lits, bound=1, vpool=vp,
                                      encoding=EncType.seqcounter).clauses)
    with Solver(name="cd15", bootstrap_with=cnf) as s:
        r = s.solve()
        if not r:
            return False, None, "UNSAT"
        model = set(l for l in s.get_model() if l > 0)
        cls = sorted([(a, m) for (m, a), v in var.items() if v in model], key=lambda t: t[1])
        cov = bytearray(L)
        for a, m in cls:
            for x in range(a % m, L, m): cov[x] = 1
        assert all(cov), "SAT model failed verification!"
        return True, cls, "SAT+verified"

def main():
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    mode = sys.argv[2] if len(sys.argv) > 2 else "H"
    print(f"scanning M <= {hi}, world = {mode}")
    found = []
    for M in range(2, hi + 1):
        P = DH(M)
        if mode == "H3":
            P = [m for m in P if m >= 3]
        if not P: continue
        b = sum(Fraction(1, m) for m in P)
        if b <= 1: continue
        ok, cls, why = decide(M, P)
        tag = "COVERING" if ok else "none"
        print(f"M={M:>6}  |D|={len(P):>3}  budget={float(b):.5f}  -> {tag} ({why})", flush=True)
        if ok:
            print("    moduli:", sorted(m for _, m in cls))
            print("    classes:", " ".join(f"{a}({m})" for a, m in cls))
            found.append(M)
            if len(found) >= 6: break
    print("\nsmallest lattices supporting a covering:", found)

main()
