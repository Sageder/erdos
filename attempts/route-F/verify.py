#!/usr/bin/env python3
"""route-F INDEPENDENT verifier.  Imports nothing from the search code.

usage:  verify.py <target-rational> <n1> <n2> ... [--minelt T]
        verify.py <target-rational> --file FILE [--minelt T]

Checks, with fractions.Fraction only (no float anywhere):
  * every element is an integer >= 2
  * elements are pairwise distinct
  * no isolated point (n in U => n-1 in U or n+1 in U)
  * sum of 1/n equals the target EXACTLY
  * min element >= T if --minelt given
Prints run count r and capacity M.
"""
import sys
from fractions import Fraction


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    target = Fraction(argv[1])
    rest = argv[2:]
    minelt = None
    if "--minelt" in rest:
        i = rest.index("--minelt")
        minelt = int(rest[i + 1])
        rest = rest[:i] + rest[i + 2:]
    if "--file" in rest:
        i = rest.index("--file")
        fn = rest[i + 1]
        rest = rest[:i] + rest[i + 2:]
        with open(fn) as f:
            rest = rest + f.read().split()
    U = [int(x) for x in rest]

    ok = True
    if len(U) != len(set(U)):
        print("FAIL: repeated element")
        ok = False
    S = set(U)
    for n in U:
        if not isinstance(n, int) or n < 2:
            print("FAIL: element %r not an integer >= 2" % (n,))
            ok = False
    for n in S:
        if (n - 1) not in S and (n + 1) not in S:
            print("FAIL: isolated point %d" % n)
            ok = False
    tot = Fraction(0)
    for n in U:
        tot += Fraction(1, n)
    if tot != target:
        print("FAIL: sum = %s  != target %s" % (tot, target))
        ok = False
    if minelt is not None and min(U) < minelt:
        print("FAIL: min element %d < %d" % (min(U), minelt))
        ok = False

    # runs
    L = sorted(S)
    rr = []
    a = b = L[0]
    for n in L[1:]:
        if n == b + 1:
            b = n
        else:
            rr.append((a, b))
            a = b = n
    rr.append((a, b))
    r = len(rr)
    cap = sum((y - x + 1) // 2 for x, y in rr)
    for x, y in rr:
        if y == x:
            print("FAIL: run of length 1 at %d" % x)
            ok = False
    print("elements=%d  min=%d  max=%d  runs=%d  capacity=%d  sum=%s"
          % (len(U), min(U), max(U), r, cap, tot))
    print("VERIFIED OK" if ok else "VERIFICATION FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
