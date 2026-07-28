"""
COMBINED ELIMINATOR for candidate lcm values of a covering system with all moduli in E.

Three independent necessary conditions are applied to every L with B_E(L) > 1:
  (N1) budget       : B_E(L) := sum_{n | L, n in E} 1/n  >  1              [Lemma M1]
  (N2) coprime/A3   : if 60 | L and B_E(L) <= 31/30 the moduli 4, 6, 10 are all forced, their
                      halves 2, 3, 5 are pairwise coprime with f({3,5}) = 1/15 >= 2 B_E(L) - 2,
                      and Lemma A2 forbids any two of them from sharing a parity half -- three
                      objects, two halves, contradiction.                   [Route A, audited]
  (N3) fiber        : for every prime q | L/2, Phi_q(S) >= 2 where S = {m : m | L/2, 2m+1 prime}
                      and Phi_q is the exact max-min q-adic fiber budget.   [Route D, audited]
Any L failing one of them cannot be the lcm of a qualifying covering system.

CONCLUSION: printed -- the list of surviving candidates and hence a lower bound on the lcm.
"""
import sys, os
from fractions import Fraction
from sympy import isprime
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from M_audit_phi import pool, phi_q_at_least


def candidates(LMAX):
    bs = bytearray([1]) * (LMAX + 2)
    bs[0] = bs[1] = 0
    i = 2
    while i * i <= LMAX + 1:
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
        i += 1
    adm = [n for n in range(4, LMAX + 1) if bs[n + 1]]
    tot = np.zeros(LMAX + 1)
    for n in adm:
        tot[n::n] += 1.0 / n
    return [int(L) for L in np.flatnonzero(tot > 1.0 + 1e-12)]


def BE(L):
    return sum(Fraction(1, n) for n in range(4, L + 1) if L % n == 0 and isprime(n + 1))


if __name__ == "__main__":
    LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6
    cand = candidates(LMAX)
    print(f"candidate lcm values L <= {LMAX} with B_E(L) > 1: {len(cand)}   smallest {cand[0]}",
          flush=True)
    survivors, killA3, killphi, capped = [], [], [], []
    for L in cand:
        b = BE(L)
        if b <= 1:
            continue
        if L % 60 == 0 and b <= Fraction(31, 30):
            killA3.append(L)
            continue
        LH = L // 2
        S = pool(LH)
        verdict = None
        for q in sorted({p for p in range(2, 100) if isprime(p) and LH % p == 0}):
            ok, best = phi_q_at_least(S, q, Fraction(2))
            if ok is False:
                verdict = ('KILL', q)
                break
            if ok is None:
                verdict = ('CAP', q, best)
                break
        if verdict and verdict[0] == 'KILL':
            killphi.append((L, verdict[1]))
            print(f"  L = {L:<9} B_E = {float(b):.5f}  KILLED by Phi_q, q = {verdict[1]}",
                  flush=True)
        elif verdict and verdict[0] == 'CAP':
            capped.append((L, verdict))
            print(f"  L = {L:<9} B_E = {float(b):.5f}  NODE CAP at q = {verdict[1]} "
                  f"(best {verdict[2]:.4f}) -> UNDECIDED", flush=True)
        else:
            survivors.append(L)
            print(f"  L = {L:<9} B_E = {float(b):.5f}  SURVIVES all three tests", flush=True)
    print(f"\nkilled by budget-only enumeration : {LMAX - len(cand)} (implicitly)")
    print(f"killed by A3 (coprime pigeonhole)  : {len(killA3)}")
    print(f"killed by the fiber condition      : {len(killphi)}")
    print(f"undecided (node cap)               : {len(capped)}  {[c[0] for c in capped]}")
    print(f"SURVIVORS                          : {len(survivors)}  {survivors}")
    if not survivors and not capped:
        print(f"\n==> THEOREM: any covering system with all moduli in E has lcm > {LMAX}.")
