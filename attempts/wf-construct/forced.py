#!/usr/bin/env python3
"""
forced.py -- WHICH PRIMES ARE FORCED OUT OF A WINDOW, EXACTLY.

=====================  LEMMA 1 (quantitative Rule (P))  =====================
Let N >= 2, let U be a finite set of integers in [2,N] and q = sum_{n in U} 1/n.
Let p be a prime with p*p > N and suppose v_p(q) >= 0.  Put

        S = { n in U : p | n },   k = |S|,   S = { p*a_1, ..., p*a_k }.

(The a_i are distinct integers in [1, floor(N/p)]; they are < p because
a_i <= N/p < p.)  Then either k = 0, or

        p  |  e_{k-1}(a_1,...,a_k)        where e_{k-1}(a) = sum_i prod_{j!=i} a_j ,

and in particular, since e_{k-1}(a) is a POSITIVE integer,

        e_{k-1}(a_1,...,a_k)  >=  p .                                    (1)

PROOF.  q = sum_{n in S} 1/n + sum_{n in U\S} 1/n.  Every term of the second
sum has denominator prime to p, so that sum lies in Z_p and v_p >= 0.  Hence
v_p( sum_{n in S} 1/n ) >= 0.  Now

        sum_{n in S} 1/n = (1/p) sum_i 1/a_i = e_{k-1}(a) / ( p * prod_i a_i ).

Since 0 < a_i < p, p does not divide prod a_i, so v_p of the right-hand side is
v_p(e_{k-1}(a)) - 1.  Therefore v_p(e_{k-1}(a)) >= 1, i.e. p | e_{k-1}(a).  As
all a_i >= 1 we have e_{k-1}(a) >= 1 > 0, so e_{k-1}(a) >= p.               []

=====================  COROLLARY 2 (the forced threshold)  ==================
e_{k-1} is strictly increasing in each variable, and the a_i are DISTINCT
integers in [A_p, B_p] with A_p = ceil(T/p), B_p = floor(N/p) when U is
contained in a window [T,N].  Hence (1) implies

        E(k,p) := e_{k-1}( B_p, B_p - 1, ..., B_p - k + 1 )  >=  p .       (2)

E(k,p) is increasing in k, so (2) defines a threshold

        kmin(p) := min { k >= 1 : E(k,p) >= p }        (kmin(p) = +inf if none).

Since also k <= m(p) := B_p - A_p + 1 (the number of multiples of p available),
we get:

  *** If p*p > N and m(p) < kmin(p) then NO element of [T,N] divisible by p
      can lie in any legal (indeed in any) U subset [T,N] with v_p(sum) >= 0. ***

Special cases of (2), with B = floor(N/p):
   k = 1 : E = 1  >= p  is false for every prime -> kmin >= 2 always
           (this is the classical "a prime needs two multiples" rule);
   k = 2 : E = 2B-1 >= p, i.e. p <= 2*floor(N/p)-1, i.e. essentially
           p <= sqrt(2N);
   k = 3 : E = 3B^2-6B+2 >= p, i.e. essentially p <= (3 N^2)^{1/3};
   general k : E(k,p) <= k*B^{k-1} <= k (N/p)^{k-1}, so (2) forces
           p^k <= k N^{k-1}, i.e.  p <= N * (k/N)^{1/k}.

=====================  COROLLARY 3 (density of the forced-out set)  ========
Let z*(T,N) = max { p prime : p*p > N and m(p) >= kmin(p) }  (and put
z* = max(z*, floor(sqrt(N))) so that the statement below is about p > sqrt(N)).
Then every U as above satisfies U subset V := { n in [T,N] : n has no prime
factor p with sqrt(N) < p and m(p) < kmin(p) }.  The number of DELETED integers
is at most

        |X| <= sum_{p forced} ( (N-T)/p + 1 ).

With Mertens' elementary estimate |sum_{p<=x} (log p)/p - log x| <= 2 one gets
        sum_{z < p <= N} 1/p <= ( log(N/z) + 4 ) / log z ,
so if z* >= N/L then the density of X in [T,N] is at most
        (log L + 4)/log(N/L) + pi(N)/(N-T).
Since z* is of order (N-T)/log N (see the table produced by this script), the
density of the forced-out set is O(log log N / log N) -> 0.

Consequently at least (N-T) - 2|X| of the pairs {n,n+1} in [T,N] survive
entirely, i.e. runs of length >= 2 survive in abundance.

Everything below is exact integer arithmetic.
usage:  forced.py T N [-corpus FILE] [-full]
"""
import sys, os
from math import isqrt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import primes_upto, largest_prime_factor_sieve


