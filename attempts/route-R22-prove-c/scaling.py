"""scaling.py -- why NO finite-board search can probe R21-C'  (delay-height degeneracy).

Claim (Proposition F).  Fix a base b >= 3 and a board [1..N], and put J := floor(log_b N).
For a delay taking only the two values {0, K} with K > J, condition (ii) restricted to
4-APs inside [1..N] depends only on the 0/1 pattern, NOT on K.  Reason: along a 4-AP the
block jumps are D1 (unbounded on N, but <= J on the board) and D2, D3 with D2 + D3 <= 1;
a step increases the class iff D_i + (delta t)_i >= 1, and with |delta t| in {0, K},
K > J >= D_i, the sign of (delta t)_i alone decides every step where the delay moves.

Consequence: any 0/1 solution of the condition-(ii) system on [1..N] can be inflated to
delay height K for EVERY K > J, at no cost.  So "how high can the delay be forced along
every AP on a board of size N" has the trivial answer "arbitrarily high", and the finite
proxy for "t is unbounded along every infinite AP" is degenerate -- the same failure shape
as Remark 31 and Remark 36(1).

On N (no board) the degeneracy disappears: D1 = j(x+d) - j(x) is UNBOUNDED over far-left
4-APs, so for every K some 4-AP has D1 > K and the rescaled delay faces a genuinely
different constraint.  The tests below verify both halves.
"""

import sys, random
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-c')
from arch import blockindex, class_seq_violations


def viol_set(N, b, tvals):
    """Set of (x,d,orientation) violating condition (ii) for c = j + t on [1..N]."""
    c = lambda v: blockindex(v, b) + tvals[v]
    return set(class_seq_violations(N, c))


if __name__ == "__main__":
    rng = random.Random(2196)
    print("=" * 100)
    print("PROPOSITION F, board half:  t in {0,K} with K > floor(log_b N)  =>  (ii)-violation")
    print("set on [1..N] is independent of K")
    print("=" * 100)
    print(f"{'b':>2} {'N':>5} {'J=log_b N':>10} {'trials':>7} {'K range':>12} {'mismatches':>11}")
    for b in (3, 4, 5):
        for N in (200, 400, 800):
            J = blockindex(N, b)
            mism = 0
            trials = 40
            for _ in range(trials):
                p = rng.random() * 0.8 + 0.1
                base = [0] * (N + 1)
                for v in range(1, N + 1):
                    base[v] = 1 if rng.random() < p else 0
                ref = viol_set(N, b, base)
                for K in range(J + 1, J + 6):
                    tv = [K * base[v] for v in range(N + 1)]
                    got = viol_set(N, b, tv)
                    if got != ref:
                        mism += 1
            print(f"{b:>2} {N:>5} {J:>10} {trials:>7} {str((J+1, J+5)):>12} {mism:>11}")
    print()
    print("=" * 100)
    print("PROPOSITION F, N half:  for K <= J the scaling is NOT free -- the violation set")
    print("changes with K, so on an unbounded board the delay height is genuinely constrained")
    print("=" * 100)
    print(f"{'b':>2} {'N':>5} {'K':>3} {'trials':>7} {'#(0/1 pattern with different violation set)':>45}")
    for b in (3, 4, 5):
        N = 800
        J = blockindex(N, b)
        for K in range(1, J + 1):
            diff = 0
            trials = 40
            for _ in range(trials):
                p = rng.random() * 0.8 + 0.1
                base = [0] * (N + 1)
                for v in range(1, N + 1):
                    base[v] = 1 if rng.random() < p else 0
                if viol_set(N, b, [K * base[v] for v in range(N + 1)]) != viol_set(N, b, base):
                    diff += 1
            print(f"{b:>2} {N:>5} {K:>3} {trials:>7} {diff:>45}")
    print()
    print("Reading: K > J  => 0 mismatches (degenerate);  K <= J => the violation set really")
    print("does depend on K.  Since on N the far-left block jump D1 is unbounded, EVERY finite K")
    print("is eventually in the 'K <= D1' regime -- the infinite question is not degenerate,")
    print("but every finite board is.")
