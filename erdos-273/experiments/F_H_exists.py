"""
F_H_exists.py -- Route F, Erdos 273, task (c).

CLAIM TESTED: for every L in an increasing range with reciprocal budget
    B_W(L) = sum_{d | L, d>1, d in W} 1/d  >  1     (W in {H, E}),
decide EXACTLY whether a covering system of Z with pairwise distinct moduli
dividing L and lying in W exists, and if so with what minimal cost
    mu = 1 + X/L,   X = min waste.
Because sum_i L/n_i <= L * B_W(L), the waste of ANY such system is at most
floor(L*B_W(L)) - L, so the iterative deepening is finite and the search is
exhaustive: "no solution up to that cap" == "no covering system at all with
moduli dividing L inside W".  This is a THEOREM ABOUT THAT L ONLY.

CONCLUSION: printed; recorded in attempts/route-F-efficiency/FINDINGS.md.
"""
import subprocess, sys, os, time
from fractions import Fraction
from F_mincost import divisors, WORLDS, verify

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "F_mincost")


def test(L, world, nodecap=0, timeout=600):
    ds = [d for d in divisors(L) if d > 1 and WORLDS[world](d)]
    B = sum(Fraction(1, d) for d in ds)
    if B <= 1:
        return ("BUDGET<=1", B, ds, None, None)
    wcap = int(sum(L // d for d in ds)) - L      # exact max possible waste
    cmd = [BIN, str(L), str(wcap), str(nodecap)] + [str(d) for d in ds]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return ("TIMEOUT", B, ds, None, None)
    last = p.stdout.strip().splitlines()[-1]
    if last.startswith("X="):
        X = int(last.split()[0][2:])
        system = []
        for tok in last.split("system=")[1].split():
            a, n = tok.split("/")
            system.append((int(n), int(a)))
        chk = verify(L, system, world, L)
        assert chk["distinct"] and chk["all>1"] and chk["divides_L"] \
            and chk["in_world"] and chk["covers_all_residues_mod_L"] \
            and chk["waste"] == X, (L, chk)
        return ("COVER", B, ds, X, sorted(system))
    if last.startswith("NOSOL"):
        return ("NO_COVER", B, ds, None, None)
    return (last.split()[0], B, ds, None, None)


def main():
    world = sys.argv[1] if len(sys.argv) > 1 else "H"
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    nodecap = int(sys.argv[4]) if len(sys.argv) > 4 else 20000000
    t0 = time.time()
    nfeas = 0
    for L in range(lo, hi + 1):
        st, B, ds, X, system = test(L, world, nodecap)
        if st == "BUDGET<=1":
            continue
        nfeas += 1
        if st == "COVER":
            mu = Fraction(L + X, L)
            print(f"*** L={L:<8} {world}  B={float(B):.4f} #mod={len(ds)}  "
                  f"COVERING EXISTS  X={X} mu={mu}={float(mu):.6f}", flush=True)
            print("      " + ", ".join(f"{a} mod {n}" for n, a in system), flush=True)
        else:
            print(f"L={L:<8} {world}  B={float(B):.4f} #mod={len(ds):<3} {st}",
                  flush=True)
    print(f"# {nfeas} budget-feasible L in [{lo},{hi}] for world {world}; "
          f"{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
