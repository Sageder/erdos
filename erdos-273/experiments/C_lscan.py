"""
C_lscan.py -- Route C, Step 2, lattice selection.

CLAIM TESTED: which smooth L give the richest H-divisor lattices (largest reciprocal
budget), with and without the modulus 2, and how big is L?  A covering system needs
sum 1/m > 1 (Davenport-Mirsky-Newman-Rado for distinct moduli), and empirically the
divisor lattices that actually support one need noticeably more.

CONCLUSION: printed table; used to pick the lattices searched by C_hcover / C_sat.
"""
from sympy import isprime
from itertools import product


def divs(pe):
    ds = [1]
    for p, e in pe:
        ds = [d * p**i for d in ds for i in range(e + 1)]
    return sorted(ds)


def report(pe):
    L = 1
    for p, e in pe:
        L *= p**e
    ds = [d for d in divs(pe) if d >= 2 and isprime(2 * d + 1)]
    b = sum(1.0 / m for m in ds)
    b2 = b - (0.5 if 2 in ds else 0)
    b23 = b2 - (1.0 / 3 if 3 in ds else 0)
    return L, len(ds), b, b2, b23, ds


CANDS = []
for a in range(2, 7):
    for b in range(1, 5):
        for c in range(0, 3):
            for d in range(0, 2):
                for e in range(0, 2):
                    for f in range(0, 2):
                        pe = [(2, a), (3, b)]
                        if c: pe.append((5, c))
                        if d: pe.append((7, d))
                        if e: pe.append((11, e))
                        if f: pe.append((13, f))
                        CANDS.append(pe)

rows = []
for pe in CANDS:
    L, n, b, b2, b23, ds = report(pe)
    if L > 5 * 10**7:
        continue
    rows.append((b2, L, n, b, b23, ds))
rows.sort(reverse=True)
print(f"{'budget-no2':>10} {'budget-no23':>11} {'budget':>8} {'#H-div':>7}  L")
for b2, L, n, b, b23, ds in rows[:30]:
    print(f"{b2:10.4f} {b23:11.4f} {b:8.4f} {n:7d}  {L}")
print()
print("smallest H-divisors of the top lattice:", rows[0][5][:40])
