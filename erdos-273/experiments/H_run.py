"""
H_run.py -- driver: for a given Y, build M = R(Y) (the L5-reduced set), compute
kappa = budget(M) - 1 exactly, and launch the exhaustive capped covering search.

CLAIM TESTED: is there a covering system of Z with distinct moduli all in H ∩ [2,Y] whose
reciprocal sum is <= budget(R(Y)) - 1?   UNSAT => no covering system of Z with distinct
moduli all of the form p-1 (p >= 5 prime) and all <= 2Y.

Usage: python3 H_run.py Y [extra args passed to H_capsearch2]
CONCLUSION: printed by the C engine.
"""
import subprocess, sys, os
from fractions import Fraction
from H_reduce import H_upto, reduce_set, budget, lcm_of

HERE = os.path.dirname(os.path.abspath(__file__))

def run(Y, extra=()):
    M = H_upto(Y)
    R, _ = reduce_set(M)
    b = budget(R)
    kappa = b - 1
    L = lcm_of(R)
    print("Y=%d  |R|=%d  budget(R)=%s=%.9f  kappa=%s=%.9f  lcm=%d"
          % (Y, len(R), b, float(b), kappa, float(kappa), L))
    if kappa <= 1:
        print("  kappa <= 1  =>  UNSAT by budget alone (no covering set has reciprocal sum <= 1)")
        return "UNSAT-budget"
    cmd = [os.path.join(HERE, "H_capsearch2"), "--mods", ",".join(map(str, R)),
           "--capfrac", "%d/%d" % (kappa.numerator, kappa.denominator)] + list(extra)
    print("  $", " ".join(cmd[:2]), "<mods>", *cmd[3:])
    sys.stdout.flush()
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(p.stdout[-4000:])
    if p.stderr:
        print("stderr tail:", p.stderr[-2000:])
    return p.stdout

if __name__ == "__main__":
    Y = int(sys.argv[1])
    run(Y, sys.argv[2:])
