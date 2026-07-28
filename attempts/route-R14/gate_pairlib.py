"""R14 gate 2: cross-check pairlib against sympy on a small range (exhaustive)."""
import numpy as np
from sympy import factorint, factorial
from pairlib import pair_data

X, y, P0 = 200000, 200, 4

def carries(n, l):
    c = 0; carry = 0
    while n > 0:
        d = n % l
        if 2*d + carry >= l: carry = 1; c += 1
        else: carry = 0
        n //= l
    return c

d = pair_data(X, y, P0)
n = d['n']
print("X=%d y=%d : %d smooth pairs" % (X, y, len(n)))

bf_nfail, bf_oksmall, bf_lpf1, bf_faillpf1, bf_omega, bf_sq = [], [], [], [], [], []
for v in n:
    v = int(v)
    nf = 0; om = 0; sq = True
    f1 = factorint(v+1); f2 = factorint(v+2)
    assert max(f1) <= y and max(f2) <= y, (v, f1, f2)
    for f, j in ((f1, 1), (f2, 2)):
        for l, e in f.items():
            if l <= P0: continue
            om += 1
            if e > 1: sq = False
            if carries(v, l) < 2*e: nf += 1
    bf_nfail.append(nf); bf_omega.append(om); bf_sq.append(sq)
    ok = True
    for p in (2, 3):
        dem = f1.get(p, 0) + f2.get(p, 0)
        if carries(v, p) < 2*dem: ok = False
    bf_oksmall.append(ok)
    L = max([l for l in f1 if l > P0], default=0)
    bf_lpf1.append(L)
    bf_faillpf1.append(L > 0 and carries(v, L) < 2*f1[L])

assert (np.array(bf_nfail) == d['nfail_large'][n]).all(), "nfail mismatch"
assert (np.array(bf_omega) == d['omega_large'][n]).all(), "omega mismatch"
assert (np.array(bf_sq)    == d['sqfree'][n]).all(),      "sqfree mismatch"
assert (np.array(bf_oksmall) == d['ok_small'][n]).all(),  "ok_small mismatch"
assert (np.array(bf_lpf1)  == d['lpf1'][n]).all(),        "lpf1 mismatch"
assert (np.array(bf_faillpf1) == d['fail_lpf1'][n]).all(),"fail_lpf1 mismatch"
print("GATE 2 PASS: pairlib == sympy brute force on all %d smooth pairs (X=%d,y=%d)." % (len(n), X, y))

mem = (d['nfail_large'][n] == 0) & d['ok_small'][n]
sel = n[np.nonzero(mem)[0][:40]]
for v in sel:
    assert factorial(2*int(v)) % (factorial(int(v)+2)**2) == 0, v
print("GATE 2b PASS: %d certified members re-verified by exact factorial division; e.g. %s"
      % (len(sel), [int(x) for x in sel[:8]]))
