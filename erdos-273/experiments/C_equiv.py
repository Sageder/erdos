"""
C_equiv.py  --  Route C, Step 1.

CLAIM TESTED (the parity/halving equivalence, proved by hand in the route notes, here
verified computationally in BOTH directions):

    There is a covering system of Z with pairwise distinct moduli all lying in
        E = {p-1 : p prime, p >= 5} = {n >= 4 : n+1 prime}
    IF AND ONLY IF
    there are two DISJOINT finite sets M_0, M_1 contained in
        H = {(p-1)/2 : p prime, p >= 5} = {m >= 2 : 2m+1 prime}
    such that for each j in {0,1} the set M_j is the modulus set of a covering system of Z
    (moduli pairwise distinct, each used exactly once, each > 1).

The two constructive maps are

    (=>)  n_i = 2 m_i,  eps_i = a_i mod 2 in {0,1},  a_i = 2 b_i + eps_i,
          M_j := {m_i : eps_i = j},  residue b_i mod m_i;
    (<=)  for m in M_j:  modulus 2m,  residue 2 b_{j,m} + j.

The mathematical content of BOTH maps is the single POINTWISE identity

    (P)   for every x in Z:   x in (a + 2m Z)   <=>   x = 2y + eps  and  y in (b + m Z),

where eps = a mod 2 and b = (a - eps)/2, together with the observation that a class with
an even modulus contains only integers of one parity.  This script tests (P) exhaustively
on windows of POSITIVE AND NEGATIVE integers for large random families, then tests the
"covers Z" consequence over full periods, then tests round trips, then negative controls.
Nothing here needs a covering system to exist, so the test is not circular.

CONCLUSION (printed): all assertions pass.

Runtime: a few seconds.
"""
import random
from math import lcm
from sympy import isprime


# ------------------------------------------------------------------ worlds
def in_E(n):
    return n >= 4 and isprime(n + 1)


def in_H(m):
    return m >= 2 and isprime(2 * m + 1)


def E_upto(X):
    return [n for n in range(4, X + 1) if in_E(n)]


def H_upto(Y):
    return [m for m in range(2, Y + 1) if in_H(m)]


# ------------------------------------------------------------------ the maps
def forward(classes_E):
    """E-world system -> (even-half system, odd-half system) in the H-world."""
    out = {0: [], 1: []}
    for a, n in classes_E:
        assert n % 2 == 0, "every element of E is even"
        m = n // 2
        eps = a % 2                 # Python's % gives 0/1 also for negative a
        b = (a - eps) // 2
        out[eps].append((b % m, m))
    return out[0], out[1]


def backward(sys0, sys1):
    """(M_0-system, M_1-system) in the H-world -> E-world system."""
    res = []
    for j, sysj in ((0, sys0), (1, sys1)):
        for b, m in sysj:
            res.append(((2 * b + j) % (2 * m), 2 * m))
    return sorted(res, key=lambda t: t[1])


# ------------------------------------------------------------------ verification helpers
def hit(x, classes):
    return any((x - a) % n == 0 for a, n in classes)


def covers_Z(classes, neg_window=4000):
    """True iff the union of the classes is all of Z.  Exhaustive over one full period,
    plus an independent sweep of a window of negative integers."""
    if not classes:
        return False
    L = 1
    for _a, n in classes:
        L = lcm(L, n)
    cov = bytearray(L)
    for a, n in classes:
        for x in range(a % n, L, n):
            cov[x] = 1
    if not all(cov):
        return False
    for x in range(-neg_window, 0):
        if not hit(x, classes):
            return False
    return True


