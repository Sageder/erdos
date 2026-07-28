import sys, time, itertools
from reach import reach, sat_prefix
CAP=96
print("Reach(s) for K=4, cap=%d  ('%d' means >= cap)"%(CAP,CAP))
for L in (2,3,4):
    res={}
    for s in itertools.permutations(range(1,7), L):
        if max(s) > 6: continue
        r = reach(list(s), cap=CAP)
        res[s]=r
    fin = {s:r for s,r in res.items() if r<CAP}
    print(f"len={L}: {len(res)} prefixes from [1..6], {len(fin)} have Reach<{CAP}")
    from collections import Counter
    print("   Reach distribution:", sorted(Counter(res.values()).items()))
    ex = sorted(fin.items(), key=lambda kv:kv[1])[:8]
    print("   smallest Reach:", ex, flush=True)
