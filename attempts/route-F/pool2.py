#!/usr/bin/env python3
"""Collect a pool of D-gadgets in a window, sliced by sum-band for diversity.

usage: pool2.py x y D ppcap out.txt nbands per_band nodecap [lofrac hifrac]
   ppcap = 0 means "no prime-power cap" (Rule (P) fixpoint only)
Output lines:  c  n1 n2 ...      with Sigma = c/D (re-checked exactly).
"""
import sys, os, subprocess, time
from fractions import Fraction
from lib import smallest_prime_factors
from universe import prune
from mk import write_problem

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    x, y, D, Q = (int(sys.argv[i]) for i in (1, 2, 3, 4))
    out = sys.argv[5]
    nbands, per, nodecap = (int(sys.argv[i]) for i in (6, 7, 8))
    lofrac = Fraction(sys.argv[9]) if len(sys.argv) > 9 else Fraction(0)
    hifrac = Fraction(sys.argv[10]) if len(sys.argv) > 10 else Fraction(1)
    ban = tuple(int(t) for t in sys.argv[11].split(",")) if len(sys.argv) > 11 else ()
    spf = smallest_prime_factors(y + 2)
    U = prune(x, y, D, spf, pp_cap=(Q or None), extra_ban=ban)
    ms = sum(Fraction(1, n) for n in U)
    LO, HI = lofrac * ms, min(hifrac * ms, ms)
    print("[%d,%d] ppcap=%d |U|=%d maxsum=%s band=[%s,%s]"
          % (x, y, Q, len(U), float(ms), float(LO), float(HI)), flush=True)
    tag = "%s.t%d" % (out, os.getpid())
    found = {}
    if os.path.exists(out):
        for line in open(out):
            t = line.split()
            if t:
                found[int(t[0])] = [int(v) for v in t[1:]]
        print("  (appending to existing pool of %d)" % len(found), flush=True)
    t0 = time.time()
    for k in range(nbands):
        lo = LO + (HI - LO) * Fraction(k, nbands)
        hi = LO + (HI - LO) * Fraction(k + 1, nbands)
        write_problem(tag + ".prob", U, D, None, lo, hi)
        subprocess.run([os.path.join(HERE, "search"), tag + ".prob", tag + ".out",
                        str(per), str(nodecap)], stderr=subprocess.DEVNULL)
        for line in open(tag + ".out"):
            try:
                V = [int(t) for t in line.split()]
            except ValueError:
                continue
            if not V:
                continue
            s = sum(Fraction(1, n) for n in V)
            if (s * D).denominator != 1:
                continue
            found.setdefault(int(s * D), V)
        if (k + 1) % 5 == 0 or k + 1 == nbands:
            print("  band %d/%d  pool=%d  (%.0fs)" % (k + 1, nbands, len(found),
                                                     time.time() - t0), flush=True)
        with open(out, "w") as g:
            for c in sorted(found):
                g.write("%d %s\n" % (c, " ".join(map(str, found[c]))))
    print("pool %d -> %s" % (len(found), out), flush=True)
    for e in (".prob", ".out"):
        try: os.remove(tag + e)
        except OSError: pass


if __name__ == "__main__":
    main()
