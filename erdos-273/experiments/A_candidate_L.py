"""
A_candidate_L.py

CLAIM TESTED: enumerate EVERY L <= X (not just smooth ones) for which the density bound
        B_E(L) = sum_{n | L, n in E} 1/n  >  1
holds.  Every other L is UNSAT for Erdos 273 outright: a covering system with moduli in E
and lcm dividing L would need sum of reciprocals >= 1, and by Davenport-Mirsky-Newman-Rado
(no exact cover by distinct moduli > 1) the inequality is strict.

Implementation: a numpy sieve.  For each n in E with n <= X add 1/n to every multiple of n.
Exact enough: the accumulation is done in float128/float64 and every candidate that comes
out within 1e-9 of the threshold is re-checked in exact Fraction arithmetic.

Also reports, for each candidate, the number of E-divisors and sum of E-divisors (= number
of Boolean variables in the direct SAT encoding), i.e. the cost of deciding it.

CONCLUSION: printed list; used to drive A_sat_cover.py runs.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import is_prime, D_E, budget
from fractions import Fraction

if __name__ == "__main__":
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 2 * 10 ** 6
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    B = np.zeros(X + 1, dtype=np.float64)
    Ecount = np.zeros(X + 1, dtype=np.int32)
    for n in range(4, X + 1):
        if is_prime(n + 1):
            B[n::n] += 1.0 / n
            Ecount[n::n] += 1
    idx = np.nonzero(B > 1.0 - 1e-9)[0]
    print(f"X = {X}: {len(idx)} values of L with B_E(L) > 1 - eps")
    rows = []
    for L in idx:
        L = int(L)
        if L < lo:
            continue
        d = D_E(L)
        b = budget(d)
        if b <= 1:
            continue
        rows.append((L, len(d), float(b), sum(d)))
    print(f"exactly-verified: {len(rows)}")
    print(f"{'L':>10} {'#E-div':>7} {'B_E':>8} {'sum(n)=#vars':>13} {'L*k lits':>12}")
    for L, k, b, s in rows:
        print(f"{L:>10} {k:>7} {b:>8.5f} {s:>13} {L*k:>12}")
