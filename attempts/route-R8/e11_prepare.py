"""e11_prepare.py — solve and save verified two-sided windows for folding experiments."""
import sys
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import e4_zjoint  # dyadic Z macro
import e10_zb3    # ternary Z macro


def assemble(mod, taus):
    slots = sorted((mod.slot_of_block(m), m) for m in taus)
    seq = []
    center = None
    for s_, m in slots:
        if s_ == 0:
            # position 0 sits inside this block: center = index of value 0
            center = len(seq) + taus[m].index(0)
        seq.extend(taus[m])
    return seq, center


out = {}
taus5 = e4_zjoint.solve_joint(6, k=5, verbose=False)
seq5, c5 = assemble(e4_zjoint, taus5)
out["Z_dyadic_5free_M6"] = {"window": seq5, "center": c5, "k": 5}

taus4 = e10_zb3.solve_joint(3, k=4, verbose=False)
seq4, c4 = assemble(e10_zb3, taus4)
out["Z_ternary_4free_M3"] = {"window": seq4, "center": c4, "k": 4}

with open(os.path.join(HERE, "windows.json"), "w") as f:
    json.dump(out, f)
print("saved windows.json:", {k: len(v["window"]) for k, v in out.items()})
