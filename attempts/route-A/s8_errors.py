#!/usr/bin/env python3
"""
s8_errors.py -- TASK ITEM 1: "approximate 1/m by a block" systematically, and try to
make the accumulated errors cancel EXACTLY.

Part A.  Error table.  For every m and every block [a,b] with |H(a,b) - 1/m| small,
         tabulate the exact error  E(m;a,b) = H(a,b) - 1/m  in Q.
         In particular the two canonical length-2 choices
              [2m , 2m+1] : E = -1/(2m(2m+1))     (low)
              [2m-1, 2m ] : E = +1/(2m(2m-1))     (high)
         and length-L blocks centred on Lm.

Part B.  Take a classical Egyptian representation  1 = sum_{m in S} 1/m  and replace
         each 1/m by a block; the resulting block system sums to 1 + sum of errors,
         so we need the errors to cancel exactly.  We enumerate all Egyptian
         representations of 1 with denominators <= DMAX, all block choices from a
         candidate list per m, check DISJOINTNESS, and test the exact total.
         (Also allows "extra" free blocks taken from a small pool.)

All arithmetic exact (Fraction).
"""
import sys
from fractions import Fraction
from itertools import product


def H(a, b):
    return sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))


def error_table(mmax=12, Lmax=6, show=True):
    print("=== Part A: exact errors H(a,b) - 1/m for blocks near L*m ===")
    tab = {}
    for m in range(1, mmax + 1):
        rows = []
        for L in range(2, Lmax + 1):
            # block of length L whose sum is closest to 1/m: a ~ L*m - (L-1)/2
            a0 = max(2, round(L * m - (L - 1) / 2))
            for a in range(max(2, a0 - 2), a0 + 3):
                b = a + L - 1
                e = H(a, b) - Fraction(1, m)
                rows.append((L, a, b, e))
        rows.sort(key=lambda r: abs(r[3]))
        tab[m] = rows
        if show:
            print(" m=%d  1/m=%s" % (m, Fraction(1, m)))
            for (L, a, b, e) in rows[:6]:
                print("     L=%d [%d,%d]  H=%s  err=%s" % (L, a, b, H(a, b), e))
    return tab


def egyptian_reps(dmax, k_max=6):
    """all sets S of distinct integers 2<=m<=dmax (plus possibly nothing else)
       with sum 1/m = 1, |S| <= k_max"""
    reps = []

    def rec(rem, start, cur):
        if rem == 0:
            reps.append(tuple(cur))
            return
        if len(cur) >= k_max:
            return
        # need rem <= (k_max-len(cur)) / start
        if rem > Fraction(k_max - len(cur), start):
            return
        for m in range(start, dmax + 1):
            f = Fraction(1, m)
            if f > rem:
                continue
            if rem > Fraction(k_max - len(cur), m):
                break
            cur.append(m)
            rec(rem - f, m + 1, cur)
            cur.pop()

    rec(Fraction(1), 2, [])
    return reps


def part_B(dmax=40, k_max=6, Lmax=5, window=2):
    print("=== Part B: replace each 1/m by a nearby block, require exact cancellation ===")
    reps = egyptian_reps(dmax, k_max)
    print("Egyptian representations of 1 with denominators <= %d and <= %d terms: %d"
          % (dmax, k_max, len(reps)))
    found = []
    tested = 0
    for S in reps:
        cand = []
        for m in S:
            cs = []
            for L in range(2, Lmax + 1):
                a0 = max(2, int(round(L * m - (L - 1) / 2)))
                for a in range(max(2, a0 - window), a0 + window + 1):
                    b = a + L - 1
                    cs.append((a, b, H(a, b) - Fraction(1, m)))
            cand.append(cs)
        # DFS with interval pruning on the accumulated error (errors are tiny)
        k = len(cand)
        lo = [Fraction(0)] * (k + 1)   # most negative achievable from suffix
        hi = [Fraction(0)] * (k + 1)   # most positive achievable from suffix
        for i in range(k - 1, -1, -1):
            lo[i] = lo[i + 1] + min(c[2] for c in cand[i])
            hi[i] = hi[i + 1] + max(c[2] for c in cand[i])
        chosen = []

        def rec(i, acc):
            nonlocal tested
            tested += 1
            if acc + lo[i] > 0 or acc + hi[i] < 0:
                return
            if i == k:
                if acc == 0:
                    iv = sorted(chosen)
                    if all(iv[j][1] < iv[j + 1][0] for j in range(len(iv) - 1)):
                        found.append((S, iv))
                        print("   *** EXACT: S=%s blocks=%s" % (S, iv))
                return
            for c in cand[i]:
                chosen.append((c[0], c[1]))
                rec(i + 1, acc + c[2])
                chosen.pop()

        rec(0, Fraction(0))
    print("   combinations tested: %d ; exact cancellations with disjoint blocks: %d"
          % (tested, len(found)))
    return found


if __name__ == "__main__":
    error_table(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
    part_B(dmax=int(sys.argv[2]) if len(sys.argv) > 2 else 40,
           k_max=int(sys.argv[3]) if len(sys.argv) > 3 else 5,
           Lmax=int(sys.argv[4]) if len(sys.argv) > 4 else 5)
