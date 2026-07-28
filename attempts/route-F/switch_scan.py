#!/usr/bin/env python3
"""Measure switches across scales.

For each window, build a pruned universe, enumerate legal subsets (capped),
find residue-vector collisions = SWITCHES, verify each candidate EXACTLY with
Fraction, and report:
  * whether GADGETS exist in the same universe (exhaustive run of search.c)
  * number of switches, number of distinct |c|, min |c|, gcd of all c
usage: switch_scan.py D maxsubsets  x:y:ppcap [x:y:ppcap ...]
"""
import sys, os, subprocess
from fractions import Fraction
from math import gcd, log2
from functools import reduce
from lib import smallest_prime_factors
from universe import prune, lcm_of
from entropy import count_legal
from mk import write_problem

HERE = os.path.dirname(os.path.abspath(__file__))
D = int(sys.argv[1]); MAXS = int(sys.argv[2])
specs = sys.argv[3:]
spf = smallest_prime_factors(max(int(s.split(":")[1]) for s in specs) + 2)


def legal(U):
    S = set(U)
    return len(S) == len(U) and all(n >= 2 for n in S) and \
        all((n - 1) in S or (n + 1) in S for n in S)


for s in specs:
    x, y, q = (int(t) for t in s.split(":"))
    U = prune(x, y, D, spf, pp_cap=(q or None))
    if len(U) < 2:
        print("%-18s universe too small" % s); continue
    if len(U) > 128:
        print("%-18s |U|=%d >128 skipped" % (s, len(U))); continue
    L = lcm_of(U); lam = (L // gcd(L, D)).bit_length()
    nleg = count_legal(U); Lam = log2(nleg)
    ms = sum(Fraction(1, n) for n in U)
    pf = "ss%d.prob" % os.getpid()
    write_problem(pf, U, D, None, Fraction(0), ms)
    # gadget test (exhaustive)
    r = subprocess.run([os.path.join(HERE, "search"), pf, "ss%d.gad" % os.getpid(),
                        "5", "3000000000"], capture_output=True, text=True)
    gad = r.stderr.strip()
    # switch search
    r2 = subprocess.run([os.path.join(HERE, "switchc"), pf, "ss%d.sw" % os.getpid(),
                         str(MAXS)], capture_output=True, text=True)
    cs = {}
    nsw = 0
    for line in open("ss%d.sw" % os.getpid()):
        if "|" not in line:
            continue
        l, rr = line.split("|")
        A = [int(t) for t in l.split()]; B = [int(t) for t in rr.split()]
        assert legal(A) and legal(B) and min(A + B) >= x, (A, B)
        d = (sum(Fraction(1, n) for n in B) - sum(Fraction(1, n) for n in A)) * D
        assert d.denominator == 1, "NOT a switch!"
        c = int(d)
        if c == 0:
            continue
        nsw += 1
        cs.setdefault(abs(c), (A, B))
    g = reduce(gcd, cs) if cs else 0
    print("%-18s |U|=%-4d Lam=%-6.1f lam=%-4d maxsum=%.4f | gadgets: %s | switches=%d "
          "distinct|c|=%d min|c|=%s gcd=%d"
          % (s, len(U), Lam, lam, float(ms), gad.replace("\n", " "), nsw,
             len(cs), min(cs) if cs else "-", g))
    sys.stdout.flush()
    if cs:
        k = min(cs); A, B = cs[k]
        with open("switch_witness_%d_%d_%d.txt" % (x, y, q), "w") as h:
            h.write("%s | %s\n" % (" ".join(map(str, sorted(A))),
                                   " ".join(map(str, sorted(B)))))
    for e in (".prob", ".gad", ".sw"):
        try: os.remove("ss%d%s" % (os.getpid(), e))
        except OSError: pass
