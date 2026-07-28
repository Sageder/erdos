"""
ADVERSARIAL AUDIT 3: Lemma A2 (forced overlap).

Claim: M = modulus set of a covering system with distinct moduli, T subset M pairwise coprime.
Then  X := sum_{m in M} 1/m - 1  >=  f(T) := sum_{m in T} 1/m - 1 + prod_{m in T}(1 - 1/m).

We (a) hunt for counterexamples over many random and exhaustive covering systems,
    (b) check the boundary cases T = {} and |T| = 1,
    (c) check that BOTH hypotheses (T subset M, T pairwise coprime) are load-bearing by
        exhibiting explicit failures when each is dropped,
    (d) verify the CRT density identity dens(union over T) = 1 - prod(1-1/m) for ALL residues,
    (e) verify the monotonicity step g(S u {c}) >= g(S) directly.
"""
import random, itertools
from fractions import Fraction
from math import gcd


def lcm(xs):
    L = 1
    for x in xs:
        L = L * x // gcd(L, x)
    return L


def dens(classes):
    """exact natural density of a finite union of residue classes"""
    if not classes:
        return Fraction(0)
    L = lcm([n for _, n in classes])
    hit = bytearray(L)
    for a, n in classes:
        s = hit[a % n::n]
        hit[a % n::n] = b'\x01' * len(s)
    return Fraction(sum(hit), L)


def is_cover(classes):
    return classes and dens(classes) == 1


def fT(T):
    s = sum(Fraction(1, m) for m in T) - 1
    p = Fraction(1)
    for m in T:
        p *= Fraction(m - 1, m)
    return s + p


def pairwise_coprime(T):
    return all(gcd(a, b) == 1 for a, b in itertools.combinations(T, 2))


# ---------------------------------------------------------------- (a) hunt
def hunt(trials=20000, seed=7):
    rng = random.Random(seed)
    Ls = [12, 24, 36, 48, 60, 72, 90, 120, 144, 180, 240, 360]
    tested = 0
    worst = None
    for _ in range(trials):
        L = rng.choice(Ls)
        divs = [d for d in range(2, L + 1) if L % d == 0]
        k = rng.randint(2, min(len(divs), 10))
        mods = rng.sample(divs, k)
        cls = [(rng.randrange(m), m) for m in mods]
        if not is_cover(cls):
            continue
        M = sorted(mods)
        X = sum(Fraction(1, m) for m in M) - 1
        for r in range(0, min(len(M), 4) + 1):
            for T in itertools.combinations(M, r):
                if not pairwise_coprime(T):
                    continue
                v = fT(T)
                tested += 1
                assert X >= v, ("COUNTEREXAMPLE", M, T, X, v, cls)
                slack = X - v
                if T and (worst is None or slack < worst[0]):
                    worst = (slack, tuple(M), tuple(T), X, v)
    print(f"  (a) {tested} (covering, coprime-subset) pairs tested, NO violation.")
    print(f"      tightest slack {worst[0]} at M={worst[1]} T={worst[2]} X={worst[3]} f(T)={worst[4]}")


# ---------------------------------------------------------------- exhaustive small
def exhaustive(Lmax=60):
    """exhaustively enumerate ALL distinct-moduli coverings on small lattices."""
    tested = 0
    for L in [12, 24, 36, 60]:
        divs = [d for d in range(2, L + 1) if L % d == 0]
        for k in range(1, 5):
            for mods in itertools.combinations(divs, k):
                if lcm(mods) != L:
                    continue
                if sum(Fraction(1, m) for m in mods) <= 1:
                    continue
                for res in itertools.product(*[range(m) for m in mods]):
                    cls = list(zip(res, mods))
                    if not is_cover(cls):
                        continue
                    X = sum(Fraction(1, m) for m in mods) - 1
                    for r in range(0, len(mods) + 1):
                        for T in itertools.combinations(mods, r):
                            if not pairwise_coprime(T):
                                continue
                            tested += 1
                            assert X >= fT(T), ("COUNTEREXAMPLE", mods, T, X, fT(T), cls)
    print(f"  (b) exhaustive over L in 12,24,36,60, k<=4: {tested} pairs, NO violation.")


# ---------------------------------------------------------------- (c) hypotheses load-bearing
def D(C):
    return [(0, 2)] + [(2 * a + 1, 2 * n) for a, n in C]


def hypotheses():
    C = [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]
    for k in range(3):
        C = D(C)
    mods = sorted(n for _, n in C)
    X = sum(Fraction(1, m) for m in mods) - 1
    assert is_cover(C)
    print(f"  (c) cheap covering C_3: moduli {mods}, X = {X} = {float(X):.6f}")
    T = (2, 3)
    print(f"      T={T} pairwise coprime, f(T) = {fT(T)} > X   -- but 3 NOT in M.")
    assert 3 not in mods and fT(T) > X
    print("      ==> hypothesis 'T subset M' is LOAD-BEARING (lemma false without it).")
    T2 = (2, 4)
    assert 2 in mods and 4 in mods
    print(f"      T={T2} subset M but NOT coprime, f(T2) = {fT(T2)} = {float(fT(T2)):.6f} > X")
    assert fT(T2) > X
    print("      ==> hypothesis 'pairwise coprime' is LOAD-BEARING.")
    # boundary
    print(f"      f(empty) = {fT(())} (empty product = 1) ; f({{6}}) = {fT((6,))} -- both 0, vacuous but true.")


# ---------------------------------------------------------------- (d)/(e)
def crt_and_monotone(trials=3000, seed=11):
    rng = random.Random(seed)
    pools = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 25]
    for _ in range(trials):
        k = rng.randint(1, 4)
        T = rng.sample(pools, k)
        if not pairwise_coprime(T):
            continue
        cls = [(rng.randrange(m), m) for m in T]
        d = dens(cls)
        pred = 1 - Fraction(1) * __import__('functools').reduce(
            lambda a, b: a * b, [Fraction(m - 1, m) for m in T], Fraction(1))
        assert d == pred, (T, cls, d, pred)
    # monotonicity of g
    for _ in range(trials):
        k = rng.randint(1, 5)
        mods = rng.sample([2, 3, 4, 5, 6, 8, 9, 10, 12], k)
        cls = [(rng.randrange(m), m) for m in mods]
        g = sum(Fraction(1, m) for m in mods) - dens(cls)
        m2 = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 15])
        cls2 = cls + [(rng.randrange(m2), m2)]
        g2 = sum(Fraction(1, n) for _, n in cls2) - dens(cls2)
        assert g2 >= g, (cls, cls2, g, g2)
    print("  (d) CRT independence density identity holds for ALL residues tested.")
    print("  (e) g(S) = sum 1/m - dens(union S) is non-decreasing under adding a class. OK")


if __name__ == "__main__":
    print("== Lemma A2 audit ==")
    hunt()
    exhaustive()
    hypotheses()
    crt_and_monotone()
