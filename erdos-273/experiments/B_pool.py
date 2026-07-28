"""
B_pool.py  -- Route B (recursive / hierarchical construction), step 1.

CLAIM TESTED
------------
(1) The recursion of Route B.  To cover a residue class  r (mod D)  using only moduli that are
    multiples of D, substitute x = r + D*y; a modulus n = D*e covers a class mod e in y-space,
    and n lies in E  iff  D*e + 1 is prime and D*e >= 4.   So the LOCAL POOL at node D is
        P(D) := { e >= 1 : D*e + 1 prime,  D*e >= 4 }.
    e = 1 is the terminating move (single modulus D closes the whole class).
    This script VERIFIES that identity directly (brute force on small D) and then measures
    the pool budgets.

(2) Heuristic prediction for the pool budget
        B(D,Y) := sum_{e in P(D), e <= Y} 1/e   ~   (D/phi(D)) * log( log(D*Y) / log(D) ).
    (Primes in the AP 1 mod D have density  1/(phi(D) log t); substituting t = D e gives
     density  D/(phi(D) log(De))  in e-space, and integrating 1/(e log(De)) gives the log-log.)
    This script MEASURES B(D,Y) for many D and Y and compares with the prediction.

(3) Divisor-restricted budgets: for smooth L,
        sum_{n | L, n in E} 1/n      and      sum_{m | L, m in H} 1/m,
    where H = {m >= 2 : 2m+1 prime}.  These are the budgets actually available to a covering
    system whose lcm divides L.  A covering needs budget >= 1 (E-world) / >= 2 (H-world, since
    the E-problem splits into TWO DISJOINT H-coverings).

CONCLUSION: see the printed tables; recorded in attempts/route-B-recursive/FINDINGS.md.

Deterministic; primality by sieve (exact integer arithmetic).
"""
import sys
from math import gcd, lcm, log
from sympy import isprime, totient


# ---------------------------------------------------------------- sieve helpers
def primes_upto(N):
    bs = bytearray([1]) * (N + 1)
    bs[0:2] = b"\x00\x00"
    i = 2
    while i * i <= N:
        if bs[i]:
            bs[i * i::i] = bytearray(len(range(i * i, N + 1, i)))
        i += 1
    return bs


def pool_sieve(D, Y, small_primes):
    """Exact list of e in [1,Y] with D*e+1 prime (trial division by primes <= sqrt(D*Y))."""
    import numpy as np
    n = np.arange(1, Y + 1, dtype=np.int64) * D + 1
    isp = np.ones(Y, dtype=bool)
    lim = int((D * Y + 1) ** 0.5) + 1
    for p in small_primes:
        if p > lim:
            break
        # first index where n[i] % p == 0  ->  D*e+1 = 0 mod p  ->  e = -D^{-1} mod p
        if D % p == 0:
            continue
        inv = pow(int(D), -1, p)
        e0 = (-inv) % p
        if e0 == 0:
            e0 = p
        idx = e0 - 1
        if idx < Y:
            isp[idx::p] = False
        # p itself may equal D*e+1
        if (p - 1) % D == 0:
            e = (p - 1) // D
            if 1 <= e <= Y:
                isp[e - 1] = True
    return [int(e) for e in np.nonzero(isp)[0] + 1]


