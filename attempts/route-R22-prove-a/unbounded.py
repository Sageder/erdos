"""unbounded.py — the question that actually matters after R21-C is refuted.

Fact (Proposition R22-2, proved in the report): for c = j_b + t with t >= 0 and classes
emitted in increasing index order, if t <= T on an infinite AP P then
pos_P(n) <= b^{T+1} n + O(1) — LINEAR displacement on P, so P kills design principle D1.
Hence:  D1-compatibility  <=>  t is UNBOUNDED on every infinite AP.

A scale-invariant delay t(v) = tau(mantissa_b(v)) with tau : [1,b) -> {0..T} is bounded,
so the whole bounded scale-invariant family (including the R22-1 counterexample) is
D1-dead.  To be D1-compatible a scale-invariant delay must have UNBOUNDED tau, i.e.
nested level sets  [1,b) contains L_1 = {tau>=1} superset L_2 = {tau>=2} superset ...,
each of positive length (so that every AP meets each L_k in every large block).

Truncation lemma: tau satisfies (CONT) iff min(tau,T) does, for every T
(a violating 4-tuple involves 4 values; cap above their max and it survives).
So the question is decidable level by level with decide.py.

This script searches, for T = 2 and T = 3, all NESTED step taus on a rational grid
    0 = tau outside [A1,B1);  tau = k on [A_k,B_k) \\ [A_{k+1},B_{k+1});
with b > B1 > B2 > ... > A2 > A1 >= 1, and reports those satisfying (CONT).
"""
import sys, itertools
from fractions import Fraction as F
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-a')
from decide import decide                                             # noqa: E402


def nested_tau(bounds, b):
    """bounds = [(A1,B1),(A2,B2),...] strictly nested.  Returns tau cut list."""
    pts = {}
    pts[F(1)] = 0
    for k, (A, B) in enumerate(bounds, start=1):
        pts[F(A)] = k
        pts[F(B)] = k - 1
    cuts = sorted(pts.items())
    out = [(cuts[0][0], cuts[0][1])]
    for s, v in cuts[1:]:
        if v != out[-1][1]:
            out.append((s, v))
    return out


def grid(b, den):
    return [F(n, den) for n in range(den, b * den + 1)]


def search(b, T, den, limit=12):
    g = grid(b, den)
    found = []
    tried = 0
    for combo in itertools.combinations(g, 2 * T):
        # combo sorted ascending: A1 < A2 < ... < AT < BT < ... < B1
        As = combo[:T]
        Bs = combo[T:][::-1]
        bounds = list(zip(As, Bs))
        if bounds[-1][0] >= bounds[-1][1]:
            continue
        if bounds[0][1] >= b:            # need B1 < b for an interior descent
            continue
        if bounds[0][0] <= 1:
            continue
        tau = nested_tau(bounds, b)
        tried += 1
        if decide(tau, b) is None:
            found.append(bounds)
            if len(found) >= limit:
                break
    return found, tried


if __name__ == "__main__":
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    den = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    for T in (1, 2, 3):
        f, tried = search(b, T, den)
        print(f"b={b} den={den} T={T}: {len(f)} of {tried} nested taus satisfy (CONT)")
        for x in f[:8]:
            print("     ", x)
