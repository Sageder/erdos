"""
F_H_cheap.py -- Route F, Erdos 273, task (c): how CHEAP can an H-covering be?

CLAIM TESTED: for L in a candidate list, compute (or bound)
    mu_H(L) = min { sum 1/m : H-covering of Z, distinct moduli m | L, 2m+1 prime }
    = 1 + X/L,
and compare with the total available budget B_H(L) = sum_{m|L, m in H} 1/m.
The gap B_H(L) - mu_H(L) is exactly the SLACK: an E-covering needs TWO DISJOINT
H-coverings, hence needs B_H(L) >= mu_1 + mu_2 > 2.

Method: binary search on the waste W (feasibility of "waste <= W" is monotone
in W), each probe an exact exhaustive DFS (F_mincost, single-target mode).
Node caps give UNKNOWN rather than a wrong answer.

CONCLUSION: printed; see FINDINGS.md.
"""
import subprocess, sys, os, time
from fractions import Fraction
from F_mincost import divisors, WORLDS, verify

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "F_mincost")


def probe(L, mods, W, nodecap, timeout=900):
    """Exact decision: is there a covering with moduli in `mods` and waste <= W?"""
    cmd = [BIN, str(L), str(-W), str(nodecap)] + [str(d) for d in mods]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, None
    last = p.stdout.strip().splitlines()[-1]
    if last.startswith("X="):
        system = []
        for tok in last.split("system=")[1].split():
            a, n = tok.split("/")
            system.append((int(n), int(a)))
        return True, sorted(system)
    if last.startswith("ABORT"):
        return None, None
    return False, None


def analyse(L, world="H", nodecap=60000000, verbose=True):
    mods = [d for d in divisors(L) if d > 1 and WORLDS[world](d)]
    B = sum(Fraction(1, d) for d in mods)
    tot = sum(L // d for d in mods)
    if tot < L:
        return {"L": L, "status": "BUDGET<=1", "B": float(B), "nmod": len(mods)}
    hi = tot - L                      # max conceivable waste
    lo = 2                            # proved lower bound (see FINDINGS L3)
    best_sys = None
    r, s = probe(L, mods, hi, nodecap)
    if r is None:
        return {"L": L, "status": "UNKNOWN(cap)", "B": float(B), "nmod": len(mods)}
    if r is False:
        return {"L": L, "status": "NO_COVER", "B": float(B), "nmod": len(mods)}
    best_sys, best_W = s, hi
    while lo < hi:
        mid = (lo + hi) // 2
        r, s = probe(L, mods, mid, nodecap)
        if r is None:
            return {"L": L, "status": f"UNKNOWN(cap) bounds[{lo},{hi}]",
                    "B": float(B), "nmod": len(mods), "ub_W": best_W,
                    "ub_mu": float(Fraction(L + best_W, L)), "system": best_sys}
        if r:
            hi = mid
            best_sys, best_W = s, mid
        else:
            lo = mid + 1
    X = hi
    chk = verify(L, best_sys, world, L)
    assert chk["distinct"] and chk["in_world"] and chk["covers_all_residues_mod_L"] \
        and chk["divides_L"] and chk["waste"] == X, (L, chk, X)
    return {"L": L, "status": "OK", "X": X, "mu": str(Fraction(L + X, L)),
            "mu_f": (L + X) / L, "B": float(B), "nmod": len(mods),
            "k": len(best_sys), "system": best_sys}


def main():
    world = sys.argv[1] if len(sys.argv) > 1 else "H"
    Ls = [int(t) for t in sys.argv[2].split(",")]
    nodecap = int(sys.argv[3]) if len(sys.argv) > 3 else 60000000
    for L in Ls:
        t0 = time.time()
        r = analyse(L, world, nodecap)
        dt = time.time() - t0
        if r["status"] == "OK":
            print(f"L={L:<9}{world} #mod={r['nmod']:<3} B={r['B']:.5f}  "
                  f"mu={r['mu']}={r['mu_f']:.6f}  k={r['k']}  "
                  f"slack B-mu={r['B']-r['mu_f']:.5f}  [{dt:.0f}s]", flush=True)
            print("     " + ", ".join(f"{a} mod {n}" for n, a in r["system"]),
                  flush=True)
        else:
            print(f"L={L:<9}{world} #mod={r.get('nmod','-'):<3} "
                  f"B={r.get('B',0):.5f} {r['status']} "
                  f"ub_mu={r.get('ub_mu','-')} [{dt:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
