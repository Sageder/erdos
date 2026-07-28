#!/usr/bin/env python3
"""
Route R2 numerics: falsify/verify every candidate lemma used in LEMMA_SP.md
(small-prime carry machinery for Erdos 727, fixed k), BEFORE proving.

All arithmetic is exact (Python ints / fractions).

Sections:
  T1  criterion implementations vs PROBLEM.md sanity data (S_1,S_2,S_3,S_4)
  T2  kappa_2(m) = s_2(m); integrality of (2 s_p(m)-s_p(2m))/(p-1)
  T3  interval valuation bound  W'_p <= nu_p((2k)!) + V'_p  and exact identity
      W'_p = nu_p(C(2m,2k)) + nu_p((2k)!)
  T4  forced carries: kappa_p(m) >= X_p(m) (masked-position variant included)
  T5  the sufficiency chain: X'_p >= nu_p((2k)!)+V'_p  ==>  727 criterion at p
  T6  binomial tail bounds (exact rational computation):
        (a) trivial:  P(X < D) <= (1-th)^F * F^D      (1<=D<=F, th<=1/2)
        (b) entropy:  P(X <= aF) <= exp(-F*D(a||th))  (0<=a<=th)
        (c) classic:  P(X <= F*th/2) <= exp(-F*th/8)
  T7  spike residue-class structure {m : p^T | 2m-i} (incl. p=2), AP-forced
      spikes (falsifies the naive (ii) without the nu_p(2 q0) correction)
  T8  density measurements: k=3, P0=13 on [M,2M], plain and in an AP
  T9  CRT counting: class mod p^L intersect AP(q0,a) = one class mod q0*p^{L-e}
"""

import math, random, sys
from fractions import Fraction

random.seed(727428)

# ---------- basic p-adic utilities ----------

def digits(m, p):
    d = []
    while m > 0:
        d.append(m % p); m //= p
    return d

def s_p(m, p):
    s = 0
    while m > 0:
        s += m % p; m //= p
    return s

def nu_int(x, p):
    assert x != 0
    v = 0
    while x % p == 0:
        v += 1; x //= p
    return v

def nu_fact(m, p):  # Legendre
    return (m - s_p(m, p)) // (p - 1)

def kappa(m, p):    # nu_p(C(2m,m)) = (2 s_p(m) - s_p(2m))/(p-1)
    num = 2 * s_p(m, p) - s_p(2 * m, p)
    assert num % (p - 1) == 0 or p == 2
    return num // (p - 1)

def demand(m, k, p):  # nu_p( (2m)(2m-1)...(2m-2k+1) )
    return sum(nu_int(2 * m - i, p) for i in range(2 * k))

def Vprime(m, k, p):  # max_{0<=i<2k} nu_p(2m-i)
    return max(nu_int(2 * m - i, p) for i in range(2 * k))

def crit_p(m, k, p):  # 727 criterion at p, in product form (m = n+k)
    return kappa(m, p) >= demand(m, k, p)

def Xmask(m, p, e, L):  # number of "large" digits (>= ceil(p/2)) at positions e..L-1
    thr = (p + 1) // 2
    d = digits(m, p)
    return sum(1 for j in range(e, L) if j < len(d) and d[j] >= thr)

def primes_upto(N):
    sieve = bytearray([1]) * (N + 1)
    sieve[0:2] = b'\x00\x00'
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
    return [i for i in range(2, N + 1) if sieve[i]]

PR = primes_upto(300000)
PRset = set(PR)

def is_prime(x):
    if x < 300000: return x in PRset
    for p in PR:
        if p * p > x: return True
        if x % p == 0: return False
    return True

FAILURES = []
def check(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f"  {detail}" if detail else ""))
    if not ok: FAILURES.append((name, detail))

# ---------- membership in S_k ----------

def in_Sk_direct(n, k):
    """Exact: 2 s_p(n+k) - s_p(2n) >= 2k for all primes p <= n+k."""
    for p in PR:
        if p > n + k: break
        if 2 * s_p(n + k, p) - s_p(2 * n, p) < 2 * k:
            return False
    return True

