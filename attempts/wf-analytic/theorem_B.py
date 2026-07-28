"""
theorem_B.py -- REPAIRING THE CIRCLE METHOD: the SMOOTH UNIVERSE.

Theorem A says the h=0 term of the circle method over the full interval [T,N]
with modulus L = lcm(T..N) is <= 2 always, and -> 0 for legal sets.  The reason
is purely that log L ~ N while the entropy of legal sets is only
(log lambda)(N-T) < (log 2)(N-T).

Theorem C says NOTHING IS LOST by deleting from the universe every n with a
prime factor > y(T,N) ~ N/log N: no solution ever uses such an n.

So run the circle method over
        V = V(T,N,y) = { n in [T,N] : P^+(n) <= y },      Lambda = lcm(V).
Every n in V divides Lambda, so for U subset V the integer X_U = sum_{n in U} Lambda/n
is defined and  sum_{n in U} 1/n in Z  <=>  Lambda | X_U.  Orthogonality on Z/Lambda:

  EXACT IDENTITY (B):
      (1/Lambda) sum_{h mod Lambda} G(h)  =  #{legal U subset V : sum 1/n in Z},
      G(h) = sum_{legal U subset V} prod_{n in U} e(h/n),  G(0) = #legal(V).

  If H(T,N) < 2 the right-hand side equals 1 + #{solutions in [T,N]} (Thm C).

THEOREM B (verified exactly below for explicit (T,N,y)).
      G(0)/Lambda = #legal(V) / lcm(V)  is ASTRONOMICALLY LARGE
(e.g. > 10^600 already at (T,N) = (1000,4000)).
Asymptotically log #legal(V) = (log lambda + o(1)) (N-T) while
log lcm(V) <= theta(y) + O(sqrt(N) log N) = O(N/log N) = o(N),
so  log(G(0)/Lambda) = (log lambda + o(1))(N-T).

So in this normalisation the h=0 term IS a genuine, exponentially large main
term, and CRUX reduces to the honest minor-arc inequality

      (MA)     sum_{h=1}^{Lambda-1} |G(h)|  <  G(0) - Lambda.

This script computes G(0), Lambda, and the exact comparison, for a grid of
(T, N, y).  All arithmetic is exact Python integers.
"""
import sys
from math import isqrt
from fractions import Fraction
from core import (largest_prime_factor_table, lcm_int, legal_count_mask,
                  primes_upto, report_log, H)
from theorem_C import table as thmC_table
from core import smoothness_threshold


def analyse(T, N, y, lpf):
    mask = [lpf[n] <= y for n in range(T, N + 1)]
    Lam = 1
    HV = Fraction(0)
    for i, n in enumerate(range(T, N + 1)):
        if mask[i]:
            Lam = lcm_int(Lam, n)
            HV += Fraction(1, n)
    G0 = legal_count_mask(mask)
    kept = sum(mask)
    return dict(T=T, N=N, y=y, M=N - T + 1, kept=kept, Lam=Lam, G0=G0, HV=HV)


def show(d):
    T, N, y = d['T'], d['N'], d['y']
    lg0, lL = report_log(d['G0']), report_log(d['Lam'])
    print(f"T={T:<6} N={N:<6} y={y:<6} M={d['M']:<6} |V|={d['kept']:<6} "
          f"log G0={lg0:9.2f}  log Lam={lL:8.2f}  log(G0/Lam)={lg0-lL:9.2f}  "
          f"G0>Lam:{d['G0']>d['Lam']}  H(V)={float(d['HV']):.4f}")


def main():
    N_MAX = 20000
    lpf = largest_prime_factor_table(N_MAX)
    print("=== the smooth universe at the Theorem-C threshold y(T,N) ===")
    cases = [(100, 400), (200, 800), (500, 2000), (1000, 4000), (2000, 8000),
             (5000, 20000)]
    for (T, N) in cases:
        y = smoothness_threshold(T, N)
        show(analyse(T, N, y, lpf))

    print()
    print("=== dependence on y (y may be taken larger than the Thm-C threshold; ")
    print("    V still contains every solution, so the identity still counts them) ===")
    for (T, N) in [(1000, 4000), (5000, 20000)]:
        y0 = smoothness_threshold(T, N)
        best = None
        for mult in (0.25, 0.5, 1, 2, 4, 8, 1000000):
            y = min(int(y0 * mult), N)
            d = analyse(T, N, y, lpf)
            show(d)
            r = report_log(d['G0']) - report_log(d['Lam'])
            if best is None or r > best[0]:
                best = (r, y)
        print(f"    best log(G0/Lam) = {best[0]:.2f} at y = {best[1]}"
              f"   (Thm-C threshold y0 = {y0})")
        print()

    print("=== ratio N/T (need 1 < H(T,N) < 2 for 'sum in Z' <=> 'sum = 1') ===")
    for (T, ratio) in [(1000, 2.8), (1000, 3), (1000, 4), (1000, 5), (1000, 6), (1000, 7.3)]:
        N = int(T * ratio)
        y = smoothness_threshold(T, N)
        d = analyse(T, N, y, lpf)
        HT = H(T, N)
        print(f"  N/T={ratio:<5} H(T,N)={float(HT):.4f} "
              f"{'OK' if 1 < HT < 2 else 'BAD'}  ", end="")
        show(d)


if __name__ == "__main__":
    main()
