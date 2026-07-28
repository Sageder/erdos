"""
INDEPENDENT AUDIT of Route D's necessary condition Phi_q(S) >= 2 and of the resulting
unconditional lower bound on the lcm.  Written from scratch; it does NOT import any D_ code.

THE CONDITION (re-derived here, not taken on trust).
By the parity split (Lemma M3), a covering system with all moduli in E is the same thing as two
DISJOINT sets M_0, M_1 of H-moduli, each carrying a covering system of Z. Fix a prime q and let
J = max_{m in S} nu_q(m), where S = {m : m | L_H, 2m+1 prime} is the pool of available H-moduli.
Give each used modulus m a residue b_m and define, for r in Z/q^J,

    F_q(r) = sum over used m with b_m = r (mod q^{nu_q(m)})  of  q^{nu_q(m)} / m.

For a single covering system of Z one has F_q(r) >= 1 for EVERY r: indeed the integers y = r
(mod q^J) that the class b_m (mod m) can meet are exactly those with b_m = r (mod q^{nu_q(m)}),
and inside that fiber the class has relative density q^{nu_q(m)}/m; density is subadditive, and
the fiber must be covered.  Since M_0 and M_1 are disjoint subsets of S with their own residues,
F_q = F_q^{(0)} + F_q^{(1)} >= 2 pointwise.  Enlarging the used set only increases F_q, so

    Phi_q(S) := max over residue assignments to ALL of S of  min_r F_q(r)     must be  >= 2.

If Phi_q(S) < 2 for some q, NO covering system with all moduli in E has lcm_H = L_H.
Note nu_q(m) determines only the q-part of b_m; the rest of b_m is unconstrained, so the search
space is exactly: assign each m with nu_q(m) = j >= 1 to one of the q^j nodes at level j; moduli
with nu_q(m) = 0 contribute 1/m to every fiber.

ALGORITHM: exact branch and bound on feasibility of "every fiber >= T", T = 2.
Items are processed in decreasing weight. Prunes:
  (A) aggregate: sum_r max(0, T - cur_r) must be <= sum over remaining items of w * (#fibers it
      covers) = sum w * q^{J-j};
  (B) per-fiber: for each fiber r, T - cur_r must be <= sum of w over ALL remaining items
      (any remaining item could in principle be placed above r).
Symmetry: the first item at each level may be fixed to node 0 of its level only when no earlier
item has broken the symmetry; to stay safe this audit fixes the FIRST item overall to node 0,
which is valid because the whole configuration space is invariant under the automorphism group of
the q-ary tree acting transitively on level-j nodes.

CONCLUSION: printed. Compare with Route D's claimed kills.
"""
import sys
from fractions import Fraction
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


def nu(n, q):
    j = 0
    while n % q == 0:
        n //= q
        j += 1
    return j


def phi_q_at_least(S, q, T):
    """exact: is there an assignment with every fiber >= T?  returns (bool, best_found)."""
    J = max(nu(m, q) for m in S)
    if J == 0:
        base = sum(Fraction(1, m) for m in S)
        return (base >= T, float(base))
    F = q ** J
    base = sum(Fraction(1, m) for m in S if m % q != 0)
    items = []
    for m in S:
        j = nu(m, q)
        if j >= 1:
            items.append((Fraction(q ** j, m), j, q ** (J - j)))
    items.sort(key=lambda t: -t[0])
    n = len(items)
    suffix_w = [Fraction(0)] * (n + 1)      # sum of w over items i..n-1
    suffix_cov = [Fraction(0)] * (n + 1)    # sum of w * (#fibers) over items i..n-1
    for i in range(n - 1, -1, -1):
        suffix_w[i] = suffix_w[i + 1] + items[i][0]
        suffix_cov[i] = suffix_cov[i + 1] + items[i][0] * items[i][2]
    cur = [base] * F
    best = [min(cur)]
    nodes = [0]

    def rec(i, sym_free):
        nodes[0] += 1
        if nodes[0] > 60_000_000:
            raise TimeoutError("node cap")
        mn = min(cur)
        if mn >= T:
            return True
        if i == n:
            best[0] = max(best[0], float(mn))
            return False
        deficit = sum((T - c) for c in cur if c < T)
        if deficit > suffix_cov[i]:
            return False
        if max(T - c for c in cur) > suffix_w[i]:
            return False
        w, j, blk = items[i]
        nnodes = q ** j
        limit = 1 if sym_free else nnodes
        for b in range(limit):
            for t in range(b * blk, (b + 1) * blk):
                cur[t] += w
            if rec(i + 1, False):
                return True
            for t in range(b * blk, (b + 1) * blk):
                cur[t] -= w
        return False

    try:
        ok = rec(0, True)
    except TimeoutError:
        return (None, best[0])
    return (ok, best[0])


def pool(LH):
    return [m for m in divisors(LH) if m >= 2 and isprime(2 * m + 1)]


if __name__ == "__main__":
    LHs = [int(x) for x in sys.argv[1:]] or [27720, 32760, 50400, 55440, 65520, 75600, 83160, 90720]
    T = Fraction(2)
    for LH in LHs:
        S = pool(LH)
        b = sum(Fraction(1, m) for m in S)
        line = f"L_H = {LH:<8} (L_E = {2*LH:<9})  |S| = {len(S):3d}  budget = {float(b):.5f}"
        if b < T:
            print(line + "   -> ELIMINATED by the budget bound alone (< 2)")
            continue
        verdicts = []
        for q in sorted({p for p in [2, 3, 5, 7, 11, 13] if LH % p == 0}):
            ok, best = phi_q_at_least(S, q, T)
            if ok is False:
                verdicts.append(f"q={q}: Phi_q < 2  ** KILL **")
                break
            elif ok is None:
                verdicts.append(f"q={q}: node cap (best {best:.4f})")
            else:
                verdicts.append(f"q={q}: >=2 OK")
        print(line + "   " + " | ".join(verdicts))