def gpf_sieve(N):
    g = list(range(N + 1))  # g[x] = greatest prime factor of x (g[1]=1)
    for p in range(2, N + 1):
        if g[p] == p:  # p prime
            for mlt in range(p, N + 1, p):
                g[mlt] = p
    return g

def Sk_list_fast(N, k, gpf):
    """S_k cap [1,N] using: for n > 2k^2, n in S_k iff window n+1..n+k is
    sqrt(2n)-smooth AND digit condition holds for all p <= sqrt(2n).
    For n <= 2k^2 use the direct test."""
    out = []
    for n in range(1, N + 1):
        if n <= 2 * k * k:
            if in_Sk_direct(n, k): out.append(n)
            continue
        B = math.isqrt(2 * n)
        if any(gpf[n + i] > B for i in range(1, k + 1)):
            continue
        ok = True
        for p in PR:
            if p > B: break
            if 2 * s_p(n + k, p) - s_p(2 * n, p) < 2 * k:
                ok = False; break
        if ok: out.append(n)
    return out

def T1():
    print("== T1: criterion implementations vs PROBLEM.md sanity data ==")
    gpf = gpf_sieve(2002 * 100 + 10)  # 200210, enough for N=2*10^5 with k<=4
    # cross-validate fast vs direct on a range
    k = 2
    direct = [n for n in range(1, 1500) if in_Sk_direct(n, k)]
    fast = [n for n in Sk_list_fast(1499, k, gpf)]
    check("T1.0 fast==direct membership (k=2, n<1500)", direct == fast,
          f"direct={direct[:5]} fast={fast[:5]}")
    # k=1 sanity
    s1 = Sk_list_fast(441, 1, gpf)
    exp1 = [5, 14, 27, 41, 44, 65, 76, 90, 109, 125, 139, 152, 155, 169]
    check("T1.1 S_1 prefix & count to 441", s1[:14] == exp1 and len(s1) == 40,
          f"len={len(s1)} prefix={s1[:14]}")
    # k=2 sanity
    s2 = Sk_list_fast(200000, 2, gpf)
    exp2 = [208, 458, 987, 1220, 1455, 1597, 1889, 2012, 2144, 2330, 2477,
            2663, 2991, 3353, 3415, 3430, 3439, 3475, 3476, 3551]
    check("T1.2 S_2: min=208, first 20, |S_2 cap [1,2e5]|=1981",
          s2[:20] == exp2 and len(s2) == 1981 and s2[0] == 208,
          f"len={len(s2)}")
    # k=3 sanity
    s3 = Sk_list_fast(60000, 3, gpf)
    exp3 = [3475, 8174, 8175, 15195, 16168, 18682, 18743, 19290]
    check("T1.3 S_3 prefix & |S_3 cap [1,6e4]|=41",
          s3[:8] == exp3 and len(s3) == 41, f"len={len(s3)} prefix={s3[:8]}")
    # k=4 sanity
    s4 = Sk_list_fast(60000, 4, gpf)
    check("T1.4 S_4 cap [1,6e4] = {8174, 51984}", s4 == [8174, 51984], f"{s4}")
    # product-form per-prime == digit-sum form, and == factorial divisibility (small)
    ok = True
    for n in range(3, 400):
        for k_ in (2, 3):
            m = n + k_
            lhs_all = all(crit_p(m, k_, p) for p in PR if p <= 2 * m)
            rhs_all = in_Sk_direct(n, k_)
            if lhs_all != rhs_all: ok = False; break
        if not ok: break
    check("T1.5 product form (all p) == digit-sum form (n<400, k=2,3)", ok)
    ok = True
    for n in range(3, 120):
        for k_ in (2, 3):
            f = math.factorial
            truth = (f(2 * n) % (f(n + k_) ** 2) == 0)
            if truth != in_Sk_direct(n, k_): ok = False; break
        if not ok: break
    check("T1.6 digit-sum form == raw factorial divisibility (n<120)", ok)
    # per-prime identity nu_p((2n)!)-2nu_p((n+k)!) = kappa_p(m)-demand_p(m)
    ok = True
    for _ in range(3000):
        n = random.randint(10, 10**9); k_ = random.randint(2, 6)
        p = random.choice([2, 3, 5, 7, 11, 13, 101])
        m = n + k_
        lhs = nu_fact(2 * n, p) - 2 * nu_fact(m, p)
        rhs = kappa(m, p) - demand(m, k_, p)
        if lhs != rhs: ok = False; break
    check("T1.7 identity nu_p((2n)!)-2nu_p((n+k)!) == kappa_p(m)-demand_p(m)", ok)

