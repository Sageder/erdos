"""r13enum.py — avoider enumeration + record/grounded utilities for route R13.

Cross-validated against experiments/apcheck.py (trusted) and against the
calibration counts 6,22,102,564,3336,22266,168864 (N=3..9).

Conventions (PROBLEM.md): perm is a tuple, perm[i] = value at position i+1.
pos[v] = 1-based position of value v.

record (sigma_N-record): pos[w] < pos[v] for every v in (w, N].
grounded:                pos[g] > pos[v] for every v in [1, g).

NOTE ON FAITHFULNESS (recorded, used throughout):
 * `grounded` is EXACT: for g <= N, g is grounded in an infinite avoider a iff g is
   grounded in the restriction sigma_N (the defining condition mentions only values < g).
 * `record` is a RELAXATION: a genuine record of a, restricted, is a sigma_N-record,
   but sigma_N may have extra records.  Consequently:
     - a pattern EXCLUDED on all finite boards is excluded for genuine records too
       (restriction of an infinite avoider is a finite avoider);
     - a pattern REALIZED on a finite board refutes only the LOCAL form of a candidate
       lemma (the form derivable from "w precedes the finitely many mentioned larger
       values" plus 4-AP-freeness inside the window).  Every proof in this project is
       of that local form, so this is the operative refutation criterion.
"""

import sys

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos  # noqa: E402


def gen_avoiders(n, callback, first=None, last=None):
    """Call callback(perm) for every monotone-4-AP-free permutation of [1..n].

    Optional `first` / `last` pin perm[0] / perm[-1].
    Prune soundness: in a monotone 4-AP the LAST-positioned term is the largest value
    (increasing orientation) or the smallest (decreasing), so the violation is detected
    exactly when that term is appended.
    """
    perm = []
    placed = [False] * (n + 2)
    pos = [0] * (n + 2)

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
        t = len(perm)
        if t == n:
            callback(tuple(perm))
            return
        if first is not None and t == 0:
            cand = [first]
        elif last is not None and t == n - 1:
            cand = [last]
        else:
            cand = range(1, n + 1)
        for w in cand:
            if placed[w]:
                continue
            if last is not None and w == last and t != n - 1:
                continue
            if not ok(w):
                continue
            placed[w] = True
            pos[w] = t
            perm.append(w)
            rec()
            perm.pop()
            placed[w] = False

    rec()


def posarray(perm):
    n = len(perm)
    pos = [0] * (n + 1)
    for i, v in enumerate(perm):
        pos[v] = i + 1
    return pos


def records(pos, n):
    """sigma_N-records: w with pos[w] < pos[v] for all v in (w, n]."""
    out = []
    best = n + 10 ** 9
    for w in range(n, 0, -1):
        if pos[w] < best:
            out.append(w)
        best = min(best, pos[w])
    out.reverse()
    return out


def grounded(pos, n):
    """g with pos[g] > pos[v] for all v < g."""
    out = []
    best = -1
    for g in range(1, n + 1):
        if pos[g] > best:
            out.append(g)
        best = max(best, pos[g])
    return out


if __name__ == "__main__":
    from itertools import permutations
    # cross-check the enumerator against a literal filter
    for n in range(3, 9):
        brute = set(p for p in permutations(range(1, n + 1))
                    if not has_monotone_kap_pos(p, 4))
        dfs = set()
        gen_avoiders(n, dfs.add)
        assert dfs == brute, n
        print(f"N={n}: DFS==brute-filter, count={len(dfs)}", flush=True)
    EXPECT = {3: 6, 4: 22, 5: 102, 6: 564, 7: 3336, 8: 22266, 9: 168864}
    for n in range(3, 10):
        c = [0]
        gen_avoiders(n, lambda p: c.__setitem__(0, c[0] + 1))
        assert c[0] == EXPECT[n], (n, c[0])
        print(f"N={n}: count {c[0]} matches calibration", flush=True)
    # cross-check records/grounded against literal definitions on all N=6 avoiders
    def chk(p):
        n = len(p)
        po = posarray(p)
        R = set(w for w in range(1, n + 1)
                if all(po[w] < po[v] for v in range(w + 1, n + 1)))
        G = set(g for g in range(1, n + 1)
                if all(po[g] > po[v] for v in range(1, g)))
        assert set(records(po, n)) == R, (p, records(po, n), R)
        assert set(grounded(po, n)) == G, (p, grounded(po, n), G)
    gen_avoiders(6, chk)
    gen_avoiders(7, chk)
    print("records/grounded helpers verified against literal definitions (N=6,7).")
    print("ENUM VERIFIED")
