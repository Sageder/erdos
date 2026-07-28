"""
ADVERSARIAL AUDIT 6: the rigidity theorem.

Claim: if residue classes with PAIRWISE DISTINCT moduli > 1 partition Z \ (c mod D) exactly,
then D = 2^m and the moduli are exactly 2,4,...,2^m.

Exhaustive test.  Work mod P.  The target set is T = {x : x mod D != 0} (c = 0 WLOG by
translation).  DFS: take the smallest element of T not yet covered; every modulus m still
available must, if used to cover it, use the class x mod m -- so the residue is FORCED.  Try
each available modulus, require the whole class to lie inside T and be disjoint from what is
already placed.  This enumerates ALL exact partitions with distinct moduli, with no residue
blow-up.
"""
import sys
from fractions import Fraction
from math import gcd


def search_for_P(P, verbose=False):
    out = []
    divs = [d for d in range(2, P + 1) if P % d == 0]
    for D in divs:
        target = bytearray(1 if x % D else 0 for x in range(P))
        need = sum(target)
        avail = [m for m in divs if m != 0]
        sols = []

        def dfs(hit, count, used):
            if count == need:
                if lcmset(used + [D]) == P:
                    sols.append(tuple(sorted(used)))
                return
            x = next(i for i in range(P) if target[i] and not hit[i])
            for m in avail:
                if m in used:
                    continue
                a = x % m
                cls = list(range(a, P, m))
                if any((not target[t]) or hit[t] for t in cls):
                    continue
                for t in cls:
                    hit[t] = 1
                used.append(m)
                dfs(hit, count + len(cls), used)
                used.pop()
                for t in cls:
                    hit[t] = 0

        def lcmset(xs):
            L = 1
            for x in xs:
                L = L * x // gcd(L, x)
            return L

        if need == 0:
            continue
        dfs(bytearray(P), 0, [])
        for s in set(sols):
            out.append((D, s))
    return out


def dyadic(D, M):
    if D & (D - 1):
        return False
    m = D.bit_length() - 1
    return tuple(sorted(M)) == tuple(2 ** i for i in range(1, m + 1))


if __name__ == "__main__":
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    allf, bad = [], []
    for P in range(2, PMAX + 1):
        f = search_for_P(P)
        for D, M in f:
            allf.append((P, D, M))
            if not dyadic(D, M):
                bad.append((P, D, M))
    seen = set()
    for P, D, M in allf:
        if (D, M) not in seen:
            seen.add((D, M))
            print(f"  P={P:<5} D={D:<5} moduli {M}")
    print(f"\nexhaustive over P <= {PMAX}: {len(allf)} exact partitions of Z \\ (0 mod D) by "
          f"distinct moduli > 1")
    print(f"NON-DYADIC: {len(bad)}   {bad[:10]}")
    print("\nboundary: D=1 gives an empty complement (empty family, m=0); D=2 gives {2}.")
