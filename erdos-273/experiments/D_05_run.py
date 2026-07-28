"""
D_05_run.py  --  driver for D_05_phi

CLAIM TESTED.  Necessary condition for Erdos 273 (via Prop. D1 + Prop. D2):
if a covering system with distinct moduli in E exists, and L is the lcm of the halved moduli
(H-world), then for EVERY prime q
        Phi_q( D_H(L) )  >=  2 ,        D_H(L) = {m | L : m >= 2, 2m+1 prime}.
Phi_q is monotone under inclusion of the modulus set, so  Phi_q(D_H(L)) < 2  kills L and
simultaneously every L' dividing L.

This driver evaluates the condition on a list of candidate L (e.g. the divisor-maximal
survivors of the budget sieve D_04) and reports which L are killed.

CONCLUSION: printed at run time.
"""
import subprocess, sys, os
from sympy import isprime, factorint

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "D_05_phi")


def DH(L):
    ds = []
    d = 1
    while d * d <= L:
        if L % d == 0:
            for x in (d, L // d):
                if x >= 2 and isprime(2 * x + 1):
                    ds.append(x)
        d += 1
    return sorted(set(ds))


def phi(ds, q, target=2.0, nodecap=200_000_000):
    e = 0
    t = 1
    while all(True for _ in ()) or True:
        if any(m % (t * q) == 0 for m in ds):
            t *= q
            e += 1
        else:
            break
    flat = sum(1.0 / m for m in ds if m % q != 0)
    items = []
    for m in ds:
        j = 0
        x = m
        while x % q == 0:
            x //= q
            j += 1
        if j:
            items.append((j, q ** j / m))
    if not items:
        return ("PHI", flat, e, 0)
    inp = "%.17g\n" % flat + "".join("%d %.17g\n" % it for it in items)
    args = [BIN, str(q), str(e), str(len(items)), str(nodecap)]
    if target:
        args.append("%.17g" % target)
    out = subprocess.run(args, input=inp, capture_output=True, text=True).stdout.strip()
    return (out, flat, e, len(items))


def test_L(L, target=2.0, verbose=True, nodecap=200_000_000):
    ds = DH(L)
    b = sum(1.0 / m for m in ds)
    fac = factorint(L)
    res = {}
    killed = None
    for q in sorted(fac):
        out, flat, e, ni = phi(ds, q, target, nodecap)
        res[q] = (out, flat, e, ni)
        if isinstance(out, str) and out.startswith("PHI_LT"):
            killed = q
            break
    if verbose:
        print("L = %-10d fac=%-34s |D_H|=%-4d budget=%.5f" % (L, dict(fac), len(ds), b))
        for q, (out, flat, e, ni) in res.items():
            print("     q=%-3d e=%d  A_0=%.5f  #items=%-4d  %s" % (q, e, flat, ni, out))
        if killed:
            print("     ==> KILLED by q=%d  (Phi_q < %.1f): no covering with H-lcm dividing %d"
                  % (killed, target, L))
        else:
            print("     ==> survives the Phi test")
    return killed, res


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--file":
        Ls = [int(l.split()[0]) for l in open(sys.argv[2])]
    else:
        Ls = [int(a) for a in sys.argv[1:]] or [1801800]
    nk = 0
    for L in Ls:
        k, _ = test_L(L)
        nk += (k is not None)
    print("\nkilled %d of %d candidates" % (nk, len(Ls)))
