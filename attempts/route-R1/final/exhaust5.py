"""exhaust5.py — EXHAUSTIVE search for a feasible 5-element cut set with max <= M.

A "cut" of a permutation a of N is a value V with pos_a(v) <= V for all v <= V
(equivalently [1..V] fills the first V positions).  Feasibility of a finite cut set
S is a NECESSARY condition (C1&C2 of cutsys.py) for some monotone-4-AP-free
permutation of N to have all of S as cuts; feasibility is monotone: S' feasible and
S subset of S'  =>  S feasible.  So a DFS over prefixes with pruning is exhaustive.

Geometry (Lemma G, proved + machine-checked): with >= 2 cuts already fixed, the next
cut V must satisfy V >= 3*V_prev - 2.  This prunes the branching factor hard.

Output: every feasible cut set found, and the verdict on depth 5.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/final")
from cutsys import CutSystem, solve_lazy, verify_witness_full

M = int(sys.argv[1]) if len(sys.argv) > 1 else 200
TCAP = float(sys.argv[2]) if len(sys.argv) > 2 else 600.0

CACHE = {}
STATS = {'calls': 0, 'sat': 0, 'unsat': 0, 'time': 0.0}


def feas(cuts):
    key = tuple(cuts)
    if key in CACHE:
        return CACHE[key]
    t0 = time.time()
    s = CutSystem(list(cuts))
    r, w = solve_lazy(s, solver_name='cadical195', time_cap=TCAP)
    dt = time.time() - t0
    STATS['calls'] += 1
    STATS['time'] += dt
    if r == 'SAT':
        verify_witness_full(list(cuts), list(w))
        STATS['sat'] += 1
    elif r == 'UNSAT':
        STATS['unsat'] += 1
    else:
        print(f"!! {r} at {list(cuts)} ({dt:.0f}s) -- treated as INCONCLUSIVE, "
              f"branch kept alive", flush=True)
    CACHE[key] = r
    return r


FOUND5 = []


def dfs(cuts, depth):
    """cuts is feasible; extend."""
    if depth == 5:
        FOUND5.append(list(cuts))
        print(f"*** DEPTH-5 FEASIBLE: {list(cuts)}", flush=True)
        return
    last = cuts[-1]
    if len(cuts) >= 2:
        lo = 3 * last - 2          # geometry lemma
    else:
        lo = last + 1
    # remaining depth needs at least (5-depth) more cuts, each >= 3x-2
    need = 5 - depth
    for V in range(lo, M + 1):
        # can we still reach depth 5 within M?  V, 3V-2, 9V-8, ...
        w = V
        ok = True
        for _ in range(need - 1):
            w = 3 * w - 2
            if w > M:
                ok = False
                break
        if not ok:
            break
        r = feas(cuts + [V])
        if r != 'UNSAT':
            dfs(cuts + [V], depth + 1)


if __name__ == "__main__":
    print(f"# exhaustive 5-cut search, max cut <= {M}", flush=True)
    t0 = time.time()
    # V1: any value; V2: any value > V1.  Bound them by the reachability test.
    for V1 in range(1, M + 1):
        w = V1
        ok = True
        for _ in range(4):
            w = 3 * w - 2 if w > 1 else w + 1
            if w > M:
                ok = False
                break
        if not ok:
            break
        r = feas([V1])
        if r == 'UNSAT':
            continue
        for V2 in range(V1 + 1, M + 1):
            w = V2
            ok = True
            for _ in range(3):
                w = 3 * w - 2
                if w > M:
                    ok = False
                    break
            if not ok:
                break
            if feas([V1, V2]) == 'UNSAT':
                continue
            dfs([V1, V2], 2)
    print(f"# DONE M={M}: depth-5 feasible sets = {FOUND5}", flush=True)
    print(f"# stats {STATS} wall={time.time()-t0:.0f}s", flush=True)
