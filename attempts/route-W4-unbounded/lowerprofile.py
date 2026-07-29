"""lowerprofile.py -- the LOWER-profile family A(K).

DEFINITION.  A(K, n): there exist DISTINCT positive integers v_1, ..., v_n with
    q * v_i  <=  p * i      for all i        (K = p/q, exact integer arithmetic)
and no monotone 4-AP among them, i.e. no indices i1<i2<i3<i4 with
(v_{i1}, v_{i2}, v_{i3}, v_{i4}) an arithmetic progression with nonzero common difference
(either sign).

WHY THIS MATTERS (Prop W4-B, see report).  "a(n) <= K n for all n" is the same as
"pos(v) >= v/K for all v", and that is exactly the displacement content of a class
architecture c = floor(log_b .) + t with t >= 0 and at-least-geometric fibres.  A
4-AP-free BIJECTION with a(n) <= Kn gives, by truncation, a valid A(K, n) for every n;
so a finite UNSAT of A(K, n) REFUTES the whole family at that K.  (The converse fails --
A(K) only asks for an injection -- so SAT proves nothing.  Stated asymmetrically on
purpose.)

A(K,n) is monotone in n: truncating a witness of length n+1 gives one of length n.  So
one UNSAT kills all larger n; minimality still needs the SAT point immediately below.

Two independent engines: exhaustive DFS (ground truth, small n) and CP-SAT.
Both are cross-validated against experiments/apcheck.py.
"""
import sys
from fractions import Fraction
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_general


def maxval(p, q, i):
    """largest integer v with q*v <= p*i"""
    return (p * i) // q


