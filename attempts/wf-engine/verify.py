#!/usr/bin/env python3
"""
verify.py -- independent exact verification of SOL lines.

Reads lines "SOL n1 n2 ..." (any other line is ignored) from the files named on
the command line (or stdin) and checks, with fractions.Fraction only:
  * all n >= 2 and pairwise distinct,
  * no isolated point (n-1 in U or n+1 in U for every n in U),
  * sum 1/n == the target (default 1; override with --target u/v),
and prints run count r, capacity M = sum floor(L_i/2), min and max.

usage: verify.py [--target u/v] [--minelt T] file...
"""
import sys
from fractions import Fraction


def runs(U):
    U = sorted(U)
    out = []
    cur = [U[0]]
    for a, b in zip(U, U[1:]):
        if b == a + 1:
            cur.append(b)
        else:
            out.append(cur)
            cur = [b]
    out.append(cur)
    return out


def main():
    args = sys.argv[1:]
    target = Fraction(1)
    minelt = 2
    while args and args[0].startswith("--"):
        if args[0] == "--target":
            target = Fraction(args[1])
            del args[:2]
        elif args[0] == "--minelt":
            minelt = int(args[1])
            del args[:2]
        else:
            raise SystemExit("bad option " + args[0])
    lines = []
    if args:
        for fn in args:
            lines += open(fn).read().splitlines()
    else:
        lines = sys.stdin.read().splitlines()
    nok = nbad = 0
    seen = set()
    for ln in lines:
        p = ln.split()
        if not p or p[0] != "SOL":
            continue
        U = [int(x) for x in p[1:]]
        key = tuple(sorted(U))
        errs = []
        if len(set(U)) != len(U):
            errs.append("repeated element")
        if min(U) < max(2, minelt):
            errs.append(f"element below {max(2, minelt)}")
        S = set(U)
        iso = [n for n in U if (n - 1) not in S and (n + 1) not in S]
        if iso:
            errs.append(f"isolated points {iso}")
        s = sum(Fraction(1, n) for n in U)
        if s != target:
            errs.append(f"sum={s} != {target}")
        R = runs(U)
        if any(len(r) < 2 for r in R):
            errs.append("run of length 1")
        if errs:
            nbad += 1
            print("BAD  " + "; ".join(errs) + "  :: " + ln[:120])
        else:
            nok += 1
            dup = " DUP" if key in seen else ""
            seen.add(key)
            print(f"OK   |U|={len(U):3d} min={min(U):5d} max={max(U):5d} "
                  f"r={len(R):3d} cap={sum(len(r)//2 for r in R):3d} sum={s}{dup}")
    print(f"--- verified {nok} OK, {nbad} BAD, {len(seen)} distinct, target={target}")
    return 1 if nbad else 0


if __name__ == "__main__":
    sys.exit(main())
