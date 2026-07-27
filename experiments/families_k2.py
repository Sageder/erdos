"""Test the k=2 ansatz families and the auto-fail/auto-pass discoveries (NOTES 2026-07-27).

Claims tested:
 (F1) density of {X in [A,B] : X^2-2 in S_2} — the quadratic ansatz baseline;
 (F2) density of {z in [C,D] : z^4-2 in S_2} — the quartic ansatz (Discovery 2);
 (F3) Discovery 1a: q || X-1, q odd prime, 2(X-1)^2 < q^3, q not dividing other window parts
      ==> membership FAILS at q. Verified exhaustively in the F1 range.
 (F4) Discovery 1c: P(X) > X^{2/3} (largest prime factor, q||X, single-digit quotient regime
      q^3 > X^2) ==> FAILS at q. Verified exhaustively in the F1 range.
 (F5) failure-source histogram for the quartic family: which primes fail, at what
      beta = log q / log m (m = z^4), and which window element they divide.

Conclusion printed at end.
"""
import sys, math
from collections import Counter
sys.path.insert(0, '.')
from erdos727 import s_p, in_Sk_fast, failing_primes
from sympy import factorint, sieve

def cond_at(n, k, p):
    return 2 * s_p(n + k, p) - s_p(2 * n, p) >= 2 * k

# ---- F1: quadratic ansatz density
A, B = 300, 1500
quad_hits = []
for X in range(A, B + 1):
    n = X * X - 2
    if in_Sk_fast(n, 2):
        quad_hits.append(X)
print(f"F1 quadratic ansatz: {len(quad_hits)}/{B-A+1} hits "
      f"({100*len(quad_hits)/(B-A+1):.2f}%) first: {quad_hits[:12]}", flush=True)

# ---- F2: quartic ansatz density
C, D = 18, 260
quart_hits = []
quart_fail_data = []
for z in range(C, D + 1):
    n = z ** 4 - 2
    if in_Sk_fast(n, 2):
        quart_hits.append(z)
    else:
        fps = failing_primes(n, 2)
        quart_fail_data.append((z, fps))
print(f"F2 quartic ansatz: {len(quart_hits)}/{D-C+1} hits "
      f"({100*len(quart_hits)/(D-C+1):.2f}%) hits: {quart_hits[:20]}", flush=True)

# ---- F3: auto-fail at q || X-1 with 2(X-1)^2 < q^3
viol3 = []
checked3 = 0
for X in range(A, B + 1):
    n = X * X - 2
    fac = factorint(X - 1)
    for q, e in fac.items():
        if q > 3 and e == 1 and 2 * (X - 1) ** 2 < q ** 3:
            checked3 += 1
            if cond_at(n, 2, q):
                viol3.append((X, q))
print(f"F3 auto-fail q||X-1 (2(X-1)^2<q^3): {checked3} cases, violations: {viol3[:5]} "
      f"{'PASS' if not viol3 else 'FAIL'}", flush=True)

# ---- F4: auto-fail at q || X with q^3 > X^2
viol4 = []
checked4 = 0
for X in range(A, B + 1):
    n = X * X - 2
    fac = factorint(X)
    for q, e in fac.items():
        if q > 3 and e == 1 and q ** 3 > X ** 2:
            checked4 += 1
            if cond_at(n, 2, q):
                viol4.append((X, q))
print(f"F4 auto-fail q||X (q^3>X^2): {checked4} cases, violations: {viol4[:5]} "
      f"{'PASS' if not viol4 else 'FAIL'}", flush=True)

# ---- F5: failure histogram for quartic family
hist = Counter()
beta_buckets = Counter()
for z, fps in quart_fail_data:
    n = z ** 4 - 2
    m = n + 2  # = z^4
    for q in fps:
        # which window-related element does q divide?
        srcs = []
        if (z - 1) % q == 0: srcs.append('z-1')
        if (z + 1) % q == 0: srcs.append('z+1')
        if z % q == 0: srcs.append('z')
        if (z * z + 1) % q == 0: srcs.append('z^2+1')
        if n % q == 0: srcs.append('n')  # n = m-2 window shifted? n+1..n+2 = m-1, m
        if (2 * n + 1) % q == 0: srcs.append('2n+1')
        if (2 * n + 3) % q == 0: srcs.append('2n+3')
        if not srcs: srcs.append('none')
        beta = math.log(q) / math.log(m)
        bb = round(beta * 10) / 10
        hist['+'.join(srcs)] += 1
        beta_buckets[bb] += 1
print(f"F5 failure sources (quartic): {dict(hist)}", flush=True)
print(f"F5 failure beta histogram (beta=log q/log m rounded to 0.1): "
      f"{dict(sorted(beta_buckets.items()))}", flush=True)
# per-z failure counts
cnts = Counter(len(fps) for _, fps in quart_fail_data)
print(f"F5 #failing-primes-per-failing-z histogram: {dict(sorted(cnts.items()))}", flush=True)
print(f"F5 small-prime (p<=13) failures: "
      f"{sum(1 for _, fps in quart_fail_data for q in fps if q <= 13)} "
      f"of {sum(len(f) for _, f in quart_fail_data)} total failing-prime instances", flush=True)
