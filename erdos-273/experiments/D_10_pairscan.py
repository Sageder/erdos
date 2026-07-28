"""
D_10_pairscan.py

CLAIM MEASURED.  The MULTI-PRIME fiber max-min  Phi_Q  (see D_08_phiQ.c for the proof that
Phi_Q(S) >= 2 is necessary, and that Phi_Q <= min_{q in Q} Phi_q, so pairs are strictly
stronger than single primes).  For each candidate L we run the exact branch-and-bound of
D_08_phiQ in BEST-VALUE mode with a node cap.  The value it reports is a rigorous LOWER bound
on Phi_Q (it is the value of an explicit assignment); if it terminates without hitting the cap
the value is exactly Phi_Q.

Reading the output:
  * "PHI x"          -> Phi_Q = x exactly.  x < 2  ==>  L is KILLED (rigorously), together
                        with every divisor of L.
  * "PHI_UNKNOWN x"  -> only x <= Phi_Q is proved; if x < 2 the test is inconclusive.

CONCLUSION: printed at run time.
"""
import sys, time
from sympy import factorint
from D_09_runQ import DH, build, exact_Q


def run(Ls, Qs, nodecap=8_000_000):
    for L in Ls:
        ds = DH(L)
        b = sum(1.0 / m for m in ds)
        print("L=%-9d fac=%-32s |D_H|=%-4d budget=%.5f"
              % (L, dict(factorint(L)), len(ds), b))
        for Q in Qs:
            if any(L % q for q in Q):
                continue
            e, flat, items = build(ds, Q)
            cells = 1
            for q, ei in zip(Q, e):
                cells *= q ** ei
            t = time.time()
            out = exact_Q(e, flat, items, Q, 0.0, nodecap)   # target 0 => best-value mode
            print("    Q=%-10s cells=%-5d items=%-4d flat=%.4f  %-34s (%.0fs)"
                  % (str(Q), cells, len(items), flat, out, time.time() - t))
            sys.stdout.flush()
        print()


if __name__ == "__main__":
    Ls = [int(a) for a in sys.argv[1:]] or [720720, 1801800, 1441440, 1081080]
    Qs = [(2, 3), (2, 5), (3, 5), (2, 7), (3, 7), (5, 7), (2, 11), (3, 11)]
    run(Ls, Qs)