# ------------------------------------------------------------------ tests
def test_worlds():
    print("=" * 78)
    print("[1] worlds E and H")
    E = E_upto(102)
    assert E[:25] == [4, 6, 10, 12, 16, 18, 22, 28, 30, 36, 40, 42, 46, 52, 58,
                      60, 66, 70, 72, 78, 82, 88, 96, 100, 102], E[:25]
    assert all(n % 2 == 0 for n in E_upto(5000)), "every element of E is even"
    print("    E starts", E[:12], "...  ALL EVEN  OK")
    H = H_upto(56)
    assert H == [2, 3, 5, 6, 8, 9, 11, 14, 15, 18, 20, 21, 23, 26, 29, 30, 33,
                 35, 36, 39, 41, 44, 48, 50, 51, 53, 54, 56], H
    print("    H up to 56 =", H)
    assert in_H(54) and isprime(109)
    print("    CORRECTION to the prompt's list: 54 IS in H (2*54+1 = 109 prime).")
    for m in [4, 7, 10, 12, 13, 16, 17, 19, 22, 24, 25, 27, 28]:
        assert not in_H(m), m
    print("    claimed omissions 4,7,10,12,13,16,17,19,22,24,25,27,28 confirmed  OK")
    assert H.count(2) == 1 and H.count(3) == 1
    print("    2 and 3 occur exactly once each in H  OK")
    assert set(E_upto(2000)) == {2 * m for m in H_upto(1000)}
    print("    n <-> 2m is a bijection E <-> H on [4,2000]  OK")
    # structural facts used later
    assert all(m % 3 != 1 for m in H_upto(5000)), "m == 1 mod 3 would make 3 | 2m+1"
    print("    every m in H satisfies m != 1 (mod 3)   [3 | 2m+1 otherwise]  OK")
    assert all(m % 5 != 2 for m in H_upto(5000) if m > 2)
    print("    every m in H with m > 2 satisfies m != 2 (mod 5)  OK")
    pw2 = [k for k in range(1, 22) if in_H(2 ** k)]
    assert pw2 == [1, 3, 7, 15], pw2
    print("    powers of two in H below 2^22: 2, 8, 128, 32768 only (Fermat primes)  OK")


def test_pointwise(rng):
    print("=" * 78)
    print("[2] POINTWISE identity (P) -- the whole content of both maps")
    N = 4000
    for trial in range(300):
        k = rng.randrange(1, 9)
        mods = rng.sample(H_upto(200), k)
        classes_E = [(rng.randrange(-500, 500), 2 * m) for m in mods]
        h0, h1 = forward(classes_E)
        for x in range(-N, N + 1):
            lhs = hit(x, classes_E)
            eps = x % 2
            y = (x - eps) // 2
            rhs = hit(y, h0 if eps == 0 else h1)
            assert lhs == rhs, (trial, x, lhs, rhs)
    print(f"    forward map: identity verified for all x in [-{N},{N}] on 300 random")
    print("    E-systems (residues include negatives; distinct even moduli)  OK")

    for trial in range(300):
        k0 = rng.randrange(1, 7)
        k1 = rng.randrange(1, 7)
        pool = H_upto(200)
        rng.shuffle(pool)
        M0, M1 = pool[:k0], pool[k0:k0 + k1]          # disjoint by construction
        s0 = [(rng.randrange(-300, 300), m) for m in M0]
        s1 = [(rng.randrange(-300, 300), m) for m in M1]
        E_sys = backward(s0, s1)
        assert len({n for _a, n in E_sys}) == len(E_sys), "moduli must be distinct"
        assert all(in_E(n) for _a, n in E_sys)
        for x in range(-N, N + 1):
            eps = x % 2
            y = (x - eps) // 2
            assert hit(x, E_sys) == hit(y, s0 if eps == 0 else s1)
    print(f"    backward map: identity verified for all x in [-{N},{N}] on 300 random")
    print("    disjoint (M_0, M_1) pairs; all moduli 2m land in E and stay distinct  OK")


