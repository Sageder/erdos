"""
CLAIM TESTED: basic structural / budget facts about
    E = {p-1 : p prime, p >= 5}   and   H = {(p-1)/2 : p prime, p >= 5}.
Recomputes every numeric claim of PROMPT.md Section 4 in exact rational arithmetic.

CONCLUSION (printed): see run output; recorded in NOTES.md.

Deterministic, exact (Fraction / sympy.isprime).
"""
from fractions import Fraction
from sympy import isprime, factorint
import sys

def E_upto(X):
    return [n for n in range(4, X + 1) if isprime(n + 1)]

def H_upto(Y):
    return [m for m in range(2, Y + 1) if isprime(2 * m + 1)]

def main():
    # ---- PROMPT.md Section 1: the listed initial segment of E
    E = E_upto(102)
    print("E ∩ [4,102] =", E)
    assert E[:25] == [4, 6, 10, 12, 16, 18, 22, 28, 30, 36, 40, 42, 46, 52, 58,
                      60, 66, 70, 72, 78, 82, 88, 96, 100, 102], E[:25]
    print("  matches PROMPT.md Section 1 list  ✓")

    # non-members claimed in PROMPT.md
    nonmem = [8, 14, 20, 24, 26, 32, 34, 38, 44, 48, 50, 54, 56, 62, 64, 68, 74,
              76, 80, 84, 86, 90, 92, 94, 98]
    assert all(not isprime(n + 1) for n in nonmem)
    print("  claimed non-members 8,14,20,...,98 all verified composite+1  ✓")

    # ---- Section 4: budget of the 17 smallest elements of E
    E17 = E_upto(66)
    assert len(E17) == 17, (len(E17), E17)
    s17 = sum(Fraction(1, n) for n in E17)
    print("\n17 smallest elements of E:", E17)
    print("  sum of reciprocals =", s17, "=", float(s17))
    assert s17 == Fraction(160107799, 160240080), s17
    assert s17 < 1
    print("  == 160107799/160240080  ✓  and  < 1  ✓")
    E18 = E_upto(70)
    assert len(E18) == 18 and E18[-1] == 70
    s18 = sum(Fraction(1, n) for n in E18)
    print("  adding 70:", s18, "=", float(s18), " > 1 :", s18 > 1)
    L18 = 1
    from math import lcm
    for n in E18:
        L18 = lcm(L18, n)
    print("  lcm of the 18 smallest =", L18, "=", factorint(L18))
    assert L18 == 480720240

    # ---- Section 4: H, the halved world
    H = H_upto(44)
    print("\nH ∩ [2,44] =", H)
    assert H == [2, 3, 5, 6, 8, 9, 11, 14, 15, 18, 20, 21, 23, 26, 29, 30, 33,
                 35, 36, 39, 41, 44], H
    print("  matches PROMPT.md Section 4 list  ✓")
    missing = [4, 7, 10, 12, 13, 16, 17, 19, 22, 24, 25, 27, 28]
    assert all(not isprime(2 * m + 1) for m in missing)
    print("  claimed omissions 4,7,10,12,13,16,17,19,22,24,25,27,28 verified  ✓")

    # ---- budgets: how much reciprocal mass is available at all
    print("\nBudget  B_E(X) = sum_{n in E, n<=X} 1/n     (all of E, no divisibility restriction)")
    for X in [10**2, 10**3, 10**4, 10**5, 10**6, 10**7]:
        b = 0.0
        # sieve for speed
        b = sum(1.0 / n for n in sieve_E(X))
        print(f"   X = 10^{len(str(X))-1:<2}  B_E = {b:.5f}")

    print("\nBudget  B_H(Y) = sum_{m in H, m<=Y} 1/m  = 2 * B_E(2Y)")
    for Y in [10**2, 10**3, 10**4, 10**5, 10**6, 10**7]:
        b = sum(1.0 / m for m in sieve_H(Y))
        print(f"   Y = 10^{len(str(Y))-1:<2}  B_H = {b:.5f}")

    # ---- enrichment: fraction of E-budget carried by multiples of d
    print("\nEnrichment of E at multiples of d  (share of budget; heuristic value 1/phi(d))")
    from sympy import totient
    X = 10**7
    Es = sieve_E(X)
    tot = sum(1.0 / n for n in Es)
    for d in [2, 3, 4, 5, 6, 8, 9, 10, 12, 16, 30, 105]:
        s = sum(1.0 / n for n in Es if n % d == 0)
        print(f"   d={d:<4} share={s/tot:.4f}   1/phi(d)={1.0/int(totient(d)):.4f}"
              f"   1/d={1.0/d:.4f}")

def sieve_E(X):
    """all n in [4,X] with n+1 prime, via a sieve of Eratosthenes on [0,X+1]."""
    N = X + 1
    bs = bytearray([1]) * (N + 1)
    bs[0] = bs[1] = 0
    i = 2
    while i * i <= N:
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
        i += 1
    return [p - 1 for p in range(5, N + 1) if bs[p]]

def sieve_H(Y):
    return [(p - 1) // 2 for p in sieve_primes(2 * Y + 1) if p >= 5]

def sieve_primes(N):
    bs = bytearray([1]) * (N + 1)
    bs[0] = bs[1] = 0
    i = 2
    while i * i <= N:
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
        i += 1
    return [i for i in range(N + 1) if bs[i]]

if __name__ == "__main__":
    main()
