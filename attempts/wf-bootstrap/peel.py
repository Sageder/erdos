#!/usr/bin/env python3
"""
peel.py -- THE PEELING BOOTSTRAP.

PEEL LEMMA (proved; see final report).  Let U be a solution (legal, Sigma(U)=1),
let B = [m, m'] be its LOWEST maximal run (m = min U).  Let S be a legal set with

        Sigma(S) = H(m,m') = Sigma(B),     S ∩ (U \ B) = empty,     min(S) > m.

Then U' := (U \ B) ∪ S is a solution with min(U') > min(U).

Proof.  U \ B is a union of maximal runs of U, hence legal.  A union of legal
sets is legal (every element keeps a neighbour inside its own part).  The sums
add because the parts are disjoint.  min(U\B) > m'+1 > m and min(S) > m.  ∎

Iterating the Peel Lemma is a BOOTSTRAP: each step strictly raises min U.  If
the step always succeeds, CRUX (hence Erdos 289) follows.  This script runs the
iteration on real certificates and records exactly which steps succeed.

Everything exact: universe.py fixpoint (sound), route-E search.c (exact 128-bit
integers), and an independent re-verification with fractions.Fraction after
every step.

usage: peel.py solfile|--inline n1,n2,... [--target T] [--nmax N] [--rounds R]
"""
import sys, os
from fractions import Fraction
import liftscan as LS

HERE = os.path.dirname(os.path.abspath(__file__))


def runs(U):
    U = sorted(U)
    out, cur = [], [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            out.append(cur); cur = [x]
    out.append(cur)
    return out


def legal(S):
    s = set(S)
    return all((n - 1 in s) or (n + 1 in s) for n in s)


def stats(U):
    R = runs(U)
    return len(R), sum(len(r) // 2 for r in R)


def peel_once(U, total, tmin=None, nmax_list=(150, 200, 260, 320, 400, 500, 640, 800), nsol=1, verbose=True):
    """One peel step.  Returns (U', info) or (None, info)."""
    R = runs(U)
    B = R[0]
    q = sum(Fraction(1, n) for n in B)
    banned = set(U) - set(B)
    lo = (tmin if tmin is not None else min(U) + 1)
    for N in nmax_list:
        if N <= lo + 1:
            continue
        st, sols, nodes, lb = LS.run(q, lo, N, nsol=nsol, banned=frozenset(banned))
        if verbose:
            print("    peel B=%s q=%s window[%d,%d] Lbits=%d nodes=%d -> %s"
                  % (B, q, lo, N, lb, nodes, st), flush=True)
        if st == "SOL":
            S = sols[0]
            U2 = sorted(set(U) - set(B) | set(S))
            assert len(U2) == len(U) - len(B) + len(S)
            assert legal(U2)
            assert sum(Fraction(1, n) for n in U2) == total
            return U2, ("SOL", N, nodes)
    return None, ("FAIL", None, None)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "--inline":
        U = sorted(int(x) for x in a[1].replace(",", " ").split())
        a = a[2:]
    else:
        U = sorted(int(x) for x in open(a[0]).read().replace("SOL", " ").split())
        a = a[1:]
    tmin, rounds = None, 100
    nmax = [150, 200, 260, 320, 400, 500, 640, 800, 1000]
    i = 0
    while i < len(a):
        if a[i] == "--target": tmin = int(a[i + 1]); i += 2
        elif a[i] == "--rounds": rounds = int(a[i + 1]); i += 2
        elif a[i] == "--nmax": nmax = [int(x) for x in a[i + 1].split(",")]; i += 2
        else: i += 1
    total = sum(Fraction(1, n) for n in U)
    assert legal(U)
    print("start: min=%d max=%d |U|=%d sum=%s r,cap=%s" % (min(U), max(U), len(U), total, stats(U)))
    for rd in range(rounds):
        U2, info = peel_once(U, total, tmin, nmax)
        if U2 is None:
            print("STOP at round %d, min=%d" % (rd, min(U)))
            break
        U = U2
        r, cap = stats(U)
        print("round %d: min=%d max=%d |U|=%d r=%d cap=%d" % (rd, min(U), max(U), len(U), r, cap), flush=True)
        print("   U =", " ".join(map(str, U)), flush=True)
    print("FINAL min=%d max=%d |U|=%d sum=%s r,cap=%s" % (min(U), max(U), len(U), sum(Fraction(1, n) for n in U), stats(U)))
    print("SOL " + " ".join(map(str, U)))
