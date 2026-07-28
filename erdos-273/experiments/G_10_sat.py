"""
G_10_sat.py -- Route G, step 10: SAT decision procedure for "is there a covering system with
distinct moduli drawn from a given pool of divisors of L?"

CLAIM TESTED.  Given L and a pool P of divisors of L, decide EXACTLY whether residues can be
chosen so that the classes cover Z/L, using each modulus at most once.

ENCODING.  Boolean variable x[m][a] = "the class a (mod m) is used", for m in P, 0 <= a < m.
  * coverage: for every r in Z/L,   OR_{m in P} x[m][r mod m]      (L clauses, width |P|)
  * distinctness: at most one a per m  (sequential-counter cardinality encoding, linear)
UNSAT  <=>  no covering system with distinct moduli from P exists (with lcm dividing L).
Any SAT model is re-verified independently by an exhaustive sweep of Z/L in Python.

RELEVANCE.  By the structure lemma an E-covering with lcm 2M is a pair of DISJOINT
H-coverings with moduli | M; one of the two cannot use m = 2.  So
   world 'H3'  (pool = D_H(M) \\ {2})  is a NECESSARY condition for lcm | 2M;
   world 'E'   (pool = 2*D_H(M), L = 2M) is the full question at that lattice.

USAGE: python3 G_10_sat.py <M> <world in {H,H3,E}> [--solver cd15] [--timeout S]

CONCLUSION: recorded in the route-G report.
"""
import sys, time
from fractions import Fraction
from sympy import divisors, isprime

from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

def DH(M):
    return [d for d in divisors(M) if d >= 2 and isprime(2*d+1)]

def build(L, pool):
    pool = sorted(pool)
    vp = IDPool()
    var = {}
    for m in pool:
        for a in range(m):
            var[(m, a)] = vp.id(("x", m, a))
    cnf = CNF()
    # coverage
    for r in range(L):
        cnf.append([var[(m, r % m)] for m in pool])
    # at most one residue per modulus
    for m in pool:
        lits = [var[(m, a)] for a in range(m)]
        if len(lits) <= 12:
            for i in range(len(lits)):
                for j in range(i+1, len(lits)):
                    cnf.append([-lits[i], -lits[j]])
        else:
            enc = CardEnc.atmost(lits=lits, bound=1, vpool=vp, encoding=EncType.seqcounter)
            cnf.extend(enc.clauses)
    return cnf, var, pool, vp

def verify(L, classes):
    cov = bytearray(L)
    for a, m in classes:
        for r in range(a % m, L, m):
            cov[r] = 1
    return all(cov), [r for r in range(L) if not cov[r]]

def main():
    M = int(sys.argv[1]); world = sys.argv[2]
    solver_name = "cd15"
    tmo = None
    args = sys.argv[3:]
    for i, a in enumerate(args):
        if a == "--solver": solver_name = args[i+1]
        if a == "--timeout": tmo = float(args[i+1])

    P = DH(M)
    if world == "H":
        L, pool = M, P
    elif world == "H3":
        L, pool = M, [m for m in P if m >= 3]
    elif world == "E":
        L, pool = 2*M, [2*m for m in P]
    else:
        raise SystemExit("world must be H, H3 or E")

    print(f"M = {M}   world = {world}   L = {L}   |pool| = {len(pool)}")
    print(f"pool = {pool}")
    print(f"reciprocal sum of pool = {sum(Fraction(1,m) for m in pool)} = "
          f"{float(sum(Fraction(1,m) for m in pool)):.6f}")
    if sum(Fraction(1, m) for m in pool) <= 1:
        print("DENSITY OBSTRUCTION: reciprocal sum <= 1, no covering possible.  UNSAT (proved).")
        return
    t = time.time()
    cnf, var, pool, vp = build(L, pool)
    print(f"CNF: {cnf.nv} vars, {len(cnf.clauses)} clauses  (built in {time.time()-t:.1f}s)")
    t = time.time()
    with Solver(name=solver_name, bootstrap_with=cnf) as s:
        res = s.solve()
        el = time.time() - t
        print(f"solver {solver_name}: {'SAT' if res else 'UNSAT'}   ({el:.1f}s)")
        print("stats:", s.accum_stats())
        if res:
            model = set(l for l in s.get_model() if l > 0)
            classes = [(a, m) for (m, a), v in var.items() if v in model]
            classes.sort(key=lambda t: t[1])
            print("CLASSES:", " ".join(f"{a}({m})" for a, m in classes))
            ok, unc = verify(L, classes)
            print("INDEPENDENT VERIFICATION over Z/%d: covering = %s (uncovered %d)" % (L, ok, len(unc)))
            print("moduli used:", sorted(m for _, m in classes))
            print("reciprocal sum used:", sum(Fraction(1, m) for _, m in classes),
                  "=", float(sum(Fraction(1, m) for _, m in classes)))
            if world == "E":
                even = sorted(m//2 for a, m in classes if a % 2 == 0)
                odd = sorted(m//2 for a, m in classes if a % 2 == 1)
                print("halved split: S0 (even residues) =", even)
                print("              S1 (odd  residues) =", odd)
                print("disjoint:", set(even).isdisjoint(odd))
        else:
            print("PROVED (SAT, exhaustive): no covering system with distinct moduli from this")
            print("pool exists.  In particular no E-covering has lcm dividing", 2*M if world!="E" else L)

main()
