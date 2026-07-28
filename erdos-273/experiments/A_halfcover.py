"""
A_halfcover.py

CLAIM TESTED / ESTABLISHED: half of Erdos 273 is easy.  There IS a finite family of residue
classes with DISTINCT moduli, all of the form p-1 with p >= 5 prime, whose union is
exactly the set of all EVEN integers -- and, by translating by 1, another whose union is
exactly the set of all ODD integers.

What the problem actually asks for is BOTH at once with the two modulus sets DISJOINT
(Lemma A1).  This script exhibits the even-half family, verifies it from scratch, and then
reports the disjointness obstruction quantitatively.

CONCLUSION: printed; the family below is verified exhaustively over a raw integer window.
"""
import sys, os
from sympy import isprime
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# from the H-world certificate at Lh = 180 (A_sat_cover.py, world H, mode full)
H_CERT = [(2, 0), (3, 2), (5, 0), (6, 3), (9, 7), (15, 4), (18, 1), (20, 7),
          (30, 1), (36, 13), (90, 13)]

if __name__ == "__main__":
    even = [(2 * m, 2 * b % (2 * m)) for m, b in H_CERT]
    odd = [(n, (a + 1) % n) for n, a in even]
    for name, fam, par in [("EVEN", even, 0), ("ODD", odd, 1)]:
        mods = [n for n, _ in fam]
        assert len(set(mods)) == len(mods)
        assert all(isprime(n + 1) and n >= 4 for n in mods), mods
        print(f"{name} family: {len(fam)} classes")
        print(f"   moduli {mods}")
        print(f"   n+1 primes {[n+1 for n in mods]}")
        print(f"   classes {fam}")
        print(f"   sum 1/n = {float(sum(Fraction(1,n) for n in mods)):.6f}")
        lo, hi = -4000, 4000
        miss = []
        for x in range(lo, hi):
            if x % 2 != par:
                continue
            if not any((x - a) % n == 0 for n, a in fam):
                miss.append(x)
        print(f"   every integer of parity {par} in [{lo},{hi}) covered: "
              f"{'YES' if not miss else 'NO ' + str(miss[:5])}")
        # and it covers NOTHING of the other parity, automatically:
        wrong = [x for x in range(lo, hi) if x % 2 != par
                 and any((x - a) % n == 0 for n, a in fam)]
        print(f"   covers no integer of the other parity: "
              f"{'YES' if not wrong else 'NO'}")
    print()
    print("The two families above use the SAME 11 moduli, which is exactly what the")
    print("problem forbids.  Erdos 273 asks for two such families with DISJOINT modulus")
    print("sets -- see Lemma A1 and the budget arithmetic in the report.")
