"""sweep1.py — first R16 sweep: baselines + F1 weighted-digit gradings.

F1: g(n) = sum_l q_l(digit_l(n)), q_l = (0, alpha_l, beta_l), ties broken by tau*
with chosen priorities.  Rationale (REPORT.md sec. F1): for any 4-AP whose g-word
is carry-free at its cycle level, the word is (q(a), q(a+delta), q(a+2delta), q(a))
+ const, which contains an ascent and a descent whenever q_v is injective — the AP
is killed by the GRADING ITSELF via the same cycle mechanism as tau.  All residual
danger sits in carry-affected words.  Hand analysis (REPORT.md) shows delta=1
single-trit APs are ALL safe when alpha_l > beta_l (q(1) > q(2)); delta=2 cases
generate cross-level inequality demands.  This sweep measures where each law dies.
"""

import math
from r16lib import (GradedTauOrder, make_F1, prio_const, prio_magnitude,
                    prio_per_level, verdict, report_line, diagnose,
                    mode_histogram, len3)

L = 12  # levels (3^12 = 531441 > 10^4 * 3)


def geom(A, r, L=L):
    return [max(1, round(A * r ** l)) for l in range(L)]


CANDS = []

# ---- baselines (expected dead; taxonomy calibration)
CANDS.append(GradedTauOrder(lambda n: len3(n), name="B0 scale blocks + tau (O4 repro)"))
CANDS.append(GradedTauOrder(lambda n: n, name="B1 value order"))


def relabel(n, perm=(0, 2, 1)):
    tot, p = 0, 1
    while n:
        tot += perm[n % 3] * p
        p *= 3
        n //= 3
    return tot

CANDS.append(GradedTauOrder(lambda n: relabel(n), name="B2 digit-relabel (021) bijection"))
CANDS.append(GradedTauOrder(lambda n: relabel(n, (0, 2, 1)) if len3(n) % 2 == 0
                            else relabel(n, (0, 1, 2)),
                            name="B2b relabel alternating by length"))

# ---- F1: geometric laws, alpha vs beta order, several ratios
for r in (1.6, 2.0, 3.0, 4.0):
    A = geom(10, r)
    B = geom(7, r)
    CANDS.append(make_F1(A, B, name=f"F1 geom r={r} alpha>beta (10,7)"))
    CANDS.append(make_F1(B, A, name=f"F1 geom r={r} alpha<beta (7,10)"))

# magnitude-consistent tie priorities
A = geom(10, 2.0); B = geom(7, 2.0)
CANDS.append(make_F1(A, B, prio=prio_magnitude(A, B),
                     name="F1 geom r=2 a>b, prio=magnitude"))

# ---- F1: Fibonacci-coupled growth (the cross-level inequality flavor)
A = [0] * L; B = [0] * L
A[0], B[0] = 3, 2
for l in range(1, L):
    B[l] = B[l - 1] + A[l - 1]      # beta grows Fibonacci-ish
    A[l] = B[l] + B[l - 1]          # alpha stays above beta
CANDS.append(make_F1(A, B, name="F1 fib-coupled a>b"))

# ---- F1: zigzag alpha (up/down alternating), beta just below alpha
A = [0] * L; B = [0] * L
hi = 10
for l in range(L):
    if l % 2 == 0:
        A[l] = hi; B[l] = max(1, hi - 1 - l)
        hi = hi * 3
    else:
        A[l] = max(1, A[l - 1] // 4); B[l] = max(1, A[l] - 1 - l)
CANDS.append(make_F1(A, B, name="F1 zigzag alpha, beta=alpha-eps"))

# ---- F1: alpha=beta+1 tight (many ties across levels? no—values distinct)
A = geom(6, 2.0); B = [a - 1 for a in A]
CANDS.append(make_F1(A, B, name="F1 tight a=b+1 geom r=2"))

# ---- F1: pure powers of 3 with per-level magnitude permutation (bijection-like)
A = [2 * 3 ** l for l in range(L)]; B = [3 ** l for l in range(L)]
CANDS.append(make_F1(A, B, name="F1 a=2*3^l b=3^l (relabel 021 equivalent)"))
B2 = [3 ** l + (1 if l % 2 else -0) for l in range(L)]
CANDS.append(make_F1(A, B2, name="F1 a=2*3^l b=3^l perturbed"))

# ---- F1: slow growth (superlinear displacement regime: g ~ 1.3^l => pos ~ g^{~4})
for r in (1.25, 1.4):
    A = geom(8, r); B = geom(5, r)
    CANDS.append(make_F1(A, B, name=f"F1 slow geom r={r} a>b"))

if __name__ == "__main__":
    for o in CANDS:
        res = verdict(o, M=10000, quickM=1200)
        print(report_line(res), flush=True)
        if res["nwits"]:
            print(diagnose(o, res["perm"], res["wits"], kmax=5))
            h = mode_histogram(o, res["wits"])
            tot = sum(h.values())
            top = ", ".join(f"{k}:{v}" for k, v in h.most_common(6))
            print(f"    modes({tot} sampled): {top}")
        print()
