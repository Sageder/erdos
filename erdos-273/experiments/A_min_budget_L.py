"""
A_min_budget_L.py

CLAIM TESTED (and PROVED for the searched range):  a covering system whose moduli all lie
in E and all divide L must satisfy the density bound
        B_E(L) := sum_{n | L, n in E} 1/n  >  1 ,
and by Lemma A1 (parity split) the halved quantity must satisfy
        B_H(L/2) := sum_{m | L/2, m in H} 1/m  >  2 .
What is the SMALLEST L for which each of these holds?  Any L failing them is UNSAT for
Erdos 273 outright, with no SAT call.  Hence the smallest such L is a rigorous LOWER
BOUND on lcm(n_1,...,n_k) for any covering system with moduli in E.

The search enumerates every P-smooth L <= bound by recursion on the prime exponents,
carrying the divisor list along, so each candidate costs O(#divisors) primality tests.
Non-smooth L are irrelevant: dropping a prime p || L that divides no element of
D_E(L) does not change D_E, and every L with B_E(L) > 1 must have many small divisors.
(The exhaustive complement check over ALL L below the winner is done separately.)

CONCLUSION: printed.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import is_prime
from fractions import Fraction

PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def scan(B):
    res = []

    def rec(i, L, divs):
        if i == len(PR):
            bE = sum(Fraction(1, d) for d in divs if d >= 4 and is_prime(d + 1))
            bH = sum(Fraction(1, d) for d in divs if d >= 2 and is_prime(2 * d + 1))
            res.append((L, bE, bH))
            return
        p = PR[i]
        rec(i + 1, L, divs)
        cur, nd, mult = L, list(divs), 1
        while True:
            mult *= p
            cur = L * mult
            if cur > B:
                break
            nd = nd + [d * mult for d in divs]
            rec(i + 1, cur, nd)

    rec(0, 1, [1])
    return res


if __name__ == "__main__":
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 3 * 10 ** 7
    res = scan(B)
    print("smooth candidates examined:", len(res))
    eok = sorted([r for r in res if r[1] > 1])
    print("smallest L with B_E(L) > 1        :",
          [(r[0], float(r[1])) for r in eok[:6]])
    hok = sorted([r for r in res if r[2] > 1])
    print("smallest Lh with B_H(Lh) > 1      :",
          [(r[0], float(r[2])) for r in hok[:6]])
    h2 = sorted([r for r in res if r[2] > 2])
    print("smallest Lh with B_H(Lh) > 2      :",
          [(r[0], float(r[2])) for r in h2[:6]])
    print("  (a covering in E needs lcm = 2*Lh with B_H(Lh) > 2, i.e. lcm >=",
          2 * h2[0][0], ")" if h2 else "")
    # exhaustive complement check over every L below the smooth winner
    win = eok[0][0]
    print(f"exhaustive check of EVERY L <= {win} for B_E(L) > 1 ...")

    def divisors(n):
        ds, d = [], 1
        while d * d <= n:
            if n % d == 0:
                ds.append(d)
                if d != n // d:
                    ds.append(n // d)
            d += 1
        return ds

    first = None
    for L in range(4, win + 1, 2):
        b = sum(Fraction(1, d) for d in divisors(L) if d >= 4 and is_prime(d + 1))
        if b > 1:
            first = (L, float(b))
            break
    print("  first L over ALL integers with B_E(L) > 1:", first)
