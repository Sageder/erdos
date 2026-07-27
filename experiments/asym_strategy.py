"""asym_strategy.py — probe the asymmetric NO-strategy:
Does there exist (finitely, at growing N) a permutation of [1..N] with
  (i) NO monotone DECREASING 3-AP, and (ii) NO monotone INCREASING 4-AP?
Any such permutation is automatically monotone-4-AP-free (a decreasing 4-AP contains a
decreasing 3-AP). If such permutations exist for all N with displacement control, this
is a NO-construction target; if they die at finite N, that is a structural theorem.

Engine: exhaustive count for small N; interval-based DFS (values in increasing order)
for existence at larger N. Constraints when placing v (values 1..v-1 placed):
  - for each d: if pair (v-2d, v-d) is positionally DEcreasing, then pos(v) > pos(v-d)
    [else dec-3AP (v-2d, v-d, v)]  -> Lo constraint
  - for each d: if triple (v-3d, v-2d, v-d) is positionally INcreasing, then
    pos(v) < pos(v-d)  [else inc-4AP]  -> Hi constraint
Exact; cross-validated against brute-force definition checks.
"""

import sys, random
from itertools import permutations
sys.path.insert(0, '/home/user/erdos/experiments')


def violates(perm):
    """True iff perm (tuple of values) has a decreasing monotone 3-AP or an increasing
    monotone 4-AP. Brute force via positions."""
    n = len(perm)
    pos = [0] * (n + 1)
    for i, v in enumerate(perm):
        pos[v] = i
    for d in range(1, (n - 1) // 2 + 1):
        for x in range(1, n - 2 * d + 1):
            if pos[x] > pos[x + d] > pos[x + 2 * d]:
                return True
    for d in range(1, (n - 1) // 3 + 1):
        for x in range(1, n - 3 * d + 1):
            if pos[x] < pos[x + d] < pos[x + 2 * d] < pos[x + 3 * d]:
                return True
    return False


def count_exhaustive(n):
    return sum(1 for p in permutations(range(1, n + 1)) if not violates(p))


def dfs_exists(N, seed=0, tries=3000, choice="random"):
    """Randomized greedy with restarts using the interval structure. Returns a witness
    permutation or None."""
    rng = random.Random(seed)
    for _ in range(tries):
        pos = {}
        occupied = set()
        ok = True
        for v in range(1, N + 1):
            lo, hi = 0, N + 1
            for d in range(1, (v - 1) // 2 + 1):
                if v - 2 * d >= 1 and pos[v - 2 * d] > pos[v - d]:
                    lo = max(lo, pos[v - d])
            for d in range(1, (v - 1) // 3 + 1):
                if pos[v - 3 * d] < pos[v - 2 * d] < pos[v - d]:
                    hi = min(hi, pos[v - d])
            cands = [p for p in range(lo + 1, hi) if p not in occupied]
            if not cands:
                ok = False
                break
            p = rng.choice(cands)
            pos[v] = p
            occupied.add(p)
        if ok:
            perm = [0] * N
            for v, p in pos.items():
                perm[p - 1] = v
            assert sorted(perm) == list(range(1, N + 1))
            assert not violates(tuple(perm)), perm
            return perm
    return None


if __name__ == "__main__":
    print("Exhaustive counts (no dec-3AP, no inc-4AP):")
    for n in range(3, 11):
        print(f"  N={n}: {count_exhaustive(n)}", flush=True)
    print("Randomized existence at larger N (interval DFS, 3000 restarts):")
    for N in (12, 15, 20, 25, 30, 40, 50, 70, 100):
        w = dfs_exists(N, seed=196)
        print(f"  N={N}: {'FOUND' if w else 'not found'}"
              + (f"  perm={w}" if w and N <= 30 else ""), flush=True)
