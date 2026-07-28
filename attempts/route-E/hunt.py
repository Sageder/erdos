#!/usr/bin/env python3
"""
hunt.py  target poolfile probfile2 seconds budget [seed0]

Two-window hunt.  `poolfile` is a pool of gadgets (legal systems with
denominator dividing D) in a LOW window; `probfile2` is a problem file for a
DISJOINT HIGHER window, searched in gadget mode.  For every gadget found in the
higher window with value s2 we test whether  target - s2  occurs in the pool; if
it does, the union of the two gadgets is a legal system with sum exactly
`target` and minimum element = min of the low window.

Everything exact (Fraction).  The certificate is re-verified before printing.
"""
import sys, subprocess, os, time
from fractions import Fraction
import verify as V

target = Fraction(sys.argv[1])
poolfile = sys.argv[2]; prob2 = sys.argv[3]
secs = float(sys.argv[4]); budget = int(sys.argv[5])
seed0 = int(sys.argv[6]) if len(sys.argv) > 6 else 1
HERE = os.path.dirname(os.path.abspath(__file__))

pool = {}
for line in open(poolfile):
    t = line.split()
    if len(t) < 3:
        continue
    v = Fraction(int(t[0]), int(t[1]))
    U = [int(x) for x in t[2:]]
    if v not in pool or len(U) < len(pool[v]):
        pool[v] = U
print("# pool %d values, range %.5f .. %.5f" % (len(pool), float(min(pool)), float(max(pool))), flush=True)

t0 = time.time()
seed = seed0
tried = 0
while time.time() - t0 < secs:
    p = subprocess.run(["timeout", "60", os.path.join(HERE, "search"), prob2, "0", str(budget), str(seed)],
                       capture_output=True, text=True)
    seed += 1
    for line in p.stdout.splitlines():
        if not line.startswith("G "):
            continue
        U2 = [int(x) for x in line.split()[1:]]
        s2 = sum(Fraction(1, n) for n in U2)
        tried += 1
        need = target - s2
        if need in pool:
            U1 = pool[need]
            U = sorted(U1 + U2)
            ok, msg = V.check(U, target, minelt=min(U))
            print("HIT  s1=%s  s2=%s" % (need, s2))
            print("CERT", " ".join(map(str, U)))
            print(msg if ok else "VERIFY FAILED " + msg)
            sys.exit(0 if ok else 1)
    print("# seed %d done, %d gadgets tried, %.0fs" % (seed - 1, tried, time.time() - t0), flush=True)
print("# no hit after %d high-window gadgets" % tried)
