"""ladder.py -- the ACCELERATION direction: pairs (W,U) at a FIXED ratio U/W = rho,
with W growing.  rho = 3 is the P-diagonal (all dead, W = 10..40).  Acceleration
needs rho large; the forced-inversion density inside the top block is ~ 1/(4 rho),
so large rho is exactly where the pair obstruction is weakest.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def death(W, U, mults=(3, 4, 5), cap=2400):
    M = 3 * U - 2
    for m in mults:
        M = 3 * U - 2 if m == 3 else m * U
        t0 = time.time()
        S = wsys.Sys((W, U), M)
        v, o = wsys.solve_lazy(S, time_cap=cap)
        if v == 'GEOM_DEAD':
            v = 'UNSAT'
        print(f"     N({W},{U},{M}) {v} [{time.time()-t0:.0f}s]", flush=True)
        if v == 'UNSAT':
            return 'DEAD', M
        if v == 'TIME_CAP':
            return 'TIMEOUT', M
    return 'ALIVE', M


if __name__ == '__main__':
    rho = float(sys.argv[1])
    Ws = [int(x) for x in sys.argv[2].split(',')]
    print(f"## ratio U/W = {rho}", flush=True)
    for W in Ws:
        U = int(round(rho * W))
        t0 = time.time()
        st, M = death(W, U)
        print(f"  ({W},{U}) rho={U/W:.2f}: {st} M0<={M} [{time.time()-t0:.0f}s]",
              flush=True)
