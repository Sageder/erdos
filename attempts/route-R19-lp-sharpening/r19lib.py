"""r19lib.py -- exact tools for route R19 (LP sharpening via prefix-completion ledger).

Conventions (PROBLEM.md): a permutation of [1..N] is a list `perm` with
perm[i] = value at position i+1.  pos[v] = 1-based position of value v.

Central objects (all EXACT integer arithmetic):

  m(w)   = min{ v <= w : pos(v) >= pos(w) }          ("prefix depth" of w)
  e*(w)  = w - m(w)                                   (max drop scale of w; CORE Thm 12)
  R(p)   = max{ j : [1..j] subset of positions [1..p-1] }   (staircase / prefix reach)
  tau_j  = max_{v <= j} pos(v)                        (completion time of [1..j])
  A_e    = { w : e*(w) < e } = { w : [1..w-e] all precede w }   ("e-grounded" values)

Exact identities proved in REPORT.md (Prop 1):
  m(w) = R(pos(w)) + 1
  sum_w e*(w) = N(N+1)/2 - N - sum_p R(p) = sum_j tau_j - N^2 + N(N+1)/2 - N
  #{w : e*(w) >= e} = N - |A_e|
All are asserted numerically in self_test().
"""

import sys
from itertools import permutations

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import (has_monotone_kap_pos, has_monotone_kap_brute,
                     has_monotone_kap_general)


# ---------------------------------------------------------------- basic checks

def pos_array(perm):
    N = len(perm)
    pos = [0] * (N + 1)
    for i, v in enumerate(perm):
        pos[v] = i + 1
    return pos


def has_inc_4ap(perm):
    """True iff perm has an INCREASING monotone 4-AP (values x,x+d,x+2d,x+3d in
    increasing position order)."""
    N = len(perm)
    pos = pos_array(perm)
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            if pos[x] < pos[x + d] < pos[x + 2 * d] < pos[x + 3 * d]:
                return True
    return False


def has_dec_4ap(perm):
    N = len(perm)
    pos = pos_array(perm)
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            if pos[x] > pos[x + d] > pos[x + 2 * d] > pos[x + 3 * d]:
                return True
    return False


# ---------------------------------------------------------------- ledger stats

def mstar(perm):
    """m(w) for all w; returns list indexed 1..N."""
    N = len(perm)
    pos = pos_array(perm)
    m = [0] * (N + 1)
    for w in range(1, N + 1):
        mm = w
        for v in range(1, w):
            if pos[v] > pos[w]:
                mm = v
                break
        m[w] = mm
    return m


def estar(perm):
    m = mstar(perm)
    return [0] + [w - m[w] for w in range(1, len(perm) + 1)]


def staircase(perm):
    """R(p) for p = 1..N+1 (R[p] with p 1-based); R(1)=0."""
    N = len(perm)
    pos = pos_array(perm)
    seen = [False] * (N + 2)
    R = [0] * (N + 2)
    j = 0
    for p in range(1, N + 2):
        R[p] = j
        if p <= N:
            seen[perm[p - 1]] = True
            while j + 1 <= N and seen[j + 1]:
                j += 1
    return R


def taus(perm):
    """tau_j = max_{v<=j} pos(v), j = 1..N."""
    N = len(perm)
    pos = pos_array(perm)
    out = [0] * (N + 1)
    cur = 0
    for j in range(1, N + 1):
        cur = max(cur, pos[j])
        out[j] = cur
    return out


def A_sizes(perm):
    """|A_e| for e = 1..N, where A_e = {w : e*(w) < e}."""
    N = len(perm)
    es = estar(perm)
    cnt = [0] * (N + 2)
    for w in range(1, N + 1):
        cnt[es[w] + 1] += 1   # w in A_e iff e > e*(w)
    out = [0] * (N + 2)
    run = 0
    for e in range(1, N + 2):
        run += cnt[e]
        out[e] = run
    return out


def ledger_stats(perm):
    N = len(perm)
    es = estar(perm)
    R = staircase(perm)
    tj = taus(perm)
    S_e = sum(es[1:])
    S_R = sum(R[p] for p in range(1, N + 1))
    S_tau = sum(tj[1:])
    return dict(N=N, sum_estar=S_e, sum_R=S_R, sum_tau=S_tau,
                gamma=S_tau / N ** 2, beta=S_e / N ** 2,
                Cbound=(1 / (1 - 2 * S_e / (N * (N + 1) / 2)) if S_e < N * (N + 1) / 4 else float('inf')))


