"""
A_common.py  -- shared utilities for Route A (SAT / exact-cover certificate search),
Erdos problem 273.

CLAIM TESTED (by the scripts that import this): for a given modulus L, can Z/L be covered
by residue classes whose moduli are DISTINCT divisors of L lying in
    E = {p-1 : p prime, p >= 5}      ("world E", membership: n >= 4 and n+1 prime)
or in
    H = {(p-1)/2 : p prime, p >= 5}  ("world H", membership: m >= 2 and 2m+1 prime) ?

STRUCTURAL FACT USED THROUGHOUT (proved in FINDINGS.md, Lemma A1):
Every n in E is even, n = 2m with m in H.  A class a mod 2m only meets integers of the
parity of a.  Hence an E-covering with moduli 2m_1,...,2m_k splits into two DISJOINT
families M_0 (classes with even residue) and M_1 (odd residue), and, after writing
even integers as 2t and odd as 2t+1, EACH of M_0, M_1 must be a covering system of Z
with distinct moduli taken from H.  Consequently:

   E-world at L = 2*Lh  is satisfiable  <=>  D_H(Lh) can be split into two disjoint
   subsets each of which supports a covering of Z/Lh.
   In particular  H-world at Lh UNSAT  ==>  E-world at 2*Lh UNSAT.

CONCLUSION: utilities only; conclusions are printed by the driver scripts.

Deterministic; exact integer / Fraction arithmetic only.
"""
from fractions import Fraction
from math import gcd
import itertools


# ----------------------------------------------------------------------------- primality
def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin (exact for all n < 3.3e24 with this witness set)."""
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def in_E(n: int) -> bool:
    return n >= 4 and is_prime(n + 1)


def in_H(m: int) -> bool:
    return m >= 2 and is_prime(2 * m + 1)


# ----------------------------------------------------------------------------- divisors
def divisors(L: int):
    ds, d = [], 1
    while d * d <= L:
        if L % d == 0:
            ds.append(d)
            if d != L // d:
                ds.append(L // d)
        d += 1
    return sorted(ds)


def D_E(L: int):
    """E-divisors of L, sorted increasing."""
    return [d for d in divisors(L) if in_E(d)]


def D_H(L: int):
    """H-divisors of L, sorted increasing."""
    return [d for d in divisors(L) if in_H(d)]


def D_V(L: int):
    """VALIDATION world only: every even divisor >= 4 of L.  Lemma A1 (the parity split)
    applies verbatim to any family of even moduli, so this world exercises exactly the same
    parity/budget machinery as world E while being small enough for brute force."""
    return [d for d in divisors(L) if d >= 4 and d % 2 == 0]


def budget(mods):
    return sum(Fraction(1, m) for m in mods)


# --------------------------------------------------------------- split feasibility (NEC)
def split_feasible(mods_H):
    """Is there a partition of mods_H into two disjoint parts, each with reciprocal
    sum > 1?  (Necessary condition for the E-world problem, by Lemma A1 plus the strict
    inequality sum 1/m > 1 valid for any covering system with distinct moduli > 1 --
    Davenport-Mirsky-Newman-Rado rules out equality.)

    Greedy witness search (exact Fraction arithmetic): add elements in DECREASING order
    of 1/m until the running sum first exceeds 1.  The overshoot is at most the last
    element added, so this gives the *smallest-overshoot-ish* part; if its complement
    also exceeds 1 we have a witness.  A negative answer from this routine is only
    conclusive when tot <= 2 (then it is a proof)."""
    tot = budget(mods_H)
    if tot <= 2:
        return False, tot, None
    best = None
    order = sorted(mods_H)                      # increasing m == decreasing 1/m
    for start in range(len(order)):
        part, s = [], Fraction(0)
        for m in order[start:] + order[:start]:
            if s > 1:
                break
            part.append(m)
            s += Fraction(1, m)
        if s > 1 and tot - s > 1:
            rest = sorted(set(mods_H) - set(part))
            best = (sorted(part), rest)
            break
    return (best is not None), tot, best


# ----------------------------------------------------------------------------- verify
def verify_cover(L, classes, world="E", relaxed=False):
    """classes = list of (n, a).  Checks: distinct moduli, all in the world, all divide L,
    and coverage of Z/L (all residues, or all but 0 when relaxed=True).
    Returns (ok, message)."""
    mods = [n for n, a in classes]
    if len(set(mods)) != len(mods):
        return False, "moduli not distinct"
    test = {"E": in_E, "H": in_H, "V": lambda d: d >= 4 and d % 2 == 0}[world]
    for n, a in classes:
        if not test(n):
            return False, f"modulus {n} not in world {world}"
        if L % n != 0:
            return False, f"modulus {n} does not divide L={L}"
        if relaxed and a % n == 0:
            return False, f"relaxed mode but class {a} mod {n} covers 0"
    cov = bytearray(L)
    for n, a in classes:
        a %= n
        cov[a::n] = b"\x01" * len(range(a, L, n))
    if relaxed:
        if cov[0]:
            return False, "residue 0 is covered but relaxed mode requires it uncovered"
        bad = [r for r in range(1, L) if not cov[r]]
    else:
        bad = [r for r in range(L) if not cov[r]]
    if bad:
        return False, f"{len(bad)} uncovered residues, e.g. {bad[:10]}"
    return True, "OK"
