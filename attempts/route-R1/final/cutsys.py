"""cutsys.py — INDEPENDENT re-implementation of the R1 in-order cut-stage constraint
system (route-R1/final).  Written from the mathematical definition, not from
satsearch.py / satsearch2.py, so that agreement is genuine cross-validation.

SETTING.  Let 0 = V_0 < V_1 < ... < V_k be cut points.  An "in-order cut permutation
with cut prefix (V_1,...,V_k)" is a permutation a of N such that for each j <= k the
value set [1..V_j] occupies exactly the first V_j positions.  Equivalently the blocks
B_j = (V_{j-1}, V_j] are laid out in increasing order of j, each internally in an
arbitrary order, and everything above V_k comes after.

NECESSARY CONDITIONS on the internal orders (both machine-enforced here):
  (C1) no monotone 4-AP among values [1..V_k] (either orientation);
  (C2) no positionally-increasing 3-AP (x, x+d, x+2d) inside [1..V_k] with
       x + 3d > V_k  (that 4th term is placed later, completing an increasing 4-AP).
No "decreasing 3-AP with missing lower term" condition is needed: all values below
V_k are covered.

SOUNDNESS.  C1 and C2 are necessary for every 4-AP-free permutation of N whose cut
set contains {V_1,...,V_k}.  Hence UNSAT  =>  NO 4-AP-free permutation of N has all
of V_1,...,V_k as cut points.  (No Koenig needed for the negative direction; Koenig
is only needed for the converse "all stages SAT => an infinite object exists".)

RELAXATIONS (all preserve soundness of UNSAT):
  * TOP relaxation: keep only clauses all of whose free literals are pairs inside the
    top block (V_{k-1}, V_k].  Cross-block orders are constants.
  * WINDOW relaxation: keep only clauses all of whose free literals are pairs inside
    a value window W.  Dropping clauses can only make the system easier.
Transitivity clauses on the retained variables are valid consequences and may be
added eagerly.
"""

import sys
from itertools import combinations

# ---------------------------------------------------------------------------
# geometry


def seg_of(cuts):
    """seg(v) = index of the block containing v (0-based); len(cuts) if v > V_k."""
    def seg(v):
        for j, c in enumerate(cuts):
            if v <= c:
                return j
        return len(cuts)
    return seg


