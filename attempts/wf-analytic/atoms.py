"""
atoms.py -- THE ATOM MODEL: an exactly-factorising sub-family of legal sets,
and the exact reduction of CRUX to a minor-arc inequality.

THE FAMILY.  Fix a cap B and put
    good(n)  <=>  every prime power dividing n(n+1) is <= B      (n in [T,N-1]).
Choose pairwise DISJOINT atoms  A_i = {a_i, a_i+1}  with good(a_i), greedily.
Every union of atoms is a LEGAL set (a union of adjacent atoms is a longer run,
still with no isolated point), so we get 2^m legal sets from m atoms.
Put  v_i = 1/a_i + 1/(a_i+1) = (2a_i+1)/D_i,  D_i = a_i(a_i+1)  (already reduced:
gcd(2a+1, a(a+1)) = 1),  and  Lambda = lcm(D_1,...,D_m)  |  prod_{p<=B} p^{f_p},
f_p = floor(log_p B).

EXACT IDENTITY (atom model).  X_S = sum_{i in S} Lambda v_i is an integer, and
   (1/Lambda) sum_{h mod Lambda} G(h) = #{S subset [m] : sum_{i in S} v_i in Z},
   G(h) = prod_{i=1}^m (1 + e(h v_i)),      G(0) = 2^m.
If  sum_i v_i < 2  the right-hand side is  1 + #{S : sum_{i in S} v_i = 1}.
So, writing  |1+e(t)| = 2|cos(pi t)|,

   THEOREM (REDUCTION).  If  sum_i v_i in (1,2)  and
        (MA)     Theta := sum_{h=1}^{Lambda-1}  prod_{i=1}^m |cos(pi h v_i)|
                        <  1 - Lambda * 2^{-m},
   then there is a LEGAL U subset [T,N] with sum_{n in U} 1/n = 1.
   (Proof: Z = (1/Lambda) sum_h G(h) - 1 >= (2^m - 2^m Theta)/Lambda - 1 > 0.)

Everything before (MA) is exact and elementary.  (MA) is the whole difficulty.

HEURISTIC SIZE OF Theta.  If the h v_i equidistributed, the average of the
product over h mod Lambda would be prod_i E|cos| = (2/pi)^m, so
Theta ~ Lambda (2/pi)^m = exp(log Lambda - 0.4516 m).  This script computes
log Lambda and m exactly; log Lambda = o(m) with a power saving, so the
heuristic margin in (MA) is exp(-(0.4516+o(1)) m).

WHERE (MA) CAN FAIL.  ||h v_i|| = 0 exactly when D_i | h.  So with
d = Lambda/gcd(h,Lambda) and K = Lambda/d, the set of ACTIVATED atoms is
    A(d) = { i : D_i does not divide K },      |A(d)| = m - #{i : D_i | K},
and |G(h)| = 2^m prod_{i in A(d)} |cos(pi h v_i)|.  The number of h at level d
is phi(d).  The heuristic "product of averages" then predicts

    Theta ~ sum_{d | Lambda, d>1} phi(d) (2/pi)^{|A(d)|},

so (MA) needs the ACTIVATION LOWER BOUND
    (ACT)   |A(d)| >= C log d  for all divisors d>1 of Lambda,  C > 1/log(pi/2) = 2.2146.
This script computes |A(d)| exactly for the extremal levels d and reports
min |A(d)|/log d.

CONNECTION TO RULE (P).  min_{h != 0} |A(h)| = min_p #{i : nu_p(D_i) = e_p},
the number of atoms attaining the top p-level.  If that minimum is 1 the atom
in question is FORCED OUT by Rule (P) of the repository -- so the "worst minor
arcs" of the circle method are exactly the p-adic obstructions Rule (P) detects.
"""
import sys
from math import log, gcd
from fractions import Fraction
from core import primes_upto, lcm_int, report_log, H


def prime_power_profile(N, B):
    """
    For every n <= N record max prime power dividing n, to test the cap.
    Returns list mpp[n] = max_{p^k || n} p^k.
    """
    mpp = [1] * (N + 1)
    for p in primes_upto(N):
        q = p
        while q <= N:
            for mlt in range(q, N + 1, q):
                if mpp[mlt] < q:
                    mpp[mlt] = q
            q *= p
    return mpp


