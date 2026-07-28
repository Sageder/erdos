"""sat_height.py — mission item 2: SAT with EXTRA forcing constraints.

Constraint HEIGHT(K): the forcing digraph of the board (edges u -> u+d for u open at
scale d, target inside the board) has no directed path with K+1 edges, i.e. h(u) <= K
for every u.  Note |Cl(u)| <= B implies h(u) <= B-1, and h(u) <= K bounds closures by
the branching; height is the encodable proxy for "closures stay small".

Encoding on top of experiments/sat_order.py's order variables:
  op[u,d]  with  x[u-2d,u-d] AND x[u-d,u] -> op[u,d]              (definition, one way:
           op only occurs positively here and negatively below, so a solver always may
           take the minimal op, making the encoding sound AND complete)
  H[u,i]   "h(u) >= i", i = 1..K
  op[u,d] -> H[u,1] ;  op[u,d] & H[u+d,i] -> H[u,i+1] ;  NOT(op[u,d] & H[u+d,K])

WARNING (proved in REPORT.md, Prop R18.1): the parity permutation sigma_N is 4-AP-free
with NO open value at all, so HEIGHT(K) alone is SAT for every K >= 0 and every N.
Any informative experiment must ALSO impose a displacement profile pos(v) <= C*v
(CORE.md Lemma 6).  This script therefore always runs the two knobs together.
"""

import sys, time, math
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from sat_order import build, decode                       # noqa: E402
from apcheck import has_monotone_kap_pos                  # noqa: E402
from forcing_tools import board_stats, closures_and_heights  # noqa: E402
from pysat.solvers import Cadical195, Glucose42           # noqa: E402
from pysat.card import CardEnc, EncType                   # noqa: E402


def solve(N, K=None, C=None, solver="cadical", timeout_note=None):
    cl, pool, var = build(N, inc4=True, dec4=True)
    if K is not None:
        for u in range(3, N + 1):
            for d in range(1, (u - 1) // 2 + 1):
                if u + d > N:
                    continue
                x1, x2 = var(u - 2 * d, u - d), var(u - d, u)
                if K == 0:
                    cl.append([-x1, -x2])
                    continue
                op = pool.id(('op', u, d))
                cl.append([-x1, -x2, op])
                cl.append([-op, pool.id(('H', u, 1))])
                for i in range(1, K):
                    cl.append([-op, -pool.id(('H', u + d, i)), pool.id(('H', u, i + 1))])
                cl.append([-op, -pool.id(('H', u + d, K))])
        for u in range(1, N + 1):        # monotone H
            for i in range(1, K):
                cl.append([-pool.id(('H', u, i + 1)), pool.id(('H', u, i))])
    if C is not None:
        for v in range(1, N + 1):
            bound = math.ceil(C * v)
            if bound >= N:
                continue
            lits = []
            for w in range(1, N + 1):
                if w == v:
                    continue
                lits.append(var(min(v, w), max(v, w)) * (1 if w < v else -1))
            enc = CardEnc.atmost(lits=lits, bound=bound - 1, vpool=pool,
                                 encoding=EncType.seqcounter)
            cl.extend(enc.clauses)
    S = Cadical195(bootstrap_with=cl) if solver == "cadical" else Glucose42(bootstrap_with=cl)
    t0 = time.time()
    sat = S.solve()
    dt = time.time() - t0
    perm = decode(S.get_model(), N, var) if sat else None
    S.delete()
    if perm:
        assert not has_monotone_kap_pos(perm, 4), "checker disagrees"
        st = board_stats(perm)
        if K is not None:
            assert st['max_height'] <= K, (K, st)
        if C is not None:
            pos = {v: i + 1 for i, v in enumerate(perm)}
            assert all(pos[v] <= math.ceil(C * v) for v in range(1, N + 1))
    return ("SAT" if sat else "UNSAT"), dt, perm


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "grid"
    if what == "vacuity":
        # HEIGHT(K) with no profile: SAT at every N (parity)
        for K in (0, 1, 2):
            for N in (20, 40, 60):
                st, dt, perm = solve(N, K=K, C=None)
                print(f"HEIGHT({K}) alone, N={N}: {st} ({dt:.1f}s)", flush=True)
    else:
        Ks = [None, 0, 1, 2, 3]
        for C in (1.5, 2, 3):
            for K in Ks:
                lastsat = None
                for N in (10, 14, 18, 22, 26, 30, 36, 44, 54, 66, 80):
                    st, dt, perm = solve(N, K=K, C=C)
                    tag = "none" if K is None else str(K)
                    print(f"C={C} HEIGHT={tag} N={N}: {st} ({dt:.1f}s)", flush=True)
                    if st == "UNSAT":
                        break
                    lastsat = N
                    if dt > 90:
                        print(f"   (stopping: last SAT N={N}, getting slow)", flush=True)
                        break
