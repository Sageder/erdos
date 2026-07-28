"""
theorem_A.py -- THE h=0 TERM IS NEVER A MAIN TERM (in the full-lcm normalisation).

SETTING.  I = [T,N] cap Z, M = N-T+1, L = lcm(I), w_n = L/n in Z.
For a family F of subsets of I put
        Phi_F(h) = sum_{U in F} prod_{n in U} e(h/n),      e(x) = exp(2 pi i x),
which is well defined for h in Z/L because  h/n = h*w_n/L.
Orthogonality on Z/L gives the EXACT identity

  (1/L) sum_{h mod L} Phi_F(h) = #{ U in F : sum_{n in U} 1/n is an integer }.  (*)

If moreover H(T,N) < 2 and F contains the empty set, the right side is
  1 + #{U in F : sum_{n in U} 1/n = 1}.
The "h = 0" term of (*) is  Phi_F(0)/L = |F| / L.  This is what a circle-method
proof would want to be the main term.

THEOREM A.  For every T >= 1 and N > T, with M = N-T+1:
  (A1)  lcm(1,...,M)  divides  lcm(T,...,N).
  (A2)  lcm(1,...,M) >= 2^{M-1}.
  (A3)  hence for ANY family F of subsets of [T,N]:   |F|/L <= 2^M/2^{M-1} = 2.
  (A4)  the number of LEGAL subsets of an interval of length M satisfies
        a(M) <= (351/200)^M,  so for F = legal subsets:
              |F|/L <= 2 * (351/400)^M  ->  0   exponentially (ratio 0.8775).

PROOFS.
 (A1) For a prime power q <= M, the interval [T,N] has length M >= q, hence
      contains a multiple of q; so nu_p(lcm[T,N]) >= nu_p(lcm[1,M]) for all p.
 (A2) Classical: for 0 <= m <= n,
        int_0^1 x^m (1-x)^{n-m} dx = 1/((n+1) binom(n,m)),
      and expanding (1-x)^{n-m} the integral is a rational with denominator
      dividing lcm(1..n+1); hence (n+1) binom(n,m) divides lcm(1..n+1).
      Taking m = floor(n/2) gives lcm(1..n+1) >= (n+1) binom(n,floor(n/2)) >= 2^n.
      Put n = M-1.
 (A3) |F| <= 2^M.
 (A4) Exact rational Perron certificate, verified below:  with mu = 351/200 and
      w = (mu-1, 1/mu, 1)^T one has A w <= mu w entrywise for the transfer
      matrix A = [[1,1,0],[0,0,1],[1,0,1]] -- this is equivalent to
      mu^3 - 2 mu^2 + mu - 1 >= 0 -- and the accept vector (1,0,1)^T <= (200/151) w,
      while the start vector picks out w_0 = 151/200.  Hence
      a(M) = e_0 A^M (1,0,1)^T <= (200/151) mu^M w_0 = mu^M.

CONSEQUENCE.  In the normalisation proposed for the circle method (full modulus
L = lcm(T..N)), the h = 0 term is bounded by the absolute constant 2 for *any*
family whatsoever, and tends to 0 exponentially for the legal family.  Since the
count on the left of (*) is >= 1 whenever a solution exists, the ENTIRE count
comes from h != 0.  No "main term dominates the minor arcs" argument can exist
in this normalisation.  (This is a proof, not a heuristic.)
"""
from fractions import Fraction
from core import (legal_count_interval, lcm_interval, primes_upto, report_log)

MU = Fraction(351, 200)


def check_perron_certificate():
    mu = MU
    # A w <= mu w  with w = (mu-1, 1/mu, 1)
    w = [mu - 1, 1 / mu, Fraction(1)]
    Aw = [w[0] + w[1], w[2], w[0] + w[2]]
    ok = all(Aw[i] <= mu * w[i] for i in range(3))
    charpoly = mu ** 3 - 2 * mu ** 2 + mu - 1
    return ok, charpoly, w


def check_aM_bound(Mmax=400):
    bad = []
    for M in range(0, Mmax + 1):
        if Fraction(legal_count_interval(M)) > MU ** M:
            bad.append(M)
    return bad


def check_A1(cases):
    bad = []
    for (T, N) in cases:
        M = N - T + 1
        if lcm_interval(T, N) % lcm_interval(1, M) != 0:
            bad.append((T, N))
    return bad


def check_A2(Mmax=400):
    bad = [M for M in range(1, Mmax + 1) if lcm_interval(1, M) < 2 ** (M - 1)]
    return bad


def main():
    ok, cp, w = check_perron_certificate()
    print("A4 Perron certificate  A w <= mu w  with mu = 351/200 :", ok)
    print("   mu^3-2mu^2+mu-1 =", cp, "( > 0 required ) ->", cp > 0)
    bad = check_aM_bound(400)
    print("A4 a(M) <= (351/200)^M verified for 0<=M<=400, counterexamples:", bad)

    bad = check_A2(400)
    print("A2 lcm(1..M) >= 2^(M-1) verified for 1<=M<=400, counterexamples:", bad)

    cases = [(T, N) for T in (2, 5, 10, 50, 100, 300) for N in (T + 5, T + 20, 2 * T, 4 * T)]
    bad = check_A1(cases)
    print("A1 lcm(1..M) | lcm(T..N) verified on", len(cases), "cases, bad:", bad)

    print()
    print("EXACT h=0 TERM  a(M)/lcm(T..N)  (legal family).  log = natural log,")
    print("computed from exact integers (reporting only); the COMPARISON is exact.")
    print(f"{'T':>7} {'N':>7} {'M':>6} {'log a(M)':>10} {'log L':>10} {'log(a/L)':>10}  a(M) < L ?")
    for (T, N) in [(2, 85), (2, 200), (100, 400), (100, 900), (1000, 4000),
                   (10 ** 4, 4 * 10 ** 4)]:
        M = N - T + 1
        a = legal_count_interval(M)
        L = lcm_interval(T, N)
        print(f"{T:>7} {N:>7} {M:>6} {report_log(a):10.2f} {report_log(L):10.2f} "
              f"{report_log(a) - report_log(L):10.2f}  {a < L}")

    print()
    print("Uniform bound: for ANY family F of subsets of [T,N], |F|/L <= 2.")
    print("For the legal family, |F|/L <= 2*(351/400)^M, ratio =", float(Fraction(351, 400)))


if __name__ == "__main__":
    main()
