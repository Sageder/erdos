"""clsd1.py — the AP-uniformity experiment at the level of CLASS FUNCTIONS (route R21).

The object searched for (mission items (i)-(iii), CORE.md Corollary 26 / route R20
Lemma R20-1, Proposition R20-3):

    c : [1..N] -> {0,...,K-1}      "class function"; the architecture emits class 0,
                                   then class 1, ... , each class internally in a
                                   free order.

  (i)   FINITE / COARSE FIBRES.  Every used class has size in [mmin, mmax]; used classes
        form an initial segment of {0,...,K-1}.  mmin >= 2 is what makes the
        architecture a genuine coarsening (R20-3(b): O(log v)-thin classes are no
        reduction); mmax models the finite-fibre design.

  (ii)  NO STRICTLY MONOTONE CLASS SEQUENCE ALONG ANY 4-AP.  For every x, d with
        x+3d <= N, the sequence (c(x), c(x+d), c(x+2d), c(x+3d)) is neither strictly
        increasing nor strictly decreasing.  This is exactly the conclusion of Lemma
        R20-1 and is what makes the "coarse case" of the architecture free.

  (iii) AP NON-DEGENERACY (the finite proxy for design principle D1).  For every AP
        P = {r+q, r+2q, ...} with q <= qmax, and for every dyadic index window W of P,
        c restricted to P has a strict DESCENT inside W:  some consecutive pair
        p_m < p_{m+1} of P with m in W and c(p_{m+1}) < c(p_m).
        Rationale: a finite sequence is weakly increasing iff it has no adjacent strict
        descent; and if c|_P is weakly increasing on a tail of P then the induced order
        on that tail is an in-order contiguous block ordering, whose relative
        displacement is bounded by the block ratio -- exactly R20-3(a)'s D1 violation.
        Requiring a descent in EVERY dyadic window is the scale-invariant form: it says
        c|_P is not weakly increasing on any tail at any scale.

Engines: primary = OR-Tools CP-SAT; independent second engine = pysat/Cadical + Glucose
on an order encoding of c (clsd1_sat.py).  Any UNSAT used must be reproduced by both.
"""

import sys, time
from ortools.sat.python import cp_model

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_elements                                   # noqa: E402


def four_aps(N):
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            yield (x, x + e, x + 2 * e, x + 3 * e)


def dyadic_windows(L, wmin=3):
    """Index windows [lo, hi) of adjacency indices m (pairs (p_m, p_{m+1}), 1<=m<L),
    dyadic from the top: [L/2, L), [L/4, L/2), ... , each with >= wmin pairs."""
    out, hi = [], L
    while True:
        lo = max(1, hi // 2)
        if hi - lo < wmin:
            break
        out.append((lo, hi))
        if lo == 1:
            break
        hi = lo
    return out


def build_model(N, K, mmin, mmax, qmax, wmin=3, want_descents=True, verbose=False):
    m = cp_model.CpModel()
    c = [None] + [m.NewIntVar(0, K - 1, f"c{v}") for v in range(1, N + 1)]

    # --- reified strict comparisons on the pairs we need -------------------------
    lt = {}

    def LT(u, w):
        """Boolean b with b <=> c[u] < c[w]."""
        if (u, w) in lt:
            return lt[(u, w)]
        b = m.NewBoolVar(f"lt_{u}_{w}")
        m.Add(c[u] < c[w]).OnlyEnforceIf(b)
        m.Add(c[u] >= c[w]).OnlyEnforceIf(b.Not())
        lt[(u, w)] = b
        return b

    # --- (ii) no strictly monotone class sequence along a 4-AP -------------------
    n4 = 0
    for (a, b, cc, d) in four_aps(N):
        inc = [LT(a, b), LT(b, cc), LT(cc, d)]
        dec = [LT(b, a), LT(cc, b), LT(d, cc)]
        m.AddBoolOr([x.Not() for x in inc])
        m.AddBoolOr([x.Not() for x in dec])
        n4 += 1

    # --- (i) fibre design ---------------------------------------------------------
    ind = {}
    for j in range(K):
        col = []
        for v in range(1, N + 1):
            b = m.NewBoolVar(f"is_{v}_{j}")
            m.Add(c[v] == j).OnlyEnforceIf(b)
            m.Add(c[v] != j).OnlyEnforceIf(b.Not())
            ind[(v, j)] = b
            col.append(b)
        used = m.NewBoolVar(f"used_{j}")
        m.Add(sum(col) >= mmin).OnlyEnforceIf(used)
        m.Add(sum(col) == 0).OnlyEnforceIf(used.Not())
        if mmax is not None:
            m.Add(sum(col) <= mmax)
        ind[('used', j)] = used
    for j in range(K - 1):                        # used classes are an initial segment
        m.AddImplication(ind[('used', j + 1)], ind[('used', j)])
    m.Add(ind[('used', 0)] == 1)

    # --- (iii) AP non-degeneracy ---------------------------------------------------
    ndesc = 0
    if want_descents:
        for q in range(1, qmax + 1):
            for r in range(q):
                el = ap_elements(N, q, r)
                L = len(el)
                for (lo, hi) in dyadic_windows(L, wmin):
                    lits = [LT(el[k], el[k - 1]) for k in range(lo, hi)]  # c(p_{k+1})<c(p_k)
                    m.AddBoolOr(lits)
                    ndesc += 1
    if verbose:
        print(f"  model: N={N} K={K} mmin={mmin} mmax={mmax} qmax={qmax}: "
              f"{n4} 4-APs, {len(lt)} comparison bools, {ndesc} descent clauses",
              flush=True)
    return m, c


def run(N, K, mmin, mmax=None, qmax=8, wmin=3, want_descents=True, tl=120.0, workers=4,
        verbose=True):
    m, c = build_model(N, K, mmin, mmax, qmax, wmin, want_descents, verbose)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_search_workers = workers
    t0 = time.time()
    st = s.Solve(m)
    dt = time.time() - t0
    name = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
            cp_model.INFEASIBLE: "UNSAT", cp_model.UNKNOWN: "UNKNOWN",
            cp_model.MODEL_INVALID: "INVALID"}[st]
    sol = None
    if name == "SAT":
        sol = [0] + [s.Value(c[v]) for v in range(1, N + 1)]
    return name, sol, dt


