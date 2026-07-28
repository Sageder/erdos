"""
B_deep.py -- Route B: does the local budget at a DEEP node recover if the local lcm M grows?

CLAIM TESTED
------------
At a node with node-modulus D the usable moduli are  D*f  with  f | M, D f + 1 prime, where M
is the lcm the node is allowed to build.  The node can only be covered if

        beta(D, M) := sum_{ f | M, f >= 2, D f + 1 prime } 1/f   >   1

(and empirically one needs beta >~ 1.9 for an actual covering to exist).  The heuristic value is

        beta(D,M) ~ (D/phi(D)) * sum_{f | M} 1 / ( f * log(D f) ),

so it is a tug-of-war between the enrichment D/phi(D) (which grows like e^gamma loglog D) and
the 1/log(D f) damping (which grows like 1/log D).  This script measures beta(D,M) exactly for
fixed D as M runs through an increasing chain of smooth numbers, up to ~1e5 divisors.

CONCLUSION: printed; the sup over M of beta(D,M) decays with D -- see the run output.
"""
import sys
from sympy import isprime, nextprime

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def chain_of_M(maxdiv):
    """increasing chain of smooth M, each obtained from the previous by the exponent bump that
    maximises sum_{f|M} 1/f per divisor added."""
    exps = [0] * len(PRIMES)
    out = []
    while True:
        best = None
        for i, p in enumerate(PRIMES):
            e = exps[i]
            # gain in sigma(M)/M from bumping p^e -> p^(e+1), cost = divisor-count factor
            gain = (1.0 / p ** (e + 1))
            cost = (e + 2) / (e + 1)
            score = gain / (cost - 1)
            if best is None or score > best[0]:
                best = (score, i)
        exps[best[1]] += 1
        nd = 1
        M = 1
        for i, p in enumerate(PRIMES):
            nd *= exps[i] + 1
            M *= p ** exps[i]
        if nd > maxdiv:
            break
        out.append((M, nd, tuple(exps)))
    return out


def divisors_from_exps(exps):
    ds = [1]
    for i, p in enumerate(PRIMES):
        if exps[i]:
            ds = [d * p ** k for d in ds for k in range(exps[i] + 1)]
    return ds


def beta(D, exps):
    s = 0.0
    n = 0
    for f in divisors_from_exps(exps):
        if f < 2:
            continue
        if isprime(D * f + 1):
            s += 1.0 / f
            n += 1
    return s, n


def main():
    maxdiv = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    chain = chain_of_M(maxdiv)
    print(f"chain of M: {len(chain)} entries, largest #div = {chain[-1][1]}, "
          f"largest M = {chain[-1][0]:.4g}")
    Ds = [2, 6, 12, 60, 210, 420, 2310, 4620, 30030, 60060, 510510, 1021020,
          9699690, 19399380, 223092870]
    print(f"{'D':>10} " + " ".join(f"{nd:>7}" for _, nd, _ in chain[::max(1, len(chain)//9)]))
    for D in Ds:
        row = []
        best = 0.0
        for M, nd, exps in chain[::max(1, len(chain) // 9)]:
            b, k = beta(D, exps)
            row.append(f"{b:7.3f}")
        for M, nd, exps in chain:
            b, k = beta(D, exps)
            best = max(best, b)
        print(f"{D:>10} " + " ".join(row) + f"   | sup over the whole chain = {best:.3f}")


if __name__ == "__main__":
    main()
