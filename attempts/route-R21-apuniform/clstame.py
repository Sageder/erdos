"""clstame.py — can condition (ii) and D1-compatibility coexist at the COARSE level?

Search for c : [1..N] -> {0..K-1} with
  (ii)  no strictly monotone class sequence along any 4-AP  (Lemma R20-1's conclusion);
  (i)   EXACT geometric fibre design |F_j| = |[b^j, b^{j+1}) cap [1..N]|  (the standard
        ratio-b block design; finite fibres with the growth that makes the architecture
        a reduction);
  (iii-tame)  NO TAME AP: for every AP P = {r+q, r+2q, ...} with q <= qmax, the class
        sequence c|_P is NOT weakly increasing on the top half of P.  By Proposition
        R21-2 a weakly-increasing tail caps the AP displacement at 1 + (block ratio),
        so "no tame AP" is the scale-robust finite proxy for design principle D1 --
        and it is precisely the property route R20's CLS(b,rho) family fails
        (14 of the 36 APs with q <= 8 are tame there: measured in rules.py).

Optionally also (iii-disp): coarse displacement >= T on every dyadic index window.

Primary engine CP-SAT; SAT models re-verified from the raw class vector; any UNSAT is
re-run with a second engine (clstame_sat.py, pysat order encoding, cadical + glucose).
"""

import sys, time, json
from fractions import Fraction
from ortools.sat.python import cp_model

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_elements                                       # noqa: E402
from clsdisp import four_aps, geometric_sizes, windows               # noqa: E402


def build(N, sizes, qmax, T=None, wmin=2, verbose=False):
    K = len(sizes)
    m = cp_model.CpModel()
    c = [None] + [m.NewIntVar(0, K - 1, f"c{v}") for v in range(1, N + 1)]
    lt = {}

    def LT(u, w):
        if (u, w) in lt:
            return lt[(u, w)]
        bv = m.NewBoolVar(f"lt{u}_{w}")
        m.Add(c[u] < c[w]).OnlyEnforceIf(bv)
        m.Add(c[u] >= c[w]).OnlyEnforceIf(bv.Not())
        lt[(u, w)] = bv
        return bv

    for (a, b_, cc, d) in four_aps(N):
        m.AddBoolOr([LT(a, b_).Not(), LT(b_, cc).Not(), LT(cc, d).Not()])
        m.AddBoolOr([LT(b_, a).Not(), LT(cc, b_).Not(), LT(d, cc).Not()])

    ind = {}
    for j in range(K):
        col = []
        for v in range(1, N + 1):
            bv = m.NewBoolVar(f"i{v}_{j}")
            m.Add(c[v] == j).OnlyEnforceIf(bv)
            m.Add(c[v] != j).OnlyEnforceIf(bv.Not())
            ind[(v, j)] = bv
            col.append(bv)
        m.Add(sum(col) == sizes[j])

    ntame, nwin = 0, 0
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(N, q, r)
            L = len(el)
            if L < 4:
                continue
            lo = L // 2
            m.AddBoolOr([LT(el[k], el[k - 1]) for k in range(lo, L)])  # descent in top half
            ntame += 1
            if T is not None:
                wins = windows(L, T, wmin)
                if not wins:
                    continue
                S = [m.NewIntVar(0, L, f"S{q}_{r}_{j}") for j in range(K + 1)]
                m.Add(S[0] == 0)
                for j in range(K):
                    m.Add(S[j + 1] == S[j] + sum(ind[(v, j)] for v in el))
                Sat = {}
                for (a_, b2) in wins:
                    sel = []
                    for n in range(a_, b2):
                        if n not in Sat:
                            x = m.NewIntVar(0, L, f"Sa{q}_{r}_{n}")
                            m.AddElement(c[el[n - 1]], S[:K], x)
                            Sat[n] = x
                        bs = m.NewBoolVar("")
                        m.Add(T.denominator * (1 + Sat[n]) >= T.numerator * n).OnlyEnforceIf(bs)
                        sel.append(bs)
                    m.AddBoolOr(sel)
                    nwin += 1
    if verbose:
        print(f"   [N={N} sizes={sizes} qmax={qmax} T={T}: {len(lt)} lt-bools, "
              f"{ntame} no-tame clauses, {nwin} window clauses]", flush=True)
    return m, c


def verify(cl, N, sizes, qmax, T=None, wmin=2):
    from collections import Counter
    K = len(sizes)
    for (a, b_, cc, d) in four_aps(N):
        s = (cl[a], cl[b_], cl[cc], cl[d])
        assert not (s[0] < s[1] < s[2] < s[3]), ("inc", a, b_, cc, d, s)
        assert not (s[0] > s[1] > s[2] > s[3]), ("dec", a, b_, cc, d, s)
    cnt = Counter(cl[1:])
    for j in range(K):
        assert cnt.get(j, 0) == sizes[j], ("size", j, cnt.get(j, 0), sizes[j])
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(N, q, r)
            L = len(el)
            if L < 4:
                continue
            cls = [cl[v] for v in el]
            assert any(cls[k] < cls[k - 1] for k in range(L // 2, L)), ("tame AP", q, r)
            if T is not None:
                for (a_, b2) in windows(L, T, wmin):
                    ok = any(Fraction(1 + sum(1 for x in cls if x < cls[n - 1]), n) >= T
                             for n in range(a_, b2))
                    assert ok, ("window", q, r, a_, b2)
    return True


def run(N, b, qmax, T=None, tl=300.0, workers=4, verbose=True):
    sizes = geometric_sizes(N, b)
    m, c = build(N, sizes, qmax, T, verbose=verbose)
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
        verify(cl, N, sizes, qmax, T)
    return name, cl, dt, sizes


if __name__ == "__main__":
    args = dict(a.split('=') for a in sys.argv[1:])
    b = float(args.get('b', 3)); qmax = int(args.get('qmax', 8))
    tl = float(args.get('tl', 300))
    T = None if args.get('T', 'none') == 'none' else Fraction(args['T'])
    for N in [int(x) for x in args.get('N', '60,100,160,250').split(',')]:
        res, cl, dt, sizes = run(N, b, qmax, T, tl=tl)
        print(f"N={N} b={b} qmax={qmax} T={T} sizes={sizes}: {res} ({dt:.1f}s)", flush=True)
        if res == "SAT":
            open(f"/home/user/erdos/attempts/route-R21-apuniform/"
                 f"tame_N{N}_b{b}_q{qmax}.json", "w").write(json.dumps(cl[1:]))
