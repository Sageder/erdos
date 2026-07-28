"""
G_01_pools.py  -- Route G (Selfridge template surgery), step 1.

CLAIM TESTED (all exact, no floating point in any assertion):
  (a) E = {p-1 : p prime, p>=5} = {n>=4 : n+1 prime}; H = {m>=2 : 2m+1 prime}; E = 2*H.
  (b) The divisors d of 360 with d+1 prime are exactly {1,2,4,6,10,12,18,30,36,40,60,72,180}.
      Excluding d=1 the pool P360 = {2,4,6,10,12,18,30,36,40,60,72,180} has
      sum of reciprocals = 460/360 = 23/18.
  (c) Removing the modulus 2 leaves sum 280/360 = 7/9 < 1, so NO covering system with
      moduli among the divisors of 360 lying in E can exist (density bound).
  (d) The prompt's displayed initial segment of H omits 54 (2*54+1 = 109 is prime);
      correspondingly the displayed segment of E omits 108.
  (e) Structure lemma (checked numerically here on small cases, proved in FINDINGS.md):
      every element of E is even, so an E-covering splits into two DISJOINT H-coverings.

CONCLUSION (see printed output): (a)-(d) all VERIFIED.  In particular the divisor-of-360
world is dead once modulus 2 is removed, for a trivial density reason.
"""
from fractions import Fraction
from sympy import isprime, divisors

def E_upto(X):
    return [n for n in range(4, X + 1) if isprime(n + 1)]

def H_upto(X):
    return [m for m in range(2, X + 1) if isprime(2 * m + 1)]

def DE(L):
    """divisors of L that lie in E"""
    return [d for d in divisors(L) if d >= 4 and isprime(d + 1)]

def DH(L):
    """divisors of L that lie in H"""
    return [d for d in divisors(L) if d >= 2 and isprime(2 * d + 1)]

def rsum(S):
    return sum(Fraction(1, x) for x in S)

def main():
    print("=" * 78)
    print("(a) E and H")
    E = E_upto(120); H = H_upto(60)
    print("  E cap [4,120] =", E)
    print("  H cap [2, 60] =", H)
    assert [2 * m for m in H_upto(60)] == E_upto(120)
    print("  E = 2*H verified on [4,120]                                  OK")

    print()
    print("(d) prompt-list audit")
    prompt_H = [2,3,5,6,8,9,11,14,15,18,20,21,23,26,29,30,33,35,36,39,41,44,48,50,51,53,56]
    true_H = H_upto(56)
    print("  prompt H-list :", prompt_H)
    print("  computed H    :", true_H)
    missing = [m for m in true_H if m not in prompt_H]
    print("  MISSING from prompt's H list:", missing, " (2*54+1 =", 2*54+1,
          "isprime =", isprime(109), ")")
    assert missing == [54]
    print("  => prompt's H segment is wrong by exactly one element, 54.")
    print("  => correspondingly 108 = 2*54 belongs to E (109 prime).")

    print()
    print("=" * 78)
    print("(b) the divisor-of-360 pool")
    d360 = divisors(360)
    print("  divisors(360) =", d360)
    good = [d for d in d360 if isprime(d + 1)]
    print("  d | 360 with d+1 prime :", good)
    assert good == [1, 2, 4, 6, 10, 12, 18, 30, 36, 40, 60, 72, 180]
    P = [d for d in good if d > 1]
    print("  pool P360 (moduli > 1) :", P)
    s = rsum(P)
    print("  sum 1/d over P360      =", s, "=", 460, "/", 360, "?", s == Fraction(460, 360))
    assert s == Fraction(460, 360) == Fraction(23, 18)
    print("  numerically             =", float(s), "                        OK")

    print()
    print("(c) delete the modulus 2")
    P2 = [d for d in P if d != 2]
    s2 = rsum(P2)
    print("  pool without 2         :", P2)
    print("  sum 1/d                =", s2, "= 280/360 =", Fraction(280,360),
          "?", s2 == Fraction(280, 360))
    assert s2 == Fraction(280, 360) == Fraction(7, 9)
    print("  numerically             =", float(s2), "< 1  ==> IMPOSSIBLE (density)")
    print("  Deficit  1 - 7/9       =", 1 - s2, "= density of guaranteed-uncovered set")
    print("  i.e. at least", (1 - s2) * 360, "residues mod 360 must remain uncovered.")

    print()
    print("=" * 78)
    print("(e) halved world for L=360: the H-pool is the divisors of 180 in H")
    PH = DH(180)
    print("  D_H(180) =", PH, " sum =", rsum(PH), "=", float(rsum(PH)))
    assert PH == [2, 3, 5, 6, 9, 15, 18, 20, 30, 36, 90]
    assert rsum(PH) == Fraction(280, 180)
    print("  (2*this pool) = ", [2*m for m in PH], " = P360 minus {2}   OK")

    print()
    print("=" * 78)
    print("Budget table: for L (E-world lcm) the H-world lcm is M = L/2.")
    print("An E-covering with all moduli | L needs TWO DISJOINT H-coverings with moduli | M,")
    print("hence needs  sum_{m | M, 2m+1 prime, m>=2} 1/m  > 2.")
    hdr = f"{'M':>8} {'#D_H(M)':>8} {'sum 1/m':>14} {'float':>9}  D_H(M)"
    print(hdr)
    for M in [6, 12, 18, 24, 30, 36, 60, 90, 120, 180, 360, 720, 1260, 2520,
              5040, 27720, 55440, 720720]:
        P = DH(M)
        print(f"{M:>8} {len(P):>8} {str(rsum(P)):>14} {float(rsum(P)):>9.4f}  {P if len(P)<=16 else str(P[:16])+'...'}")
    print()
    print("ALL ASSERTIONS PASSED")

main()
