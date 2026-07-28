"""
ADVERSARIAL AUDIT 5: the q-adic fiber test and the branch-and-bound in M_audit_phi.py.

Three independent computations of Phi_q(S) = max_assign min_r F_q(r):
  (BF)  literal brute force over ALL residue assignments, using the LITERAL definition
        F_q(r) = sum_{m : b_m = r mod q^{nu_q(m)}} q^{nu_q(m)}/m  with r ranging over Z/q^J.
        This does NOT use the contiguous-block relabelling, so it also tests that.
  (REC) exact recursion on the q-ary tree (distribute items among children, recurse).
  (BB)  M_audit_phi.phi_q_at_least (the code under audit), queried as a decision oracle.
Also: verify the fiber lemma F_q(r) >= 1 directly on genuine covering systems, and verify
the Haar-average identity avg_r F_q(r) = sum 1/m.
"""
import sys, os, random, itertools
from fractions import Fraction
from math import gcd
from sympy import isprime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from M_audit_phi import phi_q_at_least, pool, divisors, nu


def lcm(xs):
    L = 1
    for x in xs:
        L = L * x // gcd(L, x)
    return L


# ------------------------------------------------------------------ literal brute force
def phi_bruteforce(S, q):
    J = max(nu(m, q) for m in S)
    base = sum(Fraction(1, m) for m in S if m % q != 0)
    items = [(Fraction(q ** nu(m, q), m), nu(m, q)) for m in S if m % q == 0]
    if not items:
        return base
    best = None
    for choice in itertools.product(*[range(q ** j) for _, j in items]):
        F = [base] * (q ** J)
        for (w, j), b in zip(items, choice):
            qj = q ** j
            for r in range(q ** J):
                if r % qj == b:
                    F[r] += w
        v = min(F)
        if best is None or v > best:
            best = v
    return best


# ------------------------------------------------------------------ exact tree recursion
def phi_recursive(S, q):
    J = max(nu(m, q) for m in S)
    base = sum(Fraction(1, m) for m in S if m % q != 0)
    items = tuple(sorted((Fraction(q ** nu(m, q), m), nu(m, q)) for m in S if m % q == 0))
    memo = {}

    def val(base, items):
        if not items:
            return base
        key = (base, items)
        if key in memo:
            return memo[key]
        best = None
        for choice in itertools.product(range(q), repeat=len(items)):
            groups = [[] for _ in range(q)]
            addbase = [Fraction(0)] * q
            for (w, j), c in zip(items, choice):
                if j == 1:
                    addbase[c] += w
                else:
                    groups[c].append((w, j - 1))
            v = min(val(base + addbase[c], tuple(sorted(groups[c]))) for c in range(q))
            if best is None or v > best:
                best = v
        memo[key] = best
        return best

    return val(base, items)


# ------------------------------------------------------------------ cross-checks
def cross_check(trials=40, seed=5):
    rng = random.Random(seed)
    Hsmall = [m for m in range(2, 200) if isprime(2 * m + 1)]
    nchk = 0
    for _ in range(trials):
        q = rng.choice([2, 3, 5])
        k = rng.randint(2, 6)
        S = sorted(rng.sample(Hsmall, k))
        if all(m % q for m in S):
            continue
        J = max(nu(m, q) for m in S)
        if q ** J > 64:
            continue
        nit = sum(1 for m in S if m % q == 0)
        if q ** (nit * 2) > 200000:
            continue
        bf = phi_bruteforce(S, q)
        rc = phi_recursive(S, q)
        assert bf == rc, ("BF != REC", S, q, bf, rc)
        # decision oracle agreement at several thresholds
        for T in [bf, bf + Fraction(1, 1000), bf - Fraction(1, 1000), Fraction(1), Fraction(2)]:
            ok, _ = phi_q_at_least(S, q, T)
            assert ok is not None
            assert ok == (bf >= T), ("BB disagrees", S, q, T, bf, ok)
        nchk += 1
    print(f"  cross-check on {nchk} random pools: literal brute force == tree recursion == "
          f"branch-and-bound decision, at 5 thresholds each.  NO disagreement.")


def fiber_lemma_check(trials=400, seed=9):
    """F_q(r) >= 1 on genuine covering systems, and the Haar average identity."""
    rng = random.Random(seed)
    Ls = [12, 24, 36, 60, 72, 120, 180, 360]
    ncov = 0
    for _ in range(trials):
        L = rng.choice(Ls)
        pooled = [d for d in range(2, L + 1) if L % d == 0]
        hit = bytearray(L)
        cls, used = [], set()
        for _ in range(12):
            try:
                r = hit.index(0)
            except ValueError:
                break
            av = [n for n in pooled if n not in used]
            if not av:
                break
            n = rng.choice(av)
            used.add(n)
            a = r % n
            cls.append((a, n))
            seg = hit[a::n]
            hit[a::n] = b'\x01' * len(seg)
        if not all(hit):
            continue
        ncov += 1
        for q in [2, 3, 5, 7]:
            if all(n % q for _, n in cls):
                continue
            J = max(nu(n, q) for _, n in cls)
            F = []
            for r in range(q ** J):
                s = Fraction(0)
                for a, n in cls:
                    j = nu(n, q)
                    if (a - r) % (q ** j) == 0:
                        s += Fraction(q ** j, n)
                F.append(s)
            assert min(F) >= 1, ("FIBER LEMMA FAILS", cls, q, F)
            avg = sum(F) / len(F)
            assert avg == sum(Fraction(1, n) for _, n in cls), ("Haar average wrong", cls, q)
    print(f"  fiber lemma on {ncov} genuine coverings x q in {{2,3,5,7}}: min_r F_q(r) >= 1 always,"
          f" and avg_r F_q(r) = sum 1/n exactly.  OK")


def monotone_pool_check(trials=60, seed=13):
    """'enlarging the used set only increases F_q' -> Phi_q monotone in S."""
    rng = random.Random(seed)
    Hsmall = [m for m in range(2, 120) if isprime(2 * m + 1)]
    for _ in range(trials):
        q = rng.choice([2, 3])
        k = rng.randint(2, 5)
        S = sorted(rng.sample(Hsmall, k))
        extra = rng.choice([m for m in Hsmall if m not in S])
        S2 = sorted(S + [extra])
        if q ** max(nu(m, q) for m in S2) > 32:
            continue
        if sum(1 for m in S2 if m % q == 0) > 6:
            continue
        a = phi_bruteforce(S, q) if any(m % q == 0 for m in S) else sum(Fraction(1, m) for m in S)
        b = phi_bruteforce(S2, q)
        assert b >= a, ("Phi not monotone in S", S, S2, q, a, b)
    print("  Phi_q is monotone under enlarging the pool S (checked on random pools). OK")


def specific_kills():
    print("  specific elimination claims:")
    for name, LE in [("L_E = 55440 (L_H = 27720)", 55440), ("L_E = 110880 (L_H=55440)", 110880)]:
        LH = LE // 2
        S = pool(LH)
        B = sum(Fraction(1, m) for m in S)
        out = []
        for q in sorted({p for p in range(2, 60) if isprime(p) and LH % p == 0}):
            ok, best = phi_q_at_least(S, q, Fraction(2))
            out.append(f"q={q}:{'KILL' if ok is False else ('cap' if ok is None else 'ok')}")
        print(f"    {name}: |S|={len(S)} H-budget={float(B):.5f} (=2*B_E) -> " + " ".join(out))


if __name__ == "__main__":
    print("== q-adic fiber test audit ==")
    cross_check()
    fiber_lemma_check()
    monotone_pool_check()
    specific_kills()
