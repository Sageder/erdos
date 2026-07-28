"""gaplaws.py — the ANCHOR-GAP laws, and how far apart the two anchors can be.

Lemma R13-G (grounded gap law; dual of CORE Lemma 43).  For ANY permutation a of N with
grounded values g_1 < g_2 < ... (g grounded iff pos(g) > pos(v) for all v < g):

        g_{i+1}  <=  pos(g_i) + 1.

Proof.  The running maximum Mx(v) = max_{u<=v} pos(u) is constant = pos(g_i) on
[g_i, g_{i+1}), so every v < g_{i+1} other than g_i has pos(v) < pos(g_i).  There are
g_{i+1}-2 such values, all at distinct positions < pos(g_i); hence pos(g_i)-1 >= g_{i+1}-2.

Corollary.  For every value w the least grounded value g > w satisfies
        g <= Psi(w) + 1,      Psi(w) := max_{v<=w} pos(v).
So the RATIO of the two anchors of a record-grounded two-point law is bounded by the local
displacement ratio Psi(w)/w -- this is the only mechanism found in route R13 that takes the
choice of the second anchor away from the adversary.

Part 1 verifies both gap laws literally on ALL permutations of [1..n], n <= 8 (they are
facts about permutations, not about avoiders).
Part 2 measures the actual anchor gaps on SAT-produced 4-AP-free avoiders.
"""

import sys
from itertools import permutations

sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R13-twopoint")
from apcheck import has_monotone_kap_pos          # noqa: E402
from r13enum import posarray, records, grounded   # noqa: E402


def part1(nmax=8):
    tot = 0
    for n in range(2, nmax + 1):
        for p in permutations(range(1, n + 1)):
            pos = posarray(p)
            R = records(pos, n)
            G = grounded(pos, n)
            for a, b in zip(R, R[1:]):                    # CORE Lemma 43
                assert pos[b] <= a + 1, ("L43", p, a, b)
                tot += 1
            for a, b in zip(G, G[1:]):                    # Lemma R13-G
                assert b <= pos[a] + 1, ("R13-G", p, a, b)
                tot += 1
            # corollary: least grounded > w is <= Psi(w)+1
            psi = 0
            gi = 0
            for w in range(1, n + 1):
                psi = max(psi, pos[w])
                nxt = [g for g in G if g > w]
                if nxt:
                    assert nxt[0] <= psi + 1, ("cor", p, w, nxt[0], psi)
                    tot += 1
            _ = gi
    print(f"part 1: gap laws verified on ALL permutations of [1..n], n<={nmax}; "
          f"{tot} instances, 0 violations")


def part2():
    from sat_order import build, decode
    from pysat.solvers import Cadical195
    for N in (60, 100, 160, 220):
        cl, pool, var = build(N, inc4=True, dec4=True)
        S = Cadical195(bootstrap_with=cl)
        assert S.solve()
        perm = decode(S.get_model(), N, var)
        S.delete()
        assert not has_monotone_kap_pos(perm, 4)
        pos = posarray(perm)
        R = records(pos, N)
        G = grounded(pos, N)
        # ratio of the two anchors in the record-grounded laws, for records w <= N/2
        ratios = []
        for w in R:
            if 2 * w > N:
                break
            nxt = [g for g in G if g > w]
            if nxt:
                ratios.append(round(nxt[0] / w, 2))
        print(f"N={N:4d} |Lambda|={len(R):3d} |Gamma|={len(G):3d} "
              f"record-gap-ratios={[round(b / a, 2) for a, b in zip(R, R[1:])][:8]} "
              f"grounded-gap-ratios={[round(b / a, 2) for a, b in zip(G, G[1:])][:8]} "
              f"anchor-ratios(g/w)={ratios[:8]}", flush=True)


if __name__ == "__main__":
    part1(8)
    part2()
