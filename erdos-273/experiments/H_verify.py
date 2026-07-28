"""
H_verify.py -- independent exact verifier.

CLAIM TESTED: a given list of pairs (a, m) is a covering system of Z with distinct moduli,
and (optionally) all moduli lie in H = {m>=2 : 2m+1 prime}  or  in E = {n>=4 : n+1 prime}.
Verification is an exhaustive sweep of {0,...,L-1}, L = lcm(moduli), in exact integer
arithmetic, written independently of the C search.

Usage: python3 H_verify.py --world H "0 mod 2, 1 mod 3, ..."
   or  python3 H_verify.py --world H --pairs "0:2,1:3,3:6"

CONCLUSION: prints COVERING VERIFIED / NOT A COVERING (+ an uncovered witness).
"""
import sys
from math import lcm
from sympy import isprime


def verify(pairs, world):
    mods = [m for (_, m) in pairs]
    assert len(set(mods)) == len(mods), "moduli not distinct: %s" % mods
    if world == 'H':
        bad = [m for m in mods if not (m >= 2 and isprime(2 * m + 1))]
        assert not bad, "not in H: %s" % bad
    elif world == 'E':
        bad = [m for m in mods if not (m >= 4 and isprime(m + 1))]
        assert not bad, "not in E: %s" % bad
    L = 1
    for m in mods:
        L = lcm(L, m)
    cov = bytearray(L)
    for (a, m) in pairs:
        for r in range(a % m, L, m):
            cov[r] = 1
    miss = [r for r in range(L) if not cov[r]]
    return L, miss


def main():
    world = 'H'
    args = sys.argv[1:]
    if args and args[0] == '--world':
        world = args[1]; args = args[2:]
    if args and args[0] == '--pairs':
        s = args[1]
        pairs = [tuple(int(t) for t in item.split(':')) for item in s.split(',')]
    else:
        s = ' '.join(args)
        pairs = []
        for item in s.split(','):
            a, _, m = item.split()
            pairs.append((int(a), int(m)))
    L, miss = verify(pairs, world)
    print("k = %d congruences, moduli = %s" % (len(pairs), sorted(m for _, m in pairs)))
    print("L = lcm = %d" % L)
    if miss:
        print("NOT A COVERING: %d uncovered residues mod L, e.g. %s" % (len(miss), miss[:10]))
        sys.exit(1)
    print("COVERING VERIFIED (all %d residues mod L covered; world %s membership checked)" % (L, world))


if __name__ == "__main__":
    main()
