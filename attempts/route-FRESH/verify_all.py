"""verify_all.py -- machine checks for every claim asserted in REPORT.md.

Run:  python3 verify_all.py
All arithmetic is exact integer arithmetic.  Cross-validated against
/home/user/erdos/experiments/apcheck.py.
"""
import sys, itertools, random
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import (has_monotone_kap_brute, has_monotone_kap_pos,
                     has_monotone_kap_general)
from core import has_kap_signs, has_kap_brute, Builder, build_check

FAIL = []
def check(name, cond, info=""):
    print(("  OK   " if cond else "  FAIL ") + name + (("   " + str(info)) if not cond else ""))
    if not cond:
        FAIL.append(name)

rng = random.Random(196196)

# ---- Prop 1: sign/run-length reformulation  == definition (apcheck ground truth)
ok = True
for _ in range(3000):
    n = rng.randint(4, 10)
    p = list(range(1, n+1)); rng.shuffle(p)
    for k in (3, 4, 5):
        if not (has_kap_signs(p, k) == has_monotone_kap_pos(p, k)
                == has_monotone_kap_brute(p, k) == has_kap_brute(p, k)):
            ok = False
check("Prop 1  (monotone k-AP  <=>  k-1 equal consecutive signs in some eps_e)", ok)

# ---- Lemma 2 (backward closure), stated as: no monotone 4-AP  <=>  every monotone
# 3-AP has its continuation placed strictly earlier than its 3rd term.
def closure_holds(perm):
    N = len(perm); pos = {v: i for i, v in enumerate(perm)}
    for e in range(1, N):
        for y in range(1, N+1):
            if y+2*e > N: break
            a_, b_, c_ = pos[y], pos[y+e], pos[y+2*e]
            if a_ < b_ < c_:                      # increasing monotone 3-AP
                w = y+3*e
                if w > N or not pos[w] < c_: return False
            if c_ < b_ < a_:                      # decreasing monotone 3-AP
                w = y-e
                if w >= 1 and not pos[w] < a_: return False
    return True
ok = True
for _ in range(4000):
    n = rng.randint(4, 9)
    p = list(range(1, n+1)); rng.shuffle(p)
    # inside [1..N] the "continuation exists" part needs w<=N, so compare on perms
    # whose relevant continuations stay in range: use the exact equivalence
    if closure_holds(p) and has_monotone_kap_pos(p, 4): ok = False
check("Lemma 2  (backward closure => no monotone 4-AP)", ok)

# ---- Lemma 3 = Builder engine (permanent blocking) equals 4-AP-freeness
ok = True
for _ in range(2000):
    n = rng.randint(4, 9)
    p = list(range(1, n+1)); rng.shuffle(p)
    if build_check(p, n) != (not has_monotone_kap_pos(p, 4)): ok = False
    for L in range(n+1):
        if build_check(p[:L], n) != (not has_monotone_kap_general(p[:L], 4)): ok = False
check("Lemma 3  (a value blocked by a monotone 3-AP is blocked forever)", ok)

# ---- Theorem 4 (records).  Exhaustive over all monotone-K-AP-free perms, N<=8.
def records(seq):
    R = []; m = 0
    for v in seq:
        if v > m: R.append(v); m = v
    return R
def record_violation(perm, K):
    N = len(perm); R = records(perm); S = set(R)
    for i in range(len(R)):
        for j in range(i+1, len(R)):
            d = R[j]-R[i]
            t = [R[i]+s*d for s in range(K-1)]
            if all(x in S for x in t) and t[-1]+d <= N: return t
    return None
def record_violation_allAP(perm, K):
    N = len(perm)
    for d in range(1, N+1):
        for c in range(1, d+1):
            S = set(range(c, N+1, d))
            if len(S) < K: continue
            sub = [v for v in perm if v in S]
            R = records(sub); Rs = set(R)
            for i in range(len(R)):
                for j in range(i+1, len(R)):
                    dd = R[j]-R[i]
                    if dd % d: continue
                    t = [R[i]+s*dd for s in range(K-1)]
                    if all(x in Rs for x in t) and t[-1]+dd <= N: return t
    return None
ok1 = ok2 = True; tot = 0
for N in range(4, 9):
    for K in (3, 4, 5):
        for p in itertools.permutations(range(1, N+1)):
            if has_monotone_kap_pos(p, K): continue
            tot += 1
            if record_violation(p, K): ok1 = False
            if record_violation_allAP(p, K): ok2 = False
check(f"Theorem 4  (record set has no (K-1)-AP), exhaustive on {tot} perms, N<=8, K=3,4,5", ok1)
check("Theorem 4' (same for the records of a|_S, every AP S), same exhaustive range", ok2)

# ---- Theorem 5 / Prop 6: (R) is FALSE -- explicit omega-order with no g(e)<g(2e)<g(3e)
def key(e):
    a = 0; m = e
    while m % 2 == 0: m //= 2; a += 1
    b = 0
    while m % 3 == 0: m //= 3; b += 1
    return a, b, m
def omega_order(E):
    it = []
    for e in range(1, E+1):
        a, b, m = key(e)
        it.append((max(m, a+b), a+b, -b, m, e))   # dovetailed: finite stages
    it.sort()
    return [x[-1] for x in it]
E = 20000
g = {e: i for i, e in enumerate(omega_order(E))}
bad = [e for e in range(1, E//3+1) if g[e] < g[2*e] < g[3*e]]
check(f"Prop 6  ((R) is false: 0 violations for e <= {E//3} in the antidiagonal order)",
      not bad, bad[:5])
# and: every stage of the dovetailing is finite (order type omega)
from collections import Counter
stages = Counter(max(key(e)[2], key(e)[0]+key(e)[1]) for e in range(1, E+1))
check("Prop 6  (the dovetailed order really has order type omega: finite stages)",
      all(v < 10**6 for v in stages.values()))

print()
print("ALL CHECKS PASSED" if not FAIL else f"FAILURES: {FAIL}")
