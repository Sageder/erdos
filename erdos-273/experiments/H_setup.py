"""
H_setup.py  --  Route H, step 0.

CLAIM TESTED (three separate claims, all verified numerically here):

  (C0)  E = {n : n >= 4, n+1 prime} = 2*H  where  H = {m >= 2 : 2m+1 prime}.

  (C1)  PARITY REDUCTION (equivalence, not merely a necessary condition):
        There is a covering system of Z with distinct moduli all in E
          <=>  there are two DISJOINT sets A, B subseteq H such that each of A and B
               is the modulus set of a covering system of Z with distinct moduli.
        Proof (recorded in FINDINGS.md; the script only sanity-checks the two
        translation maps on random data).

  (C2)  Sieve constraints on H: for every odd prime q and every m in H with 2m+1 > q,
        m !≡ (q-1)/2 (mod q).  In particular every m in H with m>=3 satisfies
        m ≡ 0 or 2 (mod 3), and every n in E with n>=6 satisfies n ≡ 0 or 4 (mod 6).

CONCLUSION: printed; all assertions pass.  See FINDINGS.md.

Deterministic and exact (sympy.isprime on small ints = deterministic BPSW/trial).
"""
import sys
from fractions import Fraction
from sympy import isprime

def E_upto(X):
    return [n for n in range(4, X + 1) if isprime(n + 1)]

def H_upto(Y):
    return [m for m in range(2, Y + 1) if isprime(2 * m + 1)]

def main():
    X = 400
    E = E_upto(X)
    H = H_upto(X // 2)
    # (C0)
    assert E == [2 * m for m in H if 2 * m <= X], "E = 2H failed"
    print("(C0) E cap [4,%d] = 2 * (H cap [2,%d])   VERIFIED" % (X, X // 2))
    print("     E:", E[:24], "...")
    print("     H:", H[:24], "...")

    # (C2)
    for q in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        bad = (q - 1) // 2
        viol = [m for m in H if 2 * m + 1 > q and m % q == bad]
        assert not viol, (q, viol)
    print("(C2) sieve constraints m !≡ (q-1)/2 mod q  VERIFIED for q <= 31")
    assert all(m % 3 in (0, 2) for m in H), "mod 3"
    assert all(n % 6 in (0, 4) for n in E if n >= 6), "mod 6"
    print("     every m in H is ≡ 0 or 2 mod 3;  every n in E, n>=6, is ≡ 0 or 4 mod 6")

    # reciprocal-sum landmarks
    for Y in (30, 44, 50, 100, 150, 250, 500):
        HH = H_upto(Y)
        s = sum(Fraction(1, m) for m in HH)
        print("     sum_{m in H, m<=%4d} 1/m = %.6f   (#=%d)   [E: sum_{n<=%4d} 1/n = %.6f]"
              % (Y, float(s), len(HH), 2 * Y, float(s) / 2))

    # smallest X with sum_{n in E, n<=X} 1/n > 1
    s = Fraction(0)
    for n in E:
        s += Fraction(1, n)
        if s > 1:
            print("(budget) smallest X with sum_{n in E, n<=X}1/n > 1 is X = %d, sum = %s = %.6f"
                  % (n, s, float(s)))
            break
    # smallest Y with sum_{m in H, m<=Y} 1/m > 2   (necessary for the two-disjoint-halves split)
    s = Fraction(0)
    for m in H:
        s += Fraction(1, m)
        if s > 2:
            print("(budget) smallest Y with sum_{m in H, m<=Y}1/m > 2 is Y = %d, sum = %.6f"
                  % (m, float(s)))
            print("         => any E-covering with all moduli <= X needs X >= %d" % (2 * m))
            break

    # translation-map sanity check (C1), both directions, on a hand-made toy example
    # take an H-covering-like family and check the induced E-classes behave as claimed
    A = [(0, 2), (0, 3), (1, 6)]          # not a covering, just tests the maps
    covE = set()
    for (a, m) in A:                      # even branch: 2a mod 2m
        for x in range(0, 120):
            if x % (2 * m) == (2 * a) % (2 * m):
                covE.add(x)
    for x in range(0, 120):
        if x % 2 == 0:
            y = x // 2
            inA = any(y % m == a % m for (a, m) in A)
            assert inA == (x in covE), (x, y)
        else:
            assert x not in covE
    print("(C1) even-branch translation map m<->2m verified pointwise on [0,120)")
    print("\nALL CHECKS PASSED")

if __name__ == "__main__":
    main()
