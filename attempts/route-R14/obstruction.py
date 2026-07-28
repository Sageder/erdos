"""
R14.  Two things at once.

(A)  THE T1 NUMBER.  At l = P(n+1) (assumed l || n+1) and W = (n+1)/l, measure inside the
     smooth pairs:
        - the rate of the EXACT failure event  (W-1 digit-poor base l)
        - the rate of DP_1 : W mod l in [1,(l-1)/2]   -- a single condition mod l^2,
          which is exactly 1/2 of the classes coprime to l.
     If the DP_1 rate is <= 1/2 + o(1) then T1 holds with delta = 1/2 - o(1).

(B)  THE UNCONDITIONAL OBSTRUCTION.  Compare
        A(x,b) = #{n<=x : n+1 y-smooth, l=P(n+1)||n+1, W-1 digit-poor}      (n+2 NOT required)
        S(x,b) = #{n<=x : n+1 and n+2 both y-smooth}
     A/S -> infinity (the digit-poor event is a ~2^{-u} event, the extra smoothness a
     rho(u) ~ u^{-u} event).  Hence NO upper bound for the bad set that discards the
     smoothness of n+2 can ever be better than trivial:  the smoothness of the SECOND
     neighbour must be carried through the whole argument.  This is the T1-localised form
     of the first-moment obstruction of MIRROR.md section 6.
"""
import sys
import numpy as np
from pairlib import primes_upto, smooth_mask, digitpoor_vec, multiples_slice
from equidist import count_dp


def run(X, b, P0=4):
    y = int(X ** b)
    sm = smooth_mask(X, y)
    is1 = np.zeros(X + 1, dtype=bool); is1[1:X - 1] = sm[2:X]
    isp = np.zeros(X + 1, dtype=bool); isp[1:X - 1] = sm[2:X] & sm[3:X + 1]
    lpf = np.zeros(X + 1, dtype=np.int64)
    for l in primes_upto(y):
        l = int(l)
        if l <= P0:
            continue
        n, W = multiples_slice(X, l, 1)
        if len(n) == 0:
            continue
        lpf[n] = l                       # ascending: last write = largest prime factor
    res = {}
    for name, msk in (('SM1', is1), ('SM12', isp)):
        idx = np.nonzero(msk & (lpf > P0))[0]
        tot = fail = dp1 = 0
        modl = 0.0
        for l in np.unique(lpf[idx]):
            l = int(l)
            sub = idx[lpf[idx] == l]
            W = (sub + 1) // l
            keep = (W % l != 0)             # l || n+1
            W = W[keep]
            if len(W) == 0:
                continue
            tot += len(W)
            fail += int(digitpoor_vec(W - 1, l, None).sum())
            dp1 += int(digitpoor_vec(W - 1, l, 1).sum())
            Y = X // l + 1
            modl += len(W) * (count_dp(Y, l, None) / (Y * (1.0 - 1.0 / l)))
        res[name] = dict(tot=tot, fail=fail, dp1=dp1, mod=modl,
                         Nset=int(msk.sum()))
    res['y'] = y
    return res


if __name__ == "__main__":
    Xs = [int(float(v)) for v in sys.argv[1].split(',')]
    bs = [float(v) for v in sys.argv[2].split(',')]
    print("(A)  rates at l = P(n+1), l || n+1")
    print("%10s %5s %7s %6s %10s %8s %8s %8s %8s" %
          ("X", "b", "y", "set", "#(l||n+1)", "exact", "model", "DP_1", "DP_1/0.5"))
    store = {}
    for X in Xs:
        for b in bs:
            r = run(X, b); store[(X, b)] = r
            for k in ('SM1', 'SM12'):
                d = r[k]
                if d['tot'] == 0: continue
                print("%10d %5.2f %7d %6s %10d %8.4f %8.4f %8.4f %8.4f" %
                      (X, b, r['y'], k, d['tot'], d['fail'] / d['tot'], d['mod'] / d['tot'],
                       d['dp1'] / d['tot'], d['dp1'] / d['tot'] / 0.5))
            sys.stdout.flush()
    print()
    print("(B)  the obstruction ratio   A/S   (A ignores the smoothness of n+2)")
    print("%10s %5s %7s %12s %12s %10s" % ("X", "b", "y", "A", "S", "A/S"))
    for (X, b), r in store.items():
        A = r['SM1']['fail']; S = r['SM12']['Nset']
        print("%10d %5.2f %7d %12d %12d %10.2f" % (X, b, r['y'], A, S, A / max(S, 1)))
