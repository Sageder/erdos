"""
G_07_templates.py -- Route G, step 7: classical divisor-lattice templates vs. admissibility.

CLAIM TESTED.  For each classical modulus-lattice L (L = 12, 24, 36, 48, 60, 120, 180, 360,
720, 1260, 2520, 5040, ...):
  * which divisors of L are ADMISSIBLE
        E-world:  d in E  <=>  d >= 4 and d+1 prime
        H-world:  d in H  <=>  d >= 2 and 2d+1 prime
  * the reciprocal sum of the admissible part vs the whole divisor lattice (exact fractions);
  * the EXACT minimal deformation:  min over ALL covering systems with distinct moduli > 1
    dividing L of the number of inadmissible moduli used.  (Computed by the exhaustive
    branch-and-bound G_06_mindeform; 0 would mean a solution at that L.)
  * for the canonical templates, the explicit list of inadmissible moduli.

Also verifies the classical mod-12 covering and the standard mod-24/mod-36 templates.

CONCLUSION: printed table; recorded in attempts/route-G-selfridge/FINDINGS.md.
"""
import subprocess, sys, os
from fractions import Fraction
from sympy import divisors, isprime, factorint

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "G_06_mindeform")

def inE(d): return d >= 4 and isprime(d+1)
def inH(d): return d >= 2 and isprime(2*d+1)

def run(L, admiss, cap=6, tl=180):
    ds = [d for d in divisors(L) if d > 1]
    spec = ",".join(f"{d}:{0 if admiss(d) else 1}" for d in ds)
    try:
        r = subprocess.run([BIN, str(L), spec, "--cap", str(cap), "--timelimit", str(tl)],
                           capture_output=True, text=True, timeout=tl+60)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT", ""
    out = r.stdout
    val = None; status = "?"
    for line in out.splitlines():
        if line.startswith("MIN #inadmissible"):
            val = int(line.split("=")[1].split()[0])
        if "EXHAUSTIVE" in line: status = "EXHAUSTIVE"
        if "INCOMPLETE" in line: status = "INCOMPLETE"
        if line.startswith("no covering"): val = None
    sysline = [l for l in out.splitlines() if l.startswith("SYSTEM:")]
    return val, status, (sysline[0] if sysline else "")

def report(Ls, admiss, name):
    print("=" * 96)
    print(f"WORLD: {name}")
    print(f"{'L':>8} {'#div>1':>7} {'#adm':>5} {'sum 1/d all':>13} {'sum 1/d adm':>13} "
          f"{'mindef':>7} {'status':>11}")
    for L in Ls:
        ds = [d for d in divisors(L) if d > 1]
        ad = [d for d in ds if admiss(d)]
        sa = sum(Fraction(1,d) for d in ds)
        sb = sum(Fraction(1,d) for d in ad)
        val, status, sysline = run(L, admiss)
        print(f"{L:>8} {len(ds):>7} {len(ad):>5} {float(sa):>13.5f} {float(sb):>13.5f} "
              f"{str(val):>7} {status:>11}")
        if val is not None and val <= 3:
            bad = []
            if sysline:
                import re
                ms = [int(x) for x in re.findall(r"mod (\d+)", sysline)]
                bad = sorted(m for m in ms if not admiss(m))
            print(f"          witness inadmissible moduli: {bad}")
            print(f"          {sysline}")
        print(f"          admissible divisors: {ad}")
        print(f"          INadmissible divisors: {[d for d in ds if not admiss(d)]}")
    print()

CLASSICAL = {
    "Erdos 1950 (lcm 12)":      [(0,2),(0,3),(1,4),(5,6),(7,12)],
    "shifted mod 12":           [(0,2),(1,3),(3,4),(5,6),(9,12)],
    "lcm 24 (Selfridge-like)":  [(0,2),(0,3),(1,4),(3,8),(7,12),(23,24)],
}

def check_classical():
    print("=" * 96)
    print("CLASSICAL TEMPLATES: verification + admissibility audit")
    for name, S in CLASSICAL.items():
        L = 1
        from math import gcd
        for a,m in S: L = L*m//gcd(L,m)
        unc = [x for x in range(L) if not any((x-a) % m == 0 for a,m in S)]
        mods = [m for _,m in S]
        print(f"\n  {name}: classes {S}")
        print(f"    lcm = {L}, distinct moduli = {len(set(mods))==len(mods)}, "
              f"covers Z/{L} = {not unc}" + ("" if not unc else f", uncovered={unc}"))
        print(f"    reciprocal sum = {sum(Fraction(1,m) for m in mods)}")
        print(f"    E-admissible moduli (p-1):   {[m for m in mods if inE(m)]}")
        print(f"    E-INadmissible:              {[m for m in mods if not inE(m)]}")
        print(f"    H-admissible moduli ((p-1)/2): {[m for m in mods if inH(m)]}")
        print(f"    H-INadmissible:                {[m for m in mods if not inH(m)]}")
    print()

if __name__ == "__main__":
    check_classical()
    Ls = [12, 24, 36, 48, 60, 72, 120, 180, 240, 360, 720, 1260, 2520]
    report(Ls, inH, "HALVED (H): admissible m <=> 2m+1 prime   [E-covering = 2 disjoint H-coverings]")
    report([2*x for x in Ls], inE, "E-WORLD: admissible n <=> n+1 prime")
