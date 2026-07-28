"""
THE PIVOT (Corollary to Lemma M3 / Observation M4):
   is there a covering system of Z with distinct moduli drawn from H \\ {2}
   (equivalently: all moduli of the form (p-1)/2 with p >= 7 prime)?
A NEGATIVE answer proves that Erdos 273 has answer NO, since 2 in H can belong to at most one of
the two disjoint halves M_0, M_1, so the other half avoids 2.

This script eliminates lattices M for the pivot, cheaply, using two necessary conditions for a
SINGLE covering system drawn from S = {m | M : 2m+1 prime, m != 2}:
   (P1) budget : sum_{m in S} 1/m > 1;
   (P2) fiber  : for every prime q | M, Phi_q(S) >= 1, with Phi_q the exact max-min q-adic fiber
                 budget (same machinery as M_audit_phi.py, threshold 1 instead of 2).
Any M failing one of these admits no covering avoiding the modulus 2. Surviving M are undecided
and must be attacked by SAT / exhaustive search.

NOTE ON SCOPE: this eliminates individual lattices only. H \\ {2} is infinite, so no finite list of
eliminations can prove the pivot negatively. These are search lemmas, not a proof.

CONCLUSION: printed.
"""
import sys, os
from fractions import Fraction
from sympy import isprime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from M_audit_phi import phi_q_at_least, divisors


def pool_no2(M):
    return [m for m in divisors(M) if m >= 3 and isprime(2 * m + 1)]


def run(Ms):
    kills_budget, kills_fiber, survivors, capped = [], [], [], []
    for M in Ms:
        S = pool_no2(M)
        if not S:
            continue
        b = sum(Fraction(1, m) for m in S)
        if b <= 1:
            kills_budget.append(M)
            continue
        verdict = None
        for q in sorted({p for p in range(2, 100) if isprime(p) and M % p == 0}):
            Sq = [m for m in S]
            ok, best = phi_q_at_least(Sq, q, Fraction(1))
            if ok is False:
                verdict = ('KILL', q)
                break
            if ok is None:
                verdict = ('CAP', q, best)
                break
        if verdict and verdict[0] == 'KILL':
            kills_fiber.append((M, verdict[1]))
            print(f"  M = {M:<8} |S| = {len(S):3d} budget {float(b):.5f}  "
                  f"KILLED by Phi_{verdict[1]} < 1", flush=True)
        elif verdict and verdict[0] == 'CAP':
            capped.append(M)
            print(f"  M = {M:<8} |S| = {len(S):3d} budget {float(b):.5f}  NODE CAP q={verdict[1]}",
                  flush=True)
        else:
            survivors.append(M)
            print(f"  M = {M:<8} |S| = {len(S):3d} budget {float(b):.5f}  "
                  f"SURVIVES both tests -> undecided", flush=True)
    print(f"\nbudget kills: {len(kills_budget)}   fiber kills: {len(kills_fiber)}   "
          f"node caps: {len(capped)}   survivors: {len(survivors)}")
    if survivors:
        print("survivors (undecided, need SAT/exhaustive search):", survivors[:40])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        MMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
        # every M whose pool without 2 has budget > 1 is a candidate
        Ms = []
        for M in range(6, MMAX + 1):
            S = pool_no2(M)
            if sum(1.0 / m for m in S) > 1.0:
                Ms.append(M)
        print(f"lattices M <= {MMAX} whose pool H(M)\\{{2}} has budget > 1: {len(Ms)}")
        run(Ms)
    else:
        run([int(x) for x in sys.argv[1:]])
