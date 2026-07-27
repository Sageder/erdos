"""Calibration gate (PROMPT §6, mandatory first experiment).

Claims tested:
 (C1) digit criterion == exact big-integer criterion for k in 1..4, n in 1..300 (zero mismatches);
 (C2) S_1 starts 5,14,27,41,44,65,76,90,109,125,139,152,155,169 and has 40 elements up to 441;
 (C3) S_2 smallest element is 208; first 20 elements match PROBLEM.md; |S_2 ∩ [1,2e5]| = 1981;
 (C4) S_3 starts 3475,8174,8175,15195,16168,18682,18743,19290; |S_3 ∩ [1,6e4]| = 41;
 (C5) S_4 ∩ [1,6e4] = {8174, 51984};
 (C6) exact big-int spot checks: (6!)^2|10! quotient 7; (210!)^2|416!; (460!)^2|916!; (989!)^2|1974!.

Conclusion is printed at the end; any FAIL means our Legendre/digit code is wrong.
"""
import sys
sys.path.insert(0, '.')
from erdos727 import in_Sk_digit, in_Sk_bigint, in_Sk_fast
from sympy import factorial

ok = True

# C1: equivalence chain digit vs bigint; and fast vs digit on a wider range
mismatches = []
for k in range(1, 5):
    for n in range(1, 301):
        if in_Sk_digit(n, k) != in_Sk_bigint(n, k):
            mismatches.append((n, k))
print(f"C1a digit==bigint on k<=4, n<=300: {'PASS' if not mismatches else 'FAIL ' + str(mismatches)}", flush=True)
ok &= not mismatches
mismatches2 = []
for k in range(1, 5):
    for n in range(1, 4001):
        if in_Sk_fast(n, k) != in_Sk_digit(n, k):
            mismatches2.append((n, k))
print(f"C1b fast==digit on k<=4, n<=4000: {'PASS' if not mismatches2 else 'FAIL ' + str(mismatches2)}", flush=True)
ok &= not mismatches2

# C2: S_1
S1 = [n for n in range(1, 442) if in_Sk_digit(n, 1)]
exp_start = [5, 14, 27, 41, 44, 65, 76, 90, 109, 125, 139, 152, 155, 169]
c2 = S1[:14] == exp_start and len(S1) == 40
print(f"C2 S_1 start+count: {'PASS' if c2 else 'FAIL'} (got start {S1[:14]}, count {len(S1)})")
ok &= c2

# C3: S_2
S2 = [n for n in range(1, 200001) if in_Sk_fast(n, 2)]
exp_S2_start = [208, 458, 987, 1220, 1455, 1597, 1889, 2012, 2144, 2330, 2477, 2663, 2991,
                3353, 3415, 3430, 3439, 3475, 3476, 3551]
c3 = S2[:20] == exp_S2_start and len(S2) == 1981 and S2[0] == 208
print(f"C3 S_2: {'PASS' if c3 else 'FAIL'} (first20 match {S2[:20] == exp_S2_start}, count {len(S2)})")
ok &= c3

# C4: S_3
S3 = [n for n in range(1, 60001) if in_Sk_fast(n, 3)]
exp_S3_start = [3475, 8174, 8175, 15195, 16168, 18682, 18743, 19290]
c4 = S3[:8] == exp_S3_start and len(S3) == 41
print(f"C4 S_3: {'PASS' if c4 else 'FAIL'} (start {S3[:8]}, count {len(S3)})")
ok &= c4

# C5: S_4
S4 = [n for n in range(1, 60001) if in_Sk_fast(n, 4)]
c5 = S4 == [8174, 51984]
print(f"C5 S_4: {'PASS' if c5 else 'FAIL'} (got {S4})")
ok &= c5

# C6: exact big-int spot checks
q = factorial(10) // (factorial(6) ** 2)
c6 = (factorial(10) % (factorial(6) ** 2) == 0 and q == 7
      and factorial(416) % (factorial(210) ** 2) == 0
      and factorial(916) % (factorial(460) ** 2) == 0
      and factorial(1974) % (factorial(989) ** 2) == 0)
print(f"C6 bigint spot checks: {'PASS' if c6 else 'FAIL'}")
ok &= c6

print("CALIBRATION:", "ALL PASS" if ok else "FAILURE — do not trust the checker")
