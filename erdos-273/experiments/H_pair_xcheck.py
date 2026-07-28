"""
H_pair_xcheck.py -- cross-check of the incremental pruning in H_pair2.py.

CLAIM TESTED: the incremental prunes in H_pair2 (waste < Delta, L8 at insertion, L5 count
look-ahead, L10b look-ahead) never discard a pair that the leaf test check_set would accept.
We compare, on small modulus sets M and a range of artificial kappa values, the DFS result
against a BRUTE-FORCE enumeration of all 3^|M| assignments filtered only by the leaf tests.

CONCLUSION: printed.  Expected: identical pair sets in every instance.
"""
import itertools, random, sys
from fractions import Fraction
from math import gcd
from sympy import factorint, isprime
from H_pair import check_set, prime_powers


def brute(M, kappa):
    Delta = kappa - 1
    primes = sorted({p for m in M for p in factorint(m)})
    pps = prime_powers(M)
    out = set()
    for assign in itertools.product((0, 1, 2), repeat=len(M)):
        A = [M[i] for i in range(len(M)) if assign[i] == 1]
        B = [M[i] for i in range(len(M)) if assign[i] == 2]
        if not A or not B:
            continue
        bA = sum(Fraction(1, m) for m in A)
        bB = sum(Fraction(1, m) for m in B)
        if not (1 < bA <= kappa and 1 < bB <= kappa):
            continue
        if check_set(sorted(A), Delta, primes, pps) and check_set(sorted(B), Delta, primes, pps):
            out.add((tuple(sorted(A)), tuple(sorted(B))))
    # canonicalise unordered pairs
    return {tuple(sorted(p)) for p in out}


def dfs(M, kappa):
    """the H_pair2 search, parameterised by an explicit M and kappa"""
    Delta = kappa - 1
    primes = sorted({p for m in M for p in factorint(m)})
    pps = prime_powers(M)
    Ms = sorted(M)
    n = len(Ms)
    rc = [Fraction(1, m) for m in Ms]
    suf = [Fraction(0)] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + rc[i]
    remcnt = {pk: [0] * (n + 1) for pk in pps}
    remsum = {pk: [Fraction(0)] * (n + 1) for pk in pps}
    for pk in pps:
        for i in range(n - 1, -1, -1):
            hit = (Ms[i] % pk == 0)
            remcnt[pk][i] = remcnt[pk][i + 1] + (1 if hit else 0)
            remsum[pk][i] = remsum[pk][i + 1] + (rc[i] if hit else Fraction(0))
    pkprime = {pk: min(factorint(pk)) for pk in pps}
    out = set()

    def feasible(i, cnt, sm, mn):
        for pk in pps:
            if cnt[pk] == 0:
                continue
            q = pkprime[pk]
            if pk == q and cnt[pk] + remcnt[pk][i] < q:
                return False
            if sm[pk] + remsum[pk][i] < q * (Fraction(1, mn[pk]) - Delta):
                return False
        return True

    def rec(i, A, bA, cA, sA, mA, B, bB, cB, sB, mB, started, waste):
        if bA > kappa or bB > kappa or waste >= Delta:
            return
        if bA + suf[i] <= 1 or bB + suf[i] <= 1:
            return
        if not feasible(i, cA, sA, mA) or not feasible(i, cB, sB, mB):
            return
        if i == n:
            if bA > 1 and bB > 1 and check_set(sorted(A), Delta, primes, pps) \
               and check_set(sorted(B), Delta, primes, pps):
                out.add(tuple(sorted((tuple(sorted(A)), tuple(sorted(B))))))
            return
        m = Ms[i]
        touched = [pk for pk in pps if m % pk == 0]

        def push(S, c, s, mn):
            old = {pk: (c[pk], s[pk], mn.get(pk)) for pk in touched}
            for pk in touched:
                c[pk] += 1; s[pk] += rc[i]
                if pk not in mn:
                    mn[pk] = m
            S.append(m); return old

        def pop(S, c, s, mn, old):
            S.pop()
            for pk in touched:
                c[pk], s[pk], om = old[pk]
                if om is None: mn.pop(pk, None)
                else: mn[pk] = om

        if all(gcd(m, y) != 1 or Fraction(1, m * y) <= Delta for y in A):
            o = push(A, cA, sA, mA)
            rec(i + 1, A, bA + rc[i], cA, sA, mA, B, bB, cB, sB, mB, True, waste)
            pop(A, cA, sA, mA, o)
        if started and all(gcd(m, y) != 1 or Fraction(1, m * y) <= Delta for y in B):
            o = push(B, cB, sB, mB)
            rec(i + 1, A, bA, cA, sA, mA, B, bB + rc[i], cB, sB, mB, started, waste)
            pop(B, cB, sB, mB, o)
        rec(i + 1, A, bA, cA, sA, mA, B, bB, cB, sB, mB, started, waste + rc[i])

    z = lambda: {pk: 0 for pk in pps}
    zs = lambda: {pk: Fraction(0) for pk in pps}
    rec(0, [], Fraction(0), z(), zs(), {}, [], Fraction(0), z(), zs(), {}, False, Fraction(0))
    return out


def main():
    rng = random.Random(4242)
    H = [m for m in range(2, 200) if isprime(2 * m + 1)]
    bad = 0
    tot = 0
    nonempty = 0
    pools = [H[:24], list(range(2, 15)), list(range(2, 13))]
    for trial in range(30):
        pool = pools[trial % len(pools)]
        M = sorted(rng.sample(pool, rng.randrange(7, min(11, len(pool) + 1))))
        tb = sum(Fraction(1, m) for m in M)
        for kap in (Fraction(3, 2), Fraction(5, 2), Fraction(7, 2), tb - 1, Fraction(2)):
            if kap <= 1:
                continue
            tot += 1
            b = brute(M, kap)
            d = dfs(M, kap)
            if b:
                nonempty += 1
            if b != d:
                bad += 1
                print("MISMATCH M=%s kappa=%s brute=%d dfs=%d  only-in-brute=%s"
                      % (M, kap, len(b), len(d), list(b - d)[:2]))
    print("instances compared: %d   (with a nonempty answer: %d)   mismatches: %d" % (tot, nonempty, bad))
    print("CONCLUSION:", "incremental pruning is sound" if bad == 0 else "*** PRUNING UNSOUND ***")


if __name__ == "__main__":
    main()
