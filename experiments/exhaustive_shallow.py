"""exhaustive_shallow.py — EXHAUSTIVE counts of 4-AP-free permutations of [1..N]
subject to pinning small values to small positions. Claim probed: FIN(K)-style
extinction (CORE.md Lemma 7). If for some pinning the count hits 0 at some N0, that is
a finite theorem: no avoider of [1..N] (N >= N0) with that pinning (restriction-monotone:
an avoider of [1..N+1] with the pinning restricts to one of [1..N] with the pinning,
since pinned positions can only shrink under restriction and pinned values stay).
CAREFUL: restriction can move a value EARLIER, so 'pos(v) <= C' pinnings are inherited
downward, and count(N)=0 => count(M)=0 for all M >= N. Exact DFS, values placed in
increasing order, interval pruning per CORE.md Lemma 8.

Pinning type used: pos(v) <= C for all v <= K   (K, C given).
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos

sys.setrecursionlimit(100000)


def count_avoiders_pinned(N, K, C, cap=None, collect=None):
    """Exhaustively count 4-AP-free perms of [1..N] with pos(v) <= C for v <= K.
    cap: stop early if count exceeds cap (return cap+1). Positions 1-based."""
    pos = [0] * (N + 1)     # pos[v]
    occupied = [False] * (N + 2)
    count = 0

    def rec(v):
        nonlocal count
        if v > N:
            count += 1
            if collect is not None and len(collect) < 5:
                perm = [0] * N
                for u in range(1, N + 1):
                    perm[pos[u] - 1] = u
                collect.append(list(perm))
            return
        lo, hi = 0, N + 1
        for d in range(1, (v - 1) // 3 + 1):
            p1, p2, p3 = pos[v - d], pos[v - 2 * d], pos[v - 3 * d]
            if p3 < p2 < p1:
                if p1 < hi: hi = p1
            elif p3 > p2 > p1:
                if p1 > lo: lo = p1
        if v <= K and hi > C + 1:
            hi = C + 1
        for p in range(lo + 1, hi):
            if not occupied[p]:
                occupied[p] = True
                pos[v] = p
                rec(v + 1)
                occupied[p] = False
                pos[v] = 0
                if cap is not None and count > cap:
                    return
    rec(1)
    return count


if __name__ == "__main__":
    import time
    # sanity: unpinned must reproduce the known table
    for n, expect in [(5, 102), (7, 3336), (9, 168864)]:
        got = count_avoiders_pinned(n, 0, 0)
        assert got == expect, (n, got, expect)
    print("sanity OK (unpinned counts match)")

    for (K, C) in [(2, 2), (2, 3), (3, 3), (2, 6), (3, 6)]:
        print(f"--- pinning: pos(v) <= {C} for v <= {K}")
        prev_nonzero = True
        for N in range(6, 41):
            t0 = time.time()
            c = count_avoiders_pinned(N, K, C, cap=2 * 10**6)
            dt = time.time() - t0
            tag = ">cap" if c > 2 * 10**6 else str(c)
            print(f"  N={N}: count={tag}  ({dt:.1f}s)", flush=True)
            if c == 0:
                print(f"  EXTINCT at N={N}: THEOREM — no 4-AP-free perm of [1..{N}] "
                      f"with pos(v)<={C} for v<={K}; inherited for all larger N.")
                break
            if dt > 120:
                print("  (stopping this pinning: too slow)")
                break
