"""wlaw.py -- the FIRST-CUT LAW  W*(U,V) = max feasible first cut, measured in the
CHAIN-RELEVANT range W <= (U+2)/3 (Lemma G forces U >= 3W-2 for any three cuts with
something below W).

Prints the full S/U pattern over W = 1..floor((U+2)/3) so non-monotonicity is visible.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_eager, solve_lazy, verify

TCAP = 900

def feas(W, U, V):
    n = V - U
    r, w = (solve_eager([W, U, V]) if n <= 90 else solve_lazy([W, U, V], time_cap=TCAP))
    if r == 'SAT':
        verify([W, U, V], w)
    return r

def main():
    jobs = []
    for U in [46, 55, 64, 80, 100, 136]:
        jobs.append((U, 3 * U - 2))
    for U in [46, 55, 64, 80, 100]:
        jobs.append((U, 5 * U))
    for U, V in jobs:
        wmax_chain = (U + 2) // 3
        pat = []
        t0 = time.time()
        for W in range(1, wmax_chain + 1):
            r = feas(W, U, V)
            pat.append({'SAT': 'S', 'UNSAT': 'U'}.get(r, '?'))
            print(f"    U={U} V={V} W={W}: {r}  ({time.time()-t0:.0f}s)", flush=True)
        s = ''.join(pat)
        sats = [i + 1 for i, c in enumerate(pat) if c == 'S']
        print(f"### U={U:4d} V={V:5d} ratio={V/U:.2f}  W=1..{wmax_chain}: {s}  "
              f"W*={max(sats) if sats else None}  (U/W*="
              f"{U/max(sats):.2f})" if sats else
              f"### U={U:4d} V={V:5d}: no feasible W", flush=True)

if __name__ == "__main__":
    main()