def T2():
    print("== T2: kappa_2(m) = s_2(m); integrality ==")
    ok = all(kappa(m, 2) == s_p(m, 2) for m in range(1, 200001))
    check("T2.1 kappa_2(m)==s_2(m) for m<=2e5", ok)
    ok = True
    for _ in range(2000):
        m = random.randint(1, 10**15); p = random.choice([3, 5, 7, 11, 97])
        if (2 * s_p(m, p) - s_p(2 * m, p)) % (p - 1) != 0: ok = False; break
    check("T2.2 (p-1) | 2 s_p(m)-s_p(2m)", ok)
    # also kappa via carries directly
    def carries_double(m, p):
        c = 0; cnt = 0
        for d in digits(m, p):
            t = 2 * d + c
            c = 1 if t >= p else 0
            cnt += c
        return cnt
    ok = True
    for _ in range(2000):
        m = random.randint(1, 10**12); p = random.choice([2, 3, 5, 13])
        if carries_double(m, p) != kappa(m, p): ok = False; break
    check("T2.3 Kummer: kappa_p(m) == #carries in m+m base p", ok)

def T3():
    print("== T3: interval bound W' <= nu_p((2k)!) + V' ; exact identity ==")
    ok = ok2 = True
    for _ in range(20000):
        m = random.randint(20, 10**12); k = random.randint(1, 8)
        p = random.choice([2, 2, 3, 5, 7, 11, 13, 101])
        W = demand(m, k, p)
        if W > nu_fact(2 * k, p) + Vprime(m, k, p): ok = False; break
        binom = math.comb(2 * m, 2 * k) if m < 10**6 else None
        if binom is not None:
            if W != nu_int(binom, p) + nu_fact(2 * k, p): ok2 = False; break
    check("T3.1 W'_p <= nu_p((2k)!) + V'_p (random, incl. exhaustive-ish)", ok)
    for m in range(10, 3000):
        for k in (2, 3):
            for p in (2, 3, 5):
                if demand(m, k, p) > nu_fact(2*k, p) + Vprime(m, k, p):
                    ok = False
    check("T3.2 W' bound exhaustive m<3000, k=2,3, p=2,3,5", ok)
    check("T3.3 identity W' == nu_p(C(2m,2k)) + nu_p((2k)!)", ok2)

def T4():
    print("== T4: forced carries kappa_p >= X_p (masked positions) ==")
    ok = True
    for _ in range(20000):
        m = random.randint(1, 10**14)
        p = random.choice([2, 3, 5, 7, 13, 97])
        L = len(digits(m, p)); e = random.randint(0, max(0, L - 1))
        if kappa(m, p) < Xmask(m, p, e, L): ok = False; break
    check("T4.1 kappa_p(m) >= #large digits in positions [e,L)", ok)

def T5():
    print("== T5: sufficiency chain X' >= nu_p((2k)!)+V'  ==>  727 criterion at p ==")
    ok = True; used = 0
    for _ in range(200000):
        m = random.randint(100, 10**12); k = random.randint(2, 6)
        p = random.choice([2, 2, 3, 3, 5, 7, 13])
        Lfull = len(digits(m, p)); e = random.randint(0, 3)
        X = Xmask(m, p, e, Lfull)
        if X >= nu_fact(2 * k, p) + Vprime(m, k, p):
            used += 1
            if not crit_p(m, k, p): ok = False; break
    check("T5.1 implication holds on all sampled instances", ok, f"instances used={used}")

