"""certify_unsat.py -- independent SAT certification of the PLAIN linear-profile
extinction points found by CP-SAT.

Encoding (independent of the CP-SAT model of plain_extinct.py): the ORDER encoding of
experiments/sat_order.py -- Boolean x[u,w] ("u before w") for u<w, full transitivity,
one 3-clause per (x,e) per orientation, plus a sequential-counter cardinality
constraint pos(v) <= floor(C v) for each value v.

For each (C, N) we check:
  * N-1 : must be SAT, and the decoded model is re-verified with experiments/apcheck.py
          (trusted brute-force-validated checker) and against the profile;
  * N   : must be UNSAT, confirmed by TWO independent solvers (Cadical195, Glucose42),
          with a DRUP proof emitted by Cadical for the record.
"""

import sys, os, time
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
from apcheck import has_monotone_kap_pos
from sat_order import build, decode
from pysat.solvers import Cadical195, Glucose42


def instance(N, C):
    pin = {v: (C.numerator * v) // C.denominator for v in range(1, N + 1)}
    for v, b in pin.items():
        if b < 1:
            return None, None, None, None
    cl, pool, var = build(N, inc4=True, dec4=True, dec3=False, pinning=pin)
    return cl, pool, var, pin


def run(N, C, proof_path=None):
    cl, pool, var, pin = instance(N, C)
    if cl is None:
        return "UNSAT(trivial: floor(Cv)=0)", None, 0, 0
    nv = pool.top
    t0 = time.time()
    S = Cadical195(bootstrap_with=cl, with_proof=(proof_path is not None))
    sat1 = S.solve()
    model = S.get_model() if sat1 else None
    proof = S.get_proof() if (proof_path and not sat1) else None
    S.delete()
    t1 = time.time() - t0
    t0 = time.time()
    G = Glucose42(bootstrap_with=cl)
    sat2 = G.solve()
    G.delete()
    t2 = time.time() - t0
    assert sat1 == sat2, ("SOLVER DISAGREEMENT", N, C, sat1, sat2)
    if sat1:
        perm = decode(model, N, var)
        assert sorted(perm) == list(range(1, N + 1))
        assert not has_monotone_kap_pos(perm, 4), "decoded model has a monotone 4-AP"
        pos = {v: i + 1 for i, v in enumerate(perm)}
        for v in range(1, N + 1):
            assert pos[v] <= pin[v], (v, pos[v], pin[v])
        return "SAT", perm, len(cl), nv, t1, t2
    if proof and proof_path:
        with open(proof_path, "w") as f:
            f.write("\n".join(proof) + "\n")
    return "UNSAT", None, len(cl), nv, t1, t2


if __name__ == "__main__":
    jobs = []
    for a in sys.argv[1:]:
        C_s, N_s = a.split("@")
        jobs.append((Fraction(C_s), int(N_s)))
    if not jobs:
        jobs = [(Fraction(3, 2), 14), (Fraction(3, 2), 15),
                (Fraction(7, 4), 30), (Fraction(7, 4), 31)]
    for C, N in jobs:
        pp = None
        base = f"/home/user/erdos/attempts/route-R19-lp-sharpening/proof_C{C.numerator}_{C.denominator}_N{N}.drup"
        pp = base
        res = run(N, C, proof_path=pp)
        st = res[0]
        if st == "SAT":
            _, perm, ncl, nv, t1, t2 = res
            print(f"C={C} N={N}: SAT  ({ncl} clauses, {nv} vars; cadical {t1:.1f}s, "
                  f"glucose {t2:.1f}s)  witness verified by apcheck + profile\n"
                  f"    perm = {perm}", flush=True)
            if os.path.exists(pp):
                os.remove(pp)
        else:
            _, _, ncl, nv, t1, t2 = res
            sz = os.path.getsize(pp) if os.path.exists(pp) else 0
            print(f"C={C} N={N}: UNSAT  ({ncl} clauses, {nv} vars; cadical {t1:.1f}s, "
                  f"glucose {t2:.1f}s AGREE)  DRUP proof {sz} bytes -> {pp}", flush=True)
