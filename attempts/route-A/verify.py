#!/usr/bin/env python3
"""
INDEPENDENT CERTIFICATE VERIFIER  (route-A)

Claim tested: a given finite multiset/list of integers U is a valid certificate for
Erdos #289, i.e.

    (V1)  every element of U is an integer >= 2
    (V2)  the elements of U are pairwise distinct
    (V3)  U has no isolated point:  for every n in U, (n-1) in U or (n+1) in U
          <=> U is a disjoint union of blocks of consecutive integers of length >= 2
    (V4)  sum_{n in U} 1/n == 1   EXACTLY in Q   (fractions.Fraction only, no floats)

It also prints the maximal runs, their lengths L_i, r = #runs and
M = sum_i floor(L_i/2)  (so that P(k) holds exactly for r <= k <= M).

This file deliberately shares NO code with any search script.

usage:  python3 verify.py  cert.txt        (whitespace/comma separated integers)
        python3 verify.py  --list 2 3 7 8  (integers on the command line)
"""
import sys
from fractions import Fraction


def maximal_runs(U):
    U = sorted(U)
    runs = []
    cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append((cur[0], cur[-1]))
            cur = [x]
    runs.append((cur[0], cur[-1]))
    return runs


def verify(U, verbose=True):
    ok = True
    msgs = []

    if len(U) == 0:
        return False, ["empty set"], None

    # V2 distinctness
    if len(set(U)) != len(U):
        ok = False
        msgs.append("FAIL V2: repeated elements")
    S = sorted(set(U))

    # V1
    bad = [n for n in S if not (isinstance(n, int) and n >= 2)]
    if bad:
        ok = False
        msgs.append("FAIL V1: elements not integers >= 2: %r" % (bad[:10],))
    else:
        msgs.append("OK  V1: all %d elements are integers >= 2 (min=%d, max=%d)"
                    % (len(S), S[0], S[-1]))

    # V3 no isolated point
    Sset = set(S)
    iso = [n for n in S if (n - 1) not in Sset and (n + 1) not in Sset]
    if iso:
        ok = False
        msgs.append("FAIL V3: isolated points %r" % (iso[:10],))
    else:
        msgs.append("OK  V3: no isolated point")

    # V4 exact sum
    tot = Fraction(0)
    for n in S:
        tot += Fraction(1, n)
    if tot == 1:
        msgs.append("OK  V4: sum_{n in U} 1/n == 1 exactly")
    else:
        ok = False
        msgs.append("FAIL V4: sum = %s  (as a Fraction)" % (tot,))

    runs = maximal_runs(S)
    L = [b - a + 1 for a, b in runs]
    r = len(runs)
    M = sum(l // 2 for l in L)
    info = dict(runs=runs, lengths=L, r=r, M=M, total=tot)

    if verbose:
        for m in msgs:
            print(m)
        print("maximal runs (%d):" % r)
        for (a, b) in runs:
            print("   [%d,%d]  length %d" % (a, b, b - a + 1))
        print("lengths      :", L)
        print("r = #runs    :", r)
        print("M = sum floor(L_i/2) :", M)
        if ok:
            print("=> P(k) holds for every k with %d <= k <= %d" % (r, M))
        print("VERDICT:", "VALID CERTIFICATE" if ok else "NOT A CERTIFICATE")
    return ok, msgs, info


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--list":
        U = [int(x) for x in args[1:]]
    else:
        txt = open(args[0]).read()
        for ch in ",;[]{}()\n\t":
            txt = txt.replace(ch, " ")
        U = [int(x) for x in txt.split()]
    ok, _, _ = verify(U)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
