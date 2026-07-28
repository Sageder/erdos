#!/usr/bin/env python3
"""
design.py -- build a DESIGNED universe for a window [T,N] and a target u/v.

The design step is:  fix a smoothness threshold z and DELETE every n in [T,N]
that has a prime factor > z.  This is a *restriction*, not a prune: it can only
lose solutions, never create them.  Therefore

    * a solution found inside the designed universe is a genuine solution;
    * an emptiness/failure result inside the designed universe proves NOTHING
      about [T,N].

After the restriction we still run the sound Rule (P) + legality fixpoint
(same rules as attempts/wf-engine/prune.py, re-implemented here independently)
on the restricted universe; that is legitimate because the fixpoint only
deletes elements that cannot occur in any legal W with the given sum inside
the *current* universe.

Rationale for the design (see smoothstats.py, forced.py):
  * Rule (P) FORCES every n with a prime factor p > N/2 out (only one multiple
    of such a p exists in [1,N]).                                     [PROVED]
  * For p with exactly two multiples pa < pb in the window the Rule (P)
    congruence is  a + b == 0 (mod p), which is unsatisfiable as soon as
    a + b < p, i.e. as soon as p > 2N/p, i.e. p > sqrt(2N).           [PROVED]
    So a prime p in (sqrt(2N), N/2] can only be used if U contains >= 3
    multiples of p.
  * Empirically (smoothstats.py) every one of the 39267 known solutions has
    every element (max U / 4)-smooth, and all but two are (max U / 5)-smooth;
    the far-out ones are much smoother still.                       [OBSERVED]

usage:  design.py T N [u v] [-z Z | -zsqrt C | -zdiv C] [-o out.prob] [-v]
"""
import sys, os
from fractions import Fraction
from math import gcd, isqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import primes_upto, nu, largest_prime_factor_sieve


def rulep_fixpoint(A, N, u=1, v=1, verbose=False):
    """Sound Rule (P) + legality fixpoint on an arbitrary universe A subset [2,N]."""
    g = gcd(u, v); u //= g; v //= g
    A = set(A)
    P = primes_upto(N)
    changed = True
    rounds = 0
    while changed and A:
        changed = False
        rounds += 1
        for p in P:
            M = sorted(n for n in A if n % p == 0)
            if not M:
                if v % p == 0:
                    return []
                continue
            E = max(nu(n, p) for n in M)
            f = nu(v, p)
            if f > E:
                return []
            pe = p ** E
            if pe > (1 << 22):            # safety: skip absurd moduli
                continue
            mask = (1 << pe) - 1

            def rot(S, x):
                x %= pe
                if x == 0:
                    return S
                return ((S << x) | (S >> (pe - x))) & mask

            w = []
            for n in M:
                e = nu(n, p)
                m = n // p ** e
                w.append((p ** (E - e) * pow(m, -1, pe)) % pe)
            vv = v // p ** f
            rhs = (p ** (E - f) % pe) * (u % pe) % pe * pow(vv % pe, -1, pe) % pe
            L = len(M)
            F = [0] * (L + 1); F[0] = 1
            for i in range(L):
                F[i + 1] = F[i] | rot(F[i], w[i])
            Bn = [0] * (L + 1); Bn[L] = 1
            for i in range(L - 1, -1, -1):
                Bn[i] = Bn[i + 1] | rot(Bn[i + 1], -w[i])
            dead = [n for i, n in enumerate(M)
                    if not (rot(F[i], w[i] - rhs) & Bn[i + 1])]
            if dead:
                A.difference_update(dead)
                changed = True
                if verbose:
                    print(f"  p={p} E={E}: -{len(dead)} -> |A|={len(A)}", file=sys.stderr)
        dead = [n for n in A if (n - 1) not in A and (n + 1) not in A]
        if dead:
            A.difference_update(dead)
            changed = True
            if verbose:
                print(f"  legality: -{len(dead)} -> |A|={len(A)}", file=sys.stderr)
        if A and sum(Fraction(1, n) for n in A) < Fraction(u, v):
            return []
    if verbose:
        print(f"  fixpoint after {rounds} rounds", file=sys.stderr)
    return sorted(A)


def build(T, N, u=1, v=1, z=None, verbose=False):
    lpf = largest_prime_factor_sieve(N)
    if z is None:
        z = N
    A = [n for n in range(T, N + 1) if lpf[n] <= z]
    A = rulep_fixpoint(A, N, u, v, verbose)
    return A, z


def main():
    args = sys.argv[1:]
    out = None; verbose = False; z = None
    if "-v" in args:
        verbose = True; args.remove("-v")
    for flag in ("-z", "-zsqrt", "-zdiv", "-o"):
        pass
    if "-o" in args:
        k = args.index("-o"); out = args[k + 1]; del args[k:k + 2]
    zmode = None; zpar = None
    for flag in ("-z", "-zsqrt", "-zdiv"):
        if flag in args:
            k = args.index(flag); zmode = flag; zpar = args[k + 1]; del args[k:k + 2]
    T, N = int(args[0]), int(args[1])
    u, v = (int(args[2]), int(args[3])) if len(args) > 3 else (1, 1)
    if zmode == "-z":
        z = int(zpar)
    elif zmode == "-zsqrt":
        z = int(float(zpar) * isqrt(N))     # diagnostic only: z is then an exact int
    elif zmode == "-zdiv":
        z = N // int(zpar)
    else:
        z = N
    A, z = build(T, N, u, v, z, verbose)
    L = 1
    for n in A:
        L = L * n // gcd(L, n)
    tot = sum(Fraction(1, n) for n in A) if A else Fraction(0)
    print(f"[{T},{N}] target={u}/{v} z={z}  |A|={len(A)}  lcm bits={L.bit_length()}  "
          f"maxsum={float(tot):.5f}  reachable={tot >= Fraction(u, v)}")
    if out:
        with open(out, "w") as f:
            f.write(f"{T} {N} {u} {v}\n{len(A)}\n")
            f.write(" ".join(map(str, A)) + "\n")
        print("wrote", out)


if __name__ == "__main__":
    main()
