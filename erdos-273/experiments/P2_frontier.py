"""
P2 -- HONEST FRONTIER of the single-prime fiber elimination for THE PIVOT.

For a lattice L put S(L) = {m | L : m >= 3, 2m+1 prime}  (the pivot pool, modulus 2 banned).
The exact fiber quantity at a prime q is

    Phi_q(S) = max over residue assignments  min over fibers r in Z/q^J  F_q(r),
    F_q(r)   = sum_{m in S, b_m = r mod q^{nu_q(m)}} q^{nu_q(m)} / m .

TRIVIAL LOWER BOUND (proved, one line): every m in S with q ∤ m has nu_q(m) = 0 and therefore
contributes 1/m to EVERY fiber, whatever the assignment.  Hence

        Phi_q(S)  >=  B_q(L) := sum_{m in S(L), q ∤ m} 1/m .                    (*)

CONSEQUENCE (the honest limit of the method): if B_q(L) >= 1 then the test "Phi_q >= 1" is
VACUOUS at q.  If B_q(L) >= 1 for every prime q | L, then NO single-prime fiber test can ever
eliminate L, no matter how much CPU is spent.  Same with a finite set Q of primes and
B_Q(L) = sum over m in S(L) coprime to prod(Q).

This script measures, for every L with budget(S(L)) > 1 up to a bound:
   - budget(L) = sum 1/m over S(L),
   - minB1(L)  = min over primes q | L of B_q(L)          (single-prime frontier),
   - minB2(L)  = min over pairs  {q1,q2} | L of B_Q(L)     (two-prime frontier),
   - minB3(L)  = min over triples                          (three-prime frontier),
and reports the smallest L at which each of these tests dies (i.e. min >= 1).

CONCLUSION: printed.  This is a PROVED obstruction to the method, not to the pivot.
"""
import sys
from fractions import Fraction
from itertools import combinations
from sympy import isprime, primefactors


def sieve_H(N):
    """h[m] = True iff 2m+1 is prime, for m <= N."""
    lim = 2 * N + 1
    isp = bytearray([1]) * (lim + 1)
    isp[0] = isp[1] = 0
    i = 2
    while i * i <= lim:
        if isp[i]:
            isp[i * i::i] = bytearray(len(isp[i * i::i]))
        i += 1
    return bytearray(1 if isp[2 * m + 1] else 0 for m in range(N + 1))


def main(LMAX):
    H = sieve_H(LMAX)
    # divisor-sum style sweep: for each m in H (m>=3) add 1/m to all multiples
    # we need per-L the pool; do it by iterating multiples (harmonic, cheap)
    pools = [[] for _ in range(LMAX + 1)]
    for m in range(3, LMAX + 1):
        if H[m]:
            for L in range(m, LMAX + 1, m):
                pools[L].append(m)
    first_dead = {1: None, 2: None, 3: None}
    n_cand = 0
    alive1 = []
    for L in range(6, LMAX + 1):
        S = pools[L]
        if not S:
            continue
        bud = sum(Fraction(1, m) for m in S)
        if bud <= 1:
            continue
        n_cand += 1
        ps = primefactors(L)
        rec = {}
        for k in (1, 2, 3):
            if len(ps) < k:
                rec[k] = None
                continue
            best = None
            for Q in combinations(ps, k):
                P = 1
                for q in Q:
                    P *= q
                b = sum(Fraction(1, m) for m in S if all(m % q for q in Q))
                if best is None or b < best:
                    best = b
            rec[k] = best
        if rec[1] is not None and rec[1] >= 1 and first_dead[1] is None:
            first_dead[1] = (L, rec)
        if rec[2] is not None and rec[2] >= 1 and first_dead[2] is None:
            first_dead[2] = (L, rec)
        if rec[3] is not None and rec[3] >= 1 and first_dead[3] is None:
            first_dead[3] = (L, rec)
        if rec[1] is not None and rec[1] < 1:
            alive1.append(L)
    print(f"lattices L <= {LMAX} with pivot budget > 1 : {n_cand}")
    print(f"of those, still attackable by SOME single-prime fiber test (min_q B_q < 1): "
          f"{len(alive1)}  ({100.0*len(alive1)/max(n_cand,1):.1f}%)")
    for k in (1, 2, 3):
        fd = first_dead[k]
        if fd is None:
            print(f"  {k}-prime test: never vacuous up to {LMAX}")
        else:
            L, rec = fd
            print(f"  {k}-prime test FIRST GOES VACUOUS at L = {L}  "
                  f"(min_Q B_Q = {float(rec[k]):.5f} >= 1)")
    # tail behaviour: how the surviving fraction decays
    for hi in (1000, 3000, 10000, 30000, LMAX):
        if hi > LMAX:
            continue
        c = sum(1 for L in alive1 if L <= hi)
        t = 0
        for L in range(6, hi + 1):
            S = pools[L]
            if S and sum(Fraction(1, m) for m in S) > 1:
                t += 1
        print(f"   L <= {hi:7d}:  {t:5d} candidates, {c:5d} ({100.0*c/max(t,1):5.1f}%) "
              f"still have a non-vacuous single-prime test")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30000)
