#!/usr/bin/env python3
"""
targets.py -- "for which rationals q does a LEGAL U (no isolated point,
U subset Z_{>=2}) with sum_{n in U} 1/n = q exist, and with what max element?"

For each target q we scan N upwards, prune the universe with the
target-generalised RULE A + RULE B, and run the exact DFS (dfs3) for sum = q.
Reports the least N with a legal solution, and the witness.

This is the diagnostic asked for in the task: if legal U's realise many
rationals but never 1, that would localise an obstruction.
"""
import sys, subprocess
sys.path.insert(0, '/home/user/erdos/attempts/route-C')
from prune import prune
from fractions import Fraction

BIN = '/home/user/erdos/attempts/route-C/dfs3'


def first_hit(q, Nmax=140, tmo=300):
    for N in range(4, Nmax + 1):
        A = prune(N, True, target=q)
        if not A:
            continue
        S = set(A)
        if not (N in S and N - 1 in S):
            continue
        inp = (f"{N} 0 1 0 0 {q.numerator} {q.denominator}\n"
               f"{len(A)}\n{' '.join(map(str,A))}\n")
        try:
            r = subprocess.run([BIN], input=inp, capture_output=True, text=True, timeout=tmo)
        except subprocess.TimeoutExpired:
            return ('timeout', N, None)
        for l in r.stdout.split('\n'):
            if l.startswith('SOL'):
                U = [int(x) for x in l.split()[1:]]
                if max(U) == N:
                    assert sum(Fraction(1, n) for n in U) == q
                    ST = set(U)
                    assert all((n - 1) in ST or (n + 1) in ST for n in U)
                    return ('found', N, U)
    return ('none', Nmax, None)


if __name__ == "__main__":
    qs = [Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4),
          Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5),
          Fraction(1, 6), Fraction(5, 6), Fraction(1, 7), Fraction(1, 8),
          Fraction(5, 4), Fraction(4, 3), Fraction(3, 2), Fraction(5, 3), Fraction(7, 4),
          Fraction(1), Fraction(2), Fraction(5, 2), Fraction(3)]
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 140
    print(f"q          status   least max(U)   witness   (scan N<={Nmax})")
    for q in qs:
        st, N, U = first_hit(q, Nmax)
        print(f"{str(q):8s}  {st:8s} {N if st=='found' else '-':>6}   {U}", flush=True)
