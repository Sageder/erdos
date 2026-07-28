"""
H_pair2.py -- Route H:  same exhaustive disjoint-pair enumeration as H_pair.py, but with
INCREMENTAL pruning so that much larger Y can be reached.

CLAIM TESTED: identical to H_pair.py -- for a given Y, is there a disjoint pair A,B ⊆ R(Y)
passing every proved necessary condition?  Empty  =>  no E-covering with all moduli <= 2Y.

Incremental prunes (each is implied by the corresponding leaf condition of H_pair.check_set,
so pruning is sound):
   * waste:  budget(A)+budget(B) > 2, so the unused budget is < Delta = budget(R)-2.
   * L8 (coprime pairs) checked at insertion time.
   * L5 multiplicity: if a set already owns a multiple of q and cannot reach q of them with
     the multiples still to come, prune.
   * L10b: moduli are processed in INCREASING order, so the first multiple of q^t placed in a
     set is min(D_t); afterwards budget(D_t) can only grow by the multiples still to come, and
     the leaf condition demands budget(D_t) >= q*(1/min(D_t) - delta) >= q*(1/min - Delta).
Final acceptance uses the full H_pair.check_set (incl. the Fourier-balance condition).

CONCLUSION: printed per Y.
"""
import sys
from fractions import Fraction
from math import gcd
from sympy import factorint
from H_reduce import H_upto, reduce_set, budget, lcm_of
from H_pair import check_set, prime_powers


def analyse(Y, report=8, verbose=True, nodecap=0):
    M0 = H_upto(Y)
    M, _ = reduce_set(M0)
    bM = budget(M)
    kappa = bM - 1
    Delta = kappa - 1
    if verbose:
        print("=" * 78)
        print("Y=%d  |R|=%d  budget(R)=%.9f  Delta=%.9f  1/Delta=%s  lcm=%d"
              % (Y, len(M), float(bM), float(Delta),
                 ("%.3f" % float(1 / Delta)) if Delta > 0 else "inf", lcm_of(M)))
        sys.stdout.flush()
    if kappa <= 1:
        if verbose:
            print("  budget(R) <= 2 => no disjoint pair.  PROVED: no E-covering, moduli <= %d" % (2 * Y))
        return 0, [], 0
    primes = sorted({p for m in M for p in factorint(m)})
    pps = prime_powers(M)
    Ms = sorted(M)                      # increasing modulus = decreasing 1/m
    n = len(Ms)
    rc = [Fraction(1, m) for m in Ms]
    suf = [Fraction(0)] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + rc[i]
    # per prime power: remaining count and remaining reciprocal-sum from index i
    remcnt = {pk: [0] * (n + 1) for pk in pps}
    remsum = {pk: [Fraction(0)] * (n + 1) for pk in pps}
    for pk in pps:
        for i in range(n - 1, -1, -1):
            hit = (Ms[i] % pk == 0)
            remcnt[pk][i] = remcnt[pk][i + 1] + (1 if hit else 0)
            remsum[pk][i] = remsum[pk][i + 1] + (rc[i] if hit else Fraction(0))
    pkprime = {pk: min(factorint(pk)) for pk in pps}

    pairs = []
    stats = {"nodes": 0, "leaves": 0, "capped": False}

    # state per side: list of moduli, budget, per-pk (count, sum, min)
    def feasible_side(i, S, cnt, sm, mn):
        for pk in pps:
            c = cnt[pk]
            if c == 0:
                continue
            q = pkprime[pk]
            if pk == q and c + remcnt[pk][i] < q:
                return False
            if sm[pk] + remsum[pk][i] < q * (Fraction(1, mn[pk]) - Delta):
                return False
        return True

    def rec(i, A, bA, cA, sA, mA, B, bB, cB, sB, mB, started, waste):
        stats["nodes"] += 1
        if nodecap and stats["nodes"] > nodecap:
            stats["capped"] = True
            return
        if bA > kappa or bB > kappa or waste >= Delta:
            return
        if bA + suf[i] <= 1 or bB + suf[i] <= 1:
            return
        if not feasible_side(i, A, cA, sA, mA) or not feasible_side(i, B, cB, sB, mB):
            return
        if i == n:
            stats["leaves"] += 1
            if bA > 1 and bB > 1:
                if check_set(sorted(A), Delta, primes, pps) and check_set(sorted(B), Delta, primes, pps):
                    pairs.append((sorted(A), sorted(B)))
            return
        m = Ms[i]
        touched = [pk for pk in pps if m % pk == 0]

        def push(S, c, s, mn):
            old = {}
            for pk in touched:
                old[pk] = (c[pk], s[pk], mn.get(pk))
                c[pk] += 1
                s[pk] += rc[i]
                if pk not in mn:
                    mn[pk] = m
            S.append(m)
            return old

        def pop(S, c, s, mn, old):
            S.pop()
            for pk in touched:
                c[pk], s[pk], om = old[pk]
                if om is None:
                    mn.pop(pk, None)
                else:
                    mn[pk] = om

        # -> A
        if all(gcd(m, y) != 1 or Fraction(1, m * y) <= Delta for y in A):
            old = push(A, cA, sA, mA)
            rec(i + 1, A, bA + rc[i], cA, sA, mA, B, bB, cB, sB, mB, True, waste)
            pop(A, cA, sA, mA, old)
        # -> B
        if started and all(gcd(m, y) != 1 or Fraction(1, m * y) <= Delta for y in B):
            old = push(B, cB, sB, mB)
            rec(i + 1, A, bA, cA, sA, mA, B, bB + rc[i], cB, sB, mB, started, waste)
            pop(B, cB, sB, mB, old)
        # unused
        rec(i + 1, A, bA, cA, sA, mA, B, bB, cB, sB, mB, started, waste + rc[i])

    z = lambda: {pk: 0 for pk in pps}
    zs = lambda: {pk: Fraction(0) for pk in pps}
    rec(0, [], Fraction(0), z(), zs(), {}, [], Fraction(0), z(), zs(), {}, False, Fraction(0))
    if verbose:
        print("  nodes=%d leaves=%d  surviving disjoint pairs: %d%s"
              % (stats["nodes"], stats["leaves"], len(pairs),
                 "  (NODE CAP HIT -- inconclusive)" if stats["capped"] else ""))
        for (A, B) in pairs[:report]:
            print("     A=%s (%.6f)" % (A, float(budget(A))))
            print("     B=%s (%.6f)" % (B, float(budget(B))))
        if len(pairs) > report:
            print("     ... %d more" % (len(pairs) - report))
        if not pairs and not stats["capped"]:
            print("  ==> PROVED: no covering system with distinct moduli all in E and all <= %d"
                  % (2 * Y))
        sys.stdout.flush()
    return len(pairs), pairs, stats["nodes"]


if __name__ == "__main__":
    Ys = [int(x) for x in sys.argv[1:]] or [300, 350, 400, 450, 500]
    for Y in Ys:
        analyse(Y)
