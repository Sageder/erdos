"""mus_profile.py — which profile constraints actually drive extinction?

Instance: asym target (no dec-3AP + no inc-4AP) on [1..N], N = 34, with per-value
selector-guarded cardinality constraints pos(v) <= ceil(C*v), C = 2. The unguarded
instance is UNSAT (threshold campaign). Here each value v's profile constraint gets a
selector s_v; solving under assumptions {s_v : v in S} tests whether constraining only
S suffices for UNSAT. Deletion-based minimization over v = N..1 yields a minimal
sufficient set S* (a group-MUS w.r.t. profile groups).

Output: S* and the induced statement: "no asym witness of [1..N] has pos(v) <= 2v for
all v in S*" — a FIN-type finite theorem candidate for hand analysis.
Also run for plain target at its C=2 threshold once known (arg 'plain N').
"""

import sys, math, time
sys.path.insert(0, '/home/user/erdos/experiments')
from sat_order import build
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def build_guarded(N, C, dec3, inc4, dec4):
    cl, pool, var = build(N, inc4=inc4, dec4=dec4, dec3=dec3)
    sel = {}
    for v in range(1, N + 1):
        bound = math.ceil(C * v)
        if bound >= N:
            continue
        s = pool.id(('sel', v))
        sel[v] = s
        lits = []
        for w in range(1, N + 1):
            if w == v:
                continue
            lits.append(var(min(v, w), max(v, w)) * (1 if w < v else -1))
        enc = CardEnc.atmost(lits=lits, bound=bound - 1, vpool=pool, encoding=EncType.seqcounter)
        for c in enc.clauses:
            cl.append([-s] + c)     # constraint active only when selector true
    return cl, sel


def group_mus(N, C, dec3, inc4, dec4):
    cl, sel = build_guarded(N, C, dec3, inc4, dec4)
    S = Cadical195(bootstrap_with=cl)
    active = sorted(sel)
    assert not S.solve(assumptions=[sel[v] for v in active]), "instance is SAT with all profile constraints!?"
    # deletion-based minimization (drop from large v down, then a second pass)
    changed = True
    while changed:
        changed = False
        for v in sorted(active, reverse=True):
            trial = [u for u in active if u != v]
            if not S.solve(assumptions=[sel[u] for u in trial]):
                active = trial
                changed = True
    S.delete()
    return active


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "asym"
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 34
    C = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    t0 = time.time()
    if mode == "asym":
        core = group_mus(N, C, dec3=True, inc4=True, dec4=False)
    else:
        core = group_mus(N, C, dec3=False, inc4=True, dec4=True)
    print(f"{mode} N={N} C={C}: minimal sufficient profile-constraint set "
          f"({len(core)} values): {core}  [{time.time()-t0:.1f}s]", flush=True)
    print("Statement: no", mode, f"witness of [1..{N}] satisfies pos(v) <= ceil({C}v) "
          f"for all v in the listed set.")
