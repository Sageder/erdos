"""
F_sat_exists.py -- Route F, Erdos 273, task (c).

CLAIM TESTED: for a given L and world W in {ALL, E, H}, does there EXIST a
covering system of Z with pairwise distinct moduli > 1, all dividing L and
lying in W?  Encoded as plain SAT:
    x[d][a]  = "class a mod d is used"       (d | L, d > 1, d in W, 0<=a<d)
    HARD  cover(r): OR_d x[d][ r mod d ]     for every r = 0..L-1
    HARD  AMO(d)  : at most one a per d      (moduli pairwise distinct)
    HARD  sym     : OR_d x[d][0]             (translation symmetry breaking --
                    every covering may be translated so some class has residue 0)
SAT  <=> such a covering system exists.  UNSAT is a complete proof for that L.

Any SAT model is re-verified independently (exhaustive sweep mod L).

CONCLUSION: printed; recorded in attempts/route-F-efficiency/FINDINGS.md.
"""
import sys, time
from fractions import Fraction
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
from F_mincost import divisors, WORLDS, verify


def build(L, mods):
    pool = IDPool()
    x = {}
    for d in mods:
        for a in range(d):
            x[(d, a)] = pool.id(("x", d, a))
    cnf = CNF()
    for r in range(L):
        cnf.append([x[(d, r % d)] for d in mods])
    for d in mods:
        lits = [x[(d, a)] for a in range(d)]
        if len(lits) > 1:
            for cl in CardEnc.atmost(lits=lits, bound=1, vpool=pool,
                                     encoding=EncType.seqcounter).clauses:
                cnf.append(cl)
    cnf.append([x[(d, 0)] for d in mods])
    return cnf, x


def exists(L, world="ALL", mods=None, solver="cd15", timeout=None):
    if mods is None:
        mods = [d for d in divisors(L) if d > 1 and WORLDS[world](d)]
    B = sum(Fraction(1, d) for d in mods)
    if B <= 1:
        return False, None, mods, B, "budget<=1"
    cnf, x = build(L, mods)
    with Solver(name=solver, bootstrap_with=cnf.clauses) as s:
        r = s.solve()
        if not r:
            return False, None, mods, B, "UNSAT"
        model = set(l for l in s.get_model() if l > 0)
    system = sorted([(d, a) for (d, a), v in x.items() if v in model])
    return True, system, mods, B, "SAT"


def main():
    world = sys.argv[1]
    Ls = sys.argv[2]
    if ":" in Ls:
        lo, hi = Ls.split(":")
        Ls = range(int(lo), int(hi) + 1)
    else:
        Ls = [int(t) for t in Ls.split(",")]
    for L in Ls:
        mods = [d for d in divisors(L) if d > 1 and WORLDS[world](d)]
        B = sum(Fraction(1, d) for d in mods)
        if B <= 1:
            continue
        t0 = time.time()
        ok, system, mods, B, st = exists(L, world, mods)
        dt = time.time() - t0
        if ok:
            chk = verify(L, system, world, L)
            assert chk["distinct"] and chk["all>1"] and chk["divides_L"] \
                and chk["in_world"] and chk["covers_all_residues_mod_L"], (L, chk)
            mu = chk["sum_reciprocals"]
            print(f"*** L={L:<9}{world} B={float(B):.4f} #mod={len(mods):<3} SAT "
                  f"k={len(system)} cost={mu}={float(mu):.6f} waste={chk['waste']} "
                  f"[{dt:.1f}s]", flush=True)
            print("      " + ", ".join(f"{a} mod {d}" for d, a in system), flush=True)
        else:
            print(f"L={L:<9}{world} B={float(B):.4f} #mod={len(mods):<3} {st} "
                  f"[{dt:.1f}s]", flush=True)


if __name__ == "__main__":
    main()
