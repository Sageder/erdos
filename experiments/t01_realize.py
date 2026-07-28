"""t01_realize.py — the decisive question for the T=1 class-architecture family.

Is there ANY binary delay t : [1..N] -> {0,1} such that the architecture
c = floor(log_b v) + t(v), classes emitted in increasing index order, admits SOME choice of
within-class orders giving a monotone-4-AP-free permutation of [1..N]?

Here BOTH the delay and the within-class orders are unknowns, solved jointly. For a pair
(u,w) the literal "u before w" is
      B(u,w)  <=>  c(u) < c(w)  OR  ( c(u) = c(w)  AND  y_{uw} ),
with c(u) = j(u) + t(u), j fixed and t Boolean; y is a free same-class order variable.
Monotone 4-APs are forbidden on B in both orientations; transitivity is enforced lazily
(CEGAR), then any model is decoded and re-verified with the trusted checker.

UNSAT at some N is an impossibility theorem for the whole T=1 family at that size,
quantified over all delays AND all within-class orders.
Known reference points: t == 0 is the contiguous ratio-b block layout (dead by routes
R1/R3); t = v2 mod 2 style delays are the CLS families (CLS(3,a) died at N=250, route R20).
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from farleft import blk
from profile_cegar import find_cycles
from pysat.solvers import Cadical195, Glucose42
from pysat.formula import IDPool


def solve(N, b=3, max_rounds=200000):
    pool = IDPool()
    T = lambda v: pool.id(('t', v))
    Y = lambda u, w: pool.id(('y', u, w))          # u < w, same-class order
    B = lambda u, w: pool.id(('B', u, w))          # "u before w", for u != w
    j = [0] + [blk(v, b) for v in range(1, N + 1)]
    cl = []
    for u in range(1, N + 1):
        for w in range(1, N + 1):
            if u == w: continue
            D = j[w] - j[u]
            bu = B(u, w)
            # c(u) < c(w)  <=>  t(u) - t(w) < D
            if D >= 2:      cl.append([bu])                       # always before
            elif D <= -2:   cl.append([-bu])                      # never before
            elif D == 1:    # before unless t(u)=1,t(w)=0
                cl.append([bu, T(u)]); cl.append([bu, -T(w)])
                cl.append([-bu, -T(u), T(w)])
                # tie case t(u)=1,t(w)=0 -> same class -> use y
                # handled by the equality branch below via implication
            elif D == -1:   # c(u) < c(w) iff t(u)=0,t(w)=1
                cl.append([-bu, -T(u)]); cl.append([-bu, T(w)])
                cl.append([bu, T(u), -T(w)])
            else:           # D == 0: c(u)<c(w) iff t(u)=0,t(w)=1; equal iff t(u)=t(w)
                y = Y(u, w) if u < w else -Y(w, u)
                # bu <-> (not t(u) and t(w)) or (t(u)==t(w) and y)
                cl.append([-bu, -T(u), T(w), y] if isinstance(y, int) else [-bu])
                cl.append([bu, T(u), -T(w)])
    # antisymmetry for the D in {1,-1} tie cases and D==0 pairs
    for u in range(1, N + 1):
        for w in range(u + 1, N + 1):
            cl.append([-B(u, w), -B(w, u)])
            cl.append([B(u, w), B(w, u)])
    nap = 0
    for d in range(1, N // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            u = [x + i * d for i in range(4)]
            nap += 1
            cl.append([-B(u[0], u[1]), -B(u[1], u[2]), -B(u[2], u[3])])
            cl.append([-B(u[1], u[0]), -B(u[2], u[1]), -B(u[3], u[2])])
    S = Cadical195(bootstrap_with=cl); rounds = 0
    while True:
        if not S.solve(): S.delete(); return False, None, rounds, nap
        model = set(S.get_model())
        of = lambda u, w: (B(u, w) in model)
        cy = find_cycles(lambda u, w: of(u, w), N)
        if not cy:
            import functools
            vals = sorted(range(1, N + 1), key=functools.cmp_to_key(
                lambda u, w: 0 if u == w else (-1 if of(u, w) else 1)))
            S.delete(); return True, vals, rounds, nap
        for cyc in cy:
            L = len(cyc)
            for i in range(L):
                a, b2, e = cyc[i], cyc[(i+1) % L], cyc[(i+2) % L]
                if len({a, b2, e}) == 3:
                    S.add_clause([-B(a, b2), -B(b2, e), B(a, e)])
        rounds += 1
        if rounds > max_rounds: S.delete(); return None, None, rounds, nap


if __name__ == "__main__":
    for N in (60, 100, 160, 250, 400):
        t0 = time.time(); r, perm, rd, nap = solve(N); dt = time.time() - t0
        if r is True:
            assert sorted(perm) == list(range(1, N + 1))
            bad = has_monotone_kap_pos(perm, 4)
            print(f"N={N}: SAT ({dt:.0f}s, {rd} rounds) -- 4-AP-free: {not bad}", flush=True)
            if bad: print("   !! model failed the literal recheck", flush=True)
        elif r is False:
            print(f"N={N}: UNSAT ({dt:.0f}s) -- NO binary delay and NO within-class orders work", flush=True)
            break
        else:
            print(f"N={N}: inconclusive (round cap)", flush=True); break
