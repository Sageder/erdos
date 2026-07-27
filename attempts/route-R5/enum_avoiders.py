"""enum_avoiders.py — exhaustive enumeration of monotone-4-AP-free permutations of [1..N].

Claim tested: DFS-with-pruning enumerator is exact (cross-checked against the literal
filter of all N! permutations for N <= 8, and against the calibration counts
6, 22, 102, 564, 3336, 22266, 168864 for N = 3..9 from NOTES.md / PROMPT §5).

Soundness of the incremental prune: in any monotone 4-AP the element occupying the
LATEST position is the largest value (increasing orientation) or the smallest value
(decreasing orientation).  Hence a monotone 4-AP is detected exactly when that element
is appended, at which moment the other three terms are already placed and their relative
positions are fully known.  So the DFS emits exactly the 4-AP-free permutations.
"""

import sys
sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos
from itertools import permutations


def gen_avoiders(n, callback):
    """Call callback(perm) for every monotone-4-AP-free permutation of [1..n].

    perm is a tuple with perm[i] = value at position i+1 (0-based internally)."""
    perm = []
    placed = [False] * (n + 1)
    pos = [0] * (n + 1)

    def ok(w):
        # placing w at the current latest position: does it complete a monotone 4-AP?
        d = 1
        while w - 3 * d >= 1:  # w as top of increasing 4-AP (w-3d, w-2d, w-d, w)
            if placed[w - d] and placed[w - 2 * d] and placed[w - 3 * d] and \
                    pos[w - 3 * d] < pos[w - 2 * d] < pos[w - d]:
                return False
            d += 1
        d = 1
        while w + 3 * d <= n:  # w as bottom of decreasing 4-AP (w+3d, w+2d, w+d, w)
            if placed[w + d] and placed[w + 2 * d] and placed[w + 3 * d] and \
                    pos[w + 3 * d] < pos[w + 2 * d] < pos[w + d]:
                return False
            d += 1
        return True

    def rec():
        if len(perm) == n:
            callback(tuple(perm))
            return
        t = len(perm)
        for w in range(1, n + 1):
            if not placed[w] and ok(w):
                placed[w] = True
                pos[w] = t
                perm.append(w)
                rec()
                perm.pop()
                placed[w] = False

    rec()


def count_avoiders_dfs(n):
    c = [0]
    gen_avoiders(n, lambda p: c.__setitem__(0, c[0] + 1))
    return c[0]


if __name__ == "__main__":
    # Cross-check 1: literal filter for N <= 8 must give the SAME SET.
    for n in range(3, 9):
        brute = set(p for p in permutations(range(1, n + 1))
                    if not has_monotone_kap_pos(p, 4))
        dfs = set()
        gen_avoiders(n, dfs.add)
        assert dfs == brute, f"N={n}: DFS set != brute set"
        print(f"N={n}: DFS==brute, count={len(dfs)}", flush=True)

    # Cross-check 2: calibration counts N=3..9.
    EXPECT4 = {3: 6, 4: 22, 5: 102, 6: 564, 7: 3336, 8: 22266, 9: 168864}
    for n in range(3, 10):
        c = count_avoiders_dfs(n)
        assert c == EXPECT4[n], (n, c, EXPECT4[n])
        print(f"N={n}: count {c} matches calibration", flush=True)
    print("ENUMERATOR VERIFIED (sets N<=8, counts N<=9).")
