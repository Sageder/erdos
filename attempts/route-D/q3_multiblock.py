"""
Q2 / Q3 -- COMPLETE search for representations

      rho = H(a_1,b_1) + ... + H(a_s,b_s),   blocks pairwise disjoint,
      all elements >= T,

with s <= SMAX blocks, where the s-1 LARGEST block sums are required to come
from blocks of length <= K (the smallest one is unrestricted).

WHY THIS IS COMPLETE (for that class).  Order the blocks so that
H_1 >= H_2 >= ... >= H_s.  Then for every j,
      rho_j := rho - (H_1+...+H_{j-1})   satisfies   H_j >= rho_j/(s-j+1),
and also H_j <= H_{j-1} and H_j <= rho_j.  With k_j the length,
      k_j/b_j <= H_j <= k_j/a_j
gives the explicit two-sided bound
      k_j/rho_j - k_j + 1  <=  a_j  <=  (s-j+1) k_j / rho_j .
So each level is a finite enumeration.  At the LAST block we do not need any
length bound at all: blocks.blocks_with_sum solves H(c,d) = r completely.

Everything exact.

Run:
   python3 q3_multiblock.py 1/20 7 3 8
   python3 q3_multiblock.py unitscan 60 3 6 2
"""

import sys
from fractions import Fraction

from blocks import H, blocks_with_sum


def _disjoint_all(bs):
    bs = sorted(bs)
    for i in range(len(bs) - 1):
        if bs[i][1] >= bs[i + 1][0]:
            return False
    return True


def represent(rho, T, smax, K, want=1, stats=None, xmax=None):
    """
    All representations of rho by <= smax disjoint blocks with elements >= T,
    where all but the LAST (smallest) block have length <= K and start <= xmax.
    The last block is unrestricted (solved by the complete blocks_with_sum).
    xmax=None means no extra restriction (the natural bound left*k/r is used).
    """
    rho = Fraction(rho)
    out = []
    trunc = [False]

    def rec(r, left, hcap, chosen):
        # r > 0 still to be written as `left` blocks each with sum <= hcap
        if left == 0:
            return False
        # option: finish with ONE last block (complete solver, any length)
        if r <= hcap:
            for B in blocks_with_sum(r, cmin=T, stats=stats):
                if H(*B) <= hcap and _disjoint_all(chosen + [B]):
                    out.append(sorted(chosen + [B]))
                    if len(out) >= want:
                        return True
        if left == 1:
            return False
        # otherwise pick the current largest block
        for k in range(2, K + 1):
            lo = (k * r.denominator) // r.numerator - k + 1          # k/r - k + 1
            hi = (left * k * r.denominator) // r.numerator           # left*k/r
            lo = max(lo, T, 2)
            if xmax is not None and hi > xmax:
                hi = xmax
                trunc[0] = True
            if lo > hi:
                continue
            h = None
            for a in range(lo, hi + 1):
                b = a + k - 1
                if h is None:
                    h = H(a, b)
                else:
                    h = h - Fraction(1, a - 1) + Fraction(1, b)
                if h > min(hcap, r):
                    continue
                if h * left < r:
                    break            # h decreasing in a: no chance any more
                nxt = chosen + [(a, b)]
                if not _disjoint_all(nxt):
                    continue
                if rec(r - h, left - 1, h, nxt):
                    return True
        return False

    rec(rho, smax, rho, [])
    if stats is not None and trunc[0]:
        stats['truncated'] = True
    return out


def check(sol, rho, T):
    assert _disjoint_all(sol)
    assert min(a for a, b in sol) >= T
    s = sum((H(a, b) for a, b in sol), Fraction(0))
    assert s == Fraction(rho), (s, rho)
    return True


if __name__ == "__main__":
    if sys.argv[1] == "unitscan":
        NMAX = int(sys.argv[2])
        SMAX = int(sys.argv[3])
        K = int(sys.argv[4])
        T = int(sys.argv[5]) if len(sys.argv) > 5 else 2
        stats = {}
        for N in range(2, NMAX + 1):
            sols = represent(Fraction(1, N), T, SMAX, K, want=1, stats=stats)
            if sols:
                for s in sols:
                    check(s, Fraction(1, N), T)
                print("  1/%d = %s" % (N, sols))
        print("scan finished: 1/N for 2<=N<=%d, <=%d blocks, big blocks length<=%d,"
              " T=%d.  stats=%s" % (NMAX, SMAX, K, T, stats))
    else:
        rho = Fraction(sys.argv[1])
        T = int(sys.argv[2])
        smax = int(sys.argv[3])
        K = int(sys.argv[4])
        want = int(sys.argv[5]) if len(sys.argv) > 5 else 3
        stats = {}
        sols = represent(rho, T, smax, K, want=want, stats=stats)
        print("rho=%s T=%d smax=%d K=%d -> %d solutions  stats=%s"
              % (rho, T, smax, K, len(sols), stats))
        for s in sols:
            check(s, rho, T)
            print("   ", s)
