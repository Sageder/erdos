"""vlogv_probe.py — the decisive NO-side feasibility test.

By CORE.md Lemma 6, 196-NO needs SOME profile phi with phi-bounded monotone-4-AP-free
permutations of [1..N] for EVERY N. Linear profiles are certified dead up to C = 2
(N* = 90), and Remark 17 argues the natural surviving candidate is phi(v) ~ v log v.
Note phi(v) = v*log2(v) exceeds N once v > ~N/log N, so on a board of size N the
constraint bites only on the smaller values — exactly where the shallow probes found
avoiders alive. This script asks SAT directly, at growing N.

Profiles tested: phi(v) = max(1, floor(v*log2(v))) and the tamer floor(v*log2(v)/2).
Engine: lazy-transitivity CEGAR (validated against exhaustive enumeration at C=1.5, 1.75
and against an eager two-solver encoding).
"""
import sys, time, math
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from profile_cegar import find_cycles

def solve_phi(N, phi, max_rounds=200000, verbose=False):
    pool = IDPool()
    def var(u, w): return pool.id(('x', u, w))
    def lit(u, w): return var(u, w) if u < w else -var(w, u)
    cl = []
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            a = [lit(x + k * e, x + (k + 1) * e) for k in range(3)]
            cl.append([-a[0], -a[1], -a[2]]); cl.append([a[0], a[1], a[2]])
    bites = 0
    for v in range(1, N + 1):
        b = min(N, max(1, int(phi(v))))
        if b >= N: continue
        bites += 1
        lits = [lit(w, v) for w in range(1, N + 1) if w != v]
        cl.extend(CardEnc.atmost(lits=lits, bound=b - 1, vpool=pool,
                                 encoding=EncType.seqcounter).clauses)
    S = Cadical195(bootstrap_with=cl); rounds = 0
    while True:
        if not S.solve():
            S.delete(); return "UNSAT", None, rounds, bites
        model = set(S.get_model())
        def order_of(u, w): return var(u, w) in model
        cycs = find_cycles(order_of, N)
        if not cycs:
            import functools
            vals = list(range(1, N + 1))
            def cmp(u, w):
                if u == w: return 0
                before = order_of(u, w) if u < w else (not order_of(w, u))
                return -1 if before else 1
            vals.sort(key=functools.cmp_to_key(cmp)); S.delete()
            return "SAT", vals, rounds, bites
        for cyc in cycs:
            L = len(cyc)
            for i in range(L):
                u, w, z = cyc[i], cyc[(i+1) % L], cyc[(i+2) % L]
                if len({u, w, z}) == 3:
                    S.add_clause([-lit(u, w), -lit(w, z), lit(u, z)])
            S.add_clause([-lit(cyc[i], cyc[(i+1) % L]) for i in range(L)])
        rounds += 1
        if rounds > max_rounds:
            S.delete(); return "UNKNOWN", None, rounds, bites

if __name__ == "__main__":
    profiles = [("v*log2(v)", lambda v: v * math.log2(v) if v > 1 else 1),
                ("v*log2(v)/2", lambda v: v * math.log2(v) / 2 if v > 1 else 1)]
    for name, phi in profiles:
        for N in (60, 100, 150, 250, 400):
            t0 = time.time(); r, p, rd, bites = solve_phi(N, phi); dt = time.time() - t0
            if p:
                assert sorted(p) == list(range(1, N+1)) and not has_monotone_kap_pos(p, 4)
                pos = {v: i+1 for i, v in enumerate(p)}
                assert all(pos[v] <= max(1, int(phi(v))) for v in range(1, N+1)), "profile violated"
            print(f"phi={name} N={N}: {r} ({dt:.0f}s, {rd} rounds, {bites} values constrained)", flush=True)
            if r != "SAT": break
