"""
reduce.py -- universe reduction for Erdos 289 route B.

CLAIM TESTED / TOOL:  Given N, compute a set A subset [2,N] such that every legal
U subset [2,N] with sum_{n in U} 1/n = 1 satisfies U subset A.

Two exact necessary conditions are iterated to a fixpoint.

(P) p-adic block condition.  For every prime p:
        S_p := sum_{n in U, p | n} 1/n     satisfies   nu_p(S_p) >= 0.
    Proof: 1 = S_p + S'_p where S'_p is the sum over n in U with p not dividing n;
    every such 1/n lies in Z_p so nu_p(S'_p) >= 0; if nu_p(S_p) < 0 then
    nu_p(1) = nu_p(S_p + S'_p) = nu_p(S_p) < 0, contradiction.  QED
    Operationally: let E = max_{n in A, p|n} nu_p(n).  Then p^E/n is in Z_p for each
    multiple n, and the condition reads
        sum_{n in U, p|n}  (p^E / n)  ==  0   (mod p^E)
    which is a subset-sum-to-zero condition modulo p^E over the multiples of p in A.
    An element n (p|n) may be deleted from A whenever NO subset of the multiples of p
    in A that contains n has residue 0 mod p^E.  (Forward/backward reachability DP.)

    This strictly generalises the "two-attainer" prune: |T_e| = 1 gives a single
    subset {n} with residue p^{E-e}*inv(n/p^e) != 0 mod p^E.

(I) isolated-point condition.  If n-1 and n+1 are both outside A then n has no
    possible neighbour, so n cannot lie in any legal U; delete n.

Both rules only ever delete, so the iteration terminates, and each deleted element
provably lies in no solution.  Hence the fixpoint A is a valid over-approximation.

Conclusion (see REPORT.md): the fixpoint is dramatically smaller than the universe
used by experiments/csearch.c.
"""
import sys
from sympy import primerange


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def inv_mod(a, m):
    return pow(a, -1, m)


def rot(x, k, mod, mask):
    """cyclic left shift of a residue-bitmask by k (mod mod)"""
    if k == 0:
        return x
    return ((x << k) | (x >> (mod - k))) & mask


def prime_prune(allowed, p):
    """Return the set of multiples of p in `allowed` that must be deleted."""
    mults = sorted(n for n in allowed if n % p == 0)
    if not mults:
        return set()
    E = max(nu(n, p) for n in mults)
    mod = p ** E
    mask = (1 << mod) - 1
    coef = []
    for n in mults:
        e = nu(n, p)
        c = (p ** (E - e)) * inv_mod(n // (p ** e), mod) % mod
        coef.append(c)
    k = len(mults)
    # forward: F[i] = residues reachable from mults[0..i-1]
    F = [0] * (k + 1)
    F[0] = 1  # only residue 0
    for i in range(k):
        F[i + 1] = F[i] | rot(F[i], coef[i], mod, mask)
    # backward: B[i] = residues reachable from mults[i..k-1]
    B = [0] * (k + 2)
    B[k] = 1
    for i in range(k - 1, -1, -1):
        B[i] = B[i + 1] | rot(B[i + 1], coef[i], mod, mask)
    # reverse of B[i+1]: bit j set iff (-j mod mod) in B[i+1]
    dead = set()
    for i in range(k):
        b = B[i + 1]
        revb = 0
        for j in range(mod):
            if (b >> j) & 1:
                revb |= 1 << ((-j) % mod)
        t = (-coef[i]) % mod
        if (F[i] & rot(revb, t, mod, mask)) == 0:
            dead.add(mults[i])
    return dead


def reduce_universe(N, verbose=False, use_prime=True, use_iso=True, lo=2):
    """Fixpoint of rules (P) and (I) over the interval [lo, N].

    With lo > 2 this over-approximates the class of solutions U with
    min(U) >= lo -- a RESTRICTED class, which must be stated when reporting.
    """
    allowed = set(range(lo, N + 1))
    primes = list(primerange(2, N + 1))
    rounds = 0
    while True:
        rounds += 1
        removed = set()
        if use_prime:
            for p in primes:
                d = prime_prune(allowed, p)
                if d:
                    removed |= d
                    if verbose:
                        print(f"  p={p}: remove {sorted(d)}")
            allowed -= removed
        if use_iso:
            iso = set()
            for n in allowed:
                if (n - 1) not in allowed and (n + 1) not in allowed:
                    iso.add(n)
            if iso and verbose:
                print(f"  isolated: remove {sorted(iso)}")
            allowed -= iso
            removed |= iso
        if not removed:
            break
    return sorted(allowed), rounds


def lcm_of(xs):
    from math import gcd
    L = 1
    for x in xs:
        L = L // gcd(L, x) * x
    return L


if __name__ == "__main__":
    for N in [int(a) for a in sys.argv[1:]] or [40, 50, 60, 70, 80, 90, 100, 120, 150]:
        A, r = reduce_universe(N)
        L = lcm_of(A) if A else 1
        print(f"N={N:4d}  |A|={len(A):4d}  rounds={r}  L has {len(str(L))} digits")
        print(f"   A = {A}")
        print(f"   banned = {[n for n in range(2, N+1) if n not in set(A)]}")
        print(f"   L = {L}")
        print()
