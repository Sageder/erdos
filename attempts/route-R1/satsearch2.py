"""satsearch2.py — Route R1: staged SAT for ARBITRARY block layouts (interleaved).

Setting: value blocks B_1, B_2, ... (finite intervals partitioning N), laid out in
positions by a bijective pattern pi: slot t -> block pi(t) (order type omega since
blocks are finite). A finite stage covers slots 1..T, i.e. block set S = {pi(1..T)}.
Values in uncovered blocks are placed after slot T's values.

Necessary constraints at a stage (both machine-enforced):
 (C1) no monotone 4-AP among covered values (cross-block comparisons fixed by slot
      order; in-block comparisons are SAT variables);
 (C2) no monotone 3-AP among covered values, read in position order, whose missing
      4th AP term (above for increasing, below for decreasing) lies in an UNCOVERED
      block — the 4th term will be placed later, completing a monotone 4-AP.
Soundness across stages: any stage-T' (>T) solution restricts to a stage-T solution,
and an infinite layout works iff every stage is feasible (Koenig; finite branching).

UNSAT at any stage kills the (partition, layout-pattern) pair for ALL gadget choices.
"""

import sys
import functools
from itertools import combinations
sys.path.insert(0, "/home/user/erdos/attempts/route-R1")
from pysat.solvers import Cadical153


