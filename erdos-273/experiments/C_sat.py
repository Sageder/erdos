"""
C_sat.py  --  Route C, Step 2 (SAT encoding).

CLAIM TESTED.  Inside a fixed divisor lattice (every modulus must divide a given L):
  * single mode: is there a covering system of Z with pairwise DISTINCT moduli, all in
        H = {m >= 2 : 2m+1 prime}      (or E = {n >= 4 : n+1 prime}, or all divisors)
    optionally forbidding a given list of moduli?
  * --pair    : are there TWO such covering systems whose modulus sets are DISJOINT?
    By the Step-1 parity equivalence, SAT in --pair mode for some L is exactly a YES
    certificate for Erdos problem 273 (moduli 2m, residues 2b+j).

ENCODING.  Boolean x[m][a][j] = "class a mod m is used, in system j".
  coverage : for every r in [0,L) and every system j:   OR_{m} x[m][r mod m][j]
  distinct : for every m:  at most one of { x[m][a][j] : a in [0,m), j } is true
             (sequential-counter encoding, linear size)
UNSAT from the solver = no covering with all moduli dividing L (a genuine proof for that
divisor lattice, modulo solver correctness; SAT results are re-verified independently in
exact integer arithmetic here).

NOTE (stated explicitly, as required): UNSAT for one divisor lattice L is NOT a proof that
no covering exists; it only rules out systems all of whose moduli divide L.

CONCLUSION: printed per run; recorded in attempts/route-C-parity-H/FINDINGS.md.

usage:
  python3 C_sat.py L [--world H|E|A] [--forbid 2,3] [--pair] [--maxmod M]
                     [--solver cadical153|glucose4] [--timeout SEC] [--dimacs FILE]
"""
import sys
import time
from math import gcd
from sympy import isprime
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType


def divisors(L):
    ds = []
    d = 1
    while d * d <= L:
        if L % d == 0:
            ds.append(d)
            if d != L // d:
                ds.append(L // d)
        d += 1
    return sorted(ds)


def world_filter(world):
    if world == "H":
        return lambda x: x >= 2 and isprime(2 * x + 1)
    if world == "E":
        return lambda x: x >= 4 and isprime(x + 1)
    return lambda x: x >= 2


def build(L, mods, pair):
    pool = IDPool()
    cnf = CNF()
    nsys = 2 if pair else 1

    def V(m, a, j):
        return pool.id(("x", m, a, j))

    # coverage
    for j in range(nsys):
        for r in range(L):
            cnf.append([V(m, r % m, j) for m in mods])
    # at most one class per modulus, across both systems
    for m in mods:
        lits = [V(m, a, j) for j in range(nsys) for a in range(m)]
        if len(lits) <= 1:
            continue
        if len(lits) <= 12:
            for i in range(len(lits)):
                for k in range(i + 1, len(lits)):
                    cnf.append([-lits[i], -lits[k]])
        else:
            enc = CardEnc.atmost(lits=lits, bound=1, vpool=pool,
                                 encoding=EncType.seqcounter)
            cnf.extend(enc.clauses)
    return cnf, pool, V


def verify(L, classes):
    cov = bytearray(L)
    for a, m in classes:
        for x in range(a % m, L, m):
            cov[x] = 1
    return all(cov)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    L = int(sys.argv[1])
    world = "H"
    forbid = set()
    pair = False
    maxmod = 0
    solver_name = "cadical153"
    timeout = 0
    dimacs = None
    i = 2
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--world":
            i += 1; world = sys.argv[i]
        elif a == "--forbid":
            i += 1; forbid = {int(t) for t in sys.argv[i].split(",") if t}
        elif a == "--pair":
            pair = True
        elif a == "--maxmod":
            i += 1; maxmod = int(sys.argv[i])
        elif a == "--solver":
            i += 1; solver_name = sys.argv[i]
        elif a == "--timeout":
            i += 1; timeout = float(sys.argv[i])
        elif a == "--dimacs":
            i += 1; dimacs = sys.argv[i]
        else:
            raise SystemExit("unknown option " + a)
        i += 1

    ok = world_filter(world)
    mods = [d for d in divisors(L) if ok(d) and d not in forbid
            and (not maxmod or d <= maxmod)]
    budget = sum(1.0 / m for m in mods)
    print(f"L = {L}  world = {world}  pair = {pair}  #moduli = {len(mods)}  "
          f"budget = {budget:.6f}")
    print("moduli:", mods[:120], "..." if len(mods) > 120 else "")
    sys.stdout.flush()
    need = 2.0 if pair else 1.0
    if budget <= need:
        print(f"RESULT: UNSAT (reciprocal budget {budget:.6f} <= {need:g}; "
              f"each covering needs sum 1/m > 1)")
        return

    t = time.time()
    cnf, pool, V = build(L, mods, pair)
    print(f"CNF: {cnf.nv} vars, {len(cnf.clauses)} clauses  "
          f"(built in {time.time()-t:.1f}s)")
    sys.stdout.flush()
    if dimacs:
        cnf.to_file(dimacs)
        print("wrote", dimacs)

    from pysat.solvers import Solver
    t = time.time()
    with Solver(name=solver_name, bootstrap_with=cnf.clauses, use_timer=True) as s:
        if timeout:
            def interrupt(sv):
                sv.interrupt()
            from threading import Timer
            timer = Timer(timeout, interrupt, [s])
            timer.start()
            res = s.solve_limited(expect_interrupt=True)
            timer.cancel()
        else:
            res = s.solve()
        el = time.time() - t
        if res is None:
            print(f"RESULT: UNKNOWN (timeout after {el:.1f}s)")
            return
        if not res:
            print(f"RESULT: UNSAT (exhaustive over this divisor lattice; {el:.1f}s)")
            print(f"CAVEAT: this settles only systems all of whose moduli divide L = {L}.")
            return
        model = set(l for l in s.get_model() if l > 0)
        nsys = 2 if pair else 1
        out = [[] for _ in range(nsys)]
        for m in mods:
            for j in range(nsys):
                for a in range(m):
                    if V(m, a, j) in model:
                        out[j].append((a, m))
        print(f"RESULT: SAT ({el:.1f}s)")
        allmods = [m for j in range(nsys) for _a, m in out[j]]
        assert len(allmods) == len(set(allmods)), "DISTINCTNESS VIOLATION"
        for j in range(nsys):
            print(f"  system {j}: moduli {sorted(m for _a, m in out[j])}")
            print(f"     classes {sorted(out[j], key=lambda t: t[1])}")
            print(f"     recip sum {sum(1.0/m for _a, m in out[j]):.6f}")
            print(f"     independent verification over [0,{L}): "
                  f"{'PASS' if verify(L, out[j]) else '*** FAIL ***'}")
        if world == "H":
            print("  E-world moduli 2m:",
                  sorted(2 * m for j in range(nsys) for _a, m in out[j]))
            print("  all 2m+1 prime:",
                  all(isprime(2 * m + 1) for j in range(nsys) for _a, m in out[j]))


if __name__ == "__main__":
    main()
