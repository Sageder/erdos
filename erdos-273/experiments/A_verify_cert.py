"""
A_verify_cert.py

CLAIM TESTED: a certificate produced by A_sat_cover.py really is what it claims to be.

This script shares NO code with the search: it re-derives everything from scratch using
sympy's isprime and a plain integer sieve over Z/L.  It checks

  (1) primality of n+1 for every modulus n   (world E)   /  of 2m+1  (world H);
  (2) all moduli >= 4 (resp. >= 2) and PAIRWISE DISTINCT;
  (3) every modulus divides L, and lcm(moduli) is reported;
  (4) exhaustive mod-L sweep in exact integer arithmetic:
        mode full    : every r in [0,L) lies in some chosen class;
        mode relaxed : r = 0 lies in NO chosen class and every r in [1,L) lies in some.
  (5) additionally, for a full E-world certificate, it re-checks the equivalent
      statement "the union of the classes equals Z" by testing the window
      [-3L, 4L) directly (a redundant but independent re-derivation of periodicity).

Usage:  python3 A_verify_cert.py <cert.json> [<cert.json> ...]
        python3 A_verify_cert.py --inline L world mode "n1:a1,n2:a2,..."

CONCLUSION: prints PASS / FAIL for each certificate.
"""
import json, sys
from sympy import isprime
from math import gcd


def lcm_all(xs):
    L = 1
    for x in xs:
        L = L * x // gcd(L, x)
    return L


def check(L, world, mode, classes, verbose=True):
    ok = True

    def bad(msg):
        nonlocal ok
        ok = False
        print("   FAIL:", msg)

    mods = [n for n, a in classes]
    if len(set(mods)) != len(mods):
        bad("moduli are not pairwise distinct")
    for n, a in classes:
        if world == "E":
            if n < 4:
                bad(f"modulus {n} < 4")
            if not isprime(n + 1):
                bad(f"{n}+1 = {n+1} is not prime, so {n} is not of the form p-1, p>=5")
        else:
            if n < 2:
                bad(f"modulus {n} < 2")
            if not isprime(2 * n + 1):
                bad(f"2*{n}+1 = {2*n+1} is not prime")
        if L % n:
            bad(f"modulus {n} does not divide L={L}")
    Lc = lcm_all(mods) if mods else 1
    if verbose:
        print(f"   {len(classes)} classes, moduli distinct, lcm = {Lc}, L = {L}, "
              f"L % lcm = {L % Lc}")
        print(f"   sum of reciprocals = {sum(1.0/n for n,_ in classes):.6f}")

    cov = bytearray(L)
    for n, a in classes:
        a %= n
        for r in range(a, L, n):
            cov[r] = 1
    unc = [r for r in range(L) if not cov[r]]
    if mode == "full":
        if unc:
            bad(f"{len(unc)} uncovered residues mod L, first ones {unc[:8]}")
        elif verbose:
            print("   mod-L sweep: every residue covered")
    else:
        if unc != [0]:
            bad(f"relaxed mode: uncovered set is {unc[:8]}"
                f"{'...' if len(unc)>8 else ''} (size {len(unc)}), expected exactly [0]")
        elif verbose:
            print("   mod-L sweep: uncovered set is exactly {0}")

    if mode == "full" and ok:
        # independent re-derivation on a raw integer window (no periodicity assumed)
        lo, hi = -3 * L, 4 * L
        seen = bytearray(hi - lo)
        for n, a in classes:
            start = a % n
            # first element of the class >= lo
            t = lo + ((start - lo) % n)
            for x in range(t, hi, n):
                seen[x - lo] = 1
        miss = [x + lo for x, v in enumerate(seen) if not v]
        if miss:
            bad(f"window [-3L,4L) has uncovered integers, e.g. {miss[:8]}")
        elif verbose:
            print(f"   raw window [{lo},{hi}) fully covered "
                  f"({hi-lo} integers checked, no periodicity assumed)")
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--inline":
        L, world, mode, spec = int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
        classes = [tuple(int(t) for t in p.split(":")) for p in spec.split(",") if p]
        print(f"inline certificate L={L} world={world} mode={mode}")
        print("VERDICT:", "PASS" if check(L, world, mode, classes) else "FAIL")
    else:
        allok = True
        for fn in sys.argv[1:]:
            d = json.load(open(fn))
            print(f"--- {fn}: L={d['L']} world={d['world']} mode={d['mode']} "
                  f"verdict={d['verdict']}")
            if "classes" not in d:
                print("   (no classes: nothing to verify)")
                continue
            r = check(d["L"], d["world"], d["mode"],
                      [tuple(c) for c in d["classes"]])
            allok &= r
            print("   VERDICT:", "PASS" if r else "FAIL")
        sys.exit(0 if allok else 1)
