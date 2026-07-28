"""
ADVERSARIAL AUDIT: verify the concrete artifacts claimed in NOTES.md / FINDINGS.md.
 - the route-A H-covering with moduli {2,3,5,6,9,15,18,20,30,36,90}
 - its lift covering EXACTLY the even integers with E-moduli
 - the E-covering of ALL of Z would need a second disjoint half
 - E_selfridge360 claim: divisors of 360 in E, sum 23/18, cover exists
 - the smallest L with B_E(L) > 1 is 55440, and the 'all divisible by 60' claim
"""
import json, sys
from fractions import Fraction
from math import gcd
from sympy import isprime


def lcm(xs):
    L = 1
    for x in xs:
        L = L * x // gcd(L, x)
    return L


def hitmask(classes, L):
    hit = bytearray(L)
    for a, n in classes:
        seg = hit[a % n::n]
        hit[a % n::n] = b'\x01' * len(seg)
    return hit


def check_H_cert():
    d = json.load(open("attempts/route-A-satsearch/certs/cert_H_full_L180.json"))
    cls = [(a, m) for m, a in d["classes"]]
    mods = [m for _, m in cls]
    assert len(set(mods)) == len(mods), "moduli not distinct"
    assert all(isprime(2 * m + 1) and m >= 2 for m in mods), "not all in H"
    L = lcm(mods)
    hit = hitmask(cls, L)
    print(f"  route-A H-cert: moduli {sorted(mods)} lcm {L} covers Z: {all(hit)} "
          f"cost {sum(Fraction(1,m) for m in mods)}")
    assert all(hit)
    # lift with j=0 and j=1
    for j in (0, 1):
        E = [(2 * a + j, 2 * m) for a, m in cls]
        Emods = sorted(n for _, n in E)
        assert all(isprime(n + 1) and n >= 4 for n in Emods)
        P = lcm(Emods)
        h = hitmask(E, P)
        cov_j = all(h[x] for x in range(j, P, 2))
        cov_other = any(h[x] for x in range(1 - j, P, 2))
        print(f"    lift j={j}: E-moduli {Emods}, covers ALL x={j} mod 2: {cov_j}; "
              f"covers ANY x={1-j} mod 2: {cov_other}; cost {sum(Fraction(1,n) for n in Emods)}")
        assert cov_j and not cov_other
    print("  ==> NOTES' 'one half solved explicitly' artifact verified.")


def BE(L):
    return sum(Fraction(1, n) for n in range(4, L + 1) if L % n == 0 and isprime(n + 1))


def smallest_L(LMAX=10 ** 6):
    """independent sieve of B_E(L) for all L <= LMAX"""
    import numpy as np
    sieve = bytearray([1]) * (LMAX + 2)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= LMAX + 1:
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        i += 1
    tot = np.zeros(LMAX + 1, dtype=np.float64)
    for n in range(4, LMAX + 1):
        if sieve[n + 1]:
            tot[n::n] += 1.0 / n
    cand = [int(L) for L in (tot > 1.0 + 1e-11).nonzero()[0]]
    print(f"  L <= {LMAX} with B_E(L) > 1 (float sieve): {len(cand)}, smallest {cand[0]}")
    # exact re-check of the smallest few and of the 'all divisible by 60' claim
    exact = [(L, BE(L)) for L in cand[:200]]
    bad = [L for L, b in exact if b <= 1]
    print(f"    exact recheck of first 200: {len(bad)} false positives {bad[:5]}")
    print(f"    B_E(55440) = {BE(55440)} = {float(BE(55440)):.6f}, 55440 = 2^4*3^2*5*7*11")
    notdiv60 = [L for L in cand if L % 60]
    print(f"    candidates NOT divisible by 60: {len(notdiv60)} {notdiv60[:10]}")
    # cross-check nothing below 55440 qualifies, exactly
    worst = max((BE(L), L) for L in range(2, 55440))
    print(f"    exact max of B_E over L < 55440: {float(worst[0]):.6f} at L = {worst[1]}")
    return cand


def selfridge360():
    ds = [d for d in range(2, 361) if 360 % d == 0 and isprime(d + 1)]
    print(f"  divisors d>1 of 360 with d+1 prime: {ds}  sum {sum(Fraction(1,d) for d in ds)}")
    ds2 = [d for d in ds if d != 2]
    print(f"    without modulus 2: sum {sum(Fraction(1,d) for d in ds2)} "
          f"= {float(sum(Fraction(1,d) for d in ds2)):.5f} < 1 -> no cover. "
          f"Selfridge's pool needs 0 mod 2.")


if __name__ == "__main__":
    print("== concrete artifacts ==")
    check_H_cert()
    print("== smallest candidate lcm ==")
    smallest_L(int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6)
    print("== Selfridge 360 ==")
    selfridge360()
