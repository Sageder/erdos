"""dualprofile.py -- the DUAL (lower) displacement profile  pos(v) >= v/K.

DEFINITION.  P(K, N):  there is a permutation sigma of [1..N] with no monotone 4-AP and
    q * v  <=  p * pos_sigma(v)   for every v <= N        (K = p/q, exact integers)
equivalently  sigma(m) <= K*m  for every position m.

WHY THIS IS THE RIGHT FINITE SHADOW (Prop W4-B + Lemma W4-C in the report):
  * a class architecture c = floor(log_b .) + t with delay t >= 0 and at-least-geometric
    fibres has pos(v) >= v/K with K = b/gamma;
  * if a : N -> N is a monotone-4-AP-free BIJECTION with a(m) <= K m for all m, then its
    value-restriction sigma_N to [1..N] is a monotone-4-AP-free permutation of [1..N] with
    sigma_N(m) <= K m for all m.  [for m <= N/K, sigma_N(m) = a(m) <= Km; for m > N/K,
    sigma_N(m) <= N <= Km.]   So P(K,N) holds for EVERY N.
  * hence one UNSAT of P(K,N) REFUTES the whole family at that K -- and unlike the
    injection relaxation A(K) of lowerprofile.py, this shadow keeps SURJECTIVITY
    (sigma is onto [1..N]), which REQUIREMENTS A1 says is essential.

Central quantity:   lambda(N) := min over monotone-4-AP-free permutations sigma of [1..N]
of  max_v  v / pos_sigma(v).   P(K,N) is SAT iff lambda(N) <= K.  If lambda(N) -> oo the
entire geometric-fibre / t>=0 class-architecture family is dead; if lambda(N) stays
bounded the family survives every finite test.

Engines: (a) exhaustive DFS over avoiders (ground truth, small N); (b) lazy-transitivity
CEGAR SAT (engine from experiments/profile_cegar.py); (c) CP-SAT.  All models are
re-verified against experiments/apcheck.py and against the literal profile inequality.
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute
from profile_cegar import find_cycles


# --------------------------------------------------------------- exhaustive DFS
def dfs_P(p, q, N, node_cap=None):
    """Exhaustive: is there a 4-AP-free permutation of [1..N] with q*v <= p*pos(v)?

    Values are placed in INCREASING order 1,2,...,N into slots 1..N (Lemma 8):
    when v is placed, the only new monotone 4-APs are those with largest term v.
    """
    pos = [0] * (N + 2)
    occ = [False] * (N + 2)
    nodes = [0]

    def ok(v, s):
        for d in range(1, v // 3 + 1):
            a, b, c = v - 3 * d, v - 2 * d, v - d
            if a < 1:
                break
            pa, pb, pc = pos[a], pos[b], pos[c]
            if pa < pb < pc < s:
                return False            # increasing 4-AP
            if pa > pb > pc > s:
                return False            # decreasing 4-AP
        return True

    def rec(v):
        nodes[0] += 1
        if node_cap and nodes[0] > node_cap:
            raise TimeoutError
        if v > N:
            return True
        lo = -((-q * v) // p)           # ceil(q*v/p)
        for s in range(lo, N + 1):
            if occ[s] or not ok(v, s):
                continue
            occ[s] = True; pos[v] = s
            if rec(v + 1):
                return True
            occ[s] = False; pos[v] = 0
        return False

    try:
        found = rec(1)
    except TimeoutError:
        return None, None, nodes[0]
    if not found:
        return False, None, nodes[0]
    perm = [0] * N
    for v in range(1, N + 1):
        perm[pos[v] - 1] = v
    return True, perm, nodes[0]


def lambda_exact(N, node_cap=None, grid=None):
    """Exact lambda(N) = min_sigma max_v v/pos(v), over 4-AP-free permutations.
    Search only over the finitely many candidate values v/s (v,s in [1..N])."""
    from fractions import Fraction
    cands = sorted({Fraction(v, s) for v in range(1, N + 1) for s in range(1, N + 1)
                    if Fraction(v, s) >= 1})
    loi, hii = 0, len(cands) - 1
    best = None
    while loi <= hii:
        mid = (loi + hii) // 2
        K = cands[mid]
        r, perm, _ = dfs_P(K.numerator, K.denominator, N, node_cap)
        if r:
            best = (K, perm); hii = mid - 1
        else:
            loi = mid + 1
    return best


# --------------------------------------------------------------- CEGAR SAT
def cegar_P(p, q, N, max_rounds=200000, verbose=False):
    from pysat.solvers import Cadical195
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    pool = IDPool()
    def var(u, w): return pool.id(('x', u, w))
    def lit(u, w): return var(u, w) if u < w else -var(w, u)
    cl = []
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            a = [lit(x + k * e, x + (k + 1) * e) for k in range(3)]
            cl.append([-a[0], -a[1], -a[2]])
            cl.append([a[0], a[1], a[2]])
    for v in range(1, N + 1):
        lo = -((-q * v) // p)                     # pos(v) >= lo
        if lo <= 1:
            continue
        if lo > N:
            return "UNSAT", None, 0               # infeasible outright
        lits = [lit(w, v) for w in range(1, N + 1) if w != v]   # "w before v"
        enc = CardEnc.atleast(lits=lits, bound=lo - 1, vpool=pool,
                              encoding=EncType.seqcounter)
        cl.extend(enc.clauses)
    S = Cadical195(bootstrap_with=cl)
    rounds = 0
    while True:
        if not S.solve():
            S.delete(); return "UNSAT", None, rounds
        model = set(S.get_model())
        def order_of(u, w): return var(u, w) in model
        cycs = find_cycles(order_of, N)
        if not cycs:
            import functools
            vals = list(range(1, N + 1))
            def cmp(u, w):
                if u == w: return 0
                bef = order_of(u, w) if u < w else (not order_of(w, u))
                return -1 if bef else 1
            vals.sort(key=functools.cmp_to_key(cmp))
            S.delete(); return "SAT", vals, rounds
        for cyc in cycs:
            L = len(cyc)
            for i in range(L):
                u, w, z = cyc[i], cyc[(i + 1) % L], cyc[(i + 2) % L]
                if len({u, w, z}) == 3:
                    S.add_clause([-lit(u, w), -lit(w, z), lit(u, z)])
            S.add_clause([-lit(cyc[i], cyc[(i + 1) % L]) for i in range(L)])
        rounds += 1
        if verbose and rounds % 500 == 0:
            print(f"    [round {rounds}]", flush=True)
        if rounds > max_rounds:
            S.delete(); return "UNKNOWN", None, rounds


# --------------------------------------------------------------- CP-SAT (2nd encoding)
def cpsat_P(p, q, N, workers=4, time_limit=None):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    P = [None] + [m.NewIntVar(-((-q * v) // p), N, f"p{v}") for v in range(1, N + 1)]
    m.AddAllDifferent(P[1:])
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            t = [x + k * e for k in range(4)]
            bs = []
            for k in range(3):
                b = m.NewBoolVar("")
                m.Add(P[t[k]] < P[t[k + 1]]).OnlyEnforceIf(b)
                m.Add(P[t[k]] > P[t[k + 1]]).OnlyEnforceIf(b.Not())
                bs.append(b)
            m.AddBoolOr([b.Not() for b in bs])
            m.AddBoolOr(bs)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    if time_limit: s.parameters.max_time_in_seconds = time_limit
    st = s.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        perm = [0] * N
        for v in range(1, N + 1):
            perm[s.Value(P[v]) - 1] = v
        return "SAT", perm
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


def verify_P(perm, p, q, N):
    assert sorted(perm) == list(range(1, N + 1)), "not a permutation of [1..N]"
    assert not has_monotone_kap_pos(perm, 4), "monotone 4-AP present!"
    pos = {v: i + 1 for i, v in enumerate(perm)}
    for v in range(1, N + 1):
        assert q * v <= p * pos[v], f"profile violated: v={v} pos={pos[v]} K={p}/{q}"
    return True


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "cross"
    if mode == "cross":
        # three engines must agree; models re-verified literally
        for N in range(4, 13):
            for (p, q) in [(1, 1), (5, 4), (3, 2), (2, 1), (5, 2), (3, 1), (4, 1)]:
                r1, w1, _ = dfs_P(p, q, N)
                r2, w2, _ = cegar_P(p, q, N)
                r3, w3 = cpsat_P(p, q, N)
                s1 = "SAT" if r1 else "UNSAT"
                for w in (w1, w2, w3):
                    if w: verify_P(w, p, q, N)
                assert s1 == r2 == r3, (N, p, q, s1, r2, r3)
            print(f"N={N}: all 7 K-values agree across DFS / CEGAR / CP-SAT", flush=True)
        print("cross-validation OK")
    elif mode == "lam":
        for N in range(4, int(sys.argv[2]) + 1):
            t0 = time.time()
            best = lambda_exact(N)
            K, perm = best
            verify_P(perm, K.numerator, K.denominator, N)
            print(f"lambda({N}) = {K} = {float(K):.4f}   ({time.time()-t0:.1f}s)  "
                  f"witness={perm}", flush=True)
    else:
        p, q = int(sys.argv[2]), int(sys.argv[3])
        for N in [int(x) for x in sys.argv[4].split(',')]:
            t0 = time.time()
            r, w, rounds = cegar_P(p, q, N, verbose=True)
            if r == "SAT": verify_P(w, p, q, N)
            print(f"P(K={p}/{q}, N={N}): {r}  ({time.time()-t0:.1f}s, {rounds} rounds)",
                  flush=True)
            if r == "UNSAT":
                break
