#!/usr/bin/env python3
"""
pool.py -- collect a POOL of gadgets in a window.

A gadget in the window [T,N] is a legal set W (no isolated point) with all
elements in [T,N] whose reciprocal sum is a/D for an integer a.  This driver
prunes the window (prune.py, gadget mode), runs ./gadget in randomised-restart
mode for a while with several seeds, RE-VERIFIES every gadget from scratch in
exact rational arithmetic (fractions.Fraction: sum recomputed, legality
rechecked, all elements inside the window, denominator divides D), and writes
one representative per distinct value.

Output lines:  a D n1 n2 ... nk        meaning  sum 1/n_i = a/D  exactly.

usage: pool.py T N D secs [-lo a/b] [-hi a/b] [-seeds k] [-B budget] [-o file]
"""
import os
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def check(U, D, T, N):
    if len(set(U)) != len(U):
        return None
    if min(U) < T or max(U) > N:
        return None
    S = set(U)
    if any((n - 1) not in S and (n + 1) not in S for n in U):
        return None
    s = sum(Fraction(1, n) for n in U)
    if D % s.denominator != 0:
        return None
    return s


def build_pool(T, N, D, secs, lo, hi, seeds=4, budget=2000000, probfile=None, verbose=True):
    import prune as PR
    A = PR.prune(T, N, 1, D, gadget=True, minval=Fraction(lo))
    if not A:
        return {}, []
    probfile = probfile or os.path.join(HERE, f"pool_{T}_{N}_{D}.prob")
    with open(probfile, "w") as f:
        f.write(f"{T} {N} 1 {D}\n{len(A)}\n" + " ".join(map(str, A)) + "\n")
    best = {}
    for seed in range(1, seeds + 1):
        p = subprocess.run([os.path.join(HERE, "gadget"), probfile,
                            "-lo", str(lo), "-hi", str(hi),
                            "-R", str(seed), "-B", str(budget), "-t", str(secs)],
                           capture_output=True, text=True)
        for line in p.stdout.splitlines():
            t = line.split()
            if not t or t[0] != "G":
                continue
            a, DD = int(t[1]), int(t[2])
            U = [int(x) for x in t[3:]]
            s = check(U, DD, T, N)
            if s is None or s != Fraction(a, DD):
                print("REJECTED (failed exact re-verification):", line[:80], file=sys.stderr)
                continue
            if a not in best or len(U) < len(best[a]):
                best[a] = U
        if verbose:
            print(f"  [{T},{N}] seed {seed}: pool {len(best)}", flush=True)
    return best, A


def main():
    args = sys.argv[1:]
    lo, hi, seeds, budget, out = "0", "1", 4, 2000000, None
    i = 4
    while i < len(args):
        if args[i] == "-lo": lo = args[i + 1]; i += 2
        elif args[i] == "-hi": hi = args[i + 1]; i += 2
        elif args[i] == "-seeds": seeds = int(args[i + 1]); i += 2
        elif args[i] == "-B": budget = int(args[i + 1]); i += 2
        elif args[i] == "-o": out = args[i + 1]; i += 2
        else: raise SystemExit("bad option " + args[i])
    T, N, D, secs = int(args[0]), int(args[1]), int(args[2]), float(args[3])
    best, A = build_pool(T, N, D, secs, lo, hi, seeds, budget)
    print(f"[{T},{N}] D={D} |universe|={len(A)} distinct gadget values={len(best)}")
    if best:
        vs = sorted(best)
        print(f"   value range {Fraction(vs[0],D)} .. {Fraction(vs[-1],D)} "
              f"({float(vs[0])/D:.5f} .. {float(vs[-1])/D:.5f})")
    if out:
        with open(out, "w") as f:
            for a in sorted(best):
                f.write(f"{a} {D} " + " ".join(map(str, best[a])) + "\n")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
