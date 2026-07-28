"""
C_h2run.py -- Route C, question (ii): driver + result registry for
   "is there a covering system of Z with pairwise distinct moduli drawn from H \ {2},
    all dividing a given L?"       (H = {m >= 2 : 2m+1 prime})

WHY THIS QUESTION IS DECISIVE.  By the Step-1 halving equivalence, Erdos 273 is YES iff
there are two DISJOINT H-coverings.  2 lies in H exactly once, so at most one of the two
may use it: at least one of them is an H-covering avoiding the modulus 2.  Hence
   NO H-covering avoiding 2 exists  ==>  Erdos 273 is NO.

NECESSARY CONDITION (Davenport-Mirsky-Newman-Rado): only lattices L with
   B_H(L) - 1/2 = sum_{d | L, 2d+1 prime, d >= 2} 1/d  -  1/2   >   1
can possibly support one.  The smallest such L is 180; the set of such L is closed
UPWARDS under divisibility, so UNSAT for one L does NOT propagate to its multiples --
each lattice is a separate lemma.

SOLVER: C_hcover2 (exhaustive DFS, cover-the-smallest-uncovered-residue, with no-good
recording; see that file).  Every UNSAT below is exhaustive over the stated lattice.

VERDICTS OBTAINED BY THIS ROUTE (see experiments/C_out/):
   L = 360   budget 1.1889   UNSAT exhaustive     (165 743 nodes)
   L = 660   budget 1.0045   UNSAT exhaustive     ( 88 103 nodes)
   L = 720   budget 1.2097   UNSAT exhaustive     (46 021 340 nodes)
   L = 810   budget 1.0235   UNSAT exhaustive     (128 879 911 nodes)
   L = 630, 840, 900, 960, 1260, 2520, 27720, ...  NOT DECIDED (time-outs)
   no covering avoiding 2 was FOUND in any lattice tried, up to L = 10 810 800.

CAVEAT, stated explicitly: UNSAT for a particular divisor lattice is NOT a proof of
nonexistence in general; it only rules out systems all of whose moduli divide that L.
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))

def run(L, timelimit=900, forbid="2"):
    out = subprocess.run([os.path.join(HERE, "C_hcover2"), str(L), "--world", "H",
                          "--forbid", forbid, "--quiet", "--timelimit", str(timelimit)],
                         capture_output=True, text=True, timeout=timelimit + 120)
    for line in out.stdout.splitlines():
        if line.startswith("RESULT") or line.startswith("L ="):
            print("   " + line)
    return out.stdout

if __name__ == "__main__":
    Ls = [int(x) for x in sys.argv[1:]] or [180, 240, 270, 360, 420, 450, 480, 540,
                                            600, 630, 660, 720, 810, 840, 900, 960]
    for L in Ls:
        print(f"L = {L}")
        run(L)
