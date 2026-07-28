"""chains_tau.py — exact longest forcing chain / closure size in tau, by DP.

The tau forcing graph on [1..M]:  u -> u+d  whenever u is tau-open at scale d
(Lemma O), which requires 2d < u, hence u < u+d < 1.5u.  Values strictly increase,
so the graph is a DAG; longest paths are a backward DP.

Theorem 16(b) for a 4-AP-free PERMUTATION says |Cl(u)| <= pos(u) < infinity.
tau is 4-AP-free but NOT a permutation, so nothing a priori forces its closures to be
finite: this script measures whether they are, and how fast the longest chain grows.
Chain lengths computed inside a window [1..M] are LOWER bounds for the true values
(a chain could leave the window); we therefore also report, for start values u <= M/2,
whether the optimal chain stays well inside.
"""

import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from taulib import Tau, prio_const, v3, dig3


def open_scales_natural(u, M):
    """Open scales d of u under tau with natural priorities (0,1,2) at every level,
    restricted to u+d <= M.  Lemma O: v=v3(d), (d/3^v)%3==1, dig3(u,v)==2, 2d<u."""
    out = []
    dmax = min((u - 1) // 2, M - u)
    v = 0
    p = 1
    while p <= dmax:
        if dig3(u, v) == 2:
            e = 1
            while e * p <= dmax:
                out.append(e * p)
                e += 3
        v += 1
        p *= 3
    return out


def chain_dp(M):
    chain = [1] * (M + 2)
    arg = [0] * (M + 2)
    for u in range(M, 0, -1):
        best, ba = 1, 0
        for d in open_scales_natural(u, M):
            if chain[u + d] + 1 > best:
                best, ba = chain[u + d] + 1, d
        chain[u] = best
        arg[u] = ba
    return chain, arg


def path(chain, arg, u):
    p = [u]
    while arg[u]:
        u += arg[u]
        p.append(u)
    return p


def closure_sizes(M):
    """Exact |Cl(u) ∩ [1..M]| by backward DP with bitsets (python ints)."""
    clos = [0] * (M + 2)
    sizes = [0] * (M + 2)
    for u in range(M, 0, -1):
        b = 1 << u
        for d in open_scales_natural(u, M):
            b |= clos[u + d]
        clos[u] = b
        sizes[u] = bin(b).count("1")
    return sizes


if __name__ == "__main__":
    import time
    print("=== longest tau forcing chain inside [1..M] (natural priorities) ===")
    for M in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        t0 = time.time()
        chain, arg = chain_dp(M)
        b = max(range(1, M + 1), key=lambda u: chain[u])
        # best chain that starts small (u <= M/100) -> not a window artefact
        lim = max(4, M // 100)
        b2 = max(range(1, lim + 1), key=lambda u: chain[u])
        print(f"M={M:8d}  max chain = {chain[b]:3d} (start u={b}, path {path(chain,arg,b)[:8]}...)"
              f"   best start<=M/100: {chain[b2]} at u={b2}"
              f"   [{time.time()-t0:.1f}s]")
    print()
    print("=== exact closure sizes |Cl(u)| inside [1..M] ===")
    for M in (10 ** 3, 10 ** 4, 10 ** 5):
        t0 = time.time()
        s = closure_sizes(M)
        b = max(range(1, M + 1), key=lambda u: s[u])
        lim = max(4, M // 100)
        b2 = max(range(1, lim + 1), key=lambda u: s[u])
        print(f"M={M:8d}  max |Cl| = {s[b]:6d} (u={b})   best start<=M/100: {s[b2]} at u={b2}"
              f"   [{time.time()-t0:.1f}s]")
