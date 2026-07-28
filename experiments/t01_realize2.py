"""t01_realize2.py — clean reformulation of the T=1 realizability question.

A class architecture c = j + t with classes emitted in increasing index order produces
exactly the permutations whose position order is a linear extension of c. So:

  there is a binary delay t and within-class orders giving a monotone-4-AP-free
  permutation of [1..N]
        <=>
  there is a monotone-4-AP-free permutation of [1..N] and a binary t with
  c = j + t NON-DECREASING along the position order.

Encoding: order variables x_{uw} (u<w, "u before w") with lazy transitivity (CEGAR), the
AP clauses, plus for every ordered pair the implication
        u before w  =>  j(u) + t(u) <= j(w) + t(w),
which with D = j(w) - j(u) reads:
        D >= 1  : no constraint
        D == 0  : NOT( t(u) and not t(w) )
        D == -1 : ( not t(u) ) and t(w)
        D <= -2 : u cannot precede w at all.
UNSAT at some N is an impossibility theorem for the whole T=1 family at that size,
quantified over all delays and all within-class orders.
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
    X = lambda u, w: pool.id(('x', u, w))
    T = lambda v: pool.id(('t', v))
    lit = lambda u, w: X(u, w) if u < w else -X(w, u)      # "u before w"
    j = [0] + [blk(v, b) for v in range(1, N + 1)]
    cl = []
    for u in range(1, N + 1):
        for w in range(1, N + 1):
            if u == w: continue
            D = j[w] - j[u]
            if D >= 1: continue
            L = lit(u, w)
            if D == 0:      cl.append([-L, -T(u), T(w)])
            elif D == -1:   cl.append([-L, -T(u)]); cl.append([-L, T(w)])
            else:           cl.append([-L])
    nap = 0
    for d in range(1, N // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            u = [x + i * d for i in range(4)]; nap += 1
            cl.append([-lit(u[0], u[1]), -lit(u[1], u[2]), -lit(u[2], u[3])])
            cl.append([lit(u[0], u[1]), lit(u[1], u[2]), lit(u[2], u[3])])
    S = Cadical195(bootstrap_with=cl); rounds = 0
    while True:
        if not S.solve(): S.delete(); return False, None, rounds, nap
        model = set(S.get_model())
        of = lambda u, w: (X(u, w) in model)
        cy = find_cycles(of, N)
        if not cy:
            import functools
            vals = sorted(range(1, N + 1), key=functools.cmp_to_key(
                lambda u, w: 0 if u == w else (-1 if (of(u, w) if u < w else not of(w, u)) else 1)))
            tv = [0] + [1 if T(v) in model else 0 for v in range(1, N + 1)]
            S.delete(); return True, (vals, tv), rounds, nap
        for cyc in cy:
            Lc = len(cyc)
            for i in range(Lc):
                a, b2, e = cyc[i], cyc[(i+1) % Lc], cyc[(i+2) % Lc]
                if len({a, b2, e}) == 3:
                    S.add_clause([-lit(a, b2), -lit(b2, e), lit(a, e)])
        rounds += 1
        if rounds > max_rounds: S.delete(); return None, None, rounds, nap


if __name__ == "__main__":
    for N in (60, 100, 160, 250, 400, 600):
        t0 = time.time(); r, out, rd, nap = solve(N); dt = time.time() - t0
        if r is True:
            perm, tv = out
            assert sorted(perm) == list(range(1, N + 1))
            bad = has_monotone_kap_pos(perm, 4)
            pos = {v: i for i, v in enumerate(perm)}
            c = [0] + [blk(v, 3) + tv[v] for v in range(1, N + 1)]
            mono = all(c[perm[i]] <= c[perm[i + 1]] for i in range(N - 1))
            print(f"N={N}: SAT ({dt:.0f}s, {rd} rounds) 4-AP-free={not bad} "
                  f"class-monotone-along-order={mono} |t=1|={sum(tv[1:])}", flush=True)
        elif r is False:
            print(f"N={N}: UNSAT ({dt:.0f}s) -- NO binary delay + within-class orders work", flush=True)
            g = Glucose42; print("   (second-solver check omitted: CEGAR clauses are incremental)", flush=True)
            break
        else:
            print(f"N={N}: inconclusive (round cap {rd})", flush=True); break
