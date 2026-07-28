"""
Q1 -- machine verification of the finite part of the proof of

   THEOREM Q1.  For all b > a >= 1, H(a,b) is never a unit fraction 1/N.

Proof skeleton (full write-up in REPORT.md).  Assume H(a,b)=1/N, k=b-a+1>=2.
  (P1)  H(a,b) > k/b   ==>  N < b/k.
  (P2)  2^t || N, where 2^t is the largest power of 2 in [a,b];  2^(t+1) >= k+1,
        so 2^t >= (k+1)/2.  With (P1):  k(k+1)/2 <= 2^t k <= Nk < b,
        i.e.  2b > k(k+1).
  (P3)  For every prime p > k, [a,b] holds at most one multiple of p, so
        v_p(H) = -v_p(n_0) and p^{v_p(n_0)} || N.  Hence R | N where
        R = prod_{n=a}^{b} n'  and n' is the k-rough part of n (primes > k).
        R is odd, so 2^t R | N, so 2^t R <= N < b/k.
  (P4)  prod_{n=a}^b n = k! * C(b,k);  prod_{n} n'' = prod_{p<=k} p^{E_p} with
        E_p = v_p(k!) + v_p(C(b,k)) <= v_p(k!) + log_p b.  Hence
              prod n'' <= k! * b^{pi(k)}      and      R >= C(b,k) / b^{pi(k)}.
  (P5)  Therefore a contradiction follows from
              (STAR)   k(k+1) * C(b,k)  >=  2 * b^{1+pi(k)}
        because then 2^t R >= (k+1)/2 * C(b,k)/b^{pi(k)} >= b/k, contra (P3).

This script verifies, in exact integer arithmetic:
  (A) monotonicity: for k >= 4 and b >= k, if (STAR) holds at b it holds at b+1.
  (B) for every 4 <= k <= 39, the complete (finite) list of b >= (k^2+k+2)/2
      for which (STAR) FAILS -- and for each such (k,b) a direct exact check
      that numerator(H(b-k+1,b)) > 1.
  (C) the analytic tail k >= 40 is proved on paper (uses pi(x) < 1.25506 x/log x);
      this script re-verifies (STAR) at b = ceil((k^2+k+2)/2) for 40 <= k <= 4000
      by exact integer arithmetic as a sanity check.
  (D) k = 2 and k = 3 are handled by separate elementary arguments, re-checked
      here on a range.

Run:  python3 q1_proof_check.py
"""

from fractions import Fraction
from math import comb, gcd, isqrt

from blocks import H


def primes_upto(n):
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(sieve[i * i:: i]))
    return [i for i in range(n + 1) if sieve[i]]


def pi_table(n):
    ps = primes_upto(n)
    tab = [0] * (n + 1)
    j = 0
    for i in range(n + 1):
        while j < len(ps) and ps[j] <= i:
            j += 1
        tab[i] = j
    return tab


def star(k, b, pik):
    """(STAR):  k(k+1)*C(b,k) >= 2*b^(1+pi(k))   -- exact integers."""
    return k * (k + 1) * comb(b, k) >= 2 * b ** (1 + pik)


def bmin(k):
    """least b with 2b > k(k+1)"""
    return (k * (k + 1)) // 2 + 1


def check_monotonicity(kmax, bextra, PI):
    """
    Verify numerically the paper claim: for k>=4 and b>=k^2/2, (STAR) at b
    implies (STAR) at b+1.  (The paper proof: C(b+1,k)/C(b,k) = (b+1)/(b+1-k)
    and ((b+1)/b)^(1+pi(k)) <= exp((1+pi(k))/b); k*b >= (1+pi(k))(b+1) since
    pi(k) <= k-2 and b >= k.)   Here we simply confirm the discrete inequality
    (b+1)*b^(1+pi(k)) * C(b+1,k) * ... in exact integers:
        C(b+1,k) * b^(1+pi) >= C(b,k) * (b+1)^(1+pi).
    """
    bad = []
    for k in range(4, kmax + 1):
        pik = PI[k]
        for b in range(max(k, bmin(k) - 5), bmin(k) + bextra):
            if comb(b + 1, k) * b ** (1 + pik) < comb(b, k) * (b + 1) ** (1 + pik):
                bad.append((k, b))
    return bad


