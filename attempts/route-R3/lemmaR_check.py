"""lemmaR_check.py — machine validation of the Lemma R case analysis (base b >= 3).

Lemma R (necessity+sufficiency): for a contiguous base-b block ordering (b >= 3) given
by internal orders pi_j, a 4-AP (x,d) is monotone iff the following case rule holds.
Let t_k = x+kd, B_k = block(t_k), pairs P_k = (t_k, t_{k+1}), k=0,1,2.
  INC: monotone increasing  <=>  every same-block pair is pi-increasing
       (cross-block pairs are automatically increasing);
  DEC: monotone decreasing  <=>  all four terms in one block and all pairs pi-decreasing.
Pattern facts used by the block-level analysis (checked here):
  - B_1 <= B_2 <= B_3 <= B_1 + 1 (Lemma L2, b>=3): so among P_1, P_2 at least one is
    same-block; the possible block patterns are exactly those enumerated in REPORT.md.
Validation: for random internal orders pi_j of the base-3 and base-4 blocks of [1..N],
compare the witness set of the assembled permutation (find_mono4, cross-validated
earlier against apcheck) with the witness set predicted by the case rule, AP by AP.
"""

import random
import sys

sys.path.insert(0, "/home/user/erdos/attempts/route-R3")
sys.path.insert(0, "/home/user/erdos/experiments")
from orderings import find_mono4

rng = random.Random(196)


def blockb(n, b):
    m, p = 0, b
    while p <= n:
        m += 1
        p *= b
    return m


def run(b, N, trials):
    blk = {v: blockb(v, b) for v in range(1, N + 1)}
    members = {}
    for v in range(1, N + 1):
        members.setdefault(blk[v], []).append(v)
    for _ in range(trials):
        order = []
        for j in sorted(members):
            mem = members[j][:]
            rng.shuffle(mem)
            order.extend(mem)
        posmap = {v: i for i, v in enumerate(order)}
        actual = set(find_mono4(order, cap=10 ** 9))
        predicted = set()
        seen_patterns = set()
        for d in range(1, (N - 1) // 3 + 1):
            for x in range(1, N - 3 * d + 1):
                t = [x + k * d for k in range(4)]
                B = [blk[v] for v in t]
                assert B[1] <= B[2] <= B[3] <= B[1] + 1, (x, d, B)  # L2, b>=3
                assert not (B[1] < B[2] and B[2] < B[3])
                seen_patterns.add(tuple(v - B[0] for v in B))
                prs = [(t[k], t[k + 1]) for k in range(3)]
                inc = all(posmap[u] < posmap[w] if blk[u] == blk[w] else True
                          for (u, w) in prs)
                if inc:
                    predicted.add((x, d, 1))
                if B[0] == B[3] and all(posmap[u] > posmap[w] for (u, w) in prs):
                    predicted.add((x, d, -1))
        assert actual == predicted, (b, sorted(actual ^ predicted)[:5])
    print(f"base {b}, N={N}: witness sets match case rule on {trials} random "
          f"internal-order samples; block patterns seen: {sorted(seen_patterns)}")


run(3, 242, 30)
run(4, 255, 30)
run(5, 124, 30)
