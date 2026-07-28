#!/usr/bin/env python3
"""Basic per-solution statistics over CORPUS.txt.  Exact integer arithmetic only."""
import sys
from fractions import Fraction
from collections import Counter, defaultdict

CORPUS = "/home/user/erdos/attempts/wf-mining/CORPUS.txt"


def load(path=CORPUS):
    out = []
    for line in open(path):
        line = line.strip()
        if line:
            out.append(tuple(int(x) for x in line.split()))
    return out


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


def stat(U):
    R = runs_of(U)
    L = [len(x) for x in R]
    return dict(T=U[0], N=U[-1], m=len(U), r=len(L), cap=sum(l // 2 for l in L),
                L=L, runs=R)


if __name__ == "__main__":
    S = load()
    print("corpus size:", len(S))
    rows = [stat(U) for U in S]

    # global ranges
    print("min(min U) =", min(r["T"] for r in rows), " max(min U) =", max(r["T"] for r in rows))
    print("min(max U) =", min(r["N"] for r in rows), " max(max U) =", max(r["N"] for r in rows))
    print("min |U| =", min(r["m"] for r in rows), " max |U| =", max(r["m"] for r in rows))
    print("min r =", min(r["r"] for r in rows), " max r =", max(r["r"] for r in rows))
    print("min cap =", min(r["cap"] for r in rows), " max cap =", max(r["cap"] for r in rows))

    # k coverage
    cov = set()
    for r in rows:
        cov |= set(range(r["r"], r["cap"] + 1))
    ks = sorted(cov)
    print("k covered:", ks[0], "..", ks[-1], "gaps:", [k for k in range(ks[0], ks[-1] + 1) if k not in cov])

    # by T
    byT = defaultdict(list)
    for r in rows:
        byT[r["T"]].append(r)
    print("\n T   #sols  maxCap  minR@maxCap  max|U|  minN  maxN  medianDensity")
    for T in sorted(byT):
        g = byT[T]
        mc = max(x["cap"] for x in g)
        best = [x for x in g if x["cap"] == mc]
        mr = min(x["r"] for x in best)
        dens = sorted(Fraction(x["m"], x["N"] - x["T"] + 1) for x in g)
        med = dens[len(dens) // 2]
        print("%4d %6d %6d %8d %8d %6d %6d   %.3f" %
              (T, len(g), mc, mr, max(x["m"] for x in g), min(x["N"] for x in g),
               max(x["N"] for x in g), float(med)))
