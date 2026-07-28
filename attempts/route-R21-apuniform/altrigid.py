"""altrigid.py — rigidity of AP-alternating functions (route R21).

Route R20's class architecture is c(v) = floor(log_b v) + t(v) with t *AP-alternating*
(Lemma R20-1): for every 4-AP (x, x+d, x+2d, x+3d), writing t_i = t(x+id), one of
   (i)  t0 = t1 = t2 = t3
   (ii) t0 = t2 < min(t1, t3)
   (iii) t1 = t3 < min(t0, t2).
Proposition R20-3 observes that for t(v) = rho(v_2(v)) the odd numbers all carry the
same t, so the odd restriction is an in-order geometric block ordering with LINEAR
displacement -- the architecture violates design principle D1.

QUESTION SETTLED HERE: is that an accident of the 2-adic choice, or does AP-alternation
FORCE t to be a function of v_2 (hence constant on the odds)?  If forced, the whole
R20 class-architecture family is closed for D1 by a single structural theorem.

Machine test: for a given board [1..N] and codomain size K, ask CP-SAT whether some
AP-alternating t exists with t(u) != t(w) for a prescribed pair u, w with v_2(u)=v_2(w)
(and the aggregated version: SOME such pair differs).  UNSAT is reproduced with a second
engine (pysat/Cadical + Glucose, order encoding) in altrigid_sat.py.
"""

import sys, time
from ortools.sat.python import cp_model


def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def four_aps(N):
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            yield (x, x + e, x + 2 * e, x + 3 * e)


def build(N, K, extra=None):
    m = cp_model.CpModel()
    t = [None] + [m.NewIntVar(0, K - 1, f"t{v}") for v in range(1, N + 1)]
    for (a, b, c, d) in four_aps(N):
        s1 = m.NewBoolVar("")
        s2 = m.NewBoolVar("")
        s3 = m.NewBoolVar("")
        m.AddExactlyOne([s1, s2, s3])
        # (i) all equal
        m.Add(t[a] == t[b]).OnlyEnforceIf(s1)
        m.Add(t[b] == t[c]).OnlyEnforceIf(s1)
        m.Add(t[c] == t[d]).OnlyEnforceIf(s1)
        # (ii) t0 = t2 < min(t1,t3)
        m.Add(t[a] == t[c]).OnlyEnforceIf(s2)
        m.Add(t[a] < t[b]).OnlyEnforceIf(s2)
        m.Add(t[a] < t[d]).OnlyEnforceIf(s2)
        # (iii) t1 = t3 < min(t0,t2)
        m.Add(t[b] == t[d]).OnlyEnforceIf(s3)
        m.Add(t[b] < t[a]).OnlyEnforceIf(s3)
        m.Add(t[b] < t[c]).OnlyEnforceIf(s3)
    if extra:
        extra(m, t)
    return m, t


def solve(m, tl=60.0, workers=4):
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_search_workers = workers
    st = s.Solve(m)
    return {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
            cp_model.INFEASIBLE: "UNSAT", cp_model.UNKNOWN: "UNKNOWN"}[st], s


def verify_alternating(tv, N):
    """independent re-check of AP-alternation from the raw vector tv[1..N]."""
    for (a, b, c, d) in four_aps(N):
        t0, t1, t2, t3 = tv[a], tv[b], tv[c], tv[d]
        ok = (t0 == t1 == t2 == t3) or \
             (t0 == t2 and t0 < t1 and t0 < t3) or \
             (t1 == t3 and t1 < t0 and t1 < t2)
        assert ok, ("AP-alternation violated", a, b, c, d, (t0, t1, t2, t3))
    return True


if __name__ == "__main__":
    args = dict(a.split('=') for a in sys.argv[1:])
    K = int(args.get('K', 6))
    tl = float(args.get('tl', 60))
    mode = args.get('mode', 'odds')
    Ns = [int(x) for x in args.get('N', '20,30,40,60,80,120').split(',')]

    # control: rho(v_2) IS AP-alternating on every board
    for N in (40, 120, 400):
        tv = [0] + [min(v2(v), K - 1) for v in range(1, N + 1)]
        verify_alternating(tv, N)
    print(f"control OK: t(v)=min(v_2(v),{K-1}) is AP-alternating on [1..40],[1..120],[1..400]")

    for N in Ns:
        if mode == 'odds':
            # is there an AP-alternating t that is NOT constant on the odds?
            def extra(m, t):
                odds = [v for v in range(1, N + 1) if v % 2 == 1]
                diffs = []
                for i in range(len(odds) - 1):
                    b = m.NewBoolVar("")
                    m.Add(t[odds[i]] != t[odds[i + 1]]).OnlyEnforceIf(b)
                    diffs.append(b)
                m.AddBoolOr(diffs)
        elif mode == 'v2':
            # is there an AP-alternating t that is NOT a function of v_2?
            def extra(m, t):
                diffs = []
                by = {}
                for v in range(1, N + 1):
                    by.setdefault(v2(v), []).append(v)
                for k, vs in by.items():
                    for i in range(len(vs) - 1):
                        b = m.NewBoolVar("")
                        m.Add(t[vs[i]] != t[vs[i + 1]]).OnlyEnforceIf(b)
                        diffs.append(b)
                m.AddBoolOr(diffs)
        else:
            extra = None
        t0 = time.time()
        m, t = build(N, K, extra)
        res, s = solve(m, tl=tl)
        dt = time.time() - t0
        print(f"mode={mode} N={N} K={K}: {res} ({dt:.1f}s)", flush=True)
        if res == "SAT":
            tv = [0] + [s.Value(t[v]) for v in range(1, N + 1)]
            verify_alternating(tv, N)
            print("   witness t =", tv[1:])
            print("   t on odds:", [(v, tv[v]) for v in range(1, min(N, 40) + 1, 2)])
            bad = [(u, w) for u in range(1, N + 1) for w in range(u + 1, N + 1)
                   if v2(u) == v2(w) and tv[u] != tv[w]]
            print(f"   #(same-v2, different-t) pairs = {len(bad)}; first few {bad[:8]}")
