"""
atoms2.py -- efficient version of the atom model; scans (T, N/T, B) and reports
the three competing exact quantities

   (i)   sum_i v_i  > 1                       (target 1 must be reachable)
   (ii)  2^m > Lambda                         (h=0 main term exponentially large)
   (iii) min_d |A(d)|/log d  > 1/log(pi/2)    (activation bound (ACT) behind (MA))

See atoms.py for the statements.  All the quantities are computed exactly
(Python ints / Fraction); only the printed logarithms are floating point.
"""
import sys
from array import array
from math import log, isqrt
from fractions import Fraction
from core import primes_upto, lcm_int, report_log, H


def capped_mask(N, B):
    """capped[n] is True iff every prime power dividing n is <= B  (n <= N)."""
    capped = bytearray([1]) * (N + 1)
    for p in primes_upto(N):
        q = p
        while q <= N:
            if q > B:
                capped[q::q] = bytearray(len(capped[q::q]))
            q *= p
    return capped


def build(T, N, B, capped):
    atoms = []
    n = T
    while n < N:
        if capped[n] and capped[n + 1]:
            atoms.append(n)
            n += 2
        else:
            n += 1
    return atoms


def analyse(T, N, B, capped, do_activation=True, verbose=True):
    atoms = build(T, N, B, capped)
    m = len(atoms)
    if m == 0:
        return None
    Sv = sum(Fraction(2 * a + 1, a * (a + 1)) for a in atoms)
    # Lambda = lcm of a(a+1) = prod_{p<=B} p^{max nu_p}
    maxnu = {}
    for a in atoms:
        for x in (a, a + 1):
            t = x
            d = 2
            while d * d <= t:
                if t % d == 0:
                    e = 0
                    while t % d == 0:
                        t //= d
                        e += 1
                    if maxnu.get(d, 0) < e:
                        maxnu[d] = e
                d += 1 if d == 2 else 2
            if t > 1 and maxnu.get(t, 0) < 1:
                maxnu[t] = 1
    Lam = 1
    for p, e in maxnu.items():
        Lam *= p ** e
    logLam = sum(e * log(p) for p, e in maxnu.items())
    out = dict(T=T, N=N, B=B, m=m, Sv=Sv, Lam=Lam, logLam=logLam,
               main=m * log(2) - logLam, cover=2 * m / (N - T + 1))
    if do_activation:
        # nu_p(D_i) for every prime p dividing Lambda
        # activation at level d = p^j :  |A| = #{i : nu_p(D_i) > e_p - j}
        nucount = {p: [0] * (e + 1) for p, e in maxnu.items()}
        for a in atoms:
            for x in (a, a + 1):
                t = x
                d = 2
                while d * d <= t:
                    if t % d == 0:
                        e = 0
                        while t % d == 0:
                            t //= d
                            e += 1
                        nucount[d][e] += 1
                    d += 1 if d == 2 else 2
                if t > 1:
                    nucount[t][1] += 1
        best = None
        for p, e in maxnu.items():
            cnt = nucount[p]
            # number of atoms with nu_p(D_i) >= t  (nu_p(D_i)=nu_p(a)+nu_p(a+1),
            # but a and a+1 are coprime so at most one of them is divisible by p)
            ge = [0] * (e + 2)
            for t in range(e, 0, -1):
                ge[t] = ge[t + 1] + cnt[t]
            for j in range(1, e + 1):
                A = ge[e - j + 1]
                r = A / (j * log(p))
                if best is None or r < best[0]:
                    best = (r, A, j * log(p), f"{p}^{j}")
        out['worst'] = best
        out['ratio'] = best[0]
    if verbose:
        ok1 = Sv > 1
        ok2 = 2 ** m > Lam
        s = (f"T={T:<8} N={N:<9} B={B:<8} m={m:<7} cover={out['cover']:.3f} "
             f"logLam={logLam:9.1f} mlog2={m*log(2):9.1f} MAIN={out['main']:9.1f} "
             f"sum v={float(Sv):.4f} {'OK' if ok1 else '--'} 2^m>Lam:{'OK' if ok2 else '--'}")
        if do_activation:
            s += f" ACT={out['ratio']:.3f}@{best[3]} (|A|={best[1]})"
        print(s)
    return out


def main():
    Ts = [int(x) for x in (sys.argv[1].split(',') if len(sys.argv) > 1 else ['1000'])]
    ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 7.0
    expos = [float(x) for x in (sys.argv[3].split(',') if len(sys.argv) > 3
                                else ['0.70', '0.75', '0.80', '0.85'])]
    for T in Ts:
        N = int(T * ratio)
        print(f"--- T={T} N={N}  H(T,N)={float(H(T,N)):.4f} "
              f"{'(1<H<2 OK)' if 1 < H(T,N) < 2 else '(H OUT OF RANGE)'} ---")
        for e in expos:
            B = int(N ** e)
            capped = capped_mask(N, B)
            analyse(T, N, B, capped)
        print()


if __name__ == "__main__":
    main()
