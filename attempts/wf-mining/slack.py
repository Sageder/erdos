#!/usr/bin/env python3
"""
FEASIBILITY SLACK of the far-out window.

For a range [T,N], build the Rule-(P)+legality fixpoint A(T,N) (experiments/universe_range.py,
which only ever deletes elements that cannot lie in ANY solution inside [T,N]).  Then

    H(A(T,N)) = sum_{n in A} 1/n     (exact Fraction)

is an upper bound for the reciprocal sum of any solution inside [T,N].  So
      H(A(T,N)) < 1  ==>  NO solution with min>=T, max<=N.        (rigorous)
and the size of H(A)-1 measures how much room a far-out search actually has.

Prints, for each T, the least N on a grid with H(A) >= 1 (the "harmonic threshold"),
and the slack profile.
"""
import sys
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/experiments")
from universe_range import prune

if __name__ == "__main__":
    Ts = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else \
        [10, 20, 30, 40, 50, 60, 80, 100]
    print("  T     N   |A|   |[T,N]|  H(A) exact-as-float   H([T,N])   ratio N/T")
    for T in Ts:
        N = T * 3
        prev = None
        while N <= T * 14:
            A = prune(T, N)
            H = sum(Fraction(1, n) for n in A)
            Hfull = sum(Fraction(1, n) for n in range(T, N + 1))
            print("%4d %5d %5d %8d   %10.5f        %8.5f   %6.3f  %s"
                  % (T, N, len(A), N - T + 1, float(H), float(Hfull), N / T,
                     "H>=1" if H >= 1 else ""))
            if H >= 1 and prev is None:
                prev = N
            N = int(N * 1.15) + 1
        print("   -> least grid N with H(A)>=1 :", prev, " (N/T = %.3f)" % (prev / T) if prev else "none")
