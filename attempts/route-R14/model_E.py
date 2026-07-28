"""
R14 / T2 model.   Asymptotic prediction for  E[#failures | n+1,n+2 both x^b-smooth]
and for the union-bound budget available at level of distribution theta.

MODEL ASSUMPTIONS (stated so they can be checked -- and they ARE checked, against the
exact counts of table_efail.py; see L4A.md Table 3):
  (M1) conditionally on n+1 being x^b-smooth, the number of prime factors l = x^{beta}
       with l || n+1, beta in (v/u, (v+dv)/u)  (u = 1/b, l = y^v) has mean
             (rho(u-v)/rho(u)) dv/v ,
       the standard Dickman/"Buchstab" count  Psi(x/l,y)/Psi(x,y) summed over l ~ y^v;
  (M2) for l || n+j the cofactor W = (n+j)/l is equidistributed enough that the failure
       probability equals the uniform-W value  2^{-D},  D = floor(u/v) - 1  =  the number
       of base-l digits of W-1 (this is the ONLY place a distributional input enters;
       equidist.py measures the ratio observed/uniform and finds it -> 1);
  (M3) prime powers l^e || n+j with e >= 2 contribute o(1)  (measured column E2 -> 0).

Then          E_inf(b) = 2 * int_0^1 (rho(u-v)/rho(u)) 2^{1-floor(u/v)} dv/v ,
and if only the low j = floor(theta/beta) = floor(theta u / v) base-l digits are used
(all that a level-of-distribution x^theta permits),

              E_theta(b) = 2 * int_0^1 (rho(u-v)/rho(u)) 2^{-floor(theta u/v)} dv/v .

E_inf = E_1 (theta = 1) up to the shift by one digit; both are printed.
"""
import numpy as np


# ---------- Dickman rho ----------------------------------------------------------
def dickman(umax=32, M=4096):
    """
    rho on the grid u = i/M, 0 <= u <= umax.
    On [k,k+1] integrate  rho(u) = rho(k) - int_k^u rho(t-1)/t dt  by composite Simpson,
    using the already computed values on [k-1,k].  Accurate and monotone-stable.
    """
    N = umax * M
    u = np.arange(N + 1) / M
    r = np.zeros(N + 1)
    r[:M + 1] = 1.0
    r[M:2 * M + 1] = 1 - np.log(u[M:2 * M + 1])
    h = 1.0 / M
    for k in range(2, umax):
        g = r[(k - 1) * M:k * M + 1] / u[k * M:(k + 1) * M + 1]   # rho(t-1)/t on [k,k+1]
        # cumulative Simpson (pairs of subintervals) + trapezoid for odd points
        cum = np.zeros(M + 1)
        for i in range(1, M + 1):
            if i % 2 == 0:
                cum[i] = cum[i - 2] + h / 3 * (g[i - 2] + 4 * g[i - 1] + g[i])
            else:
                cum[i] = cum[i - 1] + h / 12 * (5 * g[i - 1] + 8 * g[i] - g[i + 1] if i + 1 <= M
                                                else 6 * (g[i - 1] + g[i]) / 2)
        r[k * M:(k + 1) * M + 1] = r[k * M] - cum
    return u, r, h


_U, _R, _H = dickman()


def rho(x):
    x = np.asarray(x, dtype=float)
    idx = np.clip((x / _H).astype(int), 0, len(_R) - 2)
    fr = x / _H - idx
    val = _R[idx] * (1 - fr) + _R[idx + 1] * fr
    return np.where(x < 0, 0.0, np.where(x <= 1, 1.0, np.maximum(val, 1e-300)))


def E_model(u, theta=1.0, shift=1, NQ=4000):
    """
    2 * int_0^1 (rho(u-v)/rho(u)) * 2^{-max(0, floor(theta*u/v) - shift)} dv/v ,
    integrated exactly piecewise between the jump points v = theta*u/k.
    shift=1 reproduces the true digit count D = floor(u/v)-1 when theta=1;
    shift=0 is the conservative "j = floor(theta u/v) digits are usable" budget.
    """
    total = 0.0
    R0 = float(rho(u))
    # jumps at v = theta*u/k for integer k;  v in (0,1]
    kmin = int(np.floor(theta * u)) if theta * u >= 1 else 0
    ks = list(range(max(kmin, 1), max(kmin, 1) + 4000))
    lo_prev = 1.0
    for k in ks:
        hi = min(1.0, theta * u / k)
        lo = theta * u / (k + 1)
        if hi <= 0:
            break
        lo = min(lo, hi)
        if hi <= 1e-12:
            break
        vs = np.linspace(lo, hi, NQ)
        w = 2.0 ** (-max(0, k - shift))
        f = rho(u - vs) / R0 * w / vs
        total += np.trapezoid(f, vs)
        if hi >= 1.0 and lo <= 0:
            break
        if lo <= 1e-9:
            break
    return 2 * total


