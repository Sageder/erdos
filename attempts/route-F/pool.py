#!/usr/bin/env python3
"""Collect a POOL of gadgets in a window: legal U with denom(Sigma(U)) | D.

Diversity is obtained by slicing the attainable sum range into bands and running
the DFS separately inside each band.

usage: pool.py x y D cap out.txt nbands per_band nodecap [lofrac hifrac]
Each output line:   c  n1 n2 n3 ...        with Sigma = c/D  (exact, re-checked)
"""
import sys, os, subprocess, time
from fractions import Fraction
from lib import smallest_prime_factors
from universe import prune, lcm_of
from mk import write_problem

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    x, y, D = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    cap = int(sys.argv[4]); out = sys.argv[5]
    nbands = int(sys.argv[6]); per = int(sys.argv[7]); nodecap = int(sys.argv[8])
    lofrac = Fraction(sys.argv[9]) if len(sys.argv) > 9 else Fraction(0)
    hifrac = Fraction(sys.argv[10]) if len(sys.argv) > 10 else Fraction(1)

    spf = smallest_prime_factors(y + 2)
    U = prune(x, y, D, spf, prime_cap=(cap or None))
    ms = sum(Fraction(1, n) for n in U)
    LO = lofrac * ms
    HI = min(hifrac * ms, ms)
    print("window [%d,%d] cap=%d |U|=%d maxsum=%s  band range [%s,%s]"
          % (x, y, cap, len(U), float(ms), float(LO), float(HI)), flush=True)
    tag = "%s.tmp%d" % (out, os.getpid())
    found = {}
    t0 = time.time()
    for k in range(nbands):
        lo = LO + (HI - LO) * Fraction(k, nbands)
        hi = LO + (HI - LO) * Fraction(k + 1, nbands)
        write_problem(tag + ".prob", U, D, None, lo, hi)
        subprocess.run([os.path.join(HERE, "search"), tag + ".prob", tag + ".out",
                        str(per), str(nodecap)],
                       stderr=subprocess.DEVNULL, check=True)
        for line in open(tag + ".out"):
            V = [int(t) for t in line.split()]
            s = sum(Fraction(1, n) for n in V)
            assert (s * D).denominator == 1
            c = int(s * D)
            if c not in found:
                found[c] = V
        print("  band %d/%d [%0.4f,%0.4f] pool=%d  (%.1fs)"
              % (k + 1, nbands, float(lo), float(hi), len(found), time.time() - t0),
              flush=True)
    with open(out, "w") as g:
        for c in sorted(found):
            g.write("%d %s\n" % (c, " ".join(map(str, found[c]))))
    print("pool size %d written to %s" % (len(found), out))
    for ext in (".prob", ".out"):
        try:
            os.remove(tag + ext)
        except OSError:
            pass


if __name__ == "__main__":
    main()
