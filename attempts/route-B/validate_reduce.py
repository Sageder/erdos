"""
validate_reduce.py -- adversarial validation of the p-adic reduction rule (P).

CLAIM TESTED:  rule (P) of reduce.py never deletes an element that occurs in a
genuine solution.  Since the target problem has no known solutions, we test rule (P)
on the RELAXED problem (drop the no-isolated-point condition): find all sets
U subset [2,N] of distinct integers with sum 1/n = 1, by exhaustive search for small
N, and check every such U satisfies U subset A_P(N) where A_P is the fixpoint of
rule (P) alone.

Also cross-checks the p-adic condition itself with fractions.Fraction on random sets.

CONCLUSION: printed at the end.
"""
from fractions import Fraction
import itertools, random, sys
from reduce import reduce_universe, prime_prune, nu
from sympy import primerange


def all_egyptian(N, cap=10 ** 9):
    """all subsets of [2,N] of distinct ints with reciprocal sum exactly 1"""
    sols = []
    elems = list(range(2, N + 1))
    tail = [Fraction(0)] * (len(elems) + 1)
    for i in range(len(elems) - 1, -1, -1):
        tail[i] = tail[i + 1] + Fraction(1, elems[i])

    cur = []

    def rec(i, rem):
        if rem == 0:
            sols.append(list(cur))
            return
        if i >= len(elems) or rem > tail[i] or rem < 0:
            return
        # take
        cur.append(elems[i])
        rec(i + 1, rem - Fraction(1, elems[i]))
        cur.pop()
        rec(i + 1, rem)

    rec(0, Fraction(1))
    return sols


def padic_ok(U):
    """direct Fraction check of nu_p(sum over multiples of p) >= 0 for all p"""
    U = list(U)
    if not U:
        return True
    mx = max(U)
    for p in primerange(2, mx + 1):
        s = sum((Fraction(1, n) for n in U if n % p == 0), Fraction(0))
        if s == 0:
            continue
        # nu_p(s) >= 0  <=>  p does not divide denominator of s
        d = s.denominator
        if d % p == 0:
            return False
    return True


def main():
    print("=== part 1: exhaustive relaxed-problem check ===")
    for N in [12, 15, 18, 20, 24, 30]:
        sols = all_egyptian(N)
        A, _ = reduce_universe(N, use_prime=True, use_iso=False)
        As = set(A)
        bad = [U for U in sols if not set(U) <= As]
        print(f"N={N}: {len(sols)} exact reciprocal-sum-1 sets, |A_P|={len(A)}, "
              f"violations={len(bad)}")
        if bad:
            print("   FAIL example:", bad[0])
            sys.exit(1)
        # every solution must also satisfy the p-adic condition directly
        assert all(padic_ok(U) for U in sols)

    print()
    print("=== part 2: the p-adic condition is exactly what prime_prune uses ===")
    random.seed(12345)
    N = 60
    for trial in range(4000):
        k = random.randint(1, 12)
        U = sorted(random.sample(range(2, N + 1), k))
        direct = padic_ok(U)
        # re-derive with the modular formulation used in prime_prune
        allowed = set(range(2, N + 1))
        ok = True
        for p in primerange(2, N + 1):
            mults = sorted(n for n in allowed if n % p == 0)
            if not mults:
                continue
            E = max(nu(n, p) for n in mults)
            mod = p ** E
            s = 0
            for n in U:
                if n % p == 0:
                    e = nu(n, p)
                    s = (s + p ** (E - e) * pow(n // p ** e, -1, mod)) % mod
            if s != 0:
                ok = False
                break
        if ok != direct:
            print("MISMATCH", U, direct, ok)
            sys.exit(1)
    print("4000 random sets: modular formulation agrees with Fraction p-adic test.")

    print()
    print("=== part 3: known identities survive rule (P) ===")
    for U, N in [([3, 4, 5, 6, 20], 20), ([2, 3, 10, 15], 15), ([2, 4, 6, 12], 12),
                 ([2, 3, 7, 42], 42), ([2, 4, 10, 12, 15], 15)]:
        assert sum(Fraction(1, n) for n in U) == 1, U
        A, _ = reduce_universe(N, use_prime=True, use_iso=False)
        assert set(U) <= set(A), (U, N, sorted(set(U) - set(A)))
        print(f"  {U} (N={N}) survives.")

    print()
    print("CONCLUSION: rule (P) is sound on all tested exhaustive ranges.")


if __name__ == "__main__":
    main()
