"""
D_07_lowerbound.py

CLAIM PROVED BY THIS SCRIPT (unconditional, complete over the stated range):

  Let a covering system with pairwise distinct moduli, all in E = {p-1 : p >= 5 prime}, exist.
  By Prop. D1 it is equivalent to two DISJOINT covering systems inside H = {m : 2m+1 prime};
  let L = lcm of the H-world moduli (so the E-world lcm is 2L).  Then

     (N1)  budget(L) = sum_{m | L, m in H} 1/m  >=  2                    [both halves >= 1]
     (N2)  for every prime q :  Phi_q(D_H(L)) >= 2                       [Prop. D2, doubled]

  Both are monotone under divisibility of L.  This script
     * sieves budget(L) for EVERY L <= X (complete, no smoothness assumption),
     * for each survivor in increasing order, certifies (N2) either by exhibiting a residue
       assignment reaching 2 (randomised greedy -- a witness, hence a proof of ">= 2") or by
       the exact branch-and-bound D_05_phi proving Phi_q < 2 (hence L is killed),
     * outputs the least L that survives BOTH -> an unconditional lower bound for the
       H-world lcm of any covering system for Erdos 273.

CONCLUSION: printed at run time.
"""
import numpy as np, subprocess, os, sys
from sympy import isprime, factorint
from D_06_greedy_phi import DH, nu, greedy
from D_09_runQ import build as buildQ, exact_Q

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "D_05_phi")


def survivors(X, thresh=2.0):
    sieve = np.ones(2 * X + 2, dtype=bool)
    sieve[:2] = False
    for p in range(2, int((2 * X + 2) ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    idx = np.nonzero(sieve[5::2])[0]
    H = (5 + 2 * idx - 1) // 2
    H = H[(H >= 2) & (H <= X)]
    bud = np.zeros(X + 1, dtype=np.float64)
    for m in H:
        bud[m::m] += 1.0 / m
    ok = np.nonzero(bud >= thresh)[0]
    return [int(L) for L in ok], bud


def exact_phi_lt(ds, q, target=2.0, nodecap=400_000_000):
    """uses D_08_phiQ (single prime), which has greedy placement ordering."""
    e, flat, items = buildQ(ds, (q,))
    if not items:
        return flat < target, "no items, Phi=%.6f" % flat
    out = exact_Q(e, flat, items, (q,), target, nodecap)
    return out.startswith("PHI_LT"), out


def main(X=2_000_000, greedy_restarts=120):
    Ls, bud = survivors(X)
    print("complete sieve: %d values of L <= %d satisfy (N1) budget >= 2; smallest = %d"
          % (len(Ls), X, Ls[0]))
    sys.stdout.flush()
    killed, survived, unknown = [], [], []
    for L in Ls:
        ds = DH(L)
        verdict = "survives"
        why = ""
        for q in sorted(factorint(L)):
            v, e, ni, _ = greedy(ds, q, greedy_restarts, seed=L)
            if v >= 2.0:
                continue                    # witnessed: Phi_q >= 2
            lt, out = exact_phi_lt(ds, q)
            if lt:
                verdict = "KILLED"
                why = "q=%d exact %s (greedy only %.5f)" % (q, out, v)
                break
            elif out.startswith("PHI_UNKNOWN"):
                verdict = "unknown"
                why = "q=%d %s" % (q, out)
                break
        print("   L=%-9d budget=%.5f  %-8s %s" % (L, bud[L], verdict, why))
        sys.stdout.flush()
        if verdict == "KILLED":
            killed.append(L)
        elif verdict == "survives":
            survived.append(L)
            print("   >>> FIRST SURVIVOR L = %d  -- lower bound stops here" % L)
            break
        else:
            unknown.append(L)
            break
    print("\nkilled: %s" % killed)
    if survived:
        print("least L <= %d passing (N1)+(N2): %d" % (X, survived[0]))
        print("=> UNCONDITIONAL: any covering system for Erdos 273 has H-world lcm L with")
        print("   L not dividing any killed value, and L >= %d is the first value not"
              % survived[0])
        print("   excluded by these two local conditions.")
    if unknown:
        print("inconclusive at L = %s" % unknown)


if __name__ == "__main__":
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    main(X)
