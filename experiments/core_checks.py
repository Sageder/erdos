"""core_checks.py — machine sanity checks for attempts/core/CORE.md.

Claims tested:
 (T1) Lemma 4 finite analogue: every 4-AP-free permutation of [1..N] (N <= 10) with
      pos(1) = 1 satisfies, for all j with 1+3j <= N: NOT(pos(1+j) < pos(1+2j) < pos(1+3j)).
 (T2) Lemma 4 general (**) finite analogue: for every 4-AP-free perm of [1..N] (N <= 9),
      every value v and every j > E(v) (max value before v; 0 if none) with v+3j <= N:
      NOT(pos(v+j) < pos(v+2j) < pos(v+3j)).
 (T3) Lemma 5 finite analogue: every permutation of [1..N] with |pos(v)-v| <= B contains
      a monotone increasing 4-AP once N >= 1 + 3*(2B+1); exhaustive for B = 1, N = 10
      (perms with displacement <= 1) and randomized for B = 2, N = 16.
 (T4) The adversary DAG (edges k -> 2k and 3j -> 2j on [1..M]) is acyclic and every node
      has finitely many ancestors; checked M = 3000 via topological sort + ancestor counts
      for sample nodes.
Conclusion: printed.
"""

from itertools import permutations
import sys
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos


def posmap(perm):
    pos = {}
    for i, v in enumerate(perm):
        pos[v] = i
    return pos


# T1, T2
for N in range(4, 10):
    for p in permutations(range(1, N + 1)):
        if has_monotone_kap_pos(p, 4):
            continue
        pos = posmap(p)
        # T1
        if p[0] == 1:
            for j in range(1, (N - 1) // 3 + 1):
                assert not (pos[1 + j] < pos[1 + 2 * j] < pos[1 + 3 * j]), (p, j)
        # T2
        for idx, v in enumerate(p):
            E = max(p[:idx]) if idx > 0 else 0
            j = E + 1
            while v + 3 * j <= N:
                assert not (pos[v + j] < pos[v + 2 * j] < pos[v + 3 * j]), (p, v, j)
                j += 1
print("T1, T2 PASS (N <= 9; T1 also N = 10 below)")

N = 10
for p in permutations(range(1, N + 1)):
    if p[0] != 1 or has_monotone_kap_pos(p, 4):
        continue
    pos = posmap(p)
    for j in range(1, (N - 1) // 3 + 1):
        assert not (pos[1 + j] < pos[1 + 2 * j] < pos[1 + 3 * j]), (p, j)
print("T1 PASS (N = 10)")

# T3 exhaustive B=1, N=10: perms with |pos(v)-v|<=1 are products of adjacent swaps;
# enumerate via DP over positions.
def perms_with_displacement(n, B):
    out = []
    def rec(i, used, cur):
        if i == n:
            out.append(tuple(cur))
            return
        for v in range(max(1, i + 1 - B), min(n, i + 1 + B) + 1):
            if v not in used:
                used.add(v); cur.append(v)
                rec(i + 1, used, cur)
                used.discard(v); cur.pop()
    rec(0, set(), [])
    return out

cnt = 0
for p in perms_with_displacement(10, 1):
    cnt += 1
    assert has_monotone_kap_pos(p, 4), p
print(f"T3 PASS (B=1, N=10 exhaustive over {cnt} perms: all contain a monotone 4-AP)")

import random
rng = random.Random(42)
allp = perms_with_displacement(16, 2)
for p in rng.sample(allp, min(20000, len(allp))):
    assert has_monotone_kap_pos(p, 4), p
print(f"T3 PASS (B=2, N=16, sampled {min(20000, len(allp))} of {len(allp)})")

# T4
M = 3000
from collections import defaultdict
edges = defaultdict(list)   # u -> v meaning u must come before v?? direction: k -> 2k (k before 2k), 3j -> 2j (3j before 2j)
indeg = defaultdict(int)
nodes = set(range(1, M + 1))
for k in range(1, M + 1):
    if 2 * k <= M:
        edges[k].append(2 * k); indeg[2 * k] += 1
    if 3 * k <= M:
        edges[3 * k].append(2 * k); indeg[2 * k] += 1
import heapq
q = [n for n in nodes if indeg[n] == 0]
seen = 0
qq = list(q)
while qq:
    u = qq.pop()
    seen += 1
    for w in edges[u]:
        indeg[w] -= 1
        if indeg[w] == 0:
            qq.append(w)
assert seen == M, f"cycle detected: only {seen}/{M} sorted"
# ancestor counts for a few nodes (within [1..M])
ranc = defaultdict(set)
import functools
parents = defaultdict(list)
for u in edges:
    for w in edges[u]:
        parents[w].append(u)
@functools.lru_cache(maxsize=None)
def anc(n):
    s = set()
    for p in parents[n]:
        s.add(p); s |= anc(p)
    return frozenset(s)
for n in (256, 1024, 972, 2048):
    a = anc(n)
    assert len(a) < 200, (n, len(a))
print(f"T4 PASS (DAG acyclic on [1..{M}]; sample ancestor counts: "
      f"{[(n, len(anc(n))) for n in (256, 1024, 972, 2048)]})")
print("ALL CORE CHECKS PASS")
