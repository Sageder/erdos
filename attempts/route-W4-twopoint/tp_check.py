"""tp_check.py -- machine verification of Lemma TP (position-anchored bounded supply)
and its two-point specialisation TP-gen.

Lemma TP.  a a bijection N->N, i<j, u=a(i), v=a(j), v>u, v>max(a(1..i-1)), e0=v-u.
Then some k with 0<=k<=j-i-1 has pos(u) < pos(u+2^k e0) < pos(u+2^{k+1} e0).

TP-gen.  Same hypotheses: EITHER pos(2v-u) lies strictly between i and j
         (i.e. 2v-u is one of a(i+1..j-1)),  OR (u, v, 2v-u) is an increasing 3-AP.

Both are statements about ARBITRARY permutations -- 4-AP-freeness is not used -- so
they are tested on all permutations of [1..N] (finite shadow: only instances all of
whose values stay in [1..N] are tested).
"""
import sys
from itertools import permutations
sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R5")
from apcheck import has_monotone_kap_pos
import enum_avoiders


def test(perm, N, stats):
    n = len(perm)
    pos = [0] * (N + 1)
    for idx, val in enumerate(perm):
        pos[val] = idx + 1
    pref = [0] * (n + 2)
    for idx in range(1, n + 1):
        pref[idx] = max(pref[idx - 1], perm[idx - 1])
    for i in range(1, n + 1):
        u = perm[i - 1]
        for j in range(i + 1, n + 1):
            v = perm[j - 1]
            if v <= u or v <= pref[i - 1]:
                continue
            e0 = v - u
            K = j - i - 1
            # TP: need all values u + 2^k e0 for k=0..K+1 to be inside [1..N]
            vals = [u + (1 << k) * e0 for k in range(K + 2)]
            if vals[-1] <= N:
                stats['TP_fire'] += 1
                good = any(pos[u] < pos[vals[k]] < pos[vals[k + 1]] for k in range(K + 1))
                if not good:
                    stats['TP_viol'] += 1
                    stats['TPwit'].append((tuple(perm), i, j))
            # TP-gen: needs only 2v-u <= N
            if 2 * v - u <= N:
                stats['TPg_fire'] += 1
                p3 = pos[2 * v - u]
                ok = (i < p3 < j) or (pos[u] < pos[v] < p3)
                if not ok:
                    stats['TPg_viol'] += 1
                    stats['TPgwit'].append((tuple(perm), i, j))


if __name__ == '__main__':
    for N in (5, 6, 7, 8):
        st = dict(TP_fire=0, TP_viol=0, TPg_fire=0, TPg_viol=0, TPwit=[], TPgwit=[])
        for p in permutations(range(1, N + 1)):
            test(list(p), N, st)
        print(f"ALL {N}! permutations of [1..{N}]:  TP fires {st['TP_fire']} viol {st['TP_viol']}"
              f" | TP-gen fires {st['TPg_fire']} viol {st['TPg_viol']}")
        if st['TPwit']:
            print("   TP counterexample:", st['TPwit'][0])
        if st['TPgwit']:
            print("   TP-gen counterexample:", st['TPgwit'][0])
    for N in (10,):
        st = dict(TP_fire=0, TP_viol=0, TPg_fire=0, TPg_viol=0, TPwit=[], TPgwit=[])
        boards = []
        enum_avoiders.gen_avoiders(N, boards.append)
        for p in boards:
            assert not has_monotone_kap_pos(p, 4)
            test(list(p), N, st)
        print(f"all {len(boards)} 4-AP-free permutations of [1..{N}]: TP fires {st['TP_fire']}"
              f" viol {st['TP_viol']} | TP-gen fires {st['TPg_fire']} viol {st['TPg_viol']}")
