"""
A_batch.py

CLAIM TESTED: run A_sat_cover on a whole list of (L, world, mode) instances, with a wall
clock budget per instance, and record the verdicts in a JSON log so nothing is lost.

Motivation (the theorem this is building towards):
  A covering system with all moduli in E and lcm = L0 forces B_E(L0) > 1.  A_candidate_L.py
  enumerates EVERY L <= X with B_E(L) > 1 -- there are only 29 of them for X = 400000.
  Deciding all of them therefore decides "is there a covering system with moduli in E and
  lcm <= X".  Each individual UNSAT is already a theorem:
     "no covering system with distinct moduli in E has lcm dividing L".

Usage:  python3 A_batch.py <outfile.json> <per-instance timeout> <world> <mode> L1 L2 ...
CONCLUSION: written to the JSON log and printed.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_sat_cover import run

CERTS = "/home/user/erdos/erdos-273/attempts/route-A-satsearch/certs"

if __name__ == "__main__":
    out_fn, tmo, world, mode = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
    Ls = [int(x) for x in sys.argv[5:]]
    log = []
    if os.path.exists(out_fn):
        log = json.load(open(out_fn))
    done = {(r["L"], r["world"], r["mode"]) for r in log
            if r["verdict"] not in ("TIMEOUT",)}
    for L in Ls:
        if (L, world, mode) in done:
            print(f"skip L={L} (already decided)", flush=True)
            continue
        t = time.time()
        try:
            r = run(L, world, mode, None, None, "weak", 6, 0, "cadical153", tmo,
                    CERTS, tag="_batch")
        except MemoryError:
            r = dict(L=L, world=world, mode=mode, verdict="OOM", solve_time=0.0,
                     build_time=0.0, nmods=0, budget=0.0)
        r.pop("classes", None)
        r["wall"] = time.time() - t
        log.append(r)
        json.dump(log, open(out_fn, "w"), indent=1)
        print(f"### L={L} {world}/{mode}: {r['verdict']}  build={r.get('build_time',0):.1f}s "
              f"solve={r.get('solve_time',0):.1f}s  #mods={r.get('nmods')} "
              f"budget={r.get('budget'):.5f}", flush=True)
    print("\n=== summary ===")
    for r in log:
        print(f"{r['L']:>10} {r['world']}/{r['mode']:<8} {r['verdict']:<15} "
              f"#mods={r.get('nmods')} budget={r.get('budget',0):.5f} "
              f"solve={r.get('solve_time',0):.1f}s")
