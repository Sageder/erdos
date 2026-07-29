"""wdsum.py — WEIGHTED DIGIT-SUM class architectures.

A mechanism that is neither a digit comparator nor a block layout:

    c(v) := sum_k  w_k * psi(eps_k(v))          (a numeric statistic, no level priority)

with weights w_k GROWING (so that fibres are finite: any v with top level K has
c(v) >= w_K * psi_min > 0, hence {v : c(v) <= t} is finite) but growing SLOWLY, so that no
single level dominates -- the order is therefore neither LSD (which needs w_k to dominate
all higher levels) nor MSD/block (which needs w_k to dominate all lower levels).

Fibres are highly non-convex level sets of an additive statistic, e.g. for base b and
w_k = k the class 2 is {2b..3b-1} u {b^2..b^2+b-1}.  Classes are emitted in increasing
index order, and within a class we use the base-2 van der Corput order tau_2, which is
monotone-3-AP-free on every subset (Proposition W4-1).

Reported: minimal killing monotone 4-AP of the value restriction to [1..N], the
displacement C = max pos(v)/v (for the REQUIREMENTS B7 blind-spot calculation), and the
first 4-AP that violates the Proposition W4-1 class criterion.
"""
import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from apkit import pos_from_order, find_4aps
from numeration import base_digits, zeck_digits, fibs_upto, factorial_digits


def vdc_key(v):
    return tuple(base_digits(v, 2)) + (0,) * 40


def build(cls, N):
    groups = {}
    for v in range(1, N + 1):
        groups.setdefault(cls[v], []).append(v)
    out = []
    for j in sorted(groups):
        out.extend(sorted(groups[j], key=vdc_key))
    return out


def crit_fail(cls, N, limit=1):
    out = []
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            s = [cls[x + i * d] for i in range(4)]
            if (s[0] == s[1] == s[2]) or (s[1] == s[2] == s[3]):
                continue
            if s[0] <= s[1] <= s[2] <= s[3] or s[0] >= s[1] >= s[2] >= s[3]:
                out.append((x, d, tuple(s)))
                if len(out) >= limit:
                    return out
    return out


def report(name, cls, N):
    order = build(cls, N)
    pos = pos_from_order(order)
    hits = find_4aps(pos, N)
    disp = max((int(pos[v]) + 1) / v for v in range(1, N + 1))
    nc = len(set(cls[1:N + 1]))
    big = max(sum(1 for v in range(1, N + 1) if cls[v] == j) for j in set(cls[1:N + 1]))
    cf = crit_fail(cls, N)
    s = (f"KILLED ({hits[0][2]},{hits[0][2]+hits[0][1]},{hits[0][2]+2*hits[0][1]},"
         f"{hits[0][0]}) d={hits[0][1]} {hits[0][3]}") if hits else f"4-AP-FREE to N={N}"
    print(f"{name:46s} | {s:42s} | C={disp:9.1f} | classes={nc:5d} maxfib={big:5d} "
          f"| crit-fail {cf[0] if cf else 'NONE'}")
    return hits


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    F = fibs_upto(N)
    weightfams = [("w_k=k", lambda k: k), ("w_k=k^2", lambda k: k * k),
                  ("w_k=k+1", lambda k: k + 1), ("w_k=2^k", lambda k: 2 ** k),
                  ("w_k=floor(k*1.5)", lambda k: (3 * k) // 2)]
    print("=== base-b weighted digit sums, psi = identity ===")
    for b in (2, 3, 4, 5):
        for wn, w in weightfams:
            cls = [0] * (N + 1)
            for v in range(1, N + 1):
                cls[v] = sum(w(k) * c for k, c in enumerate(base_digits(v, b)))
            report(f"base {b}, {wn}, psi=id", cls, N)
    print()
    print("=== base-b weighted digit sums, psi = a digit permutation ===")
    for b, perm in ((3, {0: 0, 1: 2, 2: 1}), (4, {0: 0, 1: 2, 2: 3, 3: 1}),
                    (5, {0: 0, 1: 3, 2: 1, 3: 4, 4: 2})):
        for wn, w in weightfams[:3]:
            cls = [0] * (N + 1)
            for v in range(1, N + 1):
                cls[v] = sum(w(k) * perm[c] for k, c in enumerate(base_digits(v, b)))
            report(f"base {b}, {wn}, psi={tuple(perm[i] for i in range(b))}", cls, N)
    print()
    print("=== Zeckendorf weighted digit sums (Fibonacci numeration, NON-comparator) ===")
    for wn, w in weightfams:
        cls = [0] * (N + 1)
        for v in range(1, N + 1):
            cls[v] = sum(w(k) * c for k, c in enumerate(zeck_digits(v, F)))
        report(f"Zeckendorf, {wn}", cls, N)
    print()
    print("=== factorial-base weighted digit sums ===")
    for wn, w in weightfams[:3]:
        cls = [0] * (N + 1)
        for v in range(1, N + 1):
            cls[v] = sum(w(k) * c for k, c in enumerate(factorial_digits(v)))
        report(f"factorial base, {wn}", cls, N)
