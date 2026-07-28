"""k5_calibration.py — the decisive methodological check.

Route R9 reports that finite avoiders die under every linear displacement bound
pos(v) <= C*v, for k = 5 as well as k = 4.  This matters enormously: for k = 5 an
INFINITE avoider is KNOWN to exist ([DEGS77](b)), so if the k=5 finite walls look like
the k=4 walls, then "linear-profile extinction at every C" is NOT evidence for the
affirmative answer at k=4, and — more sharply — a complete LP theorem (extinction for
every linear C) would NOT prove 196-YES, because CORE.md Lemma 6 quantifies over ALL
profiles phi, not just linear ones.

This script computes, for k = 4 and k = 5 side by side, the minimal N at which no
permutation of [1..N] with pos(v) <= floor(C*v) avoids monotone k-APs (both
orientations), by exact SAT with eager transitivity and two independent solvers.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from pysat.solvers import Cadical195, Glucose42
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def build_k(N, k, C):
    pool = IDPool()
    def var(u, w):
        return pool.id(('x', u, w))
    def lit(u, w):
        return var(u, w) if u < w else -var(w, u)
    cl = []
    for u in range(1, N + 1):                      # eager transitivity
        for v in range(u + 1, N + 1):
            for w in range(v + 1, N + 1):
                a, b, c = var(u, v), var(v, w), var(u, w)
                cl.append([-a, -b, c]); cl.append([a, b, -c])
    for e in range(1, (N - 1) // (k - 1) + 1):     # forbid both orientations of k-APs
        for x in range(1, N - (k - 1) * e + 1):
            steps = [lit(x + j * e, x + (j + 1) * e) for j in range(k - 1)]
            cl.append([-s for s in steps])
            cl.append(list(steps))
    for v in range(1, N + 1):                      # profile pos(v) <= floor(C*v)
        bound = int(C * v)
        if bound >= N:
            continue
        lits = [lit(w, v) for w in range(1, N + 1) if w != v]
        cl.extend(CardEnc.atmost(lits=lits, bound=bound - 1, vpool=pool,
                                 encoding=EncType.seqcounter).clauses)
    return cl


def sat(N, k, C, both_solvers=True):
    cl = build_k(N, k, C)
    r1 = Cadical195(bootstrap_with=cl).solve()
    if both_solvers:
        r2 = Glucose42(bootstrap_with=cl).solve()
        assert r1 == r2, f"SOLVERS DISAGREE at N={N}, k={k}, C={C}"
    return r1


def threshold(k, C, nmax=70):
    """Minimal N with no profile-bounded k-AP-free permutation (None if > nmax)."""
    lo = None
    for N in range(4, nmax + 1):
        t0 = time.time()
        s = sat(N, k, C)
        if not s:
            return N, lo
        lo = N
        if time.time() - t0 > 120:
            return None, lo
    return None, lo


if __name__ == "__main__":
    print("minimal N with NO monotone-k-AP-free permutation of [1..N] under pos(v) <= floor(C*v)")
    print(" (k=4 is Erdos 196, open; k=5 has a KNOWN infinite avoider [DEGS77(b)])\n")
    for C in (1.25, 1.5, 1.75, 2.0):
        row = []
        for k in (4, 5):
            t0 = time.time()
            N_ext, N_last = threshold(k, C)
            dt = time.time() - t0
            row.append(f"k={k}: " + (f"EXTINCT at N={N_ext}" if N_ext else
                                     f"alive through N={N_last}") + f" ({dt:.0f}s)")
        print(f"C={C}:  " + " | ".join(row), flush=True)
