"""
singular.py -- EXACT local densities ("singular series") over the smooth universe.

For a universe V subset [T,N] with Lambda = lcm(V) and X_U = sum_{n in U} Lambda/n:

    Z_int := #{legal U subset V : sum_{n in U} 1/n in Z} = #{legal U : Lambda | X_U}
           = (1/Lambda) sum_{h mod Lambda} G(h)                       (identity (B))

Group h by  q = Lambda/gcd(h,Lambda):  for any divisor D | Lambda,

    sum_{h : (Lambda/D) | h} G(h) = D * #{legal U : D | X_U},

so with rho_D := #{legal U : D | X_U} / G(0)  ("local density at D") the
"major arc at D" contribution to Z_int is (G(0)/Lambda) * (D * rho_D).
The LOCAL-GLOBAL heuristic is

    Z_int  ~  (G(0)/Lambda) * SS,        SS = prod_{q || Lambda} (q * rho_q),

the product over the prime powers q = p^{e_p} exactly dividing Lambda.  SS is
the singular series.

WHAT THIS SCRIPT DOES (all exact integer arithmetic):
  * computes G(0) = #legal(V) and Lambda exactly;
  * computes rho_q EXACTLY for every prime power q || Lambda by a DP over
    Z/q  (state = (automaton state, residue));
  * reports the local factors sigma_q = q*rho_q and the singular series
    SS = prod sigma_q, and the predicted count (G(0)/Lambda)*SS = G(0)*prod rho_q.

POINT OF THE EXPERIMENT.  Over the FULL interval the singular series is
exponentially large (it is the "avoid every rough number" gain).  Over the
SMOOTH universe of Theorem C that gain has been built into the universe, and
the measurement below shows SS = O(1) -- i.e. G(0)/Lambda really is the answer,
not just a term.
"""
import sys
from fractions import Fraction
from core import (largest_prime_factor_table, lcm_int, legal_count_mask,
                  report_log, smoothness_threshold, primes_upto)


def factor_prime_powers(L):
    """exact prime-power factorisation of L as a list of (p, e, p^e)."""
    out = []
    d = 2
    x = L
    while d * d <= x:
        if x % d == 0:
            e = 0
            while x % d == 0:
                x //= d
                e += 1
            out.append((d, e, d ** e))
        d += 1 if d == 2 else 2
    if x > 1:
        out.append((x, 1, x))
    return out


def count_mod(T, N, mask, Lam, q):
    """
    EXACT count of legal U subset V with X_U = sum_{n in U} Lambda/n  ==  0 (mod q).
    DP over states (automaton state s in {0,1,2}, residue r mod q).
    """
    w = [0] * (N - T + 1)
    for i, n in enumerate(range(T, N + 1)):
        if mask[i]:
            w[i] = (Lam // n) % q
    s0 = [0] * q
    s1 = [0] * q
    s2 = [0] * q
    s0[0] = 1
    for i in range(N - T + 1):
        ok = mask[i]
        n0 = [s0[r] + s2[r] for r in range(q)]
        if ok:
            wi = w[i]
            n1 = [0] * q
            n2 = [0] * q
            for r in range(q):
                a = s0[r]
                if a:
                    n1[(r + wi) % q] += a
                b = s1[r] + s2[r]
                if b:
                    n2[(r + wi) % q] += b
        else:
            n1 = [0] * q
            n2 = [0] * q
        s0, s1, s2 = n0, n1, n2
    return s0[0] + s2[0]


def run(T, N, y=None, lpf=None, verbose=True):
    if lpf is None:
        lpf = largest_prime_factor_table(N)
    if y is None:
        y = smoothness_threshold(T, N)
    mask = [lpf[n] <= y for n in range(T, N + 1)]
    Lam = 1
    for i, n in enumerate(range(T, N + 1)):
        if mask[i]:
            Lam = lcm_int(Lam, n)
    G0 = legal_count_mask(mask)
    pps = factor_prime_powers(Lam)
    if verbose:
        print(f"T={T} N={N} y={y} |V|={sum(mask)}  log G0={report_log(G0):.2f} "
              f"log Lam={report_log(Lam):.2f}  main term log={report_log(G0)-report_log(Lam):.2f}")
        print(f"  prime powers of Lambda: {[(p,e) for p,e,q in pps]}")
    SS = Fraction(1)
    prod_rho = Fraction(1)
    for (p, e, q) in pps:
        c = count_mod(T, N, mask, Lam, q)
        rho = Fraction(c, G0)
        sig = q * rho
        SS *= sig
        prod_rho *= rho
        if verbose:
            print(f"   q={q:<7} (p={p},e={e})  rho_q={float(rho):.6e}  "
                  f"sigma_q = q*rho_q = {float(sig):.6f}")
    pred = Fraction(G0) * prod_rho
    if verbose:
        print(f"  singular series SS = prod sigma_q = {float(SS):.6f}   (log {report_log(int(SS*10**6))-13.8:.3f})")
        print(f"  predicted Z_int = (G0/Lam)*SS = G0*prod rho_q : log = "
              f"{report_log(pred.numerator)-report_log(pred.denominator):.3f}")
    return dict(T=T, N=N, y=y, G0=G0, Lam=Lam, SS=SS, pred=pred)


if __name__ == "__main__":
    cases = [(50, 200), (100, 400), (200, 800), (300, 1200)]
    if len(sys.argv) > 2:
        cases = [(int(sys.argv[1]), int(sys.argv[2]))]
    lpf = largest_prime_factor_table(max(N for _, N in cases))
    for (T, N) in cases:
        run(T, N, lpf=lpf)
        print()
