"""
P2_xcheck -- validation battery for P2_mdfs (the exhaustive modulus-ordered pivot decider).

P2_mdfs uses two reductions whose soundness carries the whole verdict:
   (a) translation-orbit normalisation  b_{m_i} in [0, gcd(lcm(used so far), m_i)),
   (b) dominance: a class covering nothing new is dropped in favour of SKIP.
This script checks P2_mdfs against a COMPLETELY DIFFERENT decision procedure -- a SAT encoding
solved by Cadical153 -- on a large family of (L, minm) instances, including many where the
answer is SAT (positive controls, so a bug that makes the search miss solutions would show up).

Every SAT verdict is additionally verified from scratch: distinct moduli, each >= minm,
2m+1 prime, m | L, and a full sweep of Z/L.

usage: python3 P2_xcheck.py [LMAX]
"""
import sys, os, subprocess, random
from sympy import isprime

HERE = os.path.dirname(os.path.abspath(__file__))
MDFS = os.path.join(HERE, 'P2_mdfs')


def divisors(n):
    ds, i = [], 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds)


def pool(L, minm):
    return [m for m in divisors(L) if m >= minm and isprime(2 * m + 1)]


def sat_decide(L, minm):
    from pysat.formula import IDPool, CNF
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Cadical153
    S = pool(L, minm)
    if not S:
        return ('UNSAT', None)
    vp = IDPool()
    x = {(m, b): vp.id(('x', m, b)) for m in S for b in range(m)}
    cnf = CNF()
    for r in range(L):
        cnf.append([x[(m, r % m)] for m in S])
    for m in S:
        lits = [x[(m, b)] for b in range(m)]
        if len(lits) > 1:
            cnf.extend(CardEnc.atmost(lits=lits, bound=1, vpool=vp,
                                      encoding=EncType.seqcounter).clauses)
    with Cadical153(bootstrap_with=cnf) as s:
        if not s.solve():
            return ('UNSAT', None)
        mod = set(l for l in s.get_model() if l > 0)
    return ('SAT', sorted((m, b) for m in S for b in range(m) if x[(m, b)] in mod))


def verify(L, minm, cert):
    ms = [m for m, _ in cert]
    assert len(set(ms)) == len(ms)
    cov = bytearray(L)
    for m, b in cert:
        assert m >= minm and isprime(2 * m + 1) and L % m == 0 and 0 <= b < m
        for r in range(b, L, m):
            cov[r] = 1
    assert all(cov), "certificate does not cover Z/L"


def mdfs_decide(L, minm, extra=()):
    out = subprocess.run([MDFS, str(L), '--minm', str(minm)] + list(extra),
                         capture_output=True, text=True, timeout=1200).stdout
    if 'UNSAT' in out:
        return ('UNSAT', None)
    if out.startswith('CAP') or '\nCAP' in out:
        return ('CAP', None)
    cert = []
    for tok in out.split('SAT :')[1].split('\n')[0].split():
        b, m = tok.replace(')', '').split('(mod')
        cert.append((int(m), int(b)))
    return ('SAT', sorted(cert))


def main(LMAX):
    tests = []
    for L in range(4, LMAX + 1):
        for minm in (2, 3):
            tests.append((L, minm))
    random.seed(273)
    for L in [420, 480, 540, 600, 630, 660, 720, 840, 900, 960, 990, 1008, 1080, 1170, 1200,
              288, 576, 864, 1152, 1440, 1512, 1530, 1560]:
        for minm in (2, 3):
            tests.append((L, minm))
    nsat = nunsat = 0
    bad = []
    for (L, minm) in tests:
        if not pool(L, minm):
            continue
        v1, c1 = mdfs_decide(L, minm)
        v2, c2 = sat_decide(L, minm)
        if v1 != v2:
            bad.append((L, minm, v1, v2))
            print(f"  ** MISMATCH ** L={L} minm={minm}: mdfs={v1} sat={v2}", flush=True)
            continue
        if v1 == 'SAT':
            verify(L, minm, c1)
            verify(L, minm, c2)
            nsat += 1
        else:
            nunsat += 1
    print(f"\nagreement on {nsat + nunsat} instances: {nsat} SAT (certificates re-verified), "
          f"{nunsat} UNSAT;  mismatches: {len(bad)}")
    if bad:
        print("MISMATCHES:", bad)
    else:
        print("P2_mdfs agrees with an independent SAT decision on every instance tested.")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 400)
