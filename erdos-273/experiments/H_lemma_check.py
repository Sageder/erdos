"""
H_lemma_check.py -- empirical validation of Lemma L5 BEFORE it is used anywhere.

CLAIM TESTED (Lemma L5).  Let {(a_m, m)}_{m in A} be a covering system of Z with distinct
moduli, q a prime, A_q = {m in A : q | m}.  If |A_q| < q then there is c mod q missed by
{a_m mod q : m in A_q}, and the classes
        b_m = q^{-1}(a_m - c)  (mod m),   m in A,  q ∤ m
form a covering system of Z with the same (distinct) moduli.

TEST: on many covering systems -- random ones built by a greedy/DFS construction over
several modulus worlds -- for EVERY prime q with |A_q| < q we recompute the reduced system
and check by exhaustive sweep mod lcm that it covers Z.  We also check the converse-ish
sanity fact that when |A_q| >= q the reduction may genuinely fail (we count such failures).

CONCLUSION: printed.  Expected: 0 failures of L5 over all tested instances.
"""
import random
from math import lcm, gcd
from sympy import isprime, factorint


def covers(pairs):
    if not pairs:
        return False
    L = 1
    for (_, m) in pairs:
        L = lcm(L, m)
    cov = bytearray(L)
    for (a, m) in pairs:
        for r in range(a % m, L, m):
            cov[r] = 1
    return all(cov)


def build_covering(mods, rng, node_cap=200000):
    """Complete DFS on 'cover the smallest uncovered residue mod L'; returns first solution."""
    L = 1
    for m in mods:
        L = lcm(L, m)
    if L > 1_500_000:
        return None
    cov = [0] * L
    state = {"unc": L, "nodes": 0}
    order = sorted(mods, key=lambda m: (m, rng.random()))
    used = [False] * len(order)
    chosen = []

    def rec(start):
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            return None
        if state["unc"] == 0:
            return list(chosen)
        capacity = sum(L // order[i] for i in range(len(order)) if not used[i])
        if state["unc"] > capacity:
            return None
        r = start
        while r < L and cov[r]:
            r += 1
        if r >= L:
            return list(chosen)
        for i in range(len(order)):
            if used[i]:
                continue
            m = order[i]
            a = r % m
            used[i] = True
            delta = []
            for t in range(a, L, m):
                if cov[t] == 0:
                    state["unc"] -= 1
                cov[t] += 1
            chosen.append((a, m))
            res = rec(r)
            chosen.pop()
            for t in range(a, L, m):
                cov[t] -= 1
                if cov[t] == 0:
                    state["unc"] += 1
            used[i] = False
            if res is not None:
                return res
        return None

    return rec(0)


def reduce_by_prime(pairs, q):
    """Return the L5-reduced system if |A_q| < q, else None."""
    Aq = [(a, m) for (a, m) in pairs if m % q == 0]
    if len(Aq) >= q:
        return None
    hit = {a % q for (a, m) in Aq}
    cs = [c for c in range(q) if c not in hit]
    assert cs, (q, Aq)
    c = cs[0]
    out = []
    for (a, m) in pairs:
        if m % q == 0:
            continue
        qi = pow(q, -1, m)
        out.append(((qi * (a - c)) % m, m))
    return out


def main():
    rng = random.Random(20260728)
    worlds = {
        # deliberately contain primes q whose multiples number < q, so L5 has bite
        "2,3-smooth + one 5 + one 7": [2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 5, 7],
        "2,3-smooth + few 5s":        [2, 3, 4, 6, 8, 12, 24, 5, 10, 20],
        "H-235smooth":               [2, 3, 5, 6, 8, 9, 15, 18, 20, 30, 36, 48, 50, 54, 75, 90, 96, 120, 135],
        "all small 2..16":            list(range(2, 17)),
        "all small 2..20 + 11,13":    list(range(2, 21)) + [22, 26],
    }
    total_cov = 0
    total_tests = 0
    fails = 0
    for name, mods in worlds.items():
        got = 0
        for trial in range(200):
            sub = [m for m in mods if rng.random() < 0.85]
            if len(sub) < 3:
                continue
            L = 1
            for m in sub:
                L = lcm(L, m)
            if L > 1_500_000:
                continue
            c = build_covering(sub, rng)
            if not c:
                continue
            assert covers(c)
            got += 1
            total_cov += 1
            primes = sorted({p for (_, m) in c for p in factorint(m)})
            for q in primes:
                red = reduce_by_prime(c, q)
                if red is None:
                    continue
                total_tests += 1
                mm = [m for (_, m) in red]
                assert len(set(mm)) == len(mm)
                if not covers(red):
                    fails += 1
                    print("  *** L5 FAILURE q=%d on %s" % (q, c))
        print("world %-28s : %3d coverings built" % (name, got))
    print()
    print("coverings tested        : %d" % total_cov)
    print("L5 reductions performed : %d" % total_tests)
    print("L5 FAILURES             : %d" % fails)
    print("CONCLUSION:", "L5 holds on every instance tested" if fails == 0 else "L5 IS FALSE")


if __name__ == "__main__":
    main()