# ---------------------------------------------------------------- (1) verify the recursion
def verify_recursion():
    print("=" * 78)
    print("(1)  VERIFY the Route-B recursion identity  (brute force, small D)")
    print("=" * 78)
    ok = True
    for D in range(1, 60):
        # multiples of D that lie in E, up to some bound
        direct = [n for n in range(4, 4000) if n % D == 0 and isprime(n + 1)]
        viarec = [D * e for e in range(1, 4000 // max(D, 1) + 1)
                  if D * e >= 4 and D * e <= 4000 and isprime(D * e + 1)]
        if direct != viarec:
            ok = False
            print("  MISMATCH at D =", D)
    print("  {n in E : D | n} == {D*e : e in P(D)} for all D <= 59, n <= 4000 :",
          "OK" if ok else "FAIL")
    # and: class r mod D is covered by a mod (D e) iff  a = r mod D  and  y = (a-r)/D mod e
    import random
    rnd = random.Random(7)
    ok2 = True
    for _ in range(2000):
        D = rnd.randrange(1, 30)
        e = rnd.randrange(1, 30)
        r = rnd.randrange(D)
        a = r + D * rnd.randrange(e)
        b = (a - r) // D
        for x in range(r, r + D * e * 3, D):
            y = (x - r) // D
            if ((x - a) % (D * e) == 0) != ((y - b) % e == 0):
                ok2 = False
    print("  rescaling x = r + D y identifies (a mod De) with (b mod e) :",
          "OK" if ok2 else "FAIL")
    print()


# ---------------------------------------------------------------- (2) pool budgets
def pool_budgets():
    print("=" * 78)
    print("(2)  POOL BUDGETS   B(D,Y) = sum_{e<=Y, D e + 1 prime} 1/e     vs heuristic")
    print("     heuristic  = (D/phi(D)) * log( log(D Y) / log D )")
    print("=" * 78)
    bs = primes_upto(10_000_000)
    small_primes = [i for i in range(2, 10_000_000) if bs[i]]
    # keep only what we need for trial division
    small_primes = small_primes[:len(small_primes)]

    Ds = [1, 2, 4, 6, 12, 24, 30, 60, 120, 210, 360, 420, 840, 2310, 2520,
          30030, 60060, 360360, 510510, 720720, 4324320, 9699690]
    Ys = [10, 100, 1000, 10000, 100000]
    print(f"{'D':>10} {'D/phi(D)':>9} | " +
          " | ".join(f"Y=1e{len(str(Y))-1}: meas / pred" for Y in Ys))
    for D in Ds:
        row = []
        ph = int(totient(D))
        rat = D / ph
        for Y in Ys:
            P = pool_sieve(D, Y, small_primes)
            meas = sum(1.0 / e for e in P)
            if D == 1:
                pred = float('nan')
            else:
                pred = rat * log(log(D * Y) / log(D)) if D > 1 else float('nan')
            row.append(f"{meas:7.3f}/{pred:7.3f}")
        print(f"{D:>10} {rat:9.4f} | " + " | ".join(row))
    print()
    return small_primes


# ---------------------------------------------------------------- (3) divisor budgets
def divisors_of(fac):
    ds = [1]
    for p, a in fac:
        ds = [d * p ** i for d in ds for i in range(a + 1)]
    return sorted(ds)


def divisor_budgets(small_primes):
    print("=" * 78)
    print("(3)  DIVISOR-RESTRICTED BUDGETS for smooth L")
    print("     E-world:  N_E(L) = {n | L : n >= 4, n+1 prime},  budget sum 1/n   (need >= 1)")
    print("     H-world:  N_H(L) = {m | L : m >= 2, 2m+1 prime}, budget sum 1/m   (need >= 2)")
    print("=" * 78)
    isp = set()
    cands = [
        [(2, 3), (3, 2), (5, 1), (7, 1)],
        [(2, 4), (3, 2), (5, 1), (7, 1), (11, 1)],
        [(2, 4), (3, 3), (5, 2), (7, 1), (11, 1), (13, 1)],
        [(2, 5), (3, 3), (5, 2), (7, 2), (11, 1), (13, 1)],
        [(2, 6), (3, 4), (5, 2), (7, 2), (11, 1), (13, 1), (17, 1)],
        [(2, 6), (3, 4), (5, 3), (7, 2), (11, 2), (13, 1), (17, 1), (19, 1)],
        [(2, 8), (3, 5), (5, 3), (7, 2), (11, 2), (13, 2), (17, 1), (19, 1), (23, 1)],
        [(2, 10), (3, 6), (5, 4), (7, 3), (11, 2), (13, 2), (17, 1), (19, 1), (23, 1),
         (29, 1), (31, 1)],
        [(2, 12), (3, 7), (5, 4), (7, 3), (11, 2), (13, 2), (17, 2), (19, 1), (23, 1),
         (29, 1), (31, 1), (37, 1), (41, 1), (43, 1)],
    ]
    for fac in cands:
        L = 1
        for p, a in fac:
            L *= p ** a
        ds = divisors_of(fac)
        NE = [n for n in ds if n >= 4 and isprime(n + 1)]
        NH = [m for m in ds if m >= 2 and isprime(2 * m + 1)]
        bE = sum(1.0 / n for n in NE)
        bH = sum(1.0 / m for m in NH)
        print(f"L = {L:<24} ({dict(fac)})")
        print(f"   #div={len(ds):<7} |N_E|={len(NE):<6} bE={bE:8.4f}   "
              f"|N_H|={len(NH):<6} bH={bH:8.4f}")
        print(f"   N_E small: {NE[:14]}")
        print(f"   N_H small: {NH[:16]}")
        print()


if __name__ == "__main__":
    verify_recursion()
    sp = pool_budgets()
    divisor_budgets(sp)
