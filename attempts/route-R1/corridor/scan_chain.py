"""scan_chain.py -- the CHAIN-RELEVANT triple region.

If Cut(a) = {V_1 < V_2 < ...} is infinite then (Lemma G, R1/final AUDIT §4)
V_{k+1} >= 3 V_k - 2 for every k >= 3, so V_4 >= 10 and every triple
(W,U,V) = (V_k, V_{k+1}, V_{k+2}) with k >= 4 satisfies

        W >= 10,   U >= 3W-2,   V >= 3U-2.

By Lemma S monotonicity each such triple must be FEASIBLE on its own.  This scan
looks for ANY feasible triple in that region.

Usage: python3 scan_chain.py WLO WHI VCAP
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_lazy, solve_eager, verify, confirm_unsat

WLO = int(sys.argv[1]); WHI = int(sys.argv[2]); VCAP = int(sys.argv[3])
TCAP = float(sys.argv[4]) if len(sys.argv) > 4 else 300.0


def vcands(U, vcap):
    """Shoulder band + island band + a coarse tail, all <= vcap."""
    out = set()
    for V in range(3 * U - 2, 3 * U + 5):
        out.add(V)
    for c in (4.0, 4.4, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.4, 6.8, 7.5, 8.5, 10.0):
        out.add(int(round(c * U)))
    return sorted(v for v in out if 3 * U - 2 <= v <= vcap)


def main():
    t0 = time.time()
    nsat = 0
    for W in range(WLO, WHI + 1):
        Us = sorted(set(list(range(3 * W - 2, 3 * W + 4))
                        + [int(round(c * W)) for c in (3.5, 4, 5, 6, 8, 10, 13, 17, 22)]))
        for U in Us:
            if U <= W or 3 * U - 2 > VCAP:
                continue
            for V in vcands(U, VCAP):
                t = time.time()
                n = V - U
                r, w = (solve_eager([W, U, V]) if n <= 90
                        else solve_lazy([W, U, V], time_cap=TCAP))
                dt = time.time() - t
                if r == 'SAT':
                    verify([W, U, V], w)
                    nsat += 1
                    print(f"*** SAT   W={W} U={U} V={V}  ({dt:.0f}s)", flush=True)
                elif r == 'UNSAT':
                    print(f"    UNSAT W={W} U={U} V={V}  ({dt:.0f}s)", flush=True)
                else:
                    print(f"    {r} W={W} U={U} V={V}  ({dt:.0f}s)", flush=True)
    print(f"# DONE W in [{WLO},{WHI}] Vcap={VCAP}: {nsat} feasible triples, "
          f"{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
