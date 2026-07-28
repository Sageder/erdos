#!/usr/bin/env python3
"""
prune.py -- Rule (P) + legality fixpoint of a range [T,N] for an arbitrary
rational target u/v, written out as a problem file for esearch.

RULE (P).  Let W be finite, sum_{n in W} 1/n = u/v (in lowest terms), p prime,
and E any integer with E >= nu_p(n) for every n in W.  Multiplying by p^E,
every term p^E/n with p not dividing n is a p-adic integer divisible by p^E,
so
        sum_{n in W, p | n} p^E/n  ==  p^E * u/v      (mod p^E).
(The right side is a p-adic integer as soon as E >= nu_p(v).)  Taking E to be
the maximum of nu_p over the CURRENT UNIVERSE A -- which is >= the maximum over
any W contained in A -- the congruence must hold for every admissible W, so an
element n of A with p | n may be DELETED whenever no subset of the multiples of
p in A that CONTAINS n has weight sum == p^E*u/v (mod p^E).  Subset
reachability is decided exactly by a forward/backward DP over Z/p^E, carried
here as Python-integer BITMASKS (one bit per residue), which makes each prime
cost O(|multiples| * p^E / 64) word operations.

RULE (L) (legality).  If both neighbours of n have been deleted, delete n.

Both rules only ever delete, so iterating to a fixpoint is sound: every legal
W contained in [T,N] with sum u/v survives.  All arithmetic is exact integer
arithmetic (Python ints / fractions); no floating point is used.

usage:  prune.py T N [u v] [-o outfile] [-v]
"""
import sys
from math import gcd
from fractions import Fraction


def primes_upto(N):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= N:
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
        i += 1
    return [i for i in range(2, N + 1) if s[i]]


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def prune(T, N, u=1, v=1, verbose=False, gadget=False, minval=None):
    """gadget=False: exact target u/v.
       gadget=True : v = D, and ANY value a/D is acceptable (numerator free).
                     Rule (P) then reads  sum_{n in W, p|n} p^E/n == 0
                     (mod p^{max(0,E-nu_p(D))}), because p^E*a/D runs over every
                     multiple of p^{E-nu_p(D)} as a varies.
       minval      : optional Fraction; a universe whose total is below it is
                     declared empty."""
    g = gcd(u, v)
    u //= g
    v //= g
    P = primes_upto(N)
    A = set(range(T, N + 1))
    rounds = 0
    changed = True
    while changed and A:
        changed = False
        rounds += 1
        for p in P:
            M = sorted(n for n in A if n % p == 0)
            if not M:
                if not gadget and v % p == 0:
                    return []          # nothing can supply p in the denominator
                continue
            E = max(nu(n, p) for n in M)
            f = nu(v, p)
            if gadget:
                Ep = E - f
                if Ep <= 0:
                    continue           # D absorbs the whole p-part: no condition
                pe = p ** Ep
                mask = (1 << pe) - 1

                def rot(S, x, pe=pe, mask=mask):
                    x %= pe
                    if x == 0:
                        return S
                    return ((S << x) | (S >> (pe - x))) & mask

                w = []
                for n in M:
                    e = nu(n, p)
                    m = n // p ** e
                    w.append((p ** (E - e) * pow(m, -1, pe)) % pe)
                rhs = 0
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
                        print(f"  p={p} E'={Ep}: deleted {len(dead)} -> |A|={len(A)}", file=sys.stderr)
                continue
            if f > E:
                return []              # denominator p-part unreachable
            pe = p ** E
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
            F = [0] * (L + 1)          # F[i] = subset sums of w[0..i-1]
            F[0] = 1
            for i in range(L):
                F[i + 1] = F[i] | rot(F[i], w[i])
            Bn = [0] * (L + 1)         # Bn[i] = NEGATED subset sums of w[i..]
            Bn[L] = 1
            for i in range(L - 1, -1, -1):
                Bn[i] = Bn[i + 1] | rot(Bn[i + 1], -w[i])
            dead = []
            for i, n in enumerate(M):
                # need a in F[i], b in bwd[i+1] with a + w_i + b == rhs,
                # i.e. (a + w_i - rhs) in Bn[i+1]
                if not (rot(F[i], w[i] - rhs) & Bn[i + 1]):
                    dead.append(n)
            if dead:
                A.difference_update(dead)
                changed = True
                if verbose:
                    print(f"  p={p} E={E}: deleted {len(dead)} -> |A|={len(A)}", file=sys.stderr)
        dead = [n for n in A if (n - 1) not in A and (n + 1) not in A]
        if dead:
            A.difference_update(dead)
            changed = True
            if verbose:
                print(f"  legality: deleted {len(dead)} -> |A|={len(A)}", file=sys.stderr)
        need = minval if minval is not None else (None if gadget else Fraction(u, v))
        if need is not None and A and sum(Fraction(1, n) for n in A) < need:
            return []
    if verbose:
        print(f"  fixpoint after {rounds} rounds", file=sys.stderr)
    return sorted(A)


def main():
    args = [a for a in sys.argv[1:]]
    out = None
    verbose = False
    gadget = False
    minval = None
    if "-v" in args:
        verbose = True
        args.remove("-v")
    if "-g" in args:
        gadget = True
        args.remove("-g")
    if "-min" in args:
        k = args.index("-min")
        minval = Fraction(args[k + 1])
        del args[k:k + 2]
    if "-o" in args:
        k = args.index("-o")
        out = args[k + 1]
        del args[k:k + 2]
    T, N = int(args[0]), int(args[1])
    u, v = (int(args[2]), int(args[3])) if len(args) > 3 else (1, 1)
    A = prune(T, N, u, v, verbose, gadget=gadget, minval=minval)
    L = 1
    for n in A:
        L = L * n // gcd(L, n)
    tot = sum(Fraction(1, n) for n in A) if A else Fraction(0)
    need = minval if minval is not None else (Fraction(0) if gadget else Fraction(u, v))
    print(f"[{T},{N}] {'D=' if gadget else 'target='}{v if gadget else str(u) + '/' + str(v)}"
          f"  |A|={len(A)}  lcm bits={L.bit_length()}  "
          f"maxsum={float(tot):.5f}  reachable={tot >= need}")
    if out:
        with open(out, "w") as f:
            f.write(f"{T} {N} {u} {v}\n{len(A)}\n")
            f.write(" ".join(map(str, A)) + "\n")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
