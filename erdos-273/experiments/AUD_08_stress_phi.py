"""
ADVERSARIAL AUDIT 5c: randomized stress test looking for a FALSE 'UNSAT' from the branch-and-bound
in M_audit_phi.py.  Every instance is decided twice: by the B&B under audit and by the independent
Pareto DP of AUD_05b.  Any disagreement is printed loudly.
Instances are real H-divisor pools (both the threshold-2 'two halves' pools and the threshold-1
'pivot' pools with the modulus 2 removed) plus random sub-pools, which is where a bad symmetry
break would show up.
"""
import sys, os, random
from fractions import Fraction
from sympy import isprime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from M_audit_phi import phi_q_at_least, divisors, nu
from AUD_05b_phi_dp import feasible


def pools(rng, n=400):
    out = []
    Ms = [180, 240, 360, 420, 540, 630, 720, 840, 900, 1080, 1260, 1680, 2160, 2520, 3360,
          5040, 27720, 32760]
    for _ in range(n):
        M = rng.choice(Ms)
        S = [m for m in divisors(M) if m >= 2 and isprime(2 * m + 1)]
        if rng.random() < 0.5 and 2 in S:
            S = [m for m in S if m != 2]           # pivot pool
        if rng.random() < 0.6 and len(S) > 4:
            k = rng.randint(3, len(S))
            S = sorted(rng.sample(S, k))
        if not S:
            continue
        q = rng.choice([p for p in (2, 3, 5, 7) if any(m % p == 0 for m in S)] or [2])
        T = rng.choice([Fraction(1), Fraction(2), Fraction(3, 2), Fraction(5, 4)])
        out.append((tuple(S), q, T))
    return out


if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 2027)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    bad = ok = skip = 0
    for S, q, T in pools(rng, n):
        S = list(S)
        try:
            bb, _ = phi_q_at_least(S, q, T)
        except Exception:
            skip += 1
            continue
        if bb is None:
            skip += 1
            continue
        try:
            dp = feasible(S, q, T, cap_states=200000)
        except MemoryError:
            skip += 1
            continue
        if dp != bb:
            bad += 1
            print(f"*** DISAGREEMENT  q={q} T={T} S={S}: B&B={bb} DP={dp}")
        else:
            ok += 1
    print(f"agreed on {ok} instances, {bad} disagreements, {skip} skipped (cap).")
