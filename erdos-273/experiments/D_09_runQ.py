"""
D_09_runQ.py -- driver for D_08_phiQ (multi-prime fiber condition).

CLAIM TESTED.  Necessary condition for Erdos 273 (Prop. D1 + multi-prime fiber lemma):
for every set Q of primes,   Phi_Q( D_H(L) ) >= 2,  where L is the H-world lcm.
Monotone in L under divisibility, and Phi_Q <= min_{q in Q} Phi_{q}: strictly stronger than
the single-prime test of D_05/D_06.

For each candidate L and each Q we
  * first run a randomised greedy (a witness => rigorous proof of  Phi_Q >= 2),
  * if the greedy fails, run the exact branch and bound (PHI_LT => L is KILLED, rigorously,
    together with every divisor of L).

CONCLUSION: printed at run time.
"""
import subprocess, os, sys, random, itertools
from sympy import isprime, factorint

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "D_08_phiQ")


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


def build(ds, Q):
    e = [max(nu(m, q) for m in ds) for q in Q]
    flat = sum(1.0 / m for m in ds if all(m % q for q in Q))
    items = []
    for m in ds:
        lv = [nu(m, q) for q in Q]
        if any(lv):
            w = 1.0
            for q, j in zip(Q, lv):
                w *= q ** j
            items.append((lv, w / m))
    return e, flat, items


def greedy_Q(e, flat, items, Q, restarts=200, seed=0):
    dims = [q ** ei for q, ei in zip(Q, e)]
    NL = 1
    for d in dims:
        NL *= d
    stride = []
    s = 1
    for d in dims:
        stride.append(s)
        s *= d
    # precompute, once, the list of leaf-index-lists for every placement of every item
    cache = {}
    def boxes(lv):
        key = tuple(lv)
        if key in cache:
            return cache[key]
        out = []
        for v in itertools.product(*[range(q ** j) for q, j in zip(Q, lv)]):
            rngs = [range(v[i], q ** e[i], q ** lv[i]) for i, q in enumerate(Q)]
            out.append([sum(c * st for c, st in zip(combo, stride))
                        for combo in itertools.product(*rngs)])
        cache[key] = out
        return out
    prepped = [(boxes(lv), w) for lv, w in items]
    rng = random.Random(seed)
    order0 = sorted(range(len(prepped)), key=lambda i: -prepped[i][1])
    best = -1.0
    for R in range(restarts):
        cur = [flat] * NL
        order = order0 if R == 0 else sorted(
            range(len(prepped)),
            key=lambda i: -prepped[i][1] * (1 + rng.uniform(-0.15, 0.15)))
        for i in order:
            bxs, w = prepped[i]
            bi, bk = None, None
            for idx in bxs:
                mn = 1e18
                sm = 0.0
                for j in idx:
                    x = cur[j]
                    sm += x
                    if x < mn:
                        mn = x
                key = (mn, sm)
                if bk is None or key < bk:
                    bk, bi = key, idx
            for j in bi:
                cur[j] += w
        v = min(cur)
        if v > best:
            best = v
    return best, NL


def exact_Q(e, flat, items, Q, target=2.0, nodecap=3_000_000_000):
    args = [BIN, str(len(Q))]
    for q, ei in zip(Q, e):
        args += [str(q), str(ei)]
    args += [str(len(items)), str(nodecap), "%.17g" % target]
    inp = "%.17g\n" % flat + "".join(
        " ".join(str(j) for j in lv) + " %.17g\n" % w for lv, w in items)
    r = subprocess.run(args, input=inp, capture_output=True, text=True)
    return (r.stdout or r.stderr).strip()


def test(L, Qs, restarts=150, verbose=True):
    ds = DH(L)
    b = sum(1.0 / m for m in ds)
    if verbose:
        print("L=%-10d fac=%-34s |D_H|=%-4d budget=%.5f"
              % (L, dict(factorint(L)), len(ds), b))
    for Q in Qs:
        if any(L % q for q in Q):
            continue
        e, flat, items = build(ds, Q)
        g, NL = greedy_Q(e, flat, items, Q, restarts, seed=L)
        if g >= 2.0:
            if verbose:
                print("   Q=%-12s e=%s cells=%-5d items=%-4d greedy Phi_Q >= %.5f  SATISFIED"
                      % (Q, e, NL, len(items), g))
            continue
        out = exact_Q(e, flat, items, Q)
        if verbose:
            print("   Q=%-12s e=%s cells=%-5d items=%-4d greedy %.5f -> exact %s"
                  % (Q, e, NL, len(items), g, out))
        if out.startswith("PHI_LT"):
            return ("KILLED", Q, out)
        if out.startswith("PHI_UNKNOWN"):
            return ("UNKNOWN", Q, out)
    return ("survives", None, None)


if __name__ == "__main__":
    Ls = [int(a) for a in sys.argv[1:]] or [720720, 1801800, 1441440]
    Qs = [(2, 3), (2, 5), (3, 5), (2, 7), (2, 3, 5)]
    for L in Ls:
        v, Q, out = test(L, Qs)
        print("   ==> %s %s %s\n" % (v, Q or "", out or ""))
        sys.stdout.flush()
