#!/usr/bin/env python3
"""
verify.py -- independent exact re-verification of SOL lines.
Uses fractions.Fraction AND a second, Fraction-free integer check
(lcm * sum == numerator * lcm).  No floating point anywhere.

usage: verify.py [--target a/b] [--minelt T] FILE...
       (also reads stdin)
"""
import sys, os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import verify_solution, runs


def main():
    args = sys.argv[1:]
    target = Fraction(1)
    minelt = None
    if "--target" in args:
        k = args.index("--target"); target = Fraction(args[k + 1]); del args[k:k + 2]
    if "--minelt" in args:
        k = args.index("--minelt"); minelt = int(args[k + 1]); del args[k:k + 2]
    lines = []
    if args:
        for p in args:
            with open(p) as f:
                lines += f.readlines()
    else:
        lines = sys.stdin.readlines()
    n_ok = 0
    for line in lines:
        t = line.split()
        if not t:
            continue
        if t[0] == "SOL":
            t = t[1:]
        try:
            U = [int(x) for x in t]
        except ValueError:
            continue
        if not U:
            continue
        ok, info = verify_solution(U, target, minelt)
        print(("OK  " if ok else "FAIL") +
              f" |U|={len(U)} min={info['min']} max={info['max']} sum={info['sum']} "
              f"legal={info['legal']} int_check={info['int_ok']} r={info['r']} cap={info['cap']}")
        n_ok += ok
    print(f"verified {n_ok} / {sum(1 for l in lines if l.strip())} lines")


if __name__ == "__main__":
    main()
