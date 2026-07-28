"""
CLAIM: a rigorous LOWER BOUND on the lcm of any covering system with all moduli in E.

Method. By Lemma M3 an E-covering is two DISJOINT H-coverings drawn from the pool
S(L_H) = {m : m | L_H, 2m+1 prime}, and L_E = 2·L_H.  Two necessary conditions:
  (N1) budget:  Σ_{m ∈ S(L_H)} 1/m ≥ 2;
  (N2) fiber :  for every prime q | L_H,  Φ_q(S(L_H)) ≥ 2, where Φ_q is the max over residue
                assignments of the min over q-adic fibers of the fiber budget (derived and
                implemented exactly in M_audit_phi.py).
Any L_H failing (N1) or (N2) cannot be the H-lcm of a qualifying system.  Walking L_H upward and
eliminating gives an unconditional lower bound: L_E ≥ 2·(smallest surviving L_H).

Failing to kill an L_H proves nothing about it; it only stops the walk.
CONCLUSION: printed; recorded in NOTES.md and AUDITS.md.
"""
import sys, os
from fractions import Fraction
from sympy import isprime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from M_audit_phi import pool, phi_q_at_least


def sieve_budget(LMAX):
    """budget(L_H) = Σ over m | L_H with 2m+1 prime of 1/m, for all L_H ≤ LMAX (float screen)."""
    adm = [m for m in range(2, LMAX + 1) if isprime(2 * m + 1)]
    tot = [0.0] * (LMAX + 1)
    for m in adm:
        inv = 1.0 / m
        for x in range(m, LMAX + 1, m):
            tot[x] += inv
    return tot


if __name__ == "__main__":
    LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    tot = sieve_budget(LMAX)
    cands = [L for L in range(2, LMAX + 1) if tot[L] >= 2.0 - 1e-9]
    print(f"L_H <= {LMAX}: {len(cands)} pass the budget condition (N1); smallest = "
          f"{cands[0] if cands else None}", flush=True)
    T = Fraction(2)
    for L in cands:
        S = pool(L)
        b = sum(Fraction(1, m) for m in S)
        if b < T:
            continue                                  # exact re-check of (N1)
        verdict = None
        for q in sorted({p for p in range(2, 100) if isprime(p) and L % p == 0}):
            ok, best = phi_q_at_least(S, q, T)
            if ok is False:
                verdict = f"KILL q={q}"
                break
            if ok is None:
                verdict = f"NODECAP q={q} (best {best:.4f})"
                break
        if verdict and verdict.startswith("KILL"):
            print(f"  L_H = {L:<9} budget {float(b):.5f}   {verdict}", flush=True)
        else:
            print(f"  L_H = {L:<9} budget {float(b):.5f}   SURVIVES "
                  f"({verdict or 'every q reaches 2'})", flush=True)
            print(f"\n==> every budget-feasible L_H < {L} is eliminated.")
            print(f"==> THEOREM: any covering system with all moduli in E has lcm >= {2*L}.")
            break
    else:
        print(f"\n==> all budget-feasible L_H <= {LMAX} eliminated; lcm >= {2*LMAX}")
