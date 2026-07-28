"""
structure.py -- after reduction, the surviving universe A(N) is a union of maximal
runs of consecutive integers.  A legal U is obtained by choosing, independently in
each run, a subset with no isolated point *inside that run* (elements adjacent to a
run boundary have their outside neighbour banned, so runs never interact).

f(L) = # binary strings of length L with no isolated 1  = size of the choice set of
a run of length L.  The whole search space therefore has size prod_i f(L_i).

Prints, for each N, the run lengths and the total search-space size -- the number
that decides which algorithm is needed.
"""
import sys
from reduce import reduce_universe, lcm_of


def runs_of(A):
    runs = []
    cur = [A[0]]
    for x in A[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append((cur[0], cur[-1]))
            cur = [x]
    runs.append((cur[0], cur[-1]))
    return runs


def f_counts(maxL):
    # number of binary strings of length n with no isolated 1
    # state: 0 = last char 0, 1 = last char 1 and run of 1s has length 1 (unsafe),
    #        2 = last char 1 and run of 1s has length >= 2 (safe)
    from functools import lru_cache

    @lru_cache(None)
    def g(n, st):
        if n == 0:
            return 0 if st == 1 else 1
        tot = 0
        if st != 1:
            tot += g(n - 1, 0)          # place 0
        if st == 0:
            tot += g(n - 1, 1)          # start new run of 1s
        else:
            tot += g(n - 1, 2)          # extend run of 1s
        return tot

    return [g(n, 0) for n in range(maxL + 1)]


def run_configs(a, b):
    """all legal subsets of the run [a,b] (no isolated point inside the run)"""
    L = b - a + 1
    out = []
    for mask in range(1 << L):
        ok = True
        for i in range(L):
            if (mask >> i) & 1:
                left = i > 0 and ((mask >> (i - 1)) & 1)
                right = i < L - 1 and ((mask >> (i + 1)) & 1)
                if not left and not right:
                    ok = False
                    break
        if ok:
            out.append(tuple(a + i for i in range(L) if (mask >> i) & 1))
    return out


if __name__ == "__main__":
    Ns = [int(a) for a in sys.argv[1:]] or [80, 90, 100, 110, 120, 130, 140, 150,
                                            160, 180, 200, 220, 250, 300]
    F = f_counts(64)
    for N in Ns:
        A, _ = reduce_universe(N)
        if not A:
            print(f"N={N:4d}  UNIVERSE EMPTY -> no solution with max(U) <= {N}")
            continue
        rs = runs_of(A)
        Ls = [b - a + 1 for a, b in rs]
        tot = 1
        for L in Ls:
            tot *= F[L]
        Lc = lcm_of(A)
        print(f"N={N:4d} |A|={len(A):4d} runs={len(rs):3d} maxrun={max(Ls):3d} "
              f"space={tot:.4g} log2={tot.bit_length()} Ldigits={len(str(Lc))}")
        print(f"      runs={rs}")
        print(f"      lens={Ls}")
