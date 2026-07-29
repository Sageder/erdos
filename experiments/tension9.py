"""tension9.py — joint delay + within-class-order search, with CONSTRAINT AND CHECK
IDENTICAL BY CONSTRUCTION.

Two earlier versions of this experiment (tension.py, tension8.py) reported SAT models that
had tame progressions, because the imposed constraint and the tameness check used different
criteria and different scopes:
  - tension.py  constrained steps <= 4 only; solutions were tame at step 6.
  - tension8.py constrained steps <= 8 but skipped progressions with < L+2 elements, while
    the check accepted progressions with >= 8; and "a descent in every window of L" does not
    imply "the tail has a descent" unless the progression is long enough to contain a whole
    window inside its tail (len >= 2L, i.e. N >= 2Lq).

Here the property is ONE definition, used both as the SAT constraint and as the verification:

    NO-FLAT(Q, L):  for every progression of step q <= Q and every window of L consecutive
                    elements of it, the class function c has at least one strict descent
                    inside that window.

and we only test (N, q) with N >= 2*L*q, so every progression tested is long enough for the
property to have content. NO-FLAT is a genuine RATE condition and is exactly what a
non-tame architecture must satisfy at the tested scales (a tame progression is eventually
non-decreasing, so its tail contains arbitrarily long descent-free windows).

Every SAT model is re-verified: it is a permutation, it is monotone-4-AP-free (trusted
checker), and it satisfies NO-FLAT as re-checked from the decoded delay.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from tension import blk
from profile_cegar import find_cycles
from pysat.solvers import Cadical195
from pysat.formula import IDPool


def build(N, b=3, T=1, Q=6, L=8):
    pool = IDPool(); cl = []
    X = lambda u, w: pool.id(('x', u, w))
    lit = lambda u, w: X(u, w) if u < w else -X(w, u)
    D = lambda v, k: pool.id(('d', v, k))
    for v in range(1, N + 1):
        cl.append([D(v, k) for k in range(T + 1)])
        for k1 in range(T + 1):
            for k2 in range(k1 + 1, T + 1):
                cl.append([-D(v, k1), -D(v, k2)])
    for u in range(1, N + 1):
        ju = blk(u, b)
        for w in range(1, N + 1):
            if u == w: continue
            jw = blk(w, b)
            for ku in range(T + 1):
                for kw in range(T + 1):
                    if ju + ku < jw + kw:
                        cl.append([-D(u, ku), -D(w, kw), lit(u, w)])
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            a = [lit(x + k * e, x + (k + 1) * e) for k in range(3)]
            cl.append([-a[0], -a[1], -a[2]]); cl.append([a[0], a[1], a[2]])
    # NO-FLAT(Q, L), imposed only where it has content (N >= 2*L*q)
    tested = []
    for q in range(1, Q + 1):
        if N < 2 * L * q:
            continue
        tested.append(q)
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            for s0 in range(0, len(P) - L + 1):
                W = P[s0:s0 + L]; lits = []
                for i in range(len(W) - 1):
                    u, w = W[i], W[i + 1]
                    z = pool.id(('ds', q, r, s0, i))
                    for ku in range(T + 1):
                        for kw in range(T + 1):
                            if not (blk(u, b) + ku > blk(w, b) + kw):
                                cl.append([-z, -D(u, ku), -D(w, kw)])
                    lits.append(z)
                cl.append(lits)
    return cl, pool, X, D, tested


def check_noflat(t, N, tested, b=3, L=8):
    """Re-verify NO-FLAT from the decoded delay, with the SAME definition."""
    c = {v: blk(v, b) + t[v] for v in range(1, N + 1)}
    bad = []
    for q in tested:
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            for s0 in range(0, len(P) - L + 1):
                W = P[s0:s0 + L]
                if all(c[W[i]] <= c[W[i + 1]] for i in range(len(W) - 1)):
                    bad.append((q, r, W[0]))
    return bad


def solve(N, b=3, T=1, Q=6, L=8, max_rounds=200000):
    cl, pool, X, D, tested = build(N, b, T, Q, L)
    lit = lambda u, w: X(u, w) if u < w else -X(w, u)
    S = Cadical195(bootstrap_with=cl); rounds = 0
    while True:
        if not S.solve():
            S.delete(); return "UNSAT", None, rounds, tested
        model = set(S.get_model())
        order_of = lambda u, w: X(u, w) in model
        cycs = find_cycles(order_of, N)
        if not cycs:
            import functools
            vals = sorted(range(1, N + 1), key=functools.cmp_to_key(
                lambda u, w: -1 if (order_of(u, w) if u < w else not order_of(w, u)) else 1))
            t = {v: next(k for k in range(T + 1) if D(v, k) in model) for v in range(1, N + 1)}
            S.delete(); return "SAT", (vals, t), rounds, tested
        for cyc in cycs:
            Lc = len(cyc)
            for i in range(Lc):
                u, w, z = cyc[i], cyc[(i + 1) % Lc], cyc[(i + 2) % Lc]
                if len({u, w, z}) == 3:
                    S.add_clause([-lit(u, w), -lit(w, z), lit(u, z)])
            S.add_clause([-lit(cyc[i], cyc[(i + 1) % Lc]) for i in range(Lc)])
        rounds += 1
        if rounds > max_rounds:
            S.delete(); return "UNKNOWN", None, rounds, tested


if __name__ == "__main__":
    for T in (1, 2):
        for N in (100, 150, 220, 300, 400):
            t0 = time.time(); res, out, rd, tested = solve(N, T=T); dt = time.time() - t0
            if res == "SAT":
                perm, t = out
                assert sorted(perm) == list(range(1, N + 1))
                assert not has_monotone_kap_pos(perm, 4), "model is NOT 4-AP-free!"
                bad = check_noflat(t, N, tested)
                assert not bad, f"NO-FLAT violated by the model: {bad[:3]}"
                print(f"T={T} N={N}: SAT ({dt:.0f}s, {rd} rounds); steps constrained AND "
                      f"verified: {tested}; NO-FLAT holds on all of them", flush=True)
            else:
                print(f"T={T} N={N}: {res} ({dt:.0f}s, {rd} rounds); steps in scope: {tested}",
                      flush=True)
                break
