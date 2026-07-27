"""orderings.py — digit-defined order-type-omega orderings of N and their 4-AP verdicts.

Framework: an ordering is a key function n -> tuple; the induced permutation of N lists
values sorted by key.  Restriction to values [1..M] = sort([1..M], key) (restriction
principle, PROBLEM.md).  Every key here ends with (n,) so it is total; omega-type is
argued per construction in REPORT.md (all are block-graded with finite grades, or have
key dominated below by a linear function of n).

Checker: vectorized numpy scan over all (x,d), cross-validated against the trusted
apcheck checkers on random permutations and on every construction at small M.
"""

import sys
import numpy as np

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute  # validated

# ---------------------------------------------------------------- fast witness finder

def find_mono4(perm, cap=200):
    """perm: list/array, a permutation of [1..M] in position order.
    Returns list of witnesses (x, d, orient) with orient +1 increasing / -1 decreasing,
    up to cap witnesses (scanning d ascending, x ascending)."""
    M = len(perm)
    pos = np.empty(M + 1, dtype=np.int64)
    pos[np.asarray(perm, dtype=np.int64)] = np.arange(M, dtype=np.int64)
    wits = []
    for d in range(1, (M - 1) // 3 + 1):
        top = M - 3 * d
        if top < 1:
            break
        p0 = pos[1:top + 1]
        p1 = pos[1 + d:top + d + 1]
        p2 = pos[1 + 2 * d:top + 2 * d + 1]
        p3 = pos[1 + 3 * d:top + 3 * d + 1]
        inc = (p0 < p1) & (p1 < p2) & (p2 < p3)
        dec = (p0 > p1) & (p1 > p2) & (p2 > p3)
        for orient, mask in ((1, inc), (-1, dec)):
            if mask.any():
                for xi in np.nonzero(mask)[0]:
                    wits.append((int(xi) + 1, d, orient))
                    if len(wits) >= cap:
                        return wits
    return wits


def restriction(keyfunc, M):
    return sorted(range(1, M + 1), key=keyfunc)


# ---------------------------------------------------------------- digit utilities

def v2(n):
    return (n & -n).bit_length() - 1


def v3(n):
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def block2(n):
    return n.bit_length() - 1


_P3 = [3 ** i for i in range(30)]
_P4 = [4 ** i for i in range(20)]


def block3(n):
    m = 0
    while _P3[m + 1] <= n:
        m += 1
    return m


def block4(n):
    m = 0
    while _P4[m + 1] <= n:
        m += 1
    return m


def s2(n):
    return bin(n).count("1")


def s3(n):
    s = 0
    while n:
        s += n % 3
        n //= 3
    return s


def key_sigma(n, prios=(0,), depth=25):
    """Generalized parity recursion: at level i, class bit (n_i mod 2) ordered by
    prios[i % len]: 0 = odds first, 1 = evens first; recurse on ceil(n/2)."""
    w = []
    m = n
    for i in range(depth):
        b = m & 1
        p = prios[i % len(prios)]
        w.append(1 - b if p == 0 else b)
        m = (m + 1) // 2
    return tuple(w)


def key_tau(n, prios=((0, 1, 2),), depth=25):
    """Base-3 priority recursion: at level i, digit (n mod 3) ranked by permutation
    prios[i % len]; recurse on n // 3.  Kills 4-APs on every subset (Lemma T)."""
    w = []
    m = n
    for i in range(depth):
        pr = prios[i % len(prios)]
        w.append(pr[m % 3])
        m //= 3
    return tuple(w)


def digits_negabase2(n):
    d = []
    while n != 0:
        r = n & 1
        d.append(r)
        n = (n - r) // -2
    return d  # low to high, no leading zero


def gray_inv(r):
    b = r
    s = 1
    while (1 << s) <= r.bit_length() + 1 or s <= 32:
        b ^= b >> s
        s *= 2
        if s > 64:
            break
    return b


# ---------------------------------------------------------------- constructions

def O1(n):  # dyadic blocks, parity-recursion internals
    return (block2(n),) + key_sigma(n) + (n,)


def O2(n):  # base-4 blocks, parity-recursion internals
    return (block4(n),) + key_sigma(n) + (n,)


def O3(n):  # base-4 blocks, three chunks reversed, sigma chunks
    j = block4(n)
    c = (n - _P4[j]) // _P4[j]  # 0,1,2
    return (j, 2 - c) + key_sigma(n) + (n,)


def O4(n):  # base-3 blocks, tau internals (natural priorities)
    return (block3(n),) + key_tau(n) + (n,)


def O4b(n):  # base-3 blocks, tau with priorities alternating by block parity
    j = block3(n)
    pr = ((0, 1, 2),) if j % 2 == 0 else ((2, 1, 0),)
    return (j,) + key_tau(n, pr) + (n,)


def O5(n):  # base-3 blocks, six chunks of length 3^{j-1} reversed, tau chunks
    j = block3(n)
    L = _P3[j - 1] if j >= 1 else 1
    c = (n - _P3[j]) // L
    return (j, -c) + key_tau(n) + (n,)


def make_O6(C):  # v2-promotion: even numbers delayed by factor 2^min(v2,C)
    def f(n):
        return (n << min(v2(n), C), n)
    return f


def make_O6w(C):  # windowed v2-promotion: promoted scale grouped, sigma inside windows
    def f(n):
        return ((n << min(v2(n), C)) >> C,) + key_sigma(n) + (n,)
    return f


def O7(n):  # dyadic blocks, Thue-Morse split, sigma internals
    return (block2(n), s2(n) & 1) + key_sigma(n) + (n,)


def O7b(n):  # base-3 blocks, base-3 digit-sum parity split, tau internals
    return (block3(n), s3(n) % 2) + key_tau(n) + (n,)


def O8(n):  # negabinary length blocks, digits low-to-high
    d = digits_negabase2(n)
    return (len(d), tuple(d), n)


def O8r(n):  # negabinary length blocks, digits high-to-low (lex on the string)
    d = digits_negabase2(n)
    return (len(d), tuple(reversed(d)), n)


def O9(n):  # dyadic blocks, boustrophedon (alternate-bit complement) internals
    j = block2(n)
    r = n - (1 << j)
    mask = 0
    for i in range(j - 1, -1, -2):  # complement top bit, skip one, ...
        mask |= 1 << i
    return (j, r ^ mask, n)


def O9g(n):  # dyadic blocks, reflected-Gray (true zigzag at every scale) internals
    j = block2(n)
    r = n - (1 << j)
    return (j, gray_inv(r), n)


CONSTRUCTIONS = [
    ("O1 dyadic+sigma", O1),
    ("O2 base4+sigma", O2),
    ("O3 base4+revchunks+sigma", O3),
    ("O4 base3+tau", O4),
    ("O4b base3+tau-altblocks", O4b),
    ("O5 base3+revchunks+tau", O5),
    ("O6.C1 v2-promo C=1", make_O6(1)),
    ("O6.C2 v2-promo C=2", make_O6(2)),
    ("O6.C3 v2-promo C=3", make_O6(3)),
    ("O6w.C3 v2-promo windowed", make_O6w(3)),
    ("O7 dyadic+TM+sigma", O7),
    ("O7b base3+TM3+tau", O7b),
    ("O8 negabinary lex", O8),
    ("O8r negabinary revlex", O8r),
    ("O9 dyadic+boustrophedon", O9),
    ("O9g dyadic+grayzigzag", O9g),
]


# ---------------------------------------------------------------- diagnostics

def diagnose(wits, kmax=6):
    out = []
    wits_sorted = sorted(wits, key=lambda w: (w[0] + 3 * w[1], w[1]))
    for (x, d, o) in wits_sorted[:kmax]:
        terms = [x + k * d for k in range(4)]
        out.append(
            f"    ({x},{d},{'inc' if o==1 else 'dec'}) terms={terms} "
            f"b2={[block2(t) for t in terms]} b3={[block3(t) for t in terms]} "
            f"b4={[block4(t) for t in terms]} v2(d)={v2(d)} v3(d)={v3(d)}"
        )
    return "\n".join(out)


def crossvalidate():
    import random
    rng = random.Random(196)
    # random permutations: verdicts vs trusted checker
    for _ in range(400):
        M = rng.randint(4, 60)
        p = list(range(1, M + 1))
        rng.shuffle(p)
        assert (len(find_mono4(p)) > 0) == has_monotone_kap_pos(p, 4), p
    # random small perms: witness sets vs brute enumeration
    from itertools import combinations
    for _ in range(150):
        M = rng.randint(4, 14)
        p = list(range(1, M + 1))
        rng.shuffle(p)
        brute = set()
        for idxs in combinations(range(M), 4):
            vals = [p[i] for i in idxs]
            dd = vals[1] - vals[0]
            if dd != 0 and all(vals[j + 1] - vals[j] == dd for j in range(3)):
                if dd > 0:
                    brute.add((vals[0], dd, 1))
                else:
                    brute.add((vals[3], -dd, -1))
        fast = set(find_mono4(p, cap=10 ** 9))
        assert fast == brute, (p, fast, brute)
    # every construction at small M: verdict vs trusted checker
    for name, kf in CONSTRUCTIONS:
        for M in (40, 90, 160):
            p = restriction(kf, M)
            assert sorted(p) == list(range(1, M + 1)), (name, M)
            assert (len(find_mono4(p)) > 0) == has_monotone_kap_pos(p, 4), (name, M)
    print("cross-validation OK (400 random verdicts, 150 witness-set comparisons, "
          "all constructions at M=40,90,160)")


def main():
    crossvalidate()
    M = 10 ** 4
    print(f"\n=== verdicts at M = {M} ===")
    for name, kf in CONSTRUCTIONS:
        p = restriction(kf, M)
        assert sorted(p) == list(range(1, M + 1)), name  # bijectivity of restriction
        wits = find_mono4(p, cap=100000)
        if not wits:
            print(f"[SURVIVES M=1e4] {name}")
        else:
            minM = min(x + 3 * d for (x, d, o) in wits)
            ninc = sum(1 for w in wits if w[2] == 1)
            ndec = len(wits) - ninc
            print(f"[FAILS] {name}: {len(wits)} witnesses (inc={ninc}, dec={ndec}), "
                  f"minimal max-term={minM}")
            print(diagnose(wits))


if __name__ == "__main__":
    main()