def esym(vals, r):
    """elementary symmetric polynomial e_r of the list vals (exact ints)."""
    e = [1] + [0] * r
    for v in vals:
        for j in range(min(r, len(e) - 1), 0, -1):
            e[j] += e[j - 1] * v
    return e[r]


def E_of(k, B):
    """e_{k-1}(B, B-1, ..., B-k+1); the largest possible value of e_{k-1} over
    k distinct positive integers <= B.  Returns 0 if B < k (impossible)."""
    if k <= 0 or B < k:
        return 0
    vals = [B - i for i in range(k)]
    return esym(vals, k - 1)


def kmin(p, N):
    """smallest k with E(k,p) >= p; None if no k <= floor(N/p) works."""
    B = N // p
    for k in range(1, B + 1):
        if E_of(k, B) >= p:
            return k
    return None


def analyse(T, N, verbose=True):
    """Return (zstar, forced_primes, allowed_primes_gt_sqrtN, X) exactly."""
    rootN = isqrt(N)
    forced = []
    allowed = []
    for p in primes_upto(N):
        if p * p <= N:
            continue
        A = (T + p - 1) // p
        B = N // p
        m = B - A + 1
        km = kmin(p, N)
        if km is None or m < km:
            forced.append((p, m, km))
        else:
            allowed.append((p, m, km))
    zstar = max([p for p, _, _ in allowed], default=rootN)
    forcedset = set(p for p, _, _ in forced)
    X = set()
    for p in forcedset:
        A = (T + p - 1) // p
        B = N // p
        for a in range(A, B + 1):
            X.add(p * a)
    return zstar, forced, allowed, X


def main():
    args = sys.argv[1:]
    full = "-full" in args
    if full:
        args.remove("-full")
    T, N = int(args[0]), int(args[1])
    zstar, forced, allowed, X = analyse(T, N)
    W = N - T + 1
    print(f"window [{T},{N}]  |window|={W}  sqrt(N)={isqrt(N)}")
    print(f"z*(T,N) = {zstar}   (largest prime > sqrt(N) that is NOT forced out)")
    print(f"forced-out primes p > sqrt(N): {len(forced)}   allowed: {len(allowed)}")
    print(f"|X| (integers in the window killed by Lemma 1) = {len(X)}"
          f"   density = {len(X)}/{W} = {len(X)/W:.4f}")
    surv = [n for n in range(T, N + 1) if n not in X]
    survset = set(surv)
    atoms = sum(1 for n in range(T, N) if n in survset and n + 1 in survset)
    print(f"survivors = {len(surv)}   adjacent surviving pairs {{n,n+1}} = {atoms}"
          f"   (>= |window| - 2|X| = {W - 2*len(X)})")
    # run structure of the survivors
    rl = {}
    cur = 0
    for n in range(T, N + 2):
        if n in survset:
            cur += 1
        else:
            if cur:
                rl[cur] = rl.get(cur, 0) + 1
            cur = 0
    print("run-length histogram of the surviving set:",
          {k: rl[k] for k in sorted(rl)})
    print()
    print("allowed primes p > sqrt(N), with (multiples available m, kmin):")
    for p, m, km in allowed[-25:]:
        print(f"   p={p:<6} m={m:<4} kmin={km}")
    if full:
        print("\nfirst forced-out primes:")
        for p, m, km in forced[:25]:
            print(f"   p={p:<6} m={m:<4} kmin={km}")
    return zstar


if __name__ == "__main__":
    main()