if __name__ == "__main__":
    # sanity: Dickman values
    known = {2: 3.0685281944e-1, 3: 4.8608388e-2, 4: 4.9109256e-3, 5: 3.5472470e-4,
             6: 1.9649696e-5, 8: 3.2320275e-8, 10: 2.7701e-11}
    print("Dickman check:")
    for k, v in known.items():
        print("   rho(%2d) = %.6e   known %.6e   rel.err %.2e" % (k, rho(k), v, abs(rho(k)/v-1)))
    print()
    print("TABLE M1.  E_inf(b) = model prediction for E[#failures | smooth pair] as x -> oo,")
    print("and E_theta(b) = the union-bound budget obtainable from a level of distribution x^theta")
    print("(only j = floor(theta/beta) of the base-l digits of the cofactor are then usable).")
    print("%6s %7s %10s %10s %10s %10s %10s" %
          ("b", "u=1/b", "E_inf", "th=1", "th=0.5", "th=0.25", "th=0.1"))
    for b in [0.5, 0.45, 0.4, 0.35, 0.3, 0.28, 0.26, 0.25, 0.22, 0.2, 0.15, 0.12, 0.1,
              0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.015, 0.012, 0.01, 0.008, 0.006]:
        u = 1.0 / b
        if u > 30:
            print("%6.3f %7.1f %10s %10s %10s %10s %10s" % (b, u, "-", "-", "-", "-", "-"))
            continue
        print("%6.3f %7.3f %10.4f %10.4f %10.4f %10.4f %10.4f" %
              (b, u, E_model(u, 1.0, 1), E_model(u, 1.0, 0), E_model(u, 0.5, 0),
               E_model(u, 0.25, 0), E_model(u, 0.1, 0)))
    print()
    print("TABLE M2.  DISTRIBUTION-FREE budget  2G(b,theta),  G = (2/b) sum_{k>=1}(k+1) 2^{-k theta/b}.")
    print("This uses NO information about the distribution of the prime factors: it holds for EVERY")
    print("x^b-smooth n+1 and n+2 simultaneously, so a proof needs only Hypothesis U, nothing else.")
    print("%6s %12s %12s %12s %12s" % ("b", "th=1", "th=0.5", "th=0.25", "th=0.1"))
    def G2(b, th):
        t = 2.0 ** (-th / b)
        return 2 * (2.0 / b) * t * (2 - t) / (1 - t) ** 2
    for b in [0.3, 0.25, 0.2, 0.15, 0.1, 0.07, 0.05, 0.04, 0.03, 0.025, 0.02, 0.015, 0.01, 0.007]:
        print("%6.3f %12.4g %12.4g %12.4g %12.4g" % (b, *[G2(b, th) for th in (1.0, .5, .25, .1)]))
    print()
    print("largest b with 2G(b,theta) < 1  (rigorous once Hypothesis U(theta,C=1) is granted):")
    for th in (1.0, 0.5, 0.25, 0.1, 0.05):
        lo, hi = 1e-4, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if G2(mid, th) < 1: lo = mid
            else: hi = mid
        print("   theta=%.3f :  b* = %.5f   (2G = %.4f)" % (th, lo, G2(lo, th)))
    print("   and with a loss constant C: b* solves 2 C G(b,theta) = 1; C=2 shown:")
    for th in (1.0, 0.5, 0.25, 0.1):
        lo, hi = 1e-4, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if 2 * G2(mid, th) < 1: lo = mid
            else: hi = mid
        print("   theta=%.3f :  b* = %.5f" % (th, lo))

    # ---- the budget actually used in Theorem B of L4A.md ------------------------
    # per-number bound  (C/2) * H(b,theta),  H = (25/(9b)) * t(2-t)/(1-t)^2,
    # t = (3/5)^{theta/b};  total over the two neighbours = C*H(b,theta).
    print()
    print("TABLE M3.  H(b,theta) : the constant in Theorem B of L4A.md.  Need C*H < 1.")
    def H(b, th):
        t = (3.0 / 5.0) ** (th / b)
        return (25.0 / (9.0 * b)) * t * (2 - t) / (1 - t) ** 2
    print("%8s %12s %12s %12s %12s" % ("b", "th=1", "th=0.5", "th=0.25", "th=0.1"))
    for b in [0.2, 0.15, 0.1, 0.07, 0.05, 0.04, 0.03, 0.02, 0.015, 0.01, 0.007, 0.005, 0.003]:
        print("%8.3f %12.4g %12.4g %12.4g %12.4g" % (b, *[H(b, th) for th in (1., .5, .25, .1)]))
    print()
    print("largest b with C*H(b,theta) < 1 :")
    for C in (1.0, 1.1, 1.5, 2.0):
        row = []
        for th in (1.0, 0.5, 0.25, 0.1, 0.05):
            lo, hi = 1e-6, 1.0
            for _ in range(300):
                mid = (lo + hi) / 2
                if C * H(mid, th) < 1: lo = mid
                else: hi = mid
            row.append(lo)
        print("   C=%.1f :  " % C + "  ".join("theta=%.2f -> b*=%.5f" % (th, v)
                                              for th, v in zip((1., .5, .25, .1, .05), row)))
