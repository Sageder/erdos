"""calib.py — cross-validate the independent cutsys encoder against route-R1's
published verdicts (windows.log / windows2.log / windows3.log / island_edges.log).

Small instances: EAGER transitivity + two different SAT solvers + CP-SAT integer
model (three engines, two paradigms).  SAT witnesses re-verified with the trusted
checker experiments/apcheck.py.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_pysat, solve_cpsat, verify_witness_full

EXPECT = [
    ([2, 8, 22], 'SAT'), ([2, 8, 80], 'SAT'),
    ([4, 16, 46], 'SAT'), ([4, 16, 54], 'SAT'), ([4, 16, 56], 'UNSAT'),
    ([4, 16, 60], 'UNSAT'), ([4, 16, 66], 'UNSAT'), ([4, 16, 68], 'SAT'),
    ([6, 20, 62], 'SAT'), ([6, 20, 64], 'UNSAT'), ([6, 20, 86], 'UNSAT'),
    ([8, 26, 76], 'SAT'), ([8, 26, 78], 'UNSAT'), ([8, 26, 80], 'UNSAT'),
    ([8, 26, 100], 'UNSAT'), ([8, 26, 120], 'UNSAT'),
    ([8, 20, 100], 'UNSAT'), ([7, 20, 100], 'SAT'),
    ([2, 26, 76], 'SAT'), ([2, 26, 90], 'SAT'),
]


def run(cuts, engines=('cadical195', 'glucose42', 'minisat22')):
    s = CutSystem(cuts)
    t0 = time.time()
    cls, dead = s.clauses(transitivity=True)
    if dead:
        return 'GEOM_DEAD', {}, time.time() - t0
    res = {}
    for e in engines:
        r, model = solve_pysat(cls, s.nvars, solver_name=e)
        res[e] = r
        if r == 'SAT' and e == engines[0]:
            val = {abs(l): (l > 0) for l in model}
            order = extract(s, val)
            verify_witness_full(cuts, order)
            res['witness_verified'] = True
    r2, _ = solve_cpsat(s)
    res['cpsat'] = r2
    verdicts = set(v for k, v in res.items() if k != 'witness_verified')
    return (verdicts.pop() if len(verdicts) == 1 else f"DISAGREE {res}"), res, time.time() - t0


def extract(s, val):
    import functools
    V = s.V
    out = []
    byblock = {}
    for v in range(1, V + 1):
        byblock.setdefault(s.seg(v), []).append(v)
    for j in sorted(byblock):
        vals = byblock[j]

        def cmp(a, b):
            if a == b:
                return 0
            t = s.lit(a, b)
            before = val[t] if t > 0 else (not val[-t])
            return -1 if before else 1
        vals.sort(key=functools.cmp_to_key(cmp))
        out.extend(vals)
    return out


if __name__ == "__main__":
    ok = True
    for cuts, exp in EXPECT:
        v, res, dt = run(cuts)
        mark = "OK " if v == exp else "MISMATCH"
        if v != exp:
            ok = False
        print(f"{mark} cuts={cuts} mine={v} R1={exp}  ({dt:.1f}s) {res}", flush=True)
    print("CALIB", "ALL AGREE" if ok else "DISAGREEMENT FOUND", flush=True)
