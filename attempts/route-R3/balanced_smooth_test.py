"""Carry-budget vs number of prime factors of n+2 (the F-II/F-III taxonomy).

For t = 1..6 build n+2 = 2 * prod_{i<=t} p_i^{e_i} (p_i = first t odd primes, exponents
balanced so n+2 ~ target size), and test ONLY the n+2-side conditions:
    s_2(n) >= 2*nu_2(n+2)  and  carries_{p_i}(n+n) >= 2*e_i for each i.
(The n+1 side is ignored here; this isolates how hard the even-neighbour side is.)

Prediction from the digit-supply argument: demand at p_i is 2*e_i ~ (2/t)*log_{p_i}(n)
while supply is at most log_{p_i}(n) digits, of which a ~kappa fraction carry
(kappa ~ 0.4-0.6); so t <= 2 should be (near) impossible, and the success rate should
become positive and grow with t.
"""
import random
from math import log
from membership import carries

def s2(m):
    return bin(m).count("1")

random.seed(7)
PRIMES = [3, 5, 7, 11, 13, 17]
TARGET = 10 ** 10
SAMPLES = 3000

for t in range(1, 7):
    ps = PRIMES[:t]
    ok = 0
    fail_who = {p: 0 for p in ps}
    fail2 = 0
    for _ in range(SAMPLES):
        # balanced exponents with jitter
        es = []
        for p in ps:
            base = log(TARGET) / t / log(p)
            e = max(1, int(round(base * random.uniform(0.7, 1.3))))
            es.append(e)
        m = 2
        for p, e in zip(ps, es):
            m *= p ** e
        n = m - 2
        good = True
        if s2(n) < 2:  # nu_2(n+2)=1
            good = False
            fail2 += 1
        for p, e in zip(ps, es):
            if carries(n, n, p) < 2 * e:
                good = False
                fail_who[p] += 1
        if good:
            ok += 1
    print(f"t={t}: n+2-side success rate {ok/SAMPLES:.3%}; "
          f"per-prime failure rates: " +
          ", ".join(f"{p}:{fail_who[p]/SAMPLES:.0%}" for p in ps))
