#!/usr/bin/env python3
r"""
double.py -- THE DOUBLING MAP (one exact search per doubling).

DOUBLING LEMMA (proved).  Let U be a legal system with Sigma(U) = rho and
min U = T.  Fix c > 1 and let  Low  be the union of all maximal runs of U that
contain an element < cT, and  High = U \ Low.  Then High is legal and
min High >= cT.  If S is a legal system with

        Sigma(S) = Sigma(Low),    min S >= cT,    S ∩ High = empty,

then U' := High ∪ S is legal, Sigma(U') = rho and min U' >= cT.

Proof.  High is a union of maximal runs of U, hence legal, and every element of
High is >= cT by construction.  A union of legal systems is legal (each element
keeps a neighbour in its own part).  The parts are disjoint so the sums add. ∎

Iterating with c = 2 is a genuine BOOTSTRAPPING MAP: min U -> 2 min U.  Whether
it can always be applied is exactly the LIFT question for the rational
Sigma(Low) above the threshold 2T; this script decides instances exactly.

usage: double.py --inline n1,n2,...  --c 2.0 --nmax N1,N2,...  [--rounds R]
"""
import sys, os
from fractions import Fraction
import liftscan as LS


def runs(U):
    U = sorted(U); out, cur = [], [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1: cur.append(x)
        else: out.append(cur); cur = [x]
    out.append(cur); return out


def legal(S):
    s = set(S); return all((n - 1 in s) or (n + 1 in s) for n in s)


def stats(U):
    R = runs(U); return len(R), sum(len(r) // 2 for r in R)


def double_once(U, c, nmax_list, nsol=1, budget=0, seeds=(0,), above=False, tmo=None):
    T = min(U); thr = int(c * T + 0.9999)
    R = runs(U)
    Low = [x for r in R if r[0] < thr for x in r]
    High = [x for r in R if r[0] >= thr for x in r]
    q = sum(Fraction(1, n) for n in Low)
    print("  T=%d thr=%d |Low|=%d q=%s(%.5f) |High|=%d" % (T, thr, len(Low), q, float(q), len(High)), flush=True)
    lo = (max(U) + 1) if above else thr
    for N in nmax_list:
        for sd in seeds:
            st, sols, nodes, lb = LS.run(q, lo, N, nsol=nsol,
                                         banned=frozenset() if above else frozenset(High),
                                         budget=budget, seed=sd, tmo=tmo)
            print("    window[%d,%d] seed=%d Lbits=%d nodes=%d -> %s" % (lo, N, sd, lb, nodes, st), flush=True)
            if st == "SOL":
                S = sols[0]
                U2 = sorted(set(High) | set(S))
                assert legal(U2) and len(U2) == len(High) + len(S)
                return U2
            if st == "TOOBIG":
                break
    return None


if __name__ == "__main__":
    a = sys.argv[1:]
    U = None; c = 2.0; nmax = None; rounds = 1; budget = 0; seeds = (0,); above = False; tmo = None
    i = 0
    while i < len(a):
        if a[i] == "--inline": U = sorted(int(x) for x in a[i+1].replace(",", " ").split()); i += 2
        elif a[i] == "--file": U = sorted(int(x) for x in open(a[i+1]).read().replace("SOL", " ").split()); i += 2
        elif a[i] == "--c": c = float(a[i+1]); i += 2
        elif a[i] == "--nmax": nmax = [int(x) for x in a[i+1].split(",")]; i += 2
        elif a[i] == "--rounds": rounds = int(a[i+1]); i += 2
        elif a[i] == "--budget": budget = int(a[i+1]); i += 2
        elif a[i] == "--above": above = True; i += 1
        elif a[i] == "--tmo": tmo = float(a[i+1]); i += 2
        elif a[i] == "--seeds": seeds = tuple(int(x) for x in a[i+1].split(",")); i += 2
        else: i += 1
    total = sum(Fraction(1, n) for n in U)
    assert legal(U)
    print("start min=%d max=%d |U|=%d sum=%s r,cap=%s" % (min(U), max(U), len(U), total, stats(U)), flush=True)
    for rd in range(rounds):
        T = min(U); thr = int(c * T + 0.9999)
        nl = nmax if nmax else [int(thr * f) for f in (1.6, 2.0, 2.6, 3.4, 4.5, 6.0)]
        U2 = double_once(U, c, nl, budget=budget, seeds=seeds, above=above, tmo=tmo)
        if U2 is None:
            print("STOP round %d min=%d" % (rd, min(U))); break
        U = U2
        assert sum(Fraction(1, n) for n in U) == total
        r, cap = stats(U)
        print("round %d: min=%d max=%d |U|=%d r=%d cap=%d" % (rd, min(U), max(U), len(U), r, cap), flush=True)
        print("SOL " + " ".join(map(str, U)), flush=True)
    print("FINAL min=%d max=%d |U|=%d sum=%s r,cap=%s" % (min(U), max(U), len(U), sum(Fraction(1, n) for n in U), stats(U)))
    print("SOL " + " ".join(map(str, U)))