# ---------------------------------------------------------------- constructions

def triadic(N):
    """Blocks [3^k, 3^{k+1}) in increasing k, each internally DECREASING (CORE Thm 14),
    truncated to values <= N in the induced position order."""
    seq = []
    k = 0
    while 3 ** k <= N:
        blk = [v for v in range(min(3 ** (k + 1) - 1, N), 3 ** k - 1, -1)]
        seq.extend(blk)
        k += 1
    assert sorted(seq) == list(range(1, N + 1))
    return seq


def geom_blocks(N, ratio):
    """Generalised reversed-block permutation with block boundaries b_0=1,
    b_{k+1} = ratio*b_k (integer rounding)."""
    bounds = [1]
    while bounds[-1] <= N:
        nb = max(bounds[-1] + 1, int(bounds[-1] * ratio))
        bounds.append(nb)
    seq = []
    for k in range(len(bounds) - 1):
        lo, hi = bounds[k], min(bounds[k + 1] - 1, N)
        if lo > N:
            break
        seq.extend(range(hi, lo - 1, -1))
    assert sorted(seq) == list(range(1, N + 1)), (N, ratio, len(seq))
    return seq


def sigma_parity(N):
    """Parity recursion: 3-AP-free permutation of [1..N] (PROBLEM.md background).
    sigma(S) for a set S in increasing order: list sigma(odd-indexed part) then
    sigma(even-indexed part)."""
    def rec(vals):
        if len(vals) <= 1:
            return list(vals)
        return rec(vals[0::2]) + rec(vals[1::2])
    out = rec(list(range(1, N + 1)))
    assert sorted(out) == list(range(1, N + 1))
    return out


# ---------------------------------------------------------------- self test

def self_test():
    import random
    rng = random.Random(19196)
    # cross-validate has_inc_4ap / has_dec_4ap against apcheck brute force
    for _ in range(4000):
        n = rng.randint(4, 9)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        inc, dec = has_inc_4ap(p), has_dec_4ap(p)
        assert (inc or dec) == has_monotone_kap_brute(p, 4) == has_monotone_kap_pos(p, 4), p
        # brute-force direct definition of increasing 4-AP
        from itertools import combinations
        binc = False
        for idx in combinations(range(n), 4):
            vals = [p[i] for i in idx]
            d = vals[1] - vals[0]
            if d >= 1 and all(vals[t + 1] - vals[t] == d for t in range(3)):
                binc = True
        assert binc == inc, (p, inc, binc)
    # identities
    for _ in range(2000):
        n = rng.randint(3, 12)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        pos = pos_array(p)
        m = mstar(p)
        R = staircase(p)
        for w in range(1, n + 1):
            assert m[w] == R[pos[w]] + 1, (p, w)
            # direct: e*(w) = max{e : pos(w-e) > pos(w)} (0 if none)
            best = 0
            for e in range(1, w):
                if pos[w - e] > pos[w]:
                    best = e
            assert w - m[w] == best, (p, w)
        es = estar(p)
        tj = taus(p)
        S_e = sum(es[1:])
        assert S_e == n * (n + 1) // 2 - n - sum(R[q] for q in range(1, n + 1))
        assert S_e == sum(tj[1:]) - n * n + n * (n + 1) // 2 - n
        A = A_sizes(p)
        for e in range(1, n + 1):
            assert n - A[e] == sum(1 for w in range(1, n + 1) if es[w] >= e)
            assert A[e] == sum(1 for w in range(1, n + 1)
                               if all(pos[v] < pos[w] for v in range(1, max(0, w - e) + 1)))
    # constructions
    for N in (5, 9, 13, 26, 27, 40, 80, 242, 243):
        t = triadic(N)
        assert not has_inc_4ap(t), N
        pos = pos_array(t)
        for v in range(1, N + 1):
            assert pos[v] <= 3 * v - 1, (N, v)
    for N in (5, 8, 16, 32, 64, 100):
        s = sigma_parity(N)
        assert not has_monotone_kap_pos(s, 3), N
    print("r19lib self_test OK (inc/dec checkers cross-validated vs apcheck brute force;"
          " ledger identities verified; triadic + parity constructions verified)")


if __name__ == "__main__":
    self_test()
