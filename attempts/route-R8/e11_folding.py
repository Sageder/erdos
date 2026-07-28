"""e11_folding.py — folding-obstruction experiments (route R8 deliverable 2).

Object: a machine-verified two-sided window B = b[-L..R] of a Z-permutation avoiding monotone
k-APs (k = 5 dyadic macro from e4_zjoint; k = 4 ternary macro from e10_zb3).

Folding strategies applied and analyzed:
  (a) RESTRICTION: subsequence of positive values in position order.  Check: creates no new
      monotone APs (restriction lemma); but measure the SIDE-DISTRIBUTION of positive values'
      positions: if positives occupy both cofinal directions, the restriction has order type
      zeta, not omega -> not an N-permutation (obstruction (a) quantified).
  (b) ZIGZAG FOLD: positions reordered by |p| (0, +1, -1, +2, -2, ...), values mapped by
      mu(v) = 2v (v >= 1), 1 - 2v (v <= 0)  [bijection Z -> N].  The result is an N-indexed
      sequence of distinct positive integers.  Machine-find ALL monotone k-APs and 4-APs of
      the fold and classify:
        b1: all terms in one mu-class (all even / all odd values) — these pull back to Z-APs
            monotone for |p|-order but not for p-order (position-order failure);
        b2: parity-alternating terms (odd d) — new APs invisible in Z (value-map failure).
  (c) VALUE CONJUGATION rigidity: verify by machine on a sample that mu maps many Z-APs to
      non-APs and mu^{-1} maps many N-APs to non-APs (so neither direction preserves AP
      structure; the affine-rigidity lemma in REPORT.md explains why no bijection can).
"""

import sys
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "experiments"))
from zcheck import find_monotone_kaps, has_monotone_kap_window  # noqa: E402


def mu(v):
    return 2 * v if v >= 1 else 1 - 2 * v


def mu_inv(n):
    return n // 2 if n % 2 == 0 else (1 - n) // 2


def zigzag_fold(window, center):
    """window: list of values at positions -L..R (index i -> position i - L... we pass center
    = index of position 0).  Returns folded N-sequence: values mu(b(0)), mu(b(1)), mu(b(-1)),
    mu(b(2)), ... while both sides available (stop at the shorter side to keep symmetry)."""
    L = center            # positions -L..-1 exist
    R = len(window) - center - 1
    m = min(L, R)
    seq = [mu(window[center])]
    for q in range(1, m + 1):
        seq.append(mu(window[center + q]))
        seq.append(mu(window[center - q]))
    return seq


def classify_fold_aps(seq, k):
    wits = find_monotone_kaps(seq, k)
    b1e, b1o, b2 = [], [], []
    for terms, ps, orient in wits:
        pars = {t % 2 for t in terms}
        if pars == {0}:
            b1e.append((terms, orient))
        elif pars == {1}:
            b1o.append((terms, orient))
        else:
            b2.append((terms, orient))
    return b1e, b1o, b2


def analyze(name, window, center, k):
    print(f"--- {name} (|window| = {len(window)}, k = {k}) ---")
    assert not has_monotone_kap_window(window, k), "input object not verified!"
    # (a) restriction
    positives = [v for v in window if v >= 1]
    posidx = [i - center for i, v in enumerate(window) if v >= 1]
    left = sum(1 for p in posidx if p < 0)
    right = len(posidx) - left
    news = find_monotone_kaps(positives, k)
    print(f"(a) restriction to positive values: monotone {k}-APs created: {len(news)} "
          f"(restriction lemma predicts 0); positions of positives: {left} on the left side, "
          f"{right} on the right side -> order type of the infinite restriction: "
          f"{'zeta (NOT omega) -- not an N-permutation' if left > 0 and right > 0 else 'omega'}")
    # (b) zigzag fold
    fold = zigzag_fold(window, center)
    for kk in sorted({k, 4}):
        b1e, b1o, b2 = classify_fold_aps(fold, kk)
        print(f"(b) zigzag fold: monotone {kk}-APs: same-class even {len(b1e)}, "
              f"same-class odd {len(b1o)}, parity-alternating (odd d) {len(b2)}")
        for tag, lst in (("even-class", b1e), ("odd-class", b1o), ("alt", b2)):
            for terms, orient in lst[:2]:
                pull = [mu_inv(t) for t in terms]
                isap = len({pull[j + 1] - pull[j] for j in range(len(pull) - 1)}) == 1
                print(f"      e.g. {tag} {terms} orient {orient}; pullback {pull} "
                      f"{'(a Z-AP: position-order failure b1)' if isap else '(NOT a Z-AP: value-map failure b2)'}")
    # (c) rigidity samples
    apsz = [[t, t + d, t + 2 * d, t + 3 * d] for t, d in [(-9, 2), (-5, 3), (2, 5), (-20, 13)]]
    broken = sum(1 for ap in apsz
                 if len({mu(ap[j + 1]) - mu(ap[j]) for j in range(3)}) > 1)
    apn = [[t, t + d, t + 2 * d, t + 3 * d] for t, d in [(2, 3), (1, 2), (3, 8), (5, 5)]]
    brokenn = sum(1 for ap in apn
                  if len({mu_inv(ap[j + 1]) - mu_inv(ap[j]) for j in range(3)}) > 1)
    print(f"(c) mu breaks {broken}/4 sample Z-APs; mu^-1 breaks {brokenn}/4 sample N-APs "
          f"(affine rigidity lemma: unavoidable for ANY bijection Z <-> N)")


if __name__ == "__main__":
    with open(os.path.join(HERE, "windows.json")) as f:
        objs = json.load(f)
    for name, obj in objs.items():
        analyze(name, obj["window"], obj["center"], obj["k"])
