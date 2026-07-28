"""
D_04_sieve.py

CLAIM TESTED (this one is a genuine, complete, rigorous necessary condition):

  By Prop. D1, a covering system with distinct moduli in E is the same thing as two DISJOINT
  covering systems S_0, S_1 with distinct moduli in H = {m>=2 : 2m+1 prime}.  Put
  S = S_0 u S_1 and L = lcm(S).  Then

        budget(L) := sum_{m | L, m in H} 1/m  >=  sum_{m in S} 1/m
                   =  sum_{S_0} 1/m + sum_{S_1} 1/m  >=  1 + 1 = 2 .

  budget(.) is monotone under divisibility, so this rules out simultaneously every L' | L.

  This script computes budget(L) EXACTLY (float64, error < 1e-9) for EVERY L <= X by a sieve,
  and reports:
     - min{L : budget(L) >= 2}       -> unconditional lower bound for the H-world lcm
     - how many L <= X pass, and the maximal budget attained,
     - the list of divisor-maximal survivors (for the sharper Phi_q test in D_05).

CONCLUSION: printed at run time.
"""
import numpy as np
from sympy import isprime
import sys


def run(X, thresh=2.0, dump=None):
    print("sieving budget(L) = sum_{m|L, 2m+1 prime, m>=2} 1/m  for all L <= %d" % X)
    # H up to X
    sieve = np.ones(2 * X + 2, dtype=bool)
    sieve[:2] = False
    for p in range(2, int((2 * X + 2) ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    H = np.nonzero(sieve[5::2])[0]      # index i -> value 5+2i is prime
    H = (5 + 2 * H - 1) // 2            # m = (p-1)/2
    H = H[H >= 2]
    H = H[H <= X]
    print("   |H cap [2,%d]| = %d,  sum 1/m = %.6f" % (X, len(H), float(np.sum(1.0 / H))))

    bud = np.zeros(X + 1, dtype=np.float64)
    for m in H:
        bud[m::m] += 1.0 / m
    ok = np.nonzero(bud >= thresh)[0]
    print("   #{L <= %d : budget(L) >= %.1f} = %d" % (X, thresh, len(ok)))
    if len(ok):
        print("   smallest such L = %d  (budget %.6f)" % (ok[0], bud[ok[0]]))
        top = np.argsort(-bud)[:10]
        print("   top-10 L by budget:")
        for L in top:
            print("      L = %-10d budget = %.6f" % (L, bud[L]))
    # divisor-maximal survivors within [1,X]: L such that no multiple k*L <= X also passes
    if len(ok) and len(ok) < 4_000_000:
        okset = np.zeros(X + 1, dtype=bool)
        okset[ok] = True
        maximal = []
        for L in ok:
            k = 2
            m = False
            while k * L <= X:
                if okset[k * L]:
                    m = True
                    break
                k += 1
            if not m:
                maximal.append(int(L))
        print("   #divisor-maximal survivors <= %d : %d" % (X, len(maximal)))
        if dump:
            with open(dump, "w") as f:
                for L in maximal:
                    f.write("%d %.9f\n" % (L, bud[L]))
            print("   written to", dump)
    return bud


if __name__ == "__main__":
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7
    dump = sys.argv[2] if len(sys.argv) > 2 else None
    run(X, 2.0, dump)
