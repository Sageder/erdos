"""localize.py -- shrink the pair obstruction: value-window localisation and a
clause-level MUS of the TOP system.  Every relaxation here only DROPS clauses,
so each UNSAT remains a theorem.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys
from pysat.solvers import Solver


def topclauses(W, U, M, lo, hi):
    """clauses of TOP(W,U,M) restricted to order variables in [lo,hi] (inside C)."""
    S = wsys.Sys((W, U), M, window=(lo, hi))
    cls, dead = S.clauses(transitivity=False)
    return S, cls, dead


def decide(W, U, M, lo, hi, solver='cadical195'):
    S = wsys.Sys((W, U), M, window=(lo, hi))
    v, _ = wsys.solve_lazy(S, time_cap=600, solver=solver)
    return 'UNSAT' if v == 'GEOM_DEAD' else v


def mus(W, U, M, lo, hi):
    """clause-level deletion MUS with eager transitivity as hard background."""
    S = wsys.Sys((W, U), M, window=(lo, hi))
    soft, dead = S.clauses(transitivity=False)
    hard = S.trans_clauses()
    if dead:
        return S, [], dead
    with Solver(name='cadical195', bootstrap_with=hard + soft) as s:
        assert not s.solve(), "not UNSAT"
    keep = list(soft)
    i = 0
    while i < len(keep):
        trial = keep[:i] + keep[i + 1:]
        with Solver(name='cadical195', bootstrap_with=hard + trial) as s:
            if not s.solve():
                keep = trial
            else:
                i += 1
    return S, keep, []


def describe(S, W, U, cls):
    """classify each MUS clause back into (a)/(b)/(c)."""
    id2 = {t: p for p, t in S.vid.items()}
    out = []
    for c in cls:
        pairs = [(id2[abs(l)], l > 0) for l in c]
        out.append(pairs)
    return out


if __name__ == '__main__':
    job = sys.argv[1]
    W, U, M = 10, 28, 82
    if job == 'window':
        print(f"# TOP({W},{U},{M}) value-window localisation (C = [{U+1},{M}])")
        for hi in range(40, M + 1, 4):
            r = decide(W, U, M, U + 1, hi)
            print(f"   window [{U+1},{hi}] -> {r}", flush=True)
            if r == 'UNSAT':
                for lo in range(U + 1, hi):
                    r2 = decide(W, U, M, lo, hi)
                    if r2 != 'UNSAT':
                        print(f"   tight lower end: [{lo-1},{hi}] UNSAT, "
                              f"[{lo},{hi}] {r2}", flush=True)
                        break
                break
    elif job == 'mus':
        lo, hi = int(sys.argv[2]), int(sys.argv[3])
        t0 = time.time()
        S, keep, dead = mus(W, U, M, lo, hi)
        print(f"# MUS of TOP({W},{U},{M}) on window [{lo},{hi}]: "
              f"{len(keep)} clauses [{time.time()-t0:.0f}s]")
        forced = [c for c in keep if len(c) == 1]
        print(f"#   unit (forced-inversion) clauses: {len(forced)}")
        id2 = {t: p for p, t in S.vid.items()}
        for c in sorted(keep, key=len):
            txt = ' | '.join(
                (f"{id2[abs(l)][0]}<{id2[abs(l)][1]}" if l > 0
                 else f"{id2[abs(l)][1]}<{id2[abs(l)][0]}") for l in c)
            print(f"    {txt}")