# ------------------------------------------------------------------ verification ----
def verify(cvec, N, K, mmin, mmax, qmax, wmin=3, need_descents=True):
    """Independent re-check of every constraint, from the raw class vector."""
    cl = cvec
    for (a, b, cc, d) in four_aps(N):
        s = (cl[a], cl[b], cl[cc], cl[d])
        assert not (s[0] < s[1] < s[2] < s[3]), ("strictly increasing 4-AP classes", a, b, cc, d, s)
        assert not (s[0] > s[1] > s[2] > s[3]), ("strictly decreasing 4-AP classes", a, b, cc, d, s)
    from collections import Counter
    cnt = Counter(cl[1:])
    for j, k in cnt.items():
        assert k >= mmin, ("class too small", j, k)
        if mmax is not None:
            assert k <= mmax, ("class too large", j, k)
    used = sorted(cnt)
    assert used == list(range(len(used))), ("used classes not an initial segment", used)
    if need_descents:
        for q in range(1, qmax + 1):
            for r in range(q):
                el = ap_elements(N, q, r)
                L = len(el)
                for (lo, hi) in dyadic_windows(L, wmin):
                    ok = any(cl[el[k]] < cl[el[k - 1]] for k in range(lo, hi))
                    assert ok, ("no descent in window", q, r, lo, hi)
    return True


if __name__ == "__main__":
    import json
    args = dict(a.split('=') for a in sys.argv[1:])
    N = int(args.get('N', 60)); K = int(args.get('K', 12))
    mmin = int(args.get('mmin', 2)); qmax = int(args.get('qmax', 4))
    mmax = None if args.get('mmax', 'none') == 'none' else int(args['mmax'])
    tl = float(args.get('tl', 120))
    wd = args.get('desc', '1') == '1'
    res, sol, dt = run(N, K, mmin, mmax, qmax, tl=tl, want_descents=wd)
    print(f"N={N} K={K} mmin={mmin} mmax={mmax} qmax={qmax} desc={wd}: {res} ({dt:.1f}s)",
          flush=True)
    if res == "SAT":
        verify(sol, N, K, mmin, mmax, qmax, need_descents=wd)
        print("  verified independently.")
        print("  c =", sol[1:])
        open(f"/home/user/erdos/attempts/route-R21-apuniform/"
             f"c_N{N}_m{mmin}_q{qmax}.json", "w").write(json.dumps(sol[1:]))
