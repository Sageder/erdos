"""make_thresholds.py — condense results/frontier.jsonl into results/thresholds.tsv.
Machine-generated data table (no prose): per (class, C, rounding): max N with a
verified avoider, min N proven extinct, largest N checked, and monotonicity flag
(class A/D/S extinction is monotone in N by restriction/prefix; B/C checked per-N).
"""

import json
import os
from collections import defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))

by = defaultdict(list)
for line in open(os.path.join(HERE, "results", "frontier.jsonl")):
    r = json.loads(line)
    by[(r["cls"], r["C"], r.get("round", "f"))].append(r)

rows = []
for (cls, C, rnd), rs in sorted(by.items(), key=lambda kv: (kv[0][0], Fraction(kv[0][1]), kv[0][2])):
    exi = [r["N"] for r in rs if r["verdict"] == "EXISTS"]
    ext = [r["N"] for r in rs if r["verdict"] == "EXTINCT"]
    unk = [r["N"] for r in rs if r["verdict"] == "UNKNOWN"]
    mono = "yes" if cls in ("A", "D", "S") else "per-N"
    rows.append((cls, C, rnd, max(exi) if exi else "-", min(ext) if ext else "-",
                 max(ext) if ext else "-", ",".join(map(str, unk)) if unk else "-", mono))

out = os.path.join(HERE, "results", "thresholds.tsv")
with open(out, "w") as f:
    f.write("cls\tC\trounding\tmax_N_exists\tmin_N_extinct\tmax_N_extinct_checked\tunknown_N\textinction_monotone\n")
    for r in rows:
        f.write("\t".join(map(str, r)) + "\n")
print(open(out).read())
