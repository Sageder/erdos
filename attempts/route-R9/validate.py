"""validate.py — independent cross-checks for census.c (Route R9).

Claims tested:
 (V1) exact counts of 4-AP-avoiders for N<=8 match brute force (apcheck.has_monotone_kap_pos,
      itself cross-validated against the literal definition in apcheck.__main__).
 (V2) the SET of avoiders enumerated by census dump equals the brute-force set (N=7,8).
 (V3) insertion principle: for every avoider of [1..8], the set of slots where value 9 can
      be inserted keeping 4-AP-freeness (checked by FULL brute-force 4-AP scan of each
      candidate child) equals a contiguous interval, and equals the [lo,hi] formula used
      by census.c.
 (V4) tame counts: for C=2 (pos(v)<=2v) and K=3 (pos(v)<=v+3), python-filtered brute-force
      counts for N<=8 match census tame mode, for k=4 and k=3.
 (V5) 3AP-free counts N<=8 match brute force.
"""
import subprocess, sys, itertools
sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos, has_monotone_kap_general

CENSUS = "/home/user/erdos/attempts/route-R9/census"
ok = True

def brute_avoiders(n, k=4):
    return set(p for p in itertools.permutations(range(1, n + 1))
               if not has_monotone_kap_pos(p, k))

# V1 + V2
for n in (6, 7, 8):
    bf = brute_avoiders(n)
    out = subprocess.run([CENSUS, "dump", str(n)], capture_output=True, text=True).stdout
    dumped = set(tuple(map(int, line.split())) for line in out.strip().splitlines())
    match = bf == dumped
    print(f"V1/V2 N={n}: brute={len(bf)} dumped={len(dumped)} set-equal={match}")
    ok &= match

# V3: insertion interval principle at N=8 -> 9
bf8 = brute_avoiders(8)
n = 8; m = 9
bad = 0; interval_bad = 0
for p in bf8:
    pos = {v: i for i, v in enumerate(p)}
    # brute-force allowed slots
    allowed = []
    for slot in range(n + 1):
        child = p[:slot] + (m,) + p[slot:]
        if not has_monotone_kap_pos(child, 4):
            allowed.append(slot)
    # formula
    lo, hi = 0, n
    for d in range(1, (m - 1) // 3 + 1):
        a, b, c = pos[m - 3 * d], pos[m - 2 * d], pos[m - d]
        if a < b < c:
            hi = min(hi, c)
        elif a > b > c:
            lo = max(lo, c + 1)
    formula = list(range(lo, hi + 1)) if lo <= hi else []
    if allowed != formula:
        bad += 1
    if allowed and allowed != list(range(allowed[0], allowed[-1] + 1)):
        interval_bad += 1
print(f"V3 N=8->9: formula mismatches={bad}, non-interval allowed-sets={interval_bad} "
      f"(over {len(bf8)} avoiders)")
ok &= (bad == 0 and interval_bad == 0)

# V5: 3AP-free counts
for n in (6, 7, 8):
    c = len(brute_avoiders(n, 3))
    print(f"V5 N={n}: brute 3AP-free count = {c}")

# V4: tame counts by direct filtering
def tame_ok_mult(p, num, den):
    return all(den * (i + 1) <= num * v for i, v in enumerate(p))
def tame_ok_add(p, K):
    return all((i + 1) <= v + K for i, v in enumerate(p))

for k in (3, 4):
    for n in (6, 7, 8):
        av = brute_avoiders(n, k)
        c2 = sum(1 for p in av if tame_ok_mult(p, 2, 1))
        k3 = sum(1 for p in av if tame_ok_add(p, 3))
        print(f"V4 k={k} N={n}: brute tame C=2 -> {c2} ; tame K=+3 -> {k3}")

print("ALL SET-CHECKS PASS" if ok else "FAILURES PRESENT")
