"""
Q4 / Q3 -- the CORRECTION-CANCELLATION mechanism.

IDENTITY (verified in q5_identities.py).  For every n >= 1, with
m = ceil(n/2):
      H(n,n+1) = 1/n + 1/(n+1) = 1/m + sigma(n)/(n(n+1)),
      sigma(n) = +1 if n is odd,   sigma(n) = -1 if n is even.
Indeed  n=2m-1 :  1/(2m-1)+1/(2m) = 1/m + 1/((2m-1)2m);
        n=2m   :  1/(2m)+1/(2m+1) = 1/m - 1/(2m(2m+1)).

Consequence.  Let N be a set of integers >= 2 that are pairwise at distance
>= 2 (so the blocks [n,n+1], n in N, are pairwise DISJOINT).  The map
n -> m = ceil(n/2) is injective on such an N.  Hence

      sum_{n in N} H(n,n+1)  =  sum_{n in N} 1/ceil(n/2)  +  Delta(N),
      Delta(N) := sum_{n in N} sigma(n)/(n(n+1)) .

So: if Delta(N) = 0, the block sum is EXACTLY the Egyptian fraction
sum_{n in N} 1/ceil(n/2) with pairwise distinct denominators.

This script searches exhaustively for sets N with Delta(N) = 0.

The search is a signed subset-sum with the perfect telescoping bound
      sum_{n >= n0} 1/(n(n+1)) = 1/n0,
so at position n0 with residue r we may prune whenever |r| > 1/n0.  That makes
the DFS complete for a given range [nmin, nmax] and very fast.

Run:  python3 q4_correction_cancel.py 2 60
"""

import sys
from fractions import Fraction


def search_delta_zero(nmin, nmax, want=50, need_gap=2):
    """
    All nonempty N subset [nmin,nmax], consecutive elements differing by
    >= need_gap, with sum_{n in N} sigma(n)/(n(n+1)) = 0.
    Complete for the given range.
    """
    sols = []
    c = {n: Fraction(1, n * (n + 1)) for n in range(nmin, nmax + 2)}
    sig = {n: (1 if n % 2 else -1) for n in range(nmin, nmax + 2)}
    nodes = 0

    def dfs(n, r, cur):
        nonlocal nodes
        nodes += 1
        if r == 0 and cur:
            sols.append(list(cur))
            if len(sols) >= want:
                return True
            return False
        if n > nmax:
            return False
        # |remaining achievable| <= sum_{k>=n} 1/(k(k+1)) = 1/n
        if abs(r) > Fraction(1, n):
            return False
        # take n
        cur.append(n)
        if dfs(n + need_gap, r + sig[n] * c[n], cur):
            cur.pop()
            return True
        cur.pop()
        # skip n
        return dfs(n + 1, r, cur)

    dfs(nmin, Fraction(0), [])
    return sols, nodes


def report(N):
    from fractions import Fraction as F
    blocks = [(n, n + 1) for n in N]
    s = sum((F(1, x) + F(1, x + 1) for x in N), F(0))
    ms = [(n + 1) // 2 if n % 2 else n // 2 for n in N]
    egy = sum((F(1, m) for m in ms), F(0))
    delta = sum(((1 if n % 2 else -1) * F(1, n * (n + 1)) for n in N), F(0))
    return blocks, s, ms, egy, delta


if __name__ == "__main__":
    nmin = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    want = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    sols, nodes = search_delta_zero(nmin, nmax, want)
    print("Delta(N)=0 search, N subset [%d,%d], gap>=2 ; nodes=%d, found=%d"
          % (nmin, nmax, nodes, len(sols)))
    for N in sols:
        blocks, s, ms, egy, delta = report(N)
        assert delta == 0
        assert s == egy
        print("   N=%s" % N)
        print("      blocks   %s" % (blocks,))
        print("      sum      %s   =  sum of 1/m over m=%s" % (s, ms))
