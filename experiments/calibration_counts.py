"""calibration_counts.py — PROMPT §5 calibration reproduction.

Claim tested: counts of monotone-4-AP-free permutations of [1..N], N=3..9, equal
6, 22, 102, 564, 3336, 22266, 168864; and monotone-3-AP-free counts equal
4, 10, 20, 48, 104, 282, 496 (OEIS A003407).
Conclusion: printed below; MUST match or our checker is wrong.
"""

from apcheck import count_avoiders

EXPECT4 = [6, 22, 102, 564, 3336, 22266, 168864]
EXPECT3 = [4, 10, 20, 48, 104, 282, 496]

got4, got3 = [], []
for n in range(3, 10):
    c4 = count_avoiders(n, 4)
    c3 = count_avoiders(n, 3)
    got4.append(c4)
    got3.append(c3)
    print(f"N={n}: 4AP-free={c4}  3AP-free={c3}", flush=True)

assert got4 == EXPECT4, (got4, EXPECT4)
assert got3 == EXPECT3, (got3, EXPECT3)
print("CALIBRATION PASSED: both count sequences match PROMPT §5 exactly.")
