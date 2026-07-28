"""
R14 / T1 core measurement:  how far from equidistributed is the digit-poor event
inside the smooth pairs?    (slice-based, cost O(X loglog y))

For l || n+1 put W = (n+1)/l, V = W-1.  By gate_carry.py G2 the l-condition of the 727
k=2 criterion FAILS exactly when V is digit-poor base l:
      d_0(V) <= (l-3)/2   and   d_i(V) <= (l-1)/2  for all i >= 1.
DP_j = the truncation of that condition to digit positions 0..j-1: a union of
   ((l-1)/2)*((l+1)/2)^{j-1}  residue classes mod l^j  (DP_1 = "W mod l in [1,(l-1)/2]",
   exactly half of the classes coprime to l).

MODEL(l) = (#digit-poor V in [0,Y)) / (Y(1-1/l)),  Y = X/l, computed EXACTLY by digit DP.
This is what a W equidistributed in [1,X/l] and coprime to l would give.  We report
observed/MODEL in three ambient sets: ALL n<=X, n+1 smooth, n+1 AND n+2 smooth.
A bounded ratio is exactly Hypothesis U(theta,C) of L4A.md.
"""
import sys
import numpy as np
from pairlib import primes_upto, smooth_mask, digitpoor_vec, multiples_slice


def digits(Y, l):
    d = []
    while Y > 0:
        d.append(Y % l); Y //= l
    return d


def count_dp(Y, l, j=None):
    """#{ 0 <= V < Y : d_0 <= (l-3)/2, and d_i <= (l-1)/2 for 1 <= i < j } (j=None: all i)."""
    if Y <= 0:
        return 0
    c = lambda i: (l - 3) // 2 if i == 0 else (l - 1) // 2
    A = lambda i: (c(i) + 1) if (j is None or i < j) else l
    dg = digits(Y, l)
    D = len(dg)
    pref = [1] * (D + 1)
    for i in range(D):
        pref[i + 1] = pref[i] * A(i)
    total = 0
    for i in range(D - 1, -1, -1):
        total += min(dg[i], A(i)) * pref[i]
        if dg[i] >= A(i):
            break
    return total


def run(X, b, JMAX=3, P0=4):
    y = int(X ** b)
    sm = smooth_mask(X, y)
    ispair = np.zeros(X + 1, dtype=bool)
    ispair[1:X - 1] = sm[2:X] & sm[3:X + 1]
    is1 = np.zeros(X + 1, dtype=bool)
    is1[1:X - 1] = sm[2:X]
    allm = np.ones(X + 1, dtype=bool); allm[0] = False; allm[X - 1:] = False
    sets = {'ALL': allm, 'SM1': is1, 'SM12': ispair}
    P = [int(p) for p in primes_upto(y) if p > P0]
    acc = {k: {'tot': 0.0, 'obs': np.zeros(JMAX + 1), 'mod': np.zeros(JMAX + 1)} for k in sets}
    detail = {}
    accL = {'tot': 0.0, 'obs': 0.0, 'mod': 0.0}
    # largest prime factor of n+1, restricted to the smooth pairs
    lpf = np.zeros(X + 1, dtype=np.int64)

    for l in P:
        n, W = multiples_slice(X, l, 1)
        if len(n) == 0:
            continue
        ok = (W % l != 0)
        n = n[ok]; W = W[ok]
        Y = X // l + 1
        den = Y * (1.0 - 1.0 / l)
        mods = [count_dp(Y, l, None) / den] + [count_dp(Y, l, j) / den for j in range(1, JMAX + 1)]
        lpf[n[ispair[n]]] = l                      # ascending primes: last write wins
        for key, msk in sets.items():
            sel = msk[n]
            if not sel.any():
                continue
            V = W[sel] - 1
            m = len(V)
            acc[key]['tot'] += m
            for jj, jt in enumerate([None] + list(range(1, JMAX + 1))):
                acc[key]['obs'][jj] += int(digitpoor_vec(V, l, jtrunc=jt).sum())
                acc[key]['mod'][jj] += m * mods[jj]
            if key == 'SM12':
                d = detail.setdefault(l, [0, 0, 0.0])
                d[0] += m
                d[1] += int(digitpoor_vec(V, l, None).sum())
                d[2] += m * mods[0]

    # restriction to l = P(n+1), inside the smooth pairs
    idx = np.nonzero(ispair & (lpf > 0))[0]
    for l in np.unique(lpf[idx]):
        l = int(l)
        sub = idx[lpf[idx] == l]
        W = (sub + 1) // l
        keep = (W % l != 0)
        W = W[keep]
        if len(W) == 0:
            continue
        Y = X // l + 1
        accL['tot'] += len(W)
        accL['obs'] += int(digitpoor_vec(W - 1, l, None).sum())
        accL['mod'] += len(W) * (count_dp(Y, l, None) / (Y * (1.0 - 1.0 / l)))
    return dict(X=X, b=b, y=y, acc=acc, detail=detail, accL=accL, JMAX=JMAX)


if __name__ == "__main__":
    Xs = [int(float(v)) for v in sys.argv[1].split(',')]
    bs = [float(v) for v in sys.argv[2].split(',')]
    JMAX = 3
    print("%10s %5s %7s %6s %11s %s" % ("X", "b", "y", "set", "#(l||n+1)",
          "  ".join("%-22s" % s for s in ['exact'] + ['DP_%d' % j for j in range(1, JMAX + 1)])))
    for X in Xs:
        for b in bs:
            r = run(X, b, JMAX)
            for key in ('ALL', 'SM1', 'SM12'):
                a = r['acc'][key]; t = a['tot']
                if t == 0: continue
                cells = ["obs%.4f mod%.4f r%.3f" % (a['obs'][jj] / t, a['mod'][jj] / t,
                         a['obs'][jj] / max(a['mod'][jj], 1e-30)) for jj in range(JMAX + 1)]
                print("%10d %5.2f %7d %6s %11d %s" % (X, b, r['y'], key, t,
                      "  ".join("%-22s" % c for c in cells)))
            aL = r['accL']
            print("%10d %5.2f %7d %6s %11d  obs%.4f mod%.4f r%.3f" %
                  (X, b, r['y'], 'l=P1', aL['tot'], aL['obs'] / max(aL['tot'], 1),
                   aL['mod'] / max(aL['tot'], 1), aL['obs'] / max(aL['mod'], 1e-30)))
            sys.stdout.flush()