class CutSystem:
    """Order-variable encoding of (C1)&(C2) for an in-order cut prefix."""

    def __init__(self, cuts, window=None):
        self.cuts = list(cuts)
        self.V = cuts[-1]
        self.seg = seg_of(self.cuts)
        if window is None:
            window = (1, self.V)
        self.wlo, self.whi = window
        self.free = set(v for v in range(self.wlo, self.whi + 1))
        # a pair (u<v) is a FREE variable iff same block and both in window
        self.vid = {}
        nxt = 1
        for u, v in combinations(sorted(self.free), 2):
            if self.seg(u) == self.seg(v):
                self.vid[(u, v)] = nxt
                nxt += 1
        self.nvars = nxt - 1

    def lit(self, u, v):
        """Literal for 'u is positioned before v'.  True/False if determined."""
        su, sv = self.seg(u), self.seg(v)
        if su != sv:
            return su < sv          # in-order layout: earlier block first
        key = (u, v) if u < v else (v, u)
        if key not in self.vid:
            return None             # same block but not a retained variable
        t = self.vid[key]
        return t if u < v else -t

    def chain(self, vals):
        """Clause forbidding the positional chain vals[0] < vals[1] < ... .
        Returns:  None            if the chain is impossible anyway (skip),
                  'DROP'          if some pair is a non-retained variable,
                  []              if the chain is FORCED (geometry-dead),
                  list of lits    otherwise."""
        lits = []
        for a, b in zip(vals, vals[1:]):
            t = self.lit(a, b)
            if t is True:
                continue
            if t is False:
                return None
            if t is None:
                return 'DROP'
            lits.append(-t)
        return lits

    def clauses(self, transitivity=True):
        V = self.V
        cls = []
        dead = []
        # (C1) 4-APs inside [1..V], both orientations
        for d in range(1, (V - 1) // 3 + 1):
            for x in range(1, V - 3 * d + 1):
                q = (x, x + d, x + 2 * d, x + 3 * d)
                for seq in (q, q[::-1]):
                    c = self.chain(seq)
                    if c is None or c == 'DROP':
                        continue
                    if not c:
                        dead.append(('C1', seq))
                    else:
                        cls.append(c)
        # (C2) increasing 3-APs with the 4th term above V
        for d in range(1, V // 2 + 1):
            for x in range(max(1, V - 3 * d + 1), V - 2 * d + 1):
                if x + 3 * d <= V:
                    continue
                c = self.chain((x, x + d, x + 2 * d))
                if c is None or c == 'DROP':
                    continue
                if not c:
                    dead.append(('C2', (x, x + d, x + 2 * d, '->', x + 3 * d)))
                else:
                    cls.append(c)
        if transitivity:
            cls.extend(self.transitivity_clauses())
        return cls, dead

    def transitivity_clauses(self):
        """Eager transitivity on retained variables, per block."""
        out = []
        byblock = {}
        for v in sorted(self.free):
            byblock.setdefault(self.seg(v), []).append(v)
        for _, vals in byblock.items():
            n = len(vals)
            for i in range(n):
                for j in range(n):
                    if j == i:
                        continue
                    for k in range(n):
                        if k == i or k == j:
                            continue
                        u, v, w = vals[i], vals[j], vals[k]
                        out.append([-self.lit(u, v), -self.lit(v, w), self.lit(u, w)])
        return out


# ---------------------------------------------------------------------------
# engine 1: pysat


def solve_pysat(cls, nvars, solver_name='cadical195', assumptions=None):
    from pysat.solvers import Solver
    with Solver(name=solver_name, bootstrap_with=cls) as s:
        r = s.solve(assumptions=assumptions or [])
        model = s.get_model() if r else None
    return ('SAT' if r else 'UNSAT'), model


# ---------------------------------------------------------------------------
# engine 2: CP-SAT with INTEGER ranks (transitivity implicit; different paradigm)


def solve_cpsat(sysobj, nworkers=4, tlimit=None, log=False):
    from ortools.sat.python import cp_model
    vals = sorted(sysobj.free)
    n = len(vals)
    m = cp_model.CpModel()
    rank = {v: m.NewIntVar(0, n - 1, f"r{v}") for v in vals}
    m.AddAllDifferent(list(rank.values()))
    # boolean b[(u,v)] <-> rank[u] < rank[v], only for retained variables
    b = {}
    for (u, v) in sysobj.vid:
        z = m.NewBoolVar(f"b{u}_{v}")
        m.Add(rank[u] < rank[v]).OnlyEnforceIf(z)
        m.Add(rank[u] > rank[v]).OnlyEnforceIf(z.Not())
        b[(u, v)] = z
    cls, dead = sysobj.clauses(transitivity=False)
    if dead:
        return 'GEOM_DEAD', dead[:5]
    id2pair = {t: p for p, t in sysobj.vid.items()}
    for c in cls:
        lits = []
        for l in c:
            p = id2pair[abs(l)]
            lits.append(b[p] if l > 0 else b[p].Not())
        m.AddBoolOr(lits)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = nworkers
    solver.parameters.log_search_progress = log
    if tlimit:
        solver.parameters.max_time_in_seconds = tlimit
    st = solver.Solve(m)
    if st == cp_model.INFEASIBLE:
        return 'UNSAT', None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        order = sorted(vals, key=lambda v: solver.Value(rank[v]))
        return 'SAT', order
    return 'UNKNOWN', None


# ---------------------------------------------------------------------------
# lazy-transitivity engine for large blocks (sound for UNSAT)


def solve_lazy(sysobj, solver_name='cadical195', max_rounds=200000,
               per_round_cap=40000, time_cap=3600, verbose=False, tag=''):
    import time
    import numpy as np
    from pysat.solvers import Solver
    cls, dead = sysobj.clauses(transitivity=False)
    if dead:
        return 'GEOM_DEAD', dead[:5]
    vals = sorted(sysobj.free)
    idx = {v: i for i, v in enumerate(vals)}
    n = len(vals)
    id2pair = {t: p for p, t in sysobj.vid.items()}
    s = Solver(name=solver_name, bootstrap_with=cls)
    t0 = time.time()
    rounds = 0
    total = 0
    while True:
        rounds += 1
        if not s.solve():
            if verbose:
                print(f"  [{tag}] UNSAT rounds={rounds} lazy={total} "
                      f"{time.time()-t0:.0f}s", flush=True)
            return 'UNSAT', None
        if time.time() - t0 > time_cap:
            return 'TIME_CAP', None
        model = s.get_model()
        val = np.zeros(sysobj.nvars + 1, dtype=bool)
        for l in model:
            a = abs(l)
            if a <= sysobj.nvars:
                val[a] = l > 0
        A = np.zeros((n, n), dtype=np.uint8)
        for t, (u, v) in id2pair.items():
            if val[t]:
                A[idx[u], idx[v]] = 1
            else:
                A[idx[v], idx[u]] = 1
        C = (A.astype(np.uint32) @ A.astype(np.uint32))
        bad = (C > 0) & (A.T > 0)
        ii, kk = np.nonzero(bad)
        if len(ii) == 0:
            order = sorted(vals, key=lambda v: -int(np.sum(A[idx[v]])))
            return 'SAT', order
        added = 0
        for i, k in zip(ii, kk):
            js = np.nonzero(A[i] & A[:, k])[0]
            for j in js[:1]:
                u, v, w = vals[int(i)], vals[int(j)], vals[int(k)]
                for (a, bb, cc) in ((u, v, w), (v, w, u), (w, u, v)):
                    la, lb, lc = sysobj.lit(a, bb), sysobj.lit(bb, cc), sysobj.lit(a, cc)
                    s.add_clause([-la, -lb, lc])
                added += 3
            if added >= per_round_cap:
                break
        total += added
        if verbose and rounds % 25 == 0:
            print(f"  [{tag}] round {rounds}: {len(ii)} cyc pairs +{added} "
                  f"({time.time()-t0:.0f}s)", flush=True)


# ---------------------------------------------------------------------------
# independent verification of a SAT witness (trusted checker path)


def verify_witness_full(cuts, order_by_block):
    """order_by_block: dict block-index -> list of values in position order,
    or a flat list of ALL values 1..V in position order.  Checks C1 with the
    TRUSTED checker in experiments/apcheck.py, and C2 directly."""
    sys.path.insert(0, "/home/user/erdos/experiments")
    from apcheck import has_monotone_kap_general
    V = cuts[-1]
    seq = order_by_block if isinstance(order_by_block, list) else None
    assert seq is not None
    assert sorted(seq) == list(range(1, V + 1)), "not a permutation of [1..V]"
    # blocks in order
    sg = seg_of(cuts)
    last = -1
    for v in seq:
        s_ = sg(v)
        assert s_ >= last, "block order violated"
        last = max(last, s_)
    assert not has_monotone_kap_general(seq, 4), "C1 VIOLATED (trusted checker)"
    pos = {v: i for i, v in enumerate(seq)}
    for d in range(1, V // 2 + 1):
        for x in range(max(1, V - 3 * d + 1), V - 2 * d + 1):
            if x + 3 * d <= V:
                continue
            if pos[x] < pos[x + d] < pos[x + 2 * d]:
                raise AssertionError(f"C2 VIOLATED at x={x} d={d}")
    return True
