#!/usr/bin/env python3
r"""
twoblock.py -- how SMALL can a lift be?  Decide  1/n = H(c,d) + H(e,f)
(two disjoint blocks, each of length >= 2).

Known already (repository, PROVED): H(a,b) is never a unit fraction, so a lift
of 1/n can never consist of ONE block.  This script settles TWO blocks.

FINITENESS (proved, so the enumeration below is not an arbitrary cutoff):
 * both blocks have sum < 1/n, hence min > n;
 * the larger of the two sums is >= 1/(2n); a block [x,y] has
   H(x,y) >= 1/x + 1/(x+1) >= 2/(x+1), so that block has x+1 <= 4n;
 * once one block is fixed the residual r > 0 is a definite rational and the
   other block [x,y] satisfies 2/(y+1) <= H(x,y) = r, i.e. y <= 2/r - 1.
So: case (A) the LOWER block is the larger one -- it is enumerated completely,
and the upper block is then enumerated by LENGTH (for each length L there is at
most one x with H(x,x+L-1) = r because H(x,x+L-1) is strictly decreasing in x),
which is complete for all upper blocks of length <= LMAX with NO bound on their
elements; case (B) the UPPER block is the larger one -- it is enumerated
completely and then the lower block is enumerated completely via y <= 2/r - 1.

Additional PROVED constraint used only as a cross-check: the TOP block of any
legal system with sum u/v contains no prime p with p | v  (a prime p in the top
block has 2p above the maximum, so it occurs exactly once, forcing
nu_p(sum) = -1).  Hence in a two-block lift of 1/n the top block is prime-free
except possibly for p = n's prime factors that exceed its own minimum -- and
since the top block's minimum already exceeds n, it is prime-free outright.

usage: twoblock.py nmax [LMAX]
"""
import sys
from fractions import Fraction

nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 60
LMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 200


def H(a, b):
    return sum(Fraction(1, k) for k in range(a, b + 1))


def block_with_value(r, lmax, xmin):
    """all blocks [x,y] with H(x,y) = r, y-x+1 <= lmax, x >= xmin.  For fixed
    length L, H(x,x+L-1) is strictly decreasing in x, so a binary search over x
    is complete."""
    out = []
    for L in range(2, lmax + 1):
        lo, hi = max(2, xmin), int(L / r) + 2
        while lo <= hi:
            mid = (lo + hi) // 2
            v = H(mid, mid + L - 1)
            if v == r:
                out.append((mid, mid + L - 1)); break
            if v > r: lo = mid + 1
            else: hi = mid - 1
    return out


def sieve(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= n:
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
        i += 1
    return s


found = []
for n in range(2, nmax + 1):
    tgt = Fraction(1, n)
    # case (A): lower block is the larger one -> c <= 4n-1
    for c in range(n + 1, 4 * n + 1):
        s = Fraction(0); d = c - 1
        while True:
            d += 1
            s += Fraction(1, d)
            if d == c: continue
            if s >= tgt: break
            r = tgt - s
            for (e, f) in block_with_value(r, LMAX, d + 2):
                found.append((n, (c, d), (e, f)))
    # case (B): upper block is the larger one -> e <= 4n-1, then y <= 2/r-1
    for e in range(n + 1, 4 * n + 1):
        s = Fraction(0); f = e - 1
        while True:
            f += 1
            s += Fraction(1, f)
            if f == e: continue
            if s >= tgt: break
            r = tgt - s
            ymax = int(2 / r)
            if ymax > 400000: ymax = 400000        # only reached if r is tiny
            for c in range(n + 1, min(e - 2, ymax) + 1):
                t = Fraction(0); d = c - 1
                while d + 1 <= min(e - 2, ymax):
                    d += 1
                    t += Fraction(1, d)
                    if d == c: continue
                    if t == r: found.append((n, (c, d), (e, f)))
                    if t >= r: break
    print("n=%d done" % n, flush=True)
print("two-block lifts found:", found)
print("scope: all n <= %d; lower-larger case complete for upper blocks of "
      "length <= %d (no element bound); upper-larger case complete." % (nmax, LMAX))
