#!/usr/bin/env python3
"""
construct.py -- THE TWO-STAGE CONSTRUCTION.

STAGE 1 (CONSTRUCTIVE, no global search).  For every prime p in (z0,z] we
solve the Rule (P) congruence for p ALONE:

     choose S_p subset of  M_p = { n in [T,N] : P(n) = p, P(n/p) <= z0,
                                   p^2 does not divide n,
                                   n has a neighbour that is z0-smooth }
     with       sum_{n in S_p} 1/(n/p)  ==  0   (mod p).

By the Decoupling Lemma (interaction.py) the sets M_p are pairwise disjoint,
so these congruences are INDEPENDENT: each is solved on its own by an exact
subset-sum DP over Z/p, and the choices never interfere.  Each chosen n is
then escorted by a neighbour (another chosen rough element if possible,
otherwise a z0-smooth neighbour), so the resulting set R is legal.

Because every p in (z0,z] cancels and every other prime factor occurring in R
is <= z0, the value  sum_{n in R} 1/n  lies in (1/L0)Z with the FIXED SMOOTH
modulus  L0 = prod_{r<=z0} r^{floor(log_r N)}.

STAGE 2 (EXPLICIT FINITE ADJUSTMENT).  The residual  r = q - sum_R 1/n  again
lies in (1/L0)Z.  We look for a legal subset of the z0-SMOOTH part of the
window with reciprocal sum exactly r.  That is a finite exact problem modulo
the fixed modulus L0, decided by the exact engine (esearchB, arbitrary
rational target).  If it succeeds, U = R u (tail) is a genuine solution.

Everything is exact; no float is used in any decision.

usage:
  construct.py T N num den -z0 Z0 [-z Z] [-seed S] [-tries K] [-t SECS]
               [-massmin M] [-out PREFIX]
"""
import sys, os, random, subprocess
from fractions import Fraction
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import largest_prime_factor_sieve, primes_upto, verify_solution
from design import rulep_fixpoint
from mkprob import write_prob

HERE = os.path.dirname(os.path.abspath(__file__))


