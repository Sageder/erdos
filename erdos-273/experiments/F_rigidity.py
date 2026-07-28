"""
F_rigidity.py -- Route F, Erdos 273.

CLAIM TESTED (and PROVED in FINDINGS §5): the ONLY way a family of residue
classes with PAIRWISE DISTINCT moduli > 1 can partition  Z \\ (c mod D)
EXACTLY (pairwise disjoint classes, union exactly the complement of one class)
is the dyadic staircase:
        D = 2^m,   moduli exactly {2,4,8,...,2^m},
        classes  c+2^{j-1} mod 2^j  (j = 1..m).
In particular such a configuration ALWAYS contains the modulus 2.

WHY THIS MATTERS.  The dyadic staircase is exactly the mechanism that drives
sum 1/n_i -> 1 (F_infimum.py).  Since
        E cap {2,4,8,16,...} = {4,16,256,65536}   (Fermat primes minus 1; 2 is
                                                   not in E at all), and
        H cap {2,4,8,16,...} = {2,8,128,32768}    (same Fermat primes),
neither E nor H contains two CONSECUTIVE powers of two.  Hence:
  * in E there is NO exact partition of Z minus one class at all (2 not in E);
  * in H only the trivial one (D = 2, the single class 0 mod 2).
So the cheap-covering mechanism of the unrestricted world is unavailable in E
and essentially unavailable in H.

PART (a) verifies the structure theorem by exhaustive search for all L <= NMAX.
PART (b) prints the powers of two inside E and H.
PART (c) MEASURES min sum 1/n_i when the modulus 2 is FORBIDDEN (all moduli >=3)
         -- the situation faced by the second of the two disjoint H-coverings
         that an E-covering requires.

CONCLUSION: printed; see FINDINGS.md.
"""
import sys, subprocess, os
from fractions import Fraction
from F_mincost import divisors, WORLDS, _is_prime

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "F_mincost")


# ---------------- (a) exhaustive verification of the structure theorem
def exact_partitions_missing_one_class(L, verbose=False):
    """All families of pairwise-disjoint classes with distinct moduli d | L,
    d > 1, whose union is exactly Z_L minus one class c mod D (D | L, D > 1)."""
    ds = [d for d in divisors(L) if d > 1]
    base = {}
    for d in ds:
        m = 0
        for j in range(0, L, d):
            m |= 1 << j
        base[d] = m
    full = (1 << L) - 1
    found = []
    for D in ds:
        for c in range(D):
            target = full & ~(base[D] << c)
            hole = base[D] << c

            def rec(cov, used, chosen):
                if cov == target:
                    found.append((D, c, list(chosen)))
                    return
                t = target & ~cov
                r = (t & -t).bit_length() - 1
                for d in ds:
                    if d in used:
                        continue
                    m = base[d] << (r % d)
                    if m & cov or m & hole:      # must be disjoint & avoid hole
                        continue
                    used.add(d); chosen.append((d, r % d))
                    rec(cov | m, used, chosen)
                    used.discard(d); chosen.pop()
            rec(0, set(), [])
    return found


def check_structure(NMAX):
    bad = []
    tot = 0
    for L in range(2, NMAX + 1):
        for D, c, cl in exact_partitions_missing_one_class(L):
            tot += 1
            mods = sorted(d for d, a in cl)
            m = len(mods)
            ok = (D == 2 ** m) and mods == [2 ** j for j in range(1, m + 1)]
            if not ok:
                bad.append((L, D, c, cl))
    print(f"(a) exhaustive check for all L <= {NMAX}: {tot} exact partitions of "
          f"Z minus one class found; {len(bad)} violate the dyadic-staircase "
          f"structure theorem.")
    if bad:
        for b in bad[:10]:
            print("     COUNTEREXAMPLE", b)
    else:
        print("     -> structure theorem CONFIRMED on this range "
              "(every one is 2,4,...,2^m with D=2^m).")


# ---------------- (b) powers of two in E and H
def powers_of_two():
    e = [2 ** k for k in range(1, 25) if WORLDS["E"](2 ** k)]
    h = [2 ** k for k in range(1, 25) if WORLDS["H"](2 ** k)]
    print(f"(b) powers of 2 in E (n=2^k, n+1 prime), k<=24 : {e}")
    print(f"    powers of 2 in H (m=2^k, 2m+1 prime), k<=24: {h}")
    print("    (both lists are exactly 'Fermat primes'; no two CONSECUTIVE "
          "powers of 2 occur in either, so no dyadic staircase of length >= 2 "
          "exists inside E or H.)")


# ---------------- (c) minimum cost when modulus 2 is forbidden
def min_cost_no2(L, minmod=3, wcap=None, nodecap=0):
    mods = [d for d in divisors(L) if d >= minmod]
    tot = sum(L // d for d in mods)
    if tot < L:
        return None, None, "budget<=1"
    if wcap is None:
        wcap = tot - L
    cmd = [BIN, str(L), str(wcap), str(nodecap)] + [str(d) for d in mods]
    p = subprocess.run(cmd, capture_output=True, text=True)
    last = p.stdout.strip().splitlines()[-1]
    if last.startswith("X="):
        X = int(last.split()[0][2:])
        system = []
        for tok in last.split("system=")[1].split():
            a, n = tok.split("/")
            system.append((int(n), int(a)))
        return X, sorted(system), "OK"
    return None, None, last.split()[0]


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "a"):
        check_structure(int(sys.argv[2]) if len(sys.argv) > 2 else 48)
    if which in ("all", "b"):
        powers_of_two()
    if which in ("all", "c"):
        print("(c) minimum cost with the modulus 2 FORBIDDEN (all moduli >= 3), "
              "moduli dividing L:")
        for L in [12, 24, 36, 48, 60, 72, 96, 108, 144, 180, 192, 216, 288, 324]:
            X, system, st = min_cost_no2(L)
            if st == "OK":
                mu = Fraction(L + X, L)
                print(f"    L={L:<6} X={X:<5} mu={mu}={float(mu):.6f}  "
                      f"k={len(system)}  " +
                      ", ".join(f"{a} mod {n}" for n, a in system), flush=True)
            else:
                print(f"    L={L:<6} {st}", flush=True)
