"""thresh.py -- the FIRST-CUT THRESHOLD  W*(U,V) = max{W < U : (W,U,V) feasible}.

For a family of (U,V) it reports the whole feasibility pattern in W (so that
non-monotonicity in W, if any, is visible rather than assumed).
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_lazy, solve_eager, verify

def feas(W, U, V, tcap=600):
    n = V - U
    r, w = (solve_eager([W, U, V]) if n <= 90 else solve_lazy([W, U, V], time_cap=tcap))
    if r == 'SAT':
        verify([W, U, V], w)
    return r

def main():
    pairs = []
    for U in [4, 7, 10, 13, 16, 20, 22, 26, 28, 34, 40, 46, 55, 64, 80, 100]:
        pairs.append((U, 3 * U - 2))            # shoulder
    for U in [10, 16, 20, 26, 28, 34, 46]:
        pairs.append((U, int(round(5.0 * U))))  # R1's island centre
    for U, V in pairs:
        pat = []
        for W in range(1, U):
            r = feas(W, U, V)
            pat.append('S' if r == 'SAT' else ('U' if r == 'UNSAT' else '?'))
            if r == 'SAT':
                last = W
        s = ''.join(pat)
        sats = [i + 1 for i, c in enumerate(pat) if c == 'S']
        print(f"U={U:4d} V={V:5d}  W=1..{U-1}: {s}   Wmax={max(sats) if sats else None}",
              flush=True)

if __name__ == "__main__":
    main()
