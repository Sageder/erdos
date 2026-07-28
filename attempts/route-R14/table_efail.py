"""
R14 / T2.  Measured  E[#failures | n+1, n+2 both X^b-smooth] and the true pass rate.
Exact arithmetic; y = floor(X^b), P0 = 4.

  Npair  #{n <= X : n+1, n+2 both y-smooth}
  E      mean of #{l>4 : l|(n+1)(n+2), kappa_l(n) < 2 nu_l(n+j)}   (the union-bound budget)
  E1     part of E from primes with l || n+j
  E2     part of E from primes with l^2 | n+j      (finite-size: -> 0 as X -> oo)
  Esm    part of E from primes l <= y^(1/2)        (finite-size: -> 0 as X -> oo)
  pass   fraction with NO large-prime failure      (Markov: pass >= 1 - E)
  passS2 fraction actually in S_2
  Plpf   fraction failing at l = P(n+1)            (the T1 / L4a target)
  sqfr   fraction with l || n+j for every prime l > 4
"""
import sys, time
import numpy as np
from pairlib import pair_data, primes_upto


def run(X, b, P0=4):
    y = int(X ** b)
    d = pair_data(X, y, P0=P0)
    n = d['n']; N = len(n)
    if N == 0:
        return dict(X=X, b=b, y=y, N=0)
    nf = d['nfail_large'][n].astype(np.int64)
    Esm = 0.0
    for l, (c, f) in d['perprime'].items():
        if l * l <= y:
            Esm += f
    return dict(X=X, b=b, y=y, N=N, dens=N / X,
                E=nf.mean(), E1=d['nfail_e1'][n].mean(), E2=d['nfail_e2'][n].mean(),
                Esm=Esm / N,
                ppass=(nf == 0).mean(),
                passS2=((nf == 0) & d['ok_small'][n]).mean(),
                Plpf=d['fail_lpf1'][n].mean(), sqfr=d['sqfree'][n].mean(),
                omega=d['omega_large'][n].mean(), pp=d['perprime'])


if __name__ == "__main__":
    Xs = [int(float(v)) for v in sys.argv[1].split(',')]
    bs = [float(v) for v in sys.argv[2].split(',')]
    show = len(sys.argv) > 3
    print("%11s %6s %8s %10s %9s %7s %7s %7s %7s %7s %8s %7s %6s %6s" %
          ("X", "b", "y", "Npair", "dens", "E", "E1", "E2", "Esm",
           "pass", "passS2", "Plpf", "sqfr", "omega"))
    for X in Xs:
        for b in bs:
            t0 = time.time()
            r = run(X, b)
            if r['N'] == 0:
                print("%11d %6.3f %8d %10d   (no smooth pairs)" % (X, b, r['y'], 0)); continue
            print("%11d %6.3f %8d %10d %9.2e %7.4f %7.4f %7.4f %7.4f %7.4f %8.5f %7.4f %6.3f %6.2f"
                  % (X, b, r['y'], r['N'], r['dens'], r['E'], r['E1'], r['E2'], r['Esm'],
                     r['ppass'], r['passS2'], r['Plpf'], r['sqfr'], r['omega']))
            if show:
                items = sorted(r['pp'].items(), key=lambda kv: -kv[1][1])[:10]
                print("      top E_l:", "  ".join("%d:%.4f" % (l, f / r['N']) for l, (c, f) in items),
                      " [%.1fs]" % (time.time() - t0))
            sys.stdout.flush()