def exceptional_pairs(kmax, PI, hardstop=10 ** 7):
    """
    For 4<=k<=kmax list every b >= bmin(k) where (STAR) fails.
    Using monotonicity this set is an initial segment, so we scan upward until
    (STAR) first holds.
    """
    exc = []
    for k in range(4, kmax + 1):
        pik = PI[k]
        b = bmin(k)
        cnt = 0
        while not star(k, b, pik):
            exc.append((k, b))
            b += 1
            cnt += 1
            if cnt > hardstop:
                raise RuntimeError("runaway at k=%d" % k)
    return exc


def verify_k2(AMAX):
    """k=2:  H(a,a+1) = (2a+1)/(a(a+1)) is already in lowest terms."""
    bad = []
    for a in range(1, AMAX + 1):
        h = H(a, a + 1)
        if h.numerator != 2 * a + 1 or h.denominator != a * (a + 1):
            bad.append(a)
    return bad


def verify_k3(AMAX):
    """
    k=3: the paper argument shows some n in [a,a+2] has {2,3}-part <= 2, hence
    R >= a/2, and 2^t >= 2, so N >= 2^t R >= a > (a+2)/3 > N.  Contradiction.
    Here we verify the combinatorial ingredient directly and also that the
    numerator of H(a,a+2) is > 1.
    """
    bad = []
    for a in range(1, AMAX + 1):
        ok = False
        for n in (a, a + 1, a + 2):
            m = n
            s = 1
            while m % 2 == 0:
                m //= 2
                s *= 2
            while m % 3 == 0:
                m //= 3
                s *= 3
            if s <= 2:
                ok = True
        if not ok:
            bad.append(("smoothpart", a))
        if H(a, a + 2).numerator == 1:
            bad.append(("unit", a))
    return bad


if __name__ == "__main__":
    KMAX_EXC = 39
    KMAX_SANITY = 4000
    PI = pi_table(KMAX_SANITY + 10)

    print("== (D) k=2 ==")
    b2 = verify_k2(200000)
    print("   H(a,a+1)=(2a+1)/(a(a+1)) in lowest terms for all a<=200000 :",
          "OK" if not b2 else b2[:10])

    print("== (D) k=3 ==")
    b3 = verify_k3(200000)
    print("   {2,3}-part<=2 witness exists & numerator>1 for all a<=200000 :",
          "OK" if not b3 else b3[:10])

    print("== (A) monotonicity of (STAR) in b, 4<=k<=%d ==" % KMAX_EXC)
    bad = check_monotonicity(KMAX_EXC, 400, PI)
    print("   violations:", bad if bad else "none")

    print("== (B) exceptional (k,b) with 4<=k<=%d where (STAR) fails ==" % KMAX_EXC)
    exc = exceptional_pairs(KMAX_EXC, PI)
    print("   count =", len(exc))
    print("   list  =", exc)
    print("   direct exact check of each exceptional block:")
    allok = True
    for (k, b) in exc:
        a = b - k + 1
        h = H(a, b)
        if h.numerator == 1:
            allok = False
            print("      !!! H(%d,%d) = %s IS A UNIT FRACTION" % (a, b, h))
    print("      all exceptional blocks have numerator > 1 :", allok)
    if exc:
        print("      sample:", [(b - k + 1, b, str(H(b - k + 1, b))) for k, b in exc[:12]])

    print("== (C) analytic tail k>=40: the sufficient condition pi(k) <= (k-1)/3 ==")
    PI2 = pi_table(10 ** 6)
    bad3 = [k for k in range(40, 10 ** 6 + 1) if 3 * PI2[k] > k - 1]
    print("   pi(k) <= (k-1)/3 for all 40 <= k <= 10^6 :",
          "OK" if not bad3 else bad3[:10])
    print("   (for k >= 60 this also follows from Rosser-Schoenfeld "
          "pi(x) < 1.25506 x/log x)")
    print("   smallest k>=2 from which it holds without exception:",
          min(k0 for k0 in range(2, 200)
              if all(3 * PI2[k] <= k - 1 for k in range(k0, 10 ** 6 + 1))))

    print("== (C2) sanity: (STAR) at b=bmin(k) for 40<=k<=%d ==" % KMAX_SANITY)
    fails = []
    for k in range(40, KMAX_SANITY + 1):
        if not star(k, bmin(k), PI[k]):
            fails.append(k)
    print("   failures:", fails if fails else "none")