def pack_choices(Mp, p, rng, want="rand"):
    """All subsets S of Mp with sum 1/(n/p) == 0 mod p, returned as a random
    admissible one (or the maximal-mass one).  Exact DP over Z/p on the
    residues 1/(n/p) mod p; reconstruction is exact."""
    ws = [pow(n // p, -1, p) for n in Mp]
    # DP: reach[i][r] = True if some subset of the first i items sums to r
    L = len(Mp)
    reach = [[False] * p for _ in range(L + 1)]
    reach[0][0] = True
    for i, w in enumerate(ws):
        for rr in range(p):
            if reach[i][rr]:
                reach[i + 1][rr] = True
                reach[i + 1][(rr + w) % p] = True
    if not reach[L][0]:
        return None
    # backtrack, choosing greedily/randomly among admissible moves
    S = []
    rr = 0
    for i in range(L - 1, -1, -1):
        w = ws[i]
        can_skip = reach[i][rr]
        can_take = reach[i][(rr - w) % p]
        if can_take and can_skip:
            take = (rng.random() < 0.5) if want == "rand" else True
        elif can_take:
            take = True
        else:
            take = False
        if take:
            S.append(Mp[i])
            rr = (rr - w) % p
    return sorted(S)


def candidates(T, N, z0, z, lpf):
    """S0 (the z0-smooth part) and, for each rough prime p in (z0,z], the
    designed multiple set M_p."""
    S0 = set(n for n in range(T, N + 1) if lpf[n] <= z0)
    Mp = {}
    for n in range(T, N + 1):
        p = lpf[n]
        if p <= z0 or p > z:
            continue
        if lpf[n // p] > z0 or n % (p * p) == 0:
            continue
        if (n - 1) in S0 or (n + 1) in S0:
            Mp.setdefault(p, []).append(n)
    return S0, Mp


def build_R(S0, Mp, T, N, rng, masscap):
    """Stage 1: independent per-prime packs + escorts, stopping once the
    accumulated reciprocal mass reaches masscap."""
    R = set()
    mass = Fraction(0)
    for p in rng.sample(sorted(Mp), len(Mp)):
        if mass >= masscap:
            break
        S = pack_choices(Mp[p], p, rng)
        if not S:
            continue
        add = set(S)
        esc = set()
        for n in S:
            if (n - 1) in S or (n + 1) in S or (n - 1) in R or (n + 1) in R:
                continue
            c = [m for m in (n - 1, n + 1) if T <= m <= N and m in S0 and m not in R]
            if not c:
                esc = None
                break
            esc.add(rng.choice(c))
        if esc is None:
            continue
        add |= esc
        if add & R:
            continue
        m2 = sum(Fraction(1, n) for n in add)
        if mass + m2 > masscap:
            continue
        R |= add
        mass += m2
    for n in R:
        if (n - 1) not in R and (n + 1) not in R:
            return None
    return R


def main():
    a = sys.argv[1:]
    def opt(name, default=None, cast=str):
        if name in a:
            k = a.index(name); v = a[k + 1]; del a[k:k + 2]; return cast(v)
        return default
    z0 = opt("-z0", 23, int)
    z = opt("-z", 10 ** 9, int)
    z1 = opt("-z1", 0, int)      # primes in (z1,z] are DESIGNED; (z0,z1] stay in the tail
    seed = opt("-seed", 1, int)
    tries = opt("-tries", 40, int)
    tlim = opt("-t", 60, int)
    massmin = Fraction(opt("-massmin", "0", str))
    prefix = opt("-out", "cons")
    T, N = int(a[0]), int(a[1])
    q = Fraction(int(a[2]), int(a[3]))
    rng = random.Random(seed)
    lpf = largest_prime_factor_sieve(N + 1)
    L0 = 1
    for r in primes_upto(z0):
        e = 0
        while r ** (e + 1) <= N:
            e += 1
        L0 *= r ** e
    S0, Mp = candidates(T, N, max(z0, z1), z, lpf)
    # the tail universe: z0-smooth part plus the designed rough candidates of the
    # primes in (z0,z1] (still one large prime per element, so still decoupled)
    _, Mtail = candidates(T, N, z0, z1, lpf) if z1 > z0 else (None, {})
    TAILU = set(S0) | set(n for v in Mtail.values() for n in v)
    smoothmass = sum(Fraction(1, n) for n in S0)
    roughmass = sum(Fraction(1, n) for v in Mp.values() for n in v)
    print(f"[{T},{N}] target={q} z0={z0} z={z}  L0 has {L0.bit_length()} bits")
    print(f"  |TAIL universe|={len(TAILU)}")
    print(f"  |S0|={len(S0)} smooth mass={float(smoothmass):.5f}; rough primes={len(Mp)}"
          f" rough candidates={sum(len(v) for v in Mp.values())} mass={float(roughmass):.5f}")
    nfail = {"R": 0, "r": 0, "fix": 0, "mass": 0, "ratio": 0}
    for t in range(tries):
        cap = q * Fraction(rng.randint(20, 75), 100)
        R = build_R(S0, Mp, T, N, rng, cap)
        if R is None:
            nfail["R"] += 1
            continue
        vR = sum(Fraction(1, n) for n in R)
        r = q - vR
        if r <= 0:
            nfail["r"] += 1
            continue
        # STAGE 1 invariant: the residual must have a z0-smooth denominator
        if z1 <= z0:
            assert L0 % r.denominator == 0, ("stage-1 invariant violated", r.denominator)
        tail = sorted(TAILU - R)
        A = rulep_fixpoint(tail, N, r.numerator, r.denominator)
        if not A:
            nfail["fix"] += 1
            continue
        tot = sum(Fraction(1, n) for n in A)
        if tot < r:
            nfail["mass"] += 1
            continue
        print(f"  try {t}: |R|={len(R)} vR={float(vR):.5f} residual={float(r):.5f} "
              f"tail |A|={len(A)} tailmass={float(tot):.5f} ratio={float(r/tot):.3f}")
        if r * 100 > tot * int(os.environ.get("RATIO","88")):
            nfail["ratio"] += 1
            continue
        pf = f"{prefix}_{t}.prob"
        try:
            write_prob(pf, T, N, A, r)
        except Exception as e:
            print("   skip:", e)
            continue
        cmd = [os.path.join(HERE, "esearchB"), pf, "-k", "30", "-m", "1", "-t", str(tlim)]
        if len(A) > 150:
            cmd += ["-R", str(rng.randint(1, 10 ** 6)), "-B", "4000000", "-p", "85"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        sols = [l for l in res.stdout.splitlines() if l.startswith("SOL")]
        print("   ", res.stdout.strip().splitlines()[-1] if res.stdout.strip() else "no output")
        if sols:
            U = sorted(R | set(int(x) for x in sols[0].split()[1:]))
            ok, info = verify_solution(U, q, T)
            print("  *** SOLUTION", "VERIFIED" if ok else "FAILED", info)
            if ok:
                with open(f"{prefix}_cert.txt", "a") as fh:
                    fh.write(" ".join(map(str, U)) + "\n")
                return
    print("no solution produced in", tries, "tries; rejects:", nfail)


if __name__ == "__main__":
    main()
