"""Route R5: scalable segmented sieve for S_k membership (Erdos 727).

S_k = { n >= 1 : ((n+k)!)^2 | (2n)! }.

Exact membership (PROBLEM.md, Legendre):
    n in S_k  <=>  for all primes p <= n+k:  2*s_p(n+k) - s_p(2n) >= 2k.

Large-prime criterion (PROBLEM.md, valid for p > max(sqrt(2n), 2k)):
    the condition at p fails iff p divides some window element n+1..n+k.
Hence for n > 2k^2 (so that sqrt(2n) > 2k):
    n in S_k  <=>  [every n+j (1<=j<=k) is isqrt(2n)-smooth]
                   AND [digit condition holds for all p <= isqrt(2n)].
The digit condition is the EXACT condition at every prime, so checking it at a
superset of primes p <= P (P >= isqrt(2n)) is still exact: extra primes'
conditions are true statements about membership, automatically satisfied by
smooth-window survivors.

Architecture per block [L, R) of n-values (requires L > 2*k^2 for all k used):
  step (a): "rough" remainder sieve on m in [L+1, R+kmax]: divide each m by all
     prime powers q = p^e <= R+kmax with p <= P0 = isqrt(R+kmax).  The residual
     rem[m] is then 1 or a SINGLE prime > P0 (two such factors would exceed
     R+kmax, guarded by an assertion).  n survives for k iff
     max_j rem[n+j] <= isqrt(2n).
  step (b): vectorized digit check of all survivors at all p <= isqrt(2(R-1)),
     with compaction (kill order chosen by measured kill rates; any order is
     exact, order affects speed only).

All arithmetic is int64 exact (values < 2^31, digit sums tiny).
"""

import json
import math
import os

import numpy as np


def primes_upto(limit: int) -> np.ndarray:
    """All primes <= limit, ascending (numpy int64)."""
    if limit < 2:
        return np.zeros(0, dtype=np.int64)
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:: p] = False
    return np.nonzero(sieve)[0].astype(np.int64)


def rough_rem(mlo: int, mhi: int, primes_small: np.ndarray) -> np.ndarray:
    """rem[i] = (mlo+i) with all prime factors p in primes_small fully divided out,
    for m in [mlo, mhi] inclusive.  primes_small must contain every prime <= isqrt(mhi)."""
    n_el = mhi - mlo + 1
    rem = np.arange(mlo, mhi + 1, dtype=np.int64)
    for p in primes_small:
        p = int(p)
        if p * p > mhi:
            break
        q = p
        while q <= mhi:
            start = (-mlo) % q
            if start < n_el:
                rem[start::q] //= p
            q *= p
    return rem


def spvec(arr: np.ndarray, p: int) -> np.ndarray:
    """Vectorized base-p digit sum."""
    s = np.zeros(arr.shape, dtype=np.int64)
    a = arr.copy()
    while a.max(initial=0) > 0:
        s += a % p
        a //= p
    return s


def isqrt_vec(x: np.ndarray) -> np.ndarray:
    """Exact floor(sqrt(x)) for int64 x < 2^52 via float sqrt + correction."""
    r = np.sqrt(x.astype(np.float64)).astype(np.int64)
    r -= (r * r > x)
    r += ((r + 1) * (r + 1) <= x)
    return r


def block_members(L: int, R: int, ks, primes_small: np.ndarray,
                  primes_digit: np.ndarray, kill_order=None,
                  return_survivors=False):
    """Exact S_k members with n in [L, R), for each k in ks (list, ascending).

    Requires L > 2*max(ks)^2.  primes_small: all primes <= isqrt(R-1+max(ks)).
    primes_digit: all primes <= isqrt(2*(R-1)).
    kill_order: optional permutation (array of indices into primes_digit) used
    for the digit-check scan order; correctness independent of order.
    Returns dict k -> sorted numpy array of members (and dict k -> survivor
    count if return_survivors).
    """
    kmax = max(ks)
    assert L > 2 * kmax * kmax
    mhi = R - 1 + kmax
    p0 = int(primes_small[-1])
    # guard: residual after rough sieve must be 1 or a single prime, which holds
    # iff primes_small contains every prime <= isqrt(mhi): verify no prime lives
    # in (p0, isqrt(mhi)] by trial division (tiny range).
    for c in range(p0 + 1, math.isqrt(mhi) + 1):
        assert any(c % int(p) == 0 for p in primes_small if p * p <= c), \
            f"prime {c} <= isqrt(mhi) missing from primes_small"
    rem = rough_rem(L + 1, mhi, primes_small)

    nvals = np.arange(L, R, dtype=np.int64)
    thr = isqrt_vec(2 * nvals)          # isqrt(2n)
    nblock = R - L

    out = {}
    surv_counts = {}
    winmax = np.zeros(nblock, dtype=np.int64)
    for k in ks:  # ascending: extend window max incrementally
        lo = ks[0] if k == ks[0] else None
        # winmax over j=1..k of rem[n+j]; rem index of n+j is (n+j)-(L+1)
        jstart = 1 if k == ks[0] else prev_k + 1
        for j in range(jstart, k + 1):
            np.maximum(winmax, rem[j - 1: j - 1 + nblock], out=winmax)
        prev_k = k
        surv = nvals[winmax <= thr]
        surv_counts[k] = len(surv)
        # digit check with compaction
        alive = surv
        order = kill_order if kill_order is not None else range(len(primes_digit))
        for idx in order:
            if len(alive) == 0:
                break
            p = int(primes_digit[idx])
            good = 2 * spvec(alive + k, p) - spvec(2 * alive, p) >= 2 * k
            alive = alive[good]
        out[k] = alive
    if return_survivors:
        return out, surv_counts
    return out


def load_kill_order(path: str, primes_digit: np.ndarray):
    """Load a kill order file: JSON list of primes; map to indices; primes not
    listed are appended in ascending order."""
    with open(path) as f:
        plist = json.load(f)
    pos = {int(p): i for i, p in enumerate(primes_digit.tolist())}
    order = [pos[p] for p in plist if p in pos]
    seen = set(order)
    order += [i for i in range(len(primes_digit)) if i not in seen]
    return order
