"""
C_lcmbound.py  --  Route C: an UNCONDITIONAL lower bound on the lcm of any covering
system whose moduli all lie in E = {p-1 : p >= 5 prime}.

CLAIM PROVED HERE (and checked computationally):

  Let  a_1 mod n_1, ..., a_k mod n_k  be a covering system of Z with pairwise distinct
  moduli, all n_i in E.  Put  N = lcm(n_1,...,n_k)  and  L = N/2  (N is even because every
  element of E is even).  Then

        B_H(L) := sum_{ d | L , 2d+1 prime , d >= 2 } 1/d   >   2 .

  Proof.  By the Step-1 halving equivalence the system splits into two H-coverings with
  DISJOINT modulus sets M_0, M_1, and every m in M_0 u M_1 divides N/2 = L (m = n_i/2 and
  n_i | N).  Each M_j is a covering system of Z with distinct moduli > 1, so by the
  Davenport-Mirsky-Newman-Rado theorem sum_{m in M_j} 1/m > 1 (density gives >= 1; equality
  would make it an exact cover with distinct moduli > 1, which is impossible).  Adding the
  two, and using M_0 n M_1 = empty and M_0 u M_1 subset of D_H(L), gives B_H(L) > 2.  QED

  Because  L | L'  implies  D_H(L) subset D_H(L')  implies  B_H(L) <= B_H(L'), the set
  {L : B_H(L) > 2} is closed upwards under divisibility.  So the statement excludes an
  INFINITE family of lattices at once, not just the individual L that a search visits.

  The same argument with the single bound sum 1/m > 1 gives the weaker necessary condition
  B_H(L) > 1 for a single H-covering (question (i) of the route), and
  B_H(L) - 1/2 > 1 for an H-covering that avoids the modulus 2 (question (ii)).

WHAT THIS SCRIPT COMPUTES
  * B_H(L) for every L <= X by a sieve (add 1/d to all multiples of every d in H), and
    the smallest L with B_H(L) > 1, > 3/2, > 2, > 5/2, > 3;
  * hence a certified lower bound  N = 2L >= ...  for the lcm of any E-covering;
  * the same for the "avoid modulus 2" variant.

CONCLUSION: printed.
"""
import sys


def sieve_primes(N):
    bs = bytearray([1]) * (N + 1)
    bs[0] = bs[1] = 0
    i = 2
    while i * i <= N:
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
        i += 1
    return bs


def main(X=20_000_000):
    print(f"sieving B_H(L) for all L <= {X} ...")
    sys.stdout.flush()
    isp = sieve_primes(2 * X + 1)
    Hs = [d for d in range(2, X + 1) if isp[2 * d + 1]]
    print(f"   |H cap [2,{X}]| = {len(Hs)}")
    B = [0.0] * (X + 1)
    for d in Hs:
        r = 1.0 / d
        for L in range(d, X + 1, d):
            B[L] += r
    thresholds = [1.0, 1.5, 2.0, 2.5, 3.0]
    firsts = {}
    for L in range(1, X + 1):
        for t in thresholds:
            if t not in firsts and B[L] > t:
                firsts[t] = L
    print()
    print("smallest L with B_H(L) > t      (B_H(L) = sum of 1/d over d | L with 2d+1 prime)")
    for t in thresholds:
        if t in firsts:
            L = firsts[t]
            print(f"   t = {t:<4}  L = {L:<12}  B_H(L) = {B[L]:.6f}   factor hint: {factor(L)}")
        else:
            print(f"   t = {t:<4}  none with L <= {X}")
    print()
    if 2.0 in firsts:
        L2 = firsts[2.0]
        print(f"UNCONDITIONAL CONSEQUENCE.  Any covering system with distinct moduli all in")
        print(f"E must have  lcm/2  in the upward-closed set {{L : B_H(L) > 2}}; the smallest")
        print(f"member of that set is L = {L2}, so")
        print(f"      lcm(n_1,...,n_k)  >=  2 * {L2}  =  {2*L2}.")
        print(f"Moreover lcm/2 must be a MULTIPLE of one of the minimal elements of that set.")
    if 1.0 in firsts:
        L1 = firsts[1.0]
        print()
        print(f"For a single H-covering (route question (i)) the same argument gives")
        print(f"lcm of the H-moduli >= {L1}; and indeed C_hcover finds H-coverings with")
        print(f"lcm 360 -- consistent, since B_H(360) = {B[360]:.6f} > 1.")
    # avoid-2 variant
    best = None
    for L in range(1, X + 1):
        b = B[L] - (0.5 if L % 2 == 0 else 0.0)
        if b > 1.0:
            best = (L, b)
            break
    if best:
        print()
        print(f"For an H-covering AVOIDING the modulus 2 (route question (ii)) the necessary")
        print(f"condition is B_H(L) - 1/2 > 1; the smallest L satisfying it is L = {best[0]}"
              f"  (value {best[1]:.6f}).")
    # minimal elements of the upward-closed set {L : B_H(L) > 2}
    print()
    print("minimal elements (under divisibility) of {L : B_H(L) > 2} with L <= X:")
    minimal = []
    for L in range(2, X + 1):
        if B[L] <= 2.0:
            continue
        ok = True
        for p in set(factor(L)):
            if B[L // p] > 2.0:
                ok = False
                break
        if ok:
            minimal.append(L)
            if len(minimal) <= 40:
                print(f"   L = {L:<12} B_H = {B[L]:.6f}   {factor(L)}")
    print(f"   ... total {len(minimal)} minimal elements found with L <= {X}")
    print("   ANY covering system with all moduli in E has lcm/2 divisible by one of the")
    print("   minimal elements of this set (the list above is complete only up to X).")

    # a few sanity values
    print()
    for L in [360, 720, 2520, 5040, 27720, 55440, 360360, 720720]:
        if L <= X:
            print(f"   B_H({L}) = {B[L]:.6f}"
                  f"   -> pair possible only if > 2 : {'YES' if B[L] > 2 else 'NO (EXCLUDED)'}")


def factor(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


if __name__ == "__main__":
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    main(X)
