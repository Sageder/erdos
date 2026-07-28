#!/usr/bin/env python3
"""
Build a canonical, EXACTLY VERIFIED corpus of solutions (legal U with sum 1/n = 1)
from every file in the repository that emits "SOL n1 n2 ..." lines.

Exact rational arithmetic only (fractions.Fraction).  Every line is re-verified
from scratch: elements integers >= 2, distinct, no isolated point, sum == 1.
Anything that fails is reported and dropped.

Writes  attempts/wf-mining/CORPUS.txt  (one canonical sorted solution per line,
space separated, no "SOL" prefix), sorted by (max, min, tuple).
"""
import os
import sys
from fractions import Fraction

ROOT = "/home/user/erdos"


def runs_of(U):
    runs, cur = [], [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append(cur)
            cur = [x]
    runs.append(cur)
    return runs


def is_solution(U, target=Fraction(1)):
    """Exact check.  Returns (ok, reason)."""
    if len(U) != len(set(U)):
        return False, "repeat"
    if not all(isinstance(n, int) and n >= 2 for n in U):
        return False, "elt<2"
    U = sorted(U)
    s = Fraction(0)
    for n in U:
        s += Fraction(1, n)
    if s != target:
        return False, "sum=%s" % s
    S = set(U)
    if not all((n - 1 in S) or (n + 1 in S) for n in U):
        return False, "isolated"
    return True, "ok"


def gather():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith((".txt", ".out")):
                files.append(os.path.join(dirpath, fn))
    sols = {}          # tuple -> set of source basenames
    bad = []
    for path in sorted(files):
        try:
            txt = open(path, errors="replace").read()
        except Exception:
            continue
        for line in txt.splitlines():
            line = line.strip()
            if not line.startswith("SOL"):
                continue
            parts = line.split()[1:]
            try:
                U = sorted(int(x) for x in parts)
            except ValueError:
                continue
            if not U:
                continue
            ok, why = is_solution(U)
            t = tuple(U)
            if ok:
                sols.setdefault(t, set()).add(os.path.relpath(path, ROOT))
            else:
                bad.append((os.path.relpath(path, ROOT), why, t[:6]))
    return sols, bad


if __name__ == "__main__":
    sols, bad = gather()
    print("distinct verified solutions:", len(sols))
    print("rejected lines:", len(bad))
    for b in bad[:20]:
        print("  REJECT", b)
    out = os.path.join(ROOT, "attempts/wf-mining/CORPUS.txt")
    keyed = sorted(sols, key=lambda t: (t[-1], t[0], t))
    with open(out, "w") as f:
        for t in keyed:
            f.write(" ".join(map(str, t)) + "\n")
    print("wrote", out)
