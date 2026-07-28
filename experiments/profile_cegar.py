"""profile_cegar.py — the decisive profile computation, with lazy transitivity.

Question: for the PLAIN target (no monotone 4-AP, both orientations), how large can N be
with a linear displacement profile pos(v) <= C*v for all v?  By CORE.md Lemma 6 this is
exactly the finite side of the NO branch restricted to linear profiles; by Theorem 12 it
is impossible for C < 9/8, and Theorem 14 shows increasing-only arguments cannot pass
C = 3.  Contiguous geometric-block architectures of ratio r induce profiles with C ~ r,
so extinction at C = 5 would close route R1's ratio-5 island a priori.

Engine: order encoding (x_{u,w} = "u before w" for u < w) with the AP clauses and the
per-value predecessor-count cardinality constraints, but WITHOUT the O(N^3) transitivity
clauses.  Transitivity is enforced lazily (CEGAR): solve, look for a cycle in the implied
tournament; if one exists, add the triangle clauses that forbid it and re-solve.  On
termination the tournament is acyclic, hence a linear order, and the predecessor counts
are genuine positions.

SAT models are decoded and re-verified with the trusted checker (apcheck.py) and against
the profile bound.  UNSAT is a theorem only modulo solver correctness plus the CEGAR
loop's soundness: note that adding transitivity clauses only REMOVES models, so an UNSAT
at any CEGAR round is already an UNSAT for the full (transitive) system — the lazy loop
is sound for UNSAT at every stage, and complete when it terminates with an acyclic model.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def find_cycles(order_of, N, max_cycles=400):
    """Return vertex-disjoint cycles of the tournament implied by order_of (empty list
    iff acyclic). Kahn peels sources; every surviving vertex has an alive IN-neighbour,
    so a BACKWARD walk always repeats and yields a cycle. Extracting many disjoint cycles
    per CEGAR round (not one) is what makes the loop converge at useful sizes."""
    indeg = [0] * (N + 1)
    adj = [[] for _ in range(N + 1)]
    for u in range(1, N + 1):
        for w in range(u + 1, N + 1):
            if order_of(u, w):
                adj[u].append(w); indeg[w] += 1
            else:
                adj[w].append(u); indeg[u] += 1
    from collections import deque
    q = deque(v for v in range(1, N + 1) if indeg[v] == 0)
    alive = [True] * (N + 1); alive[0] = False
    removed = 0
    while q:
        v = q.popleft(); removed += 1; alive[v] = False
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    if removed == N:
        return []
    rev = [[] for _ in range(N + 1)]
    for u in range(1, N + 1):
        if alive[u]:
            for w in adj[u]:
                if alive[w]:
                    rev[w].append(u)
    cycles, used = [], [False] * (N + 1)
    for start in range(1, N + 1):
        if len(cycles) >= max_cycles:
            break
        if not alive[start] or used[start]:
            continue
        seen, path, cur, ok = {}, [], start, True
        while cur not in seen:
            if used[cur]:
                ok = False; break
            seen[cur] = len(path); path.append(cur)
            nxts = [p for p in rev[cur] if alive[p] and not used[p]]
            if not nxts:
                ok = False; break
            cur = nxts[0]
        if not ok:
            continue
        cyc = path[seen[cur]:]; cyc.reverse()
        for v in cyc:
            used[v] = True
        cycles.append(cyc)
    return cycles


def solve(N, C, max_rounds=200000, verbose=False):
    pool = IDPool()
    def var(u, w):
        return pool.id(('x', u, w))          # u < w ; true means u before w
    def lit(u, w):                            # "u before w" for arbitrary u != w
        return var(u, w) if u < w else -var(w, u)

    cl = []
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            a = [lit(x + k * e, x + (k + 1) * e) for k in range(3)]
            cl.append([-a[0], -a[1], -a[2]])   # no increasing 4-AP
            cl.append([a[0], a[1], a[2]])      # no decreasing 4-AP
    for v in range(1, N + 1):
        bound = int(C * v)
        if bound >= N:
            continue
        lits = [lit(w, v) for w in range(1, N + 1) if w != v]   # "w before v"
        enc = CardEnc.atmost(lits=lits, bound=bound - 1, vpool=pool, encoding=EncType.seqcounter)
        cl.extend(enc.clauses)

    S = Cadical195(bootstrap_with=cl)
    rounds = 0
    while True:
        if not S.solve():
            S.delete()
            return "UNSAT", None, rounds
        model = set(S.get_model())
        def order_of(u, w):                    # u < w assumed
            return var(u, w) in model
        cycs = find_cycles(order_of, N)
        if not cycs:
            import functools
            vals = list(range(1, N + 1))
            def cmp(u, w):
                if u == w: return 0
                before = order_of(u, w) if u < w else (not order_of(w, u))
                return -1 if before else 1
            vals.sort(key=functools.cmp_to_key(cmp))
            S.delete()
            return "SAT", vals, rounds
        for cyc in cycs:
            L = len(cyc)
            for i in range(L):
                u, w, z = cyc[i], cyc[(i + 1) % L], cyc[(i + 2) % L]
                if len({u, w, z}) == 3:
                    S.add_clause([-lit(u, w), -lit(w, z), lit(u, z)])
            S.add_clause([-lit(cyc[i], cyc[(i + 1) % L]) for i in range(L)])
        rounds += 1
        if verbose and rounds % 200 == 0:
            print(f"    [round {rounds}: {len(cycs)} cycles]", flush=True)
        if rounds > max_rounds:
            S.delete()
            return "UNKNOWN", None, rounds


if __name__ == "__main__":
    Cs = [float(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else ["2", "3", "5"])]
    Ns = [int(x) for x in (sys.argv[2].split(",") if len(sys.argv) > 2 else
                           ["60", "90", "130", "180", "250", "350"])]
    for C in Cs:
        for N in Ns:
            t0 = time.time()
            res, perm, rounds = solve(N, C, verbose=True)
            dt = time.time() - t0
            if res == "SAT":
                assert sorted(perm) == list(range(1, N + 1))
                assert not has_monotone_kap_pos(perm, 4), "solver model is not an avoider!"
                pos = {v: i + 1 for i, v in enumerate(perm)}
                assert all(pos[v] <= C * v for v in range(1, N + 1)), "profile violated!"
            print(f"plain C={C} N={N}: {res} ({dt:.0f}s, {rounds} cegar rounds)", flush=True)
            if res == "UNSAT":
                print(f"   ==> EXTINCTION at C={C}, N={N} (inherited for all larger N)", flush=True)
                break
            if res == "UNKNOWN":
                break
