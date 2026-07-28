"""wsys.py -- route W4-accel.  INDEPENDENT re-derivation of the necessary order
system imposed on a monotone-4-AP-free permutation a of N by a finite set of CUTS,
generalised with a HORIZON M >= max cut.

DEFINITIONS (from PROBLEM.md alone).
  V is a cut of a  iff  {a(1),...,a(V)} = {1,...,V}  iff  every value <= V precedes
  every value > V.
  Given cuts V_1 < ... < V_k and a horizon M >= V_k, the induced order on [1..M]
  satisfies:
    (L)  block layout: with B_0=[1,V_1], B_j=(V_j,V_{j+1}], B_k=(V_k,M], every value
         of B_i precedes every value of B_j for i<j.  (Order INSIDE B_k is free, and
         inside every B_j is free.)
    (C1) no monotone 4-AP among the values [1..M], either orientation.
    (C2) for x,d>=1 with x+2d <= V_k and x+3d > M: the positional chain
         x < x+d < x+2d is forbidden.
         [Justification: let V_j = least cut >= x+2d.  Then x+3d > M >= V_j, so
          x+3d sits after position V_j, hence after x+2d; the chain would complete
          an increasing monotone 4-AP.  Uses surjectivity of a.]
  No decreasing analogue of (C2) is needed: a 4th term ABOVE the top cut can never
  be the FIRST element of a decreasing chain, and every value below V_k is present.

  When M = V_k this is exactly the route-R1 cut-stage system.
  When k = 2 and M > V_2 it is a strictly stronger 2-cut system, and it is MONOTONE
  in M (a solution for M restricts to a solution for any V_k <= M' <= M), so
  "UNSAT at some M" is a statement about ALL larger horizons at once.

SOUNDNESS.  (L),(C1),(C2) are NECESSARY.  Therefore
    UNSAT  ==>  no monotone-4-AP-free permutation of N has all of V_1..V_k as cuts.
Nothing here proves the converse; SAT only says the necessary system is consistent.
"""

import sys
from itertools import combinations

sys.path.insert(0, "/home/user/erdos/experiments")


# ---------------------------------------------------------------- geometry ---
def block_index(cuts, M):
    """blk[v] for v in 1..M."""
    blk = [0] * (M + 1)
    j = 0
    for v in range(1, M + 1):
        while j < len(cuts) and v > cuts[j]:
            j += 1
        blk[v] = j
    return blk


