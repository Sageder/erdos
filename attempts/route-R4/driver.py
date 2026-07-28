"""driver.py — Route R4 frontier driver.

For each stream (class, C) pushes N upward:
  1. existence heuristics: fast2 order=1 (descending), then order=2 seeds 1,2, node cap CAPH;
  2. if no avoider found: exhaustive run (fast2 order=0, no node cap) under wall timeout;
     count=0 & exhaustive=1  => EXTINCT at N (recorded);
     wall timeout            => UNKNOWN at N, stream stops.
After first extinction, continues CONFIRM_EXTRA more values of N (exhaustive) to test
persistence (classes B and C are not a priori monotone in N; A and D are, by restriction).

All runs are appended as JSON lines to results/frontier.jsonl (restartable; done work
skipped).  Every found avoider is appended to avoiders/<cls>_<num>_<den>.txt.

Deterministic: fixed heuristic order, fixed seeds (1,2).
"""

import json
import os
import subprocess
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results", "frontier.jsonl")
AVD = os.path.join(HERE, "avoiders")
FAST2 = os.path.join(HERE, "fast2")

CAPH = 200_000_000          # node cap for heuristic existence runs
T_HEUR = 60                 # wall seconds per heuristic run (safety)
T_EX = 3600                 # wall seconds for exhaustive run
CONFIRM_EXTRA = 6           # extra N values after first extinction
NMAX = 512                  # stop pushing N here even if avoiders persist


def log(rec):
    with open(RES, "a") as f:
        f.write(json.dumps(rec) + "\n")


def load_done():
    done = {}
    if os.path.exists(RES):
        with open(RES) as f:
            for line in f:
                r = json.loads(line)
                key = (r["cls"], r["C"], r["N"])
                # keep the most informative record: found > extinct > unknown
                done.setdefault(key, []).append(r)
    return done


FASTSEQ = os.path.join(HERE, "fastseq")


def run_fast2(N, cls, C, mode, cap, maxprint, order, seed, timeout):
    if cls == "S":       # class Bp: injective sequences, engine fastseq
        cmd = [FASTSEQ, str(N), str(C.numerator), str(C.denominator), mode,
               str(cap), str(maxprint), str(order), str(seed)]
    else:
        cmd = [FAST2, str(N), cls, str(C.numerator), str(C.denominator), mode,
               str(cap), str(maxprint), str(order), str(seed)]
    t0 = time.time()
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return {"status": "walltimeout", "secs": time.time() - t0, "cmd": " ".join(cmd)}
    last = [l for l in out.splitlines() if l.startswith("RESULT")]
    d = dict(kv.split("=", 1) for kv in last[0].split()[1:])
    r = {"status": "done", "count": int(d["count"]), "nodes": int(d["nodes"]),
         "exhaustive": int(d["exhaustive"]), "secs": time.time() - t0,
         "cmd": " ".join(cmd)}
    if "example" in d:
        r["example"] = [int(x) for x in d["example"].split(",")]
    return r


def save_avoider(cls, C, N, perm, how):
    name = f"seq_B_{C.numerator}_{C.denominator}.txt" if cls == "S" else \
        f"{cls}_{C.numerator}_{C.denominator}.txt"
    fn = os.path.join(AVD, name)
    with open(fn, "a") as f:
        f.write(f"N={N} how={how} perm=" + ",".join(map(str, perm)) + "\n")


def stream(cls, C, n_start=4):
    Cs = f"{C.numerator}/{C.denominator}"
    extinct_run = 0
    N = n_start
    while N <= NMAX:
        found = None
        verdict = None
        # 1. heuristics (skip if we're confirming extinction — go straight to exhaustive)
        if extinct_run == 0:
            for order, seed in ((1, 1), (2, 1), (2, 2)):
                r = run_fast2(N, cls, C, "e", CAPH, 0, order, seed, T_HEUR)
                if r["status"] == "done" and r.get("example"):
                    found = (r, order, seed)
                    break
        if found:
            r, order, seed = found
            log({"cls": cls, "C": Cs, "N": N, "phase": "heur", "order": order,
                 "seed": seed, **{k: v for k, v in r.items() if k != "example"},
                 "verdict": "EXISTS"})
            save_avoider(cls, C, N, r["example"], f"heur-ord{order}-seed{seed}")
            verdict = "EXISTS"
        else:
            r = run_fast2(N, cls, C, "e", 0, 0, 0, 1, T_EX)
            if r["status"] == "walltimeout":
                log({"cls": cls, "C": Cs, "N": N, "phase": "exhaust",
                     "status": "walltimeout", "secs": r["secs"], "verdict": "UNKNOWN"})
                print(f"[{cls} C={Cs}] N={N}: UNKNOWN (exhaustive walltimeout) — stream stops",
                      flush=True)
                return
            if r["count"] == 0 and r["exhaustive"] == 1:
                log({"cls": cls, "C": Cs, "N": N, "phase": "exhaust", **r,
                     "verdict": "EXTINCT"})
                print(f"[{cls} C={Cs}] N={N}: EXTINCT ({r['nodes']} nodes, "
                      f"{r['secs']:.1f}s)", flush=True)
                verdict = "EXTINCT"
            elif r.get("example"):
                log({"cls": cls, "C": Cs, "N": N, "phase": "exhaust",
                     **{k: v for k, v in r.items() if k != "example"},
                     "verdict": "EXISTS"})
                save_avoider(cls, C, N, r["example"], "exhaust-ord0")
                verdict = "EXISTS"
            else:
                log({"cls": cls, "C": Cs, "N": N, "phase": "exhaust", **r,
                     "verdict": "ODD"})
                print(f"[{cls} C={Cs}] N={N}: unexpected result {r}", flush=True)
                return
        if verdict == "EXTINCT":
            extinct_run += 1
            if extinct_run > CONFIRM_EXTRA:
                print(f"[{cls} C={Cs}] extinction confirmed through N={N}; stream done",
                      flush=True)
                return
        else:
            if extinct_run > 0:
                print(f"[{cls} C={Cs}] N={N}: REVIVAL after extinction!!", flush=True)
            extinct_run = 0
        N += 1
    print(f"[{cls} C={Cs}] reached NMAX={NMAX} with avoiders alive", flush=True)


if __name__ == "__main__":
    cls = sys.argv[1]
    C = Fraction(sys.argv[2])
    n_start = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    stream(cls, C, n_start)
