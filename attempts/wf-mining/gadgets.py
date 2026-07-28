#!/usr/bin/env python3
"""
GADGET MENU per prime in a far-out window, and bottom-heaviness of far-out solutions.

For a window [T,N] and a prime p, the (E=1) Rule-(P) admissible cofactor sets are
   Feas(p;T,N) = { A subset [ceil(T/p), floor(N/p)] : p | numerator(sum_{a in A} 1/a) },
where A = {} is allowed (p simply unused).  |Feas| - 1 is the size of the menu of
non-trivial p-gadgets that a solution in [T,N] may install.  Exact integer arithmetic.
"""
import sys
from math import gcd
from fractions import Fraction
from collections import Counter

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, stat
from mult import primes_upto


def feas_count(p, lo, hi):
    """#subsets A of [lo,hi] with p | numerator(sum 1/a), by DP over residues mod p."""
    if hi < lo:
        return 1
    L = 1
    for a in range(lo, hi + 1):
        L = L * a // gcd(L, a)
    # numerator over L is sum L/a ; p | numerator(lowest terms) iff
    # v_p(sum) >= 0 - ... ; with all a < p (typical) p does not divide L, so
    # p | numerator(lowest terms)  <=>  sum_{a in A} (L/a) = 0 mod p    (when p !| L)
    vp = 0
    LL = L
    while LL % p == 0:
        LL //= p
        vp += 1
    if vp:
        # rare: p divides some a in the window; fall back to exact enumeration
        cnt = 0
        n = hi - lo + 1
        if n > 22:
            return None
        for mask in range(1 << n):
            s = Fraction(0)
            for i in range(n):
                if mask >> i & 1:
                    s += Fraction(1, lo + i)
            if s == 0 or s.numerator % p == 0:
                cnt += 1
        return cnt
    dp = [0] * p
    dp[0] = 1
    for a in range(lo, hi + 1):
        w = (L // a) % p
        nd = dp[:]
        for r in range(p):
            if dp[r]:
                nd[(r + w) % p] += dp[r]
        dp = nd
    return dp[0]


if __name__ == "__main__":
    print("=== gadget menu size per prime in the window [T, N] ===")
    for T, N in [(50, 369), (100, 740), (200, 1480)]:
        print("\n  window [%d,%d]  (N/T = %.2f)" % (T, N, N / T))
        print("    p    window of cofactors   #subsets   #admissible   share")
        tot_log = 0.0
        for p in primes_upto(N // 2):
            lo, hi = -(-T // p), N // p
            if hi < lo:
                continue
            n = hi - lo + 1
            if p == 2 or n > 40:
                continue
            f = feas_count(p, lo, hi)
            if f is None:
                continue
            if p < 11 and n > 30:
                continue
            print("   %4d   [%3d,%4d] (%2d)      2^%-3d      %-12d  %.5f"
                  % (p, lo, hi, n, n, f, f / 2 ** n))
            if p >= 3:
                tot_log += (f / 2 ** n)
        print("    (share ~ 1/p is the heuristic prediction for p not dividing the lcm)")

    # ---------- bottom-heaviness ------------------------------------
    print("\n=== bottom-heaviness of far-out solutions ===")
    S = load()
    print("   T   N     |U|   |U cap [T,2T]|   mass on [T,2T]   mass on [T,3T]   density on [T,1.3T]")
    seen = set()
    for U in sorted(S, key=lambda u: u[0]):
        T, N = U[0], U[-1]
        if T in seen or T < 20:
            continue
        seen.add(T)
        c2 = [n for n in U if n <= 2 * T]
        m2 = sum(Fraction(1, n) for n in c2)
        m3 = sum(Fraction(1, n) for n in U if n <= 3 * T)
        w = [n for n in U if n <= 1.3 * T]
        print("  %3d %4d %5d %10d        %.4f          %.4f           %.3f"
              % (T, N, len(U), len(c2), float(m2), float(m3),
                 len(w) / (int(1.3 * T) - T + 1)))