# ---------------------------------------------------------------- exhaustive DFS
def dfs(p, q, n, node_cap=None, collect_witness=True):
    """Exhaustive search for A(p/q, n).  Returns (found, witness_or_None, nodes)."""
    M = maxval(p, q, n)
    pos = [0] * (M + 2)          # pos[v] = 1-based index, 0 = unused
    seq = []
    nodes = [0]
    cap = node_cap

    def ok(v, i):
        # increasing orientation, v is the largest term at the last position
        for d in range(1, (v - 1) // 3 + 1):
            a, b, c = v - 3 * d, v - 2 * d, v - d
            pa, pb, pc = pos[a], pos[b], pos[c]
            if pa and pb and pc and pa < pb < pc:
                return False
        # decreasing orientation, v is the smallest term at the last position
        dmax = (M - v) // 3
        for d in range(1, dmax + 1):
            a, b, c = v + 3 * d, v + 2 * d, v + d
            pa, pb, pc = pos[a], pos[b], pos[c]
            if pa and pb and pc and pa < pb < pc:
                return False
        return True

    def rec(i):
        nodes[0] += 1
        if cap is not None and nodes[0] > cap:
            raise TimeoutError
        if i > n:
            return True
        hi = maxval(p, q, i)
        for v in range(hi, 0, -1):
            if pos[v]:
                continue
            if not ok(v, i):
                continue
            pos[v] = i
            seq.append(v)
            if rec(i + 1):
                return True
            seq.pop()
            pos[v] = 0
        return False

    try:
        found = rec(1)
    except TimeoutError:
        return None, None, nodes[0]
    return found, (list(seq) if found and collect_witness else None), nodes[0]


# ---------------------------------------------------------------- CP-SAT
def cpsat(p, q, n, workers=4, time_limit=None, log=False):
    from ortools.sat.python import cp_model
    M = maxval(p, q, n)
    lo = {}
    for v in range(1, M + 1):
        # smallest i with q*v <= p*i
        lo[v] = -((-q * v) // p)
    m = cp_model.CpModel()
    B = {}
    for v in range(1, M + 1):
        for i in range(lo[v], n + 1):
            B[v, i] = m.NewBoolVar(f"b{v}_{i}")
    for i in range(1, n + 1):
        m.AddExactlyOne([B[v, i] for v in range(1, M + 1) if (v, i) in B])
    used = {}
    P = {}
    for v in range(1, M + 1):
        cells = [B[v, i] for i in range(lo[v], n + 1)]
        used[v] = m.NewBoolVar(f"u{v}")
        m.Add(sum(cells) == 1).OnlyEnforceIf(used[v])
        m.Add(sum(cells) == 0).OnlyEnforceIf(used[v].Not())
        P[v] = m.NewIntVar(0, n, f"p{v}")
        m.Add(P[v] == sum(i * B[v, i] for i in range(lo[v], n + 1)))
    # "before" booleans, only for pairs that occur in some 4-AP
    need = set()
    aps = []
    for d in range(1, (M - 1) // 3 + 1):
        for x in range(1, M - 3 * d + 1):
            t = [x + j * d for j in range(4)]
            aps.append(t)
            for j in range(3):
                need.add((t[j], t[j + 1]))
    A = {}
    for (u, w) in need:
        a = m.NewBoolVar(f"a{u}_{w}")
        m.Add(P[u] < P[w]).OnlyEnforceIf(a)
        m.Add(P[u] >= P[w]).OnlyEnforceIf(a.Not())
        A[u, w] = a
    for t in aps:
        us = [used[x].Not() for x in t]
        a1, a2, a3 = A[t[0], t[1]], A[t[1], t[2]], A[t[2], t[3]]
        m.AddBoolOr(us + [a1.Not(), a2.Not(), a3.Not()])   # no increasing
        m.AddBoolOr(us + [a1, a2, a3])                     # no decreasing
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    if time_limit:
        s.parameters.max_time_in_seconds = time_limit
    s.parameters.log_search_progress = log
    st = s.Solve(m)
    if st == cp_model.OPTIMAL or st == cp_model.FEASIBLE:
        seq = [None] * (n + 1)
        for v in range(1, M + 1):
            pv = s.Value(P[v])
            if pv:
                seq[pv] = v
        return "SAT", seq[1:]
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


def verify(seq, p, q, n):
    assert len(seq) == n and len(set(seq)) == n, "not distinct / wrong length"
    for i, v in enumerate(seq, start=1):
        assert q * v <= p * i, f"profile violated at i={i}: v={v}, K={p}/{q}"
    assert not has_monotone_kap_general(seq, 4), "monotone 4-AP present!"
    return True


if __name__ == "__main__":
    import time
    args = sys.argv[1:]
    mode = args[0] if args else "cross"
    if mode == "cross":
        # cross-validate DFS against CP-SAT and against apcheck
        for (p, q) in [(1, 1), (3, 2), (2, 1), (5, 2), (3, 1)]:
            for n in range(1, 13):
                f1, w1, nodes = dfs(p, q, n)
                r2, w2 = cpsat(p, q, n)
                agree = (bool(f1) == (r2 == "SAT"))
                if w1: verify(w1, p, q, n)
                if w2: verify(w2, p, q, n)
                print(f"K={p}/{q} n={n}: dfs={'SAT' if f1 else 'UNSAT'} "
                      f"cpsat={r2} agree={agree} nodes={nodes}", flush=True)
                assert agree, (p, q, n)
    else:
        p, q = int(args[1]), int(args[2])
        ns = [int(x) for x in args[3].split(',')]
        tl = float(args[4]) if len(args) > 4 else 600.0
        for n in ns:
            t0 = time.time()
            r, w = cpsat(p, q, n, time_limit=tl)
            if r == "SAT":
                verify(w, p, q, n)
            print(f"K={p}/{q} n={n}: {r} ({time.time()-t0:.1f}s)"
                  + (f"  witness={w}" if r == "SAT" and n <= 40 else ""), flush=True)
            if r == "UNSAT":
                print(f"  ==> A({p}/{q}) EXTINCT at n={n} (inherited for all larger n)")
                break
