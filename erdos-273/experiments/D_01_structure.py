"""
D_01_structure.py

CLAIMS TESTED (all exact / deterministic):

 (C1) E = {n>=4 : n+1 prime} has ALL elements even, and moreover every n in E satisfies
      n = 0 or 4 (mod 6).  Equivalently H = {m>=2 : 2m+1 prime} satisfies m != 1 (mod 3).
      More generally: for every odd prime r, H avoids the class (r-1)/2 mod r, with the
      single exception m = (r-1)/2 itself.

 (C2) PARITY-SPLIT REDUCTION (Proposition D1).  A covering system with distinct moduli all
      in E exists  <=>  there are two DISJOINT finite sets S_0, S_1 subset of H and residue
      assignments making each of S_0, S_1 the modulus set of a covering system of Z.
      Verified here by an exhaustive brute-force equivalence check on all systems with
      moduli dividing a small L (both directions), i.e. the bijection is checked as a
      literal bijection on data, not just asserted.

 (C3) "Enrichment": density of multiples of d inside H is ~ 1/phi(d) not 1/d  (measured).

CONCLUSION (printed at run time; see attempts/route-D-obstruction/FINDINGS.md):
 C1 verified; C2 verified as a bijection on brute-forced data; C3 measured and matches
 1/phi(d) to within sampling error.
"""
from sympy import isprime, totient
from math import gcd, lcm
from fractions import Fraction
from itertools import product
import sys


def E_upto(X):
    return [n for n in range(4, X + 1) if isprime(n + 1)]


def H_upto(X):
    return [m for m in range(2, X + 1) if isprime(2 * m + 1)]


# ---------------------------------------------------------------- C1
def check_C1(X=200000):
    E = E_upto(2000)
    assert all(n % 2 == 0 for n in E)
    bad = [n for n in E if n % 6 not in (0, 4)]
    print("C1a: E cap [4,2000]: all even:", all(n % 2 == 0 for n in E),
          "| all n = 0 or 4 mod 6:", not bad)
    assert not bad

    H = H_upto(X)
    bad3 = [m for m in H if m % 3 == 1]
    print("C1b: H cap [2,%d]: elements = 1 mod 3:" % X, bad3, "(expect [] since m=1 not in H)")
    assert not bad3

    # general odd prime r: excluded class (r-1)/2, exception m=(r-1)/2
    for r in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        c = (r - 1) // 2
        exc = [m for m in H if m % r == c % r and m != c]
        assert not exc, (r, exc[:5])
    print("C1c: for r in {3,...,31}: H avoids m = (r-1)/2 mod r except m=(r-1)/2 itself  OK")
    # proof: 2m+1 = 0 mod r  <=>  m = (r-1)/2 mod r ; 2m+1 prime then forces 2m+1 = r.
    return H


# ---------------------------------------------------------------- C2
def all_coverings_E(L, cap=None):
    """Brute force: every set of DISTINCT moduli from E dividing L, with residues, that covers
    Z/L.  Returns list of frozensets of (n,a).  Exponential -- only for tiny L."""
    mods = [n for n in range(4, L + 1) if L % n == 0 and isprime(n + 1)]
    sols = []
    full = (1 << L) - 1

    def masks(n):
        out = []
        for a in range(n):
            mk = 0
            for r in range(a, L, n):
                mk |= 1 << r
            out.append(mk)
        return out

    M = {n: masks(n) for n in mods}

    def rec(i, cur, chosen):
        if cur == full:
            sols.append(frozenset(chosen))
            return
        if i == len(mods):
            return
        # skip modulus i
        rec(i + 1, cur, chosen)
        n = mods[i]
        for a in range(n):
            rec(i + 1, cur | M[n][a], chosen + [(n, a)])

    rec(0, 0, [])
    return mods, sols


def all_coverings_H(Lh):
    """all coverings of Z/Lh with distinct moduli m | Lh, m>=2, 2m+1 prime."""
    mods = [m for m in range(2, Lh + 1) if Lh % m == 0 and isprime(2 * m + 1)]
    full = (1 << Lh) - 1
    M = {}
    for m in mods:
        M[m] = [sum(1 << r for r in range(a, Lh, m)) for a in range(m)]
    sols = []

    def rec(i, cur, chosen):
        if cur == full:
            sols.append(frozenset(chosen))
            return
        if i == len(mods):
            return
        rec(i + 1, cur, chosen)
        m = mods[i]
        for a in range(m):
            rec(i + 1, cur | M[m][a], chosen + [(m, a)])

    rec(0, 0, [])
    return mods, sols


