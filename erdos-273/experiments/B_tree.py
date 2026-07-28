"""
B_tree.py -- Route B: the hierarchical (tree/chain) construction driver.

CLAIM TESTED
------------
Route B builds a covering system with moduli in E as a rooted tree of residue classes.
A node is a class r (mod D); it is finished using only moduli that are multiples of D.
Rescaling x = r + D y, the node problem is

    (NODE(D, M, holes))   cover  Z/M \\ (union of the hole classes)
                          with distinct moduli f | M, f >= 2, D*f+1 prime, D*f unused.

* holes = empty  ->  the node is CLOSED (subtree finished).
* holes = {0 mod M'}  ->  the node spawns ONE child, the class r (mod D*M').
  (By translation invariance the hole residue may be taken 0.)
* two holes {c mod M'} and {c' mod M''} -> two children.  Because all moduli in E are even,
  the ROOT (D=1) necessarily needs one hole in each parity unless one whole parity is covered
  outright; the two-hole root is the cheap option (weight ~1 instead of ~1.35+1).

The global modulus set is the union over nodes of {D*f}; distinctness is enforced globally.

This driver: (a) solves the root with two holes, (b) chains each child down, choosing at each
node a step modulus M' and looking ahead for a node that a Selfridge block {2,3,4,6,12} closes.

CONCLUSION: printed / written to JSON; recorded in attempts/route-B-recursive/FINDINGS.md
"""
import argparse, json, os, subprocess, sys
from fractions import Fraction
from math import gcd
from sympy import isprime, factorint

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "B_node")

SELFRIDGE = [(2, 0), (3, 1), (4, 3), (6, 5), (12, 9)]


def divisors(n):
    ds = [1]
    for p, a in factorint(n).items():
        ds = [d * p ** i for d in ds for i in range(a + 1)]
    return sorted(ds)


def pool(D, M, used=(), fmin=2, fmax=None):
    us = set(used)
    out = []
    for f in divisors(M):
        if f < fmin:
            continue
        if fmax and f > fmax:
            continue
        n = D * f
        if n < 4 or n in us:
            continue
        if isprime(n + 1):
            out.append(f)
    return out


def solve_node(D, M, P, holes=(), restarts=200, anneal=0, seed=1, target=0,
               exact=False, verbose=False):
    """returns (uncovered, [(f,b)...])"""
    lines = [str(M), str(len(holes))]
    for mp, c in holes:
        lines.append(f"{mp} {c % mp}")
    lines.append(str(len(P)))
    lines.append(" ".join(map(str, P)))
    inp = "\n".join(lines) + "\n"
    args = [BIN, "--restarts", str(restarts), "--anneal", str(anneal),
            "--seed", str(seed), "--target", str(target)]
    if exact:
        args.append("--exact")
    if not verbose:
        args.append("--quiet")
    r = subprocess.run(args, input=inp, capture_output=True, text=True)
    best = None
    cert = []
    incert = False
    for ln in r.stdout.split("\n"):
        if ln.startswith("BEST"):
            best = int(ln.split()[1])
        if ln.startswith("EXACT"):
            if "UNSAT" in ln:
                return (-1, [])
        if ln.startswith("CERT"):
            incert = True
            continue
        if incert and ln.strip():
            a, b = ln.split()
            cert.append((int(a), int(b)))
    if best is None:
        sys.stderr.write(r.stdout + r.stderr)
    return best, cert


def verify_node(M, holes, cert):
    """exhaustive: every residue of Z/M outside the holes must be covered"""
    cov = bytearray(M)
    for mp, c in holes:
        for x in range(c % mp, M, mp):
            cov[x] = 1
    for f, b in cert:
        assert M % f == 0, (f, M)
        for x in range(b % f, M, f):
            cov[x] = 1
    return M - sum(cov)


def selfridge_closable(D):
    return all(isprime(D * m + 1) for m, _ in SELFRIDGE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, required=True)
    ap.add_argument("--hole", action="append", default=[],
                    help="Mprime:c  (repeatable)")
    ap.add_argument("--restarts", type=int, default=200)
    ap.add_argument("--anneal", type=int, default=0)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--exclude", type=str, default="")
    ap.add_argument("--D", type=int, default=1)
    ap.add_argument("--json", type=str, default="")
    a = ap.parse_args()
    holes = []
    for h in a.hole:
        mp, c = h.split(":")
        holes.append((int(mp), int(c)))
    ex = [int(t) for t in a.exclude.split(",") if t.strip()]
    P = pool(a.D, a.L, used=ex, fmin=4 if a.D == 1 else 2)
    bud = sum(Fraction(1, f) for f in P)
    need = 1 - sum(Fraction(1, mp) for mp, _ in holes)
    print(f"NODE D={a.D}  M={a.L} = {factorint(a.L)}")
    print(f"  pool |P|={len(P)}  budget={float(bud):.5f}   holes={holes} "
          f"(uncovered target density {float(sum(Fraction(1,mp) for mp,_ in holes)):.5f})")
    print(f"  necessary: budget >= {float(need):.5f}  -> "
          f"{'OK' if bud > need else 'FAILS'}")
    u, cert = solve_node(a.D, a.L, P, holes, a.restarts, a.anneal, a.seed, verbose=True)
    print(f"  search: uncovered = {u}")
    if cert:
        chk = verify_node(a.L, holes, cert)
        w = sum(Fraction(1, f) for f in cert and [c[0] for c in cert])
        print(f"  independent verification: uncovered = {chk}, moduli used = {len(cert)}, "
              f"weight = {float(w):.5f}")
        if a.json:
            json.dump({"D": a.D, "M": a.L, "holes": holes, "cert": cert,
                       "uncovered": chk}, open(a.json, "w"))
            print(f"  wrote {a.json}")


if __name__ == "__main__":
    main()
