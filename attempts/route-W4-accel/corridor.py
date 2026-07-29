"""corridor.py -- the family that matters.

Any cut sequence V_1<...<V_k of a monotone-4-AP-free permutation of N satisfies
V_{j+1} >= 3V_j - 2 for j >= 2 (Lemma G, route-R1/final AUDIT sec.4).  Hence
  V_3 >= 4, V_4 >= 10, V_5 >= 28,
so EVERY cut sequence with >= 5 elements contains a pair (W,U) = (V_4,V_5) with
  W >= 10  and  U >= 3W-2.
Call this family P.  If every pair in P is infeasible, cut sets have at most 4
elements and NO in-order block construction (accelerating or not) exists.

This script decides membership of P in the pair-death set, using the FULL system
N(W,U,M) (stronger than the TOP relaxation, so it dies at a smaller horizon).
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def run(W, U, M, cap=900, relax=False, solver='cadical195'):
    S = wsys.Sys((W, U), M, window=((U + 1, M) if relax else None))
    v, o = wsys.solve_lazy(S, time_cap=cap, solver=solver)
    if v == 'GEOM_DEAD':
        v = 'UNSAT'
    return v


def death(W, U, mults=(3, 4, 5, 6, 8), cap=900, relax=False):
    for m in mults:
        M = int(m * U) - 2 if m == 3 else int(m * U)
        r = run(W, U, M, cap=cap, relax=relax)
        if r == 'UNSAT':
            return 'DEAD', M
        if r == 'TIME_CAP':
            return 'TIMEOUT', M
    return 'ALIVE', int(mults[-1] * U)


if __name__ == '__main__':
    job = sys.argv[1]
    if job == 'diag':
        print("## P-diagonal U = 3W-2 (the smallest legal successor of W)")
        for W in range(10, 41):
            U = 3 * W - 2
            t0 = time.time()
            st, M = death(W, U)
            print(f"  ({W},{U}): {st} M0<={M} ratio={M/U:.2f} "
                  f"[{time.time()-t0:.0f}s]", flush=True)
    elif job == 'accel':
        print("## acceleration test: W = 10 fixed, U -> large")
        for U in (28, 34, 46, 55, 64, 80, 90, 100, 120):
            t0 = time.time()
            st, M = death(10, U, cap=1500)
            print(f"  (10,{U}): {st} M0<={M} ratio={M/U:.2f} "
                  f"[{time.time()-t0:.0f}s]", flush=True)
    elif job == 'accel2':
        print("## acceleration test: W = 11..16 fixed, U -> large")
        for W in (11, 12, 13, 14, 16):
            for U in (5 * W, 8 * W, 12 * W):
                t0 = time.time()
                st, M = death(W, U, cap=1500)
                print(f"  ({W},{U}): {st} M0<={M} ratio={M/U:.2f} "
                      f"[{time.time()-t0:.0f}s]", flush=True)
    elif job == 'one':
        W, U = int(sys.argv[2]), int(sys.argv[3])
        st, M = death(W, U, cap=3000)
        print(f"  ({W},{U}): {st} M0<={M}", flush=True)
