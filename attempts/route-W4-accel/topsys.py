"""topsys.py -- TOP relaxation of the pair system N(W,U,M): keep only order
variables inside the top block C = (U,M].  Every dropped clause only weakens the
system, so UNSAT of TOP is UNSAT of N, hence a theorem:
   TOP(W,U,M) UNSAT  ==>  no monotone-4-AP-free permutation of N has both W and U
   as cuts.

TOP(W,U,M) explicitly.  Order < on C = {U+1,...,M} with
 (a) no monotone 4-AP inside C, either orientation;
 (b) for p,f>=1 with p,p+2f in C and 1 <= p-f <= U:  NOT p < p+f < p+2f;
 (c) for a<b in C with 1 <= 3a-2b <= W and W < 2a-b <= U:  b < a   (unit clauses).
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def top(W, U, M, cap=600, solver='cadical195'):
    S = wsys.Sys((W, U), M, window=(U + 1, M))
    v, o = wsys.solve_lazy(S, time_cap=cap, solver=solver, tag=f"TOP{W},{U},{M}")
    if v == 'GEOM_DEAD':
        v = 'UNSAT'
    return v


def forced_pairs(W, U, M):
    return [(a, b) for a in range(U + 1, M + 1) for b in range(a + 1, M + 1)
            if 1 <= 3 * a - 2 * b <= W and W < 2 * a - b <= U]


def death_horizon(W, U, Mmax_mult=8, cap=600, step=None):
    """least tested M with TOP(W,U,M) UNSAT; coarse grid then bisection."""
    grid = []
    m = 3 * U - 2
    while m <= Mmax_mult * U:
        grid.append(m)
        m = int(m * 1.25) + 1
    hit = None
    for M in grid:
        r = top(W, U, M, cap=cap)
        if r == 'UNSAT':
            hit = M
            break
        if r == 'TIME_CAP':
            return ('TIMEOUT', M)
    if hit is None:
        return ('ALIVE', grid[-1])
    lo = 3 * U - 3
    for M in grid:
        if M < hit:
            lo = M
    while hit - lo > 1:
        mid = (hit + lo) // 2
        r = top(W, U, mid, cap=cap)
        if r == 'UNSAT':
            hit = mid
        elif r == 'TIME_CAP':
            break
        else:
            lo = mid
    return ('DEAD', hit)


if __name__ == '__main__':
    job = sys.argv[1]
    if job == 'check':
        for (W, U, M) in [(10, 28, 82), (10, 28, 81), (8, 28, 82), (10, 31, 155),
                          (10, 34, 170)]:
            t0 = time.time()
            print(f"  TOP({W},{U},{M}) = {top(W,U,M)}  "
                  f"|F|={len(forced_pairs(W,U,M))} [{time.time()-t0:.0f}s]",
                  flush=True)
    elif job == 'pairs':
        # remaining argv: W:U pairs
        for spec in sys.argv[2:]:
            W, U = map(int, spec.split(':'))
            t0 = time.time()
            st, M = death_horizon(W, U)
            print(f"  pair ({W},{U}): {st} M0={M} ratio={M/U:.2f} "
                  f"|F|={len(forced_pairs(W,U,3*U-2))} [{time.time()-t0:.0f}s]",
                  flush=True)
    elif job == 'row':
        W = int(sys.argv[2])
        Ulo, Uhi = int(sys.argv[3]), int(sys.argv[4])
        for U in range(Ulo, Uhi + 1):
            t0 = time.time()
            st, M = death_horizon(W, U)
            print(f"  pair ({W},{U}): {st} M0={M} ratio={M/U:.2f} "
                  f"[{time.time()-t0:.0f}s]", flush=True)
    elif job == 'sweep':
        Wlo, Whi = int(sys.argv[2]), int(sys.argv[3])
        Umax = int(sys.argv[4])
        for W in range(Wlo, Whi + 1):
            for U in range(W + 1, Umax + 1):
                t0 = time.time()
                st, M = death_horizon(W, U)
                print(f"  pair ({W},{U}): {st} M0={M} ratio={M/U:.2f} "
                      f"[{time.time()-t0:.0f}s]", flush=True)
