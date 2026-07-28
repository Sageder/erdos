#!/usr/bin/env python3
"""
pool.py  T N D seconds budget outfile [tag] [nseeds]

Collect a POOL of GADGETS in the window [T,N]: legal systems whose reciprocal
sum has denominator dividing D.  Runs ./search in randomised-restart mode for
`seconds` seconds per seed.  Every gadget kept is RE-VERIFIED here in exact
rational arithmetic by the independent verifier verify.py (sum recomputed from
scratch, all elements >= T, no isolated point) and the denominator condition is
asserted.

Output lines:   num den n1 n2 ... nk     (one representative per distinct value)
"""
import sys, subprocess, os, time
from fractions import Fraction
import verify as V

T = int(sys.argv[1]); N = int(sys.argv[2]); D = int(sys.argv[3])
secs = float(sys.argv[4]); budget = int(sys.argv[5]); out = sys.argv[6]
tag = sys.argv[7] if len(sys.argv) > 7 else "p"
nseeds = int(sys.argv[8]) if len(sys.argv) > 8 else 1
ycap = sys.argv[9] if len(sys.argv) > 9 else "0"

HERE = os.path.dirname(os.path.abspath(__file__))
prob = os.path.join(HERE, "prob_%s_%d_%d.txt" % (tag, T, N))
r = subprocess.run([sys.executable, os.path.join(HERE, "mk.py"), str(T), str(N), "0", "1", "1", str(D), prob, ycap],
                   capture_output=True, text=True)
print(r.stdout.strip(), flush=True)
if r.returncode:
    print("universe empty"); sys.exit(1)

best = {}
for seed in range(1, nseeds + 1):
    t0 = time.time()
    p = subprocess.run(["timeout", str(int(secs)), os.path.join(HERE, "search"), prob, "0",
                        str(budget), str(seed)], capture_output=True, text=True)
    for line in p.stdout.splitlines():
        if line.startswith("G "):
            U = [int(x) for x in line.split()[1:]]
            s = sum(Fraction(1, n) for n in U)
            if s not in best or len(U) < len(best[s]):
                best[s] = U
    print("  seed %d -> pool %d (%.0fs)" % (seed, len(best), time.time() - t0), flush=True)

for s, U in best.items():
    ok, msg = V.check(U, s, minelt=T, quiet=True)
    assert ok, (msg, U)
    assert D % s.denominator == 0, ("denominator does not divide D", s)

with open(out, "w") as f:
    for s in sorted(best):
        f.write("%d %d %s\n" % (s.numerator, s.denominator, " ".join(map(str, best[s]))))
print("wrote %s : %d distinct gadget values in [%d,%d], D=%d" % (out, len(best), T, N, D))
if best:
    print("   value range %.6f .. %.6f" % (float(min(best)), float(max(best))))
