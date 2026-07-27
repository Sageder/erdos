"""lemmas_check.py — machine tests for the R3 digit lemmas BEFORE the proofs are trusted.

Claims tested (statements + proofs in REPORT.md):

L1 (valuation trichotomy): for any 4-AP x, x+d, x+2d, x+3d (x,d >= 1), with v = v2(d):
    (i)   if v2(x) < v:  v2(x+kd) = v2(x) for all k (constant).
    (ii)  if v2(x) = v:  v2(x) = v2(x+2d) = v; v2(x+d), v2(x+3d) >= v+1 with min exactly v+1.
    (iii) if v2(x) > v:  v2(x+d) = v2(x+3d) = v; v2(x), v2(x+2d) >= v+1 with min exactly v+1.
    Corollaries: v2 takes <= 3 distinct values along any 4-AP; the argmin set of v2 is
    {0,1,2,3}, {0,2} or {1,3}; in the non-constant cases the v2 multiset is {v,v,v+1,s}, s>=v+1.

L2 (block-gap lemma): m_k^{(b)} := floor(log_b(x+kd)).  Always m_0<=m_1<=m_2<=m_3.
    For every base b>=2:  m_2 <= m_1 + 1 and m_3 <= m_2 + 1.
    For b >= 3:           m_3 <= m_1 + 1  (so among the last three terms at least one
                          adjacent pair shares a base-b block; never two "jumps").
    For b = 2:            m_3 <= m_1 + 2, and four pairwise-distinct blocks DO occur:
                          the family x = 2^M, d = 5*2^M has blocks (M, M+2, M+3, M+4).

L3 (carry identity): with c(a,b) := number of carries when adding a+b in base 2
    (Legendre/Kummer: c(a,b) = s2(a)+s2(b)-s2(a+b)),
    [s2(x)+s2(x+3d)] - [s2(x+d)+s2(x+2d)] = c(x, x+3d) - c(x+d, x+2d)
    (since x + (x+3d) = (x+d) + (x+2d)).  Also c computed by direct addition simulation
    must equal the Legendre formula (validates both).

T (tau kills 4-APs on every subset): the base-3 priority comparator tau
    (compare lowest base-3 digit through a per-level priority permutation; on equality
    recurse on the quotient) linearly orders N and admits NO monotone 4-AP on ANY subset,
    for EVERY choice of per-level priorities.  (Analog of the parity recursion one level up:
    sigma kills 3-APs on every subset; tau kills 4-APs on every subset.  Neither is omega.)

S (sigma kills 3-APs on every subset): the parity comparator (odd-first, recurse on
    ceil(n/2)) admits no monotone 3-AP on any subset.

PropB family: for t >= 1 and odd u > 2^t, (2^t, u, 2u-2^t, 3u-2^{t+1}) is a 4-AP in case
    (iii) of L1 whose minimal-valuation terms are u and 3u-2^{t+1} and whose
    higher-valuation terms include 2^t.  (Used to prove: no order of type omega breaks all
    4-APs purely by the "minimal-v2-class-first" mechanism.)

Exact integer arithmetic throughout.  Random tests up to 10^6 plus exhaustive small ranges.
"""

import random
import sys

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_general  # validated checker

rng = random.Random(196)


def v2(n):
    assert n >= 1
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


def v3(n):
    assert n >= 1
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def s2(n):
    return bin(n).count("1")


def digits3(n, depth):
    out = []
    for _ in range(depth):
        out.append(n % 3)
        n //= 3
    return out


def blockb(n, b):
    assert n >= 1
    m = 0
    p = b
    while p <= n:
        m += 1
        p *= b
    return m


def carries_direct(a, b):
    """Simulate base-2 addition, count carries."""
    c = 0
    carry = 0
    while a or b or carry:
        s = (a & 1) + (b & 1) + carry
        carry = 1 if s >= 2 else 0
        c += carry
        a >>= 1
        b >>= 1
    return c


def check_L1(x, d):
    v = v2(d)
    vals = [v2(x + k * d) for k in range(4)]
    sx = v2(x)
    if sx < v:
        assert vals == [sx] * 4, (x, d, vals)
        arg = {0, 1, 2, 3}
    elif sx == v:
        assert vals[0] == v and vals[2] == v, (x, d, vals)
        assert vals[1] >= v + 1 and vals[3] >= v + 1, (x, d, vals)
        assert min(vals[1], vals[3]) == v + 1, (x, d, vals)
        arg = {0, 2}
    else:
        assert vals[1] == v and vals[3] == v, (x, d, vals)
        assert vals[0] >= v + 1 and vals[2] >= v + 1, (x, d, vals)
        assert min(vals[0], vals[2]) == v + 1, (x, d, vals)
        arg = {1, 3}
    # corollaries
    assert len(set(vals)) <= 3, (x, d, vals)
    mn = min(vals)
    assert {k for k in range(4) if vals[k] == mn} == arg or sx < v, (x, d, vals)
    if sx >= v:
        ms = sorted(vals)
        assert ms[0] == v and ms[1] == v and ms[2] == v + 1, (x, d, vals)


def check_L2(x, d):
    for b in (2, 3, 4, 5):
        m = [blockb(x + k * d, b) for k in range(4)]
        assert m[0] <= m[1] <= m[2] <= m[3], (b, x, d, m)
        assert m[2] <= m[1] + 1, (b, x, d, m)
        assert m[3] <= m[2] + 1, (b, x, d, m)
        if b >= 3:
            assert m[3] <= m[1] + 1, (b, x, d, m)
        else:
            assert m[3] <= m[1] + 2, (b, x, d, m)


