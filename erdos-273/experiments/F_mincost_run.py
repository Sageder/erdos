"""
F_mincost_run.py -- driver for F_mincost (Route F, Erdos 273).

CLAIM TESTED: for each L in a list and each world W in {ALL, E, H}, compute the
EXACT minimum of sum_i 1/n_i over covering systems of Z with pairwise distinct
moduli n_i > 1, n_i | L, n_i in W.  Equivalently X(L,W) = min waste, and
min sum 1/n_i = 1 + X(L,W)/L.

Every returned system is re-verified INDEPENDENTLY here (exhaustive sweep over
0..L-1 in exact integer arithmetic, distinctness check, world-membership check).

CONCLUSION: table printed; recorded in attempts/route-F-efficiency/FINDINGS.md.
"""
import subprocess, sys, os, json
from fractions import Fraction
from F_mincost import divisors, WORLDS, verify

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "F_mincost")


def run(L, world="ALL", wcap=None, nodecap=0, timeout=1500):
    ds = [d for d in divisors(L) if d > 1 and WORLDS[world](d)]
    if not ds:
        return {"L": L, "world": world, "status": "NO_MODULI"}
    budget = sum(Fraction(1, d) for d in ds)
    if budget < 1:
        return {"L": L, "world": world, "status": "BUDGET_INFEASIBLE",
                "budget": str(budget), "budget_f": float(budget), "nmod": len(ds)}
    if wcap is None:
        wcap = L  # trivial cap
    cmd = [BIN, str(L), str(wcap), str(nodecap)] + [str(d) for d in ds]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"L": L, "world": world, "status": "TIMEOUT", "nmod": len(ds),
                "budget_f": float(budget)}
    out = p.stdout.strip().splitlines()
    last = out[-1] if out else ""
    rec = {"L": L, "world": world, "nmod": len(ds), "budget_f": float(budget)}
    if last.startswith("X="):
        X = int(last.split()[0][2:])
        sysstr = last.split("system=")[1].split()
        system = []
        for tok in sysstr:
            a, n = tok.split("/")
            system.append((int(n), int(a)))
        chk = verify(L, system, world, L)
        assert chk["distinct"] and chk["all>1"] and chk["divides_L"] \
            and chk["in_world"] and chk["covers_all_residues_mod_L"], (L, world, chk)
        assert chk["waste"] == X, (chk, X)
        rec.update({"status": "OK", "X": X,
                    "mu": str(Fraction(L + X, L)), "mu_f": (L + X) / L,
                    "system": sorted(system), "verified": True})
    elif last.startswith("ABORT"):
        rec.update({"status": "ABORT", "detail": last})
    elif last.startswith("BUDGET"):
        rec.update({"status": "BUDGET_INFEASIBLE"})
    elif last.startswith("NOSOL"):
        rec.update({"status": "NO_COVERING_UPTO_WCAP", "wcap": wcap})
    else:
        rec.update({"status": "?", "detail": last})
    return rec


def main():
    Ls = [int(x) for x in sys.argv[1].split(",")]
    world = sys.argv[2] if len(sys.argv) > 2 else "ALL"
    wcap = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] else None
    nodecap = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    outfile = sys.argv[5] if len(sys.argv) > 5 else None
    res = []
    for L in Ls:
        r = run(L, world, wcap, nodecap)
        res.append(r)
        if r["status"] == "OK":
            print(f"L={L:<9} {world:3}  #mod={r['nmod']:<4} budget={r['budget_f']:.4f}  "
                  f"X={r['X']:<5} mu={r['mu']} = {r['mu_f']:.8f}", flush=True)
            print(f"     system: " +
                  ", ".join(f"{a} mod {n}" for n, a in r["system"]), flush=True)
        else:
            print(f"L={L:<9} {world:3}  #mod={r.get('nmod','-'):<4} "
                  f"budget={r.get('budget_f',0):.4f}  {r['status']} {r.get('detail','')}",
                  flush=True)
    if outfile:
        with open(outfile, "w") as f:
            json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
