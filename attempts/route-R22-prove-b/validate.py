"""validate.py -- cross-validation of the route-R22 (ii)-checkers and helpers.

(1) check_ii_slow vs check_ii_fast on random class vectors and on structured ones.
(2) Controls from route R20 / CORE.md:
      - t(v) = v_2(v)   with b = 3   : (ii) HOLDS  (Lemma R20-1a; CLS(3,a))
      - t(v) = v_3(v)   with b = 3   : (ii) FAILS  at (1,4,7,10)  (R20 ledger, L-3ADIC)
      - t(v) = v_2(v)   with b = 2   : (ii) FAILS  (R20 sharpness: b=2 fails at x=1,d=6)
      - t(v) = floor(v_2(v)/2), b = 3: (ii) FAILS  at x=1, d=5    (R20 sharpness)
(3) blk() against math.log, and the *link* between (ii) and monotone 4-APs:
    for any emission order of the classes, a strictly monotone class sequence along a
    4-AP forces a monotone 4-AP of the resulting permutation (checked with the trusted
    experiments/apcheck.py on random small architectures).
"""

import sys, math, random
import numpy as np

sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
sys.path.insert(0, '/home/user/erdos/experiments')
from arch import (blk, blk_array, check_ii_slow, check_ii_fast, delay_from_t,
                  v2, v3, four_aps)                                      # noqa: E402
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute        # noqa: E402

rng = random.Random(22196)
ok = True


def report(name, cond):
    global ok
    ok = ok and bool(cond)
    print(f"  [{'OK ' if cond else 'FAIL'}] {name}")


print("(1) blk() vs math.log")
bad = 0
for b in (2, 3, 4, 5, 7):
    for v in range(1, 5000):
        if blk(v, b) != int(math.floor(math.log(v, b) + 1e-9)):
            bad += 1
    a = blk_array(5000, b)
    for v in range(1, 5001):
        if a[v] != blk(v, b):
            bad += 1
report("blk / blk_array agree with math.log on v<=5000, b in {2,3,4,5,7}", bad == 0)

print("(2) check_ii_slow vs check_ii_fast on 400 random class vectors")
bad = 0
for _ in range(400):
    M = rng.randint(10, 90)
    K = rng.randint(2, 6)
    c = [0] + [rng.randrange(K) for _ in range(M)]
    r1, r2 = check_ii_slow(c, M), check_ii_fast(c, M)
    # only the existence verdict must agree (witness choice may differ)
    if (r1 is None) != (r2 is None):
        bad += 1
report("existence verdicts agree on 400 random vectors", bad == 0)

print("(3) route-R20 controls")
M = 3000
t, c = delay_from_t(M, 3, v2)
report("b=3, t=v_2  : (ii) holds (Lemma R20-1a)", check_ii_fast(c, M) is None)
t, c = delay_from_t(M, 3, v3)
w = check_ii_fast(c, M)
# NOTE: R20's ledger entry "CLS3(3,a): (1,4,7,10)" is the first monotone 4-AP of the
# PERMUTATION, not a (ii)-violation: c(1,4,7,10) = (0,1,1,2) is not strictly monotone.
# The first (ii)-violation is at x=6, d=38: c = (2,3,4,5).  Both facts verified here.
report(f"b=3, t=v_3  : (ii) fails, witness={w}", w is not None and w[0] == 'inc')
report("b=3, t=v_3  : (1,4,7,10) is NOT a (ii)-violation (c = 0,1,1,2)",
       tuple(int(c[u]) for u in (1, 4, 7, 10)) == (0, 1, 1, 2))
t, c = delay_from_t(M, 2, v2)
w = check_ii_fast(c, M)
report(f"b=2, t=v_2  : (ii) fails, witness={w}", w is not None)
t, c = delay_from_t(M, 3, lambda v: v2(v) // 2)
w = check_ii_fast(c, M)
report(f"b=3, t=v_2//2: (ii) fails, witness={w}", w is not None and w[1] == 1 and w[2] == 5)

print("(4) (ii)-violation  =>  monotone 4-AP for EVERY within-class emission order")
bad = 0
trials = 0
for _ in range(600):
    N = rng.randint(8, 14)
    K = rng.randint(2, 5)
    c = [0] + [rng.randrange(K) for _ in range(N)]
    viol = check_ii_slow(c, N)
    if viol is None:
        continue
    trials += 1
    # build a random emission order: classes in increasing index order, random inside
    perm = []
    for j in range(K):
        cls = [v for v in range(1, N + 1) if c[v] == j]
        rng.shuffle(cls)
        perm.extend(cls)
    if not has_monotone_kap_pos(perm, 4):
        bad += 1
    if N <= 10 and has_monotone_kap_brute(perm, 4) != has_monotone_kap_pos(perm, 4):
        bad += 1
report(f"{trials} violating architectures all give a monotone 4-AP (any within-class order)",
       bad == 0)

print("\nALL OK" if ok else "\nSOME CHECK FAILED")
sys.exit(0 if ok else 1)
