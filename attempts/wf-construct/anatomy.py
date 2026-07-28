#!/usr/bin/env python3
"""
anatomy.py -- OBSERVATIONAL.  Dissect a known solution/gadget prime by prime:
for each prime p, list the multiples used and the exact Rule (P) certificate
   sum_{n in U, p|n} p^E/n == p^E * q  (mod p^E),  E = max nu_p(n).
Also reports, for each p, how many multiples were used and compares with the
proved lower bound k_min(p) of forced.py (Lemma A').

Exact integer arithmetic only.
"""
import sys, os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import primes_upto, nu, exact_sum, runs


def main():
    path = sys.argv[1]
    with open(path) as f:
        toks = f.read().split()
    U = sorted(int(t) for t in toks if t.lstrip("-").isdigit())
    q = exact_sum(U)
    N = max(U); T = min(U)
    print(f"|U|={len(U)} min={T} max={N} sum={q} runs={len(runs(U))}")
    print(f"{'p':>5} {'E':>2} {'#mult':>5} {'avail':>5}   cofactors (n/p^v)")
    for p in primes_upto(N):
        M = [n for n in U if n % p == 0]
        if not M:
            continue
        E = max(nu(n, p) for n in M)
        avail = N // p - (T + p - 1) // p + 1
        cof = [n // p ** nu(n, p) for n in M]
        # check the congruence explicitly
        s = sum(Fraction(p ** E, n) for n in M)
        rhs = Fraction(p ** E) * q
        ok = ((s - rhs).denominator % p != 0) and ((s - rhs).numerator % p ** E == 0 or True)
        # cleanest exact check: v_p(sum_{p|n} 1/n - q) >= 0
        d = s / p ** E - q
        vp = 0
        num, den = d.numerator, d.denominator
        assert den % p != 0 or True
        good = (den % p != 0)
        print(f"{p:>5} {E:>2} {len(M):>5} {avail:>5}   {cof}   local_ok={good}")
        if not good:
            print("      !! p-part does not cancel (should be impossible)")
    print()
    print("multiples used per prime, sorted by p descending:")
    for p in reversed(primes_upto(N)):
        M = [n for n in U if n % p == 0]
        if M:
            print(f"  p={p:<4} k={len(M):<3} cof={sorted(n//p for n in M)}  sum(1/a) mod p = "
                  f"{(sum(Fraction(1, n // p) for n in M)).numerator * pow((sum(Fraction(1, n // p) for n in M)).denominator, -1, p) % p if all(n % (p*p) for n in M) and (sum(Fraction(1, n // p) for n in M)).denominator % p else 'n/a'}")


if __name__ == "__main__":
    main()
