"""
A_scan_L.py

CLAIM TESTED: which highly-composite L give the largest "E-divisor budget"
    B_E(L) = sum_{n | L, n in E} 1/n           (E = {p-1 : p >= 5 prime})
and equivalently  B_H(Lh) = 2 B_E(2 Lh) = sum_{m | Lh, m in H} 1/m ?
Also: the number of admissible moduli, and whether the necessary parity-split
condition (Lemma A1: D_H must split into two disjoint parts each with 1/m-sum > 1)
can hold at all.

Why: a covering of Z/L by classes with distinct moduli in E dividing L forces
B_E(L) > 1, and after the parity split each half needs H-sum > 1, i.e. B_H(L/2) > 2.
This picks the L worth throwing at the SAT solver, and rules out the rest OUTRIGHT.

CONCLUSION: printed table -- see attempts/route-A-satsearch/FINDINGS.md.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import D_E, D_H, budget, split_feasible, divisors
from fractions import Fraction
from math import lcm

CANDIDATES = [
    720720, 2162160, 4324320, 5045040, 10810800, 21621600,
    360360, 1441440, 2882880, 8648640, 12252240, 17297280, 32432400,
    # a few extra shapes
    2 * 2 * 2 * 2 * 3 * 3 * 5 * 7 * 11 * 13,          # 720720
    2**5 * 3**3 * 5**2 * 7 * 11 * 13,                  # 8648640
    2**4 * 3**3 * 5**2 * 7 * 11 * 13,                  # 4324320
    2**4 * 3**2 * 5**2 * 7 * 11 * 13 * 17,             # 61261200
    2**5 * 3**2 * 5**2 * 7 * 11 * 13,                  # 7207200
    2**4 * 3**4 * 5**2 * 7 * 11 * 13,                  # 12972960
    2**6 * 3**3 * 5**2 * 7 * 11 * 13,                  # 17297280
    2**4 * 3**3 * 5**2 * 7**2 * 11 * 13,               # 30270240
]


def report(L):
    de = D_E(L)
    dh = D_H(L // 2) if L % 2 == 0 else []
    be = budget(de)
    bh = budget(dh)
    ok, tot, wit = split_feasible(dh) if dh else (False, Fraction(0), None)
    lcm_de = 1
    for n in de:
        lcm_de = lcm(lcm_de, n)
    return dict(L=L, nE=len(de), B_E=float(be), lcmE=lcm_de,
                Lh=L // 2, nH=len(dh), B_H=float(bh), split=ok, wit=wit, de=de, dh=dh)


if __name__ == "__main__":
    seen = set()
    rows = []
    for L in CANDIDATES:
        if L in seen:
            continue
        seen.add(L)
        rows.append(report(L))
    rows.sort(key=lambda r: r["L"])
    print(f"{'L':>12} {'#E-div':>7} {'B_E':>8} {'lcm(D_E)':>12} "
          f"{'Lh=L/2':>10} {'#H-div':>7} {'B_H':>8} {'split?':>7}")
    for r in rows:
        print(f"{r['L']:>12} {r['nE']:>7} {r['B_E']:>8.4f} {r['lcmE']:>12} "
              f"{r['Lh']:>10} {r['nH']:>7} {r['B_H']:>8.4f} {str(r['split']):>7}")
    print()
    for r in rows:
        print(f"L={r['L']}  D_E = {r['de']}")
        print(f"    Lh={r['Lh']} D_H = {r['dh']}")
        if r["wit"]:
            p, q = r["wit"]
            print(f"    a legal split: {p}  (sum {float(budget(p)):.4f})  |  "
                  f"{q} (sum {float(budget(q)):.4f})")
        print()
