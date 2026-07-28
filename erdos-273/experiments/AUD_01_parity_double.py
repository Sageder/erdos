"""
ADVERSARIAL AUDIT 1+2: parity split (Lemma M3) and the doubling map / infimum (Lemma M2).
Written from scratch; imports nothing from the project.
"""
import random
from fractions import Fraction
from math import gcd
from sympy import isprime


def lcm(xs):
    L = 1
    for x in xs:
        L = L * x // gcd(L, x)
    return L


def hitmask(classes, L):
    hit = bytearray(L)
    for a, n in classes:
        seg = hit[a % n::n]
        hit[a % n::n] = b'\x01' * len(seg)
    return hit


def is_cover(classes):
    if not classes:
        return False
    L = lcm([n for _, n in classes])
    return all(hitmask(classes, L))


def gen_cover(pool, L, rng, maxk=14):
    """greedy random covering with DISTINCT moduli from pool (divisors of L); None on failure."""
    hit = bytearray(L)
    used, cls = set(), []
    for _ in range(maxk):
        try:
            r = hit.index(0)
        except ValueError:
            return cls
        avail = [n for n in pool if n not in used]
        if not avail:
            return None
        n = rng.choice(avail)
        used.add(n)
        a = r % n
        cls.append((a, n))
        seg = hit[a::n]
        hit[a::n] = b'\x01' * len(seg)
    return cls if all(hit) else None


def Eset(X):
    return [n for n in range(4, X + 1) if isprime(n + 1)]


def Hset(Y):
    return [m for m in range(2, Y + 1) if isprime(2 * m + 1)]


def split(classes):
    out = {0: [], 1: []}
    for a, n in classes:
        assert n % 2 == 0
        j = a % 2
        out[j].append(((a - j) // 2, n // 2))
    return out


def lift(M0, M1):
    return [(2 * b + j, 2 * m) for j, Mj in ((0, M0), (1, M1)) for b, m in Mj]


def test_parity_split(trials=6000, seed=1):
    rng = random.Random(seed)
    Ls = [12, 24, 36, 60, 72, 120, 180, 360]
    n_cov = n_not = 0
    for t in range(trials):
        L2 = rng.choice(Ls) * 2
        pool = [d for d in range(2, L2 + 1) if L2 % d == 0 and d % 2 == 0]
        if rng.random() < 0.5:
            cls = gen_cover(pool, L2, rng)          # biased towards coverings
            if cls is None:
                continue
        else:
            k = rng.randint(1, min(len(pool), 9))   # random, usually not a covering
            cls = [(rng.randrange(m), m) for m in rng.sample(pool, k)]
        cov = is_cover(cls)
        halves = split(cls)
        h0 = is_cover(halves[0])
        h1 = is_cover(halves[1])
        assert cov == (h0 and h1), (cls, cov, h0, h1)
        P = lcm([n for _, n in cls])
        hit = hitmask(cls, P)
        for j in (0, 1):
            allj = all(hit[x] for x in range(j, P, 2))
            assert allj == is_cover(halves[j]), ("parity refinement fails", cls, j)
        m0 = [m for _, m in halves[0]]
        m1 = [m for _, m in halves[1]]
        assert len(set(m0)) == len(m0) and len(set(m1)) == len(m1)
        assert not (set(m0) & set(m1))
        if cov:            # negative integers explicitly
            for x in range(-3 * P - 7, -3 * P + 7):
                assert any((x - a) % n == 0 for a, n in cls), ("negative x uncovered", x, cls)
        LH = lcm(m0 + m1)
        assert P == 2 * LH, ("lcm_E = 2 lcm_H fails", P, LH, cls)
        n_cov += cov
        n_not += (not cov)
    print(f"  (i)=>(ii): {n_cov} covering / {n_not} non-covering instances, all consistent;")
    print(f"      parity-refined equivalence, distinctness, disjointness, lcm_E=2lcm_H, "
          f"negatives: all OK")


def test_lift(trials=4000, seed=2):
    rng = random.Random(seed)
    ncov = 0
    LHs = [180, 360, 720, 2520]
    for _ in range(trials):
        LH = rng.choice(LHs)
        H = [m for m in range(2, LH + 1) if LH % m == 0 and isprime(2 * m + 1)]
        k0, k1 = rng.randint(1, 5), rng.randint(1, 5)
        if k0 + k1 > len(H):
            continue
        s = rng.sample(H, k0 + k1)
        M0 = [(rng.randrange(m), m) for m in s[:k0]]
        M1 = [(rng.randrange(m), m) for m in s[k0:]]
        cls = lift(M0, M1)
        mods = [n for _, n in cls]
        assert len(set(mods)) == len(mods)
        assert all(isprime(n + 1) and n >= 4 for n in mods)
        c = is_cover(cls)
        assert c == (is_cover(M0) and is_cover(M1))
        ncov += c
    print(f"  (ii)=>(i): {trials} instances ({ncov} genuine coverings), moduli distinct and in E, "
          f"equivalence holds")


def test_lift_needs_disjoint():
    M0, M1 = [(0, 2)], [(1, 2)]
    cls = lift(M0, M1)
    print(f"  disjointness: M0=M1={{2}} lifts to moduli {[n for _,n in cls]} -> repeated modulus, "
          f"violates the distinctness convention. Disjointness IS forced.")


def D(C):
    return [(0, 2)] + [(2 * a + 1, 2 * n) for a, n in C]


def test_doubling():
    C = [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]
    for k in range(0, 11):
        assert is_cover(C), ("not a covering at k=", k)
        mods = [n for _, n in C]
        assert len(set(mods)) == len(mods) and all(n > 1 for n in mods)
        cost = sum(Fraction(1, n) for n in mods)
        assert cost == 1 + Fraction(1, 3) * Fraction(1, 2 ** k), (k, cost)
        if k < 4:
            print(f"    k={k}: moduli {sorted(mods)}  cost {cost}")
        C = D(C)
    print("  C_0..C_10: coverings, distinct moduli > 1, cost = 1 + (1/3)2^-k exactly. OK")
    E = Eset(600)
    bad = [n for n in E if not isprime(2 * n + 1)]
    print(f"  n -> 2n on E: {len(bad)}/{len(E)} of E<=600 have 2n+1 composite "
          f"(e.g. {bad[:8]}); also 2 not in E.  ==> D does NOT act on E-systems.")
    # a stronger statement: does ANY E-covering arise as D(C)?  D(C) always contains modulus 2.
    print("  Every D(C) contains the modulus 2, and 2 is not in E, so no image of D is an "
          "E-system. Confirmed.")


if __name__ == "__main__":
    print("== parity split ==")
    test_parity_split()
    test_lift()
    test_lift_needs_disjoint()
    print("== doubling map / infimum ==")
    test_doubling()
