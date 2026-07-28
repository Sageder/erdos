"""clsdisp.py — the AP-uniformity experiment proper (route R21, main engine).

Searched object: a CLASS FUNCTION c : [1..N] -> {0..K-1} that is the coarse skeleton of a
block architecture (classes emitted in increasing index order, within-class order free),
subject to the three mission conditions:

 (i)   fibre design: |F_j| <= U_j with U_j = ceil(A * b^j)  (finite fibres, geometric
       growth -- the standard block design; every class nonempty, used classes an
       initial segment).
 (ii)  no strictly monotone class sequence along any 4-AP (Lemma R20-1's conclusion);
 (iii) AP-uniformity at level T, scale-invariantly: for every AP P = {r+q, r+2q, ...}
       with q <= qmax, and every dyadic index window [n0, 2n0) of P with 2n0 <= L/T,
       there is n in the window with

           COARSE DISPLACEMENT   cdisp_P(n) := (1 + #{m : c(p_m) < c(p_n)}) / n  >=  T.

       cdisp_P(n) is a LOWER bound for pos_P(n)/n valid for every within-class order
       (elements of strictly smaller classes are all positioned earlier), so a solution
       gives an architecture whose AP-displacement is >= T at every dyadic scale on
       every AP with q <= qmax -- the finite, scale-invariant proxy for design principle
       D1 (CORE.md Corollary 26).

       The window cap 2n0 <= L/T is forced: cdisp_P(n) <= L/n, so displacement T is
       invisible at indices n > L/T.  This is the finite-board resolution limit.

 Key identity used for a cheap encoding:  #{m : c(p_m) < c(p_n)} = S_{P, c(p_n)} where
 S_{P,j} := #{v in P : c(v) < j}.  So only K integer variables per AP are needed, plus
 one AddElement per index.

Primary engine OR-Tools CP-SAT; every SAT model is re-verified from the raw class vector
by `verify` below (independent recomputation of all three conditions in exact integer
arithmetic).  Any UNSAT that is relied on is re-run with a second engine.
"""

import sys, time, json
from fractions import Fraction
from ortools.sat.python import cp_model

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_elements                                     # noqa: E402


def four_aps(N):
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            yield (x, x + e, x + 2 * e, x + 3 * e)


