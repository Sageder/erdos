"""
D_03_Lscan.py

CLAIM TESTED: how rich is  D_H(L) = {m : m | L, m >= 2, 2m+1 prime}  as L ranges over smooth
numbers?  The parity-split reduction (Prop. D1) says Erdos 273 = "two DISJOINT covering
systems with distinct moduli inside H".  A necessary condition is
        budget(L) := sum_{m in D_H(L)} 1/m  >= 2 ,
and, per half, the q-adic fiber density conditions must hold with threshold 1 for each half,
i.e. threshold 2 for the union.  This script:

  (a) scans all L = 2^a 3^b 5^c 7^d 11^e 13^f 17^g 19^h ... below a cap and reports the
      smallest L attaining budget >= 1, >= 1.5, >= 2, >= 2.5, >= 3;
  (b) for the best L found, prints D_H(L), the budget, and the per-prime "q-free budget"
      A_0(q) = sum_{m in D_H(L), q nmid m} 1/m  (if A_0(q) >= 2 the fiber condition at q is
      automatic);
  (c) reports the smallest L for which the *doubled* fiber conditions are automatic at every
      prime, i.e. min_q A_0(q) >= 2.

CONCLUSION: printed at run time.
"""
from sympy import isprime
from fractions import Fraction
import itertools, sys, heapq

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]


def divisors(fac):
    ds = [1]
    for p, e in fac.items():
        ds = [d * p ** i for d in ds for i in range(e + 1)]
    return ds


def DH(fac):
    return sorted(m for m in divisors(fac) if m >= 2 and isprime(2 * m + 1))


def budget(ds):
    return sum(1.0 / m for m in ds)


def qfree(ds, q):
    return sum(1.0 / m for m in ds if m % q != 0)


def scan(cap, maxprimes=8):
    """enumerate smooth L <= cap over the first maxprimes primes, return best budgets."""
    ps = PRIMES[:maxprimes]
    best = {}       # threshold -> (L, budget)
    thresholds = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    results = []

    def rec(i, L, fac):
        if i == len(ps):
            ds = DH(fac)
            b = budget(ds)
            results.append((b, L, dict(fac)))
            return
        p = ps[i]
        e = 0
        Lp = L
        while True:
            f2 = dict(fac)
            if e:
                f2[p] = e
            rec(i + 1, Lp, f2)
            e += 1
            if Lp * p > cap:
                break
            Lp *= p

    rec(0, 1, {})
    results.sort(key=lambda t: t[1])          # by L ascending
    print("scanned %d smooth L <= %d over primes %s" % (len(results), cap, ps))
    for th in thresholds:
        cand = [r for r in results if r[0] >= th]
        if cand:
            b, L, fac = min(cand, key=lambda t: t[1])
            print("   smallest L with budget >= %.1f :  L = %-12d budget = %.4f  fac = %s"
                  % (th, L, b, fac))
        else:
            print("   smallest L with budget >= %.1f :  none <= %d" % (th, cap))
    return results


def report(fac):
    L = 1
    for p, e in fac.items():
        L *= p ** e
    ds = DH(fac)
    b = budget(ds)
    print("\nL = %d = %s" % (L, fac))
    print("   #divisors = %d   |D_H(L)| = %d   budget = %.6f" % (len(divisors(fac)), len(ds), b))
    print("   D_H(L) =", ds if len(ds) <= 80 else str(ds[:80]) + " ...")
    print("   per-prime q-free budget A_0(q) (fiber condition at q is automatic iff >= 2):")
    for q in sorted(fac):
        print("      q=%-3d  A_0 = %.4f   #multiples of q in D_H = %d"
              % (q, qfree(ds, q), sum(1 for m in ds if m % q == 0)))
    return L, ds, b


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7
    res = scan(cap, maxprimes=8)
    # best budget overall
    res.sort(key=lambda t: -t[0])
    print("\ntop 10 smooth L <= %d by budget:" % cap)
    for b, L, fac in res[:10]:
        print("   L = %-14d budget = %.5f  fac = %s" % (L, b, fac))
    report(res[0][2])
    # smallest L with min_q A_0(q) >= 2
    ok = []
    for b, L, fac in res:
        if b < 2:
            continue
        ds = DH(fac)
        mq = min(qfree(ds, q) for q in fac)
        if mq >= 2:
            ok.append((L, b, mq, fac))
    ok.sort()
    print("\nsmallest smooth L <= %d with min_q A_0(q) >= 2 (all fiber conditions automatic):"
          % cap)
    if ok:
        for L, b, mq, fac in ok[:5]:
            print("   L = %-14d budget = %.4f  min_q A_0 = %.4f  fac = %s" % (L, b, mq, fac))
    else:
        print("   NONE -- at every smooth L <= %d some prime q has q-free budget < 2." % cap)
        # show the best attempt
        best = None
        for b, L, fac in res:
            ds = DH(fac)
            mq = min(qfree(ds, q) for q in fac) if fac else 0
            if best is None or mq > best[2]:
                best = (L, b, mq, fac)
        print("   best min_q A_0 achieved: %.4f at L = %d, fac = %s" % (best[2], best[0], best[3]))
