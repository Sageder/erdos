"""alpha_wall.py — locate alpha*(N) = min alpha with a phi_alpha-bounded avoider of [1..N],
phi_alpha(v) = ceil(alpha v log2(2v)).  Compare with the linear wall C*(N) (Remark 17).

Sound: UNSAT from the lazy-transitivity CEGAR is UNSAT for the full system; SAT models
are re-verified with the trusted checker.
"""
import sys, time, math
sys.path.insert(0, '/home/user/erdos/attempts/route-R20-vlogv')
from profile_sat import solve_profile, vlogv, verify

ALPHAS = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.75, 1.00]

if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1].split(",")]
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
    for N in Ns:
        found = None
        for a in ALPHAS:
            t0 = time.time()
            res, perm, rounds = solve_profile(N, vlogv(a))
            dt = time.time() - t0
            if res == "SAT":
                verify(perm, vlogv(a), N)
            print(f"  N={N} alpha={a}: {res} ({dt:.0f}s, {rounds} rounds)", flush=True)
            if res == "SAT":
                found = a
                with open(f"/home/user/erdos/attempts/route-R20-vlogv/wit_N{N}_a{a}.txt", "w") as f:
                    f.write(repr(perm))
                break
            if res == "UNKNOWN" or dt > tl:
                break
        print(f"ALPHA-WALL N={N}: alpha*(N) = {found}", flush=True)
