"""verify_R2_S1S2.py — independent test of route R2's PROPOSITION
(exact structure of the monotone 4-APs of Construction A).

Claim: every monotone 4-AP of a is ASCENDING and of exactly one shape
  S1: block(t0) < block(t1) = m-1,  {t2,t3} in B_m,  bit_l(t2) = m mod 2
  S2: block(t0) < m,  {t1,t2} in B_m,  t3 in B_{m+1}, bit_l(t1) = m mod 2
with t_i = x + i d and l = v2(d); and conversely.

I count the two sides SEPARATELY (positions census vs. the arithmetic predicate)
and compare.  R2 reports 979,436 (S1) + 324,832 (S2) = 1,304,268 at N = 16383.
"""
import numpy as np
from verify_R2 import construction_A_prefix

K = 7
N = 4 ** K - 1
seq = construction_A_prefix(K)
pos = np.zeros(N + 1, dtype=np.int64)
pos[np.array(seq, dtype=np.int64)] = np.arange(1, N + 1, dtype=np.int64)

blk = np.zeros(N + 1, dtype=np.int64)
for m in range(K):
    blk[4 ** m: min(4 ** (m + 1), N + 1)] = m

v2 = np.zeros(N + 1, dtype=np.int64)
for v in range(1, N + 1):
    v2[v] = (v & -v).bit_length() - 1

n_pos_inc = n_pos_dec = 0
n_s1 = n_s2 = 0
n_both = 0
mismatch = []

for d in range(1, (N - 1) // 3 + 1):
    top = N - 3 * d
    x = np.arange(1, top + 1, dtype=np.int64)
    t0, t1, t2, t3 = x, x + d, x + 2 * d, x + 3 * d
    p0, p1, p2, p3 = pos[t0], pos[t1], pos[t2], pos[t3]
    inc = (p0 < p1) & (p1 < p2) & (p2 < p3)
    dec = (p0 > p1) & (p1 > p2) & (p2 > p3)
    n_pos_inc += int(inc.sum()); n_pos_dec += int(dec.sum())

    l = int(v2[d])                       # v2 is constant along d
    b0, b1, b2, b3 = blk[t0], blk[t1], blk[t2], blk[t3]
    bit_t2 = (t2 >> l) & 1
    bit_t1 = (t1 >> l) & 1
    s1 = (b0 < b1) & (b1 == b2 - 1) & (b2 == b3) & (bit_t2 == (b2 & 1))
    s2 = (b0 < b1) & (b1 == b2) & (b3 == b2 + 1) & (bit_t1 == (b1 & 1))
    n_s1 += int(s1.sum()); n_s2 += int(s2.sum()); n_both += int((s1 & s2).sum())
    bad = np.nonzero(inc ^ (s1 | s2))[0]
    if bad.size and len(mismatch) < 5:
        for i in bad[:5]:
            mismatch.append((int(x[i]), d, bool(inc[i]), bool(s1[i]), bool(s2[i])))

lines = [
    f"Construction A, N = {N}",
    f"  monotone 4-APs by POSITION census : increasing {n_pos_inc}, decreasing {n_pos_dec}",
    f"  by ARITHMETIC predicate           : S1 {n_s1}, S2 {n_s2}, overlap {n_both}, "
    f"total {n_s1 + n_s2 - n_both}",
    f"  R2 REPORT claims                  : S1 979436, S2 324832, total 1304268, all ascending",
    f"  predicate == census, AP by AP     : {'YES (0 mismatches)' if not mismatch else 'NO: ' + str(mismatch)}",
]
print("\n".join(lines))
with open("/home/user/erdos/attempts/consolidated/verify_R2_S1S2.out", "w") as f:
    f.write("\n".join(lines) + "\n")
