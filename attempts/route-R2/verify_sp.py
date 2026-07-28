#!/usr/bin/env python3
"""
Route R2 numerics: falsify/verify every candidate lemma used in LEMMA_SP.md
(small-prime carry machinery for Erdos 727, fixed k), BEFORE proving.

All arithmetic is exact (Python ints / fractions); floats appear only in
reporting and in checks of purely-real-analytic inequalities (with margins).

Sections (test numbers match the citations in LEMMA_SP.md):
  T1  criterion implementations vs PROBLEM.md sanity data (S_1,S_2,S_3,S_4)
  T2  kappa_2(m) = s_2(m); integrality; Kummer carry count
  T3  interval valuation bound  W_p <= nu_p((2k)!) + V_p  and exact identity
      W_p = nu_p(C(2m,2k)) + nu_p((2k)!)
  T4  forced carries: kappa_p(m) >= X_p^{[e,L)}(m) (masked positions)
  T5  sufficiency chain: X^{[e,L)} >= nu_p((2k)!)+V_p  ==>  727 criterion at p
  T6  binomial tail bounds (exact rational computation):
        (a) trivial:  P(X < D) <= (1-th)^F * F^D      (1<=D<=F, th<=1/2)
        (b) entropy:  P(X <= aF) <= exp(-F*D(a||th))  (0<=a<=th)
        (c) classic:  P(X <= mu/2) <= exp(-mu/8),  mu = F*th
  T7  spike residue-class structure {m : p^T | 2m-i} (incl. p=2); AP-forced
      spikes (falsifies the naive (ii) WITHOUT the nu_p(2 q0) correction)
  T8  density measurements: k=3, P0=13 on [M,2M], plain and in APs
      (incl. q0 = 2^10 with the corrected spike threshold)
  T9  CRT counting: class mod p^L intersect AP(q0,a) = one class mod q0*p^{L-e}
  T10 in-AP masked sufficiency chain, exhaustive at M = 2*10^5
  T11 threshold lemma SP.9 and the scalar inequalities behind E(M)
  T12 (part of T8 output) union-bound consistency
  T13 large-scale sampling test of the packaged lemma at M = 2^64..10^60:
      exact per-instance threshold check, then (C_p & S_p for all p) ==> (i),
      plus empirical failure rates vs the proved Chernoff/spike bounds
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
    assert p == 2 or num % (p - 1) == 0
    return num // (p - 1)

def demand(m, k, p):  # W_p(m) = nu_p( (2m)(2m-1)...(2m-2k+1) )
    return sum(nu_int(2 * m - i, p) for i in range(2 * k))

def Vprime(m, k, p):  # V_p(m) = max_{0<=i<2k} nu_p(2m-i)
    return max(nu_int(2 * m - i, p) for i in range(2 * k))

def crit_p(m, k, p):  # 727 criterion at p, product form (m = n+k)
    return kappa(m, p) >= demand(m, k, p)

def Xmask(m, p, e, L):  # number of "large" digits (>= ceil(p/2)) at positions e..L-1
    thr = (p + 1) // 2
    d = digits(m, p)
    return sum(1 for j in range(e, L) if j < len(d) and d[j] >= thr)

def theta(p):  # exact probability that a uniform base-p digit is >= ceil(p/2)
    return Fraction(p // 2, p)

def primes_upto(N):
    sieve = bytearray([1]) * (N + 1)
    sieve[0:2] = b'\x00\x00'
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
    return [i for i in range(2, N + 1) if sieve[i]]

PR = primes_upto(300000)
PRset = set(PR)

FAILURES = []
def check(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f"  {detail}" if detail else ""), flush=True)
    if not ok: FAILURES.append((name, detail))

# ---------- fast array builders (exact integer arithmetic) ----------

def sp_array(N, p):
    """sp[m] = s_p(m) for 0 <= m <= N (bytearray; values < 256 for N <= 4e6)."""
    sp = bytearray(N + 1)
    for m in range(min(p, N + 1)):
        sp[m] = m
    for q in range(1, N // p + 1):
        base = q * p; v = sp[q]
        top = min(p, N + 1 - base)
        for r in range(top):
            sp[base + r] = v + r
    return sp

def nu_array(N, p):
    """nu[x] = nu_p(x) for 1 <= x <= N (nu[0] unused)."""
    nu = bytearray(N + 1)
    for x in range(p, N + 1, p):
        nu[x] = nu[x // p] + 1
    return nu

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
        if g[p] == p:
            for mlt in range(p, N + 1, p):
                g[mlt] = p
    return g

def Sk_list_fast(N, k, gpf):
    """S_k cap [1,N]: for n > 2k^2 use smooth-window + digit criterion for
    p <= sqrt(2n) (PROBLEM.md large-prime criterion); direct test otherwise."""
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
    gpf = gpf_sieve(200210)
    k = 2
    direct = [n for n in range(1, 1200) if in_Sk_direct(n, k)]
    fast = [n for n in Sk_list_fast(1199, k, gpf)]
    check("T1.0 fast==direct membership (k=2, n<1200)", direct == fast,
          f"direct={direct[:5]} fast={fast[:5]}")
    s1 = Sk_list_fast(441, 1, gpf)
    exp1 = [5, 14, 27, 41, 44, 65, 76, 90, 109, 125, 139, 152, 155, 169]
    check("T1.1 S_1 prefix & count to 441", s1[:14] == exp1 and len(s1) == 40,
          f"len={len(s1)} prefix={s1[:14]}")
    s2 = Sk_list_fast(200000, 2, gpf)
    exp2 = [208, 458, 987, 1220, 1455, 1597, 1889, 2012, 2144, 2330, 2477,
            2663, 2991, 3353, 3415, 3430, 3439, 3475, 3476, 3551]
    check("T1.2 S_2: min=208, first 20, |S_2 cap [1,2e5]|=1981",
          s2[:20] == exp2 and len(s2) == 1981 and s2[0] == 208,
          f"len={len(s2)}")
    s3 = Sk_list_fast(60000, 3, gpf)
    exp3 = [3475, 8174, 8175, 15195, 16168, 18682, 18743, 19290]
    check("T1.3 S_3 prefix & |S_3 cap [1,6e4]|=41",
          s3[:8] == exp3 and len(s3) == 41, f"len={len(s3)} prefix={s3[:8]}")
    s4 = Sk_list_fast(60000, 4, gpf)
    check("T1.4 S_4 cap [1,6e4] = {8174, 51984}", s4 == [8174, 51984], f"{s4}")
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
    ok = True
    for _ in range(3000):
        n = random.randint(10, 10**9); k_ = random.randint(2, 6)
        p = random.choice([2, 3, 5, 7, 11, 13, 101])
        m = n + k_
        lhs = nu_fact(2 * n, p) - 2 * nu_fact(m, p)
        rhs = kappa(m, p) - demand(m, k_, p)
        if lhs != rhs: ok = False; break
    check("T1.7 identity nu_p((2n)!)-2nu_p((n+k)!) == kappa_p(m)-W_p(m)", ok)

def T2():
    print("== T2: kappa_2(m) = s_2(m); integrality; Kummer ==")
    ok = all(kappa(m, 2) == s_p(m, 2) for m in range(1, 200001))
    check("T2.1 kappa_2(m)==s_2(m) for m<=2e5", ok)
    ok = True
    for _ in range(2000):
        m = random.randint(1, 10**15); p = random.choice([3, 5, 7, 11, 97])
        if (2 * s_p(m, p) - s_p(2 * m, p)) % (p - 1) != 0: ok = False; break
    check("T2.2 (p-1) | 2 s_p(m)-s_p(2m)", ok)
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
    print("== T3: interval bound W <= nu_p((2k)!) + V ; exact identity ==")
    ok = ok2 = True
    for _ in range(20000):
        m = random.randint(20, 10**12); k = random.randint(1, 8)
        p = random.choice([2, 2, 3, 5, 7, 11, 13, 101])
        W = demand(m, k, p)
        if W > nu_fact(2 * k, p) + Vprime(m, k, p): ok = False; break
        binom = math.comb(2 * m, 2 * k) if m < 10**6 else None
        if binom is not None:
            if W != nu_int(binom, p) + nu_fact(2 * k, p): ok2 = False; break
    check("T3.1 W_p <= nu_p((2k)!) + V_p (random)", ok)
    for m in range(10, 3000):
        for k in (2, 3):
            for p in (2, 3, 5):
                if demand(m, k, p) > nu_fact(2*k, p) + Vprime(m, k, p):
                    ok = False
    check("T3.2 W bound exhaustive m<3000, k=2,3, p=2,3,5", ok)
    check("T3.3 identity W_p == nu_p(C(2m,2k)) + nu_p((2k)!)", ok2)

def T4():
    print("== T4: forced carries kappa_p >= X_p^{[e,L)} (masked positions) ==")
    ok = True
    for _ in range(20000):
        m = random.randint(1, 10**14)
        p = random.choice([2, 3, 5, 7, 13, 97])
        L = len(digits(m, p)); e = random.randint(0, max(0, L - 1))
        if kappa(m, p) < Xmask(m, p, e, L): ok = False; break
    check("T4.1 kappa_p(m) >= #large digits in positions [e,L)", ok)

def T5():
    print("== T5: chain X^{[e,L)} >= nu_p((2k)!)+V_p ==> 727 criterion at p ==")
    ok = True; used = 0
    for _ in range(200000):
        m = random.randint(100, 10**12); k = random.randint(2, 6)
        p = random.choice([2, 2, 3, 3, 5, 7, 13])
        Lfull = len(digits(m, p)); e = random.randint(0, 3)
        X = Xmask(m, p, e, Lfull)
        if X >= nu_fact(2 * k, p) + Vprime(m, k, p):
            used += 1
            if not crit_p(m, k, p): ok = False; break
    check("T5.1 implication holds on all sampled instances", ok,
          f"instances used={used}")

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
            for D in (1, 2, 3, F // 2, F):
                if D < 1 or D > F: continue
                lhs = tail_le(F, D - 1, th)
                rhs = (1 - th)**F * Fraction(F)**D
                if lhs > rhs: ok_a = False
            for D in range(0, int(F * th) + 1):
                a = Fraction(D, F)
                lhs = float(tail_le(F, D, th))
                KL = 0.0
                if a > 0:
                    KL += float(a) * math.log(float(a / th))
                KL += float(1 - a) * math.log(float((1 - a) / (1 - th)))
                if lhs > math.exp(-F * KL) * (1 + 1e-12): ok_b = False
            mu = F * th
            lhs = float(tail_le(F, math.floor(mu / 2), th))
            if lhs > math.exp(-float(mu) / 8) * (1 + 1e-12): ok_c = False
    check("T6.a trivial small-count tail bound", ok_a)
    check("T6.b entropy (KL) Chernoff bound", ok_b)
    check("T6.c classic mu/2 Chernoff, constant 1/8 (P(X<=mu/2)<=e^{-mu/8})", ok_c)
    ok = all(sum(math.comb(F, j) for j in range(D)) <= F**D
             for F in range(2, 60) for D in range(1, F + 1))
    check("T6.d sum_{j<D} C(F,j) <= F^D  (1<=D<=F)", ok)

def T7():
    print("== T7: spike residue classes; AP-forced spikes ==")
    ok = True
    for _ in range(1500):
        p = random.choice([2, 3, 5, 7, 13])
        T = random.randint(1, 6)
        while p**T > 5000:
            T -= 1
        i = random.randint(0, 11)
        lo = random.randint(1, 10**6); hi = lo + 3 * p**T + 500
        sols = [m for m in range(lo, hi) if (2 * m - i) % p**T == 0]
        if p == 2 and i % 2 == 1:
            if sols: ok = False; break
            continue
        nu2 = 1 if p == 2 else 0
        Q = p**max(T - nu2, 0)
        if sols:
            r = sols[0] % Q
            expect = [m for m in range(lo, hi) if m % Q == r]
            if sols != expect: ok = False; break
    check("T7.1 {m: p^T | 2m-i} is a single class mod p^{T-nu_p(2)} (or empty)",
          ok)
    q0 = 2**10
    bad = [m for m in range(q0, 40 * q0, q0) if nu_int(2 * m, 2) < 11]
    check("T7.2 naive spike bound WITHOUT nu_p(2 q0) term is FALSE on AP "
          "(every m=0 mod 2^10 has nu_2(2m)>=11, as the corrected lemma "
          "predicts)", bad == [])

# ---------- fast density scan ----------

def density_scan(Mlo, k, P0_primes, q0=1, a=0, t_add=None):
    """Scan m in [Mlo, 2Mlo] with m = a mod q0 (exact arithmetic via sieved
    arrays). Spike threshold (if t_add given): nu_p(2 q0) + J_p + t_add.
    Returns (tot, #fail(i), #fail(ii), per-prime fail(i) counts)."""
    Mhi = 2 * Mlo
    start = Mlo + ((a - Mlo) % q0)
    ms = list(range(start, Mhi + 1, q0))
    n = len(ms)
    bad_i = bytearray(n); bad_ii = bytearray(n)
    perprime_fail = {}
    N2 = 2 * Mhi + 2
    for p in P0_primes:
        sp = sp_array(N2, p); nu = nu_array(N2, p)
        pm1 = p - 1
        Jp = 0
        while p**(Jp + 1) <= 2 * k: Jp += 1
        e_p = nu_int(q0, p) if q0 % p == 0 else 0
        nu2q0 = e_p + (1 if p == 2 else 0)
        thr = nu2q0 + Jp + (t_add if t_add is not None else 0)
        pf = 0
        twok = 2 * k
        for idx, m in enumerate(ms):
            m2 = 2 * m
            dem = 0; V = 0
            for i in range(twok):
                v = nu[m2 - i]
                dem += v
                if v > V: V = v
            if 2 * sp[m] - sp[m2] < pm1 * dem:   # kappa < demand
                pf += 1; bad_i[idx] = 1
            if t_add is not None and V > thr:
                bad_ii[idx] = 1
        perprime_fail[p] = pf
        del sp, nu
    return n, sum(bad_i), sum(bad_ii), perprime_fail

def T8():
    print("== T8: density measurements (k=3, P0=13); union-bound check ==")
    k = 3; P0 = [2, 3, 5, 7, 11, 13]
    rates = []
    for Mlo in (10**5, 10**6):
        t_add = math.ceil(math.log(math.log(Mlo)))
        tot, f1, f2, pp = density_scan(Mlo, k, P0, t_add=t_add)
        dens = 1 - f1 / tot
        union = sum(pp.values()) / tot
        rates.append(f1 / tot)
        print(f"   M={Mlo:>8}: density(i for all p<=13) = {dens:.4f}   "
              f"fail(i)={f1}/{tot}  union-bound sum={union:.4f}  "
              f"fail(ii,t={t_add})={f2} ({f2/tot:.4f})")
        print("      per-prime fail(i) rates: " +
              ", ".join(f"p={p}:{pp[p]/tot:.4f}" for p in P0))
        check(f"T8.1 M={Mlo}: union bound >= actual failure rate",
              union >= f1 / tot - 1e-12)
    check("T8.2 fail(i) rate decreases from M=1e5 to M=1e6",
          rates[1] < rates[0], f"{rates[0]:.4f} -> {rates[1]:.4f}")
    t_add = math.ceil(math.log(math.log(10**6)))
    tot, f1, f2, pp = density_scan(10**6, k, P0, q0=24, a=7, t_add=t_add)
    print(f"   M=1e6, AP m=7 mod 24: density(i)={1-f1/tot:.4f}  N_AP={tot}  "
          f"fail(ii)={f2}")
    check("T8.3 AP density also high (sanity)", f1 / tot < 0.2,
          f"fail rate {f1/tot:.4f}")
    tot, f1, f2, pp = density_scan(10**6, k, P0, q0=2**10, a=0, t_add=t_add)
    print(f"   M=1e6, AP m=0 mod 2^10: density(i)={1-f1/tot:.4f}  N_AP={tot}  "
          f"p=2 fail(i)={pp[2]/tot:.4f}  fail(ii, corrected thr)={f2}")
    check("T8.4 corrected spike threshold (with nu_2(2 q0)=11) makes fail(ii) "
          "rare even in AP mod 2^10", f2 / tot < 0.1, f"{f2/tot:.4f}")
    print("   (note: density(i) in the 2^10-AP is lower at this small scale "
          "because the forced demand at p=2 is ~11+ while s_2(m)~10 on "
          "average here; the lemma's threshold requires larger M in this AP, "
          "exactly as SP.9 predicts)")

def T9():
    print("== T9: CRT counting for bad classes inside an AP ==")
    ok = True
    for _ in range(500):
        p = random.choice([2, 3, 5, 7]); e = random.randint(0, 3)
        qprime = random.choice([1, 3, 5, 7, 11, 24, 35])
        while qprime % p == 0:
            qprime = random.choice([1, 3, 5, 7, 11, 13])
        q0 = p**e * qprime
        L = random.randint(e + 1, e + 4)
        a = random.randint(0, q0 - 1)
        r = (a % p**e) + p**e * random.randint(0, p**(L - e) - 1)
        M = random.randint(2 * 10**4, 6 * 10**4)
        start = M + ((a - M) % q0)
        sols = [m for m in range(start, 2 * M + 1, q0) if m % p**L == r]
        Q = q0 * p**(L - e)
        if sols:
            r0 = sols[0] % Q
            if any(s % Q != r0 for s in sols): ok = False; break
        if len(sols) > (M + 1) / Q + 1: ok = False; break
    check("T9.1 AP cap class mod p^L = one class mod q0*p^{L-e}; "
          "count <= (M+1)/Q + 1", ok)

def T10():
    print("== T10: in-AP masked sufficiency chain, exhaustive ==")
    Mlo = 2 * 10**5; k = 3; P0 = [2, 3, 5, 7, 11, 13]
    ok = True; used = 0
    for (q0, a) in [(24, 7), (1024, 512), (405, 17)]:
        start = Mlo + ((a - Mlo) % q0)
        for m in range(start, 2 * Mlo + 1, q0):
            for p in P0:
                e_p = nu_int(q0, p) if q0 % p == 0 else 0
                Lfull = len(digits(m, p))
                X = Xmask(m, p, e_p, Lfull)
                if X >= nu_fact(2 * k, p) + Vprime(m, k, p):
                    used += 1
                    if not crit_p(m, k, p):
                        ok = False
                        print(f"   VIOLATION q0={q0} a={a} m={m} p={p}")
    check("T10.1 in-AP: X^{[e_p,*)} >= nu_p((2k)!)+V_p ==> criterion at p "
          "(exhaustive, three APs)", ok, f"instances used={used}")

def T11():
    print("== T11: threshold lemma SP.9 and scalar inequalities for E(M) ==")
    # (a) c - 7/(240c) <= -1/120 for 0 < c <= 1/6 (exact at endpoint).
    ok = Fraction(1, 6) - Fraction(7 * 6, 240) == Fraction(-1, 120)
    for c in [Fraction(1, 100), Fraction(1, 20), Fraction(1, 10),
              Fraction(1, 7), Fraction(1, 6)]:
        if c - Fraction(7, 240) / c > Fraction(-1, 120): ok = False
    check("T11.a c - 7/(240c) <= -1/120 for c in (0,1/6], equality at c=1/6",
          ok)
    # (b) sum_{n>=2} n^{-t} <= 3*2^{-t} for t >= 3.
    ok = True
    for t in range(3, 51):
        S = sum(n**(-t) for n in range(2, 4000)) + 4000.0**(1 - t) / (t - 1)
        if S > 3 * 2.0**(-t): ok = False
    check("T11.b sum_{n>=2} n^{-t} <= 3*2^{-t} for 3<=t<=50", ok)
    # (c) 2k/p^{J_p+1} < 1 with p^{J_p} <= 2k < p^{J_p+1} (definitional).
    ok = True
    for k in range(2, 30):
        for p in [2, 3, 5, 7, 11, 13, 37]:
            Jp = 0
            while p**(Jp + 1) <= 2 * k: Jp += 1
            if not (p**Jp <= 2 * k < p**(Jp + 1)): ok = False
    check("T11.c J_p = floor(log_p 2k): p^J <= 2k < p^{J+1}", ok)
    # (d) Chernoff constant: (1 - ln 2)/2 >= 1/8.
    check("T11.d (1-ln2)/2 >= 1/8", (1 - math.log(2)) / 2 >= 0.125)
    # (e) threshold SP.9 in reduced form: f(u) = (7/60)u - 1/6 -
    #     [2k + u/10 + log2(2k) + t] >= 0 at u = sqrt(log M)/c and t = t_max;
    #     f is increasing in u, so u_min suffices.
    ok = True
    c = 1 / 6
    for k in (2, 3, 10):
        for logM in (10**4, 3 * 10**4, 10**5, 10**6):
            u_min = math.sqrt(logM) / c
            t_max = math.floor(math.sqrt(logM) / (60 * c) - 2 * k
                               - math.log2(2 * k) - 1)
            if t_max < 3:
                continue  # below M_0(k,c): hypothesis (a) unsatisfiable
            f = (7 / 60) * u_min - 1 / 6 - (2 * k + u_min / 10
                                            + math.log2(2 * k) + t_max)
            if f < -1e-9: ok = False
            # spot-check the *exact* per-prime inequality for small primes,
            # where u is even larger:
            for p in [2, 3, 5, 7, 13, 97]:
                u = logM / math.log(p)
                L = math.floor(0.8 * u); e = math.floor(u / 10)
                lhs = float(theta(p)) * (L - e) / 2
                rhs = (nu_fact(2 * k, p) + 1 + e
                       + math.floor(math.log(2 * k) / math.log(p)) + t_max)
                if lhs < rhs - 1e-9: ok = False
    check("T11.e threshold SP.9 holds at u_min (and at small primes) for "
          "k=2,3,10, log M >= 1e4 where t_max>=3", ok)
    # (f) monotonicity of f in u: coefficient 7/60 - 1/10 = 1/60 > 0.
    check("T11.f 7/60 - 1/10 = 1/60 > 0", Fraction(7, 60) - Fraction(1, 10)
          == Fraction(1, 60))

def exact_Lp(M, p):
    """L_p = floor((4/5) log M / log p) computed exactly:
    largest L >= 0 with p^{5L} <= M^4."""
    L = 0
    M4 = M**4; P5 = p**5; cur = 1
    while cur * P5 <= M4:
        cur *= P5; L += 1
    return L

def T13():
    print("== T13: packaged lemma at large M (exact sampling test) ==")
    NSAMP = 20000
    configs = [
        ("A: M=2^200, k=2, q0=1",        2**200, 2, 1,     0,     3),
        ("B: M=2^200, k=3, q0=24, a=7",  2**200, 3, 24,    7,     4),
        ("C: M=10^60, k=3, q0=2^10*3^4", 10**60, 3, 82944, 12345, 4),
        ("D: M=2^64, k=2, q0=1",         2**64,  2, 1,     0,     2),
    ]
    Pset = [2, 3, 5, 7, 11, 13]
    for name, M, k, q0, a, t in configs:
        assert q0**10 <= M, "q0 <= M^{1/10} violated in config"
        # exact per-prime threshold check (SP.9 instantiated):
        info = {}
        thr_all_ok = True
        for p in Pset:
            L = exact_Lp(M, p)
            e = nu_int(q0, p) if q0 % p == 0 else 0
            nu2q0 = e + (1 if p == 2 else 0)
            Jp = 0
            while p**(Jp + 1) <= 2 * k: Jp += 1
            mu2 = theta(p) * (L - e) / 2  # exact Fraction
            need = nu_fact(2 * k, p) + nu2q0 + Jp + t
            if mu2 < need: thr_all_ok = False
            info[p] = (L, e, nu2q0, Jp, mu2, need)
        check(f"T13.thr[{name}] exact threshold mu'_p/2 >= nu_p((2k)!)+"
              f"nu_p(2q0)+J_p+t for all p<=13", thr_all_ok)
        if not thr_all_ok:
            continue
        # sampling
        m0 = M + ((a - M) % q0)
        nsteps = (2 * M - m0) // q0
        good = 0; viol = 0
        cfail = {p: 0 for p in Pset}; sfail = {p: 0 for p in Pset}
        for _ in range(NSAMP):
            m = m0 + q0 * random.randint(0, nsteps)
            allgood = True
            for p in Pset:
                L, e, nu2q0, Jp, mu2, need = info[p]
                X = Xmask(m, p, e, L)
                C_ok = (X >= mu2)                  # exact Fraction compare
                V = Vprime(m, k, p)
                S_ok = (V <= nu2q0 + Jp + t)
                if not C_ok: cfail[p] += 1
                if not S_ok: sfail[p] += 1
                if not (C_ok and S_ok): allgood = False
            if allgood:
                good += 1
                for p in Pset:
                    if not crit_p(m, k, p):
                        viol += 1
                        print(f"   VIOLATION {name}: m={m} p={p}")
        check(f"T13.i[{name}] every sampled good m satisfies criterion (i) "
              f"at all p<=13", viol == 0,
              f"good={good}/{NSAMP} ({good/NSAMP:.3f})")
        # empirical rates vs proved bounds (Chernoff e^{-mu'/8}; spike
        # 2k p^{-(J_p+t+1)} up to boundary terms):
        ok_rates = True
        for p in Pset:
            L, e, nu2q0, Jp, mu2, need = info[p]
            mu = float(2 * mu2)
            cb = math.exp(-mu / 8)
            sb = 2 * k / p**(Jp + t + 1)
            emp_c = cfail[p] / NSAMP; emp_s = sfail[p] / NSAMP
            if emp_c > cb + 4 * math.sqrt(max(cb * (1 - cb), 1e-6) / NSAMP) \
               + 1e-6:
                ok_rates = False
            if emp_s > sb + 4 * math.sqrt(max(sb * (1 - sb), 1e-6) / NSAMP) \
               + 1e-6:
                ok_rates = False
        check(f"T13.r[{name}] empirical C/S failure rates within proved "
              f"bounds (+4 sigma)", ok_rates,
              "  ".join(f"p={p}:C {cfail[p]/NSAMP:.4f}<="
                        f"{math.exp(-float(2*info[p][4])/8):.4f}"
                        for p in Pset))

if __name__ == "__main__":
    fast = "--fast" in sys.argv
    T2(); T3(); T4(); T5(); T6(); T7(); T9(); T10(); T11(); T13()
    if not fast:
        T1(); T8()
    print()
    if FAILURES:
        print("FAILURES:"); [print("  ", f) for f in FAILURES]; sys.exit(1)
    print("ALL CHECKS PASSED")
