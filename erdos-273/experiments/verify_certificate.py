"""
INDEPENDENT VERIFIER for a claimed answer to Erdos problem 273.

Input: a text file, one congruence per line, "a n"  meaning the class  a (mod n).
Blank lines and lines starting with '#' are ignored.

It re-checks, from scratch and in exact integer arithmetic, EVERY requirement of the problem:

  (1) ADMISSIBILITY: each modulus n satisfies n >= 4 and n+1 is prime, i.e. n = p-1 for a prime
      p >= 5.  Primality is checked by DETERMINISTIC trial division (no probabilistic test), and
      independently cross-checked against sympy.isprime.
  (2) DISTINCTNESS: the moduli are pairwise distinct, and #congruences == #distinct moduli.
  (3) MODULI > 1 and FINITENESS: implied by (1) and by the file being finite.
  (4) COVERAGE of ALL of Z over a FULL period L = lcm(n_i).  Two independent methods:
        (4a) direct sweep of every residue r in {0,...,L-1}   [used when L is small enough];
        (4b) exact class-elimination: the uncovered set is maintained as an explicit finite union
             of residue classes and is shown to be empty.  The intersection of a (mod n) with
             r (mod d) is empty, or a single class mod lcm(n,d); removing it from r (mod d)
             leaves exactly lcm(n,d)/d - 1 classes mod lcm(n,d).  Starting from the single class
             0 (mod 1) = Z and removing every congruence, an empty final list is a rigorous proof
             of coverage of Z (negative integers included: classes are two-sided and the whole
             computation is in Z/L).
      Both methods are run whenever feasible and must agree.

Exit status 0 and "VERDICT: VALID COVERING SYSTEM" only if every check passes.
"""
import sys
from math import gcd, lcm


def is_prime_trial(n):
    """deterministic primality by trial division; exact, no probabilistic step."""
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


def read_cert(path):
    congs = []
    with open(path) as f:
        for line in f:
            line = line.split('#')[0].strip()
            if not line:
                continue
            parts = line.replace(',', ' ').split()
            if len(parts) < 2:
                raise ValueError(f"bad line: {line!r}")
            a, n = int(parts[0]), int(parts[1])
            congs.append((a % n, n))
    return congs


def check_admissible(congs):
    bad = []
    for a, n in congs:
        ok = n >= 4 and is_prime_trial(n + 1)
        try:
            from sympy import isprime
            ok2 = n >= 4 and bool(isprime(n + 1))
            if ok != ok2:
                raise AssertionError(f"primality disagreement at n={n}")
        except ImportError:
            pass
        if not ok:
            bad.append(n)
    return bad


def sweep(congs, L):
    cov = bytearray(L)
    for a, n in congs:
        cov[a % n::n] = b'\x01' * len(range(a % n, L, n))
    return cov.count(0)


def class_elimination(congs, node_cap=40_000_000):
    """exact: maintain the uncovered set as a list of classes (r mod d); returns [] iff covering."""
    unc = [(0, 1)]
    order = sorted(congs, key=lambda t: t[1])
    for a, n in order:
        new = []
        for (r, d) in unc:
            g = gcd(d, n)
            if (a - r) % g != 0:
                new.append((r, d))          # disjoint: nothing removed
                continue
            l = lcm(d, n)
            k = l // d
            if k == 1:
                continue                     # n | d and compatible: class fully removed
            # split r mod d into k classes mod l and drop the one lying in a mod n
            for t in range(k):
                rr = r + t * d
                if (rr - a) % n != 0:
                    new.append((rr, l))
            if len(new) > node_cap:
                raise MemoryError("class list exceeded cap; use the sweep method")
        unc = new
        if not unc:
            return []
    return unc


def main(path, force_sweep_limit=300_000_000):
    congs = read_cert(path)
    print(f"read {len(congs)} congruences from {path}")
    if not congs:
        print("VERDICT: INVALID (empty system)")
        return 1

    bad = check_admissible(congs)
    if bad:
        print(f"VERDICT: INVALID — moduli not of the form p-1 with p>=5 prime: {sorted(set(bad))}")
        return 1
    print(f"(1) admissibility OK: every modulus n has n >= 4 and n+1 prime "
          f"(deterministic trial division)")

    mods = [n for _, n in congs]
    if len(set(mods)) != len(mods):
        from collections import Counter
        dup = [n for n, c in Counter(mods).items() if c > 1]
        print(f"VERDICT: INVALID — repeated moduli: {sorted(dup)}")
        return 1
    print(f"(2) distinctness OK: {len(set(mods))} pairwise distinct moduli, "
          f"min = {min(mods)}, max = {max(mods)}")

    L = 1
    for n in mods:
        L = lcm(L, n)
    print(f"(3) period L = lcm = {L}")
    inv = sum(1 for _ in mods)
    from fractions import Fraction
    s = sum(Fraction(1, n) for n in mods)
    print(f"    sum 1/n_i = {s} = {float(s):.8f}  (must exceed 1)")

    ok_sweep = ok_class = None
    if L <= force_sweep_limit:
        miss = sweep(congs, L)
        ok_sweep = (miss == 0)
        print(f"(4a) full mod-L sweep of all {L} residues: uncovered = {miss}  -> "
              f"{'OK' if ok_sweep else 'FAIL'}")
    else:
        print(f"(4a) full sweep skipped (L = {L} exceeds the sweep limit)")
    try:
        left = class_elimination(congs)
        ok_class = (len(left) == 0)
        print(f"(4b) exact class-elimination: uncovered classes remaining = {len(left)}  -> "
              f"{'OK' if ok_class else 'FAIL'}")
        if left[:5]:
            print("     e.g.", left[:5])
    except MemoryError as e:
        print(f"(4b) class-elimination aborted: {e}")

    checks = [c for c in (ok_sweep, ok_class) if c is not None]
    if checks and all(checks):
        print("VERDICT: VALID COVERING SYSTEM with all moduli of the form p-1, p >= 5 prime.")
        return 0
    print("VERDICT: INVALID (coverage check failed or could not be completed)")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
