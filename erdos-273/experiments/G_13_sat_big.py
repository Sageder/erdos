"""
G_13_sat_big.py -- Route G, step 13: fast SAT build for the large lattices.

CLAIM TESTED: identical to G_10_sat.py (does the given pool of divisors of L admit a covering
system with distinct moduli?) but with a hand-rolled variable numbering and a linear
"at-most-one" ladder encoding, so that the CNF for L ~ 10^5 builds in seconds instead of
minutes.  Any SAT model is re-verified by an exhaustive sweep of Z/L.

The decisive instance is  M = 27720  world H3:  by G_12 every E-covering has lcm >= 55440 and
lcm/2 must have s(lcm/2) > 2, the smallest such value being 27720; and by Corollary 3 an
E-covering with lcm = 55440 requires a covering with distinct moduli from D_H(27720)\\{2}.

USAGE: python3 G_13_sat_big.py <M> <H|H3|E> [solver] [seconds]
"""
import sys, time
from fractions import Fraction
from sympy import divisors, isprime
from pysat.solvers import Solver

M = int(sys.argv[1]); world = sys.argv[2]
solver_name = sys.argv[3] if len(sys.argv) > 3 else "cd15"

P = [d for d in divisors(M) if d >= 2 and isprime(2*d + 1)]
if world == "H":   L, pool = M, P
elif world == "H3": L, pool = M, [m for m in P if m >= 3]
elif world == "E":  L, pool = 2*M, [2*m for m in P]
else: raise SystemExit("world")

pool = sorted(pool)
print(f"M={M} world={world} L={L} |pool|={len(pool)}")
print("pool:", pool)
b = sum(Fraction(1, m) for m in pool)
print("budget:", b, "=", float(b))
if b <= 1:
    print("DENSITY OBSTRUCTION -> UNSAT (proved)"); sys.exit()

t = time.time()
base = {}
nv = 0
for m in pool:
    base[m] = nv          # var for class a mod m is base[m]+a+1
    nv += m
cls = []
# coverage
for r in range(L):
    cls.append([base[m] + (r % m) + 1 for m in pool])
# at most one class per modulus: ladder (sequential) encoding, linear size
for m in pool:
    if m <= 10:
        for i in range(m):
            for j in range(i + 1, m):
                cls.append([-(base[m]+i+1), -(base[m]+j+1)])
    else:
        # s_i = "some x_0..x_i true"
        s0 = nv; nv += m
        S = lambda i: s0 + i + 1
        X = lambda i: base[m] + i + 1
        cls.append([-X(0), S(0)])
        for i in range(1, m):
            cls.append([-X(i), S(i)])
            cls.append([-S(i-1), S(i)])
            cls.append([-X(i), -S(i-1)])
print(f"CNF: {nv} vars, {len(cls)} clauses (built {time.time()-t:.1f}s)")

t = time.time()
with Solver(name=solver_name, bootstrap_with=cls) as s:
    res = s.solve()
    print(f"solver={solver_name}: {'SAT' if res else 'UNSAT'}  ({time.time()-t:.1f}s)")
    print("stats:", s.accum_stats())
    if res:
        model = set(l for l in s.get_model() if l > 0)
        chosen = []
        for m in pool:
            for a in range(m):
                if base[m] + a + 1 in model:
                    chosen.append((a, m))
        chosen.sort(key=lambda z: z[1])
        print("CLASSES:", " ".join(f"{a}({m})" for a, m in chosen))
        cov = bytearray(L)
        for a, m in chosen:
            for r in range(a % m, L, m): cov[r] = 1
        print("INDEPENDENT VERIFICATION: covering =", all(cov),
              " uncovered =", L - sum(cov))
        print("moduli:", sorted(m for _, m in chosen))
        print("reciprocal sum:", sum(Fraction(1, m) for _, m in chosen))
    else:
        print("PROVED: no covering system with distinct moduli from this pool.")