def build_atoms(T, N, B, mpp=None):
    if mpp is None:
        mpp = prime_power_profile(N, B)
    atoms = []
    n = T
    while n < N:
        if mpp[n] <= B and mpp[n + 1] <= B:
            atoms.append(n)
            n += 2
        else:
            n += 1
    return atoms


def factor(x):
    f = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            f[d] = f.get(d, 0) + 1
            x //= d
        d += 1 if d == 2 else 2
    if x > 1:
        f[x] = f.get(x, 0) + 1
    return f


def analyse(T, N, B, mpp=None, verbose=True):
    atoms = build_atoms(T, N, B, mpp)
    m = len(atoms)
    if m == 0:
        return None
    D = [a * (a + 1) for a in atoms]
    Lam = 1
    for d in D:
        Lam = lcm_int(Lam, d)
    Sv = sum(Fraction(2 * a + 1, a * (a + 1)) for a in atoms)
    logLam = report_log(Lam)
    res = dict(T=T, N=N, B=B, m=m, Lam=Lam, logLam=logLam, Sv=Sv,
               main=m * log(2) - logLam, atoms=atoms, D=D)

    # activation profile
    fL = factor(Lam)
    # exponent of p in each D_i
    def nu(x, p):
        e = 0
        while x % p == 0:
            x //= p
            e += 1
        return e

    levels = []           # (d, |A(d)|, log d, label)
    # single prime powers d = p^j
    for p, e in sorted(fL.items()):
        nus = [nu(x, p) for x in D]
        for j in range(1, e + 1):
            # K = Lambda / p^j  => nu_p(K) = e-j ; D_i | K iff nu_p(D_i) <= e-j
            #                    (all other primes unchanged)
            A = sum(1 for t in nus if t > e - j)
            levels.append((p ** j, A, j * log(p), f"{p}^{j}"))
    # d = Lambda (all levels dropped)
    A_all = sum(1 for x in D if x == 1)
    levels.append((Lam, m - A_all, logLam, "Lambda"))
    # d = product of the k largest prime powers
    pps = sorted([(p ** e, p, e) for p, e in fL.items()], reverse=True)
    for k in (2, 3, 5, 10, 20, 50):
        if k > len(pps):
            break
        dd = 1
        for (q, p, e) in pps[:k]:
            dd *= q
        cnt = 0
        for x in D:
            ok = True
            for (q, p, e) in pps[:k]:
                if nu(x, p) > 0:
                    ok = False
                    break
            if not ok:
                cnt += 1
        levels.append((dd, cnt, sum(log(q) for q, p, e in pps[:k]),
                       f"top{k}pp"))

    worst = min(levels, key=lambda t: (t[1] / t[2]) if t[2] > 0 else 1e9)
    res['levels'] = levels
    res['worst'] = worst
    res['ratio'] = worst[1] / worst[2]
    if verbose:
        print(f"T={T} N={N} B={B}: m={m} atoms, log Lambda={logLam:.2f}, "
              f"m*log2={m*log(2):.2f}, MAIN TERM log(2^m/Lam)={res['main']:.2f}, "
              f"sum v_i={float(Sv):.4f} {'(>1 OK)' if Sv>1 else '(<=1 : target 1 unreachable)'}")
        print(f"   2^m > Lambda ? {2**m > Lam}   (exact)")
        print(f"   activation:  min |A(d)|/log d = {res['ratio']:.3f}  at d={worst[3]} "
              f"(|A|={worst[1]}, log d={worst[2]:.2f});  need > 2.2146")
    return res


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    N = int(T * ratio)
    mpp = prime_power_profile(N, N)
    print(f"H(T,N) = {float(H(T,N)):.4f}  (need 1 < H < 2)")
    for expo in (0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 1.0):
        B = int(N ** expo)
        r = analyse(T, N, B, mpp)
        if r is None:
            print(f"  B=N^{expo}={B}: no atoms")


if __name__ == "__main__":
    main()
