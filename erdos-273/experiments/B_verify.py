"""
B_verify.py -- Route B: independent, from-scratch, exhaustive verification of a certificate.

CLAIM TESTED
------------
Given a list of pairs (n_i, a_i), verify EXACTLY and EXHAUSTIVELY that

  (1) every modulus n_i lies in E, i.e. n_i >= 4 and n_i + 1 is prime  (primality re-proved
      here by deterministic trial division, NOT by sympy);
  (2) the moduli are pairwise distinct;
  (3) the union of the classes a_i (mod n_i) contains the target set:
        --target all   : all of Z            (sweep of Z/L, L = lcm n_i)
        --target even  : all even integers   (sweep of the even residues of Z/L)
        --target odd   : all odd integers.
  Because the union of the classes is periodic mod L = lcm(n_i), the sweep of one period is a
  complete proof.

Nothing in this file is shared with the search code: primality, lcm, and the sweep are all
recomputed from scratch.

usage: python3 B_verify.py cert.json [--target all|even|odd]
   cert.json = {"moduli": [[n, a], ...]}
"""
import json, sys
from math import gcd


def is_prime_trial(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def main():
    path = sys.argv[1]
    target = "all"
    if "--target" in sys.argv:
        target = sys.argv[sys.argv.index("--target") + 1]
    obj = json.load(open(path))
    pairs = [(int(n), int(a)) for n, a in obj["moduli"]]

    print(f"certificate: {len(pairs)} classes, target = {target}")
    # (1) membership in E
    bad = [n for n, _ in pairs if n < 4 or not is_prime_trial(n + 1)]
    assert not bad, f"moduli not in E: {bad}"
    print(f"  (1) every modulus n has n>=4 and n+1 prime (trial division)          OK")
    print(f"      moduli = {sorted(n for n, _ in pairs)}")
    print(f"      n+1    = {sorted(n+1 for n, _ in pairs)}")
    # (2) distinctness
    ms = [n for n, _ in pairs]
    assert len(set(ms)) == len(ms), "moduli not distinct"
    print(f"  (2) moduli pairwise distinct                                          OK")
    # (3) exhaustive sweep of one period
    L = 1
    for n, _ in pairs:
        L = L * n // gcd(L, n)
    print(f"  (3) L = lcm = {L}")
    cov = bytearray(L)
    for n, a in pairs:
        r = a % n
        cov[r::n] = b"\x01" * len(range(r, L, n))
    if target == "all":
        miss = [x for x in range(L) if not cov[x]]
    elif target == "even":
        miss = [x for x in range(0, L, 2) if not cov[x]]
    else:
        miss = [x for x in range(1, L, 2) if not cov[x]]
    print(f"      uncovered residues in the target set: {len(miss)}"
          + (f"   first few: {miss[:10]}" if miss else ""))
    print(f"      reciprocal sum = {sum(1 / n for n, _ in pairs):.6f}")
    print("RESULT:", "VERIFIED COVERING of " + target if not miss else "NOT A COVERING")


if __name__ == "__main__":
    main()
