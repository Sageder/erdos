#!/usr/bin/env python3
"""
mkuniverse2.py A N p q outfile
    generalised q-sieve for the problem   "legal U subset [A,N] with sum 1/n = p/q".

GENERALISED LEMMA.  Let U be finite, sum_{n in U} 1/n = T, ell a prime,
E := max_{n in U} nu_ell(n) (0 if none), and write the elements attaining E as
ell^E c_i.  Then  sum_{n in U} 1/n = ell^{-E} * (sum_i 1/c_i) + R  with nu_ell(R) > -E,
hence
      nu_ell(T) >= -E, with equality  <=>  sum_i 1/c_i  !=  0 in Z/ell.
So with f := max(0, -nu_ell(T)):
      E >= f  always;  and if E > f then sum_i 1/c_i == 0 in Z/ell.
Static sieve: while the universe's top ell-level E exceeds f and no NONEMPTY subset
of {1/c mod ell} sums to 0 mod ell, that level is unusable -> delete it.
If the universe's top level ever drops below f, no U exists at all.
Plus: delete allowed n that are isolated in the universe (U has no isolated point).
"""
import sys, math
from fractions import Fraction

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from s4_qsieve import primes_upto, nu, zero_subset_sum_possible


def sieve_target(A, N, T):
    P = primes_upto(N)
    fl = {}
    for ell in P:
        t = nu(T.numerator, ell) - nu(T.denominator, ell)
        fl[ell] = max(0, -t)
    allowed = set(range(A, N + 1))
    changed = True
    while changed and allowed:
        changed = False
        for ell in P:
            f = fl[ell]
            while True:
                lvl = {}
                for n in allowed:
                    e = nu(n, ell)
                    if e:
                        lvl.setdefault(e, []).append(n)
                E = max(lvl) if lvl else 0
                if E < f:
                    return set()          # infeasible
                if E <= f:
                    break
                vals = [pow(n // ell ** E, ell - 2, ell) % ell for n in lvl[E]]
                if zero_subset_sum_possible(vals, ell):
                    break
                for n in lvl[E]:
                    allowed.discard(n)
                changed = True
        iso = [n for n in allowed if (n - 1) not in allowed and (n + 1) not in allowed]
        if iso:
            for n in iso:
                allowed.discard(n)
            changed = True
    return allowed


def main():
    A = int(sys.argv[1]); N = int(sys.argv[2])
    T = Fraction(int(sys.argv[3]), int(sys.argv[4]))
    out = sys.argv[5]
    S = sorted(sieve_target(A, N, T))
    if not S:
        open(out, "w").write("%d %d\n1\n1\n\n" % (N, A))
        print("A=%d N=%d T=%s  universe EMPTY -> NO SOLUTION (sieve)" % (A, N, T))
        return
    L = 1
    for n in S:
        L = L * n // math.gcd(L, n)
    if L % T.denominator:
        open(out, "w").write("%d %d\n1\n1\n\n" % (N, A))
        print("A=%d N=%d T=%s  denominator not realisable -> NO SOLUTION" % (A, N, T))
        return
    R0 = T.numerator * (L // T.denominator)
    with open(out, "w") as f:
        f.write("%d %d\n%d\n%d\n" % (N, A, L, R0))
        f.write(" ".join(map(str, S)) + "\n")
    print("A=%d N=%d T=%s universe=%d lcm_bits=%d max=%d"
          % (A, N, T, len(S), L.bit_length(), S[-1]))


if __name__ == "__main__":
    main()
