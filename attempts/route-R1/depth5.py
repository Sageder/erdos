"""depth5.py — decide the depth-5 island with two sound probes per point.

Point set: {2,8,26,140,V5} for V5 in {740,760,780,800}, and {5,25,125,625}.

Probe L (LOCAL, top segment only): all constraints that involve ONLY top-segment
order variables, with cross-segment positions fixed by the layout:
  - unit inversions: APs with exactly one free top pair, other terms in distinct
    earlier segments (their mutual order is layout-fixed increasing);
  - triple bans: APs with 3 top terms + 1 term below (increasing orientation only —
    decreasing needs the below-term last, impossible in-order);
  - in-segment 4-AP bans (both orientations) and increasing-3AP bans with
    x+3d > V5 (upper extension) or x-d in a lower segment (lower extension...
    the latter is again a triple/unit ban depending on how many terms are top);
  - APs whose below-terms share a segment are DROPPED (they couple lower-segment
    variables): the local system is a sound RELAXATION — UNSAT => config dead.
Probe F (FULL): the complete satsearch-style system, lazy transitivity everywhere
above a size cap, with numpy-vectorized cyclic-triangle detection (all triangles
found per round, capped clause additions).

Soundness of lazy UNSAT: clauses added are always implied (transitivity instances),
and UNSAT of a subset implies UNSAT of the full system.  SAT results from probe F are
re-verified with the trusted checker; SAT of probe L alone is inconclusive.
"""

import sys, time
from itertools import combinations
import numpy as np
sys.path.insert(0, "/home/user/erdos/attempts/route-R1")
from pysat.solvers import Cadical153


def seg_of_factory(cuts):
    def seg(v):
        for j, c in enumerate(cuts):
            if v <= c:
                return j
        return len(cuts)
    return seg


def local_top_probe(cuts, verbose=True):
    """Probe L for cut list cuts=[V1..Vk]; top segment (V_{k-1}, V_k]."""
    Vmax, Vprev = cuts[-1], cuts[-2]
    seg = seg_of_factory(cuts)
    top = lambda v: Vprev < v <= Vmax
    vals = list(range(Vprev + 1, Vmax + 1))
    vid = {}
    nxt = 1
    for a, b in combinations(vals, 2):
        vid[(a, b)] = nxt; nxt += 1
    def lit(a, b):
        return vid[(a, b)] if a < b else -vid[(b, a)]

    cls = []
    geom_dead = None
    # full 4-APs with >=2 top terms
    for d in range(1, (Vmax - 1) // 3 + 1):
        for x in range(1, Vmax - 3 * d + 1):
            q = [x, x + d, x + 2 * d, x + 3 * d]
            tmask = [top(t) for t in q]
            ntop = sum(tmask)
            if ntop == 4:
                cls.append([-lit(q[0], q[1]), -lit(q[1], q[2]), -lit(q[2], q[3])])
                cls.append([-lit(q[3], q[2]), -lit(q[2], q[1]), -lit(q[1], q[0])])
            elif ntop == 3:      # q[1],q[2],q[3] top, q[0] below (placed first)
                cls.append([-lit(q[1], q[2]), -lit(q[2], q[3])])
            elif ntop == 2:      # q[2],q[3] top; q[0],q[1] below
                s0, s1 = seg(q[0]), seg(q[1])
                if s0 != s1:     # order fixed increasing => unit ban on top pair
                    cls.append([-lit(q[2], q[3])])
                # same lower segment: coupled clause, dropped (relaxation)
    # extension 3-APs x+2d <= Vmax < x+3d
    for d in range(1, Vmax // 2 + 1):
        for x in range(1, Vmax - 2 * d + 1):
            if x + 3 * d <= Vmax:
                continue
            t = [x, x + d, x + 2 * d]
            tmask = [top(v) for v in t]
            ntop = sum(tmask)
            if ntop == 3:
                cls.append([-lit(t[0], t[1]), -lit(t[1], t[2])])
            elif ntop == 2:      # t[1],t[2] top, t[0] below
                cls.append([-lit(t[1], t[2])])
            elif ntop == 1 and seg(t[0]) != seg(t[1]):
                geom_dead = (x, d)   # forced increasing chain, config dead outright
    if geom_dead:
        if verbose:
            print(f"  local probe {cuts}: GEOM_DEAD via {geom_dead}", flush=True)
        return 'GEOM_DEAD'
    return cegar_solve(vals, vid, lit, cls, tag=f"local {cuts}", verbose=verbose)


def cegar_solve(vals, vid, lit, cls, tag="", verbose=True, max_rounds=100000,
                per_round_cap=60000, time_cap=5400):
    n = len(vals)
    lo = vals[0]
    sol = Cadical153(bootstrap_with=cls)
    t0 = time.time()
    rounds = 0
    added_total = 0
    while True:
        rounds += 1
        if not sol.solve():
            print(f"  [{tag}] UNSAT after {rounds} rounds, {added_total} lazy clauses, "
                  f"{time.time()-t0:.0f}s", flush=True)
            return 'UNSAT'
        if time.time() - t0 > time_cap:
            print(f"  [{tag}] TIME_CAP after {rounds} rounds ({time.time()-t0:.0f}s)", flush=True)
            return 'TIME_CAP'
        model = sol.get_model()
        val = np.zeros(len(vid) + 1, dtype=bool)
        for l in model:
            a = abs(l)
            if a <= len(vid):
                val[a] = l > 0
        A = np.zeros((n, n), dtype=np.uint8)
        for (a, b), i in vid.items():
            if val[i]:
                A[a - lo, b - lo] = 1
            else:
                A[b - lo, a - lo] = 1
        # cyclic triangles: pairs (i,k) with A[k,i]=1 and exists j: A[i,j]&A[j,k]
        C = (A @ A)                      # uint8 overflow ok for detection? use uint16
        C = (A.astype(np.uint16) @ A.astype(np.uint16))
        bad = (C > 0) & (A.T > 0)
        idx_i, idx_k = np.nonzero(bad)
        if len(idx_i) == 0:
            print(f"  [{tag}] SAT after {rounds} rounds, {added_total} lazy clauses, "
                  f"{time.time()-t0:.0f}s", flush=True)
            order = sorted(vals, key=lambda v: int(np.sum(A[:, v - lo])))
            return ('SAT', order, A)
        added = 0
        for i, k in zip(idx_i, idx_k):
            js = np.nonzero(A[i] & A[:, k])[0]
            for j in js[:1]:
                u, v, w = vals[int(i)], vals[int(j)], vals[int(k)]
                for (a, b, c) in ((u, v, w), (v, w, u), (w, u, v)):
                    sol.add_clause([-lit(a, b), -lit(b, c), lit(a, c)])
                added += 3
            if added >= per_round_cap:
                break
        added_total += added
        if verbose and rounds % 20 == 0:
            print(f"  [{tag}] round {rounds}: {len(idx_i)} cyclic pairs, "
                  f"+{added} clauses ({time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    jobs = []
    if which in ("all", "chain"):
        for V5 in (740, 760, 780, 800):
            jobs.append([2, 8, 26, 140, V5])
    if which in ("all", "pure"):
        jobs.append([5, 25, 125, 625])
    for cuts in jobs:
        r = local_top_probe(cuts)
        tagr = r if isinstance(r, str) else r[0]
        print(f"LOCAL PROBE {cuts}: {tagr}", flush=True)
    print("DEPTH5 LOCAL DONE", flush=True)
