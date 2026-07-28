"""
C_budget.py  --  Route C, Step 2: how much reciprocal budget can an H-divisor LATTICE
actually offer?

CLAIM TESTED.  Every covering system whose moduli all divide L uses moduli from
    D_H(L) = { d : d | L, 2d+1 prime },
so its reciprocal sum is at most  B(L) := sum_{d in D_H(L)} 1/d.
By Davenport-Mirsky-Newman-Rado a covering with distinct moduli needs sum 1/m > 1, and the
Step-1 equivalence needs TWO DISJOINT H-coverings inside one lattice, hence  B(L) > 2.
Empirically (measured by C_hcover) the H-coverings that exist in a lattice consume almost
the WHOLE of B(L), so "two disjoint ones" plausibly needs B(L) of order twice the minimum
reciprocal sum of a single H-covering.

This script measures how fast B(L) can grow: for L = prod_{q <= Q} q^{e(q)} with generous
exponents it prints B(L), the count |D_H(L)|, and log10(L).  It also prints the
unrestricted budget B_H(Y) = sum_{m in H, m <= Y} 1/m for comparison (the lattice can never
beat that for a comparable modulus range).

CONCLUSION (printed): B(L) grows extremely slowly -- doubly logarithmically -- so the
"two disjoint coverings in one divisor lattice" target is far out of computational reach
even though nothing here proves it impossible.
"""
from sympy import primerange, isprime
import math


def lattice_budget(primes, exps):
    """B(L) and |D_H(L)| for L = prod p^e, computed without enumerating divisors of huge L
    -- we enumerate divisors but stop if there are too many."""
    divs = [1]
    for p, e in zip(primes, exps):
        newd = []
        pk = 1
        for i in range(e + 1):
            for d in divs:
                newd.append(d * pk)
            pk *= p
        divs = newd
        if len(divs) > 4_000_000:
            raise MemoryError("too many divisors")
    b = 0.0
    n = 0
    logL = sum(e * math.log10(p) for p, e in zip(primes, exps))
    for d in divs:
        if d >= 2 and isprime(2 * d + 1):
            b += 1.0 / d
            n += 1
    return b, n, logL


def BH(Y):
    s = 0.0
    n = 0
    # sieve
    N = 2 * Y + 1
    bs = bytearray([1]) * (N + 1)
    bs[0] = bs[1] = 0
    i = 2
    while i * i <= N:
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
        i += 1
    for p in range(5, N + 1, 2):
        if bs[p]:
            s += 2.0 / (p - 1)
            n += 1
    return s, n


def main():
    print("Unrestricted H-budget  B_H(Y) = sum_{m in H, m<=Y} 1/m")
    for Y in [10**2, 10**3, 10**4, 10**5, 10**6, 10**7]:
        s, n = BH(Y)
        print(f"   Y = 1e{len(str(Y))-1:<2}   B_H = {s:8.4f}   |H cap [2,Y]| = {n}")
    print()
    print("Divisor-lattice budgets  B(L) = sum_{d | L, 2d+1 prime} 1/d")
    print(f"{'primes<=Q':>10} {'exponent profile':>34} {'log10 L':>9} {'|D_H|':>8} "
          f"{'B(L)':>8} {'B(L)-1/2':>9}")
    profiles = [
        ([2, 3], [3, 2]),
        ([2, 3, 5, 7], [3, 2, 1, 1]),
        ([2, 3, 5, 7, 11, 13], [3, 2, 1, 1, 1, 1]),
        ([2, 3, 5, 7, 11, 13], [4, 3, 2, 1, 1, 1]),
        ([2, 3, 5, 7, 11, 13], [5, 3, 2, 2, 1, 1]),
        ([2, 3, 5, 7, 11, 13, 17, 19], [4, 3, 2, 1, 1, 1, 1, 1]),
        ([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], [4, 3, 2, 1, 1, 1, 1, 1, 1, 1]),
        ([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37], [4, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]),
        ([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43],
         [5, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        (list(primerange(2, 60)), None),
        (list(primerange(2, 80)), None),
        (list(primerange(2, 110)), None),
    ]
    for primes, exps in profiles:
        if exps is None:
            exps = [max(1, int(6 / math.log2(p))) for p in primes]
        try:
            b, n, logL = lattice_budget(primes, exps)
        except MemoryError:
            print(f"{max(primes):>10} {'(too many divisors)':>34}")
            continue
        print(f"{max(primes):>10} {str(exps):>34} {logL:9.2f} {n:8d} {b:8.4f} {b-0.5:9.4f}")
    print()
    print("Reading: to give two DISJOINT H-coverings room inside ONE lattice one needs")
    print("B(L) comfortably above 2 (each covering needs > 1, and measured H-coverings")
    print("use nearly the whole budget of their lattice).  B(L) climbs past 3 only for L")
    print("with tens of prime factors, i.e. L astronomically beyond any mod-L sweep.")


if __name__ == "__main__":
    main()
