"""verify_R2.py — INDEPENDENT re-implementation and verification of route R2's
"Construction A" (= CORE.md Theorem 21, [DEGS77](b) confirmation).

Written from the PROSE spec only (blocks B_m = [4^m, 4^{m+1}), van der Corput
order inside, reversed for odd m); no code reused from route-R2.

Checks:
  V0  cross-validate my fast k-AP checker against experiments/apcheck.py
  V1  bijectivity: the length-(4^k - 1) prefix is a permutation of [1..4^k-1]
  V2  order type omega witness: value v and pos(v) lie in the same window
      [4^m, 4^{m+1}) -> pos(v) finite, every position filled (structural)
  V3  no monotone 5-AP on value-restrictions [1..N], N = 255,1023,4095,16383,65535
  V4  no monotone DESCENDING 3-AP
  V5  monotone 4-APs DO exist; smallest one reported
  V6  displacement profile max/min of pos(v)/v
Exact integer arithmetic throughout (numpy int64 only for index bookkeeping).
"""
import sys, time
import numpy as np

sys.path.insert(0, "/home/user/erdos/experiments")
import apcheck


# ---------- construction ----------
def vdc_key(u, width):
    """Bit-reversed value of u over `width` bits: sorting ascending by this key
    is exactly the van der Corput order (compare at least significant differing
    bit, 0 first)."""
    r = 0
    for i in range(width):
        r = (r << 1) | ((u >> i) & 1)
    return r


def construction_A_prefix(K):
    """Return the list of values at positions 1..4^K - 1 (blocks B_0..B_{K-1})."""
    seq = []
    for m in range(K):
        lo, hi = 4 ** m, 4 ** (m + 1)          # block B_m = [lo, hi)
        width = 2 * (m + 1)                    # hi-1 < 4^{m+1} = 2^{2(m+1)}
        blk = sorted(range(lo, hi), key=lambda u: vdc_key(u, width))
        if m % 2 == 1:
            blk.reverse()
        seq.extend(blk)
    return seq


