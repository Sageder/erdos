"""
H_pair3.py -- Route H: disjoint-pair enumeration with the FULL coprime-subset inequality.

NEW NECESSARY CONDITION (Lemma L8+, proved in FINDINGS.md):
  If A is a covering set and S ⊆ A is PAIRWISE COPRIME, then
        budget(A)  >=  W(S) := sum_{m in S} 1/m  +  prod_{m in S} (1 - 1/m).
  (The S-classes are independent by CRT, so their union has density exactly 1 - prod(1-1/m);
  the rest of A must cover the complement, of density prod(1-1/m).)
  W is monotone increasing under adding a coprime element, so the binding S are the maximal
  pairwise-coprime subsets.  Since every modulus in R(Y) is {2,3,5,7,11}-smooth for the Y we
  handle, a pairwise-coprime subset has at most 5 elements and they are enumerable by
  prime-support mask.  |S|=2 recovers Lemma L8.

  Used as a hard filter: every covering set A ⊆ R(Y) has budget(A) <= kappa, so
  max_S W(S) <= kappa is necessary -- a purely combinatorial condition on the SET.

Everything else is as in H_pair2.py.  CONCLUSION printed per Y.
"""
import sys
from fractions import Fraction
from math import gcd
from sympy import factorint
from H_reduce import H_upto, reduce_set, budget, lcm_of
from H_pair import check_set, prime_powers


def support_mask(m, primes):
    s = 0
    for i, p in enumerate(primes):
        if m % p == 0:
            s |= 1 << i
    return s


def maxW(S, primes):
    """max over pairwise-coprime subsets T of S of  sum 1/m + prod (1-1/m)."""
    if not S:
        return Fraction(0)
    groups = {}
    for m in S:
        groups.setdefault(support_mask(m, primes), []).append(m)
    masks = sorted(groups)
    best = Fraction(0)

    def rec(k, usedmask, ssum, prod):
        nonlocal best
        val = ssum + prod
        if val > best:
            best = val
        if k == len(masks):
            return
        for j in range(k, len(masks)):
            mk = masks[j]
            if mk & usedmask:
                continue
            for m in groups[mk]:
                rec(j + 1, usedmask | mk, ssum + Fraction(1, m), prod * (1 - Fraction(1, m)))

    rec(0, 0, Fraction(0), Fraction(1))
    return best


def analyse(Y, report=6, verbose=True, nodecap=0):
    M0 = H_upto(Y)
    M, _ = reduce_set(M0)
    bM = budget(M)
    kappa = bM - 1
    Delta = kappa - 1
    primes = sorted({p for m in M for p in factorint(m)})
    if verbose:
        print("=" * 78)
        print("Y=%d  |R|=%d  budget(R)=%.9f  kappa=%.9f  Delta=%.9f  primes=%s"
              % (Y, len(M), float(bM), float(kappa), float(Delta), primes))
        sys.stdout.flush()
    if kappa <= 1:
        if verbose:
            print("  budget(R) <= 2 => PROVED: no E-covering with moduli <= %d" % (2 * Y))
        return 0, []
    pps = prime_powers(M)
    Ms = sorted(M)
    n = len(Ms)
    rc = [Fraction(1, m) for m in Ms]
    suf = [Fraction(0)] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + rc[i]
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

    def feasible(i, cnt, sm, mn):
        for pk in pps:
            if cnt[pk] == 0:
                continue
            q = pkprime[pk]
            if pk == q and cnt[pk] + remcnt[pk][i] < q:
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
        if not feasible(i, cA, sA, mA) or not feasible(i, cB, sB, mB):
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
            old = {pk: (c[pk], s[pk], mn.get(pk)) for pk in touched}
            for pk in touched:
                c[pk] += 1; s[pk] += rc[i]
                if pk not in mn:
                    mn[pk] = m
            S.append(m); return old

        def pop(S, c, s, mn, old):
            S.pop()
            for pk in touched:
                c[pk], s[pk], om = old[pk]
                if om is None: mn.pop(pk, None)
                else: mn[pk] = om

        # -> A  (L8+ : max coprime-subset value must stay <= kappa)
        A.append(m)
        ok = maxW(A, primes) <= kappa
        A.pop()
        if ok:
            o = push(A, cA, sA, mA)
            rec(i + 1, A, bA + rc[i], cA, sA, mA, B, bB, cB, sB, mB, True, waste)
            pop(A, cA, sA, mA, o)
        if started:
            B.append(m)
            ok = maxW(B, primes) <= kappa
            B.pop()
            if ok:
                o = push(B, cB, sB, mB)
                rec(i + 1, A, bA, cA, sA, mA, B, bB + rc[i], cB, sB, mB, started, waste)
                pop(B, cB, sB, mB, o)
        rec(i + 1, A, bA, cA, sA, mA, B, bB, cB, sB, mB, started, waste + rc[i])

    z = lambda: {pk: 0 for pk in pps}
    zs = lambda: {pk: Fraction(0) for pk in pps}
    rec(0, [], Fraction(0), z(), zs(), {}, [], Fraction(0), z(), zs(), {}, False, Fraction(0))
    if verbose:
        print("  nodes=%d leaves=%d  surviving disjoint pairs: %d%s"
              % (stats["nodes"], stats["leaves"], len(pairs),
                 "  (NODE CAP -- inconclusive)" if stats["capped"] else ""))
        for (A, B) in pairs[:report]:
            print("     A=%s (%.6f)" % (A, float(budget(A))))
            print("     B=%s (%.6f)" % (B, float(budget(B))))
        if not pairs and not stats["capped"]:
            print("  ==> PROVED: no covering system with distinct moduli all in E and all <= %d"
                  % (2 * Y))
        sys.stdout.flush()
    return len(pairs), pairs


if __name__ == "__main__":
    Ys = [int(x) for x in sys.argv[1:]] or [363, 400, 500]
    for Y in Ys:
        analyse(Y)
