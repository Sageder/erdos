"""
P2_naive -- a deliberately DUMB, from-scratch, easily auditable exhaustive check of the pivot
on a single lattice L.  Its only purpose is to corroborate the fast C searches (P2_mdfs /
P2_exact2) on the headline lattices without relying on ANY of their reductions.

It contains:
  * NO symmetry normalisation
  * NO dominance rule
  * exactly one prune, the trivial density bound  #uncovered <= sum over unused moduli of L/m,
    which is needed only so that the recursion terminates in reasonable time and is obviously
    valid (a class b mod m covers exactly L/m residues of Z/L).

Moduli are processed in increasing order; for each one, every residue 0..m-1 is tried, plus the
option of not using it.  That enumerates every possible choice of distinct moduli from
S(L) = {m | L : m >= minm, 2m+1 prime} with every possible residue.

usage: python3 P2_naive.py L [minm]
"""
import sys
from sympy import isprime


def divisors(n):
    ds, i = [], 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds)


def run(L, minm=3):
    S = [m for m in divisors(L) if m >= minm and isprime(2 * m + 1)]
    n = len(S)
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + L // S[i]
    print(f"L = {L}  minm = {minm}  |S| = {n}  pool = {S}")
    print(f"budget = {suffix[0]}/{L} = {suffix[0]/L:.6f}")
    if suffix[0] <= L:
        print("INFEASIBLE (budget <= 1)")
        return None
    covered = bytearray(L)
    nodes = [0]
    choice = [None] * n

    def rec(i, u):
        nodes[0] += 1
        if u == 0:
            return True
        if i == n or u > suffix[i]:
            return False
        m = S[i]
        for b in range(m):
            newly = [t for t in range(b, L, m) if not covered[t]]
            for t in newly:
                covered[t] = 1
            choice[i] = b
            if rec(i + 1, u - len(newly)):
                return True
            for t in newly:
                covered[t] = 0
        choice[i] = None
        return rec(i + 1, u)

    ok = rec(0, L)
    if ok:
        cert = [(S[i], choice[i]) for i in range(n) if choice[i] is not None]
        print(f"FEASIBLE, nodes = {nodes[0]}\ncertificate: {cert}")
        chk = bytearray(L)
        for m, b in cert:
            for t in range(b, L, m):
                chk[t] = 1
        assert all(chk) and len(set(m for m, _ in cert)) == len(cert)
        print("certificate re-verified from scratch")
        return cert
    print(f"INFEASIBLE -- exhaustive, no reductions, nodes = {nodes[0]}")
    print(f"SCOPE: this only says no pivot covering has lcm dividing {L}.")
    return None


if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 3)
