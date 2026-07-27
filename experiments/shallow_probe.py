"""shallow_probe.py — probe FIN(K) (CORE.md Lemma 7): can 4-AP-free permutations of
[1..N] keep ALL values <= K within the first C positions, for large N?

Method: randomized DFS with restarts, placing values v = 1..N in increasing order.
By CORE.md Lemma 8 the feasible positions for v (w.r.t. 4-AP-freeness against smaller
values) form the interval (Lo(v), Hi(v)); we intersect with free slots and with the
probe constraint pos(v) <= C for v <= K. Existence search only (failure to find is NOT
proof of nonexistence — exhaustive work is route R4's job).

Sanity: the checker cross-validates each found permutation with the trusted
has_monotone_kap_pos from apcheck.py.

Output: for each (K, C): largest N reached with a witness within budget.
"""

import random
import sys
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos


def find_avoider(N, constraint=None, rng=None, tries=400, choice="random"):
    """Try to find a 4-AP-free permutation of [1..N] with pos(v) <= constraint(v)
    (constraint: function value -> max position, or None). Returns perm (list of values
    by position, 1-based values) or None. Randomized DFS with restarts; per-try node cap."""
    rng = rng or random.Random(0)
    for _ in range(tries):
        pos = {}          # value -> position (1-based)
        occupied = set()
        ok = True
        for v in range(1, N + 1):
            lo, hi = 0, N + 1
            for d in range(1, (v - 1) // 3 + 1):
                p1, p2, p3 = pos[v - d], pos[v - 2 * d], pos[v - 3 * d]
                if p3 < p2 < p1:
                    hi = min(hi, p1)
                elif p3 > p2 > p1:
                    lo = max(lo, p1)
            cap = hi
            if constraint is not None:
                cap = min(cap, constraint(v) + 1)
            cands = [p for p in range(lo + 1, cap) if p not in occupied]
            if not cands:
                ok = False
                break
            if choice == "random":
                p = rng.choice(cands)
            elif choice == "low":
                p = cands[0] if rng.random() < 0.7 else rng.choice(cands)
            else:
                p = cands[len(cands) // 2]
            pos[v] = p
            occupied.add(p)
        if ok:
            perm = [0] * N
            for v, p in pos.items():
                perm[p - 1] = v
            assert sorted(perm) == list(range(1, N + 1))
            assert not has_monotone_kap_pos(perm, 4), perm
            if constraint is not None:
                assert all(pos[v] <= constraint(v) for v in range(1, N + 1)), "constraint violated"
            return perm
    return None


def probe(K, C, Ns, seed=196, tries=400):
    rng = random.Random(seed)
    results = {}
    last = None
    for N in Ns:
        cons = (lambda v: C if v <= K else 10**9)
        w = find_avoider(N, cons, rng, tries=tries)
        results[N] = w is not None
        if w is not None:
            last = (N, w)
    return results, last


if __name__ == "__main__":
    Ns = [10, 15, 20, 25, 30, 40, 50, 60, 80, 100]
    print("Unconstrained sanity (does the randomized search find plain avoiders?):")
    r, _ = probe(0, 0, Ns, tries=200)
    print("  ", {n: ("Y" if v else "n") for n, v in r.items()}, flush=True)
    for K, C in [(2, 3), (2, 6), (3, 5), (3, 10), (4, 8), (4, 20), (6, 12), (8, 16)]:
        r, last = probe(K, C, Ns, tries=200)
        line = {n: ("Y" if v else "n") for n, v in r.items()}
        print(f"K={K} C={C}: {line}", flush=True)
        if last and last[0] >= 80:
            print(f"   witness at N={last[0]}: first {max(12, K+2)} slots = {last[1][:max(12, K+2)]}")
