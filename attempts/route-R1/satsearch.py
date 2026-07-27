"""satsearch.py — Route R1: exact feasibility of the block ansatz via SAT.

Claim tested: for a fixed block partition (covering values 1..V exactly) and a fixed
block layout order, does there exist ANY choice of per-block gadget permutations such
that the resulting prefix
  (i)  has no monotone 4-AP among values 1..V, and
  (ii) has no increasing 3-AP (x, x+d, x+2d) with x+3d > V
       [fatal for ANY continuation: every value > V is placed later in the layouts
        considered here, so such a 3-AP would complete to an increasing 4-AP], and
  (iii) if the layout places some covered block AFTER a not-yet-covered one — not the
        case for the layouts used here — this encoding would be unsound; we assert
        that all covered blocks precede all future values.

Encoding: boolean var o_{uv} (u<v, same block) = "pos(u) < pos(v)". Cross-block
relative positions are constants from the layout. Each forbidden monotone chain gives
one clause. In-block totality is automatic (vars are a tournament); acyclicity is
enforced lazily (CEGAR on 3-cycles) or eagerly for small blocks.

UNSAT at stage k  => the ansatz (that partition + layout, arbitrary gadgets) is DEAD.
SAT              => witness gadgets extracted and re-verified with framework checkers.
"""

import sys
from itertools import combinations
sys.path.insert(0, "/home/user/erdos/attempts/route-R1")
from framework import (monotone_4ap_violations, restrict_to_M, block_index_of,
                       has_monotone_4ap_np)
from pysat.solvers import Cadical153


