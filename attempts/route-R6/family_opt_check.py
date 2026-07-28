"""family_opt_check.py — machine checks for Prop 7.5 (block-family rigidity).

Reversed-interval-block permutations: block starts 2 <= b1 < b2 < ..., block
[b_k, b_{k+1}) listed decreasingly, blocks in increasing order (b_0 = 1).
Fact (proved in PROOFS.md 7.5): such a permutation has an increasing monotone
4-AP iff some (x,d) has a block start in each gap (x,x+d], (x+d,x+2d], (x+2d,x+3d]
("bad window").

Checks here:
  (F1) Feasibility lemma, exhaustive: for 2 <= alpha <= (beta-1)/2, beta <= 60,
       beta < gamma <= 3*beta + 4:
       [ exists x,d with x < alpha <= x+d < beta <= x+2d < gamma <= x+3d ]
       <=>  [ gamma <= 3*beta - 5  and not (alpha == 2, beta even, gamma == beta+1) ].
  (F2) End-to-end: dyadic starts {2^k} yield an increasing 4-AP (bad); triadic
       starts {3^k} do not (good); triadic with one extra start inserted at
       2*3^k becomes bad; the chain b_{k+1} = 3 b_k - 5 (just inside the
       forbidden zone) is bad; b_{k+1} = 3 b_k - 4 chain: probe and report.
  (F3) No three consecutive integers are all block starts in any good sequence
       (else (x,d=1) bad window); verified as a special case of F1 logic.
"""

import sys

import numpy as np

sys.path.insert(0, "/home/user/erdos/attempts/route-R6")


def bad_window_triple(alpha, beta, gamma):
    for x in range(1, alpha):
        # need x+d >= alpha, x+d <= beta-1
        for d in range(max(1, alpha - x), beta - x):
            if x + 2 * d >= beta and x + 2 * d < gamma and x + 3 * d >= gamma:
                return (x, d)
    return None


def blocks_perm(starts, N):
    """Reversed-block permutation of [1..N]; starts = sorted block starts >= 2,
    all < N; final block truncated at N (kept complete by construction below)."""
    bs = [1] + [s for s in starts if s <= N] + [N + 1]
    seq = []
    for i in range(len(bs) - 1):
        seq.extend(range(bs[i + 1] - 1, bs[i] - 1, -1))
    return seq


def first_inc_4ap(perm):
    n = len(perm)
    pos = np.empty(n + 1, dtype=np.int64)
    pos[np.array(perm)] = np.arange(n)
    for d in range(1, (n - 1) // 3 + 1):
        top = n - 3 * d
        if top < 1:
            break
        p1, p2 = pos[1:top + 1], pos[1 + d:top + d + 1]
        p3, p4 = pos[1 + 2 * d:top + 2 * d + 1], pos[1 + 3 * d:top + 3 * d + 1]
        hit = (p1 < p2) & (p2 < p3) & (p3 < p4)
        if hit.any():
            return (int(np.argmax(hit)) + 1, d)
    return None


# ---- F1
bad_count = ok = 0
for beta in range(5, 61):
    for alpha in range(2, (beta - 1) // 2 + 1):
        for gamma in range(beta + 1, 3 * beta + 5):
            got = bad_window_triple(alpha, beta, gamma) is not None
            pred = (gamma <= 3 * beta - 5) and not (
                alpha == 2 and beta % 2 == 0 and gamma == beta + 1
            )
            assert got == pred, (alpha, beta, gamma, got, pred)
            ok += 1
print(f"F1 OK: feasibility predicate exact on {ok} triples (beta <= 60)")

# ---- F2
N = 2**13 - 1
dy = blocks_perm([2**k for k in range(1, 13)], N)
assert sorted(dy) == list(range(1, N + 1))
w = first_inc_4ap(dy)
assert w is not None
print(f"F2 dyadic: increasing 4-AP exists, e.g. (x,d)={w}  [expected: bad]")

N = 3**8 - 1
tri_starts = [3**k for k in range(1, 8)]
tri = blocks_perm(tri_starts, N)
assert first_inc_4ap(tri) is None
print("F2 triadic: no increasing 4-AP  [expected: good]")

spoiled = sorted(tri_starts + [2 * 3**4])
sp = blocks_perm(spoiled, N)
w = first_inc_4ap(sp)
assert w is not None
print(f"F2 triadic + extra start at 2*3^4={2*3**4}: increasing 4-AP (x,d)={w}  [expected: bad]")

# chain just inside the forbidden zone: b_{k+1} = 3 b_k - 5
starts, b = [], 7
while b < 40000:
    starts.append(b)
    b = 3 * b - 5
chain = blocks_perm(starts, 40000)
w = first_inc_4ap(chain)
assert w is not None
print(f"F2 chain b->3b-5 from 7: increasing 4-AP (x,d)={w}  [expected: bad, since 3b-5 in (b+1, 3b-5]]")

# chain at the edge of the allowed zone: b_{k+1} = 3 b_k - 4
starts, b = [], 7
while b < 40000:
    starts.append(b)
    b = 3 * b - 4
chain = blocks_perm(starts, 40000)
w = first_inc_4ap(chain)
print(f"F2 chain b->3b-4 from 7: first increasing 4-AP = {w}  [probe: Prop 7.5 allows either]")

# ---- F3
# three consecutive starts m, m+1, m+2 give bad window (x=m-1, d=1)
for m in (5, 12, 33):
    assert bad_window_triple(m, m + 1, m + 2) is not None or m - 1 < 1
print("F3 OK: three consecutive block starts always produce a bad window (d=1)")

print("FAMILY CHECKS COMPLETE")
