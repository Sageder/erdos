#!/usr/bin/env python3
"""Probe: how fast does the engine produce gadgets in a given window/cap?
usage: probe.py D timeout_sec  x:y:cap [x:y:cap ...]
"""
import sys, os, time, subprocess
from fractions import Fraction
from lib import smallest_prime_factors
from universe import prune, lcm_of
from mk import write_problem
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
D = int(sys.argv[1]); TO = float(sys.argv[2])
specs = sys.argv[3:]
mx = max(int(s.split(":")[1]) for s in specs)
spf = smallest_prime_factors(mx + 2)
for s in specs:
    x, y, cap = (int(t) for t in s.split(":"))
    U = prune(x, y, D, spf, prime_cap=(cap or None))
    if not U:
        print("%-22s EMPTY" % s); continue
    L = lcm_of(U); lam = (L // gcd(L, D)).bit_length()
    ms = sum(Fraction(1, n) for n in U)
    pf = "probe%d.prob" % os.getpid(); of = "probe%d.out" % os.getpid()
    write_problem(pf, U, D, None, Fraction(0), ms)
    t0 = time.time()
    try:
        subprocess.run([os.path.join(HERE, "search"), pf, of, "400", "10000000000"],
                       stderr=subprocess.DEVNULL, timeout=TO)
    except subprocess.TimeoutExpired:
        pass
    dt = time.time() - t0
    vals = []
    for line in open(of):
        try:
            V = [int(t) for t in line.split()]
        except ValueError:
            continue
        vals.append(float(sum(Fraction(1, n) for n in V)))
    print("%-22s |U|=%-4d lam=%-4d maxsum=%.4f  found=%-4d in %.1fs   range=[%s,%s]"
          % (s, len(U), lam, float(ms), len(vals), dt,
             "%.4f" % min(vals) if vals else "-", "%.4f" % max(vals) if vals else "-"))
    sys.stdout.flush()
    for f in (pf, of):
        try: os.remove(f)
        except OSError: pass
