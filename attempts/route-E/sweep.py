#!/usr/bin/env python3
"""
sweep.py T u v Nlist ylist [secs]

For each window [T,N] and prime cap y, build the exact-mode problem for the
target u/v and run ./search with a wall-clock limit.  Reports FOUND (with the
certificate re-verified) / EXHAUSTED-EMPTY (a rigorous negative for that
restricted universe) / TIMEOUT.

Capping the primes only DELETES elements, so
  * FOUND  is a genuine certificate for the full problem;
  * EXHAUSTED-EMPTY is a negative statement about the capped universe only
    (for y = 0, i.e. no cap, it is a negative for the whole window).
"""
import sys, subprocess, os
from fractions import Fraction
import verify as V

T = int(sys.argv[1]); u = int(sys.argv[2]); v = int(sys.argv[3])
Ns = [int(x) for x in sys.argv[4].split(",")]
ys = [int(x) for x in sys.argv[5].split(",")]
secs = int(sys.argv[6]) if len(sys.argv) > 6 else 60
HERE = os.path.dirname(os.path.abspath(__file__))
target = Fraction(u, v)

for N in Ns:
    for y in ys:
        prob = os.path.join(HERE, "sw_%d_%d_%d.txt" % (T, N, y))
        r = subprocess.run([sys.executable, os.path.join(HERE, "mk.py"), str(T), str(N), "1",
                            str(u), str(v), "1", prob, str(y)], capture_output=True, text=True)
        if r.returncode:
            print("T=%d N=%d y=%d : EMPTY UNIVERSE" % (T, N, y), flush=True); continue
        info = r.stdout.strip()
        p = subprocess.run(["timeout", str(secs), os.path.join(HERE, "search"), prob, "1", "0", "1"],
                           capture_output=True, text=True)
        out = p.stdout
        status = "TIMEOUT"
        cert = None
        for line in out.splitlines():
            if line.startswith("SOL"):
                cert = [int(x) for x in line.split()[1:]]
                status = "FOUND"
            elif "done EXHAUSTIVE" in line and cert is None:
                status = "EXHAUSTED-NONE " + line.split("nodes=")[1].split()[0] + " nodes"
        print("T=%-5d N=%-5d y=%-4d %s | %s" % (T, N, y, info.split("|univ|=")[1] if "|univ|=" in info else "", status), flush=True)
        if cert:
            ok, msg = V.check(cert, target, minelt=T)
            print("   CERT", " ".join(map(str, cert)))
            print("   " + msg.replace("\n", "\n   ") if ok else "   VERIFY FAILED: " + msg, flush=True)
            sys.exit(0)
