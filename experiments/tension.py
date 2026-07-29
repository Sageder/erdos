"""tension.py — the descent/realizability tension for class architectures, at UNBOUNDED delay.

The tension (derived inline, CORE Props 29/40/41):
  * NON-TAMENESS along a progression P requires the class function c to descend infinitely
    often along P (else c is eventually non-decreasing there and Prop 29 gives linear
    displacement, which is fatal).
  * But c -> infinity along P, so a descent forces c to REVISIT values: every progression
    then contains infinitely many SAME-CLASS pairs.
  * Same-class pairs are exactly where condition (ii) has NO content -- their relative
    order is decided inside the class -- so each one that sits in a 4-AP imposes a
    within-class ordering constraint. That is the realizability layer, which Prop 41 found
    UNSAT for binary delays.

So: non-tameness manufactures precisely the constraints that realizability struggles with.
This script tests whether more room in the delay (larger T) relieves it. We search JOINTLY
for a delay t : [1..N] -> [0..T] and within-class orders such that the induced permutation
is genuinely monotone-4-AP-free AND every progression of step <= Q has a positive descent
rate in c (finite proxy for non-tameness, bounding a RATE not one occurrence).

Encoding: order variables for the induced permutation (so within-class orders are free),
class-consistency clauses tying the order to c = j + t (lower class => earlier), the AP
clauses in FULL (both orientations, no coarse approximation), and the descent-rate clauses.
Lazy transitivity. Every SAT model is re-verified against the literal definitions.
"""
import sys, time, math
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from profile_cegar import find_cycles
from pysat.solvers import Cadical195, Glucose42
from pysat.formula import IDPool

def blk(v, b):
    j, p = 0, 1
    while p * b <= v: p *= b; j += 1
    return j

def build(N, b=3, T=1, Q=4, L=10):
    pool = IDPool(); cl = []
    X = lambda u, w: pool.id(('x', u, w))            # u<w : u before w
    lit = lambda u, w: X(u, w) if u < w else -X(w, u)
    # delay is one-hot over [0..T]
    D = lambda v, k: pool.id(('d', v, k))
    for v in range(1, N + 1):
        cl.append([D(v, k) for k in range(T + 1)])
        for k1 in range(T + 1):
            for k2 in range(k1 + 1, T + 1):
                cl.append([-D(v, k1), -D(v, k2)])
    # class consistency: c(u) < c(w)  =>  u before w  (classes emitted in increasing order)
    # c(v) = blk(v) + t(v); encode pairwise over the one-hot delay
    for u in range(1, N + 1):
        for w in range(1, N + 1):
            if u == w: continue
            ju, jw = blk(u, b), blk(w, b)
            for ku in range(T + 1):
                for kw in range(T + 1):
                    if ju + ku < jw + kw:
                        cl.append([-D(u, ku), -D(w, kw), lit(u, w)])
    # FULL AP constraints on the induced order (both orientations)
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            a = [lit(x + k * e, x + (k + 1) * e) for k in range(3)]
            cl.append([-a[0], -a[1], -a[2]]); cl.append([a[0], a[1], a[2]])
    # descent RATE: every window of L consecutive elements of every AP of step <= Q must
    # contain a class descent c(p_i) > c(p_{i+1})
    for q in range(1, Q + 1):
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            if len(P) < L + 2: continue
            for s0 in range(0, len(P) - L):
                W = P[s0:s0 + L]; lits = []
                for i in range(len(W) - 1):
                    u, w = W[i], W[i + 1]
                    z = pool.id(('desc', q, r, s0, i))
                    # z -> c(u) > c(w)
                    for ku in range(T + 1):
                        for kw in range(T + 1):
                            if not (blk(u, b) + ku > blk(w, b) + kw):
                                cl.append([-z, -D(u, ku), -D(w, kw)])
                    lits.append(z)
                cl.append(lits)
    return cl, pool, X, D

def solve(N, b=3, T=1, Q=4, L=10, max_rounds=100000):
    cl, pool, X, D = build(N, b, T, Q, L)
    S = Cadical195(bootstrap_with=cl); rounds = 0
    lit = lambda u, w: X(u, w) if u < w else -X(w, u)
    while True:
        if not S.solve():
            S.delete(); return "UNSAT", None, rounds
        model = set(S.get_model())
        order_of = lambda u, w: X(u, w) in model
        cycs = find_cycles(order_of, N)
        if not cycs:
            import functools
            vals = sorted(range(1, N + 1), key=functools.cmp_to_key(
                lambda u, w: -1 if (order_of(u, w) if u < w else not order_of(w, u)) else 1))
            t = {v: next(k for k in range(T + 1) if D(v, k) in model) for v in range(1, N + 1)}
            S.delete(); return "SAT", (vals, t), rounds
        for cyc in cycs:
            Lc = len(cyc)
            for i in range(Lc):
                u, w, z = cyc[i], cyc[(i+1) % Lc], cyc[(i+2) % Lc]
                if len({u, w, z}) == 3:
                    S.add_clause([-lit(u, w), -lit(w, z), lit(u, z)])
            S.add_clause([-lit(cyc[i], cyc[(i+1) % Lc]) for i in range(Lc)])
        rounds += 1
        if rounds > max_rounds:
            S.delete(); return "UNKNOWN", None, rounds

if __name__ == "__main__":
    for T in (1, 2, 3):
        for N in (60, 100, 150, 220):
            t0 = time.time(); res, out, rd = solve(N, T=T); dt = time.time() - t0
            extra = ""
            if res == "SAT":
                perm, t = out
                assert sorted(perm) == list(range(1, N + 1))
                assert not has_monotone_kap_pos(perm, 4), "model is NOT 4-AP-free!"
                extra = f"  (verified 4-AP-free; delay values used: {sorted(set(t.values()))})"
            print(f"T={T} N={N}: {res} ({dt:.0f}s, {rd} rounds){extra}", flush=True)
            if res in ("UNSAT", "UNKNOWN"): break
