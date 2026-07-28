"""blocksat.py — solve the per-block CSPs of the block decomposition (blocks.py) with
CP-SAT, block by block, and verify the assembled permutation with the trusted checker.

Modes for the only inter-block constraint type [2+2]
   (x,x+d) in B_j, (x+2d,x+3d) in B_{j+1}: NOT( x before x+d AND x+2d before x+3d ):
  "seq"    : solve B_0, B_1, ... in order; when solving B_{j+1}, every [2+2] whose lower
             pair was left un-inverted in pi_j becomes an inversion demand on the upper pair.
  "strong" : additionally demand that EVERY [2+2]-lower pair inside a block be inverted;
             this decouples the blocks completely (each block an independent CSP).

Output is a per-block SAT/UNSAT verdict.  UNSAT for a block under "seq" (with the strongest
possible help from below, i.e. after trying to invert as many lower pairs as possible) is a
genuine death certificate for that cut sequence.
"""

import sys, time, json
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from ortools.sat.python import cp_model                     # noqa: E402
from apcheck import has_monotone_kap_pos                    # noqa: E402
from blocks import constraints, blk_of, check_orders, assemble  # noqa: E402


def geom_cuts(r, top):
    c = [1]
    while c[-1] <= top:
        c.append(c[-1] * r)
    return c


def solve_block(vals, inv_pairs, noinc3, no4, extra_inv=(), time_limit=60.0, workers=4,
                hint=None):
    """CP-SAT for one block.  vals: sorted list of the block's values.
    inv_pairs: iterable of (u,w) u<w meaning w must come before u.
    noinc3: iterable of (a,e) meaning (a,a+e,a+2e) must NOT be positionally increasing.
    no4: iterable of (a,e) meaning (a,..,a+3e) must be neither inc nor dec.
    Returns (status_str, order or None)."""
    n = len(vals)
    idx = {v: i for i, v in enumerate(vals)}
    m = cp_model.CpModel()
    p = [m.NewIntVar(0, n - 1, f"p{v}") for v in vals]
    m.AddAllDifferent(p)
    bcache = {}

    def before(u, w):
        """Bool: p[u] < p[w]."""
        key = (u, w)
        if key in bcache:
            return bcache[key]
        b = m.NewBoolVar(f"b{u}_{w}")
        m.Add(p[idx[u]] < p[idx[w]]).OnlyEnforceIf(b)
        m.Add(p[idx[u]] > p[idx[w]]).OnlyEnforceIf(b.Not())
        bcache[key] = b
        return b

    for (u, w) in list(inv_pairs) + list(extra_inv):
        m.Add(p[idx[w]] < p[idx[u]])
    for (a, e) in noinc3:
        m.AddBoolOr([before(a, a + e).Not(), before(a + e, a + 2 * e).Not()])
    for (a, e) in no4:
        l1, l2, l3 = before(a, a + e), before(a + e, a + 2 * e), before(a + 2 * e, a + 3 * e)
        m.AddBoolOr([l1.Not(), l2.Not(), l3.Not()])
        m.AddBoolOr([l1, l2, l3])
    if hint:
        for v, pv in hint.items():
            if v in idx:
                m.AddHint(p[idx[v]], pv)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_search_workers = workers
    st = s.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        order = sorted(vals, key=lambda v: s.Value(p[idx[v]]))
        return "SAT", order
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


def run(cuts, N, mode="seq", time_limit=60.0, verbose=True):
    C = constraints(cuts, N)
    if C['fatal']:
        return dict(status="FATAL", detail=C['fatal'][:3])
    B = blk_of(cuts, N)
    blocks = {}
    for v in range(1, N + 1):
        blocks.setdefault(B[v], []).append(v)
    per_inv = {j: set() for j in blocks}
    per_noinc3 = {j: set() for j in blocks}
    per_no4 = {j: set() for j in blocks}
    for (j, u, w) in C['inv']:
        per_inv[j].add((u, w))
    for (j, a, e) in C['noinc3']:
        per_noinc3[j].add((a, e))
    for (j, a, e) in C['no4']:
        per_no4[j].add((a, e))
    # [2+2] links, indexed by the LOWER block
    low22 = {j: [] for j in blocks}
    for (lo, hi) in C['pair22']:
        low22[lo[0]].append((lo[1], lo[2], hi[0], hi[1], hi[2]))

    orders, report = {}, []
    for j in sorted(blocks):
        extra = set()
        if mode == "strong":
            extra |= {(a, b) for (a, b, _, _, _) in low22[j]}
        # induced demands from the block below
        for jj in sorted(blocks):
            if jj >= j:
                continue
            for (a, b, hk, c_, d_) in low22[jj]:
                if hk == j and jj in orders:
                    pos = {v: i for i, v in enumerate(orders[jj])}
                    if pos[a] < pos[b]:            # lower pair NOT inverted
                        extra.add((c_, d_))
        t0 = time.time()
        st, order = solve_block(blocks[j], per_inv[j], per_noinc3[j], per_no4[j],
                                extra_inv=extra, time_limit=time_limit)
        dt = time.time() - t0
        report.append(dict(block=j, size=len(blocks[j]), rng=[blocks[j][0], blocks[j][-1]],
                           n_inv=len(per_inv[j]), n_extra=len(extra),
                           n_noinc3=len(per_noinc3[j]), n_no4=len(per_no4[j]),
                           status=st, secs=round(dt, 1)))
        if verbose:
            print(f"    block {j} [{blocks[j][0]}..{blocks[j][-1]}] size={len(blocks[j])}: "
                  f"{st} ({dt:.1f}s)  inv={len(per_inv[j])}+{len(extra)} "
                  f"noinc3={len(per_noinc3[j])} no4={len(per_no4[j])}", flush=True)
        if st != "SAT":
            return dict(status=st, first_bad_block=j, report=report)
        orders[j] = order
    perm = assemble(cuts, N, orders)
    bad = check_orders(cuts, N, orders)
    assert not bad, bad
    assert not has_monotone_kap_pos(perm, 4), "TRUSTED CHECKER DISAGREES"
    return dict(status="SAT", report=report, perm=perm)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "seq"
    for r in (3, 4, 5, 6):
        for top in (r ** 3, r ** 4, r ** 5):
            cuts = geom_cuts(r, top)
            N = cuts[-1] - 1
            if N > 8000:
                continue
            print(f"\n== ratio {r}, cuts={cuts[:-1]}, N={N}, mode={mode} ==", flush=True)
            res = run(cuts, N, mode=mode, time_limit=120.0)
            print(f"  => {res['status']}", flush=True)
            if res['status'] == 'SAT':
                with open(f"witness_r{r}_N{N}_{mode}.json", "w") as f:
                    json.dump(res['perm'], f)
            else:
                break