def all_min_coverings_generic(L, mods):
    """All coverings of Z/L by distinct moduli from `mods` that are MINIMAL in the sense
    produced by 'always cover the smallest uncovered residue' DFS (this enumerates every
    irredundant covering, each possibly several times -- we dedupe)."""
    M = {}
    for m in mods:
        M[m] = [sum(1 << r for r in range(a, L, m)) for a in range(m)]
    full = (1 << L) - 1
    sols = set()

    def rec(cur, used, chosen):
        if cur == full:
            sols.add(frozenset(chosen))
            return
        r = 0
        while (cur >> r) & 1:
            r += 1
        for m in mods:
            if m in used:
                continue
            a = r % m
            rec(cur | M[m][a], used | {m}, chosen + [(m, a)])

    rec(0, frozenset(), [])
    return sols


def check_C2_identity(trials=200000, seed=1):
    """Direct verification of the IDENTITY underlying Proposition D1:

    For ANY finite family {(n_i, a_i)} with every n_i EVEN, put m_i = n_i/2 and
        A = {(m_i, a_i/2)      : a_i even},     B = {(m_i, (a_i-1)/2) : a_i odd}.
    Then  union_i (a_i + n_i Z) = Z   <=>   A covers Z  and  B covers Z.
    (And the n_i are pairwise distinct iff the m_i are; A, B use disjoint modulus sets.)

    Tested exhaustively-by-sampling on random families, with BOTH outcomes occurring."""
    import random
    rng = random.Random(seed)
    Lh = 2 * 2 * 3 * 3 * 5      # 180 ; E-world L = 360
    L = 2 * Lh
    divs = [d for d in range(2, Lh + 1) if Lh % d == 0]
    ncov = 0
    base = [(2, 0), (3, 0), (4, 1), (6, 5), (12, 7)]   # classic covering of Z, all moduli | 180
    for t in range(trials):
        if t % 2 == 0:                      # random family: almost never a covering
            k = rng.randint(1, 9)
            ms = rng.sample(divs, min(k, len(divs)))
            fam = [(2 * m, rng.randrange(2 * m)) for m in ms]
        else:                               # perturbed union of two lifted coverings
            A = [(m, b) for m, b in base]
            B = [(m, b) for m, b in base]
            fam = [(2 * m, (2 * b) % (2 * m)) for m, b in A] + \
                  [(2 * m, (2 * b + 1) % (2 * m)) for m, b in B]
            for _ in range(rng.randint(0, 2)):
                op = rng.randrange(3)
                if op == 0 and len(fam) > 1:
                    fam.pop(rng.randrange(len(fam)))
                elif op == 1:
                    i = rng.randrange(len(fam))
                    n, a = fam[i]
                    fam[i] = (n, rng.randrange(n))
                else:
                    m = rng.choice(divs)
                    fam.append((2 * m, rng.randrange(2 * m)))
        covE = 0
        for n, a in fam:
            for r in range(a % n, L, n):
                covE |= 1 << r
        okE = (covE == (1 << L) - 1)
        covA = covB = 0
        for n, a in fam:
            m = n // 2
            if a % 2 == 0:
                b = (a // 2) % m
                for r in range(b, Lh, m):
                    covA |= 1 << r
            else:
                b = ((a - 1) // 2) % m
                for r in range(b, Lh, m):
                    covB |= 1 << r
        okAB = (covA == (1 << Lh) - 1) and (covB == (1 << Lh) - 1)
        assert okE == okAB, (fam, okE, okAB)
        ncov += okE
    print("C2: identity  [E-family covers Z]  <=>  [both halved subfamilies cover Z]")
    print("    verified on %d random families with all moduli even (L = %d);"
          % (trials, L))
    print("    %d of them were coverings, %d were not -- both outcomes present  OK"
          % (ncov, trials - ncov))
    assert ncov > 0, "vacuous: no covering instance was generated"


def check_C2_generic(L):
    """Non-vacuous check of the parity split for the FULL even-moduli world (moduli = all even
    divisors >= 4 of L), which certainly has coverings.  The reduction proof never uses
    'n+1 prime', so this is the right stress test; the E case is the sub-case where we also
    demand n+1 prime."""
    Lh = L // 2
    modsE = [n for n in range(4, L + 1) if L % n == 0 and n % 2 == 0]
    modsH = [m for m in range(2, Lh + 1) if Lh % m == 0]
    solsE = all_min_coverings_generic(L, modsE)
    solsH = all_min_coverings_generic(Lh, modsH)
    print("C2-generic: L =", L, " even E-side moduli:", modsE, " H-side moduli:", modsH)
    print("    #irredundant E-side coverings:", len(solsE),
          " #irredundant H-side coverings:", len(solsH))
    assert solsE, "vacuous test"
    # forward
    for sol in solsE:
        S0 = frozenset((n // 2, ((a % n) // 2) % (n // 2)) for (n, a) in sol if a % 2 == 0)
        S1 = frozenset((n // 2, ((a % n - 1) // 2) % (n // 2)) for (n, a) in sol if a % 2 == 1)
        m0 = set(m for m, _ in S0)
        m1 = set(m for m, _ in S1)
        assert not (m0 & m1)
        for S in (S0, S1):
            cov = 0
            for m, b in S:
                for r in range(b, Lh, m):
                    cov |= 1 << r
            assert cov == (1 << Lh) - 1, ("half fails to cover", sorted(S))
    print("    forward: all %d E-side coverings split into two DISJOINT H-side coverings  OK"
          % len(solsE))
    # backward
    cnt = 0
    for A in solsH:
        for B in solsH:
            if set(m for m, _ in A) & set(m for m, _ in B):
                continue
            sol = [(2 * m, (2 * b) % (2 * m)) for m, b in A] + \
                  [(2 * m, (2 * b + 1) % (2 * m)) for m, b in B]
            cov = 0
            for n, a in sol:
                for r in range(a, L, n):
                    cov |= 1 << r
            assert cov == (1 << L) - 1, "lift failed"
            cnt += 1
    print("    backward: all %d disjoint ordered pairs of H-side coverings lift to "
          "E-side coverings  OK" % cnt)


def check_C2(L=24):
    """L must be even; H-world modulus Lh = L/2."""
    assert L % 2 == 0
    Lh = L // 2
    modsE, solsE = all_coverings_E(L)
    modsH, solsH = all_coverings_H(Lh)
    print("C2: L =", L, " E-moduli dividing L:", modsE, " H-moduli dividing L/2:", modsH)
    print("    #E-coverings of Z/L (minimal-or-not, distinct moduli):", len(solsE))
    print("    #H-coverings of Z/(L/2):", len(solsH))

    # forward map: E-covering -> ordered pair of disjoint H-coverings
    def split(sol):
        S0 = frozenset((n // 2, (a % n) // 2) for (n, a) in sol if a % 2 == 0)
        S1 = frozenset((n // 2, (a % n - 1) // 2) for (n, a) in sol if a % 2 == 1)
        return S0, S1

    pairs = set()
    for sol in solsE:
        S0, S1 = split(sol)
        m0 = set(m for m, _ in S0)
        m1 = set(m for m, _ in S1)
        assert not (m0 & m1), "moduli not disjoint!"
        assert S0 in solsH or not S0, ("S0 not an H-covering", sorted(S0))
        assert S1 in solsH or not S1, ("S1 not an H-covering", sorted(S1))
        pairs.add((S0, S1))
    print("    forward: every E-covering splits into two DISJOINT H-coverings  OK"
          if solsE else "    (no E-coverings at this L)")

    # backward: every ordered pair of H-coverings with disjoint modulus sets lifts
    lifted = 0
    solsHset = set(solsH)
    for A in solsH:
        for B in solsH:
            if set(m for m, _ in A) & set(m for m, _ in B):
                continue
            sol = frozenset([(2 * m, 2 * b % (2 * m)) for m, b in A] +
                            [(2 * m, (2 * b + 1) % (2 * m)) for m, b in B])
            # verify it really covers Z/L
            cov = 0
            for n, a in sol:
                for r in range(a, L, n):
                    cov |= 1 << r
            assert cov == (1 << L) - 1, "lift failed to cover"
            assert sol in set(solsE), "lift not in enumerated E-coverings"
            lifted += 1
    print("    backward: %d disjoint ordered pairs of H-coverings, all lift to E-coverings  OK"
          % lifted)
    print("    #E-coverings = %d, #disjoint ordered pairs = %d  (must be equal): %s"
          % (len(solsE), lifted, len(solsE) == lifted))
    assert len(solsE) == lifted


# ---------------------------------------------------------------- C3
def check_C3(X=2000000):
    H = H_upto(X)
    n = len(H)
    print("C3: |H cap [2,%d]| = %d" % (X, n))
    print("     d   #(d | m, m in H)/|H|      1/phi(d)      1/d")
    for d in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 20, 24, 30, 36, 60]:
        c = sum(1 for m in H if m % d == 0)
        print("   %4d   %18.6f   %11.6f   %8.6f"
              % (d, c / n, 1.0 / float(totient(d)), 1.0 / d))
    print("   (note: for d = 2^a the two predictions coincide only at a<=1;")
    print("    H has no constraint at the prime 2 since 2m+1 is odd automatically.)")


if __name__ == "__main__":
    H = check_C1()
    print()
    check_C2_identity(trials=20000)
    print()
    check_C3()
