"""
ADVERSARIAL AUDIT 3b: a much harder counterexample hunt for Lemma A2, plus an independent
re-derivation of the STRENGTHENED A3 (M_A2plus.py) verdict on L = 55440.

Lemma A2 depends only on the MODULUS SET M (it is residue-free), so the sharp test is:
  for every modulus set M that admits SOME covering assignment, and every pairwise coprime
  T subset M, check  sum_M 1/m - 1  >=  f(T).
We enumerate modulus sets M inside divisor lattices and decide "does M admit a covering?" by an
exact DFS (cover the smallest uncovered residue, residue forced per modulus), which is complete.
"""
import sys, itertools
from fractions import Fraction
from math import gcd


def lcm(xs):
    L = 1
    for x in xs:
        L = L * x // gcd(L, x)
    return L


def fT(T):
    s = sum(Fraction(1, m) for m in T) - 1
    p = Fraction(1)
    for m in T:
        p *= Fraction(m - 1, m)
    return s + p


def admits_cover(M, L):
    """exact: is there a residue assignment to the moduli M making a covering of Z/L?"""
    M = sorted(M, reverse=True)
    n = len(M)

    def dfs(hit, i, remaining_recip):
        try:
            x = hit.index(0)
        except ValueError:
            return True
        if i == n:
            return False
        # budget prune: uncovered residues must be coverable
        unc = hit.count(0)
        if sum(L // m for m in M[i:]) < unc:
            return False
        for k in range(i, n):
            m = M[k]
            a = x % m
            M[i], M[k] = M[k], M[i]
            new = [t for t in range(a, L, m) if not hit[t]]
            for t in new:
                hit[t] = 1
            if dfs(hit, i + 1, 0):
                for t in new:
                    hit[t] = 0
                M[i], M[k] = M[k], M[i]
                return True
            for t in new:
                hit[t] = 0
            M[i], M[k] = M[k], M[i]
        return False

    return dfs(bytearray(L), 0, 0)


def hunt(Ls=(12, 24, 36, 48, 60, 72, 90, 120, 144, 180), kmax=6):
    tested = worst = 0
    worstdat = None
    ncov = 0
    for L in Ls:
        divs = [d for d in range(2, L + 1) if L % d == 0]
        for k in range(1, kmax + 1):
            for M in itertools.combinations(divs, k):
                s = sum(Fraction(1, m) for m in M)
                if s <= 1 or lcm(M) != L:
                    continue
                if not admits_cover(list(M), L):
                    continue
                ncov += 1
                X = s - 1
                for r in range(2, min(len(M), 5) + 1):
                    for T in itertools.combinations(M, r):
                        if any(gcd(a, b) != 1 for a, b in itertools.combinations(T, 2)):
                            continue
                        v = fT(T)
                        tested += 1
                        if X < v:
                            print("*** COUNTEREXAMPLE", M, T, X, v)
                            return
                        if worstdat is None or X - v < worstdat[0]:
                            worstdat = (X - v, M, T, X, v)
    print(f"  {ncov} modulus sets that ADMIT a covering; {tested} coprime subsets tested; "
          f"NO violation of Lemma A2.")
    print(f"  tightest: slack {worstdat[0]} at M={worstdat[1]} T={worstdat[2]} "
          f"X={worstdat[3]} f(T)={worstdat[4]}")


def a2plus_55440():
    """independent re-derivation of the strengthened-A3 kill of L_E = 55440."""
    from sympy import isprime
    LH = 27720
    S = sorted(m for m in range(2, LH + 1) if LH % m == 0 and isprime(2 * m + 1))
    B = sum(Fraction(1, m) for m in S)
    forced = [m for m in S if B - Fraction(1, m) <= 2]     # note: <= is the correct forcing test
    print(f"  L_E=55440: H-pool size {len(S)}, B = {B} = {float(B):.6f}, slack B-2 = "
          f"{B-2} = {float(B-2):.6f}")
    print(f"  forced moduli (B - 1/m <= 2): {forced}")

    def g(F):
        best = Fraction(0)
        F = sorted(F)
        for r in range(1, len(F) + 1):
            for T in itertools.combinations(F, r):
                if any(gcd(a, b) != 1 for a, b in itertools.combinations(T, 2)):
                    continue
                best = max(best, fT(T))
        return best

    best_min, arg = None, None
    for mask in range(1 << len(forced)):
        F0 = [forced[i] for i in range(len(forced)) if not (mask >> i) & 1]
        F1 = [forced[i] for i in range(len(forced)) if (mask >> i) & 1]
        tot = g(F0) + g(F1)
        if best_min is None or tot < best_min:
            best_min, arg = tot, (F0, F1)
    print(f"  min over 2-colourings of g(F_0)+g(F_1) = {best_min} = {float(best_min):.6f} "
          f"at {arg}")
    print(f"  KILL iff min > B-2 : {best_min} > {B-2} -> {best_min > B - 2}")


if __name__ == "__main__":
    print("== hardened Lemma A2 hunt ==")
    hunt()
    print("== strengthened A3 on L = 55440, re-derived ==")
    a2plus_55440()
