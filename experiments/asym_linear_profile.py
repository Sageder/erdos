"""asym_linear_profile.py — probe: do asym witnesses (no dec-3AP, no inc-4AP) of [1..N]
exist with the linear displacement profile pos(v) <= C*v for ALL v?

Why it matters (CORE.md Lemma 6, applied to the hereditary family {dec-3AP, inc-4AP,
profile bound}): if for some fixed C this is SAT for EVERY N, then an infinite
asymmetric witness exists, hence 196-NO. SAT results here are evidence about which C
to target (or that no linear C works — steering to superlinear profiles).

Also runs the plain (both-orientation 4-AP-free) variant for comparison at one C.
Encoding: order variables + transitivity + AP clauses (sat_order.build) + atmost
cardinality for pos(v) <= C*v (only for v with C*v < N).
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from sat_order import build, decode, check_perm
from apcheck import has_monotone_kap_pos
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def solve_profile(N, C, dec3=True, inc4=True, dec4=False, timeout_note=None):
    cl, pool, var = build(N, inc4=inc4, dec4=dec4, dec3=dec3)
    for v in range(1, N + 1):
        bound = C * v
        if bound >= N:
            continue
        lits = []
        for w in range(1, N + 1):
            if w == v:
                continue
            lits.append(var(min(v, w), max(v, w)) * (1 if w < v else -1))
        enc = CardEnc.atmost(lits=lits, bound=bound - 1, vpool=pool, encoding=EncType.seqcounter)
        cl.extend(enc.clauses)
    S = Cadical195(bootstrap_with=cl)
    sat = S.solve()
    perm = decode(S.get_model(), N, var) if sat else None
    S.delete()
    if perm:
        assert check_perm(perm, inc4=inc4, dec4=dec4, dec3=dec3)
        assert not has_monotone_kap_pos(perm, 4)
        pos = {v: i + 1 for i, v in enumerate(perm)}
        assert all(pos[v] <= C * v for v in range(1, N + 1)), "profile violated"
    return sat, perm


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "asym"
    Cs = [2, 3, 5]
    Ns = [30, 45, 60, 80, 100, 130, 160]
    if mode == "asym":
        for C in Cs:
            for N in Ns:
                t0 = time.time()
                sat, perm = solve_profile(N, C, dec3=True, inc4=True, dec4=False)
                dt = time.time() - t0
                print(f"asym C={C} N={N}: {'SAT' if sat else 'UNSAT'} ({dt:.1f}s)"
                      + (f" head={perm[:14]}" if sat else "  <-- extinction for this (C,N)"),
                      flush=True)
                if not sat:
                    break
    else:  # plain
        C = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        for N in Ns:
            t0 = time.time()
            sat, perm = solve_profile(N, C, dec3=False, inc4=True, dec4=True)
            dt = time.time() - t0
            print(f"plain C={C} N={N}: {'SAT' if sat else 'UNSAT'} ({dt:.1f}s)"
                  + (f" head={perm[:14]}" if sat else "  <-- extinction for this (C,N)"),
                  flush=True)
            if not sat:
                break
