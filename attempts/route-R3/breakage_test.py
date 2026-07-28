"""k=2 breakage experiments.

B1: For every k=1 family member n = pq-1, the k=2 condition can only fail at primes
    dividing n+2 = pq+1 (at p, q the requirement is unchanged and already met).
B2: Classify failures: large primes ell | n+2 with ell > sqrt(2n) (automatic death),
    vs medium/small primes failing the carry condition.
B3: Pell parametrization n+1 = x^2, n+2 = 2y^2 (x^2 - 2y^2 = -1) and
    n+1 = 2y^2, n+2 = x^2 (x^2 - 2y^2 = +1): valuation doubling should kill it.
B4: Conditional repair: pq + 1 = 2rs with
      q,p,s,r prime, q >= 3, s >= 5,
      (3q+1)/2 <= p <= 2q-1,
      2s+1 <= r <= 4s-1,
      (2r mod s) >= (s+1)/2,
      n = pq - 1 not a power of 2
    ==> n in S_2.  Verify every found solution.
"""
from math import isqrt
from sympy import primerange, isprime, factorint
from membership import in_Sk, carries, failing_primes
from family_test import family_pairs

# ---------- B1 + B2 ----------
tot = 0
in_s2 = 0
fail_at_large = 0     # some failing prime ell | n+2 with ell^2 > 2n
fail_only_medium = 0  # all failing primes are <= sqrt(2n)
bad_B1 = []
med_examples = []
for q, p in family_pairs(300):
    n = p * q - 1
    tot += 1
    if in_Sk(n, 2):
        in_s2 += 1
        continue
    fails = failing_primes(n, 2)
    f2 = factorint(n + 2)
    for ell, d in fails:
        if (n + 1) % ell == 0 or (n + 2) % ell not in (0,):
            if (n + 2) % ell != 0:
                bad_B1.append((n, ell))
    if any(ell * ell > 2 * n for ell, _ in fails):
        fail_at_large += 1
    else:
        fail_only_medium += 1
        if len(med_examples) < 8:
            med_examples.append((n, q, p, factorint(n + 2), fails))
print(f"B1: family members q<=300: {tot}; failing primes not dividing n+2: {bad_B1[:5]}"
      f" ({len(bad_B1)} total; empty list = B1 confirmed)")
print(f"B2: in S_2: {in_s2} ({in_s2/tot:.1%}); killed by prime > sqrt(2n) in n+2: "
      f"{fail_at_large} ({fail_at_large/tot:.1%}); "
      f"n+2 smooth but carries fail: {fail_only_medium} ({fail_only_medium/tot:.1%})")
print("   medium-failure examples (n, q, p, factor(n+2), failing (prime, 2s_p(n+2)-s_p(2n))):")
for e in med_examples:
    print("   ", e)

# ---------- B3: Pell (small solutions; full slow criterion + carry-deficit analysis) ----------
# Larger Pell ranges (30 solutions each sign) are in breakage_test2.py via the fast
# equivalent criterion; here every membership verdict uses the verbatim PROBLEM.md
# all-primes criterion, so the range is capped at n < 2*10^7.
print("\nB3: Pell chains")
# x^2 - 2y^2 = -1: (x,y) = (1,1),(7,5),(41,29),... x_{k+1}=3x+4y, y_{k+1}=2x+3y
x, y = 1, 1
pell_neg = []
while x < 10**9:
    x, y = 3 * x + 4 * y, 2 * x + 3 * y
    pell_neg.append((x, y))
for x, y in pell_neg:
    n = x * x - 2           # n+1 = x^2, n+2 = 2y^2
    ok = in_Sk(n, 2) if n < 2 * 10**7 else None   # None = deferred to fast test (B3')
    fx, fy = factorint(x), factorint(y)
    # deficit analysis: at ell^e || x need 4e carries (nu_ell(n+1)=2e); at ell^e || y
    # (odd ell) need 4e carries too (nu_ell(n+2)=2e); supply is carries(n,n,ell)
    defic = []
    for ell, e in fx.items():
        c = carries(n, n, ell)
        if c < 4 * e:
            defic.append((ell, e, c))
    for ell, e in fy.items():
        if ell == 2:
            continue
        c = carries(n, n, ell)
        if c < 4 * e:
            defic.append((ell, e, c))
    print(f"   x={x} y={y} n=x^2-2: in S_2? {ok}; x={fx}, y={fy}; "
          f"carry-deficient primes (ell, nu, carries<4nu): {defic}")
    if ok is not None:
        assert ok == (not defic and bin(n).count('1') >= 2 * (1 + fy.get(2, 0))), (x, y)
x, y = 3, 2
pell_pos = []
while x < 10**9:
    pell_pos.append((x, y))
    x, y = 3 * x + 4 * y, 2 * x + 3 * y
for x, y in pell_pos:
    n = x * x - 2           # n+1 = 2y^2, n+2 = x^2
    ok = in_Sk(n, 2) if n < 2 * 10**7 else None
    print(f"   x={x} y={y} n=x^2-2 (n+1=2y^2,n+2=x^2): in S_2? {ok}")

# ---------- B4: conditional repair ----------
# Small range (q <= 1000), every solution verified by the verbatim PROBLEM.md
# all-primes criterion. The q <= 4000 search with fast criterion + sampled slow
# re-checks is in breakage_test2.py (B4').
print("\nB4: solutions of pq+1=2rs with all carry conditions, q <= 1000 (slow criterion)")
sols = []
near = 0
for q, p in family_pairs(1000):
    n = p * q - 1
    m2 = (n + 2) // 2
    assert (n + 2) % 2 == 0
    f = factorint(m2)
    if sum(f.values()) != 2 or len(f) != 2:
        continue
    s, r = sorted(f)          # s < r, both nu=1
    near += 1
    if s < 5:
        continue
    if not (2 * s + 1 <= r <= 4 * s - 1):
        continue
    if (2 * r) % s < (s + 1) // 2 + (0 if s % 2 == 0 else 0):
        # (s+1)/2 with s odd prime: integer (s+1)//2
        continue
    if n & (n - 1) == 0:
        continue
    sols.append((q, p, s, r, n))
print(f"   semiprime n+2=2rs (r,s distinct odd primes) among family members q<=1000: {near}")
print(f"   full-condition solutions found: {len(sols)}")
allok = all(in_Sk(n, 2) for _, _, _, _, n in sols)
print(f"   ALL such n in S_2: {allok}")
for t in sols[:12]:
    print("   ", t)
if not allok:
    for t in sols:
        if not in_Sk(t[4], 2):
            print("   COUNTEREXAMPLE:", t, failing_primes(t[4], 2))
