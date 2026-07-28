"""
INDEPENDENT AUDIT of route H's Lemma L5 (prime removal) and Theorem T2 (no E-covering with all
moduli <= 254).  Written from scratch; imports no H_ code.

LEMMA L5 (re-derived).  Let A be the modulus set of a covering system of Z, q a prime, and
A_q = {m in A : q | m}.  If |A_q| < q then A \\ A_q is again the modulus set of a covering system.
  Proof.  The residues a_m mod q for m in A_q number at most |A_q| < q, so some c in Z/q is not
  among them.  Every x = c (mod q) therefore fails every class with q | m (such a class forces
  x = a_m mod q).  Hence the classes with q not dividing m already cover the whole class c mod q.
  Substituting x = c + q y and using gcd(q, m) = 1, the class a_m (mod m) becomes a single class
  mod m in the variable y.  So those moduli cover Z.  []
  The moduli are UNCHANGED (m, not m/q), so the reduced set is a subset of the original.

CONSEQUENCE.  Define R(M) by iteratively deleting, from M, all multiples of any prime q with
#{m in M : q | m} < q.  Then M contains a covering set iff R(M) does; and M contains two DISJOINT
covering sets iff R(M) does (if #{m in M : q | m} < q then a fortiori #{m in A : q | m} < q for
each of the two, and the reduced sets stay disjoint).

THEOREM T2.  By the parity split, an E-covering with all moduli <= X corresponds to two disjoint
covering sets inside H cap [2, X/2], each of reciprocal sum > 1 (strictly, by DMNR).  So
budget(R(H cap [2, Y])) > 2 is necessary.  Route H reports this fails for Y = 127 and first holds
at Y = 128, giving: no E-covering has all moduli <= 254.

CONCLUSION: printed.
"""
from fractions import Fraction
from sympy import isprime, primerange, factorint
import random
from math import lcm, gcd


def H_upto(Y):
    return [m for m in range(2, Y + 1) if isprime(2 * m + 1)]


def reduce_pool(M, verbose=False):
    """iteratively delete multiples of any prime q with #{m in M : q | m} < q."""
    M = sorted(set(M))
    changed = True
    while changed:
        changed = False
        primes = sorted({p for m in M for p in factorint(m)})
        for q in primes:
            mult = [m for m in M if m % q == 0]
            if 0 < len(mult) < q:
                if verbose:
                    print(f"    delete {len(mult)} multiples of {q}: {mult}")
                M = [m for m in M if m % q != 0]
                changed = True
                break
    return M


def test_L5(trials=400, seed=20260728):
    """Stress Lemma L5.  NOTE: for an IRREDUNDANT covering, q | some modulus forces |A_q| >= q
    (route D's minimality lemma), so L5's hypothesis is vacuous there -- a naive random test finds
    no instances.  We therefore CONSTRUCT instances by adjoining redundant classes whose moduli are
    divisible by a fresh prime q, which is exactly the situation L5 is designed for."""
    rng = random.Random(seed)
    tested = 0
    for _ in range(trials):
        L = rng.choice([12, 24, 36, 48, 60, 72, 120, 180, 240, 360])
        divs = [d for d in range(2, L + 1) if L % d == 0]
        rng.shuffle(divs)
        chosen, cov = [], bytearray(L)
        for d in divs:
            a = rng.randrange(d)
            chosen.append((a, d))
            for r in range(a, L, d):
                cov[r] = 1
            if all(cov):
                break
        if not all(cov):
            continue
        # adjoin redundant classes with moduli divisible by a fresh prime q0 (< q0 of them)
        q0 = rng.choice([5, 7, 11, 13])
        extra = []
        base = [d for _, d in chosen]
        for t in range(rng.randint(1, q0 - 1)):
            d = q0 * rng.choice(base)
            if d not in base and d not in [e for _, e in extra]:
                extra.append((rng.randrange(d), d))
        chosen = chosen + extra
        A = [d for _, d in chosen]
        for q in sorted({p for d in A for p in factorint(d)}):
            Aq = [d for d in A if d % q == 0]
            if len(Aq) >= q:
                continue
            rest = [(a, d) for (a, d) in chosen if d % q != 0]
            if not rest:
                continue
            # L5 asserts: the remaining moduli cover Z (possibly with different residues,
            # but in fact with the SAME residues after the substitution).  Verify directly:
            # some c mod q is missed by {a_m mod q : q | m}; check the rest covers c + qZ.
            missed = [c for c in range(q) if all(a % q != c for (a, d) in chosen if d % q == 0)]
            assert missed, (q, "L5 hypothesis says a residue must be missed")
            c = missed[0]
            LL = 1
            for _, d in rest:
                LL = lcm(LL, d)
            LL = lcm(LL, q)
            bad = [x for x in range(c, LL * q + c, q)
                   if not any((x - a) % d == 0 for (a, d) in rest)]
            assert not bad, ("L5 FAILED", q, c, bad[:5], chosen)
            tested += 1
    return tested


if __name__ == "__main__":
    print("Stress-testing Lemma L5 on genuine covering systems ...")
    n = test_L5()
    print(f"  {n} (covering system, prime q with |A_q| < q) instances: Lemma L5 held every time.\n")

    print("Reducing H ∩ [2,Y] and computing budgets:")
    for Y in [100, 127, 128, 200, 300, 362, 363, 500]:
        M = H_upto(Y)
        R = reduce_pool(M)
        b = sum(Fraction(1, m) for m in R)
        flag = "  <= 2  -> NO pair of disjoint covering sets" if b <= 2 else "  > 2"
        print(f"  Y = {Y:<4} |H| = {len(M):3d}  |R| = {len(R):3d}  budget(R) = {float(b):.6f}{flag}")
        if Y == 127:
            print(f"       R(127) = {R}")
            print(f"       exact budget = {b}")
            assert b <= 2, "T2 would fail"
        if Y == 128:
            assert b > 2

    Y = 127
    R = reduce_pool(H_upto(Y))
    b = sum(Fraction(1, m) for m in R)
    print(f"\nTHEOREM T2 re-derived: budget(R(H ∩ [2,127])) = {b} = {float(b):.8f} <= 2.")
    print("Since an E-covering with all moduli <= 254 needs two DISJOINT covering subsets of")
    print("H ∩ [2,127], each of reciprocal sum > 1 strictly (DMNR), their total would exceed 2.")
    print("=> NO covering system with distinct moduli all in E and all <= 254.  CONFIRMED.")
    print("\n(PROMPT.md's stated bound was only 'uses a modulus >= 70'.)")
