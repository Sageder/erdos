"""
B_sat.py -- Route B: EXACT (SAT) decision procedure for a single node of the tree.

CLAIM TESTED
------------
NODE(D, M, holes):  does there exist a choice of residues b_f, for a subset of the admissible
moduli  P(D,M) = { f | M, f >= 2, D f + 1 prime }  (each modulus used AT MOST ONCE), covering
every residue of Z/M outside the given hole classes?

This is decided exactly with a SAT solver (Cadical195 via pysat):
  * variables x[f][a]  = "modulus f is used with residue a"   (a in Z/f)
  * at-most-one over a, for each f (sequential encoding, linear size)
  * for each residue r of Z/M outside the holes:  OR_f x[f][ r mod f ]
UNSAT is a PROOF that no covering system with lcm dividing M exists at this node with this
pool -- a genuine impossibility statement for that finite instance (not a search failure).

CONCLUSION: printed; recorded in attempts/route-B-recursive/FINDINGS.md

usage: python3 B_sat.py --D 2 --M 55440 [--hole q:c ...] [--exclude n1,n2,...] [--timeout 600]
"""
import argparse, sys, time
from fractions import Fraction
from sympy import isprime, factorint
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195


def divisors(n):
    ds = [1]
    for p, a in factorint(n).items():
        ds = [d * p ** i for d in ds for i in range(a + 1)]
    return sorted(ds)


def pool(D, M, used=(), fmin=2):
    us = set(used)
    out = []
    for f in divisors(M):
        if f < fmin:
            continue
        n = D * f
        if n < 4 or n in us:
            continue
        if isprime(n + 1):
            out.append(f)
    return out


def build(D, M, P, holes):
    vp = IDPool()
    cnf = CNF()
    var = {}
    for f in P:
        var[f] = [vp.id(("x", f, a)) for a in range(f)]
        if f > 1:
            cnf.extend(CardEnc.atmost(lits=var[f], bound=1, vpool=vp,
                                      encoding=EncType.seqcounter).clauses)
    holeset = holes
    ncl = 0
    for r in range(M):
        skip = False
        for q, c in holeset:
            if r % q == c % q:
                skip = True
                break
        if skip:
            continue
        cl = [var[f][r % f] for f in P]
        cnf.append(cl)
        ncl += 1
    return cnf, var, ncl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--D", type=int, default=2)
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--hole", action="append", default=[])
    ap.add_argument("--exclude", type=str, default="")
    ap.add_argument("--fmin", type=int, default=2)
    ap.add_argument("--maxf", type=int, default=0, help="cap on f (0 = no cap)")
    a = ap.parse_args()
    holes = []
    for h in a.hole:
        q, c = h.split(":")
        holes.append((int(q), int(c)))
    ex = [int(t) for t in a.exclude.split(",") if t.strip()]
    P = pool(a.D, a.M, ex, a.fmin)
    if a.maxf:
        P = [f for f in P if f <= a.maxf]
    bud = sum(Fraction(1, f) for f in P)
    need = 1 - sum(Fraction(1, q) for q, _ in holes)
    print(f"NODE D={a.D} M={a.M}={factorint(a.M)}  |P|={len(P)}  budget={float(bud):.5f}  "
          f"holes={holes}  need>{float(need):.5f}")
    if bud <= need:
        print("RESULT: UNSAT (reciprocal-sum necessary condition already fails)")
        return
    t0 = time.time()
    cnf, var, ncl = build(a.D, a.M, P, holes)
    print(f"  CNF: {cnf.nv} vars, {len(cnf.clauses)} clauses ({ncl} coverage clauses), "
          f"built in {time.time()-t0:.1f}s", flush=True)
    s = Cadical195(bootstrap_with=cnf)
    t0 = time.time()
    res = s.solve()
    print(f"RESULT: {'SAT' if res else 'UNSAT'}   ({time.time()-t0:.1f}s)")
    if res:
        mod = set(l for l in s.get_model() if l > 0)
        cert = []
        for f in P:
            for aa in range(f):
                if var[f][aa] in mod:
                    cert.append((f, aa))
                    break
        # independent verification
        cov = bytearray(a.M)
        for q, c in holes:
            for x in range(c % q, a.M, q):
                cov[x] = 1
        for f, b in cert:
            for x in range(b % f, a.M, f):
                cov[x] = 1
        assert len(set(f for f, _ in cert)) == len(cert)
        print(f"  verified uncovered = {a.M - sum(cov)}   moduli used = {len(cert)}  "
              f"weight = {float(sum(Fraction(1,f) for f,_ in cert)):.5f}")
        print(f"  CERT {cert}")


if __name__ == "__main__":
    main()
