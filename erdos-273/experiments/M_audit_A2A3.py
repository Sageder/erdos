"""
INDEPENDENT AUDIT of Route A's Lemma A2 (forced overlap) and Theorem A3.

LEMMA A2 (as stated by route A).  Let M be the modulus set of a covering system of Z (distinct
moduli > 1) and let T subset M be PAIRWISE COPRIME.  Then
        X := sum_{m in M} 1/m - 1   >=   f(T) := sum_{m in T} 1/m - 1 + prod_{m in T}(1 - 1/m).

Proof re-derived here.  For a finite family S of chosen classes put
        g(S) = sum_{m in S} 1/m - dens( union of the classes in S ).
(i) g is non-decreasing under adding a class: adding a class of modulus m' raises the first term
    by 1/m' and the density by at most 1/m'.
(ii) g(M) = X, because the union is all of Z, of density 1.
(iii) For pairwise coprime T the events "x = a_m (mod m)" are INDEPENDENT by CRT, whatever the
    residues, so dens(union over T) = 1 - prod(1 - 1/m) EXACTLY.
Hence X = g(M) >= g(T) = sum_T 1/m - 1 + prod_T (1 - 1/m) = f(T).   []

THEOREM A3.  If 60 | L and 1 < B_E(L) <= 31/30, no covering system with distinct moduli in E has
lcm dividing L.  (B_E(L) = sum of 1/n over n | L with n in E.)
Proof re-derived here.  60 | L gives 4, 6, 10 | L and all three lie in E.  B_E(L) - 1 <= 1/30,
which is smaller than 1/10 <= 1/6 <= 1/4, so each of 4, 6, 10 is FORCED: deleting it would leave
reciprocal sum <= B_E(L) - 1/n < 1, too small to cover.  By the parity split their halves 2, 3, 5
lie in the two halves M_0, M_1, which are disjoint, so X_0 + X_1 <= B_H(L) - 2 = 2 B_E(L) - 2
<= 1/15, and each X_c > 0 strictly (DMNR), so each X_c < 1/15.  The numbers 2, 3, 5 are pairwise
coprime and f({2,3}) = 1/6, f({2,5}) = 1/10, f({3,5}) = 1/15.  If two of them lay in the same
half M_c then A2 would give X_c >= 1/15, contradicting X_c < 1/15.  So 2, 3, 5 lie in three
pairwise different halves - impossible, there are only two.   []

THIS SCRIPT: (1) re-derives f, (2) tests Lemma A2 by brute force on many explicit covering
systems, hunting for a counterexample, (3) re-checks the arithmetic of A3, (4) re-runs the
enumeration of candidate lcm values and the kill count.

CONCLUSION: printed.
"""
from fractions import Fraction
from math import gcd, lcm
from itertools import combinations
import random
from sympy import isprime


def f(T):
    s = sum(Fraction(1, m) for m in T) - 1
    p = Fraction(1)
    for m in T:
        p *= Fraction(m - 1, m)
    return s + p


def covers(classes):
    L = 1
    for _, n in classes:
        L = lcm(L, n)
    cov = bytearray(L)
    for a, n in classes:
        for r in range(a % n, L, n):
            cov[r] = 1
    return all(cov), L


def test_A2(trials=4000, seed=20260728):
    """hunt for a counterexample to Lemma A2 among random covering systems."""
    rng = random.Random(seed)
    found, worst = 0, None
    for _ in range(trials):
        # build a random covering system with distinct moduli by brute force on a small lattice
        L = rng.choice([12, 24, 36, 48, 60, 72, 120, 180])
        divs = [d for d in range(2, L + 1) if L % d == 0]
        rng.shuffle(divs)
        chosen, cov = [], bytearray(L)
        for d in divs:
            a = rng.randrange(d)
            chosen.append((a, d))
            for r in range(a, L, d):
                cov[r] = 1
            if all(cov):
                break
        if not all(cov):
            continue
        M = [n for _, n in chosen]
        X = sum(Fraction(1, n) for n in M) - 1
        for t in range(2, min(4, len(M)) + 1):
            for T in combinations(sorted(M), t):
                ok = all(gcd(x, y) == 1 for x, y in combinations(T, 2))
                if not ok:
                    continue
                found += 1
                if X < f(T):
                    print("  *** COUNTEREXAMPLE to A2:", chosen, "T =", T, "X =", X, "f =", f(T))
                    return False
                slack = X - f(T)
                if worst is None or slack < worst[0]:
                    worst = (slack, tuple(sorted(M)), T)
    print(f"  A2: {found} (covering system, coprime subset) pairs tested, NO counterexample.")
    print(f"      tightest instance: X - f(T) = {worst[0]} for T = {worst[2]}")
    return True


def BE(L):
    return sum(Fraction(1, n) for n in range(4, L + 1) if L % n == 0 and isprime(n + 1))


def main():
    print("f({2,3}) =", f([2, 3]), " f({2,5}) =", f([2, 5]), " f({3,5}) =", f([3, 5]))
    assert f([2, 3]) == Fraction(1, 6) and f([2, 5]) == Fraction(1, 10) and f([3, 5]) == Fraction(1, 15)
    print("  matches route A's values.  min over pairs = 1/15; A3 threshold 1 + 1/30 = 31/30.\n")

    print("Testing Lemma A2 by brute force:")
    assert test_A2()

    print("\nRe-checking Theorem A3's forcing step at the threshold B_E = 31/30:")
    for n in (4, 6, 10):
        print(f"   dropping {n}: 31/30 - 1/{n} = {Fraction(31,30)-Fraction(1,n)} "
              f"= {float(Fraction(31,30)-Fraction(1,n)):.4f} < 1 -> {n} is forced  "
              f"{'OK' if Fraction(31,30)-Fraction(1,n) < 1 else 'FAIL'}")
        assert Fraction(31, 30) - Fraction(1, n) < 1

    print("\nEnumerating candidate lcm values L <= 10^6 with B_E(L) > 1, and applying A3:")
    import numpy as np
    LMAX = 10 ** 6
    bs = bytearray([1]) * (LMAX + 2)
    bs[0] = bs[1] = 0
    i = 2
    while i * i <= LMAX + 1:
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
        i += 1
    adm = [n for n in range(4, LMAX + 1) if bs[n + 1]]
    tot = np.zeros(LMAX + 1)
    for n in adm:
        tot[n::n] += 1.0 / n
    cand = [int(L) for L in np.flatnonzero(tot > 1.0 + 1e-12)]
    print(f"   #L <= 10^6 with B_E(L) > 1: {len(cand)}   smallest = {cand[0]}")
    all60 = all(L % 60 == 0 for L in cand)
    print(f"   every candidate divisible by 60? {all60}")
    killed = [L for L in cand if BE(L) <= Fraction(31, 30)]
    surv = [L for L in cand if BE(L) > Fraction(31, 30)]
    print(f"   killed by A3: {len(killed)}   surviving: {len(surv)}")
    print(f"   survivors: {surv}")
    print("\nNOTE: 55440 has B_E = %s > 31/30, so A3 does NOT kill it; it is killed instead by the"
          % BE(55440))
    print("      fiber condition Phi_5 < 2 (experiments/M_audit_phi.py). The two tools are"
          " complementary.")


if __name__ == "__main__":
    main()