def geometric_caps(N, A, b, K):
    return [max(1, int(-(-A * b ** j // 1))) for j in range(K)]


def geometric_sizes(N, b):
    """EXACT geometric block-size design: |F_j| = #([b^j, b^{j+1}) cap [1..N]).
    This is the standard ratio-b block partition, truncated at N; the number of classes
    is determined by N and b."""
    sizes, lo, j = [], 1, 0
    while lo <= N:
        hi = min(N + 1, int(b ** (j + 1)) + 1 if b == int(b) else int(b ** (j + 1)) + 1)
        hi = min(N + 1, max(lo + 1, int(round(b ** (j + 1)))))
        sizes.append(hi - lo)
        lo, j = hi, j + 1
    if sizes and sizes[-1] <= 0:
        sizes.pop()
    tot = sum(sizes)
    if tot < N:
        sizes[-1] += N - tot
    return sizes


def windows(L, T, wmin=2):
    """dyadic index windows [lo,hi) with hi <= L/T and at least wmin indices."""
    out = []
    hi = int(Fraction(L) / T) + 1
    hi = min(hi, L + 1)
    while hi > 1:
        lo = max(1, hi // 2)
        if hi - lo >= wmin:
            out.append((lo, hi))
        if lo <= 1:
            break
        hi = lo
    return out


def build(N, K, caps, T, qmax, wmin=2, verbose=False, exact=False):
    Tn, Td = T.numerator, T.denominator
    m = cp_model.CpModel()
    c = [None] + [m.NewIntVar(0, K - 1, f"c{v}") for v in range(1, N + 1)]

    lt = {}

    def LT(u, w):
        if (u, w) in lt:
            return lt[(u, w)]
        bvar = m.NewBoolVar(f"lt{u}_{w}")
        m.Add(c[u] < c[w]).OnlyEnforceIf(bvar)
        m.Add(c[u] >= c[w]).OnlyEnforceIf(bvar.Not())
        lt[(u, w)] = bvar
        return bvar

    # (ii)
    for (a, b_, cc, d) in four_aps(N):
        m.AddBoolOr([LT(a, b_).Not(), LT(b_, cc).Not(), LT(cc, d).Not()])
        m.AddBoolOr([LT(b_, a).Not(), LT(cc, b_).Not(), LT(d, cc).Not()])

    # (i) fibre caps + nonempty + initial segment
    ind = {}
    for j in range(K):
        col = []
        for v in range(1, N + 1):
            bv = m.NewBoolVar(f"i{v}_{j}")
            m.Add(c[v] == j).OnlyEnforceIf(bv)
            m.Add(c[v] != j).OnlyEnforceIf(bv.Not())
            ind[(v, j)] = bv
            col.append(bv)
        if exact:
            m.Add(sum(col) == caps[j])
        else:
            m.Add(sum(col) <= caps[j])
            m.Add(sum(col) >= 1)

    # (iii) AP-uniformity at level T on every dyadic window
    nwin = 0
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(N, q, r)
            L = len(el)
            wins = windows(L, T, wmin)
            if not wins:
                continue
            # S[j] = #{v in P : c(v) < j}
            S = [m.NewIntVar(0, L, f"S{q}_{r}_{j}") for j in range(K + 1)]
            m.Add(S[0] == 0)
            for j in range(K):
                m.Add(S[j + 1] == S[j] + sum(ind[(v, j)] for v in el))
            Sat = {}
            for (lo, hi) in wins:
                sel = []
                for n in range(lo, hi):
                    if n not in Sat:
                        x = m.NewIntVar(0, L, f"Sat{q}_{r}_{n}")
                        m.AddElement(c[el[n - 1]], S[:K], x)
                        Sat[n] = x
                    bsel = m.NewBoolVar("")
                    # (1 + S_at) / n >= T   <=>   Td*(1+S_at) >= Tn*n
                    m.Add(Td * (1 + Sat[n]) >= Tn * n).OnlyEnforceIf(bsel)
                    sel.append(bsel)
                m.AddBoolOr(sel)
                nwin += 1
    if verbose:
        print(f"   [model N={N} K={K} T={T} qmax={qmax}: {len(lt)} lt-bools, "
              f"{nwin} window clauses]", flush=True)
    return m, c


def verify(cl, N, K, caps, T, qmax, wmin=2, exact=False):
    """independent re-check of (i),(ii),(iii) from the raw class vector cl[1..N]."""
    from collections import Counter
    for (a, b_, cc, d) in four_aps(N):
        s = (cl[a], cl[b_], cl[cc], cl[d])
        assert not (s[0] < s[1] < s[2] < s[3]), ("inc classes", a, b_, cc, d, s)
        assert not (s[0] > s[1] > s[2] > s[3]), ("dec classes", a, b_, cc, d, s)
    cnt = Counter(cl[1:])
    for j in range(K):
        if exact:
            assert cnt.get(j, 0) == caps[j], ("size violated", j, cnt.get(j, 0), caps[j])
        else:
            assert cnt.get(j, 0) >= 1, ("empty class", j)
            assert cnt[j] <= caps[j], ("cap violated", j, cnt[j], caps[j])
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(N, q, r)
            L = len(el)
            cls = [cl[v] for v in el]
            for (lo, hi) in windows(L, T, wmin):
                ok = False
                for n in range(lo, hi):
                    S = sum(1 for x in cls if x < cls[n - 1])
                    if Fraction(1 + S, n) >= T:
                        ok = True
                        break
                assert ok, ("window unmet", q, r, lo, hi)
    return True


def coarse_profile(cl, N, qmax):
    """MEASURED table: for each AP, max_n cdisp and the index attaining it."""
    rows = []
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(N, q, r)
            cls = [cl[v] for v in el]
            best, arg = Fraction(0), None
            for n in range(1, len(el) + 1):
                S = sum(1 for x in cls if x < cls[n - 1])
                val = Fraction(1 + S, n)
                if val > best:
                    best, arg = val, n
            rows.append((q, r, len(el), best, arg))
    return rows


def run(N, K, A, b, T, qmax, tl=300.0, workers=4, wmin=2, verbose=True, mode='cap'):
    if mode == 'geo':
        caps = geometric_sizes(N, b); K = len(caps); exact = True
    else:
        caps = geometric_caps(N, A, b, K); exact = False
    m, c = build(N, K, caps, T, qmax, wmin, verbose, exact)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_search_workers = workers
    t0 = time.time()
    st = s.Solve(m)
    dt = time.time() - t0
    name = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
            cp_model.INFEASIBLE: "UNSAT", cp_model.UNKNOWN: "UNKNOWN"}[st]
    cl = None
    if name == "SAT":
        cl = [0] + [s.Value(c[v]) for v in range(1, N + 1)]
        verify(cl, N, K, caps, T, qmax, wmin, exact)
    return name, cl, dt, caps


if __name__ == "__main__":
    args = dict(a.split('=') for a in sys.argv[1:])
    N = int(args.get('N', 80)); K = int(args.get('K', 8))
    A = float(args.get('A', 2)); b = float(args.get('b', 3))
    qmax = int(args.get('qmax', 4)); tl = float(args.get('tl', 300))
    Ts = [Fraction(x) for x in args.get('T', '3/2,2,5/2,3,4').split(',')]
    mode = args.get('mode', 'cap')
    for T in Ts:
        res, cl, dt, caps = run(N, K, A, b, T, qmax, tl=tl, mode=mode)
        print(f"N={N} K={K} caps={caps} qmax={qmax} T={T}: {res} ({dt:.1f}s)", flush=True)
        if res == "SAT":
            open(f"/home/user/erdos/attempts/route-R21-apuniform/"
                 f"cls_N{N}_T{T.numerator}_{T.denominator}_q{qmax}.json",
                 "w").write(json.dumps(cl[1:]))
            print("   c =", cl[1:])
        if res == "UNSAT":
            break
