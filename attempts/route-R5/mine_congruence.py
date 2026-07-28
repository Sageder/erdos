"""Route R5 mining 2: congruence structure of S_k members.

Claims examined:
 G1. Distribution of n mod q for q in {small prime powers}: chi^2 against
     uniform; list forbidden classes (zero hits) and most enriched/depleted.
 G2. Distribution of (n+k) mod p^2 for small p: the digit condition at p is
     sensitive to low base-p digits of n+k, so structure is expected; quantify.
 G3. Distribution of n mod p for p in a band of medium primes: any bias?
All statistics are exact counts on the exact member lists; chi^2 values are
descriptive (no independence assumptions asserted).
"""

import sys
import numpy as np

DATA = "/home/user/erdos/attempts/route-R5/data"


def load(k, tags):
    parts = []
    for t in tags:
        try:
            parts.append(np.loadtxt(f"{DATA}/S{k}_{t}.txt", dtype=np.int64).reshape(-1))
        except OSError:
            pass
    return np.unique(np.concatenate(parts)) if parts else np.zeros(0, np.int64)


def chisq_uniform(counts):
    e = counts.sum() / len(counts)
    return float(((counts - e) ** 2 / e).sum()) if e > 0 else 0.0


def report_mod(arr, q, k, label, topn=6):
    cnt = np.bincount(arr % q, minlength=q)
    chi = chisq_uniform(cnt)
    dof = q - 1
    e = cnt.sum() / q
    order = np.argsort(cnt)
    forb = [int(r) for r in np.nonzero(cnt == 0)[0]]
    lowest = [(int(r), int(cnt[r]), round(cnt[r] / e, 3)) for r in order[:topn]]
    highest = [(int(r), int(cnt[r]), round(cnt[r] / e, 3)) for r in order[::-1][:topn]]
    print(f"  {label} mod {q}: chi2={chi:.1f} (dof={dof}, sqrt(2dof)={np.sqrt(2*dof):.0f}) "
          f"exp/class={e:.1f}")
    if forb and len(forb) <= 30:
        print(f"    FORBIDDEN classes: {forb}")
    elif forb:
        print(f"    {len(forb)} forbidden classes (first 30: {forb[:30]})")
    print(f"    most depleted: {lowest}")
    print(f"    most enriched: {highest}")


def main():
    tags = sys.argv[1:] or ["run1"]
    for k in [2, 3, 4]:
        arr = load(k, tags)
        arr = arr[arr > 1000]  # avoid small-n transients
        if len(arr) < 100:
            print(f"\n== k={k}: only {len(arr)} members, skipping ==")
            continue
        print(f"\n== k={k}: {len(arr)} members (n>1000) ==")
        print(" [G1] n mod small prime powers:")
        for q in [2, 4, 8, 16, 3, 9, 27, 5, 25, 7, 49, 11, 13]:
            report_mod(arr, q, k, "n")
        print(" [G2] (n+k) mod p^2:")
        for p in [2, 3, 5, 7]:
            report_mod(arr + k, p * p, k, f"n+{k}")
        print(" [G2b] (n+j) mod p for window slots j=1..k, p<=13:")
        for p in [2, 3, 5, 7, 11, 13]:
            for j in range(1, k + 1):
                cnt = np.bincount((arr + j) % p, minlength=p)
                e = cnt.sum() / p
                rat = np.round(cnt / e, 3)
                print(f"    p={p} slot j={j}: ratios {rat.tolist()}")
        print(" [G3] chi2/dof for n mod p, medium primes:")
        line = []
        for p in [17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]:
            cnt = np.bincount(arr % p, minlength=p)
            line.append((p, round(chisq_uniform(cnt) / (p - 1), 2)))
        print(f"    {line}  (1.0 = uniform expectation)")


if __name__ == "__main__":
    main()
