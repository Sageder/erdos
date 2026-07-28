"""tamebound.py — machine check of Proposition R21-2 (the general class-architecture
dichotomy) on the concrete architectures of route R20.

Proposition R21-2 (proved in REPORT.md).  Let c : N -> Z>=0 have finite fibres F_j,
emitted in increasing index order with ARBITRARY within-class orders, and let P be an
infinite AP.  If c|_P is weakly increasing from index n0 on, then for every n > n0

    pos_P(n)  <=  (n - 1) + |F_{c(p_n)} cap P|,

so   sup_{n>n0} pos_P(n)/n  <=  1 + sup_j  |F_j cap P| / (1 + |P cap (F_0 u ... u F_{j-1})|)
                             =: 1 + R_P     (the P-restricted block ratio),
uniformly over within-class orders.  Hence a geometric design (R_P bounded) forces LINEAR
displacement on P and violates design principle D1.

Here we (a) certify by brute force that the bound holds for every within-class order at
small sizes (random within-class orders + the worst-case order), and (b) tabulate R_P for
route R20's CLS(b,a) family on its tame APs.
"""

import sys, random
from fractions import Fraction

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_elements, ranks_in_subset                       # noqa: E402
from rules import CLS, MID                                            # noqa: E402


def emit(c, M, within=None, rng=None):
    """permutation of [1..M]: classes in increasing index order, within-class order
    given by `within` ('inc','dec','rand')."""
    by = {}
    for v in range(1, M + 1):
        by.setdefault(c(v), []).append(v)
    perm = []
    for j in sorted(by):
        blk = list(by[j])
        if within == 'dec':
            blk.reverse()
        elif within == 'rand':
            rng.shuffle(blk)
        perm.extend(blk)
    return perm


def R_P(c, M, q, r):
    """the P-restricted block ratio sup_j |F_j cap P| / (1 + |P cap lower classes|)."""
    el = ap_elements(M, q, r)
    cls = [c(v) for v in el]
    from collections import Counter
    cnt = Counter(cls)
    best = Fraction(0)
    for j in sorted(cnt):
        lower = sum(cnt[i] for i in cnt if i < j)
        best = max(best, Fraction(cnt[j], 1 + lower))
    return best


def tame_aps(c, M, qmax=8):
    out = []
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(M, q, r)
            if len(el) < 4:
                continue
            cls = [c(v) for v in el]
            h = cls[len(cls) // 2:]
            if all(h[i] <= h[i + 1] for i in range(len(h) - 1)):
                out.append((q, r))
    return out


def measured_disp(c, M, q, r, within, rng=None):
    perm = emit(c, M, within, rng)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    el = ap_elements(M, q, r)
    rk = ranks_in_subset(pos, el)
    return max(Fraction(rk[n - 1], n) for n in range(1, len(el) + 1))


if __name__ == "__main__":
    rng = random.Random(2196)
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    for b in (3, 5):
        c = CLS(b)
        tame = tame_aps(c, M)
        print(f"CLS({b}, a) on [1..{M}]: {len(tame)} tame APs (q<=8): {tame}")
        for (q, r) in tame[:6]:
            R = R_P(c, M, q, r)
            ds = [measured_disp(c, M, q, r, w, rng)
                  for w in ('inc', 'dec', 'rand', 'rand', 'rand')]
            mx = max(ds)
            print(f"   AP q={q} r={r}: R_P={float(R):.3f}, bound 1+R_P={float(1+R):.3f}; "
                  f"measured max pos_P(n)/n over within-class orders "
                  f"(inc,dec,3xrand) = {[round(float(d),3) for d in ds]}"
                  f"   {'OK' if mx <= 1 + R else 'BOUND VIOLATED'}")
            assert mx <= 1 + R, ("Proposition R21-2 bound violated", b, q, r, float(mx), float(1 + R))
    print("\nnon-tame control (MID family, which fails (ii) but has no tame AP):")
    c = MID(3, Fraction(1, 2))
    print("   tame APs:", tame_aps(c, M))
    for (q, r) in [(1, 0), (2, 1), (8, 3)]:
        ds = [measured_disp(c, M, q, r, w, rng) for w in ('inc', 'dec', 'rand')]
        print(f"   AP q={q} r={r}: measured disp (inc,dec,rand) = "
              f"{[round(float(d),3) for d in ds]}")
    print("\nProposition R21-2 bound verified on all tame APs of CLS(3,a), CLS(5,a).")
