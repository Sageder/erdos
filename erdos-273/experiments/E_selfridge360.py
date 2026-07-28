"""
CLAIM TESTED (Route E, item 9 of the literature brief).

Erdos-Graham [ErGr80, p.24] attribute to Selfridge a covering system all of whose moduli
are of the form p-1 with p PRIME (p = 3 allowed, i.e. the modulus 2 is permitted), the
moduli being divisors of 360.  The present script decides, by exhaustive exact search, the
existence of such a system and prints one if it exists.

Admissible moduli:
    A = { d : d | 360, d > 1, d+1 prime }.
A covering system with all moduli dividing 360 is periodic mod 360, so "covers Z" is
equivalent to "covers Z/360Z".  Moduli must be DISTINCT (each used at most once) and > 1.

Method: exact DFS on a 360-bit mask.  At each node take the least uncovered residue x and
branch over the unused moduli m, forcing the residue class x mod m (any class covering x
must be x mod m).  Prune when the remaining reciprocal budget cannot cover the remaining
uncovered points.  No floating point in the coverage test.

Deterministic; no external input.
"""
from fractions import Fraction
from sympy import isprime


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def solve(L, A):
    """Return list of (m, r) covering Z/LZ with distinct moduli from A, or None."""
    A = sorted(A)
    full = (1 << L) - 1
    masks = {}
    for m in A:
        for r in range(m):
            mk = 0
            for x in range(r, L, m):
                mk |= 1 << x
            masks[(m, r)] = mk
    # suffix budgets: budget[i] = sum_{j>=i} 1/A[j]
    n = len(A)
    budget = [Fraction(0)] * (n + 1)
    for i in range(n - 1, -1, -1):
        budget[i] = budget[i + 1] + Fraction(1, A[i])

    chosen = []
    best = [None]

    def rec(cov, used):
        if cov == full:
            best[0] = list(chosen)
            return True
        # least uncovered point
        x = ((~cov) & full)
        x = (x & -x).bit_length() - 1
        # remaining budget over unused moduli must be >= uncovered density
        unc = L - bin(cov).count("1")
        rem = sum(Fraction(1, A[i]) for i in range(n) if not (used >> i) & 1)
        if rem < Fraction(unc, L):
            return False
        for i in range(n):
            if (used >> i) & 1:
                continue
            m = A[i]
            mk = masks[(m, x % m)]
            chosen.append((m, x % m))
            if rec(cov | mk, used | (1 << i)):
                return True
            chosen.pop()
        return False

    return best[0] if rec(0, 0) else None


def main():
    L = 360
    A = [d for d in divisors(L) if d > 1 and isprime(d + 1)]
    print("L =", L)
    print("admissible moduli A = { d | 360 : d>1, d+1 prime } =", A)
    print("  (d+1 prime for each:", [(d, d + 1, isprime(d + 1)) for d in A], ")")
    s = sum(Fraction(1, d) for d in A)
    print("  sum of reciprocals of A =", s, "=", float(s))

    sol = solve(L, A)
    if sol is None:
        print("NO covering system of Z/360 with distinct moduli from A")
        return
    sol.sort()
    print("\nFOUND a covering system, %d classes:" % len(sol))
    for m, r in sol:
        print("   %3d (mod %3d)      [modulus = p-1 with p = %d prime: %s]"
              % (r, m, m + 1, isprime(m + 1)))
    print("sum of reciprocals of the moduli used =",
          sum(Fraction(1, m) for m, _ in sol),
          "=", float(sum(Fraction(1, m) for m, _ in sol)))

    # independent verification, elementwise
    covered = [False] * L
    seen = set()
    for m, r in sol:
        assert m > 1 and isprime(m + 1) and L % m == 0
        assert m not in seen
        seen.add(m)
        for x in range(r % m, L, m):
            covered[x] = True
    assert all(covered), "VERIFICATION FAILED"
    print("VERIFIED: distinct moduli, each of the form p-1 with p prime, every residue "
          "mod 360 covered.")

    # Does 4 have to be there?  And: what if modulus 2 is FORBIDDEN (the p >= 5 world,
    # restricted to divisors of 360)?
    A5 = [d for d in A if d >= 4]
    print("\nSame search with the modulus 2 removed (p >= 5 only), A5 =", A5,
          " budget =", float(sum(Fraction(1, d) for d in A5)))
    sol5 = solve(L, A5)
    print("  result:", "COVER FOUND" if sol5 else "NO COVER (exhaustive)")
    if sol5:
        print("   ", sorted(sol5))


if __name__ == "__main__":
    main()
