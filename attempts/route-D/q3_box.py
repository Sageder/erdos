"""
Q3 -- box search.   Decide (exhaustively inside the box) whether

     rho  =  sum_{n in U} 1/n ,   U subset [T,X],  U has no isolated point,
     every maximal run of U has length <= LMAX.

Enumeration is over MAXIMAL RUNS in increasing order, so each U appears once.
All arithmetic exact (Fraction).

PRUNES (each rigorous):
  P1  0 <= r  and  r <= H(pos,X)          (everything left cannot exceed this)
  P2  the next run [a,b] needs 1/a+1/(a+1) <= r, i.e. a >= amin(r)
  P3  denominator prune: for every prime power q = p^e || den(r) there must be
      a multiple of q inside [pos,X].
      (If v_p(n) < e for all remaining n, then v_p(sum) > -e, so v_p(r) > -e.)
  P4  2-adic prune: r != 0 forces  -v_2(r) <= log2(X).

Run:
   python3 q3_box.py 1 2 200 2          # rho=1, T=2, X=200, runs of length <=2
   python3 q3_box.py 1/20 7 4000 3
"""

import sys
from fractions import Fraction


def prime_powers(m):
    out = []
    d = 2
    while d * d <= m:
        if m % d == 0:
            e = 1
            m //= d
            while m % d == 0:
                m //= d
                e += 1
            out.append(d ** e)
        d += 1 if d == 2 else 2
    if m > 1:
        out.append(m)
    return out


class Box:
    def __init__(self, T, X, lmax, want=1, node_cap=None):
        self.T, self.X, self.lmax = T, X, lmax
        self.want = want
        self.node_cap = node_cap
        # tail[n] = H(n,X)
        self.tail = [Fraction(0)] * (X + 2)
        for n in range(X, T - 1, -1):
            self.tail[n] = self.tail[n + 1] + Fraction(1, n)
        self.sols = []
        self.nodes = 0
        self.capped = False

    def tailsum(self, n):
        if n > self.X:
            return Fraction(0)
        return self.tail[max(n, self.T)]

    def feasible_den(self, r, pos):
        for q in prime_powers(r.denominator):
            if q > self.X:
                return False
            if (self.X // q) * q < pos:
                return False
        return True

    def run(self, rho):
        self.sols = []
        self.nodes = 0
        self.capped = False
        self._dfs(Fraction(rho), self.T, [])
        return self.sols

    def _dfs(self, r, pos, cur):
        self.nodes += 1
        if self.node_cap and self.nodes > self.node_cap:
            self.capped = True
            return True
        if r == 0:
            self.sols.append(list(cur))
            return len(self.sols) >= self.want
        if r < 0 or pos > self.X - 1:
            return False
        if r > self.tailsum(pos):
            return False
        if not self.feasible_den(r, pos):
            return False
        for a in range(pos, self.X):
            if r > self.tailsum(a):
                return False
            h = Fraction(1, a)
            b = a
            while b < self.X and b - a + 1 < self.lmax:
                b += 1
                h += Fraction(1, b)
                if h > r:
                    break
                cur.append((a, b))
                if self._dfs(r - h, b + 2, cur):
                    cur.pop()
                    return True
                cur.pop()
        return False


def verify(sol, rho, T, X):
    U = []
    for a, b in sol:
        U.extend(range(a, b + 1))
    assert len(U) == len(set(U))
    assert min(U) >= T and max(U) <= X
    s = sum((Fraction(1, n) for n in U), Fraction(0))
    assert s == Fraction(rho), (s, rho)
    srt = sorted(U)
    for i, n in enumerate(srt):
        assert (i > 0 and srt[i - 1] == n - 1) or (i + 1 < len(srt) and srt[i + 1] == n + 1)
    return True


if __name__ == "__main__":
    rho = Fraction(sys.argv[1])
    T = int(sys.argv[2])
    X = int(sys.argv[3])
    lmax = int(sys.argv[4])
    want = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    cap = int(sys.argv[6]) if len(sys.argv) > 6 else None
    B = Box(T, X, lmax, want=want, node_cap=cap)
    sols = B.run(rho)
    print("rho=%s T=%d X=%d maxrunlen=%d  nodes=%d capped=%s"
          % (rho, T, X, lmax, B.nodes, B.capped))
    for s in sols:
        verify(s, rho, T, X)
        print("   SOLUTION runs=%s" % (s,))
    if not sols:
        print("   NONE" + (" (search truncated)" if B.capped else " (exhaustive in box)"))
