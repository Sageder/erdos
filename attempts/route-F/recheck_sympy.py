#!/usr/bin/env python3
"""Second, independent arithmetic path: re-verify every certificate with
sympy.Rational (not fractions.Fraction) and pure-integer lcm arithmetic."""
import sys, sympy
from sympy import Rational, ilcm

cases = [("cert_T200_third.txt", Rational(1, 3), 200),
         ("cert_T500_sixth.txt", Rational(1, 6), 500),
         ("cert_T200_one.txt", Rational(1), 2),
         ("cert_T500_one.txt", Rational(1), 2),
         ("one_2_3.txt", Rational(2, 3), 2),
         ("one_1_2.txt", Rational(1, 2), 2)]
ok = True
for fn, tgt, mn in cases:
    U = [int(t) for t in open(fn).read().split()]
    assert len(U) == len(set(U))
    S = set(U)
    iso = [n for n in S if (n - 1) not in S and (n + 1) not in S]
    s = sum(Rational(1, n) for n in U)
    # third path: pure integer
    L = 1
    for n in U:
        L = ilcm(L, n)
    num = sum(L // n for n in U)
    good = (s == tgt) and not iso and min(U) >= mn and all(n >= 2 for n in U) \
        and Rational(num, L) == tgt
    ok &= good
    print("%-24s n=%-4d min=%-5d max=%-5d sum=%s  %s"
          % (fn, len(U), min(U), max(U), s, "OK" if good else "FAILED"))
print("ALL OK" if ok else "SOME FAILED")
