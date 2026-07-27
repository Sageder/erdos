"""probe_bg.py — larger CP-SAT probes run in background; prints results as they finish."""
import time
import numpy as np
from satprobe import probe_contiguous, probe_separated

def run(tag, fn, *a, save=None):
    t0 = time.time()
    st, data = fn(*a)
    print(f"{tag}: {st} ({time.time()-t0:.1f}s)"
          + (f" forced {data}" if st == "UNSAT-forced" else ""), flush=True)
    if st == "SAT" and save:
        np.save(save, np.array(data))
        print(f"  saved -> {save}", flush=True)
    return st

if __name__ == "__main__":
    st = run("A base4 N=160", probe_contiguous, 4, 160, 600)
    if st == "SAT":
        st = run("A base4 N=255", probe_contiguous, 4, 255, 900,
                 save="sat_base4_255.npy")
    if st == "SAT":
        st = run("A base4 N=350", probe_contiguous, 4, 350, 1800,
                 save="sat_base4_350.npy")
    if st == "SAT":
        st = run("A base4 N=511", probe_contiguous, 4, 511, 3600,
                 save="sat_base4_511.npy")
    run("B sep2 dyadic N=255", probe_separated, 2, 255, 1800,
        save="sat_sep2_255.npy")
