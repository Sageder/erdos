"""
F_maxsat.py -- Route F, Erdos 273, task (a) [and (c)] via weighted MaxSAT.

CLAIM TESTED: exact value of
    X(L,W) = min { sum_i L/n_i - L } over covering systems of Z with pairwise
             distinct moduli n_i > 1, n_i | L, n_i in W,
so that  min sum_i 1/n_i = 1 + X(L,W)/L.

ENCODING.  Boolean x[d][a] = "the class a mod d is used" (d | L, d>1, d in W,
0 <= a < d).
  HARD  cover(r) :  OR_{d} x[d][ r mod d ]                for every r mod L
  HARD  AMO(d)   :  at most one a with x[d][a]            (distinct moduli)
  HARD  sym      :  OR_{d} x[d][0]   -- translation symmetry breaking:
                    every covering system may be translated so that some class
                    has residue 0; translation preserves moduli and cost.
  SOFT  (~x[d][a]) with weight L/d.
The MaxSAT optimum (total weight of falsified soft clauses) equals
sum_i L/n_i = L + X, so X = opt - L.  All arithmetic integral.

Independent verification of the returned system is done by F_mincost.verify.

CONCLUSION: table printed; recorded in attempts/route-F-efficiency/FINDINGS.md.
A value X(L,W) is a theorem about that L and that W only.
"""
import sys, time, json
from fractions import Fraction
from pysat.formula import WCNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2, RC2Stratified
from F_mincost import divisors, WORLDS, verify


def build(L, world="ALL", mods=None):
    if mods is None:
        mods = [d for d in divisors(L) if d > 1 and WORLDS[world](d)]
    pool = IDPool()
    x = {}
    for d in mods:
        for a in range(d):
            x[(d, a)] = pool.id(("x", d, a))
    w = WCNF()
    for r in range(L):
        w.append([x[(d, r % d)] for d in mods])
    for d in mods:
        lits = [x[(d, a)] for a in range(d)]
        if len(lits) > 1:
            enc = CardEnc.atmost(lits=lits, bound=1, vpool=pool,
                                 encoding=EncType.seqcounter)
            for cl in enc.clauses:
                w.append(cl)
    w.append([x[(d, 0)] for d in mods])          # symmetry breaking
    # u[d] = "modulus d is used";  x[d][a] -> u[d].  Only tau(L)-1 soft clauses.
    for d in mods:
        u = pool.id(("u", d))
        for a in range(d):
            w.append([-x[(d, a)], u])
        w.append([-u], weight=L // d)
    return w, x, mods


def solve(L, world="ALL", mods=None, stratified=True, verbose=False):
    w, x, mods = build(L, world, mods)
    if sum(L // d for d in mods) < L:
        return None, None, mods
    t0 = time.time()
    cls = RC2Stratified if stratified else RC2
    with cls(w, solver="cd19" if False else "g4", adapt=True, exhaust=True,
             minz=True) as rc2:
        model = rc2.compute()
        if model is None:
            return None, None, mods
        cost = rc2.cost
    inv = {v: k for k, v in x.items()}
    pos = set(l for l in model if l > 0)
    system = sorted([(d, a) for (d, a), v in x.items() if v in pos])
    if verbose:
        print(f"   rc2 time {time.time()-t0:.1f}s cost={cost}")
    return cost - L, system, mods


def main():
    Ls = [int(t) for t in sys.argv[1].split(",")]
    world = sys.argv[2] if len(sys.argv) > 2 else "ALL"
    out = sys.argv[3] if len(sys.argv) > 3 else None
    res = []
    for L in Ls:
        t0 = time.time()
        try:
            X, system, mods = solve(L, world, verbose=False)
        except MemoryError:
            print(f"L={L} {world}: MEMORY"); continue
        dt = time.time() - t0
        if X is None:
            print(f"L={L:<8} {world:3} #mod={len(mods):<4} INFEASIBLE "
                  f"(no covering with distinct moduli in this world)  [{dt:.1f}s]",
                  flush=True)
            res.append({"L": L, "world": world, "status": "INFEASIBLE",
                        "nmod": len(mods)})
            continue
        chk = verify(L, system, world, L)
        assert chk["distinct"] and chk["all>1"] and chk["divides_L"] \
            and chk["in_world"] and chk["covers_all_residues_mod_L"], (L, chk)
        assert chk["waste"] == X, (chk, X)
        mu = Fraction(L + X, L)
        print(f"L={L:<8} {world:3} #mod={len(mods):<4} X={X:<5} mu={mu} = "
              f"{float(mu):.9f}  k={len(system)}  [{dt:.1f}s]", flush=True)
        print("    " + ", ".join(f"{a} mod {d}" for d, a in system), flush=True)
        res.append({"L": L, "world": world, "status": "OK", "X": X,
                    "mu": str(mu), "mu_f": float(mu), "nmod": len(mods),
                    "system": system, "verified": True, "secs": dt})
    if out:
        json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
