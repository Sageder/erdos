"""
D_06_greedy_phi.py

CLAIM TESTED: is the necessary condition  Phi_q(D_H(L)) >= 2  (see D_05_run.py) actually
VIOLATED for the best candidate L, i.e. does the q-adic fiber max-min give an obstruction?

Phi_q is a max-min, so any explicit residue assignment gives a LOWER bound on it.  This
script runs a randomised LPT-style greedy (place the heaviest item at the q-adic node whose
leaf-block currently has the smallest minimum) with restarts.  If the greedy already reaches
>= 2 then Phi_q >= 2 and the fiber condition at q is SATISFIED -- no obstruction, rigorously
(one-sided: a witness assignment is a proof of >=).

CONCLUSION: printed at run time.
"""
import sys, random
from sympy import isprime, factorint


def DH(L):
    ds = []
    d = 1
    while d * d <= L:
        if L % d == 0:
            for x in (d, L // d):
                if x >= 2 and isprime(2 * x + 1):
                    ds.append(x)
        d += 1
    return sorted(set(ds))


def nu(m, q):
    j = 0
    while m % q == 0:
        m //= q
        j += 1
    return j


def greedy(ds, q, restarts=300, seed=0):
    e = max(nu(m, q) for m in ds)
    flat = sum(1.0 / m for m in ds if m % q != 0)
    if e == 0:
        return flat, 0, 0, None
    items = [(nu(m, q), q ** nu(m, q) / m, m) for m in ds if m % q == 0]
    items.sort(key=lambda t: -t[1])
    NL = q ** e
    rng = random.Random(seed)
    bestv, bestasg = -1.0, None
    for R in range(restarts):
        cur = [flat] * NL
        if R == 0:
            order = list(items)
        else:
            order = sorted(items, key=lambda t: -t[1] * (1 + rng.uniform(-0.15, 0.15)))
        asg = {}
        for (j, w, m) in order:
            blk = q ** (e - j)
            nn = q ** j
            bi, bk = None, None
            for v in range(nn):
                seg = cur[v * blk:(v + 1) * blk]
                key = (min(seg), sum(seg))
                if bk is None or key < bk:
                    bk, bi = key, v
            for t in range(bi * blk, (bi + 1) * blk):
                cur[t] += w
            asg[m] = bi
        v = min(cur)
        if v > bestv:
            bestv, bestasg = v, dict(asg)
    return bestv, e, len(items), bestasg


def main(Ls, restarts=300):
    for L in Ls:
        ds = DH(L)
        b = sum(1.0 / m for m in ds)
        print("L=%-10d fac=%-34s |D_H|=%-4d budget=%.5f"
              % (L, dict(factorint(L)), len(ds), b))
        allok = True
        for q in sorted(factorint(L)):
            v, e, ni, _ = greedy(ds, q, restarts)
            ok = v >= 2.0
            allok &= ok
            print("    q=%-3d e=%d items=%-4d  Phi_q >= %.5f   %s"
                  % (q, e, ni, v, "SATISFIED (>=2)" if ok
                     else "greedy < 2  (inconclusive: greedy is only a lower bound)"))
        print("    => all fiber conditions witnessed satisfied: %s" % allok)


if __name__ == "__main__":
    Ls = [int(a) for a in sys.argv[1:]] or [27720, 720720, 1801800]
    main(Ls)
