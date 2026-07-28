#!/usr/bin/env python3
"""Count legal subsets of a universe exactly (transfer-matrix DP) and report the
two quantities that decide whether GADGETS / SWITCHES can exist in a window:

  Lambda = log2 #{legal subsets of the pruned universe}
  lambda = log2( L / gcd(L,D) ),  L = lcm(universe)

heuristic:  gadgets (denom(Sigma) | D) need Lambda > lambda;
            switches (denom(Sigma(B)-Sigma(A)) | D) need 2*Lambda > lambda
            (birthday: there are ~2^{2 Lambda} ordered pairs).
Both are OBSERVATIONS/heuristics, not theorems.
"""
import sys
from math import gcd, log2
from fractions import Fraction
from lib import smallest_prime_factors
from universe import prune, lcm_of


def count_legal(U):
    """exact number of legal subsets of the integer set U (including empty)."""
    if not U:
        return 1
    k = len(U)
    s0, s1, s2 = 1, 0, 0          # before first element: 'not included' context
    # process element 0
    s0, s1, s2 = 1, 1, 0
    for i in range(1, k):
        adj = (U[i] == U[i - 1] + 1)
        n0 = n1 = n2 = 0
        if adj:
            n0 += s0 + s2
            n1 += s0
            n2 += s1 + s2
        else:
            n0 += s0 + s2
            n1 += s0 + s2
        s0, s1, s2 = n0, n1, n2
    return s0 + s2


def stats(x, y, D, cap=None, spf=None):
    if spf is None:
        spf = smallest_prime_factors(y + 2)
    A = prune(x, y, D, spf, prime_cap=cap)
    if not A:
        return dict(x=x, y=y, cap=cap, n=0, Lam=0.0, lam=0.0, maxsum=0.0)
    L = lcm_of(A)
    lam = (L // gcd(L, D)).bit_length()
    cnt = count_legal(A)
    Lam = log2(cnt) if cnt > 1 else 0.0
    ms = float(sum(Fraction(1, n) for n in A))
    return dict(x=x, y=y, cap=cap, n=len(A), Lam=Lam, lam=lam, maxsum=ms, U=A)


if __name__ == "__main__":
    x = int(sys.argv[1]); y = int(sys.argv[2]); D = int(sys.argv[3])
    caps = [int(c) for c in sys.argv[4].split(",")] if len(sys.argv) > 4 else [None]
    spf = smallest_prime_factors(y + 2)
    for cap in caps:
        s = stats(x, y, D, None if cap == 0 else cap, spf)
        print("[%d,%d] cap=%s |U|=%d Lambda=%.1f lambda=%d  Lam-lam=%.1f  2Lam-lam=%.1f  maxsum=%.4f"
              % (x, y, cap, s["n"], s["Lam"], s["lam"], s["Lam"] - s["lam"],
                 2 * s["Lam"] - s["lam"], s["maxsum"]))
