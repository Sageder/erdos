"""pairmap.py -- feasibility of a CUT PAIR {W,U} under the horizon system N(W,U,M).

N(W,U,M) UNSAT for some M  ==>  no monotone-4-AP-free permutation of N has both W
and U as cuts.  Because N is monotone in M, one UNSAT settles all larger horizons.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys

CAP = 400


def pair_status(W, U, horizons=None, cap=CAP, verbose=False):
    """returns ('DEAD', M) if some tested horizon is UNSAT, else ('ALIVE<=Mmax', Mmax)."""
    if horizons is None:
        horizons = sorted(set([3 * U - 2, 3 * U + 4, 4 * U, 5 * U]))
    best = None
    for M in horizons:
        if M <= U:
            continue
        S = wsys.Sys((W, U), M)
        t0 = time.time()
        v, o = wsys.solve_lazy(S, time_cap=cap, tag=f"{W},{U},{M}")
        if v == 'GEOM_DEAD':
            v = 'UNSAT'
        if verbose:
            print(f"     N({W},{U},{M}) {v} [{time.time()-t0:.0f}s]", flush=True)
        if v == 'UNSAT':
            return 'DEAD', M
        if v == 'TIME_CAP':
            return 'TIMEOUT', M
        best = M
    return 'ALIVE', best


if __name__ == '__main__':
    job = sys.argv[1]
    if job == 'chain':
        # every pair inside the mission's depth-5 accelerating chains
        for chain in ([1, 2, 4, 10, 90], [1, 2, 4, 10, 28], [1, 5, 6, 16, 46],
                      [1, 7, 8, 22, 64]):
            print(f"## chain {chain}", flush=True)
            for i in range(len(chain)):
                for j in range(i + 1, len(chain)):
                    W, U = chain[i], chain[j]
                    st, M = pair_status(W, U)
                    print(f"   pair {{{W},{U}}}: {st} (M={M})", flush=True)
    elif job == 'grid':
        lo, hi = int(sys.argv[2]), int(sys.argv[3])
        for W in range(lo, hi + 1):
            row = []
            for U in range(W + 1, min(4 * W + 8, 60) + 1):
                st, M = pair_status(W, U)
                row.append('D' if st == 'DEAD' else ('.' if st == 'ALIVE' else '?'))
            print(f"W={W:3d} U={W+1}..: {''.join(row)}", flush=True)