def check_L3(x, d):
    a1, a2 = x, x + 3 * d
    b1, b2 = x + d, x + 2 * d
    assert a1 + a2 == b1 + b2
    cd_a = carries_direct(a1, a2)
    cd_b = carries_direct(b1, b2)
    assert cd_a == s2(a1) + s2(a2) - s2(a1 + a2), (x, d)
    assert cd_b == s2(b1) + s2(b2) - s2(b1 + b2), (x, d)
    lhs = (s2(a1) + s2(a2)) - (s2(b1) + s2(b2))
    assert lhs == cd_a - cd_b, (x, d)


# ---------------- comparators sigma (base 2) and tau (base 3) ----------------

def key_sigma(n, depth=25):
    """Parity word of the ceil(n/2)-orbit; lex-sorting by this = parity recursion
    (odds first, recursively). Component 0 for odd (comes first), 1 for even."""
    w = []
    m = n
    for _ in range(depth):
        w.append(0 if m % 2 == 1 else 1)
        m = (m + 1) // 2
    return tuple(w)


def key_tau(n, priorities, depth=25):
    """priorities: list of permutations of (0,1,2), one per digit level (cycled).
    Lex-sorting by this key = base-3 priority recursion."""
    w = []
    m = n
    for lev in range(depth):
        pr = priorities[lev % len(priorities)]
        w.append(pr[m % 3])
        m //= 3
    return tuple(w)


def sorted_by(key, S):
    return sorted(S, key=key)


def main():
    # exhaustive small + random large for L1-L3
    for x in range(1, 260):
        for d in range(1, 260):
            check_L1(x, d)
            check_L2(x, d)
            check_L3(x, d)
    for _ in range(20000):
        x = rng.randint(1, 10 ** 6)
        d = rng.randint(1, 10 ** 6)
        check_L1(x, d)
        check_L2(x, d)
        check_L3(x, d)
    print("L1, L2, L3: OK (exhaustive x,d<260 and 20000 random pairs up to 10^6)")

    # Theorem A part (a): the forced family
    for M in range(0, 25):
        terms = [2 ** M * t for t in (1, 6, 11, 16)]
        blocks = [blockb(t, 2) for t in terms]
        assert blocks == [M, M + 2, M + 3, M + 4], (M, blocks)
        # it is an AP: x = 2^M, d = 5*2^M
        assert terms[1] - terms[0] == terms[2] - terms[1] == terms[3] - terms[2] == 5 * 2 ** M
    print("Theorem A(a): 2^M*(1,6,11,16) has pairwise distinct dyadic blocks (M,M+2,M+3,M+4), M<25: OK")

    # base >= 3: no 4-AP with 3 distinct blocks among last three (already in L2), and
    # base 2: 4 distinct blocks occur — count occurrences in a range
    found = 0
    for x in range(1, 2000):
        for d in range(1, 2000):
            m = [blockb(x + k * d, 2) for k in range(4)]
            if len(set(m)) == 4:
                found += 1
    assert found > 0
    print(f"base 2: 4-APs with 4 pairwise-distinct dyadic blocks exist ({found} with x,d<2000): OK")

    # S: sigma kills 3-APs on every subset
    for trial in range(3000):
        n = rng.randint(3, 12)
        S = rng.sample(range(1, 400), n)
        seq = sorted_by(key_sigma, S)
        assert not has_monotone_kap_general(seq, 3), (S, seq)
    print("S: sigma comparator 3-AP-free on 3000 random subsets: OK")

    # T: tau kills 4-APs on every subset, for random per-level priorities
    perms3 = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
    for trial in range(3000):
        n = rng.randint(4, 14)
        S = rng.sample(range(1, 700), n)
        pri = [rng.choice(perms3) for _ in range(25)]
        seq = sorted_by(lambda t: key_tau(t, pri), S)
        assert not has_monotone_kap_general(seq, 4), (S, pri, seq)
    # also: tau does NOT kill all 3-APs (sanity: it cannot, DEGS77(a))
    tau_nat = lambda t: key_tau(t, [(0, 1, 2)])
    seq = sorted_by(tau_nat, range(1, 100))
    assert has_monotone_kap_general(seq, 3)
    print("T: tau comparator 4-AP-free on 3000 random subsets w/ random priorities; has 3-APs: OK")

    # PropB family: (2^t, u, 2u-2^t, 3u-2^{t+1}) checks
    for t in range(1, 12):
        w = 2 ** t
        for u in range(w + 1, 8 * w, 2):  # odd u > 2^t
            x, d = w, u - w
            terms = [x, x + d, x + 2 * d, x + 3 * d]
            assert terms == [w, u, 2 * u - w, 3 * u - 2 * w]
            assert all(s >= 1 for s in terms)
            assert d >= 1 and d % 2 == 1
            assert v2(terms[0]) >= 1 and v2(terms[2]) >= 1  # high-valuation slots
            assert v2(terms[1]) == 0 and v2(terms[3]) == 0  # minimal-valuation slots
    print("PropB family: (2^t, u, 2u-2^t, 3u-2^{t+1}) valuation pattern verified: OK")

    print("ALL LEMMA CHECKS PASSED")


if __name__ == "__main__":
    main()
