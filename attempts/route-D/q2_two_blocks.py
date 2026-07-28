"""
Q2.  Two blocks:  for which N is  1/N = H(a,b) + H(c,d)  with disjoint blocks?

COMPLETE ALGORITHM (rigorous, no element bound), parameterised by K:
  order the two blocks so that H_1 >= H_2.  Then
        1/(2N) <= H_1 < 1/N .
  If k_1 = b-a+1 then  k_1/b <= H_1 <= k_1/a, hence
        a <= k_1/H_1 <= 2 N k_1        and      b >= k_1/H_1 > k_1 N,
  so   k_1 (N-1) + 1 <= a <= 2 N k_1 .
  Thus for every fixed length k_1 the first block ranges over an explicit
  finite set.  Given block 1, the second block must have sum exactly
  r = 1/N - H_1 and is then found COMPLETELY by blocks_with_sum(r) (which needs
  no element bound at all -- see blocks.py).  Disjointness is checked directly.

  The only unbounded parameter is k_1; the search below is complete for
  k_1 <= K.   Note (2-adic lemma) k_1 <= 2^(t_1+1)-1 where t_1 = -v_2(H_1);
  when v_2(N) = T2 >= 1 and the two blocks have DIFFERENT 2-levels, one has
  max(t_1,t_2) = T2 and both k_i <= 2^(T2+1)-1, so K = 2^(T2+1)-1 is already
  complete for that case.  In particular for N odd, no such splitting exists:
  the two blocks must have EQUAL 2-level.

Also included: a direct pair scan over all pairs of disjoint blocks with all
elements <= X, testing whether the sum is (i) a unit fraction, (ii) itself a
single block sum.

Run:  python3 q2_two_blocks.py unit 60 20
      python3 q2_two_blocks.py pairs 90
"""

import sys
from fractions import Fraction

from blocks import H, blocks_with_sum, v2


def disjoint(B1, B2):
    (a, b), (c, d) = B1, B2
    return b < c or d < a


def unit_two_blocks(N, K, stats=None):
    """complete for k_1 <= K; returns list of (block1, block2)"""
    target = Fraction(1, N)
    half = Fraction(1, 2 * N)
    sols = []
    for k in range(2, K + 1):
        alo = max(2, k * (N - 1) + 1)
        ahi = 2 * N * k
        h = None
        for a in range(alo, ahi + 1):
            b = a + k - 1
            if h is None:
                h = H(a, b)
            else:
                h = h - Fraction(1, a - 1) + Fraction(1, b)
            if h >= target:
                continue
            if h < half:
                break                    # H decreasing in a
            r = target - h
            for B2 in blocks_with_sum(r, cmin=2, stats=stats):
                if disjoint((a, b), B2):
                    sols.append(((a, b), B2))
    return sols


def all_blocks(X, hcap=Fraction(1)):
    out = []
    for a in range(2, X):
        h = Fraction(1, a)
        for b in range(a + 1, X + 1):
            h += Fraction(1, b)
            if h > hcap:
                break
            out.append((a, b, h))
    return out


def pair_scan(X, hcap=Fraction(1, 1)):
    """all pairs of disjoint blocks with elements <= X; report notable sums"""
    B = all_blocks(X, hcap)
    B.sort(key=lambda t: t[0])
    units = []
    isblock = []
    n = len(B)
    for i in range(n):
        a1, b1, h1 = B[i]
        for j in range(n):
            a2, b2, h2 = B[j]
            if a2 <= b1 + 0:      # need b1 < a2
                continue
            s = h1 + h2
            if s.numerator == 1:
                units.append(((a1, b1), (a2, b2), s))
            if s <= Fraction(5, 6):
                sol = blocks_with_sum(s)
                if sol:
                    isblock.append(((a1, b1), (a2, b2), s, sol))
    return len(B), units, isblock


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "unit":
        NMAX = int(sys.argv[2])
        K = int(sys.argv[3])
        stats = {}
        allsol = []
        for N in range(2, NMAX + 1):
            sols = unit_two_blocks(N, K, stats)
            if sols:
                print("  N=%d :" % N, sols)
                allsol.extend(sols)
        print("1/N = H(a,b)+H(c,d), complete for larger-sum block length <= %d, "
              "2 <= N <= %d" % (K, NMAX))
        print("   solutions:", allsol if allsol else "NONE")
        print("   solver stats:", stats)
    elif cmd == "pairs":
        X = int(sys.argv[2])
        nb, units, isblock = pair_scan(X)
        print("pairs of disjoint blocks with elements <= %d  (%d blocks)" % (X, nb))
        print("   sums that are unit fractions :", units if units else "NONE")
        print("   sums that are again a single block sum :",
              isblock if isblock else "NONE")
