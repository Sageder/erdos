#!/usr/bin/env python3
"""
Emit and INDEPENDENTLY verify an explicit certificate for each k for which a
solution is known: a list of EXACTLY k pairwise disjoint intervals, each of
length >= 2, all elements >= 2, whose reciprocals sum to exactly 1.

The splitting lemma is applied concretely (not just counted): a run of length L
is cut into t pieces (t-1 of length 2 and one of length L-2(t-1) >= 2).

Verification is from scratch, in exact rational arithmetic, with no reliance on
the search code:  count == k, every |I| >= 2, pairwise disjoint, min element >= 2,
sum == 1.
"""
import sys
from fractions import Fraction as F


def runs_of(U):
    U = sorted(U); out = []; cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1: cur.append(x)
        else: out.append((cur[0], cur[-1])); cur = [x]
    out.append((cur[0], cur[-1])); return out


def split_run(a, b, t):
    """cut [a,b] into exactly t blocks each of length >= 2"""
    L = b - a + 1
    assert 1 <= t <= L // 2, (a, b, t)
    out = []; pos = a
    for i in range(t - 1):
        out.append((pos, pos + 1)); pos += 2
    out.append((pos, b))
    assert out[-1][1] - out[-1][0] + 1 >= 2
    return out


def blocks_for_k(U, k):
    """return exactly k blocks, or None"""
    R = runs_of(U)
    caps = [(b - a + 1) // 2 for a, b in R]
    r, M = len(R), sum(caps)
    if not (r <= k <= M):
        return None
    # distribute: give each run 1, then add extra one at a time up to its capacity
    t = [1] * r
    extra = k - r
    for i in range(r):
        add = min(extra, caps[i] - 1)
        t[i] += add; extra -= add
        if extra == 0: break
    assert extra == 0
    out = []
    for (a, b), ti in zip(R, t):
        out += split_run(a, b, ti)
    return out


def verify(blocks, k):
    assert len(blocks) == k, f"block count {len(blocks)} != {k}"
    for a, b in blocks:
        assert isinstance(a, int) and isinstance(b, int)
        assert a >= 2, "element < 2"
        assert b - a + 1 >= 2, "block of length < 2"
    srt = sorted(blocks)
    for i in range(len(srt) - 1):
        assert srt[i][1] < srt[i + 1][0], "blocks overlap"
    s = F(0)
    for a, b in blocks:
        for n in range(a, b + 1):
            s += F(1, n)
    assert s == 1, f"sum {s} != 1"
    return True


if __name__ == "__main__":
    paths = sys.argv[1:] or ["attempts/route-C/allsols_le105.txt", "experiments/s130.out"]
    best = {}
    for p in paths:
        for ln in open(p):
            if not ln.startswith("SOL"): continue
            U = [int(x) for x in ln.split()[1:]]
            R = runs_of(U); r = len(R); M = sum((b - a + 1) // 2 for a, b in R)
            for k in range(r, M + 1):
                if k not in best or max(U) < max(best[k]):
                    best[k] = U
    print("k : explicit certificate (exactly k disjoint blocks, each length >= 2)\n")
    for k in sorted(best):
        B = blocks_for_k(best[k], k)
        verify(B, k)
        print(f"k={k:3d}  max={max(best[k]):4d}  VERIFIED  {B}")
    print(f"\nAll certificates verified in exact rational arithmetic. "
          f"k values: {sorted(best)}")
