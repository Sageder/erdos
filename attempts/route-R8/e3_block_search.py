"""e3_block_search.py — re-derive a DEGS77(b)-type explicit N-permutation with no monotone 5-AP,
in prefix-stable dyadic-block form:  A = tau_0 ++ tau_1 ++ ... with tau_m a permutation of the
block B_m = [2^m, 2^{m+1}).

Facts machine-checked here:
  (P) Pigeonhole lemma L2: for every AP t, t+d, ..., t+4d of positive integers, two of the LAST
      FOUR terms lie in the same dyadic block [2^j, 2^{j+1}).   (checked exhaustively in range)
  (S) Which simple per-block arrangements give monotone-5-AP-free prefixes:
      candidates: increasing, decreasing, sigma (parity recursion), reverse-sigma,
      gray (i -> i ^ (i>>1) offset order), xor-masks, etc.

A monotone 5-AP of the infinite object lies in a finite prefix, and every prefix is a
permutation of [1..2^{M+1}-1], so has_kap_perm_np on prefixes is an exact test up to that range.
"""

import sys
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "experiments"))
from fastcheck import has_kap_perm_np, find_kaps_perm_np  # noqa: E402
from parity_construction import sigma  # noqa: E402


def block_of(v):
    return v.bit_length() - 1


def check_pigeonhole(maxt, maxd):
    """L2: among t+d, t+2d, t+3d, t+4d two share a dyadic block (t, d >= 1)."""
    for t in range(1, maxt + 1):
        for d in range(1, maxd + 1):
            bs = [block_of(t + j * d) for j in (1, 2, 3, 4)]
            if len(set(bs)) == 4:
                return (t, d, bs)
    return None


# ---- block arrangement families ------------------------------------------------------------

def tau_increasing(m):
    return list(range(2 ** m, 2 ** (m + 1)))


def tau_decreasing(m):
    return list(range(2 ** (m + 1) - 1, 2 ** m - 1, -1))


def tau_sigma(m):
    n = 2 ** m
    return [2 ** m - 1 + s for s in sigma(n)]


def tau_sigma_rev(m):
    return tau_sigma(m)[::-1]


def tau_sigma_reflect(m):
    """sigma with values reflected within the block (v -> top+bottom-v)."""
    n = 2 ** m
    lo, hi = 2 ** m, 2 ** (m + 1) - 1
    return [lo + hi - v for v in tau_sigma(m)]


def tau_gray(m):
    n = 2 ** m
    return [2 ** m + (i ^ (i >> 1)) for i in range(n)]


def tau_xor(m, mask):
    n = 2 ** m
    return [2 ** m + (i ^ (mask & (n - 1))) for i in range(n)]


def assemble(tau_func, M):
    """Concatenate blocks 0..M; returns permutation of [1 .. 2^(M+1)-1]."""
    seq = []
    for m in range(M + 1):
        seq.extend(tau_func(m))
    return seq


def report(name, tau_func, M, k=5):
    seq = assemble(tau_func, M)
    n = len(seq)
    assert sorted(seq) == list(range(1, n + 1)), name
    bad = has_kap_perm_np(seq, k)
    wits = find_kaps_perm_np(seq, k, limit=4) if bad else []
    print(f"  {name:16s} M={M} N={n}: "
          + ("5-AP-FREE" if not bad else f"FAILS  witnesses (x,d,orient): {wits}"))
    return not bad


if __name__ == "__main__":
    ph = check_pigeonhole(3000, 1500)
    print("Pigeonhole L2 exhaustive t<=3000, d<=1500:",
          "HOLDS (no counterexample)" if ph is None else f"FAILS at {ph}")

    M = 9   # values up to 1023
    for name, f in [("increasing", tau_increasing),
                    ("decreasing", tau_decreasing),
                    ("sigma", tau_sigma),
                    ("sigma_rev", tau_sigma_rev),
                    ("sigma_reflect", tau_sigma_reflect),
                    ("gray", tau_gray)]:
        report(name, f, M)
    # xor masks: all-ones (= bit complement = reversal), alternating bits
    for mask_name, mask_f in [("xor_allones", lambda m: (1 << m) - 1),
                              ("xor_alt10", lambda m: int("10" * ((m + 1) // 2), 2) >> (0 if m % 2 == 0 else 1) if m > 0 else 0),
                              ]:
        def tf(m, mf=mask_f):
            return tau_xor(m, mf(m))
        report(mask_name, tf, M)
