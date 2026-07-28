"""Verify every internal digit claim of Lemma R (conditional k=2 lemma) on all
solutions found in breakage_test2.py, and re-verify membership.

Lemma R hypotheses: primes q >= 3, s >= 5, p in [(3q+1)/2, 2q-1], r in [2s+1, 4s-1],
pq + 1 = 2rs, (2r mod s) >= (s+1)/2, n := pq - 1 not a power of 2.
Digit claims used in the proof:
  base p: n = (q-1)p + (p-1),           carries at pos 0,1
  base q: n = q^2 + (p-q-1)q + (q-1),   carries at pos 0,1
  base r: n = (2s-1)r + (r-2),          carries at pos 0,1
  base s: n = A s^2 + (b-1)s + (s-2), A=floor(2r/s), b=2r mod s;  carries at pos 0,1
  base 2: c_2(n) = s_2(n) >= 2
"""
from sympy import factorint
from membership import in_Sk, carries
from family_test import family_pairs

def digits(n, p, k):
    return [(n // p**i) % p for i in range(k)]

sols = []
for q, p in family_pairs(4000):
    n = p * q - 1
    m2 = (n + 2) // 2
    f = factorint(m2)
    if len(f) != 2 or set(f.values()) != {1}:
        continue
    s, r = sorted(f)
    if s < 5 or not (2 * s + 1 <= r <= 4 * s - 1):
        continue
    if (2 * r) % s < (s + 1) // 2:
        continue
    if n & (n - 1) == 0:
        continue
    sols.append((q, p, s, r, n))

assert len(sols) == 123
for q, p, s, r, n in sols:
    # base p
    assert digits(n, p, 2) == [p - 1, q - 1] and n < p * p * ((q-1)+1)
    assert 2 * (p - 1) >= p and 2 * (q - 1) + 1 >= p
    # base q
    rq = p - q
    assert digits(n, q, 3) == [q - 1, rq - 1, 1]
    assert 2 * (q - 1) >= q and 2 * (rq - 1) + 1 >= q
    # base r
    assert digits(n, r, 2) == [r - 2, 2 * s - 1]
    assert 2 * (r - 2) >= r and 2 * (2 * s - 1) + 1 >= r
    # base s
    A, b = divmod(2 * r, s)
    assert b >= 1
    assert digits(n, s, 2) == [s - 2, b - 1]
    assert n // (s * s) == A
    assert 2 * (s - 2) >= s and 2 * (b - 1) + 1 >= s
    # base 2
    assert bin(n).count("1") >= 2
    # actual carry counts meet demands 2 at each of p,q,r,s and 2 at 2
    for ell in (p, q, r, s):
        assert carries(n, n, ell) >= 2, (q, p, s, r, ell)
    # and full membership once more (fast criterion is equivalent, but use full for n small)
    fh = factorint(n + 1); gh = factorint(n + 2)
    assert fh == {q: 1, p: 1} and gh == {2: 1, s: 1, r: 1}
    for ell in set(fh) | set(gh):
        assert carries(n, n, ell) >= 2 * fh.get(ell, 0) + 2 * gh.get(ell, 0)
print(f"Lemma R digit claims verified on all {len(sols)} solutions: OK")
# full slow criterion on the 5 smallest
for t in sols[:5]:
    assert in_Sk(t[4], 2)
print("full PROBLEM.md criterion re-confirmed on 5 smallest solutions: OK")
