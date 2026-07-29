"""fib_mechanism.py — test a genuinely NON-base-b mechanism: Fibonacci (Zeckendorf) numeration.

Motivation. Every construction and every failure in this project used base-b carries, and
the digit-comparator dichotomy (REQUIREMENTS B2) is a statement about base-b digit priority:
for a 4-AP with b^k exactly dividing d, the critical level is k and the four terms' level-k
digits read a, a+m, a+2m, a — the wrap at b = 3 is what kills 4-APs, and the wrap is what
forces the LSD priority that destroys order type ω.

Zeckendorf representation (sums of non-consecutive Fibonacci numbers) has a different carry
structure, and Fibonacci blocks [F_k, F_{k+1}) have ratio → φ ≈ 1.618 < 3, so route R1's
block-pattern taxonomy (which needs ratio ≥ 3) does not apply. Worth one honest test.

Every layout below is a genuine permutation of [1..N] of order type ω by construction
(finite blocks concatenated). The fast checker is cross-validated against the trusted
brute-force checker before use.
"""

import sys
import numpy as np
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_brute

F = [1, 2]
while F[-1] < 300000:
    F.append(F[-1] + F[-2])


def zeck(v):
    out, i = [], len(F) - 1
    while v > 0:
        while F[i] > v:
            i -= 1
        out.append(i); v -= F[i]; i -= 1
    return out


def has_kap(seq, k):
    N = len(seq)
    pos = np.zeros(N + 1, dtype=np.int64)
    pos[np.array(seq)] = np.arange(N)
    for d in range(1, (N - 1) // (k - 1) + 1):
        top = N - (k - 1) * d
        if top < 1:
            break
        cols = [pos[1 + j * d: top + j * d + 1] for j in range(k)]
        inc = np.ones(top, dtype=bool); dec = np.ones(top, dtype=bool)
        for j in range(k - 1):
            inc &= cols[j] < cols[j + 1]
            dec &= cols[j] > cols[j + 1]
        m = inc | dec
        if m.any():
            return True, int(np.nonzero(m)[0][0]) + 1, d
    return False, None, None


if __name__ == "__main__":
    import random
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(4, 9)
        p = list(range(1, n + 1)); rng.shuffle(p)
        assert has_kap(p, 4)[0] == has_monotone_kap_brute(p, 4)
    print("fast checker cross-validated against brute force")

    KEYS = {
        'zeck-LSD':      lambda v: tuple(sorted(zeck(v))),
        'zeck-MSD':      lambda v: tuple(sorted(zeck(v), reverse=True)),
        'zeck-len-then': lambda v: (len(zeck(v)), tuple(sorted(zeck(v)))),
        'zeck-parity':   lambda v: (len(zeck(v)) % 2, v),
        'zeck-lowbit':   lambda v: (zeck(v)[-1] if zeck(v) else 0, v),
    }
    for name, keyf in KEYS.items():
        for alt in (False, True):
            for nb in (12, 16, 20):
                N = F[nb] - 1
                seq = []
                for k in range(nb):
                    blk = [v for v in range(F[k], min(F[k + 1], N + 1))]
                    blk.sort(key=keyf)
                    if alt and k % 2 == 1:
                        blk.reverse()
                    seq.extend(blk)
                seq = [v for v in seq if v <= N]
                if sorted(seq) != list(range(1, N + 1)):
                    print(f"{name} alt={alt}: NOT a permutation, skipping"); break
                h4 = has_kap(seq, 4)
                tag = f"first 4-AP at x={h4[1]}, d={h4[2]}" if h4[0] else "NO monotone 4-AP"
                print(f"{name:15s} alt={alt!s:5s} nb={nb:2d} (N={N:6d}): {tag}", flush=True)
                if h4[0]:
                    break
