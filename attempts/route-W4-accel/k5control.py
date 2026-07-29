"""k5control.py -- CALIBRATION CONTROL.

The same horizon-extended cut system, but for monotone k-APs with k = 5, where a
counterexample is KNOWN ([DEGS77](b); CORE Theorem 21 gives the explicit
permutation: blocks [4^m, 4^{m+1}) concatenated, van der Corput inside, reversed
on odd blocks).  That permutation has 4^m - 1 as a cut for every m.  Therefore the
k=5 analogue of the pair system MUST be satisfiable for pairs such as (15,63),
(63,255), (15,255).  If the machinery declared them UNSAT, the encoding (or the
soundness argument) would be wrong.

This is the Remark-17 discipline: run the method on the branch whose answer is
known and check the signature does not appear there.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
sys.path.insert(0, "/home/user/erdos/experiments")
import wsys
from itertools import combinations


class SysK(wsys.Sys):
    """same layout/variables; C1 over monotone k-APs, C2 over (k-1)-prefixes."""

    def __init__(self, cuts, M=None, window=None, k=4):
        super().__init__(cuts, M, window)
        self.k = k

    def clauses(self, transitivity=True):
        M, Vk, k = self.M, self.Vk, self.k
        cls, dead = [], []
        for d in range(1, (M - 1) // (k - 1) + 1):
            for x in range(1, M - (k - 1) * d + 1):
                q = tuple(x + j * d for j in range(k))
                for seq in (q, q[::-1]):
                    c = self.chain(seq)
                    if c is None or c == 'DROP':
                        continue
                    (dead if not c else cls).append(('C1', seq) if not c else c)
        for d in range(1, Vk // (k - 2) + 1):
            for x in range(1, Vk - (k - 2) * d + 1):
                if x + (k - 1) * d <= M:
                    continue
                c = self.chain(tuple(x + j * d for j in range(k - 1)))
                if c is None or c == 'DROP':
                    continue
                (dead if not c else cls).append(('C2', x, d) if not c else c)
        if transitivity:
            cls.extend(self.trans_clauses())
        return cls, dead


def vdc4(n):
    """van der Corput style index used only to build the reference permutation."""
    return n


def degs_perm(mmax):
    """CORE Thm 21's 5-AP-free permutation, first 4^mmax values, in position order.
    Blocks [4^m,4^{m+1}) with the base-4 van der Corput order inside, reversed on
    odd m."""
    seq = [1, 2, 3]
    for m in range(1, mmax):
        lo, hi = 4 ** m, 4 ** (m + 1)
        blk = sorted(range(lo, hi), key=lambda v: _revbits(v, 2 * (m + 1) + 4))
        if m % 2 == 1:
            blk = blk[::-1]
        seq.extend(blk)
    return seq


def _revbits(v, width):
    """van der Corput key: compare binary expansions least-significant-bit first."""
    r = 0
    for _ in range(width):
        r = r * 2 + (v & 1)
        v >>= 1
    return r


def solve(cuts, M, k, window=None, cap=900):
    S = SysK(cuts, M, window=window, k=k)
    v, o = wsys.solve_lazy(S, time_cap=cap, tag=f"k{k}{cuts}@{M}")
    if v == 'GEOM_DEAD':
        v = 'UNSAT'
    return v, o


if __name__ == '__main__':
    from apcheck import has_monotone_kap_general
    print("# reference: does CORE Thm21's permutation really avoid monotone 5-APs?")
    p = degs_perm(5)          # values 1..1023
    print(f"   prefix of {len(p)} values, monotone 5-AP present: "
          f"{has_monotone_kap_general(p[:400], 5)}")
    cuts_found = [c for c in (3, 15, 63, 255) if set(p[:c]) == set(range(1, c + 1))]
    print(f"   cuts among (3,15,63,255) verified present: {cuts_found}")

    print("# CONTROL: k=5 pair systems that MUST be satisfiable")
    for (W, U, M) in [(15, 63, 189), (15, 63, 315), (3, 15, 45), (15, 63, 400),
                      (63, 255, 765)]:
        t0 = time.time()
        v, _ = solve((W, U), M, 5)
        print(f"   k=5  N({W},{U},{M}) -> {v} [{time.time()-t0:.0f}s]"
              f"{'   *** FALSE UNSAT: encoding bug' if v == 'UNSAT' else ''}",
              flush=True)

    print("# and the k=4 signature on the SAME pairs (for contrast)")
    for (W, U, M) in [(15, 63, 189), (15, 63, 315)]:
        t0 = time.time()
        v, _ = solve((W, U), M, 4)
        print(f"   k=4  N({W},{U},{M}) -> {v} [{time.time()-t0:.0f}s]", flush=True)
