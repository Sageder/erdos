"""k=2 experiments, part 2: fast membership via R4 (only primes dividing (n+1)(n+2)
matter; R4 was verified against the full PROBLEM.md criterion in reductions.py and is a
one-line theorem: for p not dividing (n+1)(n+2), 2 nu_p(n+1)+2 nu_p(n+2) = 0).

B3': Pell chains with fast test, larger range.
B4': conditional repair pq+1=2rs, larger range, fast test, but every found solution is
     RE-verified with the full slow PROBLEM.md criterion (in_Sk) as a double check.
"""
from sympy import factorint, primerange
from membership import in_Sk, carries, failing_primes
from family_test import family_pairs

def in_S2_fast(n):
    f = factorint(n + 1)
    g = factorint(n + 2)
    for p in set(f) | set(g):
        if carries(n, n, p) < 2 * f.get(p, 0) + 2 * g.get(p, 0):
            return False
    return True

# consistency spot-check of fast test vs full criterion
for n in range(1, 4000):
    assert in_S2_fast(n) == in_Sk(n, 2), n
print("fast S_2 test == full criterion for n < 4000: OK")

# ---------- B3': Pell ----------
print("\nB3': Pell x^2-2y^2=-1, n+1=x^2, n+2=2y^2")
x, y = 1, 1
hits = []
for _ in range(30):
    x, y = 3 * x + 4 * y, 2 * x + 3 * y
    n = x * x - 2
    ok = in_S2_fast(n)
    if ok:
        hits.append((x, y, n))
print(f"   checked 30 Pell(-1) solutions (x up to ~{x:.2e}); members of S_2: {hits}")

print("B3': Pell x^2-2y^2=+1, n+1=2y^2, n+2=x^2")
x, y = 3, 2
hits2 = []
for _ in range(30):
    n = x * x - 2
    ok = in_S2_fast(n)
    if ok:
        hits2.append((x, y, n))
    x, y = 3 * x + 4 * y, 2 * x + 3 * y
print(f"   checked 30 Pell(+1) solutions; members of S_2: {hits2}")

# ---------- B4': conditional repair ----------
print("\nB4': solutions of pq+1=2rs with all carry conditions, q <= 4000")
sols = []
semiprime_cnt = 0
for q, p in family_pairs(4000):
    n = p * q - 1
    m2 = (n + 2) // 2
    f = factorint(m2)
    if len(f) != 2 or set(f.values()) != {1}:
        continue
    s, r = sorted(f)
    semiprime_cnt += 1
    if s < 5:
        continue
    if not (2 * s + 1 <= r <= 4 * s - 1):
        continue
    if (2 * r) % s < (s + 1) // 2:
        continue
    if n & (n - 1) == 0:
        continue
    sols.append((q, p, s, r, n))
print(f"   members with n+2 = 2rs (r,s distinct odd primes): {semiprime_cnt}")
print(f"   full-condition solutions: {len(sols)}")
bad = [t for t in sols if not in_S2_fast(t[4])]
print(f"   counterexamples (fast test): {bad}")
# slow double-check on all solutions with n < 2*10^6, and 10 random larger ones
import random
random.seed(1)
small = [t for t in sols if t[4] < 2 * 10**6]
big = [t for t in sols if t[4] >= 2 * 10**6]
sample = small + random.sample(big, min(10, len(big)))
for t in sample:
    assert in_Sk(t[4], 2), ("slow check fails", t)
print(f"   slow full-criterion double-check on {len(sample)} solutions: OK")
print("   first 12 solutions (q,p,s,r,n):")
for t in sols[:12]:
    print("   ", t)
print("   growth: solutions with q<=1000:", len([t for t in sols if t[0] <= 1000]),
      "; q<=2000:", len([t for t in sols if t[0] <= 2000]),
      "; q<=4000:", len(sols))
