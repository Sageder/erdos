"""
B_drive.py -- Route B driver: build the admissible pool at a node and call ./B_node.

CLAIM TESTED
------------
For a node modulus D and a target lcm M, the admissible sub-moduli are
    P(D,M) = { f | M , f >= fmin , D*f + 1 prime }        (so that D*f lies in E)
and the node's class r (mod D) can be finished with the moduli {D*f} iff the classes
b_f (mod f) cover Z/M.  This script assembles P(D,M), reports its reciprocal budget, and
runs the search engine B_node to minimise the number of uncovered residues of Z/M.

CONCLUSION: printed; recorded in attempts/route-B-recursive/FINDINGS.md

usage:
  python3 B_drive.py --D <int> --M <int> [--exclude f1,f2,..] [--fmin 2]
                     [--restarts 200] [--anneal 0] [--target 0] [--exact] [--sanity]
"""
import argparse, subprocess, os, sys, json
from sympy import isprime, factorint

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "B_node")


def divisors(n):
    ds = [1]
    for p, a in factorint(n).items():
        ds = [d * p ** i for d in ds for i in range(a + 1)]
    return sorted(ds)


def pool(D, M, fmin=2, exclude=()):
    ex = set(exclude)
    out = []
    for f in divisors(M):
        if f < fmin or f in ex:
            continue
        if D * f < 4:
            continue
        if isprime(D * f + 1):
            out.append(f)
    return out


def run_node(M, P, restarts=200, anneal=0, target=0, exact=False, seed=1, quiet=True):
    inp = f"{M}\n0\n{len(P)}\n" + " ".join(map(str, P)) + "\n"
    args = [BIN, "--restarts", str(restarts), "--anneal", str(anneal),
            "--target", str(target), "--seed", str(seed)]
    if exact:
        args.append("--exact")
    if quiet:
        args.append("--quiet")
    r = subprocess.run(args, input=inp, capture_output=True, text=True)
    return r.stdout, r.stderr


def parse_cert(out):
    lines = out.strip().split("\n")
    best = None
    cert = []
    incert = False
    for ln in lines:
        if ln.startswith("BEST"):
            best = int(ln.split()[1])
        if ln.startswith("EXACT"):
            best = 0 if "FOUND" in ln else None
        if ln.startswith("CERT"):
            incert = True
            continue
        if incert and ln.strip():
            a, b = ln.split()
            cert.append((int(a), int(b)))
    return best, cert


def verify(M, cert):
    """exhaustive mod-M check, exact integer arithmetic, independent of the C code"""
    covered = bytearray(M)
    mods = [f for f, _ in cert]
    assert len(set(mods)) == len(mods), "moduli not distinct"
    for f, b in cert:
        assert M % f == 0, (f, M)
        for x in range(b % f, M, f):
            covered[x] = 1
    return M - sum(covered)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--D", type=int, required=True)
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--fmin", type=int, default=2)
    ap.add_argument("--exclude", type=str, default="")
    ap.add_argument("--restarts", type=int, default=200)
    ap.add_argument("--anneal", type=int, default=0)
    ap.add_argument("--target", type=int, default=0)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--exact", action="store_true")
    ap.add_argument("--json", type=str, default="")
    a = ap.parse_args()

    ex = [int(t) for t in a.exclude.split(",") if t.strip()]
    P = pool(a.D, a.M, a.fmin, ex)
    budget = sum(1.0 / f for f in P)
    print(f"D = {a.D}")
    print(f"M = {a.M}  ({factorint(a.M)})   #div={len(divisors(a.M))}")
    print(f"|P| = {len(P)}   budget = {budget:.5f}   smallest = {P[:20]}")
    if budget <= 1.0:
        print("  !! budget <= 1: this node is INFEASIBLE for this M (necessary condition fails)")
    out, err = run_node(a.M, P, a.restarts, a.anneal, a.target, a.exact, a.seed)
    best, cert = parse_cert(out)
    print(out.strip().split("\n")[0] if out.strip() else "(no output)")
    if cert:
        left = verify(a.M, cert)
        print(f"independent verification: uncovered = {left}  "
              f"(#moduli used = {len(cert)}, sum 1/f = {sum(1.0/f for f,_ in cert):.5f})")
        if a.json:
            json.dump({"D": a.D, "M": a.M, "cert": cert, "uncovered": left},
                      open(a.json, "w"))
    print(err.strip()[-2000:] if err.strip() else "")


if __name__ == "__main__":
    main()
