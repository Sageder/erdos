"""
ADVERSARIAL AUDIT 4: Theorem A3, its strengthened form (M_A2plus), and the enumeration claims.

A3: if 60 | L and 1 < B_E(L) <= 31/30 then no covering system with all moduli in E has lcm | L.

Steps re-derived here:
  (1) used E-moduli are a subset of {n | L : n in E}, so sum_used 1/n <= B_E(L);
  (2) sum_used 1/n > 1  (density + DMNR)  => any n with B_E(L) - 1/n <= 1 is FORCED;
  (3) 60 | L => 4,6,10 | L and all lie in E; with B_E(L) <= 31/30 all three are forced;
  (4) halves 2,3,5 in H; X_j := sum_{M_j} 1/m - 1 satisfies X_0 + X_1 <= 2 B_E(L) - 2 <= 1/15
      and X_j > 0 strictly, hence X_j < 1/15 STRICTLY;
  (5) f({2,3}) = 1/6, f({2,5}) = 1/10, f({3,5}) = 1/15 -- all >= 1/15, so Lemma A2 forbids any
      two of 2,3,5 sharing a half;
  (6) pigeonhole: 3 objects, 2 halves.
Each numbered step is checked for strictness / off-by-one below.
"""
import sys
from fractions import Fraction
from math import gcd
from sympy import isprime
from itertools import combinations
import numpy as np


def fT(T):
    s = sum(Fraction(1, m) for m in T) - 1
    p = Fraction(1)
    for m in T:
        p *= Fraction(m - 1, m)
    return s + p


def BE_exact(L):
    return sum(Fraction(1, n) for n in range(4, L + 1) if L % n == 0 and isprime(n + 1))


def step_checks():
    print("  (3) forcing at the threshold B_E(L) = 31/30:")
    for n in (4, 6, 10):
        v = Fraction(31, 30) - Fraction(1, n)
        print(f"      31/30 - 1/{n} = {v} = {float(v):.6f}  < 1 : {v < 1}")
    print("      also check the WORST allowed case is the boundary: the forcing needs "
          "B_E(L) - 1/n <= 1, i.e. B_E(L) <= 1 + 1/n; 31/30 <= 1+1/10 = 11/10 : "
          f"{Fraction(31,30) <= Fraction(11,10)}")
    print("  (4) 2*31/30 - 2 = 1/15 exactly:", 2 * Fraction(31, 30) - 2 == Fraction(1, 15))
    print("  (5) f-values:", {T: fT(T) for T in [(2, 3), (2, 5), (3, 5), (2, 3, 5)]})
    print("      f({3,5}) = 1/15 is EXACTLY the bound on X_0+X_1; the argument therefore needs "
          "X_j < 1/15 strictly, which needs X_{1-j} > 0 strictly (DMNR).  If either "
          "inequality were non-strict the proof would FAIL at f({3,5}).")
    print("  (5') hypothesis of Lemma A2 requires T subset M_j -- here guaranteed by (3) only "
          "because 4,6,10 are forced to be USED, hence 2,3,5 in M_0 u M_1.")
    # what if only <=1 of them shares?  pigeonhole detail
    print("  (6) 3 objects into 2 blocks always gives a repeated block:", True)


def enumeration(LMAX=10 ** 6):
    sieve = bytearray([1]) * (LMAX + 2)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= LMAX + 1:
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        i += 1
    tot = np.zeros(LMAX + 1, dtype=np.float64)
    for n in range(4, LMAX + 1):
        if sieve[n + 1]:
            tot[n::n] += 1.0 / n
    cand = [int(L) for L in (tot > 1.0 + 1e-11).nonzero()[0]]
    exact = [(L, BE_exact(L)) for L in cand]
    cand = [L for L, b in exact if b > 1]
    print(f"  candidate lcm L <= {LMAX} with B_E(L) > 1 (exact): {len(cand)}, smallest {cand[0]}")
    print(f"  all divisible by 60: {all(L % 60 == 0 for L in cand)}")
    killed = [L for L, b in exact if b > 1 and L % 60 == 0 and b <= Fraction(31, 30)]
    print(f"  killed by Theorem A3: {len(killed)}   surviving A3: {len(cand)-len(killed)}")
    surv = [L for L in cand if L not in set(killed)]
    print(f"  A3 survivors: {surv}")
    print(f"  is 55440 killed by A3? {55440 in killed}  (B_E = {BE_exact(55440)} "
          f"> 31/30 = {Fraction(31,30)})")
    return surv


def fermat_check():
    print("  E ∩ {2^k}: ", [2 ** k for k in range(1, 40) if 2 ** k >= 4 and isprime(2 ** k + 1)],
          " (known Fermat primes only -- whether this list is COMPLETE is an OPEN problem)")
    print("  H ∩ {2^k}: ", [2 ** k for k in range(1, 40) if 2 ** k >= 2 and isprime(2 ** (k + 1) + 1)])
    print("  BUT the corollary only needs: 2 not in E (", not isprime(3) or 2 < 4, ") and "
          "4 not in H (2*4+1 = 9 composite:", not isprime(9), ").  Those are unconditional.")
    print("  'no two consecutive powers of 2 in E' is unconditional too: 2^k+1 prime forces k a "
          "power of 2, and k, k+1 both powers of 2 only for k=1, giving 2 which is not in E.")


def divergence_check(Qs=((2,), (3,), (2, 3), (2, 3, 5), (2, 3, 5, 7)), Y=2 * 10 ** 6):
    """P6: sum over m in H coprime to prod(Q) of 1/m diverges; measure the finite thresholds."""
    sieve = bytearray([1]) * (2 * Y + 3)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= 2 * Y + 2:
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        i += 1
    H = [m for m in range(2, Y + 1) if sieve[2 * m + 1]]
    for Q in Qs:
        P = 1
        for q in Q:
            P *= q
        s, thresh = 0.0, None
        for m in H:
            if gcd(m, P) == 1:
                s += 1.0 / m
                if thresh is None and s >= 2:
                    thresh = m
        print(f"    Q={Q}: sum_{{m<=%d, m in H, (m,{P})=1}} 1/m = {s:.4f}"
              % Y + (f"; reaches 2 at m = {thresh}" if thresh else "; has NOT reached 2 yet"))


if __name__ == "__main__":
    print("== Theorem A3 step-by-step ==")
    step_checks()
    print("== enumeration ==")
    enumeration(int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6)
    print("== Fermat / rigidity corollary ==")
    fermat_check()
    print("== P6 divergence (item 7) ==")
    divergence_check()