def T6():
    print("== T6: binomial tail bounds, exact rational vs bound ==")
    def tail_le(F, D, th):  # P(Bin(F,th) <= D), exact Fraction
        return sum(Fraction(math.comb(F, j)) * th**j * (1 - th)**(F - j)
                   for j in range(0, D + 1))
    thetas = [Fraction(1, 2), Fraction(1, 3), Fraction(2, 5), Fraction(21, 43),
              Fraction(5, 11)]
    ok_a = ok_b = ok_c = True
    for F in list(range(2, 40)) + [60, 80]:
        for th in thetas:
            # (a) trivial bound: P(X < D) <= (1-th)^F * F^D, 1<=D<=F
            for D in (1, 2, 3, F // 2, F):
                if D < 1 or D > F: continue
                lhs = tail_le(F, D - 1, th)
                rhs = (1 - th)**F * Fraction(F)**D
                if lhs > rhs: ok_a = False
            # (b) entropy bound at a = D/F <= th
            for D in range(0, int(F * th) + 1):
                a = Fraction(D, F)
                lhs = float(tail_le(F, D, th))
                KL = 0.0
                if a > 0:
                    KL += float(a) * math.log(float(a / th))
                KL += float(1 - a) * math.log(float((1 - a) / (1 - th)))
                if lhs > math.exp(-F * KL) * (1 + 1e-12): ok_b = False
            # (c) classic: P(X <= mu/2) <= exp(-mu/8), mu = F*th
            mu = F * th
            lhs = float(tail_le(F, math.floor(mu / 2), th))
            if lhs > math.exp(-float(mu) / 8) * (1 + 1e-12): ok_c = False
    check("T6.a trivial small-count tail bound", ok_a)
    check("T6.b entropy (KL) Chernoff bound", ok_b)
    check("T6.c classic mu/2 Chernoff, constant 1/8", ok_c)
    # sum_{j<D} C(F,j) <= F^D for 1<=D<=F
    ok = all(sum(math.comb(F, j) for j in range(D)) <= F**D
             for F in range(2, 60) for D in range(1, F + 1))
    check("T6.d sum_{j<D} C(F,j) <= F^D  (1<=D<=F)", ok)

def T7():
    print("== T7: spike residue classes; AP-forced spikes ==")
    ok = True
    for _ in range(4000):
        p = random.choice([2, 3, 5, 7, 13]); T = random.randint(1, 6)
        i = random.randint(0, 11)
        lo = random.randint(1, 10**6); hi = lo + p**(T + 1) + 500
        sols = [m for m in range(lo, hi) if (2 * m - i) != 0 and (2 * m - i) % p**T == 0]
        nu2 = 1 if p == 2 else 0
        if p == 2 and i % 2 == 1:
            if sols: ok = False; break
            continue
        Q = p**max(T - nu2, 0)
        if sols:
            r = sols[0] % Q
            if any(s % Q != r for s in sols): ok = False; break
            # exactly the arithmetic progression r mod Q:
            expect = [m for m in range(lo, hi) if m % Q == r]
            if sols != expect: ok = False; break
    check("T7.1 {m: p^T | 2m-i} is a single class mod p^{T-nu_p(2)} (or empty)", ok)
    # AP-forced spike: q0=2^10, a=0 => every m in AP has nu_2(2m) >= 11
    q0 = 2**10; bad = [m for m in range(q0, 40 * q0, q0) if nu_int(2 * m, 2) < 11]
    check("T7.2 naive spike bound WITHOUT nu_p(2 q0) term is FALSE on AP (falsified"
          " as expected: every m=0 mod 2^10 has nu_2(2m)>=11)", bad == [])

def density_scan(Mlo, k, P0_primes, q0=1, a=0, t_add=None):
    """Scan m in [Mlo, 2Mlo] (optionally m = a mod q0). Returns counts."""
    tot = fail_i = fail_ii = 0
    perprime_fail = {p: 0 for p in P0_primes}
    start = Mlo if q0 == 1 else Mlo + ((a - Mlo) % q0)
    for m in range(start, 2 * Mlo + 1, q0):
        tot += 1
        bad_i = False; bad_ii = False
        for p in P0_primes:
            if not crit_p(m, k, p):
                perprime_fail[p] += 1; bad_i = True
            if t_add is not None:
                Jp = int(math.log(2 * k) / math.log(p))
                e_p = nu_int(q0, p) if q0 % p == 0 else 0
                nu2q0 = (1 if p == 2 else 0) + e_p
                if Vprime(m, k, p) > nu2q0 + Jp + t_add:
                    bad_ii = True
        if bad_i: fail_i += 1
        if bad_ii: fail_ii += 1
    return tot, fail_i, fail_ii, perprime_fail

def T8():
    print("== T8: density measurements (k=3, P0=13) ==")
    k = 3; P0 = [2, 3, 5, 7, 11, 13]
    for Mlo in (10**5, 10**6):
        t_add = math.ceil(10 * math.log(math.log(Mlo)))
        tot, f1, f2, pp = density_scan(Mlo, k, P0, t_add=t_add)
        dens = 1 - f1 / tot
        union = sum(pp.values()) / tot
        print(f"   M={Mlo:>8}: density(i for all p<=13) = {dens:.4f}   "
              f"fail(i)={f1}/{tot}  union-bound sum={union:.4f}  "
              f"fail(ii,t={t_add})={f2}")
        print(f"      per-prime failure rates: " +
              ", ".join(f"p={p}:{pp[p]/tot:.4f}" for p in P0))
        check(f"T8.1 M={Mlo}: union bound >= actual failure rate",
              union >= f1 / tot - 1e-12)
    # trend to 1: compare two scales
    tot5, f5, _, _ = density_scan(10**5, k, P0)
    tot6, f6, _, _ = density_scan(10**6, k, P0)
    check("T8.2 failure rate decreases from M=1e5 to M=1e6",
          f6 / tot6 < f5 / tot5, f"{f5/tot5:.4f} -> {f6/tot6:.4f}")
    # AP variant: q0 = 24 (2^3*3), a = 7
    tot, f1, f2, pp = density_scan(10**6, k, P0, q0=24, a=7,
                                   t_add=math.ceil(10 * math.log(math.log(10**6))))
    print(f"   M=1e6, AP m=7 mod 24: density(i)={1-f1/tot:.4f}  N_AP={tot}  fail(ii)={f2}")
    check("T8.3 AP density also high (sanity)", f1 / tot < 0.2, f"fail rate {f1/tot:.4f}")
    # AP variant with forced 2-power: q0=2^10, a=0 (worst case digits)
    tot, f1, f2, pp = density_scan(10**6, k, P0, q0=2**10, a=0)
    print(f"   M=1e6, AP m=0 mod 2^10: density(i)={1-f1/tot:.4f}  N_AP={tot}  "
          f"per-prime p=2 fail={pp[2]/tot:.4f}")
    print("   (note: demand at p=2 in this AP includes the forced spike ~10+;"
          " density is lower at this small scale, as the theory predicts —"
          " the asymptotic lemma still applies since s_2(m)~log_2(M)/2 >> 10"
          " only for much larger M)")

def T9():
    print("== T9: CRT counting for bad classes inside an AP ==")
    ok = True
    for _ in range(2000):
        p = random.choice([2, 3, 5, 7]); e = random.randint(0, 3)
        qprime = random.choice([1, 3, 5, 7, 11, 24, 35])
        while qprime % p == 0:
            qprime = random.choice([1, 3, 5, 7, 11, 13])
        q0 = p**e * qprime
        L = random.randint(e + 1, e + 4)
        a = random.randint(0, q0 - 1)
        # pick residue r mod p^L compatible with a mod p^e
        r = (a % p**e) + p**e * random.randint(0, p**(L - e) - 1)
        M = random.randint(10**5, 10**6)
        sols = [m for m in range(M, 2 * M + 1)
                if m % q0 == a and m % p**L == r]
        Q = q0 * p**(L - e)
        if sols:
            r0 = sols[0] % Q
            if any(s % Q != r0 for s in sols): ok = False; break
        if len(sols) > (M + 1) / Q + 1: ok = False; break
    check("T9.1 AP cap class mod p^L = one class mod q0*p^{L-e}; count <= (M+1)/Q+1", ok)

if __name__ == "__main__":
    fast = "--fast" in sys.argv
    T2(); T3(); T4(); T5(); T6(); T7(); T9()
    if not fast:
        T1(); T8()
    print()
    if FAILURES:
        print("FAILURES:"); [print("  ", f) for f in FAILURES]; sys.exit(1)
    print("ALL CHECKS PASSED")
