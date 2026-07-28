#!/usr/bin/env python3
"""
build.py -- CONSTRUCTION WITH PRESCRIBED p-ADIC STRUCTURE.

The designed universe of a window [T,N] for a target q is

    A(T,N,z0,z) =  S0                                   (the "smooth tail")
                U  { n : P(n) = p in (z0,z],  P(n/p) <= z0,
                      and n has a neighbour in S0 }     (the "rough packs")

where  S0 = { n in [T,N] : P(n) <= z0 }.

WHY THIS SHAPE  (this is the whole point of the attack):

 * Every element of A has AT MOST ONE prime factor > z0.  Hence the Rule (P)
   congruences for the primes p > z0 involve PAIRWISE DISJOINT sets of
   elements: the interaction between the large primes is switched off by
   construction.  (Without the condition P(n/p) <= z0 an element could carry
   two large primes and the congruences would couple.)
 * Every rough element has a z0-smooth neighbour, so it can be made legal
   without dragging in a second uncontrolled large prime.
 * Consequently, if for every p in (z0,z] the chosen multiples of p satisfy
   sum 1/(n/p) = 0 (mod p), then the total sum has a z0-SMOOTH DENOMINATOR,
   and what is left is an exact problem modulo
        L0 = prod_{r <= z0} r^{floor(log_r N)} ,
   i.e. modulo a FIXED SMOOTH modulus, exactly the "residual with only small
   primes in the denominator" of the plan.
 * The rough packs inject reciprocal MASS without adding any constraint that
   couples to the rest, which is what allows z0 to be pushed far below the
   value at which a purely z0-smooth universe would still carry the target.

The restriction to this universe is a DESIGN CHOICE: it can only lose
solutions, never create them.  A solution found in it is a genuine solution
(re-verified from scratch by lib.verify_solution / experiments/verify.py); a
failure inside it proves nothing about [T,N].

After the design restriction the sound Rule (P) + legality fixpoint of
design.py is applied.

usage:  build.py T N u v -z0 Z0 [-z Z] [-o out.prob] [-v]
"""
import sys, os
from fractions import Fraction
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import largest_prime_factor_sieve, primes_upto
from design import rulep_fixpoint


def designed_universe(T, N, z0, z=None, report=False):
    if z is None:
        z = N
    lpf = largest_prime_factor_sieve(N)
    S0 = set(n for n in range(T, N + 1) if lpf[n] <= z0)
    rough = {}
    for n in range(T, N + 1):
        p = lpf[n]
        if p <= z0 or p > z:
            continue
        if lpf[n // p] > z0:          # n carries two large primes -> discard
            continue
        if n % (p * p) == 0:          # p^2 | n: cofactor rule below assumes p||n
            continue
        if (n - 1) in S0 or (n + 1) in S0:
            rough.setdefault(p, []).append(n)
    A = sorted(S0 | set(x for v in rough.values() for x in v))
    if report:
        print(f"  |S0|={len(S0)}  rough primes={len(rough)}  "
              f"rough elements={sum(len(v) for v in rough.values())}")
        for p in sorted(rough):
            print(f"    p={p:<5} multiples kept: {rough[p]}  cofactors "
                  f"{[n//p for n in rough[p]]}")
    return A, S0, rough


def main():
    args = sys.argv[1:]
    out = None; verbose = False; z = None; z0 = None
    if "-v" in args:
        verbose = True; args.remove("-v")
    if "-o" in args:
        k = args.index("-o"); out = args[k + 1]; del args[k:k + 2]
    if "-z0" in args:
        k = args.index("-z0"); z0 = int(args[k + 1]); del args[k:k + 2]
    if "-z" in args:
        k = args.index("-z"); z = int(args[k + 1]); del args[k:k + 2]
    T, N = int(args[0]), int(args[1])
    u, v = (int(args[2]), int(args[3])) if len(args) > 3 else (1, 1)
    A, S0, rough = designed_universe(T, N, z0, z, report=verbose)
    A = rulep_fixpoint(A, N, u, v, verbose)
    L = 1
    for n in A:
        L = L * n // gcd(L, n)
    tot = sum(Fraction(1, n) for n in A) if A else Fraction(0)
    smooth_mass = sum(Fraction(1, n) for n in A if n in S0)
    print(f"[{T},{N}] target={u}/{v} z0={z0} z={z}  |A|={len(A)}  lcm bits={L.bit_length()}"
          f"  maxsum={float(tot):.5f} (smooth part {float(smooth_mass):.5f})"
          f"  reachable={tot >= Fraction(u,v)}")
    if out and A:
        with open(out, "w") as f:
            f.write(f"{T} {N} {u} {v}\n{len(A)}\n")
            f.write(" ".join(map(str, A)) + "\n")
        print("wrote", out)


if __name__ == "__main__":
    main()