class StagedLayoutSAT:
    def __init__(self, blocks, slot_order):
        """blocks: dict id -> (lo,hi) for COVERED blocks only (ids arbitrary ints).
        slot_order: list of covered block ids in slot order (len = #covered)."""
        self.blocks = blocks
        self.slot_order = list(slot_order)
        assert sorted(blocks) == sorted(slot_order)
        self.rank = {b: t for t, b in enumerate(slot_order)}
        self.blk = {}
        for b, (lo, hi) in blocks.items():
            for v in range(lo, hi):
                self.blk[v] = b
        self.covered = set(self.blk)
        self.varid = {}
        nxt = 1
        for b, (lo, hi) in sorted(blocks.items()):
            for u, v in combinations(range(lo, hi), 2):
                self.varid[(u, v)] = nxt
                nxt += 1

    def lit_before(self, u, v):
        bu, bv = self.blk[u], self.blk[v]
        if bu != bv:
            return self.rank[bu] < self.rank[bv]
        if u < v:
            return self.varid[(u, v)]
        return -self.varid[(v, u)]

    def chain_clause(self, vals):
        lits = []
        for a, b in zip(vals, vals[1:]):
            t = self.lit_before(a, b)
            if t is True:
                continue
            if t is False:
                return None
            lits.append(-t)
        return lits

    def clauses(self, eager_max=10**9):
        self._eager_max = eager_max
        cov = self.covered
        Vmax = max(cov)
        cls, dead = [], []
        # C1: full 4-APs inside coverage
        for d in range(1, (Vmax - 1) // 3 + 1):
            for x in range(1, Vmax - 3 * d + 1):
                q = [x, x + d, x + 2 * d, x + 3 * d]
                if not all(t in cov for t in q):
                    continue
                for seq in (q, q[::-1]):
                    c = self.chain_clause(seq)
                    if c is None:
                        continue
                    if not c:
                        dead.append(tuple(seq))
                    else:
                        cls.append(c)
        # C2: 3-APs with missing 4th term uncovered
        for d in range(1, Vmax // 2 + 1):
            for x in range(1, Vmax - 2 * d + 1):
                t = [x, x + d, x + 2 * d]
                if not all(v in cov for v in t):
                    continue
                if (x + 3 * d) not in cov:                    # upper ext, increasing
                    c = self.chain_clause(t)
                    if c is None:
                        pass
                    elif not c:
                        dead.append((x, x + d, x + 2 * d, '+ext'))
                    else:
                        cls.append(c)
                if x - d >= 1 and (x - d) not in cov:          # lower ext, decreasing
                    c = self.chain_clause(t[::-1])
                    if c is None:
                        pass
                    elif not c:
                        dead.append((x + 2 * d, x + d, x, '-ext'))
                    else:
                        cls.append(c)
        # transitivity (eager for blocks of size <= eager_max)
        for b, (lo, hi) in self.blocks.items():
            if hi - lo > getattr(self, '_eager_max', 10**9):
                continue
            rng = range(lo, hi)
            for u in rng:
                for v in rng:
                    for w in rng:
                        if u != v and v != w and u != w:
                            cls.append([-self.lit_before(u, v), -self.lit_before(v, w),
                                        self.lit_before(u, w)])
        return cls, dead

    def solve(self, eager_max=10**9, max_rounds=3000):
        cls, dead = self.clauses(eager_max=eager_max)
        if dead:
            return 'GEOM_DEAD', dead[:8]
        sol = Cadical153(bootstrap_with=cls)
        lazy_blocks = [b for b, (lo, hi) in self.blocks.items() if hi - lo > eager_max]
        import numpy as np
        for rnd in range(max_rounds):
            if not sol.solve():
                return 'UNSAT', None
            if not lazy_blocks:
                break
            model = sol.get_model()
            val = {abs(l): (l > 0) for l in model}
            added = 0
            for b in lazy_blocks:
                lo, hi = self.blocks[b]
                n = hi - lo
                A = np.zeros((n, n), dtype=bool)       # A[i,j] = (lo+i before lo+j)
                for i in range(n):
                    for j in range(i + 1, n):
                        t = self.varid[(lo + i, lo + j)]
                        A[i, j] = val[t]
                        A[j, i] = not val[t]
                # cyclic triangles: i->j->k->i ; enumerate via boolean matmul witness
                # For each ordered pair (i,j) with A[i,j], find k with A[j,k] and A[k,i].
                idx_i, idx_j = np.nonzero(A)
                for i, j in zip(idx_i, idx_j):
                    if i < j:                          # each cyclic triangle found from its min? not guaranteed; just dedupe roughly
                        ks = np.nonzero(A[j] & A[:, i])[0]
                        for k in ks[:2]:
                            u, v, w = lo + i, lo + j, lo + int(k)
                            for (a, bb, c) in ((u, v, w), (v, w, u), (w, u, v)):
                                sol.add_clause([-self.lit_before(a, bb),
                                                -self.lit_before(bb, c),
                                                self.lit_before(a, c)])
                            added += 1
                    if added > 20000:
                        break
            if added == 0:
                break
        else:
            return 'CEGAR_LIMIT', None
        val = {abs(l): (l > 0) for l in sol.get_model()}
        seq = []
        for b in self.slot_order:
            lo, hi = self.blocks[b]
            vals = list(range(lo, hi))
            def cmp(x, y):
                if x == y:
                    return 0
                t = self.lit_before(x, y)
                before = val[t] if t > 0 else (not val[-t])
                return -1 if before else 1
            vals.sort(key=functools.cmp_to_key(cmp))
            seq.extend(vals)
        self.verify(seq)
        return 'SAT', seq

    def verify(self, seq):
        """Independent recheck of C1 + C2 on the witness sequence (trusted-path:
        C1 via apcheck.has_monotone_kap_general on the raw sequence)."""
        sys.path.insert(0, "/home/user/erdos/experiments")
        from apcheck import has_monotone_kap_general
        assert not has_monotone_kap_general(seq, 4), "C1 violated (trusted checker)"
        pos = {v: i for i, v in enumerate(seq)}
        cov = self.covered
        Vmax = max(cov)
        for d in range(1, Vmax // 2 + 1):
            for x in range(1, Vmax - 2 * d + 1):
                t3 = (x, x + d, x + 2 * d)
                if not all(v in cov for v in t3):
                    continue
                inc3 = pos[t3[0]] < pos[t3[1]] < pos[t3[2]]
                dec3 = pos[t3[0]] > pos[t3[1]] > pos[t3[2]]
                if inc3 and (x + 3 * d) not in cov:
                    raise AssertionError(("C2+ violated (incr 3-AP, uncovered upper ext)", x, d))
                if dec3 and x - d >= 1 and (x - d) not in cov:
                    raise AssertionError(("C2- violated (decr 3-AP, uncovered lower ext)", x, d))


def stage(blocks_list, pattern, T, name="", **kw):
    """blocks_list: global list [(lo,hi)] indexed by block id 1..n (1-based).
    pattern: list of block ids in slot order (covering prefix of slots).
    T: number of slots covered."""
    ids = pattern[:T]
    blocks = {b: blocks_list[b - 1] for b in ids}
    nvals = sum(hi - lo for lo, hi in blocks.values())
    maxb = max(hi - lo for lo, hi in blocks.values())
    import time
    t0 = time.time()
    s = StagedLayoutSAT(blocks, ids)
    res, wit = s.solve(**kw)
    dt = time.time() - t0
    print(f"[{name} T={T}] covered={ids} nvals={nvals} maxblock={maxb}: {res} ({dt:.1f}s)",
          flush=True)
    return res, wit
