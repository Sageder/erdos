"""
Q3 -- representability table.

For a list of targets rho and thresholds T we decide, EXACTLY:

   s=1 : is rho a single block sum with all elements >= T ?
         -- complete, no bound at all (blocks.blocks_with_sum).
   s<=2, s<=3 : is rho a sum of <= s disjoint blocks with elements >= T,
         where the s-1 largest blocks have length <= K ?
         -- complete for that class (q3_multiblock.represent).

Run:  python3 q3_table.py [K] [SMAX]
"""

import sys
import time
from fractions import Fraction

from blocks import blocks_with_sum
from q3_multiblock import represent, check

TARGETS = [
    Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5), Fraction(1, 6),
    Fraction(1, 7), Fraction(1, 8), Fraction(1, 10), Fraction(1, 12), Fraction(1, 15),
    Fraction(1, 20), Fraction(1, 24), Fraction(1, 30), Fraction(1, 35), Fraction(1, 36),
    Fraction(1, 42), Fraction(1, 60), Fraction(1, 100),
    Fraction(2, 3), Fraction(3, 4), Fraction(5, 12), Fraction(11, 2520),
    Fraction(1, 1), Fraction(6, 5), Fraction(19, 20), Fraction(5, 6), Fraction(7, 12),
]
THRESH = [2, 3, 5, 7, 10, 20, 50, 100]


def one(rho, T, smax, K, xmax=20000):
    """returns (s, solution) with the least s that works, or (None,None)"""
    sol1 = blocks_with_sum(rho, cmin=T)
    if sol1:
        return 1, sol1[0]
    for s in range(2, smax + 1):
        out = represent(rho, T, s, K, want=1, xmax=xmax)
        out = [o for o in out if len(o) == s]
        if out:
            check(out[0], rho, T)
            return s, out[0]
    return None, None


if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    XM = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
    SMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    print("Q3 representability table.  K=%d (max length of the non-final blocks), "
          "SMAX=%d, start-cap=%d" % (K, SMAX, XM))
    print("entries: s = fewest blocks found (complete for the stated class); "
          "'-' = provably none in that class")
    hdr = "%-12s" % "rho" + "".join("%7s" % ("T=%d" % T) for T in THRESH)
    print(hdr)
    for rho in TARGETS:
        row = "%-12s" % rho
        for T in THRESH:
            t0 = time.time()
            s, sol = one(rho, T, SMAX, K, XM)
            row += "%7s" % (s if s else "-")
        print(row, flush=True)
