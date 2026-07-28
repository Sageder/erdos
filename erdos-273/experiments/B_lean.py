"""
B_lean.py -- Route B: how CHEAP can a covering system drawn from a Route-B pool be?

CLAIM TESTED
------------
The binding resource at every node of the Route-B tree is reciprocal budget.  A node D whose
class must be finished by a covering drawn from
        P(D,M) = { f | M, f >= 2, D f + 1 prime }
consumes  sum_{f used} 1/f  >= 1  of the pool's budget  sum_{f in P} 1/f.
Sibling nodes at the SAME D need pairwise DISJOINT modulus sets, so the number of siblings a
node can support is at most  budget(P(D,M)) / (minimum weight of a covering drawn from P).

This script measures the MINIMUM WEIGHT of a covering system drawn from P(D,M):
weighted greedy (maximise  #newly-covered * f , i.e. gain per unit of 1/f cost) with random
restarts, followed by redundancy pruning.  It then repeats on the leftover pool to see how
many pairwise disjoint coverings P(D,M) supports.

CONCLUSION: printed; recorded in attempts/route-B-recursive/FINDINGS.md

usage: python3 B_lean.py --D 2 --M 5040 [--restarts 400] [--copies 3] [--fmin 2]
"""
import argparse, random
from fractions import Fraction
from sympy import isprime, factorint


def divisors(n):
    ds = [1]
    for p, a in factorint(n).items():
        ds = [d * p ** i for d in ds for i in range(a + 1)]
    return sorted(ds)


def pool(D, M, fmin=2):
    return [f for f in divisors(M) if f >= fmin and D * f >= 4 and isprime(D * f + 1)]


def weighted_greedy(M, P, rng, alpha=0.0, jitter=0.15):
    """pick (f,a) maximising  gain * f^alpha ; alpha=0 is plain max-gain greedy."""
    uncov = list(range(M))
    unused = set(P)
    chosen = {}
    while uncov and unused:
        bestval, bestpair = -1.0, None
        for f in unused:
            cnt = [0] * f
            for x in uncov:
                cnt[x % f] += 1
            g = max(cnt)
            val = g * (f ** alpha) * (1.0 + jitter * (rng.random() - 0.5))
            if val > bestval:
                # random tie-break among argmax residues
                besta = rng.choice([a for a in range(f) if cnt[a] == g])
                bestval, bestpair = val, (f, besta)
        f, a = bestpair
        chosen[f] = a
        unused.discard(f)
        uncov = [x for x in uncov if x % f != a]
    return (chosen if not uncov else None)


def prune(M, chosen):
    """remove redundant moduli, largest 1/f first (i.e. smallest f first)"""
    ch = dict(chosen)
    for f in sorted(ch.keys()):
        trial = {g: b for g, b in ch.items() if g != f}
        cov = bytearray(M)
        for g, b in trial.items():
            cov[b % g::g] = b"\x01" * len(range(b % g, M, g))
        if all(cov):
            ch = trial
    return ch


def check(M, chosen):
    cov = bytearray(M)
    for g, b in chosen.items():
        cov[b % g::g] = b"\x01" * len(range(b % g, M, g))
    return M - sum(cov)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--D", type=int, default=2)
    ap.add_argument("--M", type=int, default=5040)
    ap.add_argument("--fmin", type=int, default=2)
    ap.add_argument("--restarts", type=int, default=200)
    ap.add_argument("--copies", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    P = pool(a.D, a.M, a.fmin)
    tot = sum(Fraction(1, f) for f in P)
    print(f"D={a.D} M={a.M} |P|={len(P)} budget={float(tot):.5f}")
    print(f"P = {P[:40]}{' ...' if len(P) > 40 else ''}")

    global ALPHAS
    ALPHAS = [0.0, 0.0, 0.1, 0.2, 0.3, 0.5]
    avail = list(P)
    for c in range(a.copies):
        best, bestw = None, None
        for r in range(a.restarts):
            ch = weighted_greedy(a.M, avail, rng, alpha=ALPHAS[r % len(ALPHAS)])
            if ch is None:
                continue
            ch = prune(a.M, ch)
            assert check(a.M, ch) == 0
            w = sum(Fraction(1, f) for f in ch)
            if bestw is None or w < bestw:
                bestw, best = w, ch
        if best is None:
            print(f"  copy {c+1}: NO covering found from the remaining pool "
                  f"(remaining budget {float(sum(Fraction(1,f) for f in avail)):.5f}, "
                  f"|pool|={len(avail)})")
            break
        print(f"  copy {c+1}: weight = {float(bestw):.5f}  ({len(best)} moduli)  "
              f"moduli={sorted(best)}")
        avail = [f for f in avail if f not in best]
        print(f"           remaining pool budget = "
              f"{float(sum(Fraction(1,f) for f in avail)):.5f}  (|pool|={len(avail)})")


if __name__ == "__main__":
    main()
