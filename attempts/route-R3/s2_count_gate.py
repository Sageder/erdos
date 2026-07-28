"""Calibration gate: |S_2 cap [1, 2*10^5]| = 1981 (PROBLEM.md sanity data).

Uses the fast per-prime form (Claim R4 of reductions.py, proved in FAMILY.md Lemma 1
and cross-checked against the verbatim PROBLEM.md criterion for n < 4000 in
breakage_test2.py): n in S_2 iff for every prime p | (n+1)(n+2),
carries_p(n+n) >= 2 nu_p(n+1) + 2 nu_p(n+2). Exact integer arithmetic only.
"""
from sympy import factorint
from membership import carries

N = 200000
cnt = 0
first = []
f1 = factorint(2)  # factorint(n+1) at n = 1
for n in range(1, N + 1):
    f2 = factorint(n + 2)
    ok = all(carries(n, n, p) >= 2 * f1.get(p, 0) + 2 * f2.get(p, 0)
             for p in set(f1) | set(f2))
    if ok:
        cnt += 1
        if len(first) < 20:
            first.append(n)
    f1 = f2
print("|S_2 cap [1, 2*10^5]| =", cnt)
assert cnt == 1981, cnt
assert first == [208, 458, 987, 1220, 1455, 1597, 1889, 2012, 2144, 2330,
                 2477, 2663, 2991, 3353, 3415, 3430, 3439, 3475, 3476, 3551]
print("S_2 count gate PASSED (1981, first 20 as in PROBLEM.md)")
