#!/usr/bin/env python3
"""
THE BLOW-UP FAMILY.

Let V be a solution (legal, sum 1) and let q = 2d+1 be odd.  Replace each n in V
by a block of length q centred near qn and shifted by s_n:

        B_n(s) = [ qn - d + s ,  qn + d + s ].

*  H(B_n(0)) = 1/n + eta_n with eta_n = sum_{j=1..d} 2j^2/(qn(q^2n^2-j^2)) > 0,
   an EXCESS of order 1/n^3; shifting by s changes the sum by roughly -s/(qn^2),
   so the menu of shifts brackets 1/n from both sides with fine granularity.
*  Disjointness: for n' >= n+2 the blocks are separated as soon as |s| <= R with
   2R < q+1.  For consecutive n, n+1 in V the blocks touch or separate according
   to  s_{n+1} >= s_n  (they may be adjacent, which is legal), so the admissible
   shift vectors are exactly those NON-DECREASING along each run of V.
*  The image is legal, has run count = (number of runs of V) -- CONSTANT in q --
   and capacity |V| * floor(q/2) -> infinity with q.

So a single hit for each of infinitely many q would give solutions with bounded
run count and unbounded capacity, i.e. P(k) for all large k.  This script decides
the exact equation  sum_n H(B_n(s_n)) = 1  by meet-in-the-middle over the runs.

Exact arithmetic throughout.
"""
import sys
from fractions import Fraction as F
from itertools import product, combinations_with_replacement


def runs_of(U):
    U = sorted(U); out = []; cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1: cur.append(x)
        else: out.append(cur); cur = [x]
    out.append(cur); return out


def H(a, b):
    return sum(F(1, n) for n in range(a, b + 1))


def run_options(run, q, R):
    """all non-decreasing shift vectors for one run, with exact block-sum totals"""
    d = (q - 1) // 2
    shifts = range(-R, R + 1)
    out = []
    for vec in combinations_with_replacement(shifts, len(run)):
        tot = F(0); blocks = []
        for n, s in zip(run, vec):
            a, b = q * n - d + s, q * n + d + s
            blocks.append((a, b)); tot += H(a, b)
        out.append((vec, tot, blocks))
    return out


def solve(V, q, R):
    Rs = runs_of(V)
    opts = [run_options(r, q, R) for r in Rs]
    h = len(opts) // 2
    tab = {}
    for combo in product(*opts[:h]):
        s = sum(c[1] for c in combo)
        tab.setdefault(s, combo)
    for combo in product(*opts[h:]):
        need = 1 - sum(c[1] for c in combo)
        if need in tab:
            return tab[need] + combo
    return None


def check(blocks):
    flat = []
    for a, b in blocks:
        assert b - a + 1 >= 2 and a >= 2
        flat += list(range(a, b + 1))
    assert len(flat) == len(set(flat)), "overlap"
    s = sum(F(1, n) for n in flat)
    S = set(flat)
    return s, all(n - 1 in S or n + 1 in S for n in flat), sorted(flat)


if __name__ == "__main__":
    V = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else \
        [5, 6, 14, 15, 17, 18, 20, 21, 22, 27, 28, 33, 34, 44, 45, 54, 55, 84, 85]
    qs = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [5, 7, 9, 11, 13]
    R = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    assert sum(F(1, n) for n in V) == 1
    for q in qs:
        if 2 * R >= q + 1:
            print(f"q={q}: R too large for disjointness, skip"); continue
        res = solve(V, q, R)
        if res is None:
            print(f"q={q} R={R}: no hit")
        else:
            blocks = [b for c in res for b in c[2]]
            s, legal, flat = check(blocks)
            L = [len(r) for r in runs_of(flat)]
            r, M = len(L), sum(x // 2 for x in L)
            print(f"*** q={q} HIT: sum={s} legal={legal} blocks={len(blocks)} "
                  f"r={r} cap={M} max={max(flat)}")
            print(f"    blocks={blocks}")
        sys.stdout.flush()
