"""cutcore.py -- INDEPENDENT re-derivation of the R1 in-order cut-stage system.

Written from PROBLEM.md + the C1/C2 stage principle directly (not copied from
satsearch.py / cutsys.py); agreement with those is therefore cross-validation.

SETTING.  a : N -> N a bijection.  V is a CUT of a iff {a(1),...,a(V)} = {1..V}.
Given cuts 0 = V_0 < V_1 < ... < V_k, the blocks B_j = (V_{j-1}, V_j] are laid out
in increasing j, arbitrary order inside each block, everything > V_k afterwards.

NECESSARY conditions on the within-block orders, for a to be monotone-4-AP-free:
  (C1) no monotone 4-AP among the values [1..V_k], either orientation;
  (C2) no positionally-increasing 3-AP (x, x+d, x+2d) inside [1..V_k] with
       x+3d > V_k.  (x+3d exists and sits after position V_k by the cut property,
       so the 4-AP (x,x+d,x+2d,x+3d) would be increasing-monotone.)
No decreasing analogue of C2 is needed: every value < V_k is already placed, so a
value > V_k can never be the FIRST term of a decreasing chain.

Hence:  UNSAT  =>  no monotone-4-AP-free permutation of N has all of V_1..V_k as
cuts.  (Purely necessary-direction; no Koenig needed.)   SAT is only feasibility of
a necessary system -- it does NOT exhibit an infinite object.

Engines:
  enc_eager   : CNF with EAGER per-block transitivity  (pysat; UNSAT unconditional)
  solve_cpsat : integer ranks + AllDifferent (transitivity implicit; different
                paradigm, used as the second solver required by the project standard)
  brute_oracle: literal enumeration of all in-order block orderings, testing the
                DEFINITION of a monotone 4-AP (ground truth for tiny cut sets)
"""

import sys
from itertools import combinations, permutations, product

sys.path.insert(0, "/home/user/erdos/experiments")


# --------------------------------------------------------------------------- #
# geometry

def blocks_of(cuts):
    """List of blocks (as (lo,hi) inclusive) for the cut list."""
    out = []
    prev = 0
    for c in cuts:
        out.append((prev + 1, c))
        prev = c
    return out


def seg_index(cuts):
    """seg[v] for v in 1..V_k."""
    V = cuts[-1]
    seg = [0] * (V + 1)
    prev = 0
    for j, c in enumerate(cuts):
        for v in range(prev + 1, c + 1):
            seg[v] = j
        prev = c
    return seg


# --------------------------------------------------------------------------- #
# constraint generation (engine-independent): a list of "chains"

