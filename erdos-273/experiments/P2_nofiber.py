"""P2_nofiber -- validate the FIBER stage of the pipeline.
P2_exact2 skips a lattice as soon as some exact Phi_q < 1; if that test were buggy it could hide
a pivot certificate.  This script re-decides every candidate lattice with P2_mdfs, which contains
NO fiber test at all -- only the exhaustive modulus-ordered search.  Every candidate must come out
infeasible."""
import subprocess, sys, os
from sympy import isprime
HERE = os.path.dirname(os.path.abspath(__file__))
def divs(n):
    ds, i = [], 1
    while i*i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n//i: ds.append(n//i)
        i += 1
    return sorted(ds)
LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
cands = []
for L in range(6, LMAX+1):
    S = [m for m in divs(L) if m >= 3 and isprime(2*m+1)]
    if S and sum(1.0/m for m in S) > 1: cands.append(L)
print(f'candidates (budget>1) up to {LMAX}: {len(cands)}', flush=True)
bad = []
for L in cands:
    out = subprocess.run([os.path.join(HERE,'P2_mdfs'), str(L), '--nodes','100000000000'],
                         capture_output=True, text=True).stdout
    if 'UNSAT' not in out:
        bad.append((L, out.strip().split('\n')[-1])); print('  ** ', L, out.strip()[-120:], flush=True)
print(f'done. lattices NOT proved infeasible by the fiber-free exhaustive search: {bad}')
