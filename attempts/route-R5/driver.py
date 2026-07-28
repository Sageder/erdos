"""Route R5 production driver: segmented S_k sieve, checkpointed and resumable.

Usage:
  python3 driver.py --start 1 --end 100000000 --ks 2,3,4,5,6 \
      --block 2000000 --workers 4 --tag run1

Each block [L, R) is computed independently (deterministic) and written
atomically to data/blocks/<tag>_b{idx:06d}.json; existing files are skipped, so
the run is resumable.  After all blocks complete, per-k sorted member lists are
merged to data/S{k}_<tag>.txt and a summary to data/summary_<tag>.json.

Exactness: see sievelib.py header.  n <= 200 (when start == 1) is handled by
the direct digit criterion (in_Sk_digit) because the large-prime rejection in
step (a) needs n > 2k^2.
"""

import argparse
import json
import math
import os
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, "/home/user/erdos/attempts/route-R5")
sys.path.insert(0, "/home/user/erdos/experiments")

import numpy as np

from sievelib import block_members, primes_upto

DATA = "/home/user/erdos/attempts/route-R5/data"
SMALL_N_CUTOFF = 200

_G = {}


def _init(ps, pd):
    _G["ps"] = ps
    _G["pd"] = pd


def _do_block(args):
    idx, L, R, ks, tag = args
    path = f"{DATA}/blocks/{tag}_b{idx:06d}.json"
    if os.path.exists(path):
        return idx, None
    t0 = time.time()
    ps, pd = _G["ps"], _G["pd"]
    mhi = R - 1 + max(ks)
    ps_b = ps[ps <= math.isqrt(mhi) + 1]
    pd_b = pd[pd <= math.isqrt(2 * (R - 1))]
    res, surv = block_members(L, R, ks, ps_b, pd_b, return_survivors=True)
    obj = {
        "L": L, "R": R, "ks": ks,
        "surv": {str(k): int(surv[k]) for k in ks},
        "members": {str(k): res[k].tolist() for k in ks},
        "secs": round(time.time() - t0, 2),
    }
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, path)
    return idx, obj["secs"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)  # exclusive
    ap.add_argument("--ks", type=str, default="2,3,4,5,6")
    ap.add_argument("--block", type=int, default=2000000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--tag", type=str, required=True)
    a = ap.parse_args()
    ks = sorted(int(x) for x in a.ks.split(","))
    kmax = max(ks)

    os.makedirs(f"{DATA}/blocks", exist_ok=True)

    small = {k: [] for k in ks}
    lo = a.start
    if a.start <= SMALL_N_CUTOFF:
        from erdos727 import in_Sk_digit
        for n in range(a.start, min(SMALL_N_CUTOFF, a.end - 1) + 1):
            for k in ks:
                if in_Sk_digit(n, k):
                    small[k].append(n)
        lo = SMALL_N_CUTOFF + 1

    ps = primes_upto(math.isqrt(a.end - 1 + kmax) + 1)
    pd = primes_upto(math.isqrt(2 * (a.end - 1)) + 1)

    tasks = []
    idx = 0
    L = lo
    while L < a.end:
        R = min(L + a.block, a.end)
        tasks.append((idx, L, R, ks, a.tag))
        idx += 1
        L = R
    todo = [t for t in tasks if not os.path.exists(f"{DATA}/blocks/{a.tag}_b{t[0]:06d}.json")]
    print(f"[driver] {len(tasks)} blocks total, {len(todo)} to compute", flush=True)

    t0 = time.time()
    with Pool(a.workers, initializer=_init, initargs=(ps, pd)) as pool:
        done = 0
        for idx_done, secs in pool.imap_unordered(_do_block, todo, chunksize=1):
            done += 1
            if done % 5 == 0 or done == len(todo):
                el = time.time() - t0
                print(f"[driver] {done}/{len(todo)} blocks, {el:.0f}s elapsed, "
                      f"eta {el/done*(len(todo)-done):.0f}s", flush=True)

    # merge
    summary = {"start": a.start, "end": a.end, "ks": ks, "counts": {},
               "surv_totals": {}, "blocks": len(tasks)}
    members = {k: list(small[k]) for k in ks}
    surv_tot = {k: 0 for k in ks}
    for t in tasks:
        with open(f"{DATA}/blocks/{a.tag}_b{t[0]:06d}.json") as f:
            obj = json.load(f)
        assert obj["L"] == t[1] and obj["R"] == t[2], "block file mismatch"
        for k in ks:
            members[k].extend(obj["members"][str(k)])
            surv_tot[k] += obj["surv"][str(k)]
    for k in ks:
        arr = np.array(sorted(members[k]), dtype=np.int64)
        assert len(np.unique(arr)) == len(arr)
        np.savetxt(f"{DATA}/S{k}_{a.tag}.txt", arr, fmt="%d")
        summary["counts"][str(k)] = int(len(arr))
        summary["surv_totals"][str(k)] = int(surv_tot[k])
        print(f"[driver] |S_{k} cap [{a.start},{a.end})| = {len(arr)} "
              f"(step-a survivors {surv_tot[k]})", flush=True)
    with open(f"{DATA}/summary_{a.tag}.json", "w") as f:
        json.dump(summary, f, indent=1)
    print(f"[driver] done in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