def test_covering_consequence(rng):
    """The COVERAGE half of the theorem:
           union of {2b+j mod 2m} over j,m  =  Z    <=>    each half covers Z.
    This is a statement about coverage only; it is TRUE whether or not M_0 and M_1 are
    disjoint (disjointness is a separate bookkeeping condition, tested in [3c]/[4]).  So
    we can test it exhaustively over full periods with arbitrary modulus multisets, and we
    are not forced to first produce a disjoint pair of coverings (which is the open part
    of the problem)."""
    print("=" * 78)
    print("[3] the 'covers Z' consequence, checked over FULL PERIODS")
    P = [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]           # classic covering
    NP = [(0, 3), (1, 5), (2, 7)]                            # not a covering
    assert covers_Z(P) and not covers_Z(NP)
    cases = [(P, P, True), (P, NP, False), (NP, P, False), (NP, NP, False),
             (HCOVER, HCOVER, True), (HCOVER, P, True), (P, HCOVER, True)]
    for s0, s1, expect in cases:
        Es = backward(s0, s1)
        assert covers_Z(Es) == expect, (sorted(m for _a, m in s0),
                                        sorted(m for _a, m in s1), expect)
        g0, g1 = forward(Es)
        # forward recovers the halves as multisets of (residue, modulus) after reduction
        assert {(b % m, m) for b, m in g0} == {(b % m, m) for b, m in s0}
        assert {(b % m, m) for b, m in g1} == {(b % m, m) for b, m in s1}
    print("    coverage equivalence + forward/backward round trip on 7 explicit cases  OK")

    n = 0
    for _ in range(200):
        s0 = [(a + rng.randrange(-5, 6) * m, m) for a, m in rng.choice([P, HCOVER])]
        s1 = [(a + rng.randrange(-5, 6) * m, m) for a, m in rng.choice([P, HCOVER])]
        Es = backward(s0, s1)
        assert covers_Z(Es)
        g0, g1 = forward(Es)
        assert covers_Z(g0) and covers_Z(g1)
        n += 1
    print(f"    same, with residues shifted by arbitrary (signed) multiples, {n} cases  OK")

    # [3c] DISTINCTNESS bookkeeping: the E-moduli are exactly {2m : m in M_0} u {2m : m in M_1}
    for _ in range(400):
        pool = H_upto(150)
        rng.shuffle(pool)
        k0 = rng.randrange(1, 8)
        k1 = rng.randrange(1, 8)
        disjoint = rng.random() < 0.5
        M0 = pool[:k0]
        M1 = pool[k0:k0 + k1] if disjoint else pool[max(0, k0 - 2):max(0, k0 - 2) + k1]
        s0 = [(rng.randrange(m), m) for m in M0]
        s1 = [(rng.randrange(m), m) for m in M1]
        Es = backward(s0, s1)
        mods = [n for _a, n in Es]
        assert (len(set(mods)) == len(mods)) == (set(M0).isdisjoint(M1))
        assert all(in_E(n) for n in mods)
    print("    E-moduli distinct  <=>  M_0 and M_1 disjoint  (400 random pairs)  OK")

    # [3d] a genuine H-world covering (single); the OPEN part is finding two DISJOINT ones
    assert covers_Z(HCOVER)
    assert all(in_H(m) for _a, m in HCOVER)
    assert len({m for _a, m in HCOVER}) == len(HCOVER)
    print(f"    stored H-covering, moduli {sorted(m for _a,m in HCOVER)}  VERIFIED  OK")
    print(f"       -> its E-image has moduli {sorted(2*m for _a,m in HCOVER)}, all in E:",
          all(in_E(2 * m) for _a, m in HCOVER))


def test_negative_controls(rng):
    print("=" * 78)
    print("[4] negative controls")
    bad = [(0, 4), (1, 6), (2, 10)]
    assert all(in_E(n) for _a, n in bad)
    assert not covers_Z(bad)
    h0, h1 = forward(bad)
    assert not (covers_Z(h0) and covers_Z(h1))
    print("    a non-covering E-system does NOT give two covering halves  OK")
    # if M_0 and M_1 overlap, the backward map yields a REPEATED modulus
    P = [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]
    E_sys = backward(P, P)
    mods = [n for _a, n in E_sys]
    assert len(set(mods)) < len(mods)
    assert covers_Z(E_sys)          # still covers Z, but violates distinctness
    print("    overlapping M_0, M_1 -> repeated modulus (rejected by the strict")
    print("    definition) even though the union still covers Z: DISJOINTNESS is")
    print("    exactly the extra content of problem 273  OK")
    # parity bookkeeping for negative residues
    for a in range(-40, 40):
        eps = a % 2
        assert eps in (0, 1) and 2 * ((a - eps) // 2) + eps == a
    print("    a = 2b + eps with eps in {0,1} holds for negative a  OK")
    # a class with even modulus meets only one parity
    for _ in range(200):
        m = rng.choice(H_upto(200))
        a = rng.randrange(-100, 100)
        assert all((a + 2 * m * t) % 2 == a % 2 for t in range(-20, 20))
    print("    a class with an even modulus contains only one parity  OK")


# ---------------------------------------------------------------- stored certificate
# A covering of Z with distinct moduli all in H, found by C_hcover (L = 360) and
# re-verified from scratch here.  Its E-image {2m} = {4,6,10,12,16,18,30,36,40,60,72,180,240}
# is a set of admissible E-moduli; it covers ONE parity class of Z, which is why the
# problem needs a SECOND, modulus-disjoint H-covering.
HCOVER = [(0, 2), (1, 3), (3, 5), (5, 6), (1, 8), (6, 9), (6, 15), (9, 18), (19, 20),
          (15, 30), (3, 36), (57, 90), (69, 120)]


def main():
    rng = random.Random(20260728)
    test_worlds()
    test_pointwise(rng)
    test_covering_consequence(rng)
    test_negative_controls(rng)
    print("=" * 78)
    print("ALL EQUIVALENCE TESTS PASSED -- both directions verified.")


if __name__ == "__main__":
    main()
