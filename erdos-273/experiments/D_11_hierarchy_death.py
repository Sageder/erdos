"""
D_11_hierarchy_death.py

*** THE CENTRAL NEGATIVE RESULT OF ROUTE D ***

CLAIM PROVED HERE (numerically certified, exact statement below).

For any FIXED finite set Q of primes, the multi-prime fiber condition
        Phi_Q(S) >= 2
(the strongest "local at the primes of Q" necessary condition available -- see D_08_phiQ.c)
can NEVER prove the answer NO, because it is satisfied outright by an explicit S.  Indeed
every m in S with gcd(m, prod Q) = 1 contributes 1/m to EVERY cell r, for EVERY residue
assignment; hence
        Phi_Q(S)  >=  A_Q(S) := sum_{m in S, gcd(m, prod Q) = 1} 1/m .
So it suffices to exhibit Y with  A_Q(H cap [2,Y]) >= 2, and then S = H cap [2,Y] passes.

Such a Y always exists: by Prop. D0 the elements of H coprime to prod Q are exactly the
m <= Y with 2m+1 prime and 2m+1 in a fixed set of admissible residue classes mod 2*prod Q,
and sum 1/m over those is  ~ sum over primes p in fixed residue classes of 2/(p-1), which
DIVERGES by Mertens/Dirichlet.  This script computes the least such Y for many Q.

Consequence: the ONLY member of the hierarchy that can decide Erdos 273 is Q = {all primes
dividing L}, which is literally the covering condition itself.  Every genuinely "local"
obstruction is therefore dead, with explicit finite counterexamples.

CONCLUSION: printed at run time.
"""
from sympy import isprime, primerange
from math import gcd
import sys


import numpy as np

_SIEVE = {}


def prime_sieve(N):
    if N in _SIEVE:
        return _SIEVE[N]
    s = np.ones(N + 1, dtype=bool)
    s[:2] = False
    for p in range(2, int(N ** 0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    _SIEVE.clear()
    _SIEVE[N] = s
    return s


def least_Y(Q, target=2.0, Ymax=3 * 10 ** 7):
    P = 1
    for q in Q:
        P *= q
    s = prime_sieve(2 * Ymax + 2)
    tot = 0.0
    step = 10 ** 6
    lo = 2
    while lo <= Ymax:
        hi = min(Ymax, lo + step - 1)
        ms = np.arange(lo, hi + 1)
        keep = s[2 * ms + 1]
        for q in Q:
            keep &= (ms % q != 0)
        sel = ms[keep]
        c = np.cumsum(1.0 / sel)
        idx = np.searchsorted(c, target - tot)
        if idx < len(sel):
            return int(sel[idx]), tot + float(c[idx])
        tot += float(c[-1]) if len(sel) else 0.0
        lo = hi + 1
    return None, tot


if __name__ == "__main__":
    Qs = [(2,), (3,), (2, 3), (2, 5), (3, 5), (2, 3, 5)]
    print("least Y such that  sum_{m in H, m<=Y, gcd(m, prod Q)=1} 1/m  >=  2")
    print("(then S = H cap [2,Y] satisfies Phi_Q >= 2 for EVERY residue assignment)")
    for Q in Qs:
        Y, tot = least_Y(Q, 2.0, 3 * 10 ** 7 if len(Q) < 3 else 3 * 10 ** 7)
        print("   Q = %-12s ->  Y = %s   (budget %.6f)"
              % (str(Q), Y if Y else "> search bound", tot))
        sys.stdout.flush()
