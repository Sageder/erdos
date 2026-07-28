"""bounded_delay.py — machine check of the window-displacement bound behind the
conditional theorem on class architectures with BOUNDED delay.

Setting. A class architecture: c : N -> Z>=0 with finite fibres F_k, classes emitted in
increasing index order, arbitrary order within each class. Take c = j + t with
j(v) = floor(log_b v) and 0 <= t <= T bounded. Then |F_k| <= sum_{m=k-T}^{k} |block m|
is automatically geometric.

Claim to check (the finite-window analogue of CORE Proposition 29). Let P = r + qN and let
W = {p_1 < ... < p_L} be a finite window of P on which t is CONSTANT. Then reading the
permutation restricted to W in position order gives, for every n,

        pos_W(n)  <=  n + #{m : j(p_m) = j(p_n)}      ... (*)

and hence  max_n pos_W(n)/n  <=  B(b, q, L)  with B bounded in terms of b alone
(asymptotically ~ b), UNIFORMLY over all within-class orders.

This script:
 (1) verifies (*) by brute force over random within-class orders, random b, q, r, and
     random constant-t windows;
 (2) measures max_n pos_W(n)/n over such windows to confirm it stays ~b and does NOT grow
     with L (the point of the theorem);
 (3) confirms the companion fact that j is non-decreasing along every AP, so t constant on
     a window makes c non-decreasing there.
Exact integer arithmetic; no floats in the logic (log_b via integer bounds).
"""

import sys, random
sys.path.insert(0, '/home/user/erdos/experiments')


def block_index(v, b):
    """floor(log_b v) by exact integer arithmetic."""
    j, p = 0, 1
    while p * b <= v:
        p *= b
        j += 1
    return j


def window_displacement(b, q, r, L, T, rng, tconst=True):
    """Build an explicit class architecture on a range covering the window, with t
    constant on the window (and arbitrary elsewhere), random within-class orders, then
    measure the restricted displacement along the window."""
    P = [r + q * i for i in range(1, L + 1)]
    V = max(P)
    # delay: constant tau on the window, arbitrary in [0,T] elsewhere
    tau = rng.randint(0, T)
    t = {}
    Wset = set(P)
    for v in range(1, V + 1):
        t[v] = tau if v in Wset else rng.randint(0, T)
    c = {v: block_index(v, b) + t[v] for v in range(1, V + 1)}
    # emit classes in increasing index order, random order inside each class
    order = []
    for k in range(0, max(c.values()) + 1):
        cls = [v for v in range(1, V + 1) if c[v] == k]
        rng.shuffle(cls)
        order.extend(cls)
    pos = {v: i + 1 for i, v in enumerate(order)}
    # restricted position ranks along the window
    ranks = sorted(P, key=lambda v: pos[v])
    posW = {v: i + 1 for i, v in enumerate(ranks)}
    worst = 0.0
    for n, p in enumerate(P, start=1):
        same = sum(1 for pp in P if block_index(pp, b) == block_index(p, b))
        assert posW[p] <= n + same, ("(*) VIOLATED", b, q, r, L, n, posW[p], same)
        worst = max(worst, posW[p] / n)
    return worst


if __name__ == "__main__":
    rng = random.Random(196)

    # (3) j is non-decreasing along every AP -- trivial but assert it
    for _ in range(2000):
        b = rng.randint(2, 6); q = rng.randint(1, 20); r = rng.randint(0, 20)
        prev = -1
        for i in range(1, 60):
            jj = block_index(r + q * i, b)
            assert jj >= prev
            prev = jj
    print("j non-decreasing along every AP: OK")

    # (1) + (2)
    print("\nwindow displacement max_n pos_W(n)/n, t constant on the window")
    print("(bound should stay ~b and NOT grow with the window length L)")
    for b in (2, 3, 4, 5):
        row = []
        for L in (10, 20, 40, 80, 160):
            worst = 0.0
            for _ in range(12):
                q = rng.randint(1, 8); r = rng.randint(0, 8); T = rng.randint(0, 3)
                worst = max(worst, window_displacement(b, q, r, L, T, rng))
            row.append(f"L={L}: {worst:.2f}")
        print(f"  b={b}: " + "  ".join(row), flush=True)
    print("\n(*) verified on every case above (assertion inside window_displacement).")
