"""tables.py — exhaustive avoider COUNTS per (class, C, N) for the report tables.

Runs fast2 (count mode, no cap, wall timeout per run); appends JSON lines to
results/counts.jsonl.  Skips (cls,C,N) already present.  Stops increasing N for a
(cls,C) once a run times out or the count exceeds COUNT_STOP (tables become
uninformative), or once count==0 twice in a row past the extinction point.
"""

import json
import os
import subprocess
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results", "counts.jsonl")
FAST2 = os.path.join(HERE, "fast2")
FASTSEQ = os.path.join(HERE, "fastseq")

T_RUN = 600
COUNT_STOP = 2_000_000_000


def have():
    d = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            r = json.loads(line)
            d.add((r["cls"], r["C"], r["N"]))
    return d


def run_count(N, cls, C, timeout):
    if cls == "S":
        cmd = [FASTSEQ, str(N), str(C.numerator), str(C.denominator), "c", "0", "0"]
    else:
        cmd = [FAST2, str(N), cls, str(C.numerator), str(C.denominator), "c", "0", "0"]
    t0 = time.time()
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return None
    d = dict(kv.split("=", 1) for kv in
             [l for l in out.splitlines() if l.startswith("RESULT")][0].split()[1:])
    return {"count": int(d["count"]), "nodes": int(d["nodes"]), "secs": time.time() - t0}


def table(cls, C, nmax):
    done = have()
    Cs = f"{C.numerator}/{C.denominator}"
    zeros = 0
    for N in range(4, nmax + 1):
        if (cls, Cs, N) in done:
            continue
        r = run_count(N, cls, C, T_RUN)
        if r is None:
            print(f"[{cls} {Cs}] N={N}: count timeout — table stops", flush=True)
            return
        with open(OUT, "a") as f:
            f.write(json.dumps({"cls": cls, "C": Cs, "N": N, **r}) + "\n")
        print(f"[{cls} {Cs}] N={N}: count={r['count']} ({r['secs']:.1f}s)", flush=True)
        if r["count"] == 0:
            zeros += 1
            if zeros >= 3:
                return
        else:
            zeros = 0
        if r["count"] > COUNT_STOP:
            return


if __name__ == "__main__":
    jobs = []
    for spec in sys.argv[1:]:
        cls, cstr, nmax = spec.split(":")
        jobs.append((cls, Fraction(cstr), int(nmax)))
    for cls, C, nmax in jobs:
        table(cls, C, nmax)