# ---------- fast exact monotone k-AP checker (numpy, independent of R2) ----------
def monotone_kap_witness(perm, k):
    """perm: list, perm[i] = value at position i+1, values exactly 1..N.
    Returns a witness (x, d, orientation) or None. Exact integer arithmetic."""
    N = len(perm)
    pos = np.zeros(N + 1, dtype=np.int64)
    pos[np.array(perm, dtype=np.int64)] = np.arange(1, N + 1, dtype=np.int64)
    for d in range(1, (N - 1) // (k - 1) + 1):
        top = N - (k - 1) * d
        xs = np.arange(1, top + 1, dtype=np.int64)
        cols = [pos[xs + j * d] for j in range(k)]
        inc = np.ones(top, dtype=bool)
        dec = np.ones(top, dtype=bool)
        for j in range(k - 1):
            inc &= cols[j] < cols[j + 1]
            dec &= cols[j] > cols[j + 1]
        if inc.any():
            return (int(xs[np.argmax(inc)]), d, "inc")
        if dec.any():
            return (int(xs[np.argmax(dec)]), d, "dec")
    return None


def count_monotone_kap(perm, k):
    N = len(perm)
    pos = np.zeros(N + 1, dtype=np.int64)
    pos[np.array(perm, dtype=np.int64)] = np.arange(1, N + 1, dtype=np.int64)
    tot_inc = tot_dec = 0
    for d in range(1, (N - 1) // (k - 1) + 1):
        top = N - (k - 1) * d
        xs = np.arange(1, top + 1, dtype=np.int64)
        cols = [pos[xs + j * d] for j in range(k)]
        inc = np.ones(top, dtype=bool)
        dec = np.ones(top, dtype=bool)
        for j in range(k - 1):
            inc &= cols[j] < cols[j + 1]
            dec &= cols[j] > cols[j + 1]
        tot_inc += int(inc.sum())
        tot_dec += int(dec.sum())
    return tot_inc, tot_dec


def main():
    out = []
    P = out.append

    # ---- V0: cross-validate against the trusted checker ----
    import random
    rng = random.Random(20260728)
    bad = 0
    for _ in range(400):
        n = rng.randint(5, 11)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        for k in (3, 4, 5):
            mine = monotone_kap_witness(p, k) is not None
            gt = apcheck.has_monotone_kap_brute(p, k)
            fast = apcheck.has_monotone_kap_pos(p, k)
            if not (mine == gt == fast):
                bad += 1
                P(f"  MISMATCH {p} k={k}: mine={mine} brute={gt} pos={fast}")
    P(f"V0 cross-validation vs apcheck brute+pos: 400 random perms x k in 3,4,5 -> "
      f"{'OK, 0 mismatches' if bad == 0 else str(bad) + ' MISMATCHES'}")
    # also cross-validate on the construction itself at small size
    s63 = construction_A_prefix(3)
    for k in (3, 4, 5):
        mine = monotone_kap_witness(s63, k) is not None
        gt = apcheck.has_monotone_kap_pos(s63, k)
        assert mine == gt, (k, mine, gt)
    P("   cross-validated on the N=63 construction prefix too (k=3,4,5): OK")

    # ---- construction sanity ----
    s15 = construction_A_prefix(2)
    P(f"V-sanity first 15 values: {s15}")
    P("   (route R2 / CORE Thm 21 claim: 2,1,3 | 15,7,11,13,5,9,14,6,10,12,4,8)")

    for K in (4, 5, 6, 7, 8):
        N = 4 ** K - 1
        t0 = time.time()
        seq = construction_A_prefix(K)
        assert len(seq) == N
        # V1 bijectivity
        ok_bij = sorted(seq) == list(range(1, N + 1))
        # V2 window property (order type omega + displacement corridor)
        pos = [0] * (N + 1)
        for i, v in enumerate(seq):
            pos[v] = i + 1
        window_ok = True
        mx = (0.0, 0)
        mn = (1e9, 0)
        for v in range(1, N + 1):
            m = v.bit_length() - 1
            m //= 2                                  # 4^m <= v < 4^{m+1}
            if not (4 ** m <= v < 4 ** (m + 1) and 4 ** m <= pos[v] < 4 ** (m + 1)):
                window_ok = False
            r = pos[v] / v
            if r > mx[0]:
                mx = (r, v)
            if r < mn[0]:
                mn = (r, v)
        # V3 / V4 / V5
        w5 = monotone_kap_witness(seq, 5)
        w4 = monotone_kap_witness(seq, 4)
        # descending 3-AP: check separately
        pa = np.zeros(N + 1, dtype=np.int64)
        pa[np.array(seq, dtype=np.int64)] = np.arange(1, N + 1, dtype=np.int64)
        dec3 = False
        for d in range(1, (N - 1) // 2 + 1):
            top = N - 2 * d
            xs = np.arange(1, top + 1, dtype=np.int64)
            if ((pa[xs] > pa[xs + d]) & (pa[xs + d] > pa[xs + 2 * d])).any():
                dec3 = True
                break
        frac98 = sum(1 for v in range(1, N + 1) if pos[v] <= 1.125 * v) / N
        P(f"N = {N:6d}: bijective={ok_bij}  window[4^m,4^(m+1)) for v and pos(v)={window_ok}"
          f"  mono-5AP={w5}  mono-dec-3AP={dec3}  mono-4AP={w4}"
          f"  max pos/v={mx[0]:.6f} (v={mx[1]})  min pos/v={mn[0]:.6f} (v={mn[1]})"
          f"  frac(pos<=1.125v)={frac98:.4f}  [{time.time()-t0:.1f}s]")

    # ---- V5 census cross-check at N = 16383 (R2 claims 1,304,268 monotone 4-APs) ----
    seq = construction_A_prefix(7)
    ci, cd = count_monotone_kap(seq, 4)
    P(f"V5 census N=16383: monotone 4-APs increasing={ci} decreasing={cd} total={ci+cd}"
      f"   (R2 claim: 1304268 total, all ascending; S1=979436 + S2=324832)")
    ci3, cd3 = count_monotone_kap(seq, 3)
    P(f"   monotone 3-APs at N=16383: increasing={ci3} decreasing={cd3}")

    print("\n".join(out))
    with open("/home/user/erdos/attempts/consolidated/verify_R2.out", "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