def chains(cuts):
    """Yield every positional chain that the system forbids, as a tuple of values.

    C1: (x, x+d, x+2d, x+3d) and its reverse, all terms <= V.
    C2: (x, x+d, x+2d) with x+2d <= V < x+3d.
    """
    V = cuts[-1]
    out = []
    for d in range(1, (V - 1) // 3 + 1):
        for x in range(1, V - 3 * d + 1):
            q = (x, x + d, x + 2 * d, x + 3 * d)
            out.append(q)
            out.append(q[::-1])
    for d in range(1, (V - 1) // 2 + 1):
        for x in range(1, V - 2 * d + 1):
            if x + 3 * d > V:
                out.append((x, x + d, x + 2 * d))
    return out


class System:
    def __init__(self, cuts):
        self.cuts = list(cuts)
        self.V = cuts[-1]
        self.seg = seg_index(self.cuts)
        self.vid = {}
        nxt = 1
        for u in range(1, self.V + 1):
            for v in range(u + 1, self.V + 1):
                if self.seg[u] == self.seg[v]:
                    self.vid[(u, v)] = nxt
                    nxt += 1
        self.nvars = nxt - 1

    def lit(self, u, v):
        """+t / -t meaning 'u before v'; True/False if fixed by the block layout."""
        su, sv = self.seg[u], self.seg[v]
        if su != sv:
            return su < sv
        t = self.vid[(u, v)] if u < v else -self.vid[(v, u)]
        return t

    def clauses(self):
        """Returns (cls, forced) where forced is a list of chains all of whose links
        are fixed TRUE by the layout (=> the system is unconditionally infeasible)."""
        cls = []
        forced = []
        for ch in chains(self.cuts):
            lits = []
            impossible = False
            for a, b in zip(ch, ch[1:]):
                t = self.lit(a, b)
                if t is True:
                    continue
                if t is False:
                    impossible = True
                    break
                lits.append(-t)
            if impossible:
                continue
            if not lits:
                forced.append(ch)
            else:
                cls.append(lits)
        return cls, forced

    def transitivity(self):
        out = []
        byb = {}
        for v in range(1, self.V + 1):
            byb.setdefault(self.seg[v], []).append(v)
        for vals in byb.values():
            for u, v, w in permutations(vals, 3):
                if u < w:            # each unordered triple contributes 3 clauses
                    out.append([-self.lit(u, v), -self.lit(v, w), self.lit(u, w)])
        return out


# --------------------------------------------------------------------------- #
# engine 1: eager CNF

def solve_eager(cuts, solver_name='cadical195', want_model=True):
    S = System(cuts)
    cls, forced = S.clauses()
    if forced:
        return 'UNSAT', {'reason': 'forced-chain', 'witness': forced[:3]}
    cls = cls + S.transitivity()
    from pysat.solvers import Solver
    with Solver(name=solver_name, bootstrap_with=cls) as s:
        r = s.solve()
        model = s.get_model() if (r and want_model) else None
    if not r:
        return 'UNSAT', {'reason': 'sat-solver', 'nclauses': len(cls)}
    return 'SAT', order_from_model(S, model)


def order_from_model(S, model):
    val = {}
    for l in model:
        if abs(l) <= S.nvars:
            val[abs(l)] = (l > 0)
    byb = {}
    for v in range(1, S.V + 1):
        byb.setdefault(S.seg[v], []).append(v)
    order = []
    for j in sorted(byb):
        vals = byb[j]
        # count of "before" relations = rank key
        key = {}
        for v in vals:
            c = 0
            for w in vals:
                if w == v:
                    continue
                t = S.lit(v, w)
                if (t > 0 and val.get(t, False)) or (t < 0 and not val.get(-t, False)):
                    c += 1
            key[v] = -c
        order.extend(sorted(vals, key=lambda v: key[v]))
    return order


# --------------------------------------------------------------------------- #
# engine 2: CP-SAT integer ranks

def solve_cpsat(cuts, tlimit=None, workers=8):
    from ortools.sat.python import cp_model
    S = System(cuts)
    cls, forced = S.clauses()
    if forced:
        return 'UNSAT', {'reason': 'forced-chain', 'witness': forced[:3]}
    m = cp_model.CpModel()
    byb = {}
    for v in range(1, S.V + 1):
        byb.setdefault(S.seg[v], []).append(v)
    rank = {}
    for j, vals in byb.items():
        n = len(vals)
        rs = [m.NewIntVar(0, n - 1, f"r{v}") for v in vals]
        m.AddAllDifferent(rs)
        for v, r in zip(vals, rs):
            rank[v] = r
    b = {}
    for (u, v), t in S.vid.items():
        z = m.NewBoolVar(f"b{u}_{v}")
        m.Add(rank[u] < rank[v]).OnlyEnforceIf(z)
        m.Add(rank[u] > rank[v]).OnlyEnforceIf(z.Not())
        b[t] = z
    for c in cls:
        m.AddBoolOr([b[l] if l > 0 else b[-l].Not() for l in c])
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    if tlimit:
        solver.parameters.max_time_in_seconds = tlimit
    st = solver.Solve(m)
    if st == cp_model.INFEASIBLE:
        return 'UNSAT', {'reason': 'cpsat'}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        order = []
        for j in sorted(byb):
            order.extend(sorted(byb[j], key=lambda v: solver.Value(rank[v])))
        return 'SAT', order
    return 'UNKNOWN', None


# --------------------------------------------------------------------------- #
# brute-force oracle over the literal definition (tiny cut sets only)

def brute_oracle(cuts):
    """Enumerate every in-order block ordering of [1..V]; test the DEFINITION of
    'monotone 4-AP' among the placed values (C1) and the C2 condition directly.
    Returns 'SAT' with a witness, or 'UNSAT'."""
    from apcheck import has_monotone_kap_general
    V = cuts[-1]
    bl = blocks_of(cuts)
    per = [list(permutations(range(lo, hi + 1))) for lo, hi in bl]
    for combo in product(*per):
        seq = [v for part in combo for v in part]
        if has_monotone_kap_general(seq, 4):
            continue
        pos = {v: i for i, v in enumerate(seq)}
        ok = True
        for d in range(1, (V - 1) // 2 + 1):
            for x in range(1, V - 2 * d + 1):
                if x + 3 * d > V and pos[x] < pos[x + d] < pos[x + 2 * d]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return 'SAT', seq
    return 'UNSAT', None


# --------------------------------------------------------------------------- #
# witness verification through the TRUSTED checker

def verify(cuts, seq):
    from apcheck import has_monotone_kap_general, has_monotone_kap_pos
    V = cuts[-1]
    assert sorted(seq) == list(range(1, V + 1)), "not a permutation of [1..V]"
    for c in cuts:
        assert set(seq[:c]) == set(range(1, c + 1)), f"cut {c} violated"
    assert not has_monotone_kap_general(list(seq), 4), "C1 violated (trusted general)"
    assert not has_monotone_kap_pos(list(seq), 4), "C1 violated (trusted pos)"
    pos = {v: i for i, v in enumerate(seq)}
    for d in range(1, (V - 1) // 2 + 1):
        for x in range(1, V - 2 * d + 1):
            if x + 3 * d > V:
                assert not (pos[x] < pos[x + d] < pos[x + 2 * d]), \
                    f"C2 violated x={x} d={d}"
    return True


# --------------------------------------------------------------------------- #
# engine 3: lazy-transitivity CEGAR (for large top blocks)
#
# The solved formula is always a SUBSET of the true system (C1 & C2 clauses plus a
# subset of the valid transitivity clauses), so UNSAT is SOUND without any further
# argument.  SAT is only returned when the per-block tournaments are acyclic, and the
# caller must re-verify the witness with verify().

def solve_lazy(cuts, solver_name='cadical195', time_cap=1800, verbose=False):
    import time
    import numpy as np
    from pysat.solvers import Solver
    S = System(cuts)
    cls, forced = S.clauses()
    if forced:
        return 'UNSAT', {'reason': 'forced-chain', 'witness': forced[:3]}
    byb = {}
    for v in range(1, S.V + 1):
        byb.setdefault(S.seg[v], []).append(v)
    blocks = [byb[j] for j in sorted(byb)]
    s = Solver(name=solver_name, bootstrap_with=cls)
    t0 = time.time()
    rounds = 0
    while True:
        rounds += 1
        if not s.solve():
            return 'UNSAT', {'reason': 'lazy', 'rounds': rounds}
        if time.time() - t0 > time_cap:
            return 'TIME_CAP', None
        model = s.get_model()
        val = np.zeros(S.nvars + 2, dtype=bool)
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
                    t = S.vid[(vals[i], vals[j])]
                    if val[t]:
                        A[i, j] = 1
                    else:
                        A[j, i] = 1
            if n > 1:
                C = A.astype(np.uint32) @ A.astype(np.uint32)
                ii, kk = np.nonzero((C > 0) & (A.T > 0))
            else:
                ii = kk = []
            if len(ii):
                clean = False
                for i, k in list(zip(ii, kk))[:4000]:
                    js = np.nonzero(A[i] & A[:, k])[0]
                    if not len(js):
                        continue
                    j = int(js[0])
                    u, v, w = vals[int(i)], vals[j], vals[int(k)]
                    for (a, b, c) in ((u, v, w), (v, w, u), (w, u, v)):
                        s.add_clause([-S.lit(a, b), -S.lit(b, c), S.lit(a, c)])
                    added += 3
            else:
                order.extend(sorted(vals, key=lambda v: -int(A[vals.index(v)].sum())))
        if clean:
            return 'SAT', order
        if added == 0:
            return 'STUCK', None
        if verbose and rounds % 20 == 0:
            print(f"   lazy round {rounds} (+{added}) {time.time()-t0:.0f}s", flush=True)


def confirm_unsat(cuts, second='glucose4'):
    """Re-decide with a SECOND solver on the eager encoding (project standard)."""
    return solve_eager(cuts, solver_name=second, want_model=False)[0]


# --------------------------------------------------------------------------- #
# WINDOW relaxation: only pairs inside [wlo,whi] are free variables; any clause
# with a same-block link outside the window is DROPPED.  Dropping clauses only
# weakens the system, so UNSAT of the relaxation is SOUND.

class WindowSystem(System):
    def __init__(self, cuts, wlo, whi):
        self.cuts = list(cuts)
        self.V = cuts[-1]
        self.seg = seg_index(self.cuts)
        self.wlo, self.whi = wlo, whi
        self.vid = {}
        nxt = 1
        for u in range(wlo, whi + 1):
            for v in range(u + 1, whi + 1):
                if self.seg[u] == self.seg[v]:
                    self.vid[(u, v)] = nxt
                    nxt += 1
        self.nvars = nxt - 1

    def lit(self, u, v):
        su, sv = self.seg[u], self.seg[v]
        if su != sv:
            return su < sv
        key = (u, v) if u < v else (v, u)
        if key not in self.vid:
            return None                     # unconstrained -> caller DROPs clause
        t = self.vid[key]
        return t if u < v else -t

    def clauses(self):
        cls, forced = [], []
        for ch in chains(self.cuts):
            lits, drop, impossible = [], False, False
            for a, b in zip(ch, ch[1:]):
                t = self.lit(a, b)
                if t is True:
                    continue
                if t is False:
                    impossible = True
                    break
                if t is None:
                    drop = True
                    break
                lits.append(-t)
            if impossible or drop:
                continue
            if not lits:
                forced.append(ch)
            else:
                cls.append(lits)
        return cls, forced

    def transitivity(self):
        out = []
        byb = {}
        for v in range(self.wlo, self.whi + 1):
            byb.setdefault(self.seg[v], []).append(v)
        for vals in byb.values():
            for u, v, w in permutations(vals, 3):
                if u < w:
                    out.append([-self.lit(u, v), -self.lit(v, w), self.lit(u, w)])
        return out


def solve_window(cuts, wlo, whi, solver_name='cadical195'):
    S = WindowSystem(cuts, wlo, whi)
    cls, forced = S.clauses()
    if forced:
        return 'UNSAT', {'reason': 'forced-chain', 'witness': forced[:3]}
    cls = cls + S.transitivity()
    from pysat.solvers import Solver
    with Solver(name=solver_name, bootstrap_with=cls) as s:
        r = s.solve()
    return ('SAT' if r else 'UNSAT'), {'nclauses': len(cls), 'nvars': S.nvars}
