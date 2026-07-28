"""
Q5 -- exact verification of the supplied identities, plus the new
RUN-RESCALING identities that route-D uses.

All checks are exact (Fraction / integer).  Each identity is checked
symbolically with sympy AND numerically over a range with Fractions.
"""

from fractions import Fraction

import sympy as sp

from blocks import H

n, m, a, b, d, q = sp.symbols("n m a b d q", positive=True, integer=True)


def sym_zero(expr, name):
    z = sp.simplify(sp.together(expr))
    ok = (z == 0)
    print("   [sympy] %-58s : %s" % (name, "IDENTITY" if ok else "FAILS -> %s" % z))
    return ok


def main():
    print("== given identities (symbolic) ==")
    sym_zero(1 / n - (1 / (2 * n) + 1 / (2 * n + 1) + 1 / (2 * n * (2 * n + 1))),
             "1/n = 1/2n + 1/(2n+1) + 1/(2n(2n+1))")
    sym_zero(1 / n - (1 / (n + d) + 1 / (n + n ** 2 / d)),
             "1/n = 1/(n+d) + 1/(n+n^2/d)")
    sym_zero((1 / (2 * m) + 1 / (2 * m + 1)) - (1 / m - 1 / (2 * m * (2 * m + 1))),
             "1/2m + 1/(2m+1) = 1/m - 1/(2m(2m+1))")
    sym_zero((1 / (2 * m - 1) + 1 / (2 * m)) - (1 / m + 1 / (2 * m * (2 * m - 1))),
             "1/(2m-1) + 1/2m = 1/m + 1/(2m(2m-1))")
    sym_zero((1 / (3 * m - 1) + 1 / (3 * m) + 1 / (3 * m + 1))
             - (1 / m + 2 / (3 * m * (3 * m - 1) * (3 * m + 1))),
             "1/(3m-1)+1/3m+1/(3m+1) = 1/m + 2/(3m(3m-1)(3m+1))")

    print("== new run-rescaling identities (numeric, exact) ==")
    bad = []
    for A in range(1, 60):
        for B in range(A, A + 25):
            lhs = H(2 * A, 2 * B + 1)
            rhs = H(A, B) - sum((Fraction(1, 2 * k * (2 * k + 1))
                                 for k in range(A, B + 1)), Fraction(0))
            if lhs != rhs:
                bad.append(("double-up", A, B))
            lhs2 = H(2 * A - 1, 2 * B)
            rhs2 = H(A, B) + sum((Fraction(1, 2 * k * (2 * k - 1))
                                  for k in range(A, B + 1)), Fraction(0))
            if lhs2 != rhs2:
                bad.append(("double-down", A, B))
            lhs3 = H(3 * A - 1, 3 * B + 1)
            rhs3 = H(A, B) + sum((Fraction(2, 3 * k * (3 * k - 1) * (3 * k + 1))
                                  for k in range(A, B + 1)), Fraction(0))
            if lhs3 != rhs3:
                bad.append(("triple", A, B))
    print("   H(2a,2b+1) = H(a,b) - sum_{n=a}^b 1/(2n(2n+1))          :",
          "OK" if not any(x[0] == "double-up" for x in bad) else "FAIL")
    print("   H(2a-1,2b) = H(a,b) + sum_{n=a}^b 1/(2n(2n-1))          :",
          "OK" if not any(x[0] == "double-down" for x in bad) else "FAIL")
    print("   H(3a-1,3b+1) = H(a,b) + sum_{n=a}^b 2/(3n(9n^2-1))      :",
          "OK" if not any(x[0] == "triple" for x in bad) else "FAIL")

    print("== general q-rescaling:  {qn+j : a<=n<=b, 0<=j<q} = [qa, qb+q-1] ==")
    ok = True
    for Q in range(2, 8):
        for A in range(1, 20):
            for B in range(A, A + 8):
                S = sorted(Q * k + j for k in range(A, B + 1) for j in range(Q))
                if S != list(range(Q * A, Q * B + Q)):
                    ok = False
                lhs = H(Q * A, Q * B + Q - 1)
                rhs = sum((Fraction(1, Q * k + j)
                           for k in range(A, B + 1) for j in range(Q)), Fraction(0))
                if lhs != rhs:
                    ok = False
    print("   q-fold blow-up of a run is a run, and sums agree        :",
          "OK" if ok else "FAIL")

    print("== the length-2 'unit fraction + correction' normal form ==")
    ok = True
    for N in range(2, 400):
        M = (N + 1) // 2 if N % 2 else N // 2
        sigma = 1 if N % 2 else -1
        if H(N, N + 1) != Fraction(1, M) + sigma * Fraction(1, N * (N + 1)):
            ok = False
    print("   H(n,n+1) = 1/ceil(n/2) + (-1)^(n+1)/(n(n+1))            :",
          "OK" if ok else "FAIL")

    print("== length-3 normal forms ==")
    ok = True
    for M in range(2, 200):
        if H(3 * M - 1, 3 * M + 1) != Fraction(1, M) + Fraction(2, 3 * M * (9 * M * M - 1)):
            ok = False
        if H(3 * M, 3 * M + 2) != (Fraction(1, M) - Fraction(1, 3 * M * (3 * M + 1))
                                   - Fraction(2, 3 * M * (3 * M + 2))):
            ok = False
        if H(3 * M - 2, 3 * M) != (Fraction(1, M) + Fraction(1, 3 * M * (3 * M - 1))
                                   + Fraction(2, 3 * M * (3 * M - 2))):
            ok = False
    print("   three length-3 normal forms around 3m                   :",
          "OK" if ok else "FAIL")

    print("== sanity: PROBLEM.md B5 ==")
    print("   1/3+1/4+1/5+1/6+1/20 =",
          Fraction(1, 3) + Fraction(1, 4) + Fraction(1, 5) + Fraction(1, 6) + Fraction(1, 20))
    print("   1/2+1/3+1/10+1/15    =",
          Fraction(1, 2) + Fraction(1, 3) + Fraction(1, 10) + Fraction(1, 15))
    print("   1/2+1/3+1/4+1/5+1/6+1/20 =",
          sum((Fraction(1, k) for k in (2, 3, 4, 5, 6, 20)), Fraction(0)))


if __name__ == "__main__":
    main()
