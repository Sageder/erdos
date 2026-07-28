#!/usr/bin/env python3
"""
verify_lemma.py -- exact verification of LEMMA 1 of forced.py on the whole
solution corpus, and of the derived threshold kmin(p).

For every solution U in the corpus and every prime p with p*p > max(U):
  * let a_1..a_k be the cofactors n/p of the multiples of p in U;
  * check  k = 0  or  p | e_{k-1}(a)  (LEMMA 1);
  * check  k >= kmin(p, max U)        (COROLLARY 2);
  * record the sharpness  k - kmin(p).

Exact integer arithmetic only.
usage: verify_lemma.py FILE [FILE...]
"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import primes_upto
from forced import esym, kmin


def load(path):
    sols = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if not p:
                continue
            if p[0] == "SOL":
                p = p[1:]
            try:
                U = [int(x) for x in p]
            except ValueError:
                continue
            if U:
                sols.append(sorted(U))
    return sols


def main():
    sols = []
    for path in sys.argv[1:]:
        sols += load(path)
    print("solutions:", len(sols))
    bad = 0
    slack = Counter()
    kmincache = {}
    checked = 0
    for U in sols:
        N = max(U)
        for p in primes_upto(N):
            if p * p <= N:
                continue
            M = [n for n in U if n % p == 0]
            k = len(M)
            if k == 0:
                continue
            a = [n // p for n in M]
            e = esym(a, k - 1)
            if e % p != 0:
                print("LEMMA 1 FAILS:", U, p, a)
                bad += 1
            if (p, N) not in kmincache:
                kmincache[(p, N)] = kmin(p, N)
            km = kmincache[(p, N)]
            if km is None or k < km:
                print("COROLLARY 2 FAILS:", U, p, k, km)
                bad += 1
            else:
                slack[k - km] += 1
            checked += 1
    print("prime-instances checked:", checked, " failures:", bad)
    print("distribution of k - kmin(p) over all used primes p > sqrt(max U):")
    for d in sorted(slack):
        print(f"   k-kmin = {d:>3} : {slack[d]}")


if __name__ == "__main__":
    main()
