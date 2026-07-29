"""tension8.py — joint delay + within-class-order search, descent condition widened.

Background. CORE Prop 29: a progression along which the class function is eventually
non-decreasing ("tame") has only LINEAR displacement, which the certified extinctions make
fatal. So a class architecture that could be a counterexample must have NO tame progression.

My first version of this experiment (tension.py) imposed the descent rate only for
progressions of step <= 4, and its solutions turned out to have TAME progressions at step 6
— i.e. the constraint was too weak and the SAT result did not mean what it appeared to.
This version widens the descent requirement to step <= 8 and, for every SAT model, REPORTS
the tame progressions up to step 12, so the result cannot be over-read again.

Every SAT model is re-verified 4-AP-free against the trusted checker.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from tension import build, blk
from profile_cegar import find_cycles
from pysat.solvers import Cadical195


def solve(N, b=3, T=1, Q=8, L=10, max_rounds=200000):
    cl, pool, X, D = build(N, b, T, Q, L)
    lit = lambda u, w: X(u, w) if u < w else -X(w, u)
    S = Cadical195(bootstrap_with=cl)
    rounds = 0
    while True:
        if not S.solve():
            S.delete()
            return "UNSAT", None, rounds
        model = set(S.get_model())
        order_of = lambda u, w: X(u, w) in model
        cycs = find_cycles(order_of, N)
        if not cycs:
            import functools
            vals = sorted(range(1, N + 1), key=functools.cmp_to_key(
                lambda u, w: -1 if (order_of(u, w) if u < w else not order_of(w, u)) else 1))
            t = {v: next(k for k in range(T + 1) if D(v, k) in model) for v in range(1, N + 1)}
            S.delete()
            return "SAT", (vals, t), rounds
        for cyc in cycs:
            Lc = len(cyc)
            for i in range(Lc):
                u, w, z = cyc[i], cyc[(i + 1) % Lc], cyc[(i + 2) % Lc]
                if len({u, w, z}) == 3:
                    S.add_clause([-lit(u, w), -lit(w, z), lit(u, z)])
            S.add_clause([-lit(cyc[i], cyc[(i + 1) % Lc]) for i in range(Lc)])
        rounds += 1
        if rounds > max_rounds:
            S.delete()
            return "UNKNOWN", None, rounds


def tame_progressions(t, N, b=3, upto=12):
    c = {v: blk(v, b) + t[v] for v in range(1, N + 1)}
    out = []
    for q in range(1, upto + 1):
        for r in range(1, q + 1):
            P = [v for v in range(r, N + 1, q)]
            if len(P) < 8:
                continue
            tail = P[len(P) // 2:]
            if all(c[tail[i]] <= c[tail[i + 1]] for i in range(len(tail) - 1)):
                out.append((q, r))
    return out


if __name__ == "__main__":
    for T in (1, 2, 3):
        for N in (60, 100, 150, 220, 300):
            t0 = time.time()
            res, out, rd = solve(N, T=T)
            dt = time.time() - t0
            if res == "SAT":
                perm, t = out
                assert sorted(perm) == list(range(1, N + 1))
                assert not has_monotone_kap_pos(perm, 4), "model is NOT 4-AP-free!"
                tm = tame_progressions(t, N)
                print(f"T={T} N={N}: SAT ({dt:.0f}s, {rd} rounds) verified 4-AP-free; "
                      f"tame progressions up to step 12: {tm if tm else 'NONE'}", flush=True)
            else:
                print(f"T={T} N={N}: {res} ({dt:.0f}s, {rd} rounds)", flush=True)
                break
