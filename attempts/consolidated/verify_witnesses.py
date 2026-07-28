"""verify_witnesses.py — re-verify stored finite witnesses of routes R4 and R9
with the TRUSTED checker experiments/apcheck.py, and independently cross-check
the class-Bp (injective sequence) enumeration by brute force.
"""
import sys, os, glob, json
from fractions import Fraction
sys.path.insert(0, "/home/user/erdos/experiments")
import apcheck

OUT = []
def P(s):
    OUT.append(s)


# ---------- 1. cross-validate the sequence (class Bp) search by pure brute force ----------
def brute_seq_levels(C, maxi):
    """All injective sequences a(1..i) of positive ints with a(j) <= floor(C*j) and no
    monotone 4-AP among values, enumerated with the DEFINITION checker (apcheck)."""
    num, den = C.numerator, C.denominator
    levels = []
    cur = [[]]
    for i in range(1, maxi + 1):
        hi = (num * i) // den
        nxt = []
        for s in cur:
            for w in range(1, hi + 1):
                if w in s:
                    continue
                t = s + [w]
                if not apcheck.has_monotone_kap_general(t, 4):
                    nxt.append(t)
        levels.append(len(nxt))
        cur = nxt
        if not cur:
            break
    return levels, cur


for C, expect in ((Fraction(1, 1), 4), (Fraction(5, 4), 6), (Fraction(4, 3), 18)):
    lv, last = brute_seq_levels(C, 25)
    ext = len(lv) if lv and lv[-1] == 0 else None
    P(f"Bp brute-force (apcheck definition checker), a(i) <= {C}*i: level counts {lv}"
      f"  -> EXTINCT at i={ext}   (route R4 thresholds.tsv claims {expect})")

# ---------- 2. R9's N=50, C<=2 witness ----------
w50 = [1, 10, 17, 2, 4, 3, 8, 9, 7, 5, 23, 6, 25, 28, 21, 22, 15, 18, 20, 16, 19, 11, 13,
       12, 37, 40, 14, 46, 38, 42, 50, 49, 47, 43, 48, 34, 35, 39, 45, 41, 44, 31, 29, 33,
       36, 32, 26, 24, 30, 27]
pos = {v: i + 1 for i, v in enumerate(w50)}
P(f"R9 N=50 witness: permutation of [1..50]={sorted(w50) == list(range(1,51))}  "
  f"monotone-4AP(apcheck brute-free fast)={apcheck.has_monotone_kap_pos(w50,4)}  "
  f"max pos(v)/v={max(pos[v]/v for v in range(1,51)):.6f}  "
  f"(claimed: 4-AP-free, max ratio 2.0)")

# ---------- 3. R4 stored avoiders: verify the largest N in each file ----------
AV = "/home/user/erdos/attempts/route-R4/avoiders"
for fn in sorted(glob.glob(os.path.join(AV, "*.txt"))):
    best = None
    with open(fn) as f:
        for line in f:
            line = line.strip()
            if not line.startswith("N="):
                continue
            parts = dict(p.split("=", 1) for p in line.split(" ", 2)[0:1])
            n = int(line.split()[0][2:])
            perm = [int(x) for x in line.split("perm=")[1].split(",")]
            if best is None or n > best[0]:
                best = (n, perm)
    if best is None:
        continue
    n, perm = best
    isperm = sorted(perm) == list(range(1, n + 1))
    ap4 = (apcheck.has_monotone_kap_pos(perm, 4) if isperm
           else apcheck.has_monotone_kap_general(perm, 4))
    posm = {v: i + 1 for i, v in enumerate(perm)}
    ratio_up = max(posm[v] / v for v in perm)          # pos(v)/v   (class A)
    ratio_val = max(perm[i] / (i + 1) for i in range(n))  # a(i)/i  (classes B / Bp)
    P(f"R4 {os.path.basename(fn):22s} largest N={n:3d}  perm-of-[1..N]={isperm}  "
      f"monotone4AP={ap4}  max pos(v)/v={ratio_up:.4f}  max a(i)/i={ratio_val:.4f}")

# ---------- 4. R4 survivor files: verify ALL entries ----------
SV = "/home/user/erdos/attempts/route-R4/survivors"
for fn in sorted(glob.glob(os.path.join(SV, "*.txt"))):
    bad = 0
    tot = 0
    ratios = []
    with open(fn) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            toks = line.replace(",", " ").split()
            try:
                perm = [int(x) for x in toks if x.lstrip("-").isdigit()]
            except ValueError:
                continue
            if not perm:
                continue
            tot += 1
            n = len(perm)
            isperm = sorted(perm) == list(range(1, n + 1))
            ap4 = (apcheck.has_monotone_kap_pos(perm, 4) if isperm
                   else apcheck.has_monotone_kap_general(perm, 4))
            if ap4:
                bad += 1
            posm = {v: i + 1 for i, v in enumerate(perm)}
            ratios.append(max(posm[v] / v for v in perm))
    P(f"R4 survivors/{os.path.basename(fn):24s} {tot:6d} entries, {bad} with a monotone 4-AP"
      f"{'' if ratios == [] else f', max pos/v in [{min(ratios):.4f},{max(ratios):.4f}]'}")

print("\n".join(OUT))
with open("/home/user/erdos/attempts/consolidated/verify_witnesses.out", "w") as f:
    f.write("\n".join(OUT) + "\n")
