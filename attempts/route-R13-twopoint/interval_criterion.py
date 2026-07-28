"""interval_criterion.py — the record/grounded SANDWICH criterion.

PROVED (see REPORT): if a is a monotone-4-AP-free permutation of N, w a value-record
and g a grounded value with w < g, then every value v in (w,g) satisfies
pos(w) < pos(v) < pos(g).  Hence the restriction of a to the value interval [w..g],
listed in position order and relabelled by v -> v-w+1, is a monotone-4-AP-free
permutation of [1..M] (M = g-w+1) whose FIRST entry is 1 and whose LAST entry is M.

Since the record set and the grounded set are both infinite (CORE Lemma 11), M is
unbounded.  So:

   if "exists monotone-4-AP-free permutation of [1..M] with 1 first and M last"
   FAILS for all sufficiently large M, then 196-YES.

This script tests that finite property (exact DFS, first solution search).
"""

import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-R13-twopoint")
sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos  # noqa: E402


def find_one(n, first=None, last=None, extra_ok=None):
    """DFS for ONE monotone-4-AP-free permutation of [1..n] with the pins."""
    perm = []
    placed = [False] * (n + 2)
    pos = [0] * (n + 2)
    found = [None]

    def ok(w):
        d = 1
        while w - 3 * d >= 1:
            if placed[w - d] and placed[w - 2 * d] and placed[w - 3 * d] and \
                    pos[w - 3 * d] < pos[w - 2 * d] < pos[w - d]:
                return False
            d += 1
        d = 1
        while w + 3 * d <= n:
            if placed[w + d] and placed[w + 2 * d] and placed[w + 3 * d] and \
                    pos[w + 3 * d] < pos[w + 2 * d] < pos[w + d]:
                return False
            d += 1
        return True

    def rec():
        if found[0] is not None:
            return
        t = len(perm)
        if t == n:
            found[0] = tuple(perm)
            return
        if first is not None and t == 0:
            cand = [first]
        elif last is not None and t == n - 1:
            cand = [last]
        else:
            cand = range(1, n + 1)
        for w in cand:
            if placed[w] or (last is not None and w == last and t != n - 1):
                continue
            if not ok(w):
                continue
            if extra_ok is not None and not extra_ok(w, t, pos, placed):
                continue
            placed[w] = True
            pos[w] = t
            perm.append(w)
            rec()
            perm.pop()
            placed[w] = False
            if found[0] is not None:
                return

    rec()
    return found[0]


if __name__ == "__main__":
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    print("M : exists 4-AP-free perm of [1..M] with 1 first and M last?")
    fails = []
    for M in range(4, hi + 1):
        p = find_one(M, first=1, last=M)
        if p is not None:
            assert p[0] == 1 and p[-1] == M
            assert not has_monotone_kap_pos(p, 4), ("checker disagreement", p)
            print(f"M={M:3d}  YES   {p if M <= 20 else ''}", flush=True)
        else:
            fails.append(M)
            print(f"M={M:3d}  NO", flush=True)
    print("failures:", fails)
