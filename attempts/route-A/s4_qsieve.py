#!/usr/bin/env python3
"""
s4_qsieve.py -- a STRENGTHENING of the two-attainer prune, and its consequences.

LEMMA (q-sieve).  Let U be a finite set of integers >= 2 with sum_{n in U} 1/n = 1.
Let q be a prime, e := max_{n in U} nu_q(n).  If e >= 1 write the elements of U
attaining nu_q = e as q^e c_1, ..., q^e c_j  (q does not divide any c_i).  Then

        sum_{i=1}^{j} 1/c_i  ==  0   in  Z/q .

Proof.  Write S = sum_{n in U} 1/n = q^{-e} * sum_i 1/c_i  +  R  where R collects the
terms with nu_q(n) < e, so nu_q(R) > -e, i.e. R is in q^{-e+1} Z_q.  Since S = 1 has
nu_q(S) = 0 >= 0 > -e we need nu_q(q^{-e} sum_i 1/c_i) > -e, i.e. sum_i 1/c_i = 0 in Z_q.
Reduction mod q of the (q-integral) rational sum_i 1/c_i gives the statement.  QED
(The two-attainer condition is the special case "the sum of one term is never 0".)

CONSEQUENCE (used as a static sieve).  Fix N = max(U).  Working in the universe
[2,N], repeat: for each prime q, let E = max nu_q over the current universe; if no
NONEMPTY subset of { 1/c mod q : c with q^E c in universe } sums to 0 in Z/q, then
U cannot meet that level, so delete all those elements and repeat.

Also PRINTS which numbers survive, and (crucially) whether the surviving universe
still contains two consecutive survivors near the top, which max(U) needs.
"""
import sys


def primes_upto(N):
    s = [True] * (N + 1)
    s[0:2] = [False, False]
    for i in range(2, int(N ** .5) + 1):
        if s[i]:
            s[i * i::i] = [False] * len(s[i * i::i])
    return [i for i in range(2, N + 1) if s[i]]


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def zero_subset_sum_possible(vals, q):
    """is there a NONEMPTY subset of vals (elements of Z/q) summing to 0 mod q?"""
    reach = 0  # bitmask over Z/q
    for v in vals:
        new = reach
        # shift reach by v
        lo = reach >> (q - v) if v else 0
        new |= ((reach << v) | lo) & ((1 << q) - 1)
        new |= 1 << (v % q)
        reach = new
        if reach & 1:
            return True
    return bool(reach & 1)


def sieve(N, verbose=True, use_isolated=True):
    """Iterate to a fixed point:
         (a) q-sieve (lemma above);
         (b) legality: an allowed n whose both  neighbours are banned can never be used
             (it would be an isolated point of U), so ban it too.
       (b) is legitimate because U has no isolated point and U is contained in the
       current universe."""
    P = primes_upto(N)
    allowed = set(range(2, N + 1))
    reasons = {}
    changed = True
    while changed:
        changed = False
        for q in P:
            while True:
                lvl = {}
                for n in allowed:
                    e = nu(n, q)
                    if e:
                        lvl.setdefault(e, []).append(n)
                if not lvl:
                    break
                E = max(lvl)
                vals = [pow(n // q ** E, q - 2, q) % q for n in lvl[E]]
                if zero_subset_sum_possible(vals, q):
                    break
                for n in lvl[E]:
                    allowed.discard(n)
                    reasons[n] = (q, E)
                changed = True
        if use_isolated:
            iso = [n for n in allowed if (n - 1) not in allowed and (n + 1) not in allowed]
            if iso:
                for n in iso:
                    allowed.discard(n)
                    reasons[n] = ("isolated", 0)
                changed = True
    banned = sorted(set(range(2, N + 1)) - allowed)
    if verbose:
        print("N=%d  universe size %d / %d" % (N, len(allowed), N - 1))
        print("  banned:", banned)
        A = sorted(allowed)
        # maximal runs of survivors
        runs = []
        cur = [A[0]]
        for x in A[1:]:
            if x == cur[-1] + 1:
                cur.append(x)
            else:
                runs.append((cur[0], cur[-1]))
                cur = [x]
        runs.append((cur[0], cur[-1]))
        runs2 = [r for r in runs if r[1] > r[0]]
        print("  survivor runs of length>=2:", runs2)
        print("  largest possible max(U): ",
              max((b for a, b in runs2), default=None))
    return allowed


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    sieve(N)