class BlockOrderSAT:
    def __init__(self, blocks, layout=None):
        self.blocks = blocks                      # list of (lo,hi), consecutive, lo of first =1
        self.V = blocks[-1][1] - 1
        nb = len(blocks)
        self.layout = list(range(nb)) if layout is None else list(layout)
        # layout rank of each block
        self.rank = [0] * nb
        for pos, j in enumerate(self.layout):
            self.rank[j] = pos
        # var ids for in-block pairs
        self.varid = {}
        nxt = 1
        self.blk = [None] * (self.V + 1)
        for j, (lo, hi) in enumerate(blocks):
            for v in range(lo, hi):
                self.blk[v] = j
            for u, v in combinations(range(lo, hi), 2):
                self.varid[(u, v)] = nxt
                nxt += 1
        self.nvars = nxt - 1

    def lit_before(self, u, v):
        """literal meaning pos(u) < pos(v); returns +/-id, or True/False constant."""
        bu, bv = self.blk[u], self.blk[v]
        if bu != bv:
            return self.rank[bu] < self.rank[bv]
        if u < v:
            return self.varid[(u, v)]
        return -self.varid[(v, u)]

    def chain_clause(self, vals):
        """Clause forbidding pos(vals[0])<pos(vals[1])<...; None if impossible anyway,
        [] if forced (UNSAT geometry)."""
        lits = []
        for a, b in zip(vals, vals[1:]):
            t = self.lit_before(a, b)
            if t is True:
                continue
            if t is False:
                return None
            lits.append(-t)
        return lits            # clause: NOT(all before) == OR of negations

    def build_clauses(self, eager_transitivity_maxsize=60):
        V = self.V
        cls = []
        geom_dead = []
        # (1) all 4-APs inside coverage, both orientations
        for d in range(1, (V - 1) // 3 + 1):
            for x in range(1, V - 3 * d + 1):
                q = [x, x + d, x + 2 * d, x + 3 * d]
                for seq in (q, q[::-1]):
                    c = self.chain_clause(seq)
                    if c is None:
                        continue
                    if not c:
                        geom_dead.append((tuple(seq), 'forced by layout geometry'))
                    else:
                        cls.append(c)
        # (2) increasing 3-APs whose upward extension leaves coverage
        for d in range(1, V // 2 + 1):
            for x in range(1, V - 2 * d + 1):
                if x + 3 * d > V:
                    c = self.chain_clause([x, x + d, x + 2 * d])
                    if c is None:
                        continue
                    if not c:
                        geom_dead.append(((x, x + d, x + 2 * d, '->', x + 3 * d),
                                          'forced increasing 3-AP w/ future extension'))
                    else:
                        cls.append(c)
        # (3) eager transitivity for small blocks
        for j, (lo, hi) in enumerate(self.blocks):
            n = hi - lo
            if n <= eager_transitivity_maxsize:
                rng = range(lo, hi)
                for u in rng:
                    for v in rng:
                        for w in rng:
                            if u != v and v != w and u != w:
                                a, b = self.lit_before(u, v), self.lit_before(v, w)
                                cimp = self.lit_before(u, w)
                                cls.append([-a, -b, cimp])
        return cls, geom_dead

    def solve(self, eager_transitivity_maxsize=60, max_cegar_rounds=400, verbose=True):
        cls, geom_dead = self.build_clauses(eager_transitivity_maxsize)
        if geom_dead:
            if verbose:
                print(f"  GEOMETRY-DEAD: {len(geom_dead)} monotone chains forced by layout alone; first: {geom_dead[0]}")
            return 'GEOM_DEAD', geom_dead[:10]
        solver = Cadical153(bootstrap_with=cls)
        big_blocks = [j for j, (lo, hi) in enumerate(self.blocks)
                      if hi - lo > eager_transitivity_maxsize]
        for rnd in range(max_cegar_rounds):
            if not solver.solve():
                return 'UNSAT', None
            model = solver.get_model()
            val = {abs(l): (l > 0) for l in model}
            # check 3-cycles in big blocks
            added = 0
            for j in big_blocks:
                lo, hi = self.blocks[j]
                rng = list(range(lo, hi))
                # before[u][v] via vars
                def before(u, v):
                    if u < v:
                        return val[self.varid[(u, v)]]
                    return not val[self.varid[(v, u)]]
                # find 3-cycles u->v->w->u  (u before v, v before w, w before u)
                # tournament: acyclic iff transitive iff no directed 3-cycle
                # scan by outdegree argument: sort candidates cheaply
                for u, v, w in self._three_cycles(rng, before, cap=3000):
                    self._add_cycle_clauses(solver, u, v, w)
                    added += 3
            if added == 0:
                return 'SAT', self.extract(val)
            if verbose and rnd % 10 == 0:
                print(f"  cegar round {rnd}: added {added} transitivity clauses")
        return 'CEGAR_LIMIT', None

    def _three_cycles(self, rng, before, cap):
        out = []
        n = len(rng)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    u, v, w = rng[i], rng[j], rng[k]
                    b_uv, b_vw, b_uw = before(u, v), before(v, w), before(u, w)
                    # cycle exists iff the tournament on {u,v,w} is cyclic
                    # orientations: u->v if b_uv else v->u, etc.
                    # cyclic iff (u->v->w->u) or (u->w->v->u)
                    if (b_uv and b_vw and not b_uw) or ((not b_uv) and (not b_vw) and b_uw):
                        out.append((u, v, w))
                        if len(out) >= cap:
                            return out
        return out

    def _add_cycle_clauses(self, solver, u, v, w):
        for (a, b, c) in ((u, v, w), (v, w, u), (w, u, v)):
            la, lb = self.lit_before(a, b), self.lit_before(b, c)
            lc = self.lit_before(a, c)
            solver.add_clause([-la, -lb, lc])

    def extract(self, val):
        """Build the witness sequence from the model."""
        import functools
        seq = []
        for j in self.layout:
            lo, hi = self.blocks[j]
            vals = list(range(lo, hi))
            def cmp(u, v):
                if u == v:
                    return 0
                t = self.lit_before(u, v)
                b = val[t] if t > 0 else (not val[-t])
                return -1 if b else 1
            vals.sort(key=functools.cmp_to_key(cmp))
            seq.extend(vals)
        return seq


def verify_witness(blocks, seq, V):
    """Independent re-check of (i) and (ii) using framework/trusted code paths."""
    perm = restrict_to_M(seq, V)
    _, total = monotone_4ap_violations(perm, max_report=0, collect=False)
    assert total == 0, "witness has a monotone 4-AP!"
    # (ii) increasing 3-APs with x+3d > V
    pos = {v: i for i, v in enumerate(perm)}
    bad = []
    for d in range(1, V // 2 + 1):
        for x in range(1, V - 2 * d + 1):
            if x + 3 * d > V:
                if pos[x] < pos[x + d] < pos[x + 2 * d]:
                    bad.append((x, d))
    assert not bad, f"witness has fatal extension 3-APs: {bad[:5]}"
    return True


def stage_test(name, blocks, layout=None, eager=60):
    V = blocks[-1][1] - 1
    print(f"[{name}] V={V} blocks={[(lo,hi) for lo,hi in blocks]}"
          + (f" layout={layout}" if layout else " layout=in-order"))
    bs = BlockOrderSAT(blocks, layout)
    res, wit = bs.solve(eager_transitivity_maxsize=eager)
    if res == 'SAT':
        verify_witness(blocks, wit, V)
        print(f"  SAT — witness verified 4-AP-free on [1..{V}] with no fatal extension 3-AP")
        return wit
    print(f"  {res}")
    return None
