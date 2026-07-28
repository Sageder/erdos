"""
H_reduce.py -- Route H, step 2.  THE PRIME-REMOVAL REDUCTION.

CLAIM TESTED / IMPLEMENTED (Lemma L5, proof in FINDINGS.md):

  L5.  Let A be the modulus set of a covering system of Z (distinct moduli >1), let q be a
       prime and A_q = {m in A : q | m}.  If |A_q| < q then A \ A_q is again the modulus set
       of a covering system of Z (same moduli, new residues), with distinct moduli.

  Proof sketch: the residues a_m mod q, m in A_q, miss some class c mod q; the fiber c+qZ is
  covered using only classes with q ∤ m; substituting x = c+qy turns a_m mod m into
  (a_m-c)q^{-1} mod m, so the moduli are unchanged.

  CONSEQUENCE (Reduction R).  Let M be any finite set of admissible moduli.  Define R(M) by
  repeatedly deleting, for every prime q with #{m in M : q | m} < q, all multiples of q.
  Then: M contains a covering set  <=>  R(M) contains a covering set; and, for the pair
  problem, M contains two DISJOINT covering sets <=> R(M) does.  (Any covering set A ⊆ M
  satisfies |A_q| <= #{m in M : q|m} < q, so the same deletions are legal for A; and the two
  reduced sets remain disjoint since they are subsets of the originals.)

  This collapses H ∩ [2,Y] to a tiny 2/3/5(/7)-smooth set with a small lcm, making exhaustive
  search possible.

CONCLUSION: printed table of R(Y), its budget and its lcm; recorded in FINDINGS.md.
"""
from fractions import Fraction
from math import lcm
from sympy import isprime, primerange, factorint
import sys


def H_upto(Y):
    return [m for m in range(2, Y + 1) if isprime(2 * m + 1)]


def reduce_set(M, verbose=False):
    """Fixpoint of: delete all multiples of q whenever #multiples of q is < q."""
    M = sorted(M)
    log = []
    changed = True
    while changed:
        changed = False
        primes = sorted({p for m in M for p in factorint(m)})
        for q in primes:
            mult = [m for m in M if m % q == 0]
            if 0 < len(mult) < q:
                log.append((q, len(mult), mult))
                M = [m for m in M if m % q != 0]
                changed = True
                break
    if verbose:
        for (q, c, mult) in log:
            print("      deleted q=%-4d (only %d multiples: %s)" % (q, c, mult))
    return M, log


def budget(M):
    return sum(Fraction(1, m) for m in M)


def lcm_of(M):
    L = 1
    for m in M:
        L = lcm(L, m)
    return L


def main():
    Ys = [10, 15, 20, 25, 30, 40, 50, 60, 75, 100, 125, 150, 200, 250, 300, 400, 500,
          750, 1000, 1500, 2000, 3000, 5000]
    print("%-6s %-5s %-9s | %-5s %-11s %-12s %s" %
          ("Y", "|H|", "bud(H)", "|R|", "bud(R)", "lcm(R)", "R(Y)"))
    for Y in Ys:
        M = H_upto(Y)
        R, log = reduce_set(M)
        bR = budget(R)
        LR = lcm_of(R)
        tag = ""
        if bR <= 1:
            tag = "  <= 1  => NO covering with moduli <= Y"
        elif bR <= 2:
            tag = "  <= 2  => NO two disjoint coverings => NO E-covering with moduli <= %d" % (2 * Y)
        print("%-6d %-5d %-9.5f | %-5d %-11.5f %-12d %s%s" %
              (Y, len(M), float(budget(M)), len(R), float(bR), LR,
               R if len(R) <= 22 else str(R[:22]) + "...", tag))
    print()
    print("Detail for a few Y:")
    for Y in (50, 100, 150, 200, 300, 500, 1000):
        M = H_upto(Y)
        print("  Y=%d:" % Y)
        R, log = reduce_set(M, verbose=True)
        print("      R(Y) = %s" % (R,))
        print("      budget = %s = %.6f    lcm = %d = %s"
              % (budget(R), float(budget(R)), lcm_of(R), factorint(lcm_of(R))))


if __name__ == "__main__":
    main()
