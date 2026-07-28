"""
H_run2.py -- Route H main driver.  For a given Y it tries, in increasing order of cost, to
prove: THERE IS NO COVERING SYSTEM OF Z WITH DISTINCT MODULI ALL IN E AND ALL <= 2Y.

Chain of proved reductions (details + proofs in ../attempts/route-H-minimalS/FINDINGS.md):

 (E<->H)  E = 2H, H = {m>=2 : 2m+1 prime}.  An E-covering with all moduli <= 2Y exists
          <=> two DISJOINT covering sets A,B ⊆ H ∩ [2,Y] exist.
 (L5)     prime removal: |A_q| < q  =>  A minus the multiples of q is still a covering set.
          Hence WLOG A,B ⊆ M := R(Y) (the L5-fixpoint of H ∩ [2,Y]).
 (DMNR)   distinct moduli > 1  =>  reciprocal sum > 1.  Since A,B ⊆ M are disjoint,
          1 < budget(A) < budget(M) - 1 =: kappa  and likewise for B.
 (PAIR)   for every prime q with  #{m in M : q|m} < 2q,  min(|A_q|,|B_q|) < q, so by (L5)
          at least ONE of A,B is a covering set inside  M_q := R(M \ multiples of q).

Tests attempted:
  T-budget : kappa <= 1                                   => done.
  T-q      : for some q as in (PAIR), budget(M_q) <= 1     => done.
  T-qsearch: for some q as in (PAIR), exhaustive capped search in M_q with cap kappa is UNSAT
                                                          => done.
  T-full   : exhaustive capped search in M itself is UNSAT => done.

Usage: python3 H_run2.py Y [--timeout S] [--maxnodes N]
CONCLUSION: printed.
"""
import subprocess, sys, os, time
from fractions import Fraction
from sympy import factorint
from H_reduce import H_upto, reduce_set, budget, lcm_of

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "H_capsearch2")


def capped_search(mods, kappa, maxnodes=0, timeout=None, extra=()):
    cmd = [ENGINE, "--mods", ",".join(map(str, mods)),
           "--capfrac", "%d/%d" % (kappa.numerator, kappa.denominator)]
    if maxnodes:
        cmd += ["--maxnodes", str(maxnodes)]
    cmd += list(extra)
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", time.time() - t0, ""
    out = p.stdout
    for tag in ("RESULT: UNSAT", "RESULT: SAT", "RESULT: UNKNOWN"):
        if tag in out:
            return tag.split()[1], time.time() - t0, out
    return "ERR", time.time() - t0, out + p.stderr


def analyse(Y, maxnodes=0, timeout=None, do_full=True):
    M0 = H_upto(Y)
    M, _ = reduce_set(M0)
    b = budget(M)
    kappa = b - 1
    print("=" * 78)
    print("Y = %d   |H∩[2,Y]| = %d   |R(Y)| = %d   budget(R) = %s = %.9f   lcm = %d"
          % (Y, len(M0), len(M), b, float(b), lcm_of(M)))
    print("   R(Y) =", M)
    print("   kappa = budget(R)-1 = %s = %.9f" % (kappa, float(kappa)))
    if kappa <= 1:
        print("   ==> T-budget: kappa <= 1, and every covering set has reciprocal sum > 1.")
        print("   ==> PROVED: no E-covering with all moduli <= %d" % (2 * Y))
        return True

    primes = sorted({p for m in M for p in factorint(m)})
    cands = []
    for q in primes:
        cnt = sum(1 for m in M if m % q == 0)
        if cnt < 2 * q:
            Mq, _ = reduce_set([m for m in M if m % q != 0])
            cands.append((q, cnt, Mq, budget(Mq)))
    print("   primes with #multiples < 2q (so one of A,B avoids them):",
          [(q, c) for (q, c, _, _) in cands] or "none")
    for (q, cnt, Mq, bq) in sorted(cands, key=lambda t: float(t[3])):
        print("     q=%d: #mult=%d ; M_q has %d moduli, budget %.6f, lcm %d"
              % (q, cnt, len(Mq), float(bq), lcm_of(Mq)))
        if bq <= 1:
            print("        ==> T-q: budget(M_q) <= 1 so M_q holds no covering set.")
            print("   ==> PROVED: no E-covering with all moduli <= %d" % (2 * Y))
            return True
        st, dt, out = capped_search(Mq, kappa, maxnodes, timeout)
        print("        capped search on M_q: %s  (%.1fs)" % (st, dt))
        if st == "UNSAT":
            print("        ==> T-qsearch UNSAT.")
            print("   ==> PROVED: no E-covering with all moduli <= %d" % (2 * Y))
            return True
        if st == "SAT":
            print("        (a covering set with reciprocal sum <= kappa EXISTS in M_q:)")
            print(out[out.find("SOLUTION"):][:600])
    if do_full:
        st, dt, out = capped_search(M, kappa, maxnodes, timeout)
        print("   full capped search on R(Y): %s (%.1fs)" % (st, dt))
        if st == "UNSAT":
            print("   ==> PROVED: no E-covering with all moduli <= %d" % (2 * Y))
            return True
    print("   ==> NOT decided at Y=%d by this chain." % Y)
    return False


if __name__ == "__main__":
    args = sys.argv[1:]
    Ys = []
    maxnodes = 0
    timeout = None
    i = 0
    while i < len(args):
        if args[i] == "--maxnodes":
            maxnodes = int(args[i + 1]); i += 2
        elif args[i] == "--timeout":
            timeout = float(args[i + 1]); i += 2
        elif args[i] == "--nofull":
            i += 1
        else:
            Ys.append(int(args[i])); i += 1
    for Y in Ys:
        analyse(Y, maxnodes, timeout)
        sys.stdout.flush()
