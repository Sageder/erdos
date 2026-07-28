"""theory_checks.py — machine checks for the structural propositions of route R16-tau.

Checks:
 (1) LEVEL DECOMPOSITION.  For any linear order on [1..N]: the monotone 4-APs with
     v3(d) = v and x = c (mod 3^v) are exactly the images, under y |-> c + 3^v y, of the
     monotone 4-APs with 3 not dividing e of the induced order on {n = c mod 3^v}.
     Hence "monotone-4-AP-free" decomposes into one LEVEL-0 PROBLEM per (v,c), and the
     family is coherent: level (v+1, c+3^v r) is the restriction of level (v,c) to
     y = r (mod 3).
 (2) PROP R1 (LSD rigidity).  Any order deciding every pair at its lowest differing
     base-3 level (context-dependent priorities allowed) puts a whole residue class
     before a fixed value: pos_[1..N](z) grows linearly in N.  Measured for tau.
 (3) PROP R2 (per-level override density).  In tau, for every level l and context c,
     the tau-down-set of any element of S_{l,c} inside S_{l,c} is infinite: measured.
 (4) tau-CONVEXITY.  Every tau-convex set with >= 2 elements is infinite and densely
     ordered by tau (so no family of reversed tau-convex pieces can have order type
     omega).  Measured: number of n <= M strictly tau-between two given values.
"""

import sys
import random
sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from taulib import Tau, prio_const, v3, dig3, mono4_witnesses


def level_decomposition_check(N=90, trials=25, seed=11):
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        perm = list(range(1, N + 1))
        rng.shuffle(perm)
        pos = {v: i for i, v in enumerate(perm)}
        # direct: all monotone 4-APs, grouped by (v3(d), x mod 3^v)
        direct = set()
        for d in range(1, (N - 1) // 3 + 1):
            for x in range(1, N - 3 * d + 1):
                p = [pos[x + k * d] for k in range(4)]
                if p[0] < p[1] < p[2] < p[3]:
                    direct.add((x, d, 1))
                elif p[0] > p[1] > p[2] > p[3]:
                    direct.add((x, d, -1))
        # via decomposition
        viadec = set()
        v = 0
        while 3 ** v <= N:
            for c in range(3 ** v):
                S = [n for n in range(1, N + 1) if n % 3 ** v == c % 3 ** v]
                if len(S) < 4:
                    continue
                sub = sorted(S, key=lambda n: pos[n])
                w = mono4_witnesses(sub, dfilter=lambda dd: dd % 3 ** v == 0
                                    and (dd // 3 ** v) % 3 != 0)
                for (x, d, o) in w:
                    viadec.add((x, d, o))
            v += 1
        if direct != viadec:
            bad += 1
            print("   DECOMP MISMATCH", sorted(direct ^ viadec)[:5])
    print(f" (1) level decomposition: {trials} random orders on [1..{N}], "
          f"{'OK' if bad == 0 else str(bad)+' mismatches'}")

    # coherence (d): restriction of (v,c) to y = r mod 3 is (v+1, c+3^v r)
    ok = True
    for v in (0, 1, 2):
        for c in range(3 ** v):
            for r in range(3):
                A = set(n for n in range(1, N + 1) if n % 3 ** v == c)
                A = set(n for n in A if (n // 3 ** v) % 3 == r)
                B = set(n for n in range(1, N + 1) if n % 3 ** (v + 1) == (c + 3 ** v * r))
                ok &= (A == B)
    print(f"     coherence of the (v,c) family: {'OK' if ok else 'FAIL'}")


def prop_R1_measure():
    t = Tau(prio_const((0, 1, 2)))
    print(" (2) Prop R1: position of value 2 in tau restricted to [1..N] "
          "(all multiples of 3 come first):")
    for N in (81, 243, 729, 2187, 6561):
        perm = t.sort(range(1, N + 1))
        p = perm.index(2) + 1
        print(f"     N={N:6d}  pos(2)={p:6d}   pos(2)/N={p/N:.4f}")


def prop_R2_measure(M=20000):
    t = Tau(prio_const((0, 1, 2)))
    print(" (3) Prop R2: |{y in S_{l,c}, y <_tau z}| for z the pr-max class, "
          f"counted inside [1..{M}]:")
    for l in (0, 1, 2, 3):
        for c in ([0] if l == 0 else [0, 1]):
            S = [n for n in range(1, M + 1) if n % 3 ** l == c % 3 ** l]
            x1, x2, x3 = t.x123(l, c)
            zs = [n for n in S if dig3(n, l) == x3]
            if not zs:
                continue
            z = zs[len(zs) // 2]
            below = sum(1 for y in S if y != z and t.before(y, z))
            print(f"     l={l} c={c}: |S|={len(S):6d}  z={z:6d}  "
                  f"#tau-predecessors of z in S = {below}")


def tau_convexity_measure(M=30000, trials=8, seed=3):
    t = Tau(prio_const((0, 1, 2)))
    rng = random.Random(seed)
    print(" (4) tau-convexity: # of n<=M strictly tau-between two random values "
          "(a tau-convex set containing both must contain all of them):")
    for _ in range(trials):
        u, w = rng.randint(1, 400), rng.randint(1, 400)
        if u == w:
            continue
        if not t.before(u, w):
            u, w = w, u
        cnt = sum(1 for n in range(1, M + 1)
                  if n != u and n != w and t.before(u, n) and t.before(n, w))
        print(f"     between {u:4d} and {w:4d}: {cnt:6d} values in [1..{M}]")


if __name__ == "__main__":
    level_decomposition_check()
    print()
    prop_R1_measure()
    print()
    prop_R2_measure()
    print()
    tau_convexity_measure()
