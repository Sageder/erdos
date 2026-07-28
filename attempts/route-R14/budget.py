"""
R14.  The explicit budget constant K(b,theta) of Theorem B in L4A.md, and the resulting
thresholds b*(theta,C).

Per-prime-power bound (Lemma 3' of L4A.md):  if l^a || n+nu, beta = log l/log x,
a*beta <= theta/11, and J = floor(theta/beta) - a, then the proportion of residues
W mod l^J coprime to l with fewer than a carries is at most, for any 0 < z <= 1,
        (5/4) z^{-a} (r+z)^J ,   r = (l+1)/(2l) <= 3/5.
With z = 1/10 and J >= theta/beta - a - 1:
        log2(prop) <= 0.322 + a*log2(10) - log2(1/0.7)*(theta/beta - a - 1)
                    = 0.837 + 3.836 a - 0.5146 theta/beta
and a <= (theta/11)/beta gives  3.836 a <= 0.3487 theta/beta, hence
        prop <= 1.79 * 2^{-0.1659 theta/beta} <= 2 * 2^{-theta/(7 beta)}   (1/7 = 0.1429).
Then Lemma 4' gives, per number,  sum_{l | m} 2^{-theta/(7 beta_l)} <= (1/b) t(2-t)/(1-t)^2,
t = 2^{-theta/(7b)}, and over the two neighbours with the factor 2C:
        K(b,theta) = (4/b) * t(2-t)/(1-t)^2 ,  t = 2^{-theta/(7b)} .
"""
import numpy as np

def K(b, th):
    t = 2.0 ** (-th / (7.0 * b))
    return (4.0 / b) * t * (2 - t) / (1 - t) ** 2

def H(b, th):                      # the sharper e=1-only constant (see L4A.md section 5 remark)
    t = (3.0 / 5.0) ** (th / b)
    return (25.0 / (9.0 * b)) * t * (2 - t) / (1 - t) ** 2

# verify the chain of inequalities in the docstring numerically
z = 0.1; r = 3.0/5.0
assert np.log2(1/(r+z)) > 0.5146 - 1e-3, np.log2(1/(r+z))
print("check: log2(1/(r+z)) = %.4f (>= 0.5146),  log2(10) = %.4f" % (np.log2(1/(r+z)), np.log2(10)))
print("check: 0.5146 - 3.836/11 = %.4f  >= 1/7 = %.4f" % (0.5146 - 3.836/11.0, 1/7))

print()
print("TABLE B1.  K(b,theta) -- the fully general budget of Theorem B (all prime powers).")
print("%8s %12s %12s %12s %12s" % ("b", "th=1", "th=0.5", "th=0.25", "th=0.1"))
for b in [0.05, 0.03, 0.02, 0.015, 0.01, 0.007, 0.005, 0.003, 0.002, 0.0015, 0.001]:
    print("%8.4f %12.4g %12.4g %12.4g %12.4g" % (b, *[K(b, t) for t in (1., .5, .25, .1)]))

print()
print("largest b with C*K(b,theta) < 1  AND b < theta/11 :")
for C in (1.0, 1.5, 2.0):
    row = []
    for th in (1.0, 0.5, 0.25, 0.1, 0.05):
        lo, hi = 1e-7, th / 11.0
        for _ in range(300):
            mid = (lo + hi) / 2
            if C * K(mid, th) < 1: lo = mid
            else: hi = mid
        row.append(lo)
    print("   C=%.1f : " % C + "  ".join("theta=%.2f -> b*=%.5f" % (t, v)
                                         for t, v in zip((1., .5, .25, .1, .05), row)))
print()
print("for comparison, the sharper e=1-only constant H:  largest b with C*H(b,theta)<1")
for C in (1.0, 1.5, 2.0):
    row = []
    for th in (1.0, 0.5, 0.25, 0.1, 0.05):
        lo, hi = 1e-7, 1.0
        for _ in range(300):
            mid = (lo + hi) / 2
            if C * H(mid, th) < 1: lo = mid
            else: hi = mid
        row.append(lo)
    print("   C=%.1f : " % C + "  ".join("theta=%.2f -> b*=%.5f" % (t, v)
                                         for t, v in zip((1., .5, .25, .1, .05), row)))
