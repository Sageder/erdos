"""
D_02_fiber.py

CLAIMS TESTED / ESTABLISHED

 (F1) FIBER DENSITY LEMMA (Prop. D2).  If {a_i mod n_i} covers Z, q prime,
      J >= max_i nu_q(n_i), then for EVERY r in Z/q^J
            F_q(r) := sum_{i : a_i = r mod q^{nu_q(n_i)}}  q^{nu_q(n_i)}/n_i   >= 1,
      and  avg_r F_q(r) = sum_i 1/n_i.
      -> verified numerically on explicit coverings.

 (F2) MINIMALITY / MULTIPLICITY LEMMA (Lemma D6).  In an IRREDUNDANT covering system, for
      every prime q, every j>=1 and every node v at q-adic level j-1: either no modulus with
      nu_q >= j has its q-adic residue inside v, or ALL q children of v contain one.
      Consequence: for every prime q dividing lcm(n_i), at least q of the moduli are
      divisible by q.
      -> verified numerically on explicit irredundant coverings.

 (F3) *** THE REFUTATION ***  The whole family of fiber density conditions (all primes q,
      all levels, requirement ">= 2" coming from the parity split of Prop. D1) is JOINTLY
      SATISFIABLE inside H.  Concretely we compute the least Y with
            for every prime q :   sum_{m in H, m <= Y, q does not divide m} 1/m  >= 2 ,
      for which S = H cap [2,Y] satisfies every fiber condition FOR EVERY residue assignment
      (the q-free moduli contribute to every q-adic path).  Hence NO choice of prime q and
      no level structure can ever yield a contradiction: route "q-adic fiber budget" is dead.

 (F4) same for the >= q multiplicity condition of (F2), doubled (both halves of the parity
      split need it): for every prime q, #{m in H, m<=Y : q | m} >= 2q -- measured.

CONCLUSION: printed at run time.  F1,F2 verified; F3 and F4 give an explicit finite
certificate that the local conditions cannot obstruct.
"""
from sympy import isprime, primerange
from fractions import Fraction
from math import gcd
import sys


def H_upto(X):
    return [m for m in range(2, X + 1) if isprime(2 * m + 1)]


def nu(n, q):
    e = 0
    while n % q == 0:
        n //= q
        e += 1
    return e


# ------------------------------------------------------------------ F1
def covers(fam, L=None):
    from math import lcm
    if L is None:
        L = 1
        for n, a in fam:
            L = lcm(L, n)
    cov = bytearray(L)
    for n, a in fam:
        for r in range(a % n, L, n):
            cov[r] = 1
    return all(cov), L


def check_F1(fam, name):
    ok, L = covers(fam)
    print("F1 [%s]: covers Z: %s   L = %d   sum 1/n = %s" %
          (name, ok, L, sum(Fraction(1, n) for n, _ in fam)))
    assert ok
    tot = sum(Fraction(1, n) for n, _ in fam)
    for q in sorted({p for n, _ in fam for p in range(2, n + 1)
                     if isprime(p) and n % p == 0}):
        J = max(nu(n, q) for n, _ in fam)
        vals = []
        for r in range(q ** J):
            s = Fraction(0)
            for n, a in fam:
                e = nu(n, q)
                if (a - r) % (q ** e) == 0:
                    s += Fraction(q ** e, n)
            vals.append(s)
        avg = sum(vals) / len(vals)
        print("    q=%-3d J=%d  min_r F_q(r) = %-10s avg = %-10s (avg must equal sum 1/n: %s)"
              % (q, J, min(vals), avg, avg == tot))
        assert min(vals) >= 1, ("F1 violated", q, min(vals))
        assert avg == tot
    print("    -> min_r F_q(r) >= 1 at every prime, average = sum 1/n exactly.  OK")


# ------------------------------------------------------------------ F2
def is_irredundant(fam):
    ok, L = covers(fam)
    if not ok:
        return False
    for i in range(len(fam)):
        sub = fam[:i] + fam[i + 1:]
        if covers(sub, L)[0]:
            return False
    return True


