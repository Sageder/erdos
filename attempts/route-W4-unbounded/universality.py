"""universality.py -- machine sanity check for Proposition W4-A.

CLAIM TESTED (Prop W4-A): the "unbounded-delay class architecture" family, as specified
(class function c : N -> Z>=0 with finite fibres, classes emitted in increasing index
order, arbitrary within-class order, written c = j + t with j(v) = floor(log_b v) and
delay t >= 0 unbounded), contains EVERY permutation of N of order type omega, with
SINGLETON fibres; and for those members condition (ii) is literally monotone-4-AP-freeness.

Construction: M_n := max(a(1..n)), phi(n) := n + floor(log_b M_n), c(v) := phi(pos_a(v)).

This script verifies, on every 4-AP-free permutation of [1..N] for N <= 8 and on random
permutations for larger N, that:
  (1) phi is strictly increasing;
  (2) c is injective (all fibres singletons, hence finite);
  (3) emitting classes in increasing index order reproduces a;
  (4) c(v) >= floor(log_b v)  for all v      [i.e. t := c - j >= 0]
  (5) t(v) >= pos(v)                          [so t is unbounded on the infinite object]
  (6) condition (ii) for c  <==>  a has no monotone 4-AP.

Cross-validated against experiments/apcheck.py.
"""
import sys, itertools, random
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute


def ilog(n, b):
    """floor(log_b n), exact integer arithmetic, n >= 1."""
    assert n >= 1
    k, p = 0, 1
    while p * b <= n:
        p *= b
        k += 1
    return k


def build_c(perm, b):
    """perm[i] = a(i+1). Returns c as a dict value -> class."""
    N = len(perm)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    M = [0] * (N + 1)
    run = 0
    for i, v in enumerate(perm):
        run = max(run, v)
        M[i + 1] = run
    phi = [None] * (N + 1)
    for n in range(1, N + 1):
        phi[n] = n + ilog(M[n], b)
    return {v: phi[pos[v]] for v in perm}, phi, pos


def cond_ii_violated(c, N):
    """condition (ii): no strictly monotone class sequence along any 4-AP."""
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            cs = [c[x + i * d] for i in range(4)]
            if cs[0] < cs[1] < cs[2] < cs[3]:
                return True
            if cs[0] > cs[1] > cs[2] > cs[3]:
                return True
    return False


def check(perm, b):
    N = len(perm)
    c, phi, pos = build_c(perm, b)
    # (1) phi strictly increasing
    assert all(phi[n] < phi[n + 1] for n in range(1, N)), "phi not strictly increasing"
    # (2) injective => singleton fibres
    assert len(set(c.values())) == N, "c not injective"
    # (3) emission order reproduces a
    emitted = sorted(range(1, N + 1), key=lambda v: c[v])
    assert emitted == list(perm), "emission order differs from a"
    # (4) c(v) >= floor(log_b v)
    assert all(c[v] >= ilog(v, b) for v in range(1, N + 1)), "t < 0 somewhere"
    # (5) t(v) >= pos(v)
    assert all(c[v] - ilog(v, b) >= pos[v] for v in range(1, N + 1)), "t(v) < pos(v)"
    # (6) condition (ii) <=> 4-AP-freeness
    return cond_ii_violated(c, N), has_monotone_kap_pos(perm, 4)


if __name__ == "__main__":
    rng = random.Random(196)
    total = 0
    for N in range(4, 9):
        for perm in itertools.permutations(range(1, N + 1)):
            for b in (2, 3, 5):
                ii, ap = check(perm, b)
                assert ii == ap, (perm, b, ii, ap)
                # independent ground truth on the AP side
                if N <= 7 and b == 2:
                    assert ap == has_monotone_kap_brute(perm, 4)
                total += 1
        print(f"N={N}: all {len(list(itertools.permutations(range(1,N+1))))} permutations OK "
              f"(b=2,3,5)", flush=True)
    for N in (20, 40, 80, 150, 300):
        for trial in range(40):
            perm = list(range(1, N + 1))
            rng.shuffle(perm)
            for b in (2, 3, 7):
                ii, ap = check(perm, b)
                assert ii == ap, (N, b)
                total += 1
        print(f"N={N}: 40 random permutations OK (b=2,3,7)", flush=True)
    print(f"Proposition W4-A verified on {total} (permutation, base) instances; "
          f"zero exceptions.")