class Sys:
    def __init__(self, cuts, M=None, window=None):
        self.cuts = list(cuts)
        self.Vk = self.cuts[-1]
        self.M = self.Vk if M is None else M
        assert self.M >= self.Vk
        self.blk = block_index(self.cuts, self.M)
        lo, hi = window if window else (1, self.M)
        self.wlo, self.whi = lo, hi
        self.vid = {}
        nxt = 1
        for u in range(lo, hi + 1):
            for v in range(u + 1, hi + 1):
                if self.blk[u] == self.blk[v]:
                    self.vid[(u, v)] = nxt
                    nxt += 1
        self.nvars = nxt - 1

    def lit(self, u, v):
        """literal for 'u before v'; True/False if forced by layout; None if dropped."""
        bu, bv = self.blk[u], self.blk[v]
        if bu != bv:
            return bu < bv
        key = (u, v) if u < v else (v, u)
        t = self.vid.get(key)
        if t is None:
            return None
        return t if u < v else -t

    def chain(self, vals):
        """clause forbidding positional chain vals[0]<vals[1]<...
        None  = chain impossible anyway (skip)
        'DROP'= involves a dropped variable
        []    = chain FORCED  -> the system is unsatisfiable outright
        list  = clause"""
        out = []
        for a, b in zip(vals, vals[1:]):
            t = self.lit(a, b)
            if t is True:
                continue
            if t is False:
                return None
            if t is None:
                return 'DROP'
            out.append(-t)
        return out

    def clauses(self, transitivity=True):
        M, Vk = self.M, self.Vk
        cls, dead = [], []
        for d in range(1, (M - 1) // 3 + 1):
            for x in range(1, M - 3 * d + 1):
                q = (x, x + d, x + 2 * d, x + 3 * d)
                for seq in (q, q[::-1]):
                    c = self.chain(seq)
                    if c is None or c == 'DROP':
                        continue
                    if not c:
                        dead.append(('C1', seq))
                    else:
                        cls.append(c)
        # (C2): x+2d <= Vk  and  x+3d > M
        for d in range(1, Vk // 2 + 1):
            xlo = max(1, M - 3 * d + 1)
            for x in range(xlo, Vk - 2 * d + 1):
                if x + 3 * d <= M:
                    continue
                c = self.chain((x, x + d, x + 2 * d))
                if c is None or c == 'DROP':
                    continue
                if not c:
                    dead.append(('C2', (x, x + d, x + 2 * d, '->', x + 3 * d)))
                else:
                    cls.append(c)
        if transitivity:
            cls.extend(self.trans_clauses())
        return cls, dead

    def trans_clauses(self):
        out = []
        byb = {}
        for v in range(self.wlo, self.whi + 1):
            byb.setdefault(self.blk[v], []).append(v)
        for vals in byb.values():
            for u, v, w in permutations3(vals):
                out.append([-self.lit(u, v), -self.lit(v, w), self.lit(u, w)])
        return out


def permutations3(vals):
    n = len(vals)
    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            for k in range(n):
                if k == i or k == j:
                    continue
                yield vals[i], vals[j], vals[k]


# ---------------------------------------------------------------- solving ----
def solve_eager(S, solver='cadical195', time_cap=None):
    from pysat.solvers import Solver
    cls, dead = S.clauses(transitivity=True)
    if dead:
        return 'GEOM_DEAD', dead[:3]
    with Solver(name=solver, bootstrap_with=cls) as s:
        r = s.solve()
        mod = s.get_model() if r else None
    if not r:
        return 'UNSAT', None
    return 'SAT', model_to_order(S, mod)


def model_to_order(S, model):
    val = {}
    for l in model:
        val[abs(l)] = l > 0
    byb = {}
    for v in range(1, S.M + 1):
        byb.setdefault(S.blk[v], []).append(v)
    order = []
    for j in sorted(byb):
        vals = byb[j]
        cnt = {v: 0 for v in vals}
        for u, w in combinations(vals, 2):
            t = S.vid.get((u, w))
            if t is None:
                continue
            if val.get(t, True):
                cnt[u] += 1
            else:
                cnt[w] += 1
        order.extend(sorted(vals, key=lambda v: -cnt[v]))
    return order


def solve_lazy(S, solver='cadical195', time_cap=1800, verbose=False, tag=''):
    """lazy transitivity CEGAR.  UNSAT sound (formula is a subset of the true one)."""
    import time
    import numpy as np
    from pysat.solvers import Solver
    cls, dead = S.clauses(transitivity=False)
    if dead:
        return 'GEOM_DEAD', dead[:3]
    byb = {}
    for v in range(S.wlo, S.whi + 1):
        byb.setdefault(S.blk[v], []).append(v)
    blocks = [byb[j] for j in sorted(byb)]
    s = Solver(name=solver, bootstrap_with=cls)
    t0 = time.time()
    rounds = 0
    while True:
        rounds += 1
        if not s.solve():
            return 'UNSAT', None
        if time.time() - t0 > time_cap:
            return 'TIME_CAP', None
        model = s.get_model()
        val = np.zeros(S.nvars + 1, dtype=bool)
        for l in model:
            a = abs(l)
            if a <= S.nvars:
                val[a] = l > 0
        clean = True
        order = []
        added = 0
        for vals in blocks:
            n = len(vals)
            A = np.zeros((n, n), dtype=np.uint8)
            for i in range(n):
                for j in range(i + 1, n):
                    t = S.vid.get((vals[i], vals[j]))
                    if t is None:
                        continue
                    if val[t]:
                        A[i, j] = 1
                    else:
                        A[j, i] = 1
            if n > 1:
                C = A.astype(np.uint32) @ A.astype(np.uint32)
                bad = (C > 0) & (A.T > 0)
                ii, kk = np.nonzero(bad)
            else:
                ii = kk = []
            if len(ii):
                clean = False
                for i, k in zip(ii, kk):
                    js = np.nonzero(A[i] & A[:, k])[0]
                    for j in js[:1]:
                        u, v, w = vals[int(i)], vals[int(j)], vals[int(k)]
                        for (a, b, c) in ((u, v, w), (v, w, u), (w, u, v)):
                            s.add_clause([-S.lit(a, b), -S.lit(b, c), S.lit(a, c)])
                        added += 3
                    if added > 40000:
                        break
            else:
                order.extend(sorted(vals, key=lambda v: -int(A[vals.index(v)].sum())))
        if clean:
            return 'SAT', order
        if verbose and rounds % 20 == 0:
            print(f"   [{tag}] round {rounds} +{added} ({time.time()-t0:.0f}s)",
                  flush=True)


def solve_cpsat(S, tlimit=None, nworkers=4):
    """second ENCODING (integer ranks + AllDifferent), different paradigm."""
    from ortools.sat.python import cp_model
    cls, dead = S.clauses(transitivity=False)
    if dead:
        return 'GEOM_DEAD', dead[:3]
    m = cp_model.CpModel()
    vals = list(range(S.wlo, S.whi + 1))
    rank = {v: m.NewIntVar(0, len(vals) - 1, f"r{v}") for v in vals}
    m.AddAllDifferent(list(rank.values()))
    b = {}
    for (u, v) in S.vid:
        z = m.NewBoolVar(f"b{u}_{v}")
        m.Add(rank[u] < rank[v]).OnlyEnforceIf(z)
        m.Add(rank[u] > rank[v]).OnlyEnforceIf(z.Not())
        b[(u, v)] = z
    id2 = {t: p for p, t in S.vid.items()}
    for c in cls:
        m.AddBoolOr([b[id2[abs(l)]] if l > 0 else b[id2[abs(l)]].Not() for l in c])
    sol = cp_model.CpSolver()
    sol.parameters.num_search_workers = nworkers
    if tlimit:
        sol.parameters.max_time_in_seconds = tlimit
    st = sol.Solve(m)
    if st == cp_model.INFEASIBLE:
        return 'UNSAT', None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        byb = {}
        for v in vals:
            byb.setdefault(S.blk[v], []).append(v)
        order = []
        for j in sorted(byb):
            order.extend(sorted(byb[j], key=lambda v: sol.Value(rank[v])))
        return 'SAT', order
    return 'UNKNOWN', None


# ------------------------------------------------------- witness verification -
def verify(cuts, M, seq):
    """Full independent check of a witness against the TRUSTED checker."""
    from apcheck import has_monotone_kap_general, has_monotone_kap_pos
    Vk = cuts[-1]
    assert sorted(seq) == list(range(1, M + 1)), "not a permutation of [1..M]"
    blk = block_index(cuts, M)
    last = -1
    for v in seq:
        assert blk[v] >= last, "block layout violated"
        last = max(last, blk[v])
    for c in cuts:
        assert set(seq[:c]) == set(range(1, c + 1)), f"{c} is not a cut"
    assert not has_monotone_kap_general(seq, 4), "C1 violated (trusted general)"
    assert not has_monotone_kap_pos(seq, 4), "C1 violated (trusted pos)"
    pos = {v: i for i, v in enumerate(seq)}
    for d in range(1, Vk // 2 + 1):
        for x in range(1, Vk - 2 * d + 1):
            if x + 3 * d <= M:
                continue
            if pos[x] < pos[x + d] < pos[x + 2 * d]:
                raise AssertionError(f"C2 violated x={x} d={d}")
    return True
