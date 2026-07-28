"""
G_08_sigma.py -- Route G, step 8: how much reciprocal sum does a covering actually cost?

CLAIM TESTED.  Define, for a modulus lattice L and a least-modulus threshold t,
    sigma_t(L) = min { sum_i 1/n_i : {a_i mod n_i} is a covering system of Z,
                       moduli DISTINCT, t <= n_1 < ... < n_k, every n_i | L }
(and +infinity if no such covering exists).  We compute sigma_t(L) EXACTLY by exhaustive
branch-and-bound (G_06_mindeform with per-modulus cost L/m, so the objective is the exact
integer L * sum 1/n_i).

WHY THIS MATTERS.  By the structure lemma an E-covering with lcm 2M is a pair of DISJOINT
H-coverings with moduli dividing M, so it needs
      sum_{m in D_H(M)} 1/m  >=  (cost of a covering containing m=2) + (cost of one with
                                  least modulus >= 3),
i.e.  s(M) >= sigma_2 + sigma_3  where sigma_t = inf_L sigma_t(L).  G_05 measured
max s(M) ~ 2.22 over smooth M <= 3*10^6 and best balanced half ~ 1.11.  So the question is
whether sigma_3 can be pushed below ~1.11.  These runs measure how the achievable
reciprocal sums behave.

CONCLUSION: printed table; recorded in attempts/route-G-selfridge/FINDINGS.md.
"""
import subprocess, os, sys
from fractions import Fraction
from sympy import divisors, isprime

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "G_06_mindeform")

def inH(d): return d >= 2 and isprime(2*d+1)

def sigma(L, pool, cap=None, tl=45):
    if not pool: return None, "empty"
    spec = ",".join(f"{d}:{L//d}" for d in pool)
    args = [BIN, str(L), spec, "--timelimit", str(tl)]
    if cap: args += ["--cap", str(cap)]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=tl+60)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    st = "EXHAUSTIVE" if "EXHAUSTIVE" in r.stdout else ("INCOMPLETE" if "INCOMPLETE" in r.stdout else "?")
    val = None
    for line in r.stdout.splitlines():
        if line.startswith("MIN #inadmissible"):
            val = int(line.split("=")[1].split()[0])
    sysline = [l for l in r.stdout.splitlines() if l.startswith("SYSTEM:")]
    return (Fraction(val, L) if val is not None else None), st + (" | " + sysline[0] if sysline else "")

def main():
    Ls = [12, 24, 36, 48, 60, 72, 120, 144, 180, 240, 360, 720]
    print("sigma_t(L) = exact minimal reciprocal sum of a covering with distinct moduli | L,")
    print("least modulus >= t.  'all' = every divisor > 1 allowed; 'H' = only m with 2m+1 prime.\n")
    print(f"{'L':>7} | {'sigma_2(L) all':>28} | {'sigma_3(L) all':>28}")
    for L in Ls:
        ds = [d for d in divisors(L) if d > 1]
        s2, st2 = sigma(L, ds)
        s3, st3 = sigma(L, [d for d in ds if d >= 3])
        f = lambda v: f"{str(v)} = {float(v):.5f}" if v is not None else "none"
        print(f"{L:>7} | {f(s2):>28} | {f(s3):>28}")
    print()
    print(f"{'M':>7} | {'sigma_2(M) H-only':>28} | {'sigma_3(M) H-only':>28}")
    for L in Ls + [1260, 2520]:
        ds = [d for d in divisors(L) if d > 1 and inH(d)]
        s2, st2 = sigma(L, ds)
        s3, st3 = sigma(L, [d for d in ds if d >= 3])
        f = lambda v: f"{str(v)} = {float(v):.5f}" if v is not None else "none"
        print(f"{L:>7} | {f(s2):>28} | {f(s3):>28}")

main()
