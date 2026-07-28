"""
H_bound.py -- Route H, step 3: the exact modulus bound obtainable from
Lemma L5 (prime-removal reduction) + the strict reciprocal-sum inequality.

CLAIMS TESTED (all exact rational arithmetic):

  (T1) For every Y, let R(Y) be the L5-fixpoint of H ∩ [2,Y].
       If budget(R(Y)) <= 1 then H ∩ [2,Y] contains NO covering set at all.
  (T2) If budget(R(Y)) <= 2 then H ∩ [2,Y] contains no TWO DISJOINT covering sets,
       hence (parity equivalence) there is no covering system of Z with distinct
       moduli all in E and all <= 2Y.

  We locate the exact largest Y for which each conclusion is available, and print the
  resulting explicit theorem.

Inputs to the argument that are themselves theorems, proved in FINDINGS.md:
  * parity equivalence E <-> two disjoint H-sets;
  * Lemma L5;
  * Davenport-Mirsky-Newman-Rado: distinct moduli > 1 => sum of reciprocals > 1 (strict).

CONCLUSION: printed.
"""
from fractions import Fraction
from math import lcm
from sympy import isprime, factorint

from H_reduce import H_upto, reduce_set, budget, lcm_of


def main():
    best1 = None
    best2 = None
    rows = []
    prev = None
    for Y in range(2, 261):
        M = H_upto(Y)
        if not M:
            continue
        R, _ = reduce_set(M)
        b = budget(R)
        rows.append((Y, len(M), len(R), b))
        if b <= 1:
            best1 = (Y, R, b)
        if b <= 2:
            best2 = (Y, R, b)
        if prev is not None and b != prev:
            pass
        prev = b

    print("Y    |H<=Y|  |R(Y)|   budget(R(Y))")
    shown = 0
    for (Y, nH, nR, b) in rows:
        if Y % 5 == 0 or Y in (2, 3, 4, 6, 8, 9, 11, 14, 15, 125, 126, 127, 128, 129, 130):
            print("%-5d %-7d %-8d %s  = %.6f" % (Y, nH, nR, b, float(b)))
            shown += 1
    print()
    if best1:
        Y, R, b = best1
        print("(T1) largest Y with budget(R(Y)) <= 1 :  Y = %d,  R(Y) = %s, budget = %s = %.6f"
              % (Y, R, b, float(b)))
        print("     => THEOREM: no covering system with distinct moduli all in H and all <= %d." % Y)
        print("     => equivalently no covering system with distinct moduli all in E and all <= %d"
              % (2 * Y))
        print("        for EITHER parity class alone (each half of an E-system is such an H-system).")
    print()
    if best2:
        Y, R, b = best2
        print("(T2) largest Y with budget(R(Y)) <= 2 :  Y = %d" % Y)
        print("     R(Y) = %s" % (R,))
        print("     budget = %s = %.6f  <= 2" % (b, float(b)))
        print("     lcm(R(Y)) = %d = %s" % (lcm_of(R), factorint(lcm_of(R))))
        print()
        print("     ==> THEOREM T2: there is NO covering system of Z with distinct moduli all")
        print("         of the form p-1 (p prime >= 5) and all <= %d." % (2 * Y))
    # transition detail
    print()
    print("transition detail:")
    for Y in range(best2[0] - 3, best2[0] + 6):
        M = H_upto(Y)
        R, _ = reduce_set(M)
        print("   Y=%-4d |R|=%-4d budget=%.6f %s" % (Y, len(R), float(budget(R)),
              "<=2" if budget(R) <= 2 else ">2"))


if __name__ == "__main__":
    main()
