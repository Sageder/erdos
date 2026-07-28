"""anchor_chain.py — R17.  The MIDPOINT-ANCHOR chain: explicit forcing chains with no
omega-argument at all.

THEOREM (R17.6').  Let a be monotone-4-AP-free, m a value, d >= 1, and suppose
        m - 2^j d  prec  m  prec  m + 2^j d          for j = 0, 1, ..., K
(each m - 2^j d >= 1).  Then for every j <= K the triple (m-2^j d, m, m+2^j d) is a
positionally increasing 3-AP with step 2^j d, so m + 2^j d is OPEN at scale 2^j d and
Theorem 16(a) forces  m + 2^{j+1} d  prec  m + 2^j d.  Hence
        m+d  succ  m+2d  succ  m+4d  succ ... succ  m+2^{K+1} d
is a forcing chain of length K+1, so  |Cl(m+d)| >= K+2  and  pos(m+d) >= K+2.

Write C(m) = { e >= 1 : m-e prec m prec m+e } (e <= m-1).  The chain length available
from anchor m is exactly the longest doubling run d, 2d, 4d, ... inside C(m), which is
<= log2(m).  ONE ANCHOR BUYS AT MOST log2(m) STEPS -- the quantitative form of R5's
one-point-anchored barrier.
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R17-cosupply')
from apcheck import has_monotone_kap_pos
from forcing2 import make_pos, closure, longest_chain, grounded, records, ALLRULES


def Cset(pos, m, N):
    return set(e for e in range(1, m) if pos[m - e] < pos[m] < pos[m + e]) if m + 1 <= N \
        else set(e for e in range(1, m) if pos[m - e] < pos[m] and m + e <= N and pos[m] < pos[m + e])


def best_run(pos, m, N):
    """longest K with d,2d,...,2^K d all in C(m) and m+2^{K+1}d <= N; returns (K, d)."""
    C = set(e for e in range(1, m) if m + e <= N and pos[m - e] < pos[m] < pos[m + e])
    best = (-1, None)
    for d in range(1, m):
        if d not in C:
            continue
        k = 0
        while (2 ** (k + 1)) * d in C:
            k += 1
        if k > best[0]:
            best = (k, d)
    return best


def verify(perm):
    """Check that every anchored doubling run really produces a descending chain."""
    N = len(perm)
    pos = make_pos(perm)
    checked = 0
    for m in range(2, N):
        K, d = best_run(pos, m, N)
        if d is None:
            continue
        chain = [m + (2 ** j) * d for j in range(0, K + 2) if m + (2 ** j) * d <= N]
        for i in range(len(chain) - 1):
            assert pos[chain[i + 1]] < pos[chain[i]], ("CHAIN VIOLATION", perm, m, d, chain)
        # and the closure bound
        assert len(chain) <= pos[chain[0]], ("SIZE VIOLATION", perm, m, d, chain, pos[chain[0]])
        checked += 1
    return checked


if __name__ == "__main__":
    from itertools import permutations
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "exh"):
        for N in range(4, 10):
            cnt = ch = 0
            for p in permutations(range(1, N + 1)):
                if has_monotone_kap_pos(p, 4):
                    continue
                cnt += 1
                ch += verify(list(p))
            print(f"N={N}: {cnt} avoiders, {ch} anchored runs, ALL chains verified descending",
                  flush=True)
    if mode in ("all", "sat"):
        from sat_order import solve
        print("\nAnchored-chain statistics on SAT-found avoiders "
              "(K = longest doubling run in C(m); chain length K+1):")
        for N in (40, 60, 80, 100, 130, 160, 200, 260):
            sat, perm = solve(N, inc4=True, dec4=True)
            assert sat and not has_monotone_kap_pos(perm, 4)
            pos = make_pos(perm)
            best = (-1, None, None)
            for m in range(2, N):
                K, d = best_run(pos, m, N)
                if K > best[0]:
                    best = (K, m, d)
            K, m, d = best
            gr = grounded(pos, N)
            # grounded anchors only
            bg = max(((best_run(pos, g, N)[0], g) for g in gr if g >= 2), default=(-1, None))
            trueG = max(longest_chain(pos, u, N, ('U1',)) for u in range(1, N + 1))
            trueGs = max(longest_chain(pos, u, N, ALLRULES) for u in range(1, N + 1))
            print(f"  N={N}: best anchored run K={K} (anchor m={m}, d={d}) -> chain length {K+1}"
                  f" [log2(N)={N.bit_length()-1}];  best grounded anchor K={bg[0]} (g={bg[1]});"
                  f"  true longest chain: G={trueG}, G*={trueGs}", flush=True)
