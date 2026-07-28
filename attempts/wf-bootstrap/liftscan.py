#!/usr/bin/env python3
"""
liftscan.py -- THE LIFT PROBLEM.

    Given a rational q > 0 and a threshold T, decide whether q is the
    reciprocal sum of a LEGAL system S (no isolated point) with min(S) >= T
    and max(S) <= N, for increasing N.

Motivation (see final report):  by the Reduction Lemma, every BLOCKWISE
sum-preserving map is a block-replacement rule  B |-> psi(B)  with
Sigma(psi(B)) = Sigma(B); such a rule raises the minimum iff every block value
q = H(a,b) is "liftable" above the current minimum.  So the entire class of
blockwise maps is decided by the LIFT problem.

Everything is exact: universe.py's RULE A + legality fixpoint (proved sound),
then route-E's search.c engine (exact integer arithmetic, 128-bit), then an
independent re-verification with fractions.Fraction here.

usage: liftscan.py u v T Nlo Nhi step [nsol] [banfile]
prints one line per N:  either SOL ... or  NONE (exhaustive, node count).
"""
import sys, subprocess, os
from fractions import Fraction
import universe2 as UV

HERE = os.path.dirname(os.path.abspath(__file__))


def legal(S):
    s = set(S)
    return all((n - 1 in s) or (n + 1 in s) for n in s)


def check(S, q, T):
    assert len(set(S)) == len(S)
    assert min(S) >= T
    assert legal(S)
    assert sum(Fraction(1, n) for n in S) == q
    return True


def run(q, T, N, nsol=1, banned=frozenset(), budget=0, seed=0, verbose=True, tmo=None):
    """returns (status, systems, nodes) with status in {'EMPTY','NONE','SOL','PARTIAL'}"""
    U = UV.build(T, N, q, set(banned))
    if not U:
        return ("EMPTY", [], 0, 0)
    L = UV.lcm_of(U, q)
    if L.bit_length() >= 127:
        return ("TOOBIG", [], 0, L.bit_length())
    pf = os.path.join(HERE, "_prob_%d_%d_%d_%d.txt" % (q.numerator, q.denominator, T, N))
    with open(pf, "w") as f:
        f.write("%d %d 1 %d %d\n" % (T, N, q.numerator, q.denominator))
        f.write("0\n\n")
        f.write("%d\n" % len(U))
        f.write(" ".join(map(str, U)) + "\n")
    try:
        out = subprocess.run([os.path.join(HERE, "search"), pf, str(nsol), str(budget), str(seed)],
                             capture_output=True, text=True, timeout=tmo).stdout
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        os.unlink(pf)
        sols = []
        for line in out.splitlines():
            if line.startswith("SOL"):
                S = [int(x) for x in line.split()[1:]]
                check(S, q, T); sols.append(S)
        return (("SOL", sols, 0, L.bit_length()) if sols else ("TIMEOUT", [], 0, L.bit_length()))
    os.unlink(pf)
    sols, nodes, exhaustive = [], 0, False
    for line in out.splitlines():
        if line.startswith("SOL"):
            S = [int(x) for x in line.split()[1:]]
            check(S, q, T)
            sols.append(S)
        elif "nodes=" in line:
            for tok in line.split():
                if tok.startswith("nodes="):
                    nodes = int(tok[6:])
            if "EXHAUSTIVE" in line or "exhausted" in line:
                exhaustive = True
    if sols:
        return ("SOL", sols, nodes, L.bit_length())
    return ("NONE" if exhaustive else "PARTIAL", [], nodes, L.bit_length())


if __name__ == "__main__":
    u, v, T, Nlo, Nhi, step = (int(x) for x in sys.argv[1:7])
    nsol = int(sys.argv[7]) if len(sys.argv) > 7 else 1
    banned = frozenset(int(x) for x in open(sys.argv[8]).read().split()) if len(sys.argv) > 8 else frozenset()
    q = Fraction(u, v)
    for N in range(Nlo, Nhi + 1, step):
        st, sols, nodes, lb = run(q, T, N, nsol, banned)
        if st == "SOL":
            print("q=%s T=%d N=%d  Lbits=%d nodes=%d  SOL %s" % (q, T, N, lb, nodes, sols[0]))
            sys.stdout.flush()
            break
        print("q=%s T=%d N=%d  Lbits=%d nodes=%d  %s" % (q, T, N, lb, nodes, st))
        sys.stdout.flush()
