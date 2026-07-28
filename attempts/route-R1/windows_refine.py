"""windows_refine.py — notch-edge refinement + V1-memory grid + 5-cut attempt prep.
Run AFTER windows.log main sweep. Appends to windows2.log."""
from satsearch import BlockOrderSAT, verify_witness
import time

def cutsat(cuts):
    blocks = []
    lo = 1
    for c in cuts:
        blocks.append((lo, c + 1)); lo = c + 1
    bs = BlockOrderSAT(blocks)
    t0 = time.time()
    res, wit = bs.solve(eager_transitivity_maxsize=10**9, verbose=False)
    dt = time.time() - t0
    if res == 'SAT':
        verify_witness(blocks, wit, cuts[-1])
    print(f"cuts {cuts} {res} ({dt:.0f}s)", flush=True)
    return res

print("--- notch edges W(4,16): bracket the 60-notch")
for v3 in (54, 56, 58, 62, 64, 66, 68):
    cutsat([4, 16, v3])
print("--- notch edges W(6,20): bracket 66-86 notch")
for v3 in (60, 62, 64, 90, 94):
    cutsat([6, 20, v3])
print("--- W(8,26) extra points")
for v3 in (76, 78, 125, 135, 145, 220):
    cutsat([8, 26, v3])
print("--- V1-memory: {V1,20,100}")
for v1 in (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14):
    cutsat([v1, 20, 100])
print("--- V1-memory: {V1,16,70}")
for v1 in (2, 4, 6, 8, 10, 12):
    cutsat([v1, 16, 70])
print("REFINE DONE", flush=True)
