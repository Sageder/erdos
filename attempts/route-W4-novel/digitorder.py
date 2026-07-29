"""digitorder.py — for which base b does an LSD ("first differing digit") comparator
kill every monotone 4-AP?

Setup (exact, from the proof shape of CORE Remark 20(a)).  Let tau_b compare u,w at the
SMALLEST level where their base-b digits differ, using a linear order <_k on {0..b-1} at
level k.  For a 4-AP t_i = x+(i-1)d with k = v_b(d) and m = (d/b^k) mod b != 0:
  * all four terms agree in digits below k;
  * digit_k(t_i) = (a + (i-1)m) mod b where a = digit_k(t_1);
  * every pair (t_i,t_j) with digit_k(t_i) != digit_k(t_j) is decided at level k.
Hence tau_b is monotone-4-AP-free  <=>  for every level order <_k, every m != 0 and
every a, the cyclic quadruple (a, a+m, a+2m, a+3m) mod b is NOT <_k-monotone, where
coincidences among the four entries make monotonicity outright impossible.

This file brute-forces, for each b, whether such a linear order on Z_b exists, and
reports one.  It also CROSS-CHECKS the conclusion directly on integers by building the
comparator order on [1..N] and running the validated apkit 4-AP scan.
"""
import itertools
import sys

sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from apkit import pos_from_key, find_4aps
from numeration import base_digits


def bad_ms(b):
    """m values that need a genuine order condition (2m,3m both nonzero mod b)."""
    out = []
    for m in range(1, b):
        if (2 * m) % b == 0 or (3 * m) % b == 0:
            continue
        out.append(m)
    return out


def order_ok(b, rank):
    """rank: tuple, rank[digit] = its rank in <_k.  Check no monotone cyclic 4-AP."""
    for m in bad_ms(b):
        for a in range(b):
            q = [(a + i * m) % b for i in range(4)]
            r = [rank[t] for t in q]
            if all(r[i] < r[i + 1] for i in range(3)):
                return False
            if all(r[i] > r[i + 1] for i in range(3)):
                return False
    return True


def search(b):
    for perm in itertools.permutations(range(b)):
        # perm[i] = digit placed at rank i -> build rank array
        rank = [0] * b
        for i, dg in enumerate(perm):
            rank[dg] = i
        if order_ok(b, rank):
            return perm
    return None


def make_key(b, perm):
    rank = [0] * b
    for i, dg in enumerate(perm):
        rank[dg] = i

    def key(v):
        d = base_digits(v, b)
        return tuple(rank[c] for c in d) + (0,) * 40  # pad; LSD-first lexicographic

    return key


if __name__ == "__main__":
    print("b : #m needing a condition : witness order (rank 0 first) : integer cross-check")
    for b in range(2, 13):
        ms = bad_ms(b)
        perm = search(b)
        if perm is None:
            print(f"{b:2d} : {len(ms):2d} : NONE EXISTS (exhaustive over all {b}! orders)")
            continue
        N = 3000
        key = make_key(b, perm)
        pos, _ = pos_from_key(N, key)
        hits = find_4aps(pos, N)
        chk = "4-AP-FREE to N=%d" % N if not hits else "FAILS: %r" % (hits[0],)
        print(f"{b:2d} : {len(ms):2d} : {perm} : {chk}")
    # a base where no order exists: also cross-check that the comparator really fails
    print()
    print("counter-direction check: for b with NO valid order, every order must fail on ints")
    for b in (5, 7, 9, 10, 11):
        if search(b) is not None:
            continue
        worst = None
        for perm in itertools.permutations(range(b)):
            key = make_key(b, perm)
            pos, _ = pos_from_key(400, key)
            h = find_4aps(pos, 400)
            if not h:
                worst = perm
                break
        print(f"  b={b}: some order 4-AP-free on [1..400]? {worst!r}")
