"""measure.py — mission item 3 + auxiliary structure measurements.

(M1) COMPATIBLE-TOWER TEST.  Take one large 4-AP-free board sigma_N; its restrictions
     sigma_M (M <= N) form a genuinely compatible tower (CORE.md Lemma 6 (=>)).  Openness
     of u depends only on values <= u, so it is restriction-invariant; forcing edges are
     the same edges with head <= M.  Hence Cl_{sigma_M}(u) is nondecreasing in M and
     stabilises at Cl_{sigma_N}(u).  We watch h and |Cl| for fixed small u as M grows,
     and max_{u<=K} h(u) as a function of M.

(M2) SCALE STRUCTURE OF FORCING CHAINS.  Exhaustive check on all 4-AP-free boards N<=9
     of the (proved) fact that two CONSECUTIVE edges of a forcing chain cannot use the
     same scale:  u --d--> u+d --d--> u+2d is impossible, because u+d open at scale d
     means pos(u) < pos(u+d) while the first edge forces pos(u+d) < pos(u).

(M3) Forcing statistics of the layered (block) witnesses produced by route R18, checking
     Proposition R18.2: in a layered permutation every forcing edge stays inside a block.
"""

import sys, json, glob
from itertools import permutations
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from apcheck import has_monotone_kap_pos                  # noqa: E402
from forcing_tools import (positions, open_scales, closures_and_heights,  # noqa: E402
                           board_stats, forcing_digraph)
from sat_order import solve as sat_solve                  # noqa: E402


def restrict(perm, M):
    return [v for v in perm if v <= M]


def M1(N=160):
    print(f"=== (M1) restriction tower of one 4-AP-free board, N={N} ===")
    sat, perm = sat_solve(N, inc4=True, dec4=True)
    assert sat and not has_monotone_kap_pos(perm, 4)
    print("   M   |O|/M  maxh  max|Cl|   h(10) |Cl(10)|  h(25) |Cl(25)|  max_{u<=20} h")
    for M in (20, 30, 40, 60, 80, 100, 130, N):
        r = restrict(perm, M)
        cl, ht, op, od, reach = closures_and_heights(r)
        st = board_stats(r)
        print(f"{M:5d} {st['frac_open']:6.2f} {st['max_height']:5d} {st['max_closure']:7d} "
              f"{ht[10]:7d} {cl[10]:8d} {ht[25] if M>=25 else -1:7d} "
              f"{cl[25] if M>=25 else -1:8d} {max(ht[u] for u in range(1,21)):8d}", flush=True)
    return perm


def M2():
    print("\n=== (M2) no two consecutive forcing edges share a scale (exhaustive N<=9) ===")
    tot = bad = 0
    for N in range(4, 10):
        for p in permutations(range(1, N + 1)):
            if has_monotone_kap_pos(p, 4):
                continue
            tot += 1
            pos = positions(list(p))
            for u in range(1, N + 1):
                for d in open_scales(pos, u):
                    w = u + d
                    if w <= N and d in open_scales(pos, w):
                        bad += 1
    print(f"   {tot} 4-AP-free boards, repeated-scale chain steps found: {bad} (expected 0)")


def M3():
    print("\n=== (M3) layered witnesses: every forcing edge stays inside its block ===")
    for fn in sorted(glob.glob('/home/user/erdos/attempts/route-R18-bounded-closure/witness_*.json')):
        d = json.load(open(fn))
        if isinstance(d, dict):
            perm, cuts = d['perm'], d['cuts']
        else:
            continue
        N = len(perm)
        def blk(v):
            j = 0
            for i, c in enumerate(cuts):
                if v >= c:
                    j = i
            return j
        edges, succ = forcing_digraph(perm)
        cross = [(u, dd, w) for (u, dd, w) in edges if blk(u) != blk(w)]
        st = board_stats(perm)
        print(f"   {fn.split('/')[-1]}: N={N} cuts={[c for c in cuts if c<=N]} "
              f"edges={len(edges)} cross-block={len(cross)} maxh={st['max_height']} "
              f"max|Cl|={st['max_closure']} (max block size="
              f"{max(len([v for v in perm if blk(v)==j]) for j in range(len(cuts)))})")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "M1"):
        M1(int(sys.argv[2]) if len(sys.argv) > 2 else 160)
    if which in ("all", "M2"):
        M2()
    if which in ("all", "M3"):
        M3()
