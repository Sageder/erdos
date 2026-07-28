#!/usr/bin/env python3
r"""
unitlift.py -- THE UNIT-FRACTION LIFT TABLE.

    Lift(n,T)  :=  "1/n is the reciprocal sum of a legal system S with
                    min S >= T"   (S finite, no isolated point).

WHY THIS IS THE RIGHT OBJECT (ELEMENT LIFTING THEOREM, proved).
  Lemma 0 (union): a union of legal systems is legal, and if they are pairwise
  disjoint the reciprocal sums add.
  Hence: if U is a solution (legal, sum 1) and for every n in U we can choose a
  legal S_n with Sigma(S_n)=1/n, min S_n >= T, and the S_n PAIRWISE DISJOINT,
  then  Phi(U) := union of the S_n  is a solution with min >= T.
  So a bootstrapping map "min T -> min 2T" exists as soon as
        Lift(n, 2T) holds for every n in U   (in particular Lift(n,2n) suffices
        when min U = T and one is content with 2T <= 2n),
  together with a disjointness selection.  Note the map need NOT respect blocks
  at all -- legality is free under unions (Lemma 0), which is exactly why the
  element-wise map is admissible even though a single element is not legal.

This script measures the table exactly: for each n it scans N upward and
reports the smallest N for which a lift with min >= T and max <= N exists,
or an EXHAUSTIVE "no lift with max <= N".

usage: unitlift.py nlo nhi ratio [Nfactor]      (T = ceil(ratio*n))
"""
import sys
from fractions import Fraction
import liftscan as LS


def scan(n, T, Nmax, verbose=True):
    q = Fraction(1, n)
    N = max(T + 4, 2 * T)
    lastN, lastnodes, lastlb = None, 0, 0
    while N <= Nmax:
        st, sols, nodes, lb = LS.run(q, T, N, nsol=1)
        if st == "SOL":
            return ("SOL", N, sols[0], lb, nodes)
        if st == "TOOBIG":
            return ("TOOBIG", N, None, lb, 0)
        if st == "PARTIAL":
            return ("PARTIAL", N, None, lb, nodes)
        lastN, lastnodes, lastlb = N, nodes, lb
        N = int(N * 1.3) + 3
    return ("NONE", lastN or N, None, lastlb, lastnodes)


if __name__ == "__main__":
    nlo, nhi = int(sys.argv[1]), int(sys.argv[2])
    ratio = float(sys.argv[3])
    Nfac = float(sys.argv[4]) if len(sys.argv) > 4 else 60.0
    for n in range(nlo, nhi + 1):
        T = int(-(-ratio * n // 1))
        st, N, S, lb, nodes = scan(n, T, int(Nfac * n) + 20)
        print("n=%3d T=%3d (ratio %.2f)  %-7s N=%5d Lbits=%3d nodes=%d  %s"
              % (n, T, ratio, st, N, lb, nodes, "" if S is None else " ".join(map(str, S))),
              flush=True)
