"""wmax.py -- is W a feasible FIRST cut of a chain-legal triple?

Chain-legality (Lemma G): any three consecutive cuts of a permutation whose cut set
has >= 4 elements satisfy U >= 3W-2 and V >= 3U-2.

For each W this scans U >= 3W-2 and V >= 3U-2 over the shoulder band and R1's
island band, and reports every feasible triple.  A finite scan can never PROVE
"no feasible triple exists" (Remark 27), so the output is a law, not a theorem.

Usage: python3 wmax.py W UMAX VCAP
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_eager, solve_lazy, verify

W = int(sys.argv[1]); UMAX = int(sys.argv[2]); VCAP = int(sys.argv[3])
TCAP = float(sys.argv[4]) if len(sys.argv) > 4 else 900.0


def feas(cuts):
    n = cuts[-1] - cuts[-2]
    r, w = (solve_eager(cuts) if n <= 85 else solve_lazy(cuts, time_cap=TCAP))
    if r == 'SAT':
        verify(cuts, w)
    return r, w


def main():
    t0 = time.time()
    sat = []
    for U in range(3 * W - 2, UMAX + 1):
        Vs = sorted({v for v in
                     list(range(3 * U - 2, 3 * U + 4))
                     + [int(round(c * U)) for c in
                        (3.3, 3.6, 4.0, 4.4, 4.8, 5.0, 5.2, 5.5, 5.8, 6.2, 6.8, 7.6)]
                     if 3 * U - 2 <= v <= VCAP})
        if not Vs:
            continue
        for V in Vs:
            t = time.time()
            r, w = feas([W, U, V])
            tag = '*** SAT' if r == 'SAT' else ('  UNSAT' if r == 'UNSAT' else '  ' + r)
            print(f"{tag} ({W},{U},{V}) V/U={V/U:.2f} [{time.time()-t:.0f}s]",
                  flush=True)
            if r == 'SAT':
                sat.append((U, V))
    print(f"# DONE W={W}, U<={UMAX}, V<={VCAP}: {len(sat)} chain-legal feasible "
          f"triples: {sat[:20]}   ({time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
