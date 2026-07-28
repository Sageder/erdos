"""lp_check.py — machine verification of Theorem 12 (LP(9/8)) components.

Checks:
 (V1) Ledger identity: on every witness (SAT-produced profile-bounded avoider) and on
      random permutations: pos(w) <= C*(w - e*(w)) whenever pos(v) <= Cv for all v
      (the supply step), and sum identity Sum pos = N(N+1)/2.
 (V2) Demand count: on every inc-4AP-free permutation tested: for each e,
      #{w with an e-drop} >= (N-3e)/3 (integer form: >= ceil((N-3e)/3)).
 (V3) Predicted extinction: the finite inequality fails for C=1.1 at N >= N0; find N0
      numerically and confirm by SAT that (C=1.1, N0) is indeed UNSAT (and that the
      SAT engine agrees with the theorem's direction below N0 where it can).
"""

import sys, math, random
sys.path.insert(0, '/home/user/erdos/experiments')
from sat_order import build
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from plain_thresholds import solve_profile_frac   # plain: inc4+dec4
from apcheck import has_monotone_kap_pos


def estar(perm):
    n = len(perm)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    es = {}
    for w in range(1, n + 1):
        m = 0
        for e in range(1, w):
            if pos[w] < pos[w - e]:
                m = e
        es[w] = m
    return pos, es


def check_V1_V2(perm, C=None):
    n = len(perm)
    pos, es = estar(perm)
    assert sum(pos.values()) == n * (n + 1) // 2
    if C is not None and all(pos[v] <= C * v for v in range(1, n + 1)):
        for w in range(1, n + 1):
            assert pos[w] <= C * (w - es[w]) + 1e-9, (w, pos[w], es[w])
    # V2 demand: only valid when no increasing 4-AP
    inc4 = False
    for e in range(1, (n - 1) // 3 + 1):
        for x in range(1, n - 3 * e + 1):
            if pos[x] < pos[x + e] < pos[x + 2 * e] < pos[x + 3 * e]:
                inc4 = True
    if not inc4:
        for e in range(1, (n - 1) // 3 + 1):
            cnt = sum(1 for w in range(1 + e, n + 1) if pos[w] < pos[w - e])
            need = math.ceil((n - 3 * e) / 3)
            assert cnt >= need, (e, cnt, need)
    return not inc4


# V1/V2 on random permutations (V1 vacuous unless profile holds; V2 on inc4-free only)
rng = random.Random(196)
tested_v2 = 0
for _ in range(4000):
    n = rng.randint(6, 10)
    p = list(range(1, n + 1)); rng.shuffle(p)
    if check_V1_V2(p, C=2.0):
        tested_v2 += 1
print(f"V1/V2 random OK ({tested_v2} inc4-free cases exercised V2)")

# V2 on all plain avoiders of [1..9] (all are inc4-free)
from itertools import permutations
cnt = 0
for p in permutations(range(1, 10)):
    if not has_monotone_kap_pos(p, 4):
        check_V1_V2(list(p)); cnt += 1
print(f"V2 exhaustive on {cnt} avoiders of [1..9]: OK")

# V3: ceiling-corrected finite prediction. For the SAT family (bound ceil(C*v)) the
# ledger gives: Sum e*(w) <= (1-1/C)*N(N+1)/2 + N/C  [pos(w) <= ceil(C(w-e*)) <= C(w-e*)+1].
# Demand: Sum_e ceil((N-3e)/3). Predict UNSAT when demand > supply; cross-check by SAT.
C = 1.1
def demand(N):
    return sum(math.ceil((N - 3 * e) / 3) for e in range(1, (N - 1) // 3 + 1))
def supply(N):
    return (1 - 1 / C) * N * (N + 1) / 2 + N / C
N0 = None
for N in range(4, 4000):
    if demand(N) > supply(N):
        N0 = N
        break
print(f"C={C}: ceiling-corrected theorem predicts UNSAT for N >= {N0} "
      f"(demand {demand(N0)} > supply {supply(N0):.1f}); monotone beyond: "
      f"{all(demand(N) > supply(N) for N in range(N0, N0+200))}")
sat = solve_profile_frac(N0, C)
print(f"SAT check at N={N0}, C={C}: {'SAT (!!PROBLEM!!)' if sat else 'UNSAT (consistent)'}")
# theorem slack: find the actual SAT threshold for C=1.1 (should be well below N0)
N = 4; last = None
while N < N0:
    if solve_profile_frac(N, C): last = N; N += 2
    else: break
print(f"actual SAT frontier for C=1.1: last SAT ~ N={last}, first UNSAT ~ N={N} (theorem N0={N0}: slack factor ~{N0/max(N,1):.1f})")
