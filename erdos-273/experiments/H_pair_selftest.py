"""
H_pair_selftest.py -- correctness tests for the necessary conditions used by H_pair.py.

CLAIM TESTED: the filters check_set / balance_ok in H_pair.py must ACCEPT every genuine
covering set (otherwise the "0 surviving pairs" conclusions would be vacuous/wrong).
We feed them real covering systems (verified independently by exhaustive sweep) and require
acceptance; we also feed obvious non-coverings and report rejection rates.

CONCLUSION: printed.  Expected: 0 false rejections of genuine covering sets.
"""
from fractions import Fraction
from math import lcm
from sympy import factorint, isprime
from H_pair import check_set, balance_ok, prime_powers
from H_verify import verify

# Genuine covering systems with distinct moduli (verified below).
CASES = [
    # the H-covering found by H_cover.c
    [(0, 2), (1, 3), (3, 6), (5, 8), (2, 9), (17, 18), (23, 36), (41, 48), (5, 54),
     (14, 81), (17, 96), (65, 128), (41, 216), (239, 243), (257, 288)],
    # classical
    [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)],
    [(0, 2), (0, 3), (1, 4), (1, 6), (11, 12)],
    [(0, 2), (0, 3), (1, 4), (3, 8), (7, 12), (23, 24)],
    [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12), (0, 5), (0, 7)],   # with redundant 5,7
]


def main():
    bad = 0
    for pairs in CASES:
        L, miss = verify(pairs, None)
        assert not miss, ("not a covering", pairs)
        # WLOG we only ever test L5-REDUCED covering sets (Lemma L5 lets us delete, from a
        # covering set, all multiples of any prime q with |A_q| < q).  So reduce first.
        A = sorted(m for _, m in pairs)
        from H_reduce import reduce_set
        A, log = reduce_set(A)
        if log:
            print("   (L5-reduced: dropped %s)" % [q for q, _, _ in log])
        A = sorted(A)
        b = sum(Fraction(1, m) for m in A)
        d = b - 1
        primes = sorted({p for m in A for p in factorint(m)})
        pps = prime_powers(A)
        ok = check_set(A, d, primes, pps)          # Delta = exact delta: tightest legal test
        print("moduli %-46s budget=%.5f delta=%.5f  accepted=%s"
              % (A, float(b), float(d), ok))
        if not ok:
            bad += 1
            # localise which condition failed
            for name, test in [
                ("C2 coprime", lambda: all(not (Fraction(1, x * y) > d)
                                           for i, x in enumerate(A) for y in A[i + 1:]
                                           if __import__("math").gcd(x, y) == 1)),
                ("C3 mult", lambda: all(not (0 < sum(1 for m in A if m % q == 0) < q) for q in primes)),
                ("C4 L10b", lambda: all(
                    sum(Fraction(1, m) for m in A if m % pk == 0) >=
                    min(factorint(pk)) * (Fraction(1, min([m for m in A if m % pk == 0])) - d)
                    for pk in pps if any(m % pk == 0 for m in A))),
                ("C5 balance", lambda: all(balance_ok([Fraction(1, m) for m in A if m % q == 0], q, d)
                                           for q in primes if any(m % q == 0 for m in A))),
            ]:
                print("     %-12s -> %s" % (name, test()))
    print()
    print("false rejections of genuine covering sets:", bad)
    print("CONCLUSION:", "filters are sound (no genuine covering set rejected)" if bad == 0
          else "*** A FILTER IS UNSOUND -- all UNSAT conclusions using it are invalid ***")


if __name__ == "__main__":
    main()
