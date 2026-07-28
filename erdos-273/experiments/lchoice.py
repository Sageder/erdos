"""
CLAIM TESTED: which smooth L admit enough divisors in E (resp. H) to have any chance of
supporting a covering system?  For each candidate L we list
    D_H(L) = {m : m | L, 2m+1 prime}          (H-world moduli; L is the H-world lcm)
    budget = sum 1/m over D_H(L)
and, because the E-world system splits by parity into two DISJOINT H-systems, the relevant
necessary condition is  budget > 2  (each half needs > 1) -- and in practice noticeably more.

CONCLUSION: printed table, recorded in NOTES.md.
"""
from sympy import isprime, factorint
from itertools import product


def divisors_from_exp(pe):
    ds = [1]
    for p, e in pe:
        ds = [d * p ** i for d in ds for i in range(e + 1)]
    return sorted(ds)


def DH(pe):
    return [m for m in divisors_from_exp(pe) if m >= 2 and isprime(2 * m + 1)]


def report(pe, label=""):
    L = 1
    for p, e in pe:
        L *= p ** e
    ds = DH(pe)
    b = sum(1.0 / m for m in ds)
    print(f"L = {L:<22} {label}")
    print(f"   factor {dict(pe)}   #divisors={len(divisors_from_exp(pe))}  "
          f"#in H = {len(ds)}   budget = {b:.4f}")
    return L, ds, b


CANDIDATES = [
    [(2, 3), (3, 2), (5, 1), (7, 1), (11, 1), (13, 1)],          # 360360
    [(2, 4), (3, 3), (5, 2), (7, 1), (11, 1), (13, 1)],
    [(2, 5), (3, 3), (5, 2), (7, 1), (11, 1), (13, 1)],
    [(2, 5), (3, 4), (5, 2), (7, 2), (11, 1), (13, 1)],
    [(2, 6), (3, 4), (5, 2), (7, 2), (11, 1), (13, 1), (17, 1)],
    [(2, 6), (3, 4), (5, 3), (7, 2), (11, 1), (13, 1), (17, 1), (19, 1)],
    [(2, 7), (3, 5), (5, 3), (7, 2), (11, 2), (13, 1), (17, 1), (19, 1), (23, 1)],
    [(2, 8), (3, 5), (5, 3), (7, 2), (11, 2), (13, 2), (17, 1), (19, 1), (23, 1),
     (29, 1), (31, 1)],
    [(2, 10), (3, 6), (5, 4), (7, 3), (11, 2), (13, 2), (17, 1), (19, 1), (23, 1),
     (29, 1), (31, 1), (37, 1), (41, 1), (43, 1)],
]

if __name__ == "__main__":
    for pe in CANDIDATES:
        L, ds, b = report(pe)
        print("   smallest 30 H-divisors:", ds[:30])
        print()
