"""scaling.py -- why NO finite-board search can probe R21-C'  (delay-height degeneracy).

Proposition F.  Fix a base b >= 3 and a board [1..N]; put J := floor(log_b N).
For a delay taking only the two values {0, K} with K > J, the set of condition-(ii)
violations among 4-APs inside [1..N] depends only on the 0/1 pattern, NOT on K.

Reason.  Along a 4-AP inside [1..N] the block jumps are D1, D2, D3 >= 0 with D2+D3 <= 1
(block-gap lemma) and D1 <= J.  A step raises the class iff D_i + (delta t)_i >= 1.  With
(delta t)_i in {0, +K, -K} and K > J >= D_i, a step with (delta t)_i = +K always raises,
a step with (delta t)_i = -K never raises, and a step with (delta t)_i = 0 raises iff
D_i >= 1.  None of that mentions K.

Consequence.  Any 0/1 solution of the (ii)-system on [1..N] inflates to delay height K
for EVERY K > J at zero cost.  So the finite question "how high can the delay be forced
along every AP on a board of size N" has the trivial answer "arbitrarily high", and every
finite proxy for R21-C' ("t is unbounded along some/every infinite AP") is degenerate --
the same failure shape as Remark 31 and Remark 36(1).

On N the degeneracy disappears: D1 = j(x+d) - j(x) is UNBOUNDED over far-left 4-APs, so
for every K there are 4-APs with D1 > K on which the rescaled delay faces a genuinely
different constraint.  Both halves are verified below.
"""

import sys, random
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-c')
from arch import blockindex


def viol_set(N, b, t, J=None):
    """(ii)-violations for c(v) = j(v) + t[v] on 4-APs inside [1..N]; exact integers."""
    jj = [0] * (N + 1)
    for v in range(1, N + 1):
        jj[v] = blockindex(v, b)
    c = [0] * (N + 1)
    for v in range(1, N + 1):
        c[v] = jj[v] + t[v]
    out = set()
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            a, b2, c3, d4 = c[x], c[x + d], c[x + 2 * d], c[x + 3 * d]
            if a < b2 < c3 < d4:
                out.add((x, d, 1))
            elif a > b2 > c3 > d4:
                out.add((x, d, -1))
    return out


if __name__ == "__main__":
    rng = random.Random(2196)
    TRIALS = 12
    print("=" * 96)
    print("PROPOSITION F (board half): t in {0,K}, K > J = floor(log_b N)")
    print("   => the (ii)-violation set on [1..N] does not depend on K")
    print("=" * 96)
    print(f"{'b':>2} {'N':>5} {'J':>3} {'trials':>7} {'K tested':>12} {'mismatches':>11}")
    for b in (3, 4, 5):
        for N in (150, 300):
            J = blockindex(N, b)
            Ks = list(range(J + 1, J + 5))
            mism = 0
            for _ in range(TRIALS):
                p = rng.random() * 0.7 + 0.15
                base = [0] * (N + 1)
                for v in range(1, N + 1):
                    base[v] = 1 if rng.random() < p else 0
                ref = viol_set(N, b, [Ks[0] * base[v] for v in range(N + 1)])
                for K in Ks[1:]:
                    if viol_set(N, b, [K * base[v] for v in range(N + 1)]) != ref:
                        mism += 1
            print(f"{b:>2} {N:>5} {J:>3} {TRIALS:>7} {str(Ks):>12} {mism:>11}", flush=True)
    print()
    print("=" * 96)
    print("PROPOSITION F (infinite half): for K <= J the scaling is NOT free")
    print("=" * 96)
    print(f"{'b':>2} {'N':>5} {'J':>3} {'K':>3} {'trials':>7} "
          f"{'#patterns with viol(K) != viol(K+1)':>38}")
    for b in (3, 4, 5):
        N = 300
        J = blockindex(N, b)
        for K in range(1, J + 3):
            diff = 0
            for _ in range(TRIALS):
                p = rng.random() * 0.7 + 0.15
                base = [0] * (N + 1)
                for v in range(1, N + 1):
                    base[v] = 1 if rng.random() < p else 0
                a = viol_set(N, b, [K * base[v] for v in range(N + 1)])
                c2 = viol_set(N, b, [(K + 1) * base[v] for v in range(N + 1)])
                if a != c2:
                    diff += 1
            print(f"{b:>2} {N:>5} {J:>3} {K:>3} {TRIALS:>7} {diff:>38}", flush=True)
    print()
    print("Reading: K > J => 0 mismatches (degenerate); K <= J => the violation set really")
    print("depends on K.  On N the far-left jump D1 is unbounded, so EVERY finite K sits in")
    print("the non-degenerate regime there: the infinite question has content, every finite")
    print("board does not.")
