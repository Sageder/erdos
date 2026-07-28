#!/usr/bin/env python3
"""
verify.py -- INDEPENDENT exact verifier for route E.

Written from scratch (does not import anything from routes A-D).  Reads a
certificate as a list of integers and checks, with exact rational arithmetic
only (fractions.Fraction; no floats anywhere):

  (1) every element is an integer >= 2  (>= T if a bound T is supplied);
  (2) the elements are pairwise distinct;
  (3) NO ISOLATED POINT: every n in U has n-1 in U or n+1 in U;
  (4) sum_{n in U} 1/n equals the claimed target exactly;
  (5) prints the maximal runs, the run count r, the capacity
      cap = sum floor(L_i/2), and the interval [r,cap] of realisable block
      counts k.

usage:
    python3 verify.py "u/v" n1 n2 n3 ...
    python3 verify.py --file FILE "u/v"     # every line "SOL n1 n2 ..." checked
    python3 verify.py --file FILE "u/v" --minelt T
"""
import sys
from fractions import Fraction


def runs_of(U):
    """maximal runs of consecutive integers of the sorted set U"""
    U = sorted(U)
    out = []
    i = 0
    while i < len(U):
        j = i
        while j + 1 < len(U) and U[j + 1] == U[j] + 1:
            j += 1
        out.append((U[i], U[j]))
        i = j + 1
    return out


def check(U, target, minelt=2, quiet=False):
    """returns (ok, message).  target is a Fraction."""
    msgs = []
    if len(U) != len(set(U)):
        return False, "elements not distinct"
    S = set(U)
    for n in U:
        if not isinstance(n, int):
            return False, f"non-integer element {n!r}"
        if n < 2:
            return False, f"element {n} < 2"
        if n < minelt:
            return False, f"element {n} < required minimum {minelt}"
    for n in U:
        if (n - 1) not in S and (n + 1) not in S:
            return False, f"isolated point {n}"
    s = Fraction(0)
    for n in sorted(S):
        s += Fraction(1, n)
    if s != target:
        return False, f"sum {s} != target {target}"
    R = runs_of(S)
    for (a, b) in R:
        if b - a + 1 < 2:
            return False, f"run [{a},{b}] has length < 2"
    r = len(R)
    cap = sum((b - a + 1) // 2 for (a, b) in R)
    if not quiet:
        msgs.append("OK  sum=%s  |U|=%d  min=%d  max=%d" % (s, len(S), min(S), max(S)))
        msgs.append("    runs: " + " ".join("[%d,%d]" % (a, b) for (a, b) in R))
        msgs.append("    lengths: " + " ".join(str(b - a + 1) for (a, b) in R))
        msgs.append("    r=%d  cap=%d  ->  realisable block counts k in [%d,%d]" % (r, cap, r, cap))
    return True, "\n".join(msgs)


def parse_target(s):
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(int(s))


def main():
    args = sys.argv[1:]
    minelt = 2
    if "--minelt" in args:
        i = args.index("--minelt")
        minelt = int(args[i + 1])
        del args[i:i + 2]
    if args and args[0] == "--file":
        fn = args[1]
        target = parse_target(args[2])
        nok = nbad = 0
        for line in open(fn):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            toks = line.split()
            if toks[0] in ("SOL", "sol"):
                toks = toks[1:]
            try:
                U = [int(t) for t in toks]
            except ValueError:
                continue
            ok, msg = check(U, target, minelt, quiet=True)
            if ok:
                nok += 1
            else:
                nbad += 1
                print("BAD:", line[:80], "->", msg)
        print(f"verified {nok} certificates OK, {nbad} bad, target={target}, minelt>={minelt}")
        return 0 if nbad == 0 else 1
    target = parse_target(args[0])
    U = [int(t) for t in args[1:]]
    ok, msg = check(U, target, minelt)
    print(msg if ok else "FAIL: " + msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
