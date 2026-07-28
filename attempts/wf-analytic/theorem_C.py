"""
theorem_C.py -- EVERY SOLUTION IS y-SMOOTH, WITH y = O(N/log N).

THEOREM C.  Let T <= N, let p be a prime with p^2 > N, put
      alpha = ceil(T/p),  beta = floor(N/p),  Q = lcm(alpha,...,beta),
      Amax  = sum_{j=alpha}^{beta} Q/j   (an integer).
Let U subset [T,N] with sum_{n in U} 1/n p-integral (e.g. the sum is an integer,
or 1/2 with p odd).  If  p > Amax  then U contains NO multiple of p.

PROOF.  p^2 > N so every n in [T,N] has nu_p(n) <= 1.  Split the sum into the
part over multiples of p and the rest; the rest is p-integral.  With
J = {j : jp in U} subset [alpha,beta],
    sum_{n in U, p | n} 1/n = (1/p) sum_{j in J} 1/j = A/(pQ),  A = sum_{j in J} Q/j.
Since beta = floor(N/p) < p, every prime factor of Q is < p, so p does not
divide Q and nu_p(A/(pQ)) = nu_p(A) - 1.  p-integrality forces p | A.  But
0 <= A <= Amax < p, so A = 0, i.e. J is empty.                              []

DEFINITION.  y(T,N) := max( isqrt(N), max{ p prime : p^2 > N and p <= Amax(p) } ).
COROLLARY.  Every U subset [T,N] with integer reciprocal sum consists of
y(T,N)-smooth integers.  (Primes p <= isqrt(N) are never constrained.)

This is a strengthening, with an explicit threshold, of the repository's
"no element of a solution is divisible by a prime > max(U)/2".
"""
import sys
from math import isqrt, log
from core import primes_upto, forced_out_bound, smoothness_threshold, largest_prime_factor_table


def table(cases):
    print(f"{'T':>7} {'N':>7} {'N/T':>6} {'sqrt N':>8} {'y(T,N)':>9} {'y/N':>8} "
          f"{'y*logN/N':>9}  largest non-forced prime")
    out = {}
    for (T, N) in cases:
        root = isqrt(N)
        worst = 0
        for p in primes_upto(N):
            if p <= root:
                continue
            Amax, forced = forced_out_bound(T, N, p)
            if not forced:
                worst = p
        y = max(root, worst)
        out[(T, N)] = y
        print(f"{T:>7} {N:>7} {N/T:>6.2f} {root:>8} {y:>9} {y/N:>8.4f} "
              f"{y*log(N)/N:>9.3f}  {worst}")
    return out


def verify_on_solutions(path, limit=None):
    """
    Every known solution U must satisfy: all elements are y(min U, max U)-smooth.
    Exact check.  Reports the maximum ratio (largest prime factor)/y over the corpus.
    """
    lpf = None
    maxN = 0
    sols = []
    with open(path) as f:
        for line in f:
            parts = line.split()
            if not parts or parts[0] != 'SOL':
                continue
            U = [int(x) for x in parts[1:]]
            sols.append(U)
            maxN = max(maxN, max(U))
            if limit and len(sols) >= limit:
                break
    lpf = largest_prime_factor_table(maxN)
    cache = {}
    viol = 0
    worst_ratio = 0.0
    worst = None
    for U in sols:
        T, N = min(U), max(U)
        key = (T, N)
        if key not in cache:
            cache[key] = smoothness_threshold(T, N)
        y = cache[key]
        P = max(lpf[n] for n in U)
        if P > y:
            viol += 1
        r = P / y
        if r > worst_ratio:
            worst_ratio, worst = r, (T, N, P, y)
    print(f"corpus: {len(sols)} solutions, {len(cache)} distinct (minU,maxU) windows")
    print(f"violations of Theorem C: {viol}")
    print(f"worst ratio  P^+(U)/y(minU,maxU) = {worst_ratio:.4f}  at (T,N,P,y) = {worst}")
    return viol


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "table"
    if what == "table":
        cases = [(2, 85), (2, 200), (50, 200), (100, 400), (100, 900), (200, 800),
                 (500, 2000), (1000, 4000), (2000, 8000), (5000, 20000)]
        table(cases)
    else:
        verify_on_solutions("/home/user/erdos/experiments/ALLSOLS.txt",
                            limit=int(sys.argv[2]) if len(sys.argv) > 2 else None)
