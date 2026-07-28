"""
P2 -- EXACT DECISION of "THE PIVOT" restricted to a divisor lattice M.

THE PIVOT: is there a covering system of Z with distinct moduli, all lying in
      H \\ {2} = {m >= 3 : 2m+1 prime}   (equivalently m = (p-1)/2, p >= 7 prime)?

Any such covering has some finite lcm L, and then every modulus divides L, so the question
splits over lattices:  for a fixed L, is there a covering of Z/L by classes b (mod m) with
m ranging over  S(L) = {m | L : m >= 3, 2m+1 prime}, each m used AT MOST ONCE?

This file decides that lattice question EXACTLY by SAT (Cadical153), written from scratch and
importing nothing from other routes.  Encoding:
    variable x[m][b]   ("class b mod m is used"),  m in S(L), 0 <= b < m
    cover clause  for each r in Z/L:  OR_{m in S} x[m][r mod m]
    at-most-one   for each m: sequential-counter AMO over {x[m][0..m-1]}   (distinct moduli)
SAT  -> explicit covering system; we re-verify it from scratch (see verify()).
UNSAT -> rigorous lemma: no covering from H\\{2} has lcm dividing L.
         (This is a statement about ONE lattice.  H\\{2} is infinite, so no finite list of
          such lemmas can prove the pivot negatively.  Say so.)

usage:  python3 P2_pivot_sat.py L1 L2 ...
"""
import sys, json, time, os
from fractions import Fraction
from sympy import isprime


def divisors(n):
    ds, i = [], 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds)


def pool(L):
    """S(L) = {m | L : m >= 3, 2m+1 prime}  -- the pivot pool on lattice L."""
    return [m for m in divisors(L) if m >= 3 and isprime(2 * m + 1)]


def verify(L, cert):
    """Independent from-scratch verification of a claimed pivot certificate.
    cert is a list of (m, b).  Checks: moduli distinct, each >= 3, 2m+1 prime,
    m | L, and a FULL sweep of Z/L shows every residue covered."""
    ms = [m for m, _ in cert]
    assert len(set(ms)) == len(ms), "moduli not distinct"
    for m, b in cert:
        assert m >= 3, f"modulus {m} < 3 (the forbidden 2 or smaller)"
        assert isprime(2 * m + 1), f"2*{m}+1 not prime -- {m} not in H"
        assert L % m == 0, f"{m} does not divide {L}"
        assert 0 <= b < m
    covered = bytearray(L)
    for m, b in cert:
        for r in range(b % m, L, m):
            covered[r] = 1
    missing = [r for r in range(L) if not covered[r]]
    assert not missing, f"uncovered residues mod {L}: {missing[:20]} (total {len(missing)})"
    # independent second check: the classes are periodic mod L, so covering Z/L == covering Z
    return True


def decide(L, timeout=None, verbose=True):
    from pysat.formula import IDPool, CNF
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Cadical153

    S = pool(L)
    if not S:
        return ('UNSAT', None, 'empty pool')
    budget = sum(Fraction(1, m) for m in S)
    if budget <= 1:
        return ('UNSAT', None, f'budget {float(budget):.6f} <= 1')

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
    t0 = time.time()
    with Cadical153(bootstrap_with=cnf) as s:
        res = s.solve()
        el = time.time() - t0
        if not res:
            return ('UNSAT', None, f'{el:.1f}s  |S|={len(S)} budget={float(budget):.5f} '
                                   f'vars={vp.top} clauses={len(cnf.clauses)}')
        model = set(l for l in s.get_model() if l > 0)
    cert = sorted((m, b) for m in S for b in range(m) if x[(m, b)] in model)
    verify(L, cert)
    return ('SAT', cert, f'{el:.1f}s  |S|={len(S)} budget={float(budget):.5f}')


if __name__ == "__main__":
    Ls = [int(a) for a in sys.argv[1:]] or [1080, 1260, 1680, 2160, 2520]
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'P2_out')
    os.makedirs(outdir, exist_ok=True)
    for L in Ls:
        S = pool(L)
        b = sum(Fraction(1, m) for m in S)
        print(f"L = {L:<8} |S| = {len(S):3d} budget = {float(b):.5f}  pool = {S}", flush=True)
        verdict, cert, info = decide(L)
        if verdict == 'SAT':
            path = os.path.join(outdir, f'pivot_cert_{L}.json')
            with open(path, 'w') as f:
                json.dump({'lattice': L, 'claim': 'covering system of Z, distinct moduli, '
                           'every modulus m>=3 with 2m+1 prime (i.e. m=(p-1)/2, p>=7 prime)',
                           'classes': [[m, bb] for m, bb in cert]}, f, indent=1)
            print(f"  ** SAT **  {info}  -> CERTIFICATE {path}")
            print(f"     {len(cert)} classes: {cert}", flush=True)
        else:
            print(f"  UNSAT (no pivot covering with lcm | {L})   {info}", flush=True)