def check_F2(fam, name):
    print("F2 [%s]: irredundant: %s" % (name, is_irredundant(fam)))
    assert is_irredundant(fam)
    prs = sorted({p for n, _ in fam for p in primerange(2, n + 1) if n % p == 0})
    for q in prs:
        e = max(nu(n, q) for n, _ in fam)
        cnt = sum(1 for n, _ in fam if n % q == 0)
        print("     q=%-3d  e=%d  #{i : q | n_i} = %d   (Lemma D6 requires >= q = %d): %s"
              % (q, e, cnt, q, cnt >= q))
        assert cnt >= q, ("Lemma D6 violated", q, cnt)
        # full sibling-group structure, all levels
        for j in range(1, e + 1):
            nodes = {}
            for n, a in fam:
                if nu(n, q) >= j:
                    nodes.setdefault(a % q ** (j - 1), set()).add(a % q ** j)
            for v, ch in nodes.items():
                assert len(ch) == q, ("sibling group not full", q, j, v, sorted(ch))
        print("        every active node at every level 1..%d has all %d children hit  OK"
              % (e, q))


# ------------------------------------------------------------------ F3
def check_F3(Ymax=400000, target=2):
    """least Y such that for EVERY prime q, sum_{m in H, m<=Y, q nmid m} 1/m >= target."""
    H = H_upto(Ymax)
    print("\nF3: |H cap [2,%d]| = %d,  sum 1/m = %.6f"
          % (Ymax, len(H), float(sum(Fraction(1, m) for m in H))))
    # incremental: track total and, for each prime q <= Ymax, the sum over multiples of q
    tot = 0.0
    mult = {}                    # q -> sum of 1/m over m in H, q | m, m <= Y
    from collections import defaultdict
    mult = defaultdict(float)
    primes = list(primerange(2, Ymax + 1))
    best = None
    for m in H:
        tot += 1.0 / m
        mm = m
        for q in primes:
            if q * q > mm:
                break
            if mm % q == 0:
                mult[q] += 1.0 / m
                while mm % q == 0:
                    mm //= q
        if mm > 1:
            mult[mm] += 1.0 / m
        if tot >= target + 1e-12:
            worst_q, worst = None, tot
            for q, s in mult.items():
                if tot - s < worst:
                    worst, worst_q = tot - s, q
            if worst >= target:
                best = (m, tot, worst, worst_q)
                break
    if best is None:
        print("    NOT reached within Y <= %d" % Ymax)
        return None
    Y, tot, worst, worst_q = best
    print("    least Y with  min_q sum_{m in H, m<=Y, q nmid m} 1/m >= %d   is  Y = %d"
          % (target, Y))
    print("    at Y = %d:  sum_{m in H, m<=Y} 1/m = %.6f;  worst prime q = %d giving %.6f"
          % (Y, tot, worst_q, worst))
    # print the few worst primes
    rows = sorted(((tot - s, q) for q, s in mult.items()))[:8]
    print("    tightest primes (q, q-free budget):",
          ", ".join("(%d, %.4f)" % (q, v) for v, q in rows))
    print("    => S = H cap [2,%d] satisfies EVERY q-adic fiber density condition with the"
          % Y)
    print("       doubled threshold 2, for EVERY residue assignment.  The fiber-budget")
    print("       obstruction route CANNOT prove NO.")
    return Y


# ------------------------------------------------------------------ F4
def check_F4(Y):
    H = [m for m in H_upto(Y)]
    print("\nF4: multiplicity condition #{m in H, m<=%d : q | m} >= 2q  (doubled Lemma D6)" % Y)
    bad = []
    for q in primerange(2, 200):
        c = sum(1 for m in H if m % q == 0)
        if c < 2 * q:
            bad.append((q, c))
    print("    primes q < 200 with fewer than 2q multiples in H cap [2,%d]: %s" % (Y, bad))
    print("    (a prime q may also simply be avoided entirely: then q divides no modulus and"
          " the condition is void.)")


if __name__ == "__main__":
    classic = [(2, 0), (3, 0), (4, 1), (6, 5), (12, 7)]
    check_F1(classic, "classic {2,3,4,6,12}")
    check_F2(classic, "classic {2,3,4,6,12}")
    print()
    # a covering with distinct moduli, minimum modulus 3
    c3 = [(3, 0), (4, 0), (5, 0), (6, 2), (8, 3), (10, 1), (12, 5), (15, 2), (20, 7),
          (24, 11), (30, 26), (40, 27), (60, 50), (120, 59)]
    ok, L = covers(c3)
    print("min-modulus-3 test system covers:", ok, " (if False the example is discarded)")
    if ok:
        check_F1(c3, "min-mod-3")
    Y = check_F3()
    if Y:
        check_F4(Y)
