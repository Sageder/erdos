#!/usr/bin/env python3
"""Rule (P) and its corollaries checked on EVERY solution of the corpus.

For each solution U and each prime p dividing some element:
  (1) nu_p( sum_{n in U, p|n} 1/n ) >= 0      [Rule (P)]
  (2) at least two elements attain E = max nu_p(n)
  (3) 2*p^{nu_p(n)} <= max(U) for every n in U and every p | n   [Corollary]
  (4) max(U) is not prime and max(U)-1 is not prime               [reported claim O10]
  (5) top run [c,N]: 2c > N and [c,N] contains no prime
Exact arithmetic only.
"""
from fractions import Fraction

ALLSOLS = "/home/user/erdos/experiments/ALLSOLS.txt"
NMAX = 400
s = bytearray([1]) * (NMAX + 1)
s[0:2] = b"\x00\x00"
i = 2
while i * i <= NMAX:
    if s[i]:
        s[i * i:: i] = bytearray(len(s[i * i:: i]))
    i += 1
PR = [i for i in range(2, NMAX + 1) if s[i]]
isprime = s


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


bad1 = bad2 = bad3 = bad5 = 0
bad4 = []
cnt = 0
for line in open(ALLSOLS):
    t = line.split()
    if not t or t[0] != "SOL":
        continue
    U = [int(x) for x in t[1:]]
    cnt += 1
    N = U[-1]
    for p in PR:
        if p > N:
            break
        mult = [n for n in U if n % p == 0]
        if not mult:
            continue
        E = max(nu(n, p) for n in mult)
        if sum(1 for n in mult if nu(n, p) == E) < 2:
            bad2 += 1
        S = sum(Fraction(1, n) for n in mult)
        if S.denominator % p == 0:
            bad1 += 1
        for n in mult:
            if 2 * p ** nu(n, p) > N:
                bad3 += 1
    if isprime[N] or isprime[N - 1]:
        bad4.append(N)
    # top run
    c = N
    Us = set(U)
    while c - 1 in Us:
        c -= 1
    if 2 * c <= N or any(isprime[x] for x in range(c, N + 1)):
        bad5 += 1

print("solutions checked           :", cnt)
print("(1) Rule (P) violations     :", bad1)
print("(2) unique-top-attainer     :", bad2)
print("(3) corollary 2p^e<=N fails :", bad3)
print("(4) max(U) or max(U)-1 prime:", sorted(set(bad4)))
print("(5) top-run violations      :", bad5)
