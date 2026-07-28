"""blockdelay.py — the R20 architecture family with a FREE delay: can it be
D1-compatible?  (route R21, the sharpest restricted search)

Family searched:   c(v) = floor(log_b v) + t(v),   t : [1..N] -> {0..Tmax}.
This is exactly route R20's class architecture with the AP-alternation requirement on t
DROPPED and replaced by the weaker, necessary condition (ii) on c itself:

  (ii)      no 4-AP has a strictly monotone class sequence  [necessary for ANY class
            architecture: a strictly increasing class sequence is a monotone increasing
            4-AP of the emitted permutation, whatever the within-class orders are];
  (no-tame) for every AP P with q <= qmax, c|_P is NOT weakly increasing on the top half
            of P.  By Proposition R21-2 a weakly increasing tail forces
            sup pos_P(n)/n <= 1 + R_P with R_P ~ b for this geometric design, i.e. LINEAR
            displacement on P -- the D1 violation that killed the whole R20 family
            (Proposition R20-3(a)).

Corollary R21-5 (proved in REPORT.md) rules out every *congruence-determined* delay t
(all p-adic valuations rho(v_p(v+s)), all functions of v mod m, all Boolean combinations):
such a t is constant on an infinite AP, which is then tame.  This search asks whether some
NON-congruence delay escapes, on boards of size N.

Engines: CP-SAT primary; SAT models re-verified from the raw t-vector by `verify`.
"""

import sys, time, json, math
from ortools.sat.python import cp_model

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_elements                                        # noqa: E402
from clsdisp import four_aps                                          # noqa: E402


def blk(v, b):
    return int(math.log(v, b) + 1e-12)


def build(N, b, Tmax, qmax, verbose=False):
    m = cp_model.CpModel()
    B = [0] + [blk(v, b) for v in range(1, N + 1)]
    t = [None] + [m.NewIntVar(0, Tmax, f"t{v}") for v in range(1, N + 1)]
    lt = {}

    def LT(u, w):
        """c(u) < c(w)  <=>  t[u] - t[w] < B[w] - B[u]."""
        if (u, w) in lt:
            return lt[(u, w)]
        bv = m.NewBoolVar(f"lt{u}_{w}")
        m.Add(t[u] - t[w] <= B[w] - B[u] - 1).OnlyEnforceIf(bv)
        m.Add(t[u] - t[w] >= B[w] - B[u]).OnlyEnforceIf(bv.Not())
        lt[(u, w)] = bv
        return bv

    for (a, b_, cc, d) in four_aps(N):
        m.AddBoolOr([LT(a, b_).Not(), LT(b_, cc).Not(), LT(cc, d).Not()])
        m.AddBoolOr([LT(b_, a).Not(), LT(cc, b_).Not(), LT(d, cc).Not()])

    nt = 0
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(N, q, r)
            L = len(el)
            if L < 4:
                continue
            m.AddBoolOr([LT(el[k], el[k - 1]) for k in range(L // 2, L)])
            nt += 1
    if verbose:
        print(f"   [N={N} b={b} Tmax={Tmax} qmax={qmax}: {len(lt)} lt-bools, "
              f"{nt} no-tame clauses]", flush=True)
    return m, t, B


def verify(tv, N, b, Tmax, qmax):
    B = [0] + [blk(v, b) for v in range(1, N + 1)]
    c = [0] + [B[v] + tv[v] for v in range(1, N + 1)]
    for v in range(1, N + 1):
        assert 0 <= tv[v] <= Tmax
    for (a, b_, cc, d) in four_aps(N):
        s = (c[a], c[b_], c[cc], c[d])
        assert not (s[0] < s[1] < s[2] < s[3]), ("inc", a, b_, cc, d, s)
        assert not (s[0] > s[1] > s[2] > s[3]), ("dec", a, b_, cc, d, s)
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(N, q, r)
            L = len(el)
            if L < 4:
                continue
            cls = [c[v] for v in el]
            assert any(cls[k] < cls[k - 1] for k in range(L // 2, L)), ("tame AP", q, r)
    return True


def run(N, b, Tmax, qmax, tl=300.0, workers=4, verbose=True):
    m, t, B = build(N, b, Tmax, qmax, verbose)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_search_workers = workers
    t0 = time.time()
    st = s.Solve(m)
    dt = time.time() - t0
    name = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
            cp_model.INFEASIBLE: "UNSAT", cp_model.UNKNOWN: "UNKNOWN"}[st]
    tv = None
    if name == "SAT":
        tv = [0] + [s.Value(t[v]) for v in range(1, N + 1)]
        verify(tv, N, b, Tmax, qmax)
    return name, tv, dt


if __name__ == "__main__":
    args = dict(a.split('=') for a in sys.argv[1:])
    b = float(args.get('b', 3)); qmax = int(args.get('qmax', 8))
    tl = float(args.get('tl', 300))
    for Tmax in [int(x) for x in args.get('Tmax', '1,2,3,4,6').split(',')]:
        for N in [int(x) for x in args.get('N', '40,60,100,160').split(',')]:
            res, tv, dt = run(N, b, Tmax, qmax, tl=tl)
            print(f"blockdelay b={b} Tmax={Tmax} N={N} qmax={qmax}: {res} ({dt:.1f}s)",
                  flush=True)
            if res == "SAT":
                open(f"/home/user/erdos/attempts/route-R21-apuniform/"
                     f"bd_N{N}_T{Tmax}_b{b}.json", "w").write(json.dumps(tv[1:]))
                print("     t =", tv[1:])
            if res == "UNSAT":
                break
