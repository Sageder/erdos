"""
G_14_mindeform_sat.py -- Route G, step 14: EXACT minimal deformation, via SAT.

CLAIM TESTED.  Fix a lattice L, a least-modulus threshold t, and an admissibility predicate
(H-world: m admissible iff 2m+1 prime; E-world: n admissible iff n+1 prime).  Among ALL
covering systems of Z with distinct moduli m | L, m >= t, what is the exact minimum number of
INADMISSIBLE moduli used?  (0 would answer Erdos 273 at that lattice.)

ENCODING.  x[m][a] = class a mod m used; at most one a per m; every residue covered;
y[m] = modulus m used (x[m][a] -> y[m]); cardinality constraint sum_{m inadmissible} y[m] <= k.
We increase k from 0 until SAT; the first SAT gives the exact minimum, every model is
re-verified by an exhaustive sweep of Z/L.  UNSAT at k gives a PROOF that k is not enough.

USAGE: python3 G_14_mindeform_sat.py L t {H|E} [kmax]
"""
import sys, time
from fractions import Fraction
from sympy import divisors, isprime
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

L = int(sys.argv[1]); t = int(sys.argv[2]); world = sys.argv[3]
kmax = int(sys.argv[4]) if len(sys.argv) > 4 else 6
adm = (lambda d: isprime(2*d+1)) if world == "H" else (lambda d: isprime(d+1))

pool = [d for d in divisors(L) if d >= t]
bad = [d for d in pool if not adm(d)]
print(f"L={L} least modulus >= {t} world={world}")
print("pool:", pool)
print("admissible:", [d for d in pool if adm(d)])
print("INadmissible:", bad)

for k in range(0, kmax + 1):
    vp = IDPool(); var = {}; y = {}
    for m in pool:
        for a in range(m):
            var[(m, a)] = vp.id(("x", m, a))
        y[m] = vp.id(("y", m))
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
        for a in range(m):
            cnf.append([-var[(m, a)], y[m]])
    if bad:
        cnf.extend(CardEnc.atmost(lits=[y[m] for m in bad], bound=k, vpool=vp,
                                  encoding=EncType.seqcounter).clauses)
    t0 = time.time()
    with Solver(name="cd15", bootstrap_with=cnf) as s:
        res = s.solve()
        print(f"  k = {k}: {'SAT' if res else 'UNSAT'}  ({time.time()-t0:.1f}s)")
        if res:
            model = set(l for l in s.get_model() if l > 0)
            cl = sorted([(a, m) for (m, a), v in var.items() if v in model], key=lambda z: z[1])
            cov = bytearray(L)
            for a, m in cl:
                for r in range(a % m, L, m): cov[r] = 1
            assert all(cov)
            used = sorted(m for _, m in cl)
            print("  EXACT MINIMUM DEFORMATION =", k)
            print("  classes:", " ".join(f"{a}({m})" for a, m in cl))
            print("  moduli used:", used)
            print("  inadmissible ones:", [m for m in used if not adm(m)])
            print("  reciprocal sum:", sum(Fraction(1, m) for m in used))
            print("  verified covering of Z/%d" % L)
            break
